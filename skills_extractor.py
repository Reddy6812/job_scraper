import re
from collections import Counter
import spacy

# Predefined list of common technical skills (expand as needed)
COMMON_SKILLS = [
    'graphql', 'next.js', 'typescript', 'react', 'angular', 'vue.js', 'node.js', 'express',
    'django', 'flask', 'python', 'java', 'c++', 'c#', 'javascript', 'sql', 'aws', 'azure', 'gcp',
    'docker', 'kubernetes', 'html', 'css', 'sass', 'less', 'webpack', 'babel', 'mongodb', 'postgresql',
    'redis', 'firebase'
]

# Load spaCy English model (ensure you have run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def is_valid_skill(chunk_text):
    """
    Determines whether a noun chunk is a valid technical skill.
    Filters out common non-skill phrases and those that are too generic.
    """
    chunk_text = chunk_text.strip()
    if not chunk_text:
        return False
    # Reject if more than 3 words (likely not a concise tech term)
    if len(chunk_text.split()) > 3:
        return False
    # Blacklist unwanted phrases (all lower-case for comparison)
    blacklist = {
        "mountain view", "computer science", "ml accelerator", "computer engineering",
        "google glassdoor", "2 days ago", "bachelor's degree", "minimum qualifications",
        "job description", "work experience", "years of experience"
    }
    if chunk_text.lower() in blacklist:
        return False
    # Known technical skills list (from predefined skills)
    known_tech_skills = set(COMMON_SKILLS)
    if chunk_text.lower() in known_tech_skills:
        return True
    # Accept if the chunk contains at least one uppercase letter (indicating a proper noun)
    if any(char.isupper() for char in chunk_text):
        return True
    # Also accept if it contains common technical symbols such as '.' or '+' or '#'
    if '.' in chunk_text or '+' in chunk_text or '#' in chunk_text:
        return True
    return False

def extract_skills(text):
    """
    Extracts and counts technical skills from the provided text.
    Combines extraction from a predefined list with dynamic extraction via spaCy NLP.
    Only includes items that pass the technical skill filter.
    """
    text_lower = text.lower()
    total_counts = Counter()

    # Predefined extraction: count occurrences of each known technical skill.
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            total_counts[skill] += len(matches)

    # Dynamic extraction using spaCy to detect potential tech skills via noun chunks.
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if not is_valid_skill(chunk_text):
            continue
        # If already counted from the predefined list (case-insensitive), skip it.
        if chunk_text.lower() in total_counts:
            continue
        # Count occurrences in the text (case-insensitive)
        count = len(re.findall(re.escape(chunk_text), text, flags=re.IGNORECASE))
        if count > 0:
            total_counts[chunk_text] = count

    # Return skills sorted by frequency in descending order.
    return sorted(total_counts.items(), key=lambda x: x[1], reverse=True)
