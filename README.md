# 🛡️ Security Tools Practice Lab

A professional, recruiter-grade learning platform to understand
offensive security tools through **theory, simulation, and validation**.

---

## 🎯 Objective

This project demonstrates:
- Ethical understanding of security tools
- Realistic attack workflows (safe mode)
- Enforced learning completion
- Quiz-based validation
- Certificate generation

---

## 🧰 Tools Covered

- Nmap
- SQLMap
- Netcat (theory)
- Metasploit (theory)
- Password Cracking
- Hydra (simulation)
- John the Ripper (simulation)

---

## 🧠 Learning Flow

1. User must scroll through **all tool pages**
2. Each page is auto-marked completed
3. Progress bar updates on home page
4. Final quiz unlocks only at **100% completion**
5. Quiz contains 30 MCQs
6. Certificate is generated on pass

---

## 🚀 Tech Stack

- Frontend: HTML, CSS, Vanilla JavaScript
- Backend: FastAPI (Python)
- Execution: Safe subprocess execution
- State tracking: Browser localStorage

---

## 🧪 Setup Instructions (IMPORTANT)

### 1️⃣ Create a Virtual Environment (Recommended)

Using a virtual environment avoids dependency conflicts.

```bash
python3 -m venv venv
source venv/bin/activate
On Windows:

venv\Scripts\activate
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
uvicorn attacks:app --reload
Open in browser:

http://127.0.0.1:8000
🔐 Security Principles
No destructive commands

SQLMap runs in restricted mode

No live exploitation

Designed strictly for education

📜 Disclaimer
This project is for educational purposes only.
All tools must be used with proper authorization.

👤 Author
Built to demonstrate real understanding, not shortcuts.


---

# 🚫 `.gitignore`  (FINAL)

```gitignore
# Python
__pycache__/
*.pyc

# Virtual Environment
venv/
.env/

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/