#!/usr/bin/env python3
"""
LOTL-APEX Identity Engine
Learns and mirrors user's digital identity and behavioral patterns
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import re
from collections import defaultdict, Counter
import numpy as np

@dataclass
class InteractionPattern:
    timestamp: datetime
    command_type: str
    context: str
    success: bool
    response_time: float
    user_satisfaction: Optional[int] = None  # 1-5 rating

@dataclass
class CommunicationStyle:
    vocabulary_complexity: float  # 0-1 scale
    sentence_length_avg: float
    technical_terms_ratio: float
    preferred_tone: str  # formal, casual, technical
    common_phrases: List[str]
    communication_patterns: Dict[str, float]

@dataclass
class DecisionPattern:
    context: str
    options_considered: List[str]
    chosen_option: str
    reasoning: str
    outcome_satisfaction: float
    timestamp: datetime

@dataclass
class UserProfile:
    user_id: str
    communication_style: CommunicationStyle
    decision_patterns: List[DecisionPattern]
    interaction_patterns: List[InteractionPattern]
    preferences: Dict[str, Any]
    habits: Dict[str, Any]
    expertise_areas: List[str]
    learning_speed: float
    created_at: datetime
    updated_at: datetime

class IdentityEngine:
    """Learns and mirrors user's digital identity"""
    
    def __init__(self, db_path: str = "identity.db"):
        self.db_path = db_path
        self.user_profile: Optional[UserProfile] = None
        self.interaction_buffer: List[InteractionPattern] = []
        self.learning_threshold = 10  # Minimum interactions before pattern recognition
        
        self._init_database()
        self._load_user_profile()
    
    def _init_database(self):
        """Initialize SQLite database for identity storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for identity data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                profile_data TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                timestamp TIMESTAMP,
                command_type TEXT,
                context TEXT,
                success BOOLEAN,
                response_time REAL,
                user_satisfaction INTEGER,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decision_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                context TEXT,
                options_considered TEXT,
                chosen_option TEXT,
                reasoning TEXT,
                outcome_satisfaction REAL,
                timestamp TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_user_profile(self, user_id: str = "hanis_default"):
        """Load existing user profile or create new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT profile_data FROM user_profiles WHERE user_id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        
        if result:
            profile_data = json.loads(result[0])
            # Reconstruct UserProfile from stored data
            self.user_profile = self._deserialize_profile(profile_data)
        else:
            # Create new profile with defaults
            self.user_profile = self._create_default_profile(user_id)
            self._save_user_profile()
        
        conn.close()
    
    def _create_default_profile(self, user_id: str) -> UserProfile:
        """Create default user profile"""
        default_comm_style = CommunicationStyle(
            vocabulary_complexity=0.5,
            sentence_length_avg=15.0,
            technical_terms_ratio=0.3,
            preferred_tone="technical",
            common_phrases=[],
            communication_patterns={}
        )
        
        return UserProfile(
            user_id=user_id,
            communication_style=default_comm_style,
            decision_patterns=[],
            interaction_patterns=[],
            preferences={
                "interface_style": "terminal",
                "verbosity_level": "detailed",
                "confirmation_required": True,
                "auto_execute_safe_commands": False
            },
            habits={
                "active_hours": [9, 17],  # 9 AM to 5 PM
                "preferred_work_blocks": 120,  # 2 hours
                "break_frequency": 30  # minutes
            },
            expertise_areas=["cybersecurity", "ai", "development"],
            learning_speed=0.7,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def record_interaction(self, command_type: str, context: str, 
                          success: bool, response_time: float,
                          user_satisfaction: Optional[int] = None):
        """Record user interaction for pattern learning"""
        interaction = InteractionPattern(
            timestamp=datetime.now(),
            command_type=command_type,
            context=context,
            success=success,
            response_time=response_time,
            user_satisfaction=user_satisfaction
        )
        
        self.interaction_buffer.append(interaction)
        
        # Analyze patterns if we have enough data
        if len(self.interaction_buffer) >= self.learning_threshold:
            self._analyze_interaction_patterns()
            self._update_user_preferences()
            self._save_interactions_to_db()
            self.interaction_buffer.clear()
    
    def record_decision(self, context: str, options: List[str], 
                       chosen: str, reasoning: str, satisfaction: float):
        """Record user decision for pattern learning"""
        decision = DecisionPattern(
            context=context,
            options_considered=options,
            chosen_option=chosen,
            reasoning=reasoning,
            outcome_satisfaction=satisfaction,
            timestamp=datetime.now()
        )
        
        self.user_profile.decision_patterns.append(decision)
        self._analyze_decision_patterns()
        self._save_user_profile()
    
    def analyze_communication_style(self, text: str) -> Dict[str, Any]:
        """Analyze communication style from user input"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Calculate metrics
        vocab_complexity = self._calculate_vocabulary_complexity(words)
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        technical_ratio = self._calculate_technical_ratio(words)
        
        # Update communication style
        style = self.user_profile.communication_style
        
        # Exponential moving average for smooth updates
        alpha = 0.1
        style.vocabulary_complexity = (1 - alpha) * style.vocabulary_complexity + alpha * vocab_complexity
        style.sentence_length_avg = (1 - alpha) * style.sentence_length_avg + alpha * avg_sentence_length
        style.technical_terms_ratio = (1 - alpha) * style.technical_terms_ratio + alpha * technical_ratio
        
        # Extract common phrases
        self._extract_common_phrases(text)
        
        return {
            "vocabulary_complexity": vocab_complexity,
            "sentence_length": avg_sentence_length,
            "technical_ratio": technical_ratio,
            "detected_tone": self._detect_tone(text)
        }
    
    def _calculate_vocabulary_complexity(self, words: List[str]) -> float:
        """Calculate vocabulary complexity (0-1 scale)"""
        if not words:
            return 0.0
        
        # Simple heuristic: longer words = more complex
        avg_word_length = np.mean([len(word) for word in words])
        unique_words_ratio = len(set(words)) / len(words)
        
        # Normalize to 0-1 scale
        complexity = min(1.0, (avg_word_length - 3) / 7 + unique_words_ratio * 0.3)
        return max(0.0, complexity)
    
    def _calculate_technical_ratio(self, words: List[str]) -> float:
        """Calculate ratio of technical terms"""
        technical_keywords = {
            'api', 'database', 'algorithm', 'function', 'variable', 'class',
            'method', 'object', 'array', 'string', 'integer', 'boolean',
            'server', 'client', 'protocol', 'framework', 'library', 'module',
            'docker', 'kubernetes', 'aws', 'cloud', 'microservice', 'devops',
            'security', 'encryption', 'authentication', 'authorization',
            'vulnerability', 'exploit', 'malware', 'firewall', 'vpn'
        }
        
        if not words:
            return 0.0
        
        technical_count = sum(1 for word in words if word.lower() in technical_keywords)
        return technical_count / len(words)
    
    def _detect_tone(self, text: str) -> str:
        """Detect communication tone"""
        formal_indicators = ['please', 'kindly', 'would you', 'could you', 'thank you']
        casual_indicators = ['hey', 'cool', 'awesome', 'yeah', 'ok', 'sure']
        technical_indicators = ['implement', 'configure', 'optimize', 'debug', 'analyze']
        
        text_lower = text.lower()
        
        formal_score = sum(1 for indicator in formal_indicators if indicator in text_lower)
        casual_score = sum(1 for indicator in casual_indicators if indicator in text_lower)
        technical_score = sum(1 for indicator in technical_indicators if indicator in text_lower)
        
        scores = {'formal': formal_score, 'casual': casual_score, 'technical': technical_score}
        return max(scores, key=scores.get)
    
    def _extract_common_phrases(self, text: str):
        """Extract and track common phrases"""
        # Simple n-gram extraction (2-3 words)
        words = text.lower().split()
        
        for i in range(len(words) - 1):
            bigram = ' '.join(words[i:i+2])
            if bigram not in self.user_profile.communication_style.common_phrases:
                if len(self.user_profile.communication_style.common_phrases) < 50:  # Limit size
                    self.user_profile.communication_style.common_phrases.append(bigram)
    
    def _analyze_interaction_patterns(self):
        """Analyze patterns in user interactions"""
        if not self.interaction_buffer:
            return
        
        # Analyze success rates by command type
        command_success = defaultdict(list)
        for interaction in self.interaction_buffer:
            command_success[interaction.command_type].append(interaction.success)
        
        # Update preferences based on success patterns
        for command_type, successes in command_success.items():
            success_rate = sum(successes) / len(successes)
            
            # If success rate is low, user might need more guidance
            if success_rate < 0.7:
                self.user_profile.preferences[f"{command_type}_guidance"] = True
            else:
                self.user_profile.preferences[f"{command_type}_guidance"] = False
    
    def _analyze_decision_patterns(self):
        """Analyze patterns in user decisions"""
        if len(self.user_profile.decision_patterns) < 5:
            return
        
        # Analyze recent decisions (last 10)
        recent_decisions = self.user_profile.decision_patterns[-10:]
        
        # Find patterns in decision making
        context_preferences = defaultdict(list)
        for decision in recent_decisions:
            context_preferences[decision.context].append(decision.chosen_option)
        
        # Update preferences based on decision patterns
        for context, choices in context_preferences.items():
            most_common = Counter(choices).most_common(1)
            if most_common:
                self.user_profile.preferences[f"preferred_{context}"] = most_common[0][0]
    
    def _update_user_preferences(self):
        """Update user preferences based on interaction patterns"""
        if not self.interaction_buffer:
            return
        
        # Analyze response times to adjust interface speed
        avg_response_time = np.mean([i.response_time for i in self.interaction_buffer])
        
        if avg_response_time > 5.0:  # Slow responses
            self.user_profile.preferences["interface_speed"] = "detailed"
        elif avg_response_time < 1.0:  # Fast responses
            self.user_profile.preferences["interface_speed"] = "rapid"
        else:
            self.user_profile.preferences["interface_speed"] = "normal"
        
        # Analyze satisfaction ratings
        satisfaction_ratings = [i.user_satisfaction for i in self.interaction_buffer 
                              if i.user_satisfaction is not None]
        
        if satisfaction_ratings:
            avg_satisfaction = np.mean(satisfaction_ratings)
            if avg_satisfaction < 3.0:
                # User is not satisfied, increase verbosity
                self.user_profile.preferences["verbosity_level"] = "detailed"
            elif avg_satisfaction > 4.0:
                # User is very satisfied, can reduce verbosity
                self.user_profile.preferences["verbosity_level"] = "concise"
    
    def get_personalized_response_style(self) -> Dict[str, Any]:
        """Get personalized response style based on learned patterns"""
        style = self.user_profile.communication_style
        prefs = self.user_profile.preferences
        
        return {
            "tone": style.preferred_tone,
            "verbosity": prefs.get("verbosity_level", "normal"),
            "technical_level": min(1.0, style.technical_terms_ratio + 0.2),
            "formality": "high" if style.vocabulary_complexity > 0.7 else "medium",
            "response_speed": prefs.get("interface_speed", "normal"),
            "include_examples": prefs.get("verbosity_level") == "detailed",
            "confirm_actions": prefs.get("confirmation_required", True)
        }
    
    def predict_user_preference(self, context: str, options: List[str]) -> str:
        """Predict user preference based on historical patterns"""
        # Look for similar contexts in decision history
        similar_decisions = [
            d for d in self.user_profile.decision_patterns
            if context.lower() in d.context.lower() or d.context.lower() in context.lower()
        ]
        
        if similar_decisions:
            # Return most common choice in similar contexts
            choices = [d.chosen_option for d in similar_decisions]
            return Counter(choices).most_common(1)[0][0]
        
        # Fallback to general preferences
        pref_key = f"preferred_{context.lower()}"
        return self.user_profile.preferences.get(pref_key, options[0] if options else "")
    
    def _save_user_profile(self):
        """Save user profile to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        profile_data = self._serialize_profile(self.user_profile)
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles 
            (user_id, profile_data, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (
            self.user_profile.user_id,
            json.dumps(profile_data),
            self.user_profile.created_at.isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _save_interactions_to_db(self):
        """Save interaction buffer to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for interaction in self.interaction_buffer:
            cursor.execute('''
                INSERT INTO interactions 
                (user_id, timestamp, command_type, context, success, response_time, user_satisfaction)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.user_profile.user_id,
                interaction.timestamp.isoformat(),
                interaction.command_type,
                interaction.context,
                interaction.success,
                interaction.response_time,
                interaction.user_satisfaction
            ))
        
        conn.commit()
        conn.close()
    
    def _serialize_profile(self, profile: UserProfile) -> Dict[str, Any]:
        """Serialize user profile for storage"""
        return {
            "user_id": profile.user_id,
            "communication_style": asdict(profile.communication_style),
            "decision_patterns": [asdict(dp) for dp in profile.decision_patterns],
            "preferences": profile.preferences,
            "habits": profile.habits,
            "expertise_areas": profile.expertise_areas,
            "learning_speed": profile.learning_speed,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat()
        }
    
    def _deserialize_profile(self, data: Dict[str, Any]) -> UserProfile:
        """Deserialize user profile from storage"""
        comm_style = CommunicationStyle(**data["communication_style"])
        
        decision_patterns = []
        for dp_data in data.get("decision_patterns", []):
            dp_data["timestamp"] = datetime.fromisoformat(dp_data["timestamp"])
            decision_patterns.append(DecisionPattern(**dp_data))
        
        return UserProfile(
            user_id=data["user_id"],
            communication_style=comm_style,
            decision_patterns=decision_patterns,
            interaction_patterns=[],  # Loaded separately if needed
            preferences=data["preferences"],
            habits=data["habits"],
            expertise_areas=data["expertise_areas"],
            learning_speed=data["learning_speed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Get summary of learned identity"""
        if not self.user_profile:
            return {"error": "No user profile loaded"}
        
        return {
            "user_id": self.user_profile.user_id,
            "communication_style": {
                "complexity": self.user_profile.communication_style.vocabulary_complexity,
                "tone": self.user_profile.communication_style.preferred_tone,
                "technical_level": self.user_profile.communication_style.technical_terms_ratio
            },
            "preferences": self.user_profile.preferences,
            "expertise_areas": self.user_profile.expertise_areas,
            "decision_patterns_count": len(self.user_profile.decision_patterns),
            "learning_progress": {
                "interactions_recorded": len(self.user_profile.interaction_patterns),
                "learning_speed": self.user_profile.learning_speed,
                "profile_age_days": (datetime.now() - self.user_profile.created_at).days
            },
            "personalized_style": self.get_personalized_response_style()
        }

# Global identity engine instance
identity_engine = IdentityEngine()

def main():
    """Test the identity engine"""
    print("🧠 LOTL-APEX Identity Engine Test")
    
    # Simulate user interactions
    identity_engine.record_interaction(
        "file_operation", "analyze project structure", True, 2.3, 4
    )
    
    # Analyze communication style
    sample_text = "Please analyze the system configuration and optimize the performance parameters"
    style_analysis = identity_engine.analyze_communication_style(sample_text)
    print(f"Communication Style: {style_analysis}")
    
    # Get identity summary
    summary = identity_engine.get_identity_summary()
    print(f"Identity Summary: {json.dumps(summary, indent=2)}")

if __name__ == "__main__":
    main()
