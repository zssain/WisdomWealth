# healthcare_agent.py
import google.generativeai as genai
import os
from typing import Dict, List

# Mock Database
POLICY_DATABASE = {
    "arogya sanjeevani": {
        "policy_name": "Arogya Sanjeevani Policy",
        "coverage_range": "₹1 Lakh to ₹5 Lakhs",
        "pre_existing_disease_waiting_period": "48 months",
        "key_features": ["Standardized benefits across all insurers", "Covers hospitalization, pre and post-hospitalization costs", "Cumulative bonus available."]
    },
    "star comprehensive": {
        "policy_name": "Star Comprehensive Insurance Policy",
        "coverage_range": "₹5 Lakhs to ₹1 Crore",
        "pre_existing_disease_waiting_period": "36 months",
        "key_features": ["No cap on room rent", "Covers health check-ups", "Personal accident cover included."]
    },
    "hdfc ergo optima restore": {
        "policy_name": "HDFC ERGO Optima Restore",
        "coverage_range": "₹5 Lakhs to ₹50 Lakhs",
        "pre_existing_disease_waiting_period": "36 months",
        "key_features": ["Restores 100% of sum insured if exhausted", "Multiplier benefit increases sum insured for claim-free years", "Daily hospital cash benefit."]
    }
}

def calculate_estimated_premium(age: int, city: str, coverage_amount: int) -> dict:
    """Calculates an estimated annual health insurance premium."""
    base_premium = 5000
    age_factor = (age - 20) * 150
    city_tier_factor = 3000 if city.lower() in ['mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'pune'] else 1500
    coverage_factor = coverage_amount / 100000 * 1000
    estimated_premium = base_premium + age_factor + city_tier_factor + coverage_factor
    return {"estimated_premium": f"₹{estimated_premium:,.2f} per year"}

def calculate_tax_deduction(premium_amount: int, is_senior_citizen: bool = False) -> dict:
    """Calculates the potential tax deduction under Section 80D of the Indian Income Tax Act."""
    limit = 50000 if is_senior_citizen else 25000
    deduction = min(premium_amount, limit)
    return {"eligible_deduction": f"₹{deduction:,.2f}", "limit_under_80D": f"₹{limit:,.2f}"}

def lookup_policy_details(policy_name: str) -> dict:
    """Looks up the details for a specific health insurance policy from the simple database."""
    policy_key = policy_name.lower().strip()
    if policy_key in POLICY_DATABASE:
        return POLICY_DATABASE[policy_key]
    else:
        return {"error": f"Policy '{policy_name}' not found in the database."}

class HealthcareFinanceAgent:
    def __init__(self, api_key: str = None):
        # Initialize Gemini API
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=api_key)
        
        # System prompt for healthcare finance
        self.system_instruction = (
            "You are an expert AI assistant from WisdomWealth for healthcare finance. "
            "Your goal is to help elderly users understand medical bills, insurance options, and healthcare costs. "
            "Always provide clear, simple explanations suitable for seniors. "
            "When analyzing medical bills, focus on potential overcharges, insurance coverage gaps, and cost-saving opportunities."
        )
        
        try:
            # Try with system_instruction first (newer versions)
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                system_instruction=self.system_instruction
            )
        except TypeError:
            # Fallback for older versions without system_instruction
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp'
            )
        
        self.chat = self.model.start_chat()
    
    def analyze_text_for_healthcare(self, text: str) -> Dict:
        """Analyze text input for healthcare-related concerns"""
        risk_level = "LOW"
        actions = []
        response = ""
        
        text_lower = text.lower()
        
        # Healthcare fraud indicators
        if any(keyword in text_lower for keyword in ["medical bill", "hospital charge", "insurance claim"]):
            if any(keyword in text_lower for keyword in ["overcharge", "expensive", "high cost", "too much"]):
                risk_level = "MEDIUM"
                actions.extend(["REVIEW_BILL", "CONTACT_INSURANCE"])
                response = self._generate_bill_review_response()
        
        # Insurance questions
        elif any(keyword in text_lower for keyword in ["premium", "policy", "coverage", "insurance"]):
            risk_level = "LOW"
            actions.append("CALCULATE_PREMIUM")
            response = self._generate_insurance_guidance_response()
        
        # Medical scam indicators
        elif any(keyword in text_lower for keyword in ["medicare", "free", "government program"]) and any(keyword in text_lower for keyword in ["social security", "personal information", "verify"]):
            risk_level = "HIGH"
            actions.extend(["DO_NOT_SHARE", "ALERT_FAMILY"])
            response = self._generate_medicare_scam_response()
        
        # Use AI for more complex analysis
        if not response:
            try:
                ai_prompt = f"""
                {self.system_instruction}
                
                Analyze this healthcare-related question from an elderly user: "{text}"
                
                Format your response in a clear, structured way for seniors:

                **🏥 HEALTHCARE FINANCE GUIDANCE**

                **📋 What This Means:**
                [Brief, simple explanation]

                **💡 Key Points:**
                • [Point 1 - use bullet points for easy reading]
                • [Point 2]
                • [Point 3]

                **🔍 What You Should Do:**
                1. [First action step]
                2. [Second action step]  
                3. [Third action step]

                **⚠️ Important Reminders:**
                • Never give personal information over the phone
                • Always verify with your insurance company directly
                • Keep records of all medical bills and insurance communications

                **📞 Need More Help?**
                Consider talking to:
                • Your insurance company directly
                • A trusted family member
                • Your doctor's billing office

                Keep the language simple, use large sections with clear headers, and focus on actionable advice.
                """
                
                ai_response = self.chat.send_message(ai_prompt)
                response = ai_response.text
                risk_level = "LOW"
                actions = ["CONSULT_HEALTHCARE"]
                
            except Exception as e:
                response = """
**🏥 HEALTHCARE FINANCE GUIDANCE**

**📋 What This Means:**
I'm here to help you understand medical bills, insurance questions, and healthcare costs.

**💡 Key Points:**
• Healthcare can be confusing, but you have rights
• Always review your bills carefully
• Your insurance should cover many services

**🔍 What You Should Do:**
1. Ask questions if you don't understand something
2. Keep all your medical and insurance paperwork organized
3. Don't be afraid to call for clarification

**📞 Need More Help?**
Feel free to ask me specific questions about:
• Medical bills you've received
• Insurance coverage questions  
• Medicare or health insurance options
                """
        
        return {
            "risk_level": risk_level,
            "response": response,
            "actions": actions,
            "agent_type": "healthcare",
            "confidence_score": 0.8
        }
    
    def analyze_medical_bill(self, bill_text: str) -> Dict:
        """Analyze medical bill for overcharges and issues"""
        prompt = f"""
        {self.system_instruction}
        
        Analyze this medical bill for an elderly patient and format the response clearly:

        **💰 MEDICAL BILL REVIEW**

        **📋 Bill Summary:**
        [Brief overview of what the bill is for]

        **✅ What Looks Normal:**
        • [List normal charges]
        • [Standard procedures/costs]

        **⚠️ What Needs Review:**
        • [Potential issues or high charges]
        • [Missing insurance coverage]
        • [Duplicate charges if any]

        **🔍 Recommended Actions:**
        1. [First specific step to take]
        2. [Second step - like calling insurance]
        3. [Third step - like requesting itemized bill]

        **💡 Money-Saving Tips:**
        • [How to reduce costs]
        • [Insurance benefits to check]
        • [Payment plan options]

        **📞 Who to Contact:**
        • Insurance company: [specific department]
        • Hospital billing: [when to call]
        • Medicare/Medicaid: [if applicable]

        Medical Bill Text: {bill_text}
        
        Keep explanations simple and actionable for elderly patients.
        """
        
        try:
            response = self.chat.send_message(prompt)
            return {
                "analysis": response.text,
                "risk_level": "MEDIUM",
                "actions": ["REVIEW_CHARGES", "CONTACT_PROVIDER"]
            }
        except Exception as e:
            return {
                "analysis": f"Unable to analyze bill: {str(e)}",
                "risk_level": "LOW",
                "actions": ["MANUAL_REVIEW"]
            }
    
    def get_insurance_advice(self, query: str) -> Dict:
        """Get insurance advice and calculations"""
        try:
            structured_prompt = f"""
            {self.system_instruction}
            
            Answer this insurance question in a clear, senior-friendly format:

            **🛡️ INSURANCE GUIDANCE**

            **📋 Your Question:**
            {query}

            **💡 Simple Answer:**
            [Clear, direct answer in plain language]

            **🔍 Key Things to Know:**
            • [Important point 1]
            • [Important point 2] 
            • [Important point 3]

            **📋 Steps You Can Take:**
            1. [First actionable step]
            2. [Second step]
            3. [Third step]

            **💰 Cost Considerations:**
            • [Premium information if relevant]
            • [Deductible explanations if relevant]
            • [Coverage details if relevant]

            **⚠️ Watch Out For:**
            • [Common pitfalls or scams related to this topic]
            • [Red flags to avoid]

            **📞 Next Steps:**
            • [Who to contact]
            • [What information to have ready]
            • [When to take action]

            Use simple language and focus on practical advice for seniors.
            """
            
            response = self.chat.send_message(structured_prompt)
            return {
                "advice": response.text,
                "risk_level": "LOW",
                "actions": ["REVIEW_OPTIONS"]
            }
        except Exception as e:
            return {
                "advice": """
**🛡️ INSURANCE GUIDANCE**

**📋 Technical Issue:**
I'm having trouble accessing detailed insurance information right now.

**💡 General Advice:**
• Keep all your insurance documents in one safe place
• Review your coverage annually during open enrollment
• Don't hesitate to call your insurance company with questions

**📞 Direct Help:**
• Contact your insurance company directly using the number on your card
• Ask to speak with a senior specialist if available
• Have your member ID ready when you call

**⚠️ Stay Safe:**
• Never give personal information to unsolicited callers
• Always verify who you're speaking with
• When in doubt, hang up and call the official number

I'll try to help you again in a moment, or you can ask me a different question.
                """,
                "risk_level": "LOW",
                "actions": ["CONSULT_EXPERT"]
            }
    
    def _generate_bill_review_response(self) -> str:
        """Generate structured response for medical bill review"""
        return """🏥 **MEDICAL BILL REVIEW ASSISTANCE** 🏥

**🔍 What We'll Check Together:**

Medical bills can be confusing, but you have the right to understand every charge. Let's make sure you're only paying what you truly owe.

**📋 Common Billing Issues to Look For:**

• **Duplicate charges** - Same service billed multiple times
• **Services not received** - Charges for care you didn't get
• **Incorrect insurance processing** - Bills that should have been covered
• **Coding errors** - Wrong medical codes leading to higher costs
• **Facility fees** - Unexpected charges for using hospital facilities

**✅ Step-by-Step Review Process:**

1. **Get your paperwork together** - Gather the bill, insurance statements, and appointment records
2. **Check the dates** - Make sure all services were actually received on those dates  
3. **Compare with your insurance** - See what your plan says it covers
4. **Look for itemized details** - Ask for a detailed breakdown if it's not provided
5. **Question anything unclear** - You have the right to understand every charge

**📞 Who to Contact:**

• **Your doctor's billing office** - Call the number on the bill to ask questions
• **Your insurance company** - Use the customer service number on your card
• **Hospital financial counselor** - Ask to speak with someone who helps with billing issues
• **Medicare** - Call 1-800-MEDICARE if this involves Medicare services

**💡 Important Rights You Have:**

• You can request itemized bills showing exactly what you're paying for
• You can ask for payment plans if the bill is difficult to afford
• You can dispute charges you believe are incorrect
• You have time to review bills - don't feel pressured to pay immediately

**🛡️ Red Flags to Watch For:**

• Bills for services you know you didn't receive
• Charges that seem much higher than expected
• Pressure to pay immediately without explanation
• Refusal to provide detailed billing information

**✅ You're Taking the Right Steps:**

By reviewing your medical bills carefully, you're protecting yourself from billing errors and overcharges. Many seniors find mistakes on their medical bills, so your vigilance is important.

**Need More Help?** I can guide you through specific questions about your bill or help you understand your insurance coverage."""

    def _generate_insurance_guidance_response(self) -> str:
        """Generate structured response for insurance guidance"""
        return """💳 **HEALTHCARE INSURANCE GUIDANCE** 💳

**🤗 Understanding Your Coverage:**

Healthcare insurance can seem complicated, but I'm here to help you understand your options and make the most of your coverage.

**📋 Key Insurance Terms Made Simple:**

• **Premium** - The monthly amount you pay for insurance
• **Deductible** - What you pay before insurance starts helping
• **Co-pay** - Fixed amount you pay for doctor visits or prescriptions
• **Co-insurance** - Percentage you pay after meeting your deductible
• **Out-of-pocket maximum** - Most you'll pay in a year for covered services

**✅ Making the Most of Your Coverage:**

**For Medicare:**
• Understand Parts A, B, C, and D and what each covers
• Know your enrollment periods to avoid penalties
• Consider Medicare Supplement (Medigap) insurance for extra coverage
• Review your plan annually during Open Enrollment (October 15 - December 7)

**For All Insurance:**
• Keep your insurance card with you always
• Verify coverage before expensive procedures
• Use in-network providers when possible to save money
• Keep records of all medical expenses for tax purposes

**💰 Ways to Save Money:**

• **Generic medications** - Often much cheaper than brand names
• **Preventive care** - Many services are covered 100% to keep you healthy
• **Annual wellness visits** - Use these free checkups to catch problems early
• **Medicare benefits** - Make sure you're getting all the services you're entitled to

**📞 Getting Help When You Need It:**

• **Insurance customer service** - Call the number on your card for questions
• **SHIP counselors** - Free Medicare counseling in every state (call 1-877-839-2675)
• **Provider billing offices** - They can help verify coverage before services
• **Medicare.gov** - Official website for Medicare information and plan comparison

**🚨 Avoiding Insurance Scams:**

• Medicare will NEVER call you asking for your Medicare number
• Be suspicious of "free" medical equipment offers over the phone
• Don't give your insurance information to unsolicited callers
• Verify any insurance offers through official channels

**✅ Important Reminders:**

• Review your insurance statements (EOBs) regularly for errors
• Report suspected fraud to your insurance company immediately
• Keep a list of your medications and medical conditions updated
• Understand your appeal rights if claims are denied

**🌟 You're Taking Care of Yourself:**

Understanding your insurance helps you get better care while protecting your finances. Don't hesitate to ask questions - insurance companies are required to help you understand your coverage.

**Have Specific Questions?** Ask me about Medicare parts, prescription coverage, or help understanding a specific insurance issue."""

    def _generate_medicare_scam_response(self) -> str:
        """Generate structured response for Medicare scam warnings"""
        return """🚨 **MEDICARE SCAM ALERT** 🚨

**⚠️ IMMEDIATE DANGER:**

This has all the warning signs of a Medicare scam! Criminals specifically target seniors by pretending to be from Medicare or other government programs.

**🎯 How Medicare Scams Work:**

• **The Call:** "We're from Medicare and need to verify your information"
• **The Request:** They ask for your Medicare number, Social Security number, or bank information
• **The Urgency:** "Your benefits will be cancelled if you don't act now"
• **The Trap:** They use your information to steal your identity or submit fake claims

**🚫 What to Do RIGHT NOW:**

1. **HANG UP immediately** - Don't continue the conversation
2. **DO NOT give any personal information** - Medicare already has what they need
3. **DO NOT pay anything** - Medicare doesn't call asking for payments
4. **Block the number** - Prevent them from calling again

**📞 Important Medicare Facts:**

• **Medicare will NEVER call you** asking for your Medicare number
• **Medicare will NEVER ask for payment** over the phone
• **Medicare will NEVER threaten** to cancel your benefits for not providing information
• **Medicare communications** come by mail to your official address

**🛡️ How to Protect Yourself:**

• **Never give your Medicare number** to anyone who calls you
• **Guard your Medicare card** like a credit card - it contains sensitive information
• **Be suspicious of "free" offers** - Especially medical equipment or services
• **Verify everything** - If you're unsure, hang up and call Medicare directly at 1-800-MEDICARE

**📋 Red Flags to Watch For:**

• Calls claiming your Medicare card is "expiring" or "deactivated"
• Offers for "free" back braces, genetic testing, or other medical equipment
• Requests to "verify" your Medicare number or Social Security number
• Claims that new Medicare cards are being issued and you need to pay for one

**✅ If You Think You've Been Targeted:**

• **Call Medicare immediately** at 1-800-MEDICARE (1-800-633-4227)
• **Report to the FTC** at 1-877-FTC-HELP (1-877-382-4357)
• **Check your Medicare statements** for services you didn't receive
• **Consider a credit freeze** if you gave out personal information

**💪 You're Staying Smart:**

By being suspicious of unsolicited calls about Medicare, you're protecting yourself from criminals who prey on seniors. Your caution is exactly what keeps you safe.

**🔒 Remember:**

• When in doubt, hang up and call the official Medicare number
• Real Medicare communications come by mail, not surprise phone calls
• You never need to pay Medicare over the phone
• Trust your instincts - if something feels wrong, it probably is

**Need Help?** If you have legitimate Medicare questions, call 1-800-MEDICARE directly or ask me about specific Medicare topics."""