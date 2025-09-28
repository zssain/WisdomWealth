#!/usr/bin/env python3
"""Test script for all agents to check response quality"""

from agents.fraud_agent import ElderlyFraudAgentWithGemini
from agents.estate_agent import EstateAgent
from agents.family_agent import FamilyAgent
from agents.healthcare_agent import HealthcareFinanceAgent

def test_all_agents():
    print("TESTING ALL WISDOMWEALTH AGENTS FOR STRUCTURED RESPONSES")
    print("="*60)
    
    # Test Fraud Agent (already improved)
    print("\n🛡️ FRAUD AGENT TEST")
    print("-" * 30)
    fraud_agent = ElderlyFraudAgentWithGemini()
    fraud_result = fraud_agent.analyze_text_for_fraud("I won a lottery and need to pay fees to claim my prize")
    print(f"Risk Level: {fraud_result['risk_level']}")
    print(fraud_result['response'][:300] + "..." if len(fraud_result['response']) > 300 else fraud_result['response'])
    
    # Test Healthcare Agent (already good) 
    print("\n🏥 HEALTHCARE AGENT TEST")
    print("-" * 30)
    try:
        healthcare_agent = HealthcareFinanceAgent(api_key="test")  # Provide dummy key to avoid error
        healthcare_result = healthcare_agent.analyze_text_for_healthcare("I received a medical bill for $500 that seems too high")
        print(f"Risk Level: {healthcare_result['risk_level']}")
        print(healthcare_result['response'][:300] + "..." if len(healthcare_result['response']) > 300 else healthcare_result['response'])
    except Exception as e:
        print(f"Healthcare agent error: {e}")
        healthcare_result = {"response": "Basic response"}
    
    # Test Estate Agent
    print("\n🏛️ ESTATE AGENT TEST")
    print("-" * 30)
    estate_agent = EstateAgent()
    estate_result = estate_agent.analyze_text_for_estate("I need to update my will and power of attorney documents")
    print(f"Risk Level: {estate_result['risk_level']}")
    print(estate_result['response'])
    
    # Test Family Agent
    print("\n👨‍👩‍👧‍👦 FAMILY AGENT TEST")
    print("-" * 30)
    family_agent = FamilyAgent()
    family_result = family_agent.analyze_text_for_family("Someone called saying my grandson is in jail and needs bail money")
    print(f"Risk Level: {family_result['risk_level']}")
    print(family_result['response'])
    
    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print(f"Fraud Agent: {'✅ Structured' if len(fraud_result['response']) > 100 else '❌ Basic'}")
    print(f"Healthcare Agent: {'✅ Structured' if len(healthcare_result['response']) > 100 else '❌ Basic'}")
    print(f"Estate Agent: {'✅ Structured' if len(estate_result['response']) > 100 else '❌ Basic'}")
    print(f"Family Agent: {'✅ Structured' if len(family_result['response']) > 100 else '❌ Basic'}")

if __name__ == "__main__":
    test_all_agents()