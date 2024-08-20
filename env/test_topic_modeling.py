from topic_modeling import extract_topics

# Example texts for topic modeling
texts = [
    "Welcome to today's meeting. First on the agenda is the project update.",
    "John reports that the development team has completed the initial phases of the project ahead of schedule.",
    "Next, Sarah will go over the budget and review the projected costs for the next quarter."
]

# Call the function to extract topics
topics = extract_topics(texts)

# Print the extracted topics
print(topics)

