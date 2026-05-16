"""
Intent Classifier
NLP pipeline using spaCy + TF-IDF + Naive Bayes for disaster intent recognition
"""

import re
import logging
from typing import Tuple, Dict, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

import spacy
from spacy.util import is_package

from .training_data import TRAINING_DATA, INTENT_METADATA, SEVERITY_KEYWORDS

logger = logging.getLogger(__name__)

class IntentClassifier:
    """
    NLP-based intent classifier for disaster emergency queries.
    Uses spaCy for preprocessing/NER and TF-IDF + Naive Bayes for classification.
    """
    
    def __init__(self, confidence_threshold: float = 0.25):
        self.confidence_threshold = confidence_threshold
        self.pipeline = None
        self.label_encoder = LabelEncoder()
        self._is_trained = False
        
        # Load spaCy model
        try:
            if not is_package('en_core_web_sm'):
                import subprocess
                subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)
            self.nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            self.nlp = None
            
        # Train on initialization
        self.train()
    
    def preprocess(self, text: str) -> str:
        """
        Clean and normalize input text using spaCy.
        - Lemmatize tokens
        - Remove stopwords, punctuation
        """
        if not text or not isinstance(text, str) or not self.nlp:
            return ""
        
        doc = self.nlp(text)
        processed = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return ' '.join(processed) if processed else text
    
    def train(self):
        """Train the classification pipeline on the training corpus"""
        try:
            texts = [self.preprocess(item[0]) for item in TRAINING_DATA]
            labels = [item[1] for item in TRAINING_DATA]
            
            # Encode labels
            self.label_encoder.fit(labels)
            encoded_labels = self.label_encoder.transform(labels)
            
            # Build TF-IDF + Naive Bayes pipeline
            self.pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    min_df=1,
                    sublinear_tf=True
                )),
                ('clf', MultinomialNB(alpha=0.1))
            ])
            
            self.pipeline.fit(texts, encoded_labels)
            self._is_trained = True
            logger.info(f"Intent classifier trained on {len(texts)} samples, "
                        f"{len(self.label_encoder.classes_)} intents")
        
        except Exception as e:
            logger.error(f"Training failed: {e}")
            self._is_trained = False
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify user message into intent.
        Returns: (intent_label, confidence_score)
        """
        if not self._is_trained or not text:
            return "general", 0.0
        
        try:
            processed = self.preprocess(text)
            if not processed:
                return "general", 0.0
            
            # Get probability predictions
            proba = self.pipeline.predict_proba([processed])[0]
            max_confidence = float(max(proba))
            predicted_idx = proba.argmax()
            
            # Decode label
            intent = self.label_encoder.inverse_transform([predicted_idx])[0]
            
            # Apply threshold
            if max_confidence < self.confidence_threshold:
                intent = "general"
            
            return intent, max_confidence
        
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return "general", 0.0
    
    def extract_severity(self, text: str) -> str:
        """
        Extract severity level from text using keyword matching.
        Returns: 'critical', 'high', 'medium', or 'low'
        """
        text_lower = text.lower()
        
        for severity, keywords in SEVERITY_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return severity
        
        return "medium"
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract relevant entities from emergency message using spaCy NER.
        Returns dict with disaster_type, severity, location hints.
        """
        intent, confidence = self.classify(text)
        severity = self.extract_severity(text)
        
        # Override severity for critical intents
        meta = INTENT_METADATA.get(intent, {})
        if meta.get('severity_default') == 'critical' and severity == 'low':
            severity = 'high'
        
        # Advanced location extraction using spaCy NER
        location = None
        if self.nlp:
            doc = self.nlp(text)
            locations = [ent.text.capitalize() for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'FAC']]
            if locations:
                location = locations[0]
                
        # Fallback to simple logic if spaCy fails or doesn't find anything
        if not location:
            words = text.lower().split()
            location_prepositions = {'near', 'in', 'at', 'around', 'from'}
            for i, word in enumerate(words):
                if word in location_prepositions and i + 1 < len(words):
                    location = words[i + 1].capitalize()
                    break
        
        return {
            'intent': intent,
            'confidence': confidence,
            'severity': severity,
            'location': location,
            'needs_escalation': meta.get('escalate', False) and severity in ['high', 'critical'],
            'disaster_type': meta.get('label', 'General'),
            'icon': meta.get('icon', '💬')
        }
    
    def get_intent_metadata(self, intent: str) -> Dict:
        """Get metadata for a given intent"""
        return INTENT_METADATA.get(intent, INTENT_METADATA.get('general', {}))


# Singleton instance
_classifier_instance = None


def get_classifier() -> IntentClassifier:
    """Get or create classifier singleton"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier()
    return _classifier_instance
