#!/usr/bin/env python3
"""Test script for fraud agent structured responses"""

from agents.fraud_agent import ElderlyFraudAgentWithGemini

def test_fraud_agent():
    agent = ElderlyFraudAgentWithGemini()
    
    # Test high-risk scenario
    print("=== HIGH RISK TEST ===")
    high_risk_text = "I received a call saying I won a $50,000 prize and I need to pay $500 in gift cards to claim it. They said this is urgent and I have 24 hours."
    result = agent.analyze_text_for_fraud(high_risk_text)
    print(f"Risk Level: {result['risk_level']}")
    print(result['response'])
    
    print("\n" + "="*50 + "\n")
    
    # Test medium-risk scenario  
    print("=== MEDIUM RISK TEST ===")
    medium_risk_text = "Someone called claiming to be from my bank asking to verify my account information because of suspicious activity."
    result = agent.analyze_text_for_fraud(medium_risk_text)
    print(f"Risk Level: {result['risk_level']}")
    print(result['response'])
    
    print("\n" + "="*50 + "\n")
    
    # Test low-risk scenario
    print("=== LOW RISK TEST ===")
    low_risk_text = "I received a call from my doctor's office confirming my appointment tomorrow."
    result = agent.analyze_text_for_fraud(low_risk_text)
    print(f"Risk Level: {result['risk_level']}")
    print(result['response'])

if __name__ == "__main__":
    test_fraud_agent()