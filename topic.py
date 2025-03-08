import spacy
import json

class TopicAnalyzer:
    def __init__(self):
        """Initialize SpaCy model and define topic hierarchy."""
        self.nlp = spacy.load("en_core_web_md")  

        # Topic Hierarchy
        self.topic_hierarchy = {
            "Delivery": ["Fast Delivery", "Quick Delivery", "Late Delivery", "Free Delivery", "Damaged Package"],
            "Quality": ["Material Quality", "Product Durability", "Build Quality", "Authenticity", "Defective Product"],
            "Clothes": ["Size", "Fit", "Color", "Design", "Fabric Quality", "Comfort"],
            "Customer Service": ["Helpful Support", "Rude Staff", "Slow Response", "Issue Resolution", "Refund Process"],
            "Pricing": ["Expensive", "Affordable", "Discounts", "Overpriced", "Value for Money"],
            "Usability": ["Easy to Use", "Complicated", "Intuitive Design", "Feature-Rich"],
            "Experience": ["Satisfaction", "Disappointment", "Exceeded Expectations", "Frustration"],
            "Packaging": ["Secure Packaging", "Damaged Packaging", "Eco-Friendly Packaging"],
            "Returns": ["Easy Returns", "Difficult Returns", "Refund Process", "Exchange Policy"]
        }


        # Similarity Thresholds
        self.topic_threshold = 0.8  
        self.subtopic_threshold = 0.5  # ✅ Exclude subtopics if below this

    def extract_keywords(self, text):
        """Extracts relevant keywords (nouns, adjectives) from feedback."""
        doc = self.nlp(text.lower())
        keywords = {token.text for token in doc if token.pos_ in {"NOUN", "ADJ"}}
        return keywords  

    def match_main_topic(self, keywords):
        """Matches keywords to main topics and selects only the most relevant subtopic."""
        main_topics = []
        subtopics = {}

        for main_topic, subtopic_list in self.topic_hierarchy.items():
            main_topic_doc = self.nlp(main_topic.lower())

            # Compute similarity between extracted keywords and main topic
            topic_similarity = max((self.nlp(keyword).similarity(main_topic_doc) for keyword in keywords), default=0)

            #print(f"Main Topic: {main_topic}, Similarity: {topic_similarity:.4f}")  # Debugging

            if topic_similarity >= self.topic_threshold or main_topic.lower() in keywords:
                main_topics.append(main_topic)

                best_subtopic = None
                best_similarity = 0
                for subtopic in subtopic_list:
                    subtopic_doc = self.nlp(subtopic.lower())

                    # Compute similarity between extracted keywords and subtopic
                    subtopic_similarity = max((self.nlp(keyword).similarity(subtopic_doc) for keyword in keywords), default=0)

                    #print(f"  Subtopic: {subtopic}, Similarity: {subtopic_similarity:.4f}")  # Debugging

                    if subtopic_similarity > best_similarity:
                        best_subtopic = subtopic
                        best_similarity = subtopic_similarity

                # ✅ Exclude subtopics if best match is below the threshold
                if best_subtopic and best_similarity >= self.subtopic_threshold:
                    subtopics[main_topic] = [best_subtopic]

        return {
            "main": main_topics,
            "subtopics": subtopics
        }

    def analyze_feedback(self, feedback_text):
        """Extracts topics & subtopics from feedback."""
        keywords = self.extract_keywords(feedback_text)
        #print(f"Extracted Keywords: {keywords}")  # Debugging
        matched_topics = self.match_main_topic(keywords)

        final_output = {
            "feedback": feedback_text,
            "topics": matched_topics
        }

        return json.dumps(final_output, indent=4)

# ==== Example Usage ====
if __name__ == "__main__":
    analyzer = TopicAnalyzer()
    
    feedback_text = "The delivery was incredibly fast and the quality was amazing! However, one of the clothing items didn't fit well."
    result = analyzer.analyze_feedback(feedback_text)
    print(result)
