import re
from collections import Counter
import spacy

# Predefined skill list (expandable)
COMMON_SKILLS = [
    'python', 'java', 'c++', 'c#', 'javascript', 'sql', 'aws', 'azure', 'gcp',
    'react', 'node', 'html', 'css', 'django', 'flask', 'machine learning',
    'data analysis', 'excel', 'linux', 'git', 'docker', 'kubernetes', 'communication',
    'teamwork', 'problem solving', 'project management'
]

# Load spaCy English model (make sure you have run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    """
    Extracts and counts occurrences of skills.
    Combines a predefined list extraction with dynamic detection via NLP.
    """
    text_lower = text.lower()

    # Extract predefined skills using regex matching
    predefined_counts = Counter()
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            predefined_counts[skill] = len(matches)

    # Dynamic detection: use spaCy to extract noun chunks
    dynamic_counts = Counter()
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        # Lowercase, trimmed text of the noun chunk.
        chunk_text = chunk.text.strip().lower()
        # Skip if already counted as a predefined skill or too short (less than two words)
        if chunk_text in predefined_counts or len(chunk_text.split()) < 2:
            continue
        # Heuristic filter: ignore common non-skill phrases (you can expand this list)
        common_exclusions = {"job description", "work experience", "project management", "years of experience"}
        if chunk_text in common_exclusions:
            continue
        # Count how many times this noun chunk appears in the text.
        count = text_lower.count(chunk_text)
        if count > 1:  # only include if mentioned more than once
            dynamic_counts[chunk_text] += count

    # Combine both counters. (Dynamic detections add additional skills not in the predefined list.)
    total_counts = predefined_counts + dynamic_counts
    # Return a sorted list of (skill, count) tuples in descending order of frequency.
    return sorted(total_counts.items(), key=lambda x: x[1], reverse=True)
