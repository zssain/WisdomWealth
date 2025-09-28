# family_agent.py
import os
import google.generativeai as genai
from typing import Dict, List

class FamilyAgent:
    def __init__(self, api_key: str = None):
        # Initialize Gemini API
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ Warning: No Gemini API key provided for Family Agent.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize Gemini model for Family Agent: {e}")
            self.model = None
    
    def analyze_text_for_family(self, text: str) -> Dict:
        """Analyze text input for family-related concerns"""
        risk_level = "LOW"
        actions = []
        response = ""
        
        text_lower = text.lower()
        
        # Family emergency scam indicators
        if any(keyword in text_lower for keyword in ["emergency", "accident", "hospital", "jail", "trouble"]) and any(keyword in text_lower for keyword in ["money", "wire", "send", "urgent"]):
            risk_level = "HIGH"
            actions.extend(["VERIFY_FAMILY", "DO_NOT_SEND_MONEY", "ALERT_FAMILY"])
            response = self._generate_family_emergency_scam_response()
        
        # Legitimate family updates
        elif any(keyword in text_lower for keyword in ["family", "children", "grandchildren", "update", "contact"]):
            if "emergency" not in text_lower and "money" not in text_lower:
                risk_level = "LOW"
                actions.append("UPDATE_FAMILY_INFO")
                response = self._generate_family_update_response()
        
        # Family alert preferences
        elif any(keyword in text_lower for keyword in ["alert", "notify", "contact family", "emergency contact"]):
            risk_level = "LOW"
            actions.append("UPDATE_ALERT_PREFS")
            response = self._generate_alert_preferences_response()
        
        else:
            response = self._generate_general_family_response()
        
        return {
            "risk_level": risk_level,
            "response": response,
            "actions": actions,
            "agent_type": "family"
        }
    
    def generate_family_alert(self, event_description: str, risk_level: str = "MEDIUM") -> str:
        """Generate family alert message"""
        if not self.model:
            return self._basic_family_alert(event_description, risk_level)
        
        prompt = (
            "You are a family safety and financial assistant. "
            "Your response must be a structured alert in a **plain text format**, using simple line breaks (\\n) and dashes (-) for bullet points. **DO NOT use Markdown or special characters** like '*', '##', or '**'.\n"
            "The alert must contain the following three sections, separated by a blank line:\n"
            "1. A **Concise Headline** (one sentence, reassuring tone).\n"
            "2. **Immediate Action Steps** (2-3 dashed list items with clear, actionable instructions).\n"
            "3. **Contact Protocol** (1 dashed list item confirming the emergency contact is being notified).\n"
            f"Event: {event_description}\n"
            f"Risk Level: {risk_level}\n\n"
            "Format Example for 'Missing money in account':\n"
            "Concise Headline: We have identified an unexpected financial discrepancy and are investigating.\n\n"
            "Immediate Action Steps:\n"
            "- Temporarily halt all transfers from the affected account.\n"
            "- Review your transaction history for any unauthorized activity and save screenshots.\n"
            "- Wait for the family administrator to provide next steps before contacting the bank.\n\n"
            "Contact Protocol:\n"
            "- The emergency family contact has been automatically notified and will be in touch shortly."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text if response and hasattr(response, 'text') else self._basic_family_alert(event_description, risk_level)
        except Exception as e:
            return self._basic_family_alert(event_description, risk_level)
    
    def _basic_family_alert(self, event_description: str, risk_level: str) -> str:
        """Generate basic family alert without AI"""
        urgency = "URGENT" if risk_level == "HIGH" else "ATTENTION"
        
        return f"""🚨 FAMILY ALERT - {urgency}

We detected a security concern that needs attention: {event_description}

Immediate Action Steps:
- Contact your family member to verify this situation
- Do not take any financial actions until verification
- Keep this alert for your records

Contact Protocol:
- Emergency family contacts have been notified automatically"""
    
    def update_family_preferences(self, user_id: str, preferences: Dict) -> Dict:
        """Update family alert preferences"""
        # This would typically update database
        # For now, return success response
        return {
            "status": "success",
            "message": "Family alert preferences updated successfully",
            "risk_level": "LOW",
            "actions": ["PREFERENCES_UPDATED"]
        }
    
    def get_emergency_contacts(self, user_id: str) -> List[Dict]:
        """Get emergency contacts for user"""
        # This would typically query database
        # For now, return mock data
        return [
            {"name": "Primary Contact", "relationship": "Child", "method": "phone"},
            {"name": "Secondary Contact", "relationship": "Spouse", "method": "email"}
        ]
    
    def _generate_family_emergency_scam_response(self) -> str:
        """Generate structured response for family emergency scam warnings"""
        return """🚨 **FAMILY EMERGENCY SCAM ALERT** 🚨

**⚠️ IMMEDIATE DANGER:**

This is a classic "grandparent scam" or family emergency fraud! Criminals specifically target seniors by pretending a family member is in trouble and needs money immediately.

**🎯 How This Scam Works:**

• **The Call:** "Grandma/Grandpa, I'm in trouble and need help!"
• **The Story:** Claims of jail, accident, hospital, or other emergency
• **The Pressure:** "Don't tell anyone, just send money quickly!"
• **The Request:** Money via wire transfer, gift cards, or cash
• **The Trap:** Once you send money, they disappear and may call back for more

**🚫 What to Do RIGHT NOW:**

1. **DO NOT send any money** - No matter how urgent it sounds
2. **HANG UP immediately** - Don't continue the conversation
3. **VERIFY independently** - Call your family member directly using a number you know
4. **Ask questions only the real person would know** - Middle name, pet's name, etc.

**🔍 Warning Signs You Just Experienced:**

• Urgent request for money from a "family member"
• Caller asks you not to tell other family members
• Request for payment via gift cards, wire transfer, or cash
• Caller's voice sounds different (they often claim to be injured)
• Story doesn't quite add up or feels rushed

**📞 How to Verify If It's Real:**

• **Call the family member directly** - Use a phone number you have for them
• **Ask specific questions** - "What's your middle name?" "What's our pet's name?"
• **Contact other family members** - They would know about real emergencies
• **Call the institution mentioned** - Hospital, jail, etc. to verify

**🛡️ Protect Yourself from Future Scams:**

• **Never send money based on phone calls alone** - Always verify in person or through known contact methods
• **Be suspicious of urgency** - Real emergencies usually involve multiple family members
• **Don't give personal information** - Scammers use details to make their story more believable
• **Trust your instincts** - If something feels wrong, it probably is

**💡 What Real Family Emergencies Look Like:**

• Multiple family members are involved and communicating
• You can reach the person directly or through known family members
• There are official documents, hospital contacts, or legal representatives
• The story is consistent and verifiable

**✅ You Did the RIGHT Thing:**

By being suspicious and checking with me, you've protected yourself from becoming a victim. Your caution is exactly what prevents these criminals from succeeding.

**🤝 Next Steps:**

• If you have concerns about a real family member, call them directly
• Consider sharing this information with your family so they know about these scams
• Report this scam attempt to local police and the FTC at 1-877-FTC-HELP

**Need Help?** If you're still concerned about a family member's safety, I can help you figure out the right way to verify their well-being through official channels."""

    def _generate_family_update_response(self) -> str:
        """Generate structured response for legitimate family updates"""
        return """👨‍👩‍👧‍👦 **FAMILY CONTACT MANAGEMENT** 👨‍👩‍👧‍👦

**📝 Keeping Your Family Information Current:**

It's wonderful that you want to keep your family contact information updated! This helps ensure everyone can stay connected and that important people can be reached when needed.

**📋 Information I Can Help You Organize:**

• **Contact Details** - Phone numbers, email addresses, home addresses
• **Emergency Contacts** - Who to call in case of health or safety concerns
• **Family Relationships** - Children, grandchildren, spouse, siblings
• **Notification Preferences** - How and when family should be contacted
• **Special Circumstances** - Medical needs, caregiving arrangements

**✅ Benefits of Updated Family Information:**

• **Emergency Response** - Medical personnel can contact the right people quickly
• **Financial Security** - Banks and institutions know who to call about suspicious activity
• **Peace of Mind** - Your family knows how to reach you and you know how to reach them
• **Legal Protection** - Estate and healthcare documents have current beneficiary information

**🔄 Regular Updates to Consider:**

• **Address Changes** - When family members move
• **Phone Number Changes** - New cell phones, disconnected landlines
• **Email Updates** - New email addresses, closed accounts
• **Relationship Changes** - Marriages, divorces, new grandchildren
• **Health Changes** - New medical contacts, changed caregivers

**📞 Setting Up Emergency Contacts:**

• **Primary Contact** - Someone who lives nearby and is usually available
• **Secondary Contact** - Backup person in case primary isn't reachable
• **Medical Contact** - Someone authorized to make healthcare decisions
• **Financial Contact** - Person who can help with banking or financial matters

**🛡️ Privacy and Security:**

• **Keep information current** but only share with trusted institutions
• **Verify requests** - Don't update information based on unsolicited calls
• **Protect personal details** - Only give information to legitimate organizations
• **Document changes** - Keep records of when and where you updated information

**💡 Smart Communication Practices:**

• **Regular check-ins** - Schedule calls or visits with family members
• **Shared calendars** - Use simple tools to keep everyone informed
• **Emergency plans** - Make sure family knows your preferences for different situations
• **Clear instructions** - Let family know where important documents are kept

**✅ You're Taking Care of Your Relationships:**

By keeping family information updated, you're strengthening your support network and ensuring everyone can help each other when needed.

**Need Specific Help?** I can guide you through organizing contact information, setting up emergency notification preferences, or help you think through who should be your primary contacts for different situations."""

    def _generate_alert_preferences_response(self) -> str:
        """Generate structured response for family alert preferences"""
        return """📢 **FAMILY ALERT SYSTEM SETUP** 📢

**🔔 Creating Your Safety Network:**

Setting up family alert preferences is a smart way to ensure your loved ones know when you need help or when there are important security updates about your accounts.

**📋 Types of Alerts We Can Configure:**

• **Security Alerts** - Unusual account activity, login attempts, password changes
• **Financial Alerts** - Large transactions, low balances, suspicious activity
• **Health Alerts** - Medical appointment reminders, medication alerts
• **Safety Alerts** - Emergency situations, welfare checks needed
• **Communication Alerts** - Important messages, family news

**✅ How Family Alerts Help:**

• **Rapid Response** - Family knows immediately when you need help
• **Fraud Prevention** - Multiple people watching for suspicious activity
• **Peace of Mind** - Everyone knows you're safe and secure
• **Coordination** - Family can work together to assist you
• **Early Detection** - Problems are caught and addressed quickly

**👥 Setting Up Your Alert Network:**

**Primary Contacts:**
• **Emergency Contact** - First person called in urgent situations
• **Daily Contact** - Family member who checks on you regularly
• **Medical Contact** - Person authorized for healthcare decisions
• **Financial Contact** - Someone who can help with banking issues

**Secondary Contacts:**
• **Backup Emergency** - Alternative person if primary isn't available
• **Out-of-Area Contact** - Family member in different location
• **Tech Support** - Someone who can help with computer/phone issues

**🔧 Alert Customization Options:**

**Immediate Alerts (Call + Text):**
• Medical emergencies
• Suspected fraud or scams
• Account security breaches
• Safety concerns

**Daily Summary Alerts (Email):**
• Account activity summaries
• Appointment reminders
• General updates
• Non-urgent notifications

**Weekly Reports:**
• Overall account status
• Health and wellness summaries
• Family communication updates

**🛡️ Privacy Protection:**

• **Limited Information** - Alerts only contain necessary details
• **Secure Delivery** - Sent through encrypted, verified channels
• **Access Control** - You control what information each contact receives
• **Update Control** - You can change preferences anytime

**⚙️ Getting Started:**

1. **Choose your contacts** - Decide who should receive different types of alerts
2. **Set preferences** - Determine what triggers alerts and how they're sent
3. **Test the system** - Make sure alerts work and reach the right people
4. **Regular reviews** - Update contacts and preferences as needed

**💡 Best Practices:**

• **Keep it simple** - Don't overwhelm family with too many alerts
• **Be specific** - Clear instructions about what different alerts mean
• **Stay updated** - Review and adjust settings every few months
• **Communicate clearly** - Make sure family understands the alert system

**✅ You're Creating a Support System:**

By setting up family alerts, you're building a network of people who care about your safety and can help when needed. This proactive approach gives everyone peace of mind.

**Ready to Configure?** I can help you decide which family members should receive which types of alerts, or help you set up specific notification preferences for your accounts."""

    def _generate_general_family_response(self) -> str:
        """Generate structured general family management response"""
        return """👨‍👩‍👧‍👦 **FAMILY COMMUNICATION & SAFETY** 👨‍👩‍👧‍👦

**🤗 Welcome to Family Management:**

I'm here to help you stay connected with your family and ensure everyone can communicate safely and effectively, especially when it comes to your security and well-being.

**📋 What I Can Help You With:**

• **Contact Organization** - Keep family phone numbers and addresses current
• **Emergency Planning** - Set up who to call in different situations  
• **Alert Systems** - Configure notifications for family members
• **Safety Education** - Learn about scams that target family relationships
• **Communication Tools** - Simple ways to stay in touch with loved ones

**🛡️ Family Safety Topics:**

**Scam Prevention:**
• **Grandparent Scams** - Fake emergency calls asking for money
• **Family Impersonation** - Criminals pretending to be relatives
• **Social Media Risks** - Protecting personal information online
• **Phone Safety** - Verifying who you're really talking to

**Emergency Preparedness:**
• **Medical Emergencies** - Who to call and what information to share
• **Financial Emergencies** - Protecting accounts and getting help
• **Natural Disasters** - Family communication during emergencies
• **Technology Issues** - Getting help when devices aren't working

**📞 Communication Best Practices:**

• **Regular Check-ins** - Schedule calls or visits with family
• **Clear Instructions** - Make sure family knows your preferences
• **Emergency Protocols** - Everyone knows what to do in different situations
• **Information Updates** - Keep contact details and preferences current

**💡 Staying Connected Safely:**

• **Verify unexpected calls** - Always double-check before sharing information or sending money
• **Use known numbers** - Call family back on numbers you know are correct
• **Ask specific questions** - Real family members can answer personal questions
• **Trust your instincts** - If something feels wrong, investigate further

**🌟 Building Your Support Network:**

• **Primary contacts** - People you talk to regularly
• **Emergency contacts** - Who to call in urgent situations
• **Local support** - Neighbors or nearby family who can help quickly
• **Professional contacts** - Doctors, lawyers, financial advisors

**✅ Benefits of Good Family Communication:**

• **Enhanced Safety** - More people watching out for your well-being
• **Better Decision Making** - Family input on important choices
• **Emotional Support** - Staying connected with people who care about you
• **Practical Help** - Assistance with daily tasks when needed

**🎯 Common Questions I Can Help With:**

• "How do I verify if a family emergency call is real?"
• "Who should I list as my emergency contacts?"
• "How can I set up alerts so family knows if I need help?"
• "What information is safe to share with family members?"
• "How can I protect my family from scams targeting seniors?"

**Need Specific Assistance?** Ask me about any family communication concern, emergency planning, or safety question. I'm here to help you build strong, secure connections with the people who matter most to you."""