# 🛡️ Security Practice Lab

A **phase-based offensive security learning platform** focused on  
**understanding attack techniques safely, ethically, and correctly**.

This project is designed to demonstrate **real-world security concepts** using:
- Guided theory
- Safe simulations
- Guarded live tooling
- Progress tracking
- Final assessment (quiz)

Built for **learning, interviews, and portfolio demonstration**.

---

## 🎯 Learning Philosophy

> “Understand before executing.”

This lab **does not encourage blind exploitation**.  
Each phase teaches:
- Why attacks work
- How attackers think
- How defenders detect and stop them
- When tools should and should not be used

---

## 🧠 Training Phases

### Phase 1 — Reconnaissance
**Goal:** Identify hosts, ports, services, and attack surface  
**Tools:**  
- Nmap (guarded execution)

---

### Phase 2 — Enumeration
**Goal:** Understand service behavior and application responses  
**Tools:**  
- Netcat (theory + safe usage patterns)

---

### Phase 3 — Exploitation Awareness
**Goal:** Learn how vulnerabilities are abused (without unsafe execution)  
**Tools:**  
- SQLMap (strictly limited, guarded mode)
- Metasploit (theory-only walkthrough)

---

### Phase 4 — Credential Attacks
**Goal:** Understand password abuse and real-world breaches  
**Tools:**  
- Hydra (online attack theory + simulation)
- John the Ripper (offline hash cracking simulation)

---

### Final — Knowledge Validation
- Progress-based unlock
- 30-question MCQ quiz
- Score-based feedback
- Completion readiness check

---

## 🔐 Safety & Ethics

This platform enforces:
- ❌ No destructive exploitation
- ❌ No OS-level shells
- ❌ No file read/write abuse
- ❌ No privilege escalation
- ❌ No unauthorized targets

All executions are:
- Guarded
- Rate-limited
- Input-validated
- Designed for **local or lab environments only**

> ⚠️ Use only on systems you own or have permission to test.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML / CSS / JavaScript
- **Execution:** Subprocess (guarded)
- **Storage:** Browser LocalStorage (progress tracking)

---

## 📂 Project Structure
```bash
Security_Practice_Lab/
│
├── attacks.py # FastAPI backend
├── security_features.html # Main dashboard
├── training/
│ ├── nmap.html
│ ├── netcat.html
│ ├── sqlmap.html
│ ├── metasploit.html
│ ├── password_cracking.html
│ ├── hydra.html
│ ├── john_the_ripper.html
│ ├── quiz.html
│ └── lesson_tracker.js
│
├── README.md
└── .gitignore

```
---

## ▶️ How to Run

### 1. Create a virtual environment (recommended)

```bash
python3 -m venv venv
```
### 2. Activate virtual environment
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
Tools like nmap and sqlmap must already be installed on the system.

### 4. Start the server
```bash
uvicorn attacks:app --reload
```
### Open in browser:
```bash
http://127.0.0.1:8000
```
🧪 Supported Platforms
OS	Status
- **Linux**	  - ✅ Fully supported
- **macOS**	  - ✅ Supported
- **Windows**	- ❌ Not supported (tooling limitations)

🎓 Who This Is For
Security students

1. thical hacking learners

2. Interview preparation

3. Portfolio demonstration

4. Educators and mentors

📜 Disclaimer
This project is for educational purposes only.
The author is not responsible for misuse.

Always follow:

- Local laws

- Organizational policies

- Ethical guidelines

⭐ Final Note
If you understand everything in this lab,
you are not a script-kiddie — you are thinking like a security engineer.
---
## Author 
Bhuvanesh kumar | cyber security enthusiast| ethical hacker
