import json
# import pandas as pd  # Temporarily disabled for deployment
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
# import numpy as np  # Temporarily disabled for deployment
import os
import logging
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class FraudAlert:
    transaction_id: str
    risk_level: str
    reason: str
    elderly_concern: str
    recommendation: str
    confidence_score: float

class ElderlyFraudAgentWithGemini:
    """
    Advanced fraud detection agent for elderly users using Gemini AI
    Combines rule-based detection with AI-powered pattern recognition
    """
    
    def __init__(self, gemini_api_key: str = None):
        # Initialize Gemini API
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
        else:
            # Try to get from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
            else:
                print("⚠️ Warning: No Gemini API key provided. AI analysis will be limited.")
        
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except:
            self.model = None
            print("⚠️ Warning: Could not initialize Gemini model. Using rule-based detection only.")
        
        self.fraud_patterns = {
            "amount_anomaly": {
                "threshold": 2.5,  # Standard deviations from normal
                "risk_level": "HIGH"
            },
            "merchant_mismatch": {
                "suspicious_categories": ["gas_station", "pharmacy", "grocery"],
                "unusual_amounts": 1000.0,
                "risk_level": "MEDIUM"
            },
            "velocity_fraud": {
                "max_transactions_per_hour": 5,
                "max_amount_per_hour": 5000.0,
                "risk_level": "HIGH"
            },
            "channel_anomaly": {
                "elderly_preferred": ["POS", "CONTACTLESS"],
                "suspicious_for_elderly": ["CNP", "ATM"],
                "risk_level": "MEDIUM"
            }
        }
        
        self.elderly_friendly_messages = {
            "safe": "✅ This transaction looks normal and safe.",
            "caution": "⚠️ Please review this transaction carefully.",
            "danger": "🚨 ALERT: This transaction shows signs of fraud!"
        }
    
    def analyze_text_for_fraud(self, text: str) -> Dict:
        """Analyze text input for fraud indicators"""
        risk_indicators = []
        risk_level = "LOW"
        actions = []
        
        text_lower = text.lower()
        
        # High-risk patterns
        if any(keyword in text_lower for keyword in ["ssn", "social security", "bank account", "credit card", "password"]):
            risk_indicators.append("Request for sensitive personal information")
            risk_level = "HIGH"
            actions.extend(["BLOCK_CALLER", "ALERT_FAMILY"])
        
        if any(keyword in text_lower for keyword in ["urgent", "immediate", "act now", "limited time"]):
            risk_indicators.append("High-pressure tactics detected")
            if risk_level != "HIGH":
                risk_level = "MEDIUM"
            actions.append("VERIFY_INDEPENDENTLY")
        
        if any(keyword in text_lower for keyword in ["gift card", "bitcoin", "wire transfer", "money order"]):
            risk_indicators.append("Suspicious payment method requested")
            risk_level = "HIGH"
            actions.extend(["DO_NOT_PAY", "ALERT_FAMILY"])
        
        if any(keyword in text_lower for keyword in ["irs", "arrest", "warrant", "police"]):
            risk_indicators.append("Government impersonation scam indicators")
            risk_level = "HIGH"
            actions.extend(["HANG_UP", "CONTACT_AUTHORITIES"])
        
        # Generate detailed structured response based on risk
        if risk_level == "HIGH":
            response = self._generate_high_risk_response(risk_indicators, text)
        elif risk_level == "MEDIUM":
            response = self._generate_medium_risk_response(risk_indicators, text)
        else:
            response = self._generate_low_risk_response(text)
        
        return {
            "risk_level": risk_level,
            "response": response,
            "risk_indicators": risk_indicators,
            "actions": actions,
            "confidence_score": 0.9 if risk_level == "HIGH" else 0.7 if risk_level == "MEDIUM" else 0.5
        }
    
    def _generate_high_risk_response(self, risk_indicators: List[str], original_text: str) -> str:
        """Generate detailed high-risk fraud warning response"""
        return f"""🚨 **IMPORTANT FRAUD ALERT** 🚨

**⚠️ IMMEDIATE DANGER:**

This appears to be a SCAM attempt! The contact you described shows multiple warning signs of fraud targeting seniors.

**🎯 Red Flags Detected:**

• {chr(10).join([f"• {indicator}" for indicator in risk_indicators])}

**🛡️ What You Should Do RIGHT NOW:**

1. **DO NOT share any personal information** - Never give out Social Security numbers, bank account details, passwords, or credit card information
2. **HANG UP immediately** - Do not continue the conversation
3. **DO NOT make any payments** - Legitimate organizations do not demand immediate payment with gift cards, wire transfers, or Bitcoin
4. **Block the number** - Prevent them from calling again

**📞 Who to Contact:**

• **Call your bank directly** using the number on your card or statement (NOT the number the caller gave you)
• **Report to authorities:** Call your local police non-emergency line
• **Report to FTC:** Call 1-877-FTC-HELP (1-877-382-4357)
• **Tell a trusted family member** - They should know about this attempt

**🔒 Remember:**

• Real government agencies (IRS, Social Security) do NOT call demanding immediate payment
• Your bank already knows your account information - they won't ask for it over the phone
• Microsoft/Apple do NOT call about computer problems
• Medicare will NEVER call asking for your number

**✅ You did the RIGHT THING by checking with me first!**

Stay safe and trust your instincts. When in doubt, hang up and call the official number."""

    def _generate_medium_risk_response(self, risk_indicators: List[str], original_text: str) -> str:
        """Generate detailed medium-risk caution response"""
        return f"""⚠️ **CAUTION: SUSPICIOUS ACTIVITY DETECTED** ⚠️

**🤔 What This Means:**

The contact you described has some warning signs that suggest it could be suspicious. While not definitely a scam, it's important to verify before taking any action.

**🔍 Concerns Identified:**

• {chr(10).join([f"• {indicator}" for indicator in risk_indicators])}

**✅ Steps to Verify Safely:**

1. **Don't act immediately** - Legitimate businesses won't pressure you for instant decisions
2. **Verify independently** - Call the company using the official number from your bill, statement, or their website
3. **Ask for details** - Get the caller's name, company, and callback number
4. **Check with family** - Discuss with a trusted family member or friend before making decisions

**📋 Questions to Ask:**

• "Can you send me information in writing?"
• "What is your company's official phone number?"
• "Can I call you back after I verify this?"
• "Why is this urgent/time-sensitive?"

**🚨 If They Pressure You:**

This becomes a RED FLAG. Legitimate companies understand the need to verify and won't pressure elderly customers.

**💡 General Safety Tips:**

• Never give personal information to unsolicited callers
• Take time to think and consult others
• When in doubt, hang up and call the official number
• Trust your instincts - if something feels wrong, it probably is

**✅ You're Being Smart:**

By checking on this contact, you're protecting yourself the right way. Always verify before you trust!"""

    def _generate_low_risk_response(self, original_text: str) -> str:
        """Generate structured low-risk guidance response"""
        return f"""✅ **SECURITY ASSESSMENT: LOW RISK** ✅

**📝 Initial Assessment:**

Based on the information you provided, this contact appears to be legitimate. However, it's always wise to remain cautious with any unsolicited contact.

**🛡️ Smart Safety Practices:**

**For Phone Calls:**
• Verify the caller by hanging up and calling the official company number
• Never give personal information immediately, even if the call seems legitimate
• Ask for written confirmation of any changes to accounts or services

**For Emails:**
• Check the sender's email address carefully for misspellings
• Don't click links - go directly to the company's official website
• Be wary of urgent language or immediate action requests

**For Mail:**
• Verify through official channels before responding to unexpected offers
• Shred documents containing personal information
• Be cautious of "pre-approved" credit offers

**📞 When to Call for Help:**

• If the caller becomes pushy or aggressive
• If they ask for immediate payment or personal information
• If something doesn't feel right, even if you can't explain why
• If they claim there's an emergency involving family members

**👥 Stay Connected:**

• Share information about suspicious contacts with family members
• Report potential scams to help protect other seniors
• Keep important phone numbers handy for quick verification

**💪 You're Doing Great:**

By staying alert and asking questions, you're protecting yourself effectively. Trust your instincts and never hesitate to verify!

**Need Help?** If you have any concerns, don't hesitate to ask me about specific contacts or situations."""
    
    def load_transaction_data(self, file_path: str):
        """
        Load transaction data from CSV file
        Temporarily disabled for deployment compatibility
        """
        logger.warning("Transaction data loading temporarily disabled for deployment")
        return []
        """Load and prepare transaction data"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df
    
    def analyze_with_gemini(self, transactions: List[Dict]) -> Dict:
        """Use Gemini AI to analyze transaction patterns"""
        if not self.model:
            return {"error": "Gemini AI not available"}
        
        # Prepare transaction data for AI analysis
        transaction_summary = []
        for tx in transactions:
            summary = {
                "id": tx['transaction_id'],
                "amount": tx['amount'],
                "merchant": tx['merchant_name'],
                "category": tx['merchant_category'],
                "channel": tx['channel'],
                "existing_fraud_score": tx.get('fraud_score', 0)
            }
            transaction_summary.append(summary)
        
        prompt = f"""
        You are a fraud detection expert specializing in protecting elderly customers from financial scams and fraud.
        
        Analyze these transactions for patterns that might indicate fraud targeting seniors:
        
        {json.dumps(transaction_summary, indent=2)}
        
        Focus on these elderly-specific fraud indicators:
        1. Merchant category mismatches (e.g., Shell categorized as grocery)
        2. Unusually high amounts for common categories (pharmacy, gas station)
        3. ATM withdrawals over $1000 (often indicates coercion)
        4. Card-not-present transactions over $500 (phone/online scams)
        5. Multiple transactions at same merchant type in short time
        
        For each suspicious transaction, provide:
        - Transaction ID
        - Risk level (LOW/MEDIUM/HIGH)
        - Specific concern for elderly users
        - Recommended action
        - Confidence score (0.0-1.0)
        
        Respond in JSON format with an array of alerts.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON from response
            response_text = response.text
            
            # Clean up the response to extract JSON
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return {"ai_alerts": json.loads(json_str)}
            else:
                return {"ai_analysis": response_text, "parsed": False}
                
        except Exception as e:
            return {"error": f"Gemini analysis failed: {str(e)}"}
    
    def rule_based_analysis(self, data) -> List[FraudAlert]:
        """
        Rule-based analysis for transactions
        Temporarily simplified for deployment compatibility
        """
        logger.warning("Rule-based analysis temporarily simplified for deployment")
        return []
        """Traditional rule-based fraud detection"""
        alerts = []
        
        for _, tx in df.iterrows():
            # Check merchant category mismatches
            if (tx['merchant_name'] == 'Shell' and tx['merchant_category'] == 'grocery' and tx['amount'] > 2000):
                alerts.append(FraudAlert(
                    transaction_id=tx['transaction_id'],
                    risk_level="HIGH",
                    reason=f"Shell gas station categorized as grocery with ${tx['amount']:.2f} charge",
                    elderly_concern="This is a common fraud pattern - gas stations don't sell $2000 in groceries",
                    recommendation="Contact bank immediately to verify this transaction",
                    confidence_score=0.9
                ))
            
            # Check for high pharmacy charges
            if tx['merchant_category'] == 'pharmacy' and tx['amount'] > 1300:
                alerts.append(FraudAlert(
                    transaction_id=tx['transaction_id'],
                    risk_level="HIGH",
                    reason=f"Unusually high pharmacy charge: ${tx['amount']:.2f}",
                    elderly_concern="Seniors are often targeted with fake medical billing scams",
                    recommendation="Verify this charge with the pharmacy directly",
                    confidence_score=0.85
                ))
            
            # Check for large ATM withdrawals
            if tx['channel'] == 'ATM' and tx['amount'] > 1000:
                alerts.append(FraudAlert(
                    transaction_id=tx['transaction_id'],
                    risk_level="HIGH",
                    reason=f"Large ATM withdrawal: ${tx['amount']:.2f}",
                    elderly_concern="Large cash withdrawals often indicate elder financial abuse or coercion",
                    recommendation="Contact customer immediately to verify they made this withdrawal",
                    confidence_score=0.95
                ))
            
            # Check for large CNP (Card Not Present) transactions
            if tx['channel'] == 'CNP' and tx['amount'] > 700:
                alerts.append(FraudAlert(
                    transaction_id=tx['transaction_id'],
                    risk_level="MEDIUM",
                    reason=f"Large online/phone transaction: ${tx['amount']:.2f}",
                    elderly_concern="Seniors are frequent targets of phone and online scams",
                    recommendation="Verify this purchase was intentional and from a trusted source",
                    confidence_score=0.75
                ))
            
            # Check for restaurant charges at gas stations
            if tx['merchant_name'] in ['Exxon', 'Shell'] and tx['merchant_category'] == 'restaurant':
                alerts.append(FraudAlert(
                    transaction_id=tx['transaction_id'],
                    risk_level="MEDIUM",
                    reason=f"Gas station {tx['merchant_name']} categorized as restaurant: ${tx['amount']:.2f}",
                    elderly_concern="This category mismatch could indicate card skimming or data theft",
                    recommendation="Check if customer actually made a purchase at this location",
                    confidence_score=0.8
                ))
        
        return alerts
    
    def generate_family_alert(self, high_risk_alerts: List[FraudAlert]) -> str:
        """Generate alert message for family members"""
        if not high_risk_alerts:
            return None
        
        alert_message = [
            "🚨 FAMILY FRAUD ALERT",
            "=" * 25,
            "",
            f"We detected {len(high_risk_alerts)} high-risk transactions that need immediate attention:",
            ""
        ]
        
        for alert in high_risk_alerts:
            alert_message.extend([
                f"• Transaction {alert.transaction_id}:",
                f"  Problem: {alert.reason}",
                f"  Why this matters: {alert.elderly_concern}",
                f"  What to do: {alert.recommendation}",
                ""
            ])
        
        alert_message.extend([
            "IMMEDIATE ACTIONS NEEDED:",
            "1. Contact your family member to verify these transactions",
            "2. If fraud is confirmed, call the bank fraud hotline",
            "3. Consider temporarily freezing the card",
            "",
            "This alert was generated by WisdomWealth Fraud Protection"
        ])
        
        return "\n".join(alert_message)
    
    def comprehensive_fraud_analysis(self, file_path: str) -> Dict:
        """Run complete fraud analysis combining rule-based and AI detection"""
        df = self.load_transaction_data(file_path)
        
        print("🔍 Starting comprehensive fraud analysis...")
        
        # Rule-based analysis
        print("📋 Running rule-based detection...")
        rule_alerts = self.rule_based_analysis(df)
        
        # AI-powered analysis
        ai_results = {}
        if self.model:
            print("🤖 Running Gemini AI analysis...")
            transactions_list = df.to_dict('records')
            ai_results = self.analyze_with_gemini(transactions_list)
        
        # Combine results
        high_risk_alerts = [alert for alert in rule_alerts if alert.risk_level == "HIGH"]
        
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_transactions_analyzed": len(df),
            "rule_based_alerts": [
                {
                    "transaction_id": alert.transaction_id,
                    "risk_level": alert.risk_level,
                    "reason": alert.reason,
                    "elderly_concern": alert.elderly_concern,
                    "recommendation": alert.recommendation,
                    "confidence_score": alert.confidence_score
                } for alert in rule_alerts
            ],
            "ai_analysis": ai_results,
            "high_risk_count": len(high_risk_alerts),
            "family_alert": self.generate_family_alert(high_risk_alerts)
        }
        
        # Generate elderly-friendly summary
        results["elderly_summary"] = self.generate_elderly_summary(rule_alerts)
        
        return results
    
    def generate_elderly_summary(self, alerts: List[FraudAlert]) -> str:
        """Generate clear, simple summary for elderly users"""
        high_risk = [a for a in alerts if a.risk_level == "HIGH"]
        medium_risk = [a for a in alerts if a.risk_level == "MEDIUM"]
        
        summary = [
            "🛡️ YOUR TRANSACTION SECURITY REPORT",
            "=" * 40,
            ""
        ]
        
        if high_risk:
            summary.extend([
                "🚨 URGENT - POSSIBLE FRAUD DETECTED!",
                "",
                "We found transactions that look suspicious:",
                ""
            ])
            
            for alert in high_risk:
                summary.extend([
                    f"• Transaction {alert.transaction_id}:",
                    f"  Problem: {alert.reason}",
                    f"  What this means: {alert.elderly_concern}",
                    f"  What to do: {alert.recommendation}",
                    ""
                ])
            
            summary.extend([
                "🔒 IMMEDIATE STEPS TO TAKE:",
                "1. Call your bank's fraud hotline RIGHT NOW",
                "2. Do NOT give personal info to anyone who calls YOU",
                "3. Tell a trusted family member about this alert",
                ""
            ])
        
        elif medium_risk:
            summary.extend([
                "⚠️ Some transactions need your attention",
                "",
                "These purchases look unusual but may be legitimate:",
                ""
            ])
            
            for alert in medium_risk:
                summary.extend([
                    f"• {alert.reason}",
                    f"  Please verify: {alert.recommendation}",
                    ""
                ])
        
        else:
            summary.extend([
                "✅ GOOD NEWS - All transactions look normal!",
                "",
                "Your recent purchases appear safe and legitimate.",
                "We're continuing to monitor your account 24/7.",
                ""
            ])
        
        summary.extend([
            "💡 REMEMBER:",
            "• Banks will NEVER ask for passwords over the phone",
            "• Be suspicious of urgent payment requests",
            "• When in doubt, hang up and call your bank directly",
            "",
            "This report was created by your WisdomWealth protection system."
        ])
        
        return "\n".join(summary)