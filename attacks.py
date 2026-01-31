import platform
import os
import subprocess
import re
import time
from typing import Dict, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(BASE_DIR, "training")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ---------------- SYSTEM CHECK ----------------

def system_check():
    if platform.system() == "Windows":
        raise HTTPException(status_code=400, detail="Tool not supported on Windows")

# ---------------- AUTH + RATE LIMIT ----------------

API_KEY = "sqlmap-training-key"
RATE_LIMIT = 5
RATE_WINDOW = 60
_rate_store: Dict[str, list] = {}

def auth_and_rate_limit(request: Optional[Request]):
    if request is None:
        raise HTTPException(status_code=400, detail="Request object is missing")
    
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if request.client is None:
        raise HTTPException(status_code=400, detail="Client information is missing")
    
    ip = request.client.host
    now = time.time()
    history = _rate_store.get(ip, [])
    history = [t for t in history if now - t < RATE_WINDOW]

    if len(history) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    history.append(now)
    _rate_store[ip] = history

# ---------------- ROOT ----------------

@app.get("/")
async def read_root():
    system_check()
    return FileResponse(os.path.join(BASE_DIR, "security_features.html"))

# ---------------- SQLMAP ----------------

@app.get("/sqlmap")
async def read_sqlmap():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "sqlmap.html"))

class SQLMapRequest(BaseModel):
    url: str = ""
    param: str = ""
    action: str = ""
    detect_waf: bool = False

def validate_sqlmap(payload: SQLMapRequest):
    if not re.match(r"^https?://.+\?.+=.+", payload.url):
        raise HTTPException(status_code=400, detail="URL must contain parameters")

    if payload.param and payload.param not in payload.url:
        raise HTTPException(status_code=400, detail="Selected parameter not in URL")

    if payload.action not in {"", "--dbs", "--tables"}:
        raise HTTPException(status_code=400, detail="Action not allowed")

@app.post("/run/sqlmap")
async def run_sqlmap(payload: SQLMapRequest = Body(...), request: Optional[Request] = None):
    system_check()
    auth_and_rate_limit(request)

    if not payload.url:
        payload.url = "http://testphp.vulnweb.com/listproducts.php?cat=1&id=2"

    validate_sqlmap(payload)

    cmd = [
        "sqlmap",
        "-u", payload.url,
        "--batch",
        "--level=1",
        "--risk=1",
        "--threads=1",
        "--timeout=10",
        "--smart"
    ]

    if payload.param:
        cmd += ["-p", payload.param]

    if payload.detect_waf:
        cmd.append("--identify-waf")

    if payload.action:
        cmd.append(payload.action)

    report_id = str(uuid4())
    report_path = os.path.join(REPORT_DIR, f"sqlmap_{report_id}.txt")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        with open(report_path, "w") as f:
            f.write("SQLMap Scan Report\n")
            f.write("=" * 50 + "\n\n")
            f.write("Command Executed:\n")
            f.write(" ".join(cmd) + "\n\n")
            f.write("STDOUT:\n")
            f.write(result.stdout + "\n\n")
            f.write("STDERR:\n")
            f.write(result.stderr + "\n")

        return {
            "command": " ".join(cmd),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report_id": report_id
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="SQLMap timed out")

@app.get("/download/sqlmap/{report_id}")
async def download_sqlmap_report(report_id: str):
    report_path = os.path.join(REPORT_DIR, f"sqlmap_{report_id}.txt")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        report_path,
        media_type="text/plain",
        filename=f"sqlmap_report_{report_id}.txt"
    )

# ---------------- MAIN ----------------

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
