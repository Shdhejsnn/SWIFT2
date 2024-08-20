from flask import Flask, request, jsonify, render_template, session
from preprocessing import preprocess_text
from summarization import generate_summary
from topic_modeling import extract_topics
from action_items import extract_action_items

app = Flask(__name__)
app.secret_key = 'teamflexbox'  # Required for using session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_minutes', methods=['POST'])
def generate_minutes():
    transcript = request.form['transcript']
    print("Transcript Received:", transcript)  # Debugging line

    # Generate results
    tokens = preprocess_text(transcript)
    summary = generate_summary(transcript)
    topics = extract_topics([transcript])
    keywords = extract_action_items(transcript)
    
    # Check if topics or keywords are empty
    formatted_topics = [{'topic_id': i, 'words': topic['words']} for i, topic in enumerate(topics)] if topics else []
    formatted_keywords = keywords if keywords else []

    # Store results in session or some temporary storage
    session['tokens'] = tokens
    session['summary'] = summary
    session['topics'] = formatted_topics
    session['keywords'] = formatted_keywords

    return jsonify({
        'tokens': tokens,
        'summary': summary,
        'topics': formatted_topics,
        'keywords': formatted_keywords
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
