# coordinator.py
import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Import agents
from agents.fraud_agent import ElderlyFraudAgentWithGemini
from agents.healthcare_agent import HealthcareFinanceAgent
from agents.estate_agent import EstateAgent
from agents.family_agent import FamilyAgent

# Import database helpers
from database.sqlite_helper import SQLiteHelper
from database.chroma_helper import ChromaHelper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentCoordinator:
    """
    Coordinates multiple specialized agents for WisdomWealth platform
    Routes requests to appropriate agents and merges responses
    """
    
    def __init__(self):
        # Initialize database helpers
        self.db = SQLiteHelper()
        self.chroma = ChromaHelper()
        
        # Get API key from environment
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        # Intent detection keywords
        self.intent_keywords = {
            "fraud": [
                "suspicious", "call", "ssn", "social security", "scam", "unknown caller", 
                "payment request", "urgent", "wire transfer", "gift card", "irs", 
                "arrest", "warrant", "bitcoin", "verify account", "compromised"
            ],
            "healthcare": [
                "medical", "bill", "insurance", "premium", "doctor", "hospital", 
                "medicare", "medicaid", "pharmacy", "prescription", "health", 
                "treatment", "diagnosis", "copay", "deductible"
            ],
            "estate": [
                "will", "testament", "beneficiary", "inheritance", "trust", 
                "power of attorney", "documents", "legal", "lawyer", "attorney",
                "estate", "probate", "assets", "property"
            ],
            "family": [
                "family", "alert", "notify", "contact", "emergency", "children",
                "grandchildren", "spouse", "relatives", "emergency contact"
            ]
        }
        
        # Risk priority mapping
        self.risk_priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
        logger.info("AgentCoordinator initialized successfully")
    
    def _initialize_agents(self) -> Dict:
        """Initialize all specialized agents"""
        agents = {}
        
        try:
            agents["fraud"] = ElderlyFraudAgentWithGemini(self.gemini_api_key)
            logger.info("✅ Fraud agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize fraud agent: {e}")
            agents["fraud"] = None
        
        try:
            agents["healthcare"] = HealthcareFinanceAgent(self.gemini_api_key)
            logger.info("✅ Healthcare agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize healthcare agent: {e}")
            agents["healthcare"] = None
        
        try:
            agents["estate"] = EstateAgent(self.gemini_api_key)
            logger.info("✅ Estate agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize estate agent: {e}")
            agents["estate"] = None
        
        try:
            agents["family"] = FamilyAgent(self.gemini_api_key)
            logger.info("✅ Family agent initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize family agent: {e}")
            agents["family"] = None
        
        return agents
    
    def detect_intents(self, text: str) -> List[str]:
        """Detect which agents should be activated based on input text"""
        text_lower = text.lower()
        activated_intents = []
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                activated_intents.append(intent)
        
        # Default to fraud agent if no specific intent detected
        if not activated_intents:
            activated_intents = ["fraud"]
        
        # Always activate family agent for HIGH risk situations
        if any(keyword in text_lower for keyword in ["emergency", "urgent", "help", "scam", "fraud"]):
            if "family" not in activated_intents:
                activated_intents.append("family")
        
        logger.info(f"Detected intents: {activated_intents} for input: '{text[:50]}...'")
        return activated_intents
    
    def _normalize_agent_response(self, agent_name: str, response: any) -> Dict:
        """Normalize different agent response formats to standard format"""
        if isinstance(response, str):
            # Simple string response
            return {
                "response": response,
                "risk_level": "LOW",
                "actions": [],
                "agent_type": agent_name
            }
        
        if isinstance(response, dict):
            # Already structured response
            return {
                "response": response.get("response", response.get("analysis", "No response")),
                "risk_level": response.get("risk_level", "LOW"),
                "actions": response.get("actions", []),
                "agent_type": agent_name,
                "confidence_score": response.get("confidence_score", 0.5),
                "metadata": response.get("metadata", {})
            }
        
        # Fallback for unexpected response types
        return {
            "response": str(response),
            "risk_level": "LOW", 
            "actions": [],
            "agent_type": agent_name
        }
    
    def _call_fraud_agent(self, text: str) -> Dict:
        """Call fraud agent with text analysis"""
        if not self.agents["fraud"]:
            return {"error": "Fraud agent not available"}
        
        try:
            # Use text analysis method for conversational input
            result = self.agents["fraud"].analyze_text_for_fraud(text)
            
            # Enhance with ChromaDB patterns if available
            if self.chroma:
                enhancement = self.chroma.enhance_fraud_analysis(text)
                if enhancement["enhancement"]:
                    enhancement_data = enhancement["enhancement"]
                    
                    # Upgrade risk level if pattern matching suggests higher risk
                    suggested_risk = enhancement_data.get("suggested_risk_level", "LOW")
                    current_risk = result.get("risk_level", "LOW")
                    
                    if self.risk_priority[suggested_risk] > self.risk_priority[current_risk]:
                        result["risk_level"] = suggested_risk
                        result["pattern_enhanced"] = True
                        
                        # Add elderly concerns from patterns
                        elderly_concerns = enhancement_data.get("elderly_concerns", [])
                        if elderly_concerns:
                            result["response"] += f" {elderly_concerns[0]}"
            
            return self._normalize_agent_response("fraud", result)
            
        except Exception as e:
            logger.error(f"Fraud agent error: {e}")
            return {
                "response": "Unable to analyze for fraud at this time.",
                "risk_level": "MEDIUM",
                "actions": ["MANUAL_REVIEW"],
                "agent_type": "fraud",
                "error": str(e)
            }
    
    def _call_healthcare_agent(self, text: str) -> Dict:
        """Call healthcare agent"""
        if not self.agents["healthcare"]:
            return {"error": "Healthcare agent not available"}
        
        try:
            result = self.agents["healthcare"].analyze_text_for_healthcare(text)
            return self._normalize_agent_response("healthcare", result)
            
        except Exception as e:
            logger.error(f"Healthcare agent error: {e}")
            return {
                "response": "Unable to analyze healthcare query at this time.",
                "risk_level": "LOW",
                "actions": ["CONSULT_HEALTHCARE"],
                "agent_type": "healthcare",
                "error": str(e)
            }
    
    def _call_estate_agent(self, text: str) -> Dict:
        """Call estate agent"""
        if not self.agents["estate"]:
            return {"error": "Estate agent not available"}
        
        try:
            result = self.agents["estate"].analyze_text_for_estate(text)
            return self._normalize_agent_response("estate", result)
            
        except Exception as e:
            logger.error(f"Estate agent error: {e}")
            return {
                "response": "Unable to analyze estate query at this time.",
                "risk_level": "LOW",
                "actions": ["CONSULT_ATTORNEY"],
                "agent_type": "estate",
                "error": str(e)
            }
    
    def _call_family_agent(self, text: str) -> Dict:
        """Call family agent"""
        if not self.agents["family"]:
            return {"error": "Family agent not available"}
        
        try:
            result = self.agents["family"].analyze_text_for_family(text)
            return self._normalize_agent_response("family", result)
            
        except Exception as e:
            logger.error(f"Family agent error: {e}")
            return {
                "response": "Unable to process family request at this time.",
                "risk_level": "LOW",
                "actions": ["MANUAL_CONTACT"],
                "agent_type": "family",
                "error": str(e)
            }
    
    def process_request(self, user_id: str, text: str, meta: Dict = None) -> Dict:
        """
        Main coordination function - processes user request and returns unified response
        
        Args:
            user_id: User identifier
            text: User input text
            meta: Optional metadata (channel, language, flags)
        
        Returns:
            Dict with response, risk_level, agent_traces, actions, logs_id
        """
        logger.info(f"Processing request for user {user_id}: '{text[:100]}...'")
        
        try:
            # Detect which agents to activate
            intents = self.detect_intents(text)
            
            # Call activated agents
            agent_responses = {}
            agent_traces = []
            
            for intent in intents:
                agent_traces.append(intent)
                
                if intent == "fraud":
                    agent_responses["fraud"] = self._call_fraud_agent(text)
                elif intent == "healthcare":
                    agent_responses["healthcare"] = self._call_healthcare_agent(text)
                elif intent == "estate":
                    agent_responses["estate"] = self._call_estate_agent(text)
                elif intent == "family":
                    agent_responses["family"] = self._call_family_agent(text)
            
            # Merge responses
            merged_response = self._merge_agent_responses(agent_responses)
            
            # Determine overall risk level (highest wins)
            overall_risk = self._determine_overall_risk(agent_responses)
            
            # Aggregate actions
            all_actions = self._aggregate_actions(agent_responses)
            
            # Generate elderly-friendly final response
            final_response = self._generate_final_response(merged_response, overall_risk)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(agent_responses)
            
            # Log incident to database
            incident_id = self.db.insert_incident(
                user_id=user_id,
                input_text=text,
                risk_level=overall_risk,
                response=final_response,
                agent_traces=agent_traces,
                actions=all_actions,
                confidence_score=confidence_score
            )
            
            # Generate family alert if needed
            family_alert_id = None
            if overall_risk == "HIGH" and self._should_alert_family(user_id, all_actions):
                family_alert_id = self._generate_family_alert(user_id, incident_id, final_response, overall_risk)
            
            # Prepare final response
            response = {
                "response": final_response,
                "risk": overall_risk.lower(),
                "agent_traces": agent_traces,
                "actions": all_actions,
                "logs_id": str(incident_id),
                "confidence_score": confidence_score,
                "timestamp": datetime.now().isoformat()
            }
            
            if family_alert_id:
                response["family_alert_id"] = str(family_alert_id)
            
            logger.info(f"Request processed successfully for user {user_id}, risk: {overall_risk}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            
            # Fallback response
            return {
                "response": "I'm experiencing technical difficulties. Please try again or contact support.",
                "risk": "medium",
                "agent_traces": ["error"],
                "actions": ["TRY_AGAIN", "CONTACT_SUPPORT"],
                "logs_id": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _merge_agent_responses(self, responses: Dict) -> str:
        """Merge multiple agent responses into coherent message"""
        if not responses:
            return "I'm here to help with your financial security questions."
        
        # Prioritize by risk level
        prioritized_responses = []
        for agent_name, response in responses.items():
            if not response or "error" in response:
                continue
            
            risk_level = response.get("risk_level", "LOW")
            priority = self.risk_priority.get(risk_level, 1)
            prioritized_responses.append((priority, agent_name, response.get("response", "")))
        
        # Sort by priority (highest first)
        prioritized_responses.sort(key=lambda x: x[0], reverse=True)
        
        if not prioritized_responses:
            return "I'm here to help with your financial security questions."
        
        # Use highest priority response as primary
        primary_response = prioritized_responses[0][2]
        
        return primary_response
    
    def _determine_overall_risk(self, responses: Dict) -> str:
        """Determine overall risk level from all agent responses"""
        max_risk = "LOW"
        
        for response in responses.values():
            if not response or "error" in response:
                continue
            
            risk_level = response.get("risk_level", "LOW")
            if self.risk_priority.get(risk_level, 1) > self.risk_priority.get(max_risk, 1):
                max_risk = risk_level
        
        return max_risk
    
    def _aggregate_actions(self, responses: Dict) -> List[str]:
        """Aggregate actions from all agents, removing duplicates"""
        all_actions = set()
        
        for response in responses.values():
            if not response or "error" in response:
                continue
            
            actions = response.get("actions", [])
            all_actions.update(actions)
        
        return list(all_actions)
    
    def _generate_final_response(self, merged_response: str, risk_level: str) -> str:
        """Generate final elderly-friendly response"""
        if risk_level == "HIGH":
            prefix = "🚨 IMPORTANT ALERT: "
        elif risk_level == "MEDIUM":
            prefix = "⚠️ Please pay attention: "
        else:
            prefix = "✅ "
        
        return prefix + merged_response
    
    def _calculate_confidence(self, responses: Dict) -> float:
        """Calculate overall confidence score"""
        confidence_scores = []
        
        for response in responses.values():
            if response and "confidence_score" in response:
                confidence_scores.append(response["confidence_score"])
        
        if not confidence_scores:
            return 0.5  # Default confidence
        
        return sum(confidence_scores) / len(confidence_scores)
    
    def _should_alert_family(self, user_id: str, actions: List[str]) -> bool:
        """Determine if family should be alerted"""
        # Check user preferences
        family_prefs = self.db.get_family_prefs(user_id)
        if family_prefs and not family_prefs.get("allow_alerts", True):
            return False
        
        # Alert on specific high-risk actions
        alert_actions = ["BLOCK_CALLER", "DO_NOT_PAY", "ALERT_FAMILY", "CONTACT_AUTHORITIES"]
        return any(action in actions for action in alert_actions)
    
    def _generate_family_alert(self, user_id: str, incident_id: int, response: str, risk_level: str) -> Optional[int]:
        """Generate and store family alert"""
        try:
            if self.agents["family"]:
                alert_message = self.agents["family"].generate_family_alert(
                    f"Security alert for user {user_id}: {response}", 
                    risk_level
                )
            else:
                alert_message = f"🚨 FAMILY ALERT: We detected a {risk_level.lower()} security concern. Please contact your family member to verify their safety."
            
            alert_id = self.db.insert_pending_alert(
                user_id=user_id,
                incident_id=incident_id,
                alert_type="SECURITY",
                alert_message=alert_message
            )
            
            logger.info(f"Generated family alert {alert_id} for user {user_id}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Failed to generate family alert: {e}")
            return None
    
    def get_health_status(self) -> Dict:
        """Get system health status"""
        return {
            "status": "healthy",
            "agents": {
                "fraud": self.agents["fraud"] is not None,
                "healthcare": self.agents["healthcare"] is not None,
                "estate": self.agents["estate"] is not None,
                "family": self.agents["family"] is not None
            },
            "database": {
                "sqlite": self.db is not None,
                "chromadb": self.chroma is not None and self.chroma.client is not None
            },
            "timestamp": datetime.now().isoformat()
        }