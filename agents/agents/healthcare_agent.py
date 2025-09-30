# healthcare_agent.py - Clean, Tool-Based Healthcare Finance Agent
import google.generativeai as genai
import os
import re
from typing import Dict, List

# --- Healthcare Tools ---

def calculate_estimated_premium(age: int, coverage_amount: int, city: str = "tier2") -> dict:
    """Calculates an estimated annual health insurance premium for Indian market."""
    base_premium = 8000
    age_factor = max(0, (age - 25)) * 200  # Increase premium with age
    coverage_factor = (coverage_amount / 100000) * 800  # Scale with coverage
    city_factor = 5000 if city.lower() in ['mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'pune'] else 2500
    
    annual_premium = base_premium + age_factor + coverage_factor + city_factor
    monthly_premium = annual_premium / 12
    
    return {
        "annual_premium": f"₹{annual_premium:,.0f}",
        "monthly_premium": f"₹{monthly_premium:,.0f}",
        "coverage": f"₹{coverage_amount:,.0f}",
        "age_group": f"{age} years",
        "city_tier": city
    }

def calculate_tax_deduction(premium_amount: int, is_senior_citizen: bool = False) -> dict:
    """Calculates tax deduction under Section 80D of Indian Income Tax Act."""
    limit = 50000 if is_senior_citizen else 25000
    deduction = min(premium_amount, limit)
    
    return {
        "eligible_deduction": f"₹{deduction:,.0f}",
        "section": "80D",
        "limit": f"₹{limit:,.0f}",
        "is_senior_citizen": is_senior_citizen
    }

def get_policy_recommendations(age: int, coverage_amount: int) -> dict:
    """Provides policy recommendations based on age and coverage needs."""
    if coverage_amount <= 500000:  # Up to 5 lakh
        recommended = "Arogya Sanjeevani Policy"
        features = ["Standardized benefits", "Basic hospitalization coverage", "Affordable premiums"]
    elif coverage_amount <= 5000000:  # Up to 50 lakh
        recommended = "Star Comprehensive Insurance"
        features = ["No room rent cap", "Health check-ups included", "Personal accident cover"]
    else:  # Above 50 lakh
        recommended = "HDFC ERGO Optima Restore"
        features = ["Sum insured restoration", "Multiplier benefits", "Premium coverage"]
    
    waiting_period = "48 months" if coverage_amount <= 500000 else "36 months"
    
    return {
        "recommended_policy": recommended,
        "key_features": features,
        "waiting_period": waiting_period,
        "coverage_range": f"₹{coverage_amount:,.0f}"
    }

# --- Healthcare Finance Agent Class ---

class HealthcareFinanceAgent:
    def __init__(self, api_key: str = None):
        # Initialize Gemini API
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=api_key)
        
        # System instruction for healthcare finance
        self.system_instruction = (
            "You are an expert AI assistant from WisdomWealth for Indian healthcare finance. "
            "Your goal is to help elderly users with healthcare costs, insurance, and medical bills. "
            "When users ask about premium calculations, always use the calculate_estimated_premium tool. "
            "For tax questions, use calculate_tax_deduction tool. "
            "For policy recommendations, use get_policy_recommendations tool. "
            "Always provide clear, actionable advice suitable for seniors. "
            "Use tools whenever possible instead of making up numbers."
        )
        
        try:
            # Create model with tools
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                system_instruction=self.system_instruction,
                tools=[calculate_estimated_premium, calculate_tax_deduction, get_policy_recommendations]
            )
            self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        except Exception as e:
            # Fallback without tools
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                system_instruction=self.system_instruction
            )
            self.chat = self.model.start_chat()
    
    def analyze_text_for_healthcare(self, text: str) -> Dict:
        """Analyze text input for healthcare-related concerns using AI and tools"""
        risk_level = "LOW"
        actions = []
        
        try:
            # Send to Gemini with tools
            response = self.chat.send_message(text)
            ai_response = response.text
            
            # Determine risk level based on content
            text_lower = text.lower()
            
            if any(keyword in text_lower for keyword in ["scam", "fraud", "suspicious", "free", "medicare call"]):
                risk_level = "HIGH"
                actions.extend(["DO_NOT_SHARE", "VERIFY_INDEPENDENTLY"])
            elif any(keyword in text_lower for keyword in ["expensive", "overcharge", "high bill", "too much"]):
                risk_level = "MEDIUM"
                actions.extend(["REVIEW_BILL", "CONTACT_INSURANCE"])
            elif any(keyword in text_lower for keyword in ["premium", "calculate", "cost", "price"]):
                risk_level = "LOW"
                actions.append("CALCULATE_PREMIUM")
            
            return {
                "risk_level": risk_level,
                "response": ai_response,
                "actions": actions,
                "confidence_score": 0.9
            }
            
        except Exception as e:
            # Fallback response
            return {
                "risk_level": "LOW",
                "response": self._generate_fallback_response(text),
                "actions": ["CONTACT_SUPPORT"],
                "confidence_score": 0.5
            }
    
    def _generate_fallback_response(self, text: str) -> str:
        """Generate fallback response when AI tools fail"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ["premium", "calculate", "cost"]):
            return """💳 **HEALTHCARE PREMIUM INFORMATION** 💳

**📊 General Premium Guidelines:**

For health insurance in India:
• **Age 30-40**: ₹8,000-₹15,000 annually for ₹5 lakh coverage
• **Age 40-50**: ₹12,000-₹25,000 annually for ₹10 lakh coverage  
• **Age 50-60**: ₹20,000-₹40,000 annually for ₹10 lakh coverage

**💡 Factors Affecting Premium:**
• **Age** - Higher age = Higher premium
• **Coverage Amount** - More coverage = Higher premium
• **City** - Metro cities cost 20-30% more
• **Medical History** - Pre-existing conditions increase cost

**🔍 To Get Exact Quote:**
• Contact insurance companies directly
• Use online premium calculators
• Speak with insurance agents
• Compare multiple policies

**📞 Recommended Actions:**
• Get quotes from 3-4 insurers
• Read policy terms carefully
• Consider your family medical history
• Start early for lower premiums

Would you like help with any specific aspect of healthcare insurance?"""
        
        elif any(keyword in text_lower for keyword in ["bill", "expensive", "cost"]):
            return """🏥 **MEDICAL BILL REVIEW GUIDANCE** 🏥

**🔍 Steps to Review Your Bill:**

1. **Request Itemized Bill** - Ask for detailed breakdown
2. **Check Insurance Coverage** - Verify what should be covered
3. **Look for Errors** - Common mistakes in billing
4. **Compare with Estimates** - Match with pre-procedure quotes

**🚨 Red Flags to Watch:**
• Duplicate charges
• Services you didn't receive
• Wrong insurance information
• Unusually high amounts

**💡 Cost Reduction Strategies:**
• **Payment Plans** - Ask for installment options
• **Financial Assistance** - Many hospitals offer programs
• **Second Opinion** - For expensive procedures
• **Generic Medications** - Ask for cheaper alternatives

**📞 Who to Contact:**
• Hospital billing department
• Your insurance company
• Patient advocacy services
• Healthcare ombudsman

**✅ Your Rights:**
• Right to understand charges
• Right to contest incorrect bills
• Right to payment plans
• Right to financial assistance

Need help with a specific medical bill concern?"""
        
        else:
            return """🏥 **HEALTHCARE FINANCE GUIDANCE** 🏥

**📋 How I Can Help:**

• **Insurance Premium Calculations** - Get cost estimates
• **Medical Bill Review** - Understand and reduce costs
• **Coverage Guidance** - Choose right insurance plans
• **Tax Benefits** - Section 80D deductions
• **Healthcare Fraud Prevention** - Protect from scams

**💡 Common Healthcare Finance Topics:**

**For Insurance:**
• Premium cost estimation
• Policy comparisons
• Coverage recommendations
• Claim procedures

**For Medical Bills:**
• Bill review and verification
• Cost reduction strategies
• Payment plan options
• Insurance coverage gaps

**🔒 Fraud Prevention:**
• Medicare scam warnings
• Verify all medical calls
• Protect personal information
• Report suspicious activities

**📞 Always Remember:**
• Get written estimates before procedures
• Understand your insurance coverage
• Keep all medical records
• Ask questions about charges

What specific healthcare finance question can I help you with today?"""

# --- Usage Example ---
if __name__ == "__main__":
    agent = HealthcareFinanceAgent()
    
    # Test cases
    test_cases = [
        "Can you calculate my insurance premium for a 40 year old with 1 crore coverage?",
        "I received a medical bill for ₹50,000 that seems too high",
        "Someone called saying Medicare owes me money",
        "What are the tax benefits for health insurance?"
    ]
    
    for test in test_cases:
        print(f"\n{'='*50}")
        print(f"Test: {test}")
        print(f"{'='*50}")
        result = agent.analyze_text_for_healthcare(test)
        print(f"Risk Level: {result['risk_level']}")
        print(f"Actions: {result['actions']}")
        print(f"Response:\n{result['response']}")