# Flask Chatbot

This project is a Flask-based chatbot that integrates various tools like SpaCy for NLP, Scikit-learn for machine learning, BeautifulSoup for web scraping, and more. The chatbot is designed to provide mental health support by processing user input and responding appropriately.

## Features
- **NLP Processing**: Using SpaCy for understanding user inputs.
- **Sentiment Analysis**: Integrated using Scikit-learn to filter abusive language and promote positive conversations.
- **Web Scraping**: Using BeautifulSoup to fetch data from mental health websites.
- **Flask Framework**: To run the chatbot as a web service.
- **API Integration**: Allows interaction with external APIs to enhance responses.

## Prerequisites
Before running the application, ensure that you have Python installed. You can download it from [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/zakikhan000/
   cd flask_chatbot

   pip install -r requirements.txt
python -m spacy download en_core_web_sm
