#!/usr/bin/env python3
"""Final verification test for structured responses across all agents"""

from agents.fraud_agent import ElderlyFraudAgentWithGemini
from agents.estate_agent import EstateAgent
from agents.family_agent import FamilyAgent
from agents.healthcare_agent import HealthcareFinanceAgent

def final_verification_test():
    print("FINAL VERIFICATION: ALL AGENTS STRUCTURED RESPONSES")
    print("="*60)
    
    test_cases = [
        {
            "agent": "Fraud",
            "class": ElderlyFraudAgentWithGemini(),
            "method": "analyze_text_for_fraud",
            "input": "Someone called saying I need to pay $200 in gift cards to unlock my social security",
            "expected_structured": True
        },
        {
            "agent": "Healthcare", 
            "class": HealthcareFinanceAgent(api_key="test"),
            "method": "analyze_text_for_healthcare",
            "input": "I got a medical bill that seems overcharged and too expensive",
            "expected_structured": True
        },
        {
            "agent": "Estate",
            "class": EstateAgent(),
            "method": "analyze_text_for_estate", 
            "input": "I need to update my power of attorney documents",
            "expected_structured": True
        },
        {
            "agent": "Family",
            "class": FamilyAgent(),
            "method": "analyze_text_for_family",
            "input": "Emergency! My grandson is in trouble and needs money sent urgently",
            "expected_structured": True
        }
    ]
    
    results = {}
    
    for test in test_cases:
        print(f"\n🔍 Testing {test['agent']} Agent")
        print("-" * 40)
        
        try:
            method = getattr(test['class'], test['method'])
            result = method(test['input'])
            response = result.get('response', '')
            
            # Check if response is structured (has multiple sections, bullet points, etc.)
            is_structured = (
                len(response) > 200 and  # Longer than basic response
                ('**' in response or '•' in response or '\n\n' in response) and  # Has formatting
                ('✅' in response or '🚨' in response or '⚠️' in response or '📋' in response)  # Has emojis
            )
            
            status = "✅ STRUCTURED" if is_structured else "❌ BASIC"
            results[test['agent']] = is_structured
            
            print(f"Status: {status}")
            print(f"Risk Level: {result.get('risk_level', 'N/A')}")
            print(f"Response Length: {len(response)} characters")
            print(f"Preview: {response[:150]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results[test['agent']] = False
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS SUMMARY:")
    print(f"{'='*60}")
    
    all_structured = True
    for agent, is_structured in results.items():
        status = "✅ Structured responses" if is_structured else "❌ Basic responses"
        print(f"{agent} Agent: {status}")
        if not is_structured:
            all_structured = False
    
    print(f"\n{'🎉' if all_structured else '⚠️'} Overall Status: {'ALL AGENTS NOW HAVE STRUCTURED RESPONSES!' if all_structured else 'Some agents still need improvement'}")
    
    if all_structured:
        print("\n🎯 SUCCESS: All WisdomWealth AI agents now provide:")
        print("   • Clear, senior-friendly structured responses")
        print("   • Organized sections with emojis and bullet points") 
        print("   • Detailed guidance and actionable steps")
        print("   • Consistent formatting across all interactions")
        print("\n👵👴 Your elderly users will now receive excellent, accessible support!")

if __name__ == "__main__":
    final_verification_test()