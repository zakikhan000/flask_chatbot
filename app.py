from flask import Flask, request, jsonify
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import requests
from bs4 import BeautifulSoup
import os
import random

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

qa_data = [
    ("What is anxiety?", "Anxiety is a feeling of worry, nervousness, or unease about something."),
    ("What are the symptoms of depression?", "Symptoms include sadness, loss of interest, changes in sleep and appetite."),
    ("How can I cope with anxiety?", "Coping strategies include mindfulness, breathing exercises, and talking to a therapist."),
    ("What is cognitive behavioral therapy?", "CBT is a type of therapy that helps manage problems by changing thought patterns."),
    ("How can I relax?", "Relaxation techniques include deep breathing, progressive muscle relaxation, and meditation."),
]

preprocessed_questions = [preprocess_text(qa[0]) for qa in qa_data]
preprocessed_answers = [qa[1] for qa in qa_data]

def build_chatbot_model(X_train, y_train):
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    return model

\model = build_chatbot_model(preprocessed_questions, preprocessed_answers)

def get_chatbot_response(model, user_input):
    processed_input = preprocess_text(user_input)
    response = model.predict([processed_input])[0]
    return response

def scrape_mental_health_websites():
    urls = [
        "https://www.nimh.nih.gov/health/topics/anxiety-disorders/index.shtml",
        "https://www.mentalhealth.org.uk/a-to-z/d/depression",
        "https://www.apa.org/topics/anxiety",
        "https://www.psychologytoday.com/us/basics/anger",
        "https://www.helpguide.org/articles/anger/anger-management.htm",
        "https://www.nhs.uk/conditions/anger-management/",
        "https://www.verywellmind.com/common-stress-problems-2794820",
        "https://www.psychologytoday.com/us/basics/stress",
        "https://www.webmd.com/mental-health/what-is-stress"
    ]

    scraped_texts = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract paragraphs as text data
        paragraphs = soup.find_all('p')
        scraped_text = ' '.join([para.get_text() for para in paragraphs])
        scraped_texts.append(scraped_text)

    combined_text = ' '.join(scraped_texts)

    # Save the combined text to a file
    with open('scraped_data.txt', 'w', encoding='utf-8') as file:
        file.write(combined_text)

    return combined_text

def load_scraped_text():
    if os.path.exists('scraped_data.txt'):
        with open('scraped_data.txt', 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return scrape_mental_health_websites()

# Generate varied answers from combined scraped text
def generate_detailed_answer(user_query, combined_text):
    sentences = nlp(combined_text).sents
    relevant_sentences = [str(sentence) for sentence in sentences if any(keyword in str(sentence).lower() for keyword in extract_keywords(user_query))]

    if not relevant_sentences:
        return "I'm not sure about that. Can you please ask something else or provide more details?"

    random.shuffle(relevant_sentences)
    detailed_answer = ' '.join(relevant_sentences[:10])
    return detailed_answer

# Extract keywords from the user query
def extract_keywords(query):
    keywords = ['anger', 'angry', 'rage', 'fury', 'irritation', 'frustration', 'depression', 'sadness', 'anxiety', 'stress', 'problem', 'issue']
    tokens = nlp(query.lower())
    extracted_keywords = [token.text for token in tokens if token.text in keywords]
    return extracted_keywords

# Add new Q&A data from text
def add_new_qa_data(user_query, detailed_answer):
    qa_data.append((user_query, detailed_answer))
    preprocessed_questions.append(preprocess_text(user_query))
    preprocessed_answers.append(detailed_answer)

    global model
    model = build_chatbot_model(preprocessed_questions, preprocessed_answers)
    print("Chatbot updated with new data.")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
    elif request.method == 'GET':
        user_input = request.args.get('message')  # Get message from URL query parameter

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    combined_text = load_scraped_text()
    detailed_answer = generate_detailed_answer(user_input, combined_text)
    add_new_qa_data(user_input, detailed_answer)

    return jsonify({'response': detailed_answer})

if __name__ == "__main__":
    # Scrape the mental health websites and save to file
    scrape_mental_health_websites()
    app.run(host="0.0.0.0", port=5001)
