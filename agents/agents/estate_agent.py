# estate_agent.py
import os
import google.generativeai as genai
from typing import Dict, List
from tabulate import tabulate

class EstateAgent:
    def __init__(self, api_key: str = None, elderly_mode: bool = True):
        self.elderly_mode = elderly_mode
        
        # Initialize Gemini API
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ Warning: No Gemini API key provided for Estate Agent.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize Gemini model for Estate Agent: {e}")
            self.model = None
    
    def analyze_text_for_estate(self, text: str) -> Dict:
        """Analyze text input for estate planning concerns"""
        risk_level = "LOW"
        actions = []
        response = ""
        
        text_lower = text.lower()
        
        # Estate document keywords
        if any(keyword in text_lower for keyword in ["will", "testament", "beneficiary", "inheritance"]):
            risk_level = "MEDIUM"
            actions.extend(["UPDATE_DOCUMENTS", "CONSULT_ATTORNEY"])
            response = self._generate_document_update_response(text)
        
        # Power of attorney indicators
        elif any(keyword in text_lower for keyword in ["power of attorney", "financial decisions", "medical decisions"]):
            risk_level = "MEDIUM"
            actions.extend(["REVIEW_POA", "UPDATE_DOCUMENTS"])
            response = self._generate_power_of_attorney_response()
        
        # Scam indicators related to inheritance
        elif any(keyword in text_lower for keyword in ["inheritance", "lottery", "beneficiary"]) and any(keyword in text_lower for keyword in ["fee", "tax", "payment required"]):
            risk_level = "HIGH"
            actions.extend(["DO_NOT_PAY", "ALERT_FAMILY"])
            response = self._generate_inheritance_scam_response()
        
        # Family update requests
        elif any(keyword in text_lower for keyword in ["family", "children", "spouse", "relatives"]):
            risk_level = "LOW"
            actions.append("UPDATE_FAMILY_INFO")
            response = self._generate_family_update_response()
        
        else:
            response = self._generate_general_estate_response()
        
        return {
            "risk_level": risk_level,
            "response": response,
            "actions": actions,
            "agent_type": "estate"
        }
    
    def generate_checklist(self, profile: Dict) -> str:
        """Return a table-like checklist of document status."""
        checklist_data = [
            ["Last Will & Testament", "✅ Yes" if profile.get("last_will_update") else "❌ No",
             f"Last updated: {profile.get('last_will_update', 'N/A')}"],
            ["Power of Attorney", "✅ Yes" if profile.get("power_of_attorney") else "❌ No",
             "Allows someone to handle your finances"],
            ["Healthcare Proxy", "✅ Yes" if profile.get("healthcare_proxy") else "❌ No",
             "Names who can make medical decisions"],
            ["Trust Documents", "✅ Yes" if profile.get("trust_documents") else "❌ No",
             "Helps transfer assets smoothly"],
        ]
        
        return tabulate(checklist_data, headers=["Document", "Status", "Notes"], tablefmt="fancy_grid")
    
    def check_documents(self, profile: Dict) -> Dict:
        """Generate elderly-friendly recommendations using AI."""
        if not self.model:
            return self._basic_document_check(profile)
        
        checklist_text = self.generate_checklist(profile)
        
        base_prompt = f"""
        You are an estate planning advisor for elderly clients.
        Review this user profile: {profile}
        
        1. Summarize what documents are missing and why they matter.
        2. Suggest next steps in very simple, friendly language.
        3. Include reminders about legal risks or family benefits.
        4. Provide gentle reassurance and encouragement.
        
        Use short sentences. Use plain language. Avoid legal terms.
        Speak warmly, like explaining to a senior family member.
        """
        
        try:
            response = self.model.generate_content(base_prompt)
            recommendation_text = response.text if response and hasattr(response, 'text') else "Unable to generate recommendations at this time."
            
            # Determine risk level based on missing documents
            missing_count = sum([
                not profile.get("last_will_update"),
                not profile.get("power_of_attorney"),
                not profile.get("healthcare_proxy"),
                not profile.get("trust_documents")
            ])
            
            risk_level = "HIGH" if missing_count >= 3 else "MEDIUM" if missing_count >= 2 else "LOW"
            
            return {
                "analysis": f"📋 Estate Planning Checklist\n\n{checklist_text}\n\n---\n\n{recommendation_text}",
                "risk_level": risk_level,
                "actions": ["UPDATE_DOCUMENTS", "CONSULT_ATTORNEY"] if missing_count > 0 else ["DOCUMENTS_CURRENT"]
            }
        except Exception as e:
            return {
                "analysis": f"Unable to analyze documents: {str(e)}",
                "risk_level": "MEDIUM",
                "actions": ["MANUAL_REVIEW"]
            }
    
    def _basic_document_check(self, profile: Dict) -> Dict:
        """Basic document check without AI"""
        missing_docs = []
        if not profile.get("last_will_update"):
            missing_docs.append("Last Will & Testament")
        if not profile.get("power_of_attorney"):
            missing_docs.append("Power of Attorney")
        if not profile.get("healthcare_proxy"):
            missing_docs.append("Healthcare Proxy")
        if not profile.get("trust_documents"):
            missing_docs.append("Trust Documents")
        
        if missing_docs:
            analysis = f"⚠️ You are missing these important documents: {', '.join(missing_docs)}. These help protect you and your family."
            risk_level = "HIGH" if len(missing_docs) >= 3 else "MEDIUM"
            actions = ["UPDATE_DOCUMENTS", "CONSULT_ATTORNEY"]
        else:
            analysis = "✅ Your estate planning documents appear to be in order. Great job!"
            risk_level = "LOW"
            actions = ["DOCUMENTS_CURRENT"]
        
        return {
            "analysis": analysis,
            "risk_level": risk_level,
            "actions": actions
        }
    
    def generate_next_steps(self, profile: Dict) -> List[str]:
        """Generate a simple step-by-step plan based on missing documents and family info."""
        steps = []
        if not profile.get("last_will_update"):
            steps.append("📄 Create or update your Last Will & Testament to ensure your assets are distributed as you wish.")
        if not profile.get("power_of_attorney"):
            steps.append("💰 Set up a Power of Attorney so someone you trust can handle finances if needed.")
        if not profile.get("healthcare_proxy"):
            steps.append("🏥 Assign a Healthcare Proxy to make medical decisions on your behalf if you cannot.")
        if not profile.get("trust_documents"):
            steps.append("🏛️ Consider setting up Trust Documents to transfer assets smoothly and avoid complications.")
        
        # Personalized steps based on family
        children = profile.get("children")
        if children and children != "0":
            steps.append(f"👨‍👩‍👧‍👦 Share your wishes with your family ({children}) so everyone understands your plans.")
        
        # Gentle closing reassurance
        steps.append("✅ Take one step at a time. You're doing a great job preparing for the future!")
        
        return steps
    
    def _generate_document_update_response(self, original_text: str) -> str:
        """Generate structured response for document updates"""
        return """📋 **ESTATE DOCUMENT REVIEW NEEDED** 📋

**🎯 What This Means:**

You've mentioned important estate planning documents that may need attention. Keeping these updated is one of the best ways to protect yourself and your family.

**📄 Key Documents to Review:**

• **Last Will & Testament** - Ensures your belongings go where you want them
• **Power of Attorney** - Lets someone you trust handle finances if needed  
• **Healthcare Proxy** - Names who makes medical decisions for you
• **Trust Documents** - Can help avoid probate and protect assets

**✅ Next Steps Made Simple:**

1. **Gather your current documents** - Look for wills, powers of attorney, and any trust papers
2. **Review the details** - Check if names, addresses, and wishes are still current
3. **Note what's missing** - Identify which documents you don't have yet
4. **Schedule a consultation** - Consider meeting with an elder law attorney

**💡 Why This Matters:**

• Without proper documents, the court decides who handles your affairs
• Outdated documents can cause family disputes and delays
• Proper planning gives you control and peace of mind
• It protects your family from unnecessary stress and costs

**🤝 You're Taking Smart Action:**

By thinking about these documents now, you're being responsible and caring. Many people put this off, but you're taking the right steps to protect yourself and your loved ones.

**Need Help?** I can guide you through understanding what each document does and help you prepare questions for your attorney."""

    def _generate_power_of_attorney_response(self) -> str:
        """Generate structured response for power of attorney concerns"""
        return """⚖️ **POWER OF ATTORNEY GUIDANCE** ⚖️

**🔑 What Power of Attorney Means:**

A Power of Attorney (POA) is a legal document that lets someone you trust make decisions for you if you can't do it yourself. It's like giving someone the keys to help you when you need it most.

**📋 Types You Should Know:**

• **Financial POA** - Handles money matters, paying bills, managing accounts
• **Healthcare POA** - Makes medical decisions, talks to doctors for you  
• **Durable POA** - Stays in effect even if you become unable to make decisions
• **Limited POA** - Only covers specific things for a specific time

**⚠️ Important Protections:**

• **Choose someone you completely trust** - This person will have significant power
• **Pick a backup person** - In case your first choice can't serve
• **Set clear limits** - Specify what they can and cannot do
• **Review regularly** - Update if relationships or circumstances change

**🛡️ Safety Tips:**

• Never sign a POA under pressure or when you feel rushed
• Read everything carefully and ask questions about anything unclear
• Consider having a lawyer explain the document to you
• Keep the original document in a safe but accessible place

**✅ Action Steps:**

1. **Think about who you trust most** - Consider their honesty, availability, and ability
2. **Decide what powers to give** - You can limit what they're allowed to do
3. **Consult an attorney** - They can explain your state's laws and requirements
4. **Tell your family** - Let them know who you've chosen and why

**💪 You're Being Smart:**

Planning for power of attorney shows wisdom and care for your future. It ensures someone you trust can help you when needed, rather than leaving it to the courts to decide."""

    def _generate_inheritance_scam_response(self) -> str:
        """Generate structured response for inheritance scam warnings"""
        return """🚨 **INHERITANCE SCAM ALERT** 🚨

**⚠️ IMMEDIATE DANGER:**

This has all the warning signs of an inheritance scam! These fraudsters specifically target seniors with fake stories about windfalls, inheritances, or lottery winnings.

**🎯 How These Scams Work:**

• **The Hook:** "You've inherited money" or "You've won a prize"
• **The Twist:** "You need to pay fees/taxes first to claim it"
• **The Pressure:** "Act quickly or you'll lose this opportunity"
• **The Trap:** Once you pay, they disappear with your money

**🚫 What to Do RIGHT NOW:**

1. **DO NOT send any money** - Real inheritances don't require upfront payments
2. **DO NOT give personal information** - No Social Security numbers, bank details, etc.
3. **HANG UP immediately** - Don't continue the conversation
4. **Block the contact** - Prevent them from calling/emailing again

**📞 Who to Contact:**

• **Your bank** - Alert them about potential fraud attempts
• **Local police** - File a report about the scam attempt  
• **FTC** - Call 1-877-FTC-HELP (1-877-382-4357) to report
• **Family members** - Let them know about this attempt

**💡 How to Spot Future Scams:**

• Real inheritances come through attorneys with proper legal documents
• Legitimate organizations don't demand payment via gift cards or wire transfers
• You would already know if a wealthy relative left you money
• Government agencies don't contact you about unclaimed inheritances by phone

**🛡️ Protect Yourself:**

• Be suspicious of any unexpected "good news" requiring payment
• Verify any inheritance claims through official channels
• Never feel pressured to act immediately
• Trust your instincts - if it sounds too good to be true, it probably is

**✅ You Did the RIGHT Thing:**

By checking with me instead of acting immediately, you've protected yourself from becoming a victim. Your caution is exactly what kept you safe!"""

    def _generate_family_update_response(self) -> str:
        """Generate structured response for family information updates"""
        return """👨‍👩‍👧‍👦 **FAMILY INFORMATION UPDATE** 👨‍👩‍👧‍👦

**📝 Keeping Family Details Current:**

Updating family information in your estate planning is smart and caring. When details are current, your wishes can be carried out smoothly and your loved ones are protected.

**👥 Information to Keep Updated:**

• **Names and addresses** - Children, grandchildren, beneficiaries
• **Relationship changes** - Marriages, divorces, new family members
• **Contact information** - Phone numbers, email addresses
• **Financial changes** - New accounts, closed accounts, changed institutions

**📋 Documents That Need Family Updates:**

• **Last Will & Testament** - Names of beneficiaries and their shares
• **Power of Attorney** - Who you trust to make decisions
• **Healthcare Proxy** - Who speaks for you in medical situations  
• **Insurance policies** - Beneficiary designations
• **Retirement accounts** - 401k and IRA beneficiaries

**✅ Steps to Update Family Information:**

1. **Make a list** - Write down all family members and their current details
2. **Gather your documents** - Collect wills, POAs, insurance policies, accounts
3. **Check each document** - See what information is outdated
4. **Contact the right people** - Attorney for legal documents, banks for accounts
5. **Keep records** - Save copies of all updates in a safe place

**💡 Why This Matters:**

• Outdated information can delay inheritance distribution
• Wrong addresses mean family members might not be notified
• Changed relationships need to be reflected in your wishes
• Current information prevents family confusion and disputes

**🤝 Staying Connected:**

• Consider sharing your estate plans with adult family members
• Let them know where important documents are kept
• Review and update information every few years or after major life changes
• Make sure your chosen decision-makers know their responsibilities

**🌟 You're Taking Care of Your Family:**

By keeping family information updated, you're showing love and consideration for those who matter most to you. This thoughtfulness will make difficult times easier for your loved ones."""

    def _generate_general_estate_response(self) -> str:
        """Generate structured general estate planning response"""
        return """🏛️ **ESTATE PLANNING GUIDANCE** 🏛️

**🤗 Welcome! I'm Here to Help:**

Estate planning might sound complicated, but it's really about making sure you stay in control of your life and protect the people you care about most.

**📋 What Estate Planning Covers:**

• **Your belongings and money** - Who gets what when you're gone
• **Medical decisions** - Who speaks for you if you can't
• **Financial decisions** - Who handles your money if needed
• **Final wishes** - How you want things handled
• **Family protection** - Avoiding problems and costs for loved ones

**✅ Common Documents You Might Need:**

• **Last Will & Testament** - Directs how your belongings are distributed
• **Power of Attorney** - Lets someone handle finances for you
• **Healthcare Proxy** - Names who makes medical decisions
• **Living Will** - States your wishes about life support
• **Trust Documents** - Can help avoid probate and protect assets

**💡 Benefits of Proper Planning:**

• **You stay in control** - Your wishes are followed, not what courts decide
• **Family harmony** - Clear instructions prevent disagreements
• **Cost savings** - Proper planning avoids expensive legal processes
• **Peace of mind** - Everything is organized and ready
• **Privacy protection** - Some documents keep your affairs private

**🎯 Getting Started is Easier Than You Think:**

1. **Think about your goals** - What matters most to you?
2. **List your assets** - Home, accounts, belongings, insurance
3. **Consider your family** - Who do you trust? Who needs protection?
4. **Start with basics** - Will and Power of Attorney are good first steps
5. **Get professional help** - An elder law attorney can guide you

**📞 Questions to Think About:**

• Who would you trust to handle your finances if you couldn't?
• What are your wishes about medical care and life support?
• How do you want your belongings distributed?
• Are there any special needs family members to consider?

**🌟 You're Being Wise:**

Taking time to think about estate planning shows you care about your future and your family's well-being. Every step you take now makes things easier later.

**Need Specific Help?** Just ask me about any estate planning topic - wills, powers of attorney, trusts, or any concerns you have. I'm here to make this as simple as possible for you."""