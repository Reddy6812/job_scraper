
# **Job Scraping and Skill Extraction**

## **Overview**
This project automates the process of extracting **technical skills** from job listings. It takes a **CSV file with job URLs**, scrapes job descriptions, extracts relevant skills using **NLP (spaCy) and regex**, and generates **two structured reports**:
1. **Job-specific Skills Report (`extracted_skills.csv`)** – Extracted skills for each job description.
2. **Overall Skill Frequency Report (`overall_skill_frequency.csv`)** – Aggregated frequency of skills across job postings.

Unlike naive keyword extraction, this project **filters out non-technical terms** (e.g., "bachelor's degree", "minimum qualifications") and **dynamically detects programming languages, frameworks, and tools** (e.g., `GraphQL`, `Next.js`, `TypeScript`, etc.).

---

## **Project Folder Structure**
```
job_scraper/
├── app.py                # Main Flask application
├── scraper.py            # Improved web scraping logic
├── skills_extractor.py   # AI-driven skill extraction using NLP and regex
├── templates/
│   ├── index.html        # File upload page
│   └── results.html      # Results page with download links
├── static/
│   └── styles.css        # UI styling (optional)
├── uploads/              # (Auto-created) Stores uploaded CSV files
├── results/              # (Auto-created) Stores generated CSV reports
├── requirements.txt      # Dependencies list
└── README.md             # Project documentation
```

---

## **Features**
- **Scrapes job descriptions** from URLs automatically  
- **Extracts skills** dynamically using NLP-based entity recognition (spaCy)  
- **Filters out irrelevant terms** (e.g., location names, company names, qualifications)  
- **Generates structured CSV reports** with **job-specific skills** and **overall skill frequency**  
- **User-friendly web interface** for file upload and downloading results  
- **Supports a predefined skill list** with **dynamic skill detection**  

---

## **Installation & Setup**
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/job-scraper.git
cd job-scraper
```

### **2. Install Dependencies**
Ensure you have Python 3.7+ installed, then run:
```bash
pip install -r requirements.txt
```

### **3. Download the NLP Model (spaCy)**
This project uses **spaCy** for natural language processing. Download the English model:
```bash
python -m spacy download en_core_web_sm
```

### **4. Run the Flask App**
```bash
python app.py
```
The app will start at: **http://127.0.0.1:5000**

---

## **How to Use**
### **Step 1: Prepare a CSV file**
Your **CSV file** should contain a column named **"URL"**, which lists job posting links.
Example:
```csv
URL
https://www.example.com/job1
https://www.example.com/job2
https://www.example.com/job3
```

### **Step 2: Upload CSV File**
- Open your browser and go to **http://127.0.0.1:5000**  
- Click **"Choose File"** and upload your CSV  
- Click **"Extract Skills"** to start processing  

### **Step 3: Download Results**
Once processing is complete, you can **download two CSV files**:
- **`extracted_skills.csv`** – Contains job descriptions and extracted skills per job listing.
- **`overall_skill_frequency.csv`** – Aggregated count of skills across all job postings.

---

## **Example Output**
### **Extracted Skills Report (`extracted_skills.csv`)**
| URL                      | Extracted Skills                                   |
|--------------------------|--------------------------------------------------|
| job1.com                | GraphQL (5), Next.js (3), TypeScript (2)         |
| job2.com                | Python (7), FastAPI (3), Docker (4)              |
| job3.com                | Java (6), Spring Boot (5), Kubernetes (3)        |

### **Overall Skill Frequency Report (`overall_skill_frequency.csv`)**
| Skill        | Frequency |
|-------------|-----------|
| Python      | 20        |
| Next.js     | 12        |
| GraphQL     | 10        |
| TypeScript  | 8         |
| Docker      | 6         |

---

## **Technologies Used**
- **Python** – Core programming language  
- **Flask** – Web framework for UI  
- **Requests & BeautifulSoup** – Web scraping libraries  
- **spaCy** – NLP engine for extracting skills  
- **pandas** – Data processing and CSV generation  

---

## **How It Works**
### **1. Web Scraping (`scraper.py`)**
- Fetches **job descriptions** from the provided URLs.
- Uses **multiple CSS selectors** to extract job postings.
- Falls back to extracting text from `<p>` and `<div>` tags if no structured job description is found.

### **2. Skill Extraction (`skills_extractor.py`)**
- Uses **a predefined list of skills** (e.g., `GraphQL`, `Next.js`, `TypeScript`).
- Dynamically detects **new skills** using **NLP noun chunking**.
- Applies a **filter to remove non-technical terms** (e.g., "bachelor's degree", "minimum qualifications").
- Returns **only valid technical skills**.

### **3. Flask UI (`app.py`)**
- Provides a **web interface** for **CSV uploads**.
- Calls **scraper and extractor** in the background.
- Generates **two downloadable reports**.

---

## **Advanced Features & Future Enhancements**
- **Better Filtering:** Custom NLP logic ensures only technical skills are extracted.  
- **Dynamic Skill Extraction:** Extracts new skills beyond the predefined list.  
- **Improved Scraping:** Works across multiple job portals.  

### **Future Enhancements**
- Support for **structured job boards (LinkedIn, Indeed, Glassdoor)**  
- **Machine learning model** for skill detection instead of rule-based extraction  
- **Better UI/UX** with progress bars and history tracking  

---

## **License**
This project is **open-source** under the **MIT License**.  
Feel free to contribute and improve it.

---