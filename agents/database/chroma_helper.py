# chroma_helper.py
import chromadb
import os
import uuid
from typing import List, Dict, Optional
from pathlib import Path
import json

class ChromaHelper:
    def __init__(self, chroma_dir: str = None):
        self.chroma_dir = chroma_dir or os.path.join(os.getenv('DATA_DIR', 'data'), 'chroma_db')
        self.enable_retrieval = os.getenv('ENABLE_RETRIEVAL', 'true').lower() == 'true'
        
        if not self.enable_retrieval:
            print("📝 ChromaDB retrieval is disabled via ENABLE_RETRIEVAL flag")
            self.client = None
            self.scam_collection = None
            self.docs_collection = None
            return
        
        # Ensure directory exists
        Path(self.chroma_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # Initialize ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(path=self.chroma_dir)
            
            # Create collections
            self.scam_collection = self.client.get_or_create_collection(
                name="scam_scripts",
                metadata={"description": "Known scam patterns and scripts for fraud detection"}
            )
            
            self.docs_collection = self.client.get_or_create_collection(
                name="user_documents", 
                metadata={"description": "User uploaded documents for analysis"}
            )
            
            # Seed with initial scam patterns if collection is empty
            self._seed_scam_patterns()
            
            print(f"✅ ChromaDB initialized at {self.chroma_dir}")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize ChromaDB: {e}")
            self.client = None
            self.scam_collection = None
            self.docs_collection = None
    
    def _seed_scam_patterns(self):
        """Seed collection with common scam patterns"""
        if not self.scam_collection or self.scam_collection.count() > 0:
            return
        
        scam_patterns = [
            {
                "text": "This is the IRS calling about your tax debt. You must pay immediately or face arrest.",
                "category": "government_impersonation",
                "risk_level": "HIGH",
                "elderly_concern": "Government agencies never threaten arrest for unpaid taxes over the phone"
            },
            {
                "text": "Your grandson is in jail and needs bail money. Send $2000 via Western Union immediately.",
                "category": "family_emergency", 
                "risk_level": "HIGH",
                "elderly_concern": "Always verify family emergencies by calling the person directly"
            },
            {
                "text": "You've won a lottery! Just pay the processing fee to claim your prize.",
                "category": "lottery_scam",
                "risk_level": "HIGH", 
                "elderly_concern": "Legitimate lotteries never require upfront fees"
            },
            {
                "text": "Your bank account has been compromised. Please provide your login details to secure it.",
                "category": "phishing",
                "risk_level": "HIGH",
                "elderly_concern": "Banks never ask for login credentials over the phone"
            },
            {
                "text": "You qualify for a free medical alert system. Just provide your Medicare number.",
                "category": "medicare_scam",
                "risk_level": "HIGH",
                "elderly_concern": "Never give Medicare information to unsolicited callers"
            },
            {
                "text": "Your computer has a virus. Allow me to remote access to fix it for $200.",
                "category": "tech_support",
                "risk_level": "HIGH",
                "elderly_concern": "Legitimate tech companies don't make unsolicited calls about viruses"
            },
            {
                "text": "Urgent payment required for your medical bill or it will go to collections.",
                "category": "medical_billing",
                "risk_level": "MEDIUM",
                "elderly_concern": "Always verify medical bills with your healthcare provider directly"
            },
            {
                "text": "Act now to lower your credit card interest rates. This offer expires today.",
                "category": "credit_card",
                "risk_level": "MEDIUM", 
                "elderly_concern": "High-pressure tactics are red flags for scams"
            }
        ]
        
        try:
            texts = [pattern["text"] for pattern in scam_patterns]
            metadatas = [{k: v for k, v in pattern.items() if k != "text"} for pattern in scam_patterns]
            ids = [str(uuid.uuid4()) for _ in scam_patterns]
            
            self.scam_collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Seeded {len(scam_patterns)} scam patterns into ChromaDB")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not seed scam patterns: {e}")
    
    def query_scam_patterns(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """Query similar scam patterns"""
        if not self.scam_collection:
            return []
        
        try:
            results = self.scam_collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            patterns = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    pattern = {
                        "text": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "similarity": 1 - results['distances'][0][i] if results['distances'] else 0.0
                    }
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            print(f"⚠️ Warning: ChromaDB query failed: {e}")
            return []
    
    def add_scam_pattern(self, text: str, category: str, risk_level: str, elderly_concern: str) -> bool:
        """Add new scam pattern to collection"""
        if not self.scam_collection:
            return False
        
        try:
            self.scam_collection.add(
                documents=[text],
                metadatas=[{
                    "category": category,
                    "risk_level": risk_level,
                    "elderly_concern": elderly_concern,
                    "user_submitted": True
                }],
                ids=[str(uuid.uuid4())]
            )
            return True
            
        except Exception as e:
            print(f"⚠️ Warning: Could not add scam pattern: {e}")
            return False
    
    def add_document(self, user_id: str, document_text: str, document_type: str, 
                    filename: str = None, metadata: Dict = None) -> str:
        """Add user document for analysis"""
        if not self.docs_collection:
            return None
        
        try:
            doc_id = str(uuid.uuid4())
            doc_metadata = {
                "user_id": user_id,
                "document_type": document_type,
                "filename": filename or "unknown",
                "upload_timestamp": str(chromadb.utils.embedding_functions.DefaultEmbeddingFunction().generate_timestamp()),
                **(metadata or {})
            }
            
            self.docs_collection.add(
                documents=[document_text],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            return doc_id
            
        except Exception as e:
            print(f"⚠️ Warning: Could not add document: {e}")
            return None
    
    def query_user_documents(self, user_id: str, query_text: str, 
                           document_type: str = None, n_results: int = 3) -> List[Dict]:
        """Query user's documents"""
        if not self.docs_collection:
            return []
        
        try:
            # Build where clause for filtering
            where_clause = {"user_id": user_id}
            if document_type:
                where_clause["document_type"] = document_type
            
            results = self.docs_collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    document = {
                        "text": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "similarity": 1 - results['distances'][0][i] if results['distances'] else 0.0
                    }
                    documents.append(document)
            
            return documents
            
        except Exception as e:
            print(f"⚠️ Warning: Document query failed: {e}")
            return []
    
    def get_user_documents(self, user_id: str) -> List[Dict]:
        """Get all documents for a user"""
        if not self.docs_collection:
            return []
        
        try:
            results = self.docs_collection.get(
                where={"user_id": user_id},
                include=["documents", "metadatas"]
            )
            
            documents = []
            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    document = {
                        "id": results['ids'][i] if results['ids'] else None,
                        "text": doc,
                        "metadata": results['metadatas'][i] if results['metadatas'] else {}
                    }
                    documents.append(document)
            
            return documents
            
        except Exception as e:
            print(f"⚠️ Warning: Could not get user documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID"""
        if not self.docs_collection:
            return False
        
        try:
            self.docs_collection.delete(ids=[document_id])
            return True
            
        except Exception as e:
            print(f"⚠️ Warning: Could not delete document: {e}")
            return False
    
    def get_collection_stats(self) -> Dict:
        """Get ChromaDB collection statistics"""
        if not self.client:
            return {"error": "ChromaDB not available"}
        
        try:
            stats = {
                "enabled": self.enable_retrieval,
                "scam_patterns": self.scam_collection.count() if self.scam_collection else 0,
                "user_documents": self.docs_collection.count() if self.docs_collection else 0,
                "collections": [col.name for col in self.client.list_collections()]
            }
            return stats
            
        except Exception as e:
            return {"error": f"Could not get stats: {e}"}
    
    def enhance_fraud_analysis(self, input_text: str) -> Dict:
        """Enhance fraud analysis with similar scam patterns"""
        if not self.enable_retrieval or not self.scam_collection:
            return {"enhancement": None, "similar_patterns": []}
        
        try:
            similar_patterns = self.query_scam_patterns(input_text, n_results=2)
            
            if not similar_patterns:
                return {"enhancement": None, "similar_patterns": []}
            
            # Find highest risk pattern
            max_risk = "LOW"
            elderly_concerns = []
            
            for pattern in similar_patterns:
                if pattern["similarity"] > 0.7:  # High similarity threshold
                    pattern_risk = pattern["metadata"].get("risk_level", "LOW")
                    if pattern_risk == "HIGH":
                        max_risk = "HIGH"
                    elif pattern_risk == "MEDIUM" and max_risk != "HIGH":
                        max_risk = "MEDIUM"
                    
                    concern = pattern["metadata"].get("elderly_concern")
                    if concern:
                        elderly_concerns.append(concern)
            
            enhancement = {
                "suggested_risk_level": max_risk,
                "elderly_concerns": elderly_concerns[:2],  # Top 2 concerns
                "pattern_match_confidence": max([p["similarity"] for p in similar_patterns])
            }
            
            return {
                "enhancement": enhancement,
                "similar_patterns": similar_patterns
            }
            
        except Exception as e:
            print(f"⚠️ Warning: Fraud analysis enhancement failed: {e}")
            return {"enhancement": None, "similar_patterns": []}