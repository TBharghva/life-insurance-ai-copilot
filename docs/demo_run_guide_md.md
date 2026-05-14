# Life Insurance AI Copilot - Demo Run Guide

## Step 1 — Open Terminal 1 (Backend)

Navigate to project folder:

```bash
cd D:\AI_lab\life-insurance-ai-copilot
```

Activate virtual environment:

```bash
.\venv\Scripts\activate
```

Start FastAPI backend server:

```bash
uvicorn backend.api.main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

Optional API Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Step 2 — Open Terminal 2 (Frontend)

Navigate to project folder:

```bash
cd D:\AI_lab\life-insurance-ai-copilot
```

Activate virtual environment:

```bash
.\venv\Scripts\activate
```

Start Streamlit frontend:

```bash
streamlit run frontend/app.py
```

Expected output:

```text
Local URL: http://localhost:8501
```

Open in browser:

```text
http://localhost:8501
```

---

# Sample Demo Questions

## Question 1

```text
I am 50 years old, diabetic, and missed premium payments for 6 months. Can I revive my policy and what underwriting concerns apply?
```

### Demonstrates

- Multi-document retrieval
- Underwriting reasoning
- Policy lapse and revival logic
- Streaming responses
- Citations

---

## Question