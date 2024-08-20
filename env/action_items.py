import re
from collections import Counter

def extract_action_items(text):
    keywords = re.findall(r'\b\w+\b', text)
    common_keywords = Counter(keywords).most_common(10)  # Adjust as needed
    return [keyword for keyword, _ in common_keywords]
