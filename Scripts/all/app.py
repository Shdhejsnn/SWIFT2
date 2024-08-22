from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from preprocessing import preprocess_text
from summarization import generate_summary
from topic_modeling import extract_topics
from action_items import extract_action_items
from textblob import TextBlob
import json

app = Flask(__name__)
app.secret_key = 'teamflexbox'

# Dummy in-memory storage for events
events = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_minutes', methods=['POST'])
def generate_minutes():
    transcript = request.form['transcript']
    event_date = request.form['eventDate']  # Get event date from form
    print("Transcript Received:", transcript)

    # Perform sentiment analysis
    blob = TextBlob(transcript)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_label = 'Positive' if sentiment_polarity > 0 else 'Negative' if sentiment_polarity < 0 else 'Neutral'

    # Generate results
    tokens = preprocess_text(transcript)
    action_items = extract_action_items(transcript)
    
    # Format topics for readability
    topics = extract_topics([transcript])
    formatted_topics = []
    for topic in topics:
        topic_words = sorted(topic['top_words'], key=lambda x: x['weight'], reverse=True)
        formatted_topic = {
            'topic_id': topic['topic_id'],
            'words': ', '.join([f"{word['word']} ({word['weight']:.2f})" for word in topic_words])
        }
        formatted_topics.append(formatted_topic)

    keywords = action_items['all_keywords']  # Updated to use 'all_keywords'
    summary = generate_summary(transcript, keywords)  # Pass keywords to generate_summary

    # Store results in session
    session['tokens'] = tokens
    session['summary'] = summary
    session['topics'] = formatted_topics
    session['keywords'] = keywords
    session['sentiment'] = sentiment_label
    session['action_items'] = action_items

    # Save event
    events.append({
        'title': 'Meeting Summary',
        'start': event_date,
        'summary': summary
    })

    return jsonify({
        'tokens': tokens,
        'summary': summary,
        'topics': formatted_topics,
        'keywords': keywords,
        'sentiment': sentiment_label,
        'action_items': action_items
    })

@app.route('/tokenized')
def tokenized():
    tokens = session.get('tokens', [])
    return render_template('tokenized.html', tokens=tokens)

@app.route('/summary')
def summary():
    summary = session.get('summary', 'No summary available.')
    return render_template('summary.html', summary=summary)

@app.route('/topics')
def topics():
    topics = session.get('topics', [])
    return render_template('topics.html', topics=topics)

@app.route('/keywords')
def keywords():
    keywords = session.get('keywords', [])
    return render_template('keywords.html', keywords=keywords)

@app.route('/action_items')
def action_items():
    action_items = session.get('action_items', {'tasks': [], 'decisions': [], 'follow_ups': []})
    return render_template('action_items.html', action_items=action_items)

@app.route('/get_events')
def get_events():
    return jsonify(events)

@app.route('/view_summary/<date>')
def view_summary(date):
    # Find the summary for the given date
    summary = next((event['summary'] for event in events if event['start'] == date), 'No summary available for this date.')
    return render_template('summary.html', summary=summary)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
