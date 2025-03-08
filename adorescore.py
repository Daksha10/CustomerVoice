import json
from emotion import EmotionAnalyzer
from topic import TopicAnalyzer

class AdorescoreCalculator:
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer()
        self.topic_analyzer = TopicAnalyzer()

        # Define emotion polarity (positive or negative impact)
        self.positive_emotions = {"joy", "admiration", "love", "approval", "gratitude", "optimism", "relief", "caring"}
        self.negative_emotions = {"disappointment", "anger", "sadness", "fear", "remorse", "disgust", "annoyance", "grief", "nervousness"}

        # Topic base weights (normalized later)
        self.topic_weights = {
            "Delivery": 0.15,
            "Quality": 0.20,
            "Clothes": 0.10,
            "Customer Service": 0.15,
            "Pricing": 0.10,
            "Usability": 0.10,
            "Experience": 0.10,
            "Packaging": 0.05,
            "Returns": 0.05
        }

    def analyze_feedback(self, feedback_text):
        """Handles emotion and topic analysis with error handling."""
        try:
            emotion_result = self.emotion_analyzer.analyze_feedback(feedback_text)
            topic_result = self.topic_analyzer.analyze_feedback(feedback_text)

            # Convert JSON string responses to dictionaries if needed
            if isinstance(emotion_result, str):
                emotion_result = json.loads(emotion_result)
            if isinstance(topic_result, str):
                topic_result = json.loads(topic_result)

            return emotion_result, topic_result

        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            print(f"Error processing feedback analysis: {e}")
            return None, None

    def compute_emotion_impact(self, emotion_name, intensity, activation, weight_factor):
        """Calculates weighted emotion impact based on activation level."""
        activation_weights = {"Low": 0.7, "Medium": 1.0, "High": 1.3}
        activation_factor = activation_weights.get(activation, 1.0)
        
        impact = 100 * intensity * weight_factor * activation_factor
        return impact if emotion_name in self.positive_emotions else -impact

    def calculate_adorescore(self, feedback_text):
        """Computes the Adorescore based on emotions and topic relevance."""

        # Analyze emotions & topics
        emotion_result, topic_result = self.analyze_feedback(feedback_text)

        if not emotion_result or not topic_result:
            return {"error": "Failed to analyze emotions or topics."}

        # Extract emotion data
        emotion_data = emotion_result.get("emotion_analysis", {}).get("emotions", {})
        primary_emotion = emotion_data.get("primary", {})
        secondary_emotion = emotion_data.get("secondary", {})

        # Extract topic data
        main_topics = topic_result.get("topics", {}).get("main", [])
        subtopics = topic_result.get("topics", {}).get("subtopics", {})

        # Compute Adorescore
        adorescore = 0
        emotion_contributions = {}

        # Process primary emotion
        if primary_emotion:
            impact = self.compute_emotion_impact(
                primary_emotion.get("emotion", ""),
                primary_emotion.get("intensity", 0),
                primary_emotion.get("activation", ""),
                weight_factor=1.0
            )
            adorescore += impact
            emotion_contributions[primary_emotion.get("emotion", "")] = round(impact, 4)

        # Process secondary emotion
        if secondary_emotion:
            impact = self.compute_emotion_impact(
                secondary_emotion.get("emotion", ""),
                secondary_emotion.get("intensity", 0),
                secondary_emotion.get("activation", ""),
                weight_factor=0.5
            )
            adorescore += impact
            emotion_contributions[secondary_emotion.get("emotion", "")] = round(impact, 4)

        # Normalize Adorescore
        adorescore = round(max(-100, min(100, adorescore)), 4)

        # Compute topic-based breakdown
        topic_breakdown = self.compute_topic_breakdown(adorescore, main_topics)

        # Output final result
        return {
            "emotions": {
                "primary": {
                    "emotion": primary_emotion.get("emotion", ""),
                    "activation": primary_emotion.get("activation", ""),
                    "intensity": round(primary_emotion.get("intensity", 0), 4)
                },
                "secondary": {
                    "emotion": secondary_emotion.get("emotion", ""),
                    "activation": secondary_emotion.get("activation", ""),
                    "intensity": round(secondary_emotion.get("intensity", 0), 4)
                }
            },
            "topics": {
                "main": main_topics,
                "subtopics": subtopics
            },
            "adorescore": {
                "overall": adorescore,
                "breakdown": topic_breakdown
            }
        }

    def compute_topic_breakdown(self, adorescore, main_topics):
        """Distributes the Adorescore across relevant topics based on their weights."""
        topic_breakdown = {}
        total_weight = sum(self.topic_weights.get(topic, 0) for topic in main_topics) or 1

        for topic in main_topics:
            weight = self.topic_weights.get(topic, 0) / total_weight
            topic_breakdown[topic] = round(adorescore * weight, 4)

        return topic_breakdown


# Example Usage
if __name__ == "__main__":
    calculator = AdorescoreCalculator()
    test_feedback = "The delivery was incredibly fast and the quality was amazing! However, one of the clothing items didn't fit well."
    result = calculator.calculate_adorescore(test_feedback)
    print(json.dumps(result, indent=4))
