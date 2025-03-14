# 📝 CustomerVoice : Customer Feedback Analysis System

- My code for Survey Sparrow Hackathon.
- An AI-powered system that processes customer feedback to extract emotions, identify topics, and compute an overall sentiment score (**Adorescore**). This helps businesses gain insights into customer sentiment and take data-driven actions to improve their services.

## 🚀 Features
- **Emotion Detection**: Uses a BERT-based transformer to classify emotions.
- **Topic Analysis**: Extracts main topics & subtopics using SpaCy NLP.
- **Adorescore Calculation**: Computes a sentiment score (-100 to +100) based on emotions & topic relevance.
- **Interactive UI**: Built with **Streamlit** for real-time feedback analysis.
- **Data Visualization**: Radar charts & detailed breakdowns for sentiment insights.

## 🏗️ System Architecture
The system consists of three core modules:
1. **Emotion Detection (`emotion.py`)** - Identifies emotions & activation levels.
2. **Topic Analysis (`topic.py`)** - Extracts topics & assigns relevance scores.
3. **Adorescore Calculation (`adorescore.py`)** - Computes sentiment scores.

## 🔧 Tech Stack
- **Programming Language**: Python
- **Frontend**: Streamlit
- **Machine Learning Model**: BERT-based Transformer (for emotion classification)
- **NLP**: SpaCy (for topic extraction)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (for radar charts & sentiment analysis)
- **Deployment**: Streamlit Cloud / Local Server
- **Version Control**: Git & GitHub

## 📦 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/customer-feedback-analysis.git
cd customer-feedback-analysis
pip install -r requirements.txt
```

## 🚀 Usage
Run the Streamlit application:
```bash
streamlit run app.py
```
- Input customer feedback.
- View detected emotions, topics, and Adorescore.
- Analyze sentiment trends using radar charts.



## 🔮 Future Enhancements
- **Optimize emotion detection** using reinforcement learning.
- **Enhance topic detection** with contextual embeddings.
- **Real-time visualization** with dynamic sentiment tracking.
- **Develop an API** for enterprise integration.

## 🤝 Contributing
Pull requests are welcome! Open an issue for feature suggestions.
