"""
NEURA v2.4 - Advanced NLP Engine
Enhanced Natural Language Processing Module
Created by: Sajjad Baloch
"""

import re
from collections import Counter
from datetime import datetime

try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    
    # Download required NLTK data
    required_downloads = [
        'vader_lexicon', 'punkt', 'stopwords', 
        'wordnet', 'averaged_perceptron_tagger', 'omw-1.4'
    ]
    for item in required_downloads:
        try:
            nltk.download(item, quiet=True)
        except:
            pass
    
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


class AdvancedNLPEngine:
    """
    Advanced NLP Processing Engine with multiple capabilities:
    - Sentiment Analysis
    - Intent Classification
    - Entity Recognition
    - Keyword Extraction
    - Topic Modeling
    - Question Type Detection
    """
    
    def __init__(self):
        self.nlp_available = NLP_AVAILABLE
        
        if self.nlp_available:
            self.sia = SentimentIntensityAnalyzer()
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        
        # Define intent patterns
        self.intent_patterns = {
            "greeting": {
                "keywords": ["hello", "hi", "hey", "greetings", "salam", "assalam", "good morning", "good evening"],
                "patterns": [r"\b(hi|hello|hey)\b", r"good (morning|evening|afternoon)"]
            },
            "farewell": {
                "keywords": ["bye", "goodbye", "see you", "exit", "quit", "later", "khuda hafiz"],
                "patterns": [r"\b(bye|goodbye)\b", r"see you"]
            },
            "question": {
                "keywords": ["what", "when", "where", "who", "why", "how", "which", "kya", "kab", "kahan"],
                "patterns": [r"^(what|when|where|who|why|how|which)", r"\?$"]
            },
            "help": {
                "keywords": ["help", "assist", "support", "guide", "madad", "how to"],
                "patterns": [r"\bhelp\b", r"how (do|can|to)"]
            },
            "fee_inquiry": {
                "keywords": ["fee", "payment", "tuition", "cost", "price", "charges", "installment"],
                "patterns": [r"\bfee\b", r"\bpayment\b", r"\bcost\b"]
            },
            "exam_inquiry": {
                "keywords": ["exam", "test", "paper", "midterm", "final", "quiz", "assessment"],
                "patterns": [r"\bexam\b", r"\btest\b", r"mid ?term", r"final"]
            },
            "attendance_inquiry": {
                "keywords": ["attendance", "present", "absent", "leave", "hazri"],
                "patterns": [r"\battendance\b", r"\babsent\b"]
            },
            "admission_inquiry": {
                "keywords": ["admission", "enroll", "join", "apply", "registration", "dakhla"],
                "patterns": [r"\badmission\b", r"\benroll\b", r"\bapply\b"]
            },
            "schedule_inquiry": {
                "keywords": ["schedule", "timetable", "class", "timing", "when is"],
                "patterns": [r"\bschedule\b", r"\btimetable\b", r"when is"]
            },
            "location_inquiry": {
                "keywords": ["where", "location", "address", "campus", "kahan"],
                "patterns": [r"\bwhere\b", r"\blocation\b", r"\baddress\b"]
            },
            "complaint": {
                "keywords": ["problem", "issue", "complaint", "not working", "error", "shikayat"],
                "patterns": [r"\bproblem\b", r"\bissue\b", r"not working"]
            },
            "appreciation": {
                "keywords": ["thank", "thanks", "appreciate", "great", "awesome", "shukriya"],
                "patterns": [r"\bthank\b", r"\bgreat\b", r"\bawesome\b"]
            }
        }
        
        # Question type patterns
        self.question_types = {
            "what": r"^what\b",
            "when": r"^when\b",
            "where": r"^where\b",
            "who": r"^who\b",
            "why": r"^why\b",
            "how": r"^how\b",
            "which": r"^which\b",
            "yes_no": r"^(is|are|do|does|can|could|will|would|should)\b"
        }
        
    def analyze_sentiment(self, text):
        """
        Perform sentiment analysis
        Returns: (sentiment_label, confidence_score, detailed_scores)
        """
        if not self.nlp_available:
            return "neutral", 0.0, {}
        
        try:
            scores = self.sia.polarity_scores(text)
            compound = scores['compound']
            
            # Determine sentiment
            if compound >= 0.05:
                sentiment = "positive"
            elif compound <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return sentiment, abs(compound), scores
        except:
            return "neutral", 0.0, {}
    
    def detect_intent(self, text):
        """
        Detect user intent with confidence score
        Returns: (intent, confidence)
        """
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, data in self.intent_patterns.items():
            score = 0
            
            # Check keywords
            keyword_matches = sum(1 for keyword in data["keywords"] if keyword in text_lower)
            score += keyword_matches * 2
            
            # Check patterns
            pattern_matches = sum(1 for pattern in data["patterns"] if re.search(pattern, text_lower))
            score += pattern_matches * 3
            
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[best_intent]
            confidence = min(max_score / 10.0, 1.0)  # Normalize to 0-1
            return best_intent, confidence
        
        return "general", 0.5
    
    def extract_keywords(self, text, top_n=5):
        """
        Extract important keywords using TF-IDF-like approach
        Returns: list of (keyword, importance_score)
        """
        if not self.nlp_available:
            words = text.lower().split()
            return [(w, 1.0) for w in words[:top_n] if len(w) > 3]
        
        try:
            # Tokenize and clean
            tokens = word_tokenize(text.lower())
            
            # Remove stopwords and non-alphabetic tokens
            filtered_tokens = [
                self.lemmatizer.lemmatize(token) 
                for token in tokens 
                if token.isalnum() and token not in self.stop_words and len(token) > 2
            ]
            
            # Count frequencies
            freq_dist = Counter(filtered_tokens)
            
            # Get top keywords
            top_keywords = freq_dist.most_common(top_n)
            
            # Normalize scores
            if top_keywords:
                max_freq = top_keywords[0][1]
                return [(word, freq/max_freq) for word, freq in top_keywords]
            
            return []
        except:
            words = text.lower().split()
            return [(w, 1.0) for w in words[:top_n] if len(w) > 3]
    
    def extract_entities(self, text):
        """
        Extract named entities using pattern matching
        Returns: dict of entity types and their values
        """
        entities = {
            "dates": [],
            "times": [],
            "emails": [],
            "phones": [],
            "urls": [],
            "money": [],
            "percentages": []
        }
        
        # Date patterns
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b'
        ]
        for pattern in date_patterns:
            entities["dates"].extend(re.findall(pattern, text, re.IGNORECASE))
        
        # Time patterns
        entities["times"] = re.findall(r'\b\d{1,2}:\d{2}\s*(am|pm|AM|PM)?\b', text)
        
        # Email
        entities["emails"] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        # Phone
        entities["phones"] = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        
        # URLs
        entities["urls"] = re.findall(r'https?://[^\s]+', text)
        
        # Money
        entities["money"] = re.findall(r'\$?\d+(?:,\d{3})*(?:\.\d{2})?', text)
        
        # Percentages
        entities["percentages"] = re.findall(r'\d+(?:\.\d+)?%', text)
        
        # Remove empty lists
        return {k: v for k, v in entities.items() if v}
    
    def detect_question_type(self, text):
        """
        Detect the type of question being asked
        Returns: question_type or None
        """
        text_lower = text.lower().strip()
        
        for q_type, pattern in self.question_types.items():
            if re.search(pattern, text_lower):
                return q_type
        
        return None
    
    def analyze_complexity(self, text):
        """
        Analyze text complexity
        Returns: dict with complexity metrics
        """
        if not self.nlp_available:
            return {
                "word_count": len(text.split()),
                "char_count": len(text),
                "complexity": "medium"
            }
        
        try:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            
            # Determine complexity
            if avg_word_length > 6 or avg_sentence_length > 20:
                complexity = "high"
            elif avg_word_length > 4 or avg_sentence_length > 12:
                complexity = "medium"
            else:
                complexity = "low"
            
            return {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "char_count": len(text),
                "avg_word_length": round(avg_word_length, 2),
                "avg_sentence_length": round(avg_sentence_length, 2),
                "complexity": complexity
            }
        except:
            return {
                "word_count": len(text.split()),
                "char_count": len(text),
                "complexity": "medium"
            }
    
    def get_comprehensive_analysis(self, text):
        """
        Perform comprehensive NLP analysis
        Returns: dict with all analysis results
        """
        sentiment, sent_score, sent_details = self.analyze_sentiment(text)
        intent, intent_conf = self.detect_intent(text)
        keywords = self.extract_keywords(text)
        entities = self.extract_entities(text)
        question_type = self.detect_question_type(text)
        complexity = self.analyze_complexity(text)
        
        return {
            "sentiment": {
                "label": sentiment,
                "score": sent_score,
                "details": sent_details
            },
            "intent": {
                "label": intent,
                "confidence": intent_conf
            },
            "keywords": keywords,
            "entities": entities,
            "question_type": question_type,
            "complexity": complexity,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_response_suggestions(self, analysis):
        """
        Generate response suggestions based on analysis
        Returns: list of suggestion strings
        """
        suggestions = []
        
        intent = analysis["intent"]["label"]
        sentiment = analysis["sentiment"]["label"]
        
        # Intent-based suggestions
        if intent == "greeting":
            suggestions.append("Respond with a warm greeting")
        elif intent == "help":
            suggestions.append("Provide helpful guidance or menu options")
        elif intent == "complaint":
            suggestions.append("Show empathy and offer solutions")
        elif intent == "appreciation":
            suggestions.append("Acknowledge gratitude warmly")
        
        # Sentiment-based suggestions
        if sentiment == "negative":
            suggestions.append("Use empathetic tone")
        elif sentiment == "positive":
            suggestions.append("Match the positive energy")
        
        # Question type suggestions
        if analysis["question_type"]:
            q_type = analysis["question_type"]
            if q_type == "yes_no":
                suggestions.append("Provide clear yes/no answer first")
            elif q_type in ["what", "when", "where", "who"]:
                suggestions.append(f"Provide specific {q_type} information")
        
        return suggestions


# Test the engine
if __name__ == "__main__":
    engine = AdvancedNLPEngine()
    
    test_queries = [
        "Hello! How are you doing today?",
        "What are the admission fees for BS Computer Science?",
        "When is the final exam scheduled?",
        "I'm having trouble with the online portal. It's not working!",
        "Thank you so much for your help!",
    ]
    
    print("=" * 80)
    print("NEURA v2.4 - Advanced NLP Engine Test")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 80)
        
        analysis = engine.get_comprehensive_analysis(query)
        
        print(f"😊 Sentiment: {analysis['sentiment']['label']} ({analysis['sentiment']['score']:.2f})")
        print(f"🎯 Intent: {analysis['intent']['label']} (confidence: {analysis['intent']['confidence']:.2f})")
        
        if analysis['keywords']:
            keywords_str = ", ".join([f"{kw} ({score:.2f})" for kw, score in analysis['keywords'][:3]])
            print(f"🔑 Keywords: {keywords_str}")
        
        if analysis['entities']:
            print(f"📍 Entities: {list(analysis['entities'].keys())}")
        
        if analysis['question_type']:
            print(f"❓ Question Type: {analysis['question_type']}")
        
        print(f"📊 Complexity: {analysis['complexity']['complexity']} "
              f"({analysis['complexity']['word_count']} words)")
        
        suggestions = engine.generate_response_suggestions(analysis)
        if suggestions:
            print(f"💡 Suggestions: {', '.join(suggestions)}")
    
    print("\n" + "=" * 80)
