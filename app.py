import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from scraper import get_job_description
from skills_extractor import extract_skills
from collections import Counter

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

# Define upload and result directories; create them if needed.
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", "error")
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash("No selected file", "error")
            return redirect(url_for('index'))
        if file and file.filename.endswith(".csv"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # Process CSV: scrape descriptions and extract skills
            extracted_path, overall_path = process_csv(file_path)
            return render_template('results.html', extracted_path=extracted_path, overall_path=overall_path)
    return render_template('index.html')

def process_csv(file_path):
    """Reads CSV, scrapes job descriptions, extracts skills, and saves the reports."""
    df = pd.read_csv(file_path)
    if 'URL' not in df.columns:
        raise Exception("CSV must contain a column named 'URL' with job description links.")

    results = []
    overall_skill_counts = Counter()

    for index, row in df.iterrows():
        url = row['URL']
        try:
            job_text = get_job_description(url)
            skills = extract_skills(job_text)
            # Create a string summary: e.g. "python (3), docker (2)"
            skills_str = ", ".join([f"{skill} ({count})" for skill, count in skills])
            # Aggregate overall skill frequency
            for skill, count in skills:
                overall_skill_counts[skill] += count
            results.append({"URL": url, "Job Description": job_text, "Extracted Skills": skills_str})
        except Exception as e:
            results.append({"URL": url, "Job Description": "Error fetching data", "Extracted Skills": str(e)})

    # Save per-job extracted skills
    results_df = pd.DataFrame(results)
    extracted_skills_path = os.path.join(RESULTS_FOLDER, "extracted_skills.csv")
    results_df.to_csv(extracted_skills_path, index=False)

    # Save overall skill frequency
    overall_skills_df = pd.DataFrame(overall_skill_counts.items(), columns=["Skill", "Frequency"])
    overall_skills_df = overall_skills_df.sort_values(by="Frequency", ascending=False)
    overall_path = os.path.join(RESULTS_FOLDER, "overall_skill_frequency.csv")
    overall_skills_df.to_csv(overall_path, index=False)

    return extracted_skills_path, overall_path

if __name__ == '__main__':
    app.run(debug=True)
