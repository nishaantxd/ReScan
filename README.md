# ReScan

A web-based AI-powered tool to analyze resumes, compare them with job descriptions (JD), and give insights on how well the resume fits according to a JD. Built using Streamlit with a modern UI and support for light/dark mode toggle.

Live App: [https://rescan1.streamlit.app](https://rescan1.streamlit.app)

---

## Features

- Upload resume in PDF or image format
- Paste any job description (JD) for comparison
- Extracts key sections like Skills, Experience, and Education using NLP
- Compares resume content with JD using BERT & TF-IDF
- Displays keyword match breakdown with pie chart visualization
- Gives suggestions for improvement and missing keywords
- Recommends relevant career roles
- Smooth light/dark mode toggle and modern UI styling

---

### Requirements

- Python >= 3.8
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (only required if uploading resume as an image)

### Steps

```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
## Future Work
- Suggest career recommendations based on content.
- Chatbot Integration for direct Q&A.
