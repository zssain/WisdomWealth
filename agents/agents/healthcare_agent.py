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
        
        text_lower = text.lower()
        
        # Check if this is a premium calculation request
        if any(keyword in text_lower for keyword in ["calculate", "premium", "cost", "price"]) and any(keyword in text_lower for keyword in ["insurance", "coverage", "policy"]):
            # Extract age and coverage for direct calculation
            try:
                import re
                age_match = re.search(r'(\d+)\s*year', text_lower)
                coverage_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|crore)', text_lower)
                
                age = int(age_match.group(1)) if age_match else 40
                # Cap age at reasonable limits
                if age > 100:
                    age = 40  # Default for unrealistic ages
                
                if coverage_match:
                    coverage_text = coverage_match.group(0).lower()
                    coverage_num = float(coverage_match.group(1))
                    if 'crore' in coverage_text:
                        coverage_amount = int(coverage_num * 10000000)  # Convert crore to rupees
                    elif 'lakh' in coverage_text:
                        coverage_amount = int(coverage_num * 100000)   # Convert lakh to rupees
                    else:
                        coverage_amount = 1000000  # Default 10 lakh
                else:
                    coverage_amount = 1000000  # Default 10 lakh
                
                # Calculate premium directly using our tool
                premium_data = calculate_estimated_premium(age, coverage_amount, "tier2")
                
                response = f"""💳 **HEALTH INSURANCE PREMIUM CALCULATION** 💳

**📊 For a {age}-year-old with ₹{coverage_amount/10000000:.1f} Crore Coverage:**

**💰 Estimated Premium:**
• **Annual Premium**: {premium_data['annual_premium']}
• **Monthly Premium**: {premium_data['monthly_premium']}

**📈 Premium Breakdown:**
• **Base Premium**: ₹8,000
• **Age Factor**: {max(0, (age - 25)) * 200:,.0f} (increases with age)
• **Coverage Factor**: ₹{(coverage_amount / 100000) * 800:,.0f} (based on coverage amount)
• **City Factor**: ₹2,500 (Tier-2 city rates)

**💡 Factors Affecting Your Premium:**

• **Age**: {age} years - {'Higher age increases premium' if age > 40 else 'Good age for affordable rates'}
• **Coverage**: ₹{coverage_amount/10000000:.1f} Crore - {'Excellent high coverage' if coverage_amount >= 5000000 else 'Good coverage amount'}
• **City**: Metro cities cost ₹2,500 more annually
• **Medical History**: Pre-existing conditions may increase cost
• **Lifestyle**: Non-smoker discounts available (5-15%)

**🏥 Coverage Benefits at This Level:**
• **ICU Coverage**: Up to ₹{coverage_amount/10000000:.1f} Crore
• **Surgery Coverage**: All major procedures covered
• **Hospitalization**: Room rent, nursing, medicines
• **Pre/Post Hospitalization**: 30/60 days coverage
• **Emergency Ambulance**: Usually included
• **Health Check-ups**: Annual preventive care

**💰 Cost Reduction Tips:**
• **Higher Deductible**: Choose ₹25,000-₹50,000 deductible (save 10-20%)
• **Co-payment Option**: 10-20% sharing reduces premium
• **Annual Payment**: Save 5-10% vs monthly payments
• **Family Floater**: More cost-effective for families
• **Corporate Plans**: Check if employer offers group rates

**📋 Tax Benefits (Section 80D):**
• **Deduction Limit**: ₹25,000 for individuals under 60
• **Senior Citizens**: ₹50,000 deduction limit
• **Actual Tax Saving**: 20-30% of premium amount

**⚠️ Important Considerations:**
• **Waiting Period**: 2-4 years for pre-existing conditions
• **Network Hospitals**: Verify preferred hospitals in network
• **Claim Settlement Ratio**: Choose insurers with 95%+ ratio
• **Premium Increase**: Expect 10-15% annual increases

**🎯 Recommended Next Steps:**
1. **Compare Quotes**: Get quotes from 3-4 top insurers
2. **Read Policy Terms**: Understand exclusions and waiting periods
3. **Health Declaration**: Be completely honest about medical history
4. **Start Soon**: Premiums increase significantly with age

**🏆 Top Insurers for ₹1 Crore Coverage:**
• **HDFC ERGO**: Optima Restore plan
• **Star Health**: Comprehensive plan
• **Care Health**: Supreme plan
• **ICICI Lombard**: Complete Health plan

Would you like me to explain any specific aspect of this premium calculation or help you compare different coverage options?"""

                risk_level = "LOW"
                actions.append("CALCULATE_PREMIUM")
                
                return {
                    "risk_level": risk_level,
                    "response": response,
                    "actions": actions,
                    "confidence_score": 0.95
                }
                
            except Exception as e:
                # If direct calculation fails, fall back to AI
                pass
        
        # Try AI with tools for other healthcare questions
        try:
            response = self.chat.send_message(text)
            ai_response = response.text
            
            # Determine risk level based on content
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