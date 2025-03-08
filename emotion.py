import spacy
import json
from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        # Load SpaCy model (optional, for future topic extraction)
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load Pretrained Emotion Model
        self.emotion_model = pipeline("text-classification", model="monologg/bert-base-cased-goemotions-original", top_k=None)
        
        # Define emotion to activation mapping
        self.emotion_activation_mapping = {
            "anger": "High", "excitement": "High", "grief": "High", "surprise": "High", "amusement": "High",
            "annoyance": "Medium", "disgust": "Medium", "disappointment": "Medium", "disapproval": "Medium",
            "sadness": "Medium", "fear": "Medium", "remorse": "Medium", "desire": "Medium", "pride": "Medium",
            "joy": "Medium", "realization": "Medium", "confusion": "Medium", "embarrassment": "Medium", "nervousness": "Medium",
            "admiration": "Low", "caring": "Low", "optimism": "Low", "love": "Low", "curiosity": "Low",
            "gratitude": "Low", "approval": "Low", "relief": "Low", "neutral": "Low"
        }
    
    def map_emotion_to_activation(self, emotion):
        return self.emotion_activation_mapping.get(emotion.lower(), "Unknown")
    
    def analyze_feedback(self, feedback_text):
        # Step 1: Emotion Analysis
        emotions = self.emotion_model(feedback_text)
        sorted_emotions = sorted(emotions[0], key=lambda x: x['score'], reverse=True)
        
        # Extract primary & secondary emotions
        primary_emotion = sorted_emotions[0]
        secondary_emotion = sorted_emotions[1] if len(sorted_emotions) > 1 else None
        
        # Process emotions into required format
        emotion_result = {
            "emotions": {
                "primary": {
                    "emotion": primary_emotion["label"],
                    "activation": self.map_emotion_to_activation(primary_emotion["label"]),
                    "intensity": round(primary_emotion["score"], 6),
                },
                "secondary": {
                    "emotion": secondary_emotion["label"],
                    "activation": self.map_emotion_to_activation(secondary_emotion["label"]),
                    "intensity": round(secondary_emotion["score"], 6),
                } if secondary_emotion else None
            }
        }
        
        # Step 3: Categorize emotions by Activation Level
        categorized_emotions = {
            "High Activation": [],
            "Medium Activation": [],
            "Low Activation": []
        }
        
        for emotion_data in sorted_emotions:
            activation = self.map_emotion_to_activation(emotion_data["label"])
            categorized_emotions[f"{activation} Activation"].append({
                "emotion": emotion_data["label"],
                "intensity": round(emotion_data["score"], 6)
            })
        
        # Final JSON output
        final_output = {
            "emotion_analysis": emotion_result,
            "categorized_emotions": categorized_emotions
        }
        
        return json.dumps(final_output, indent=4)

# Example Usage
if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    test_feedback = "The delivery was incredibly fast and the quality was amazing! However, one of the clothing items didn't fit well."
    print(analyzer.analyze_feedback(test_feedback))
