import platform
import os
import subprocess
import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# ---------------- APP INIT ----------------

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(BASE_DIR, "training")

# ---------------- STATIC FILES ----------------
app.mount(
    "/static",
    StaticFiles(directory=TRAINING_DIR),
    name="static"
)

# ---------------- SYSTEM CHECK ----------------

def system_check():
    if platform.system() == "Windows":
        raise HTTPException(
            status_code=400,
            detail="Tool not supported on Windows"
        )

# ---------------- ROOT ----------------

@app.get("/")
async def read_root():
    system_check()
    return FileResponse(
        os.path.join(BASE_DIR, "security_features.html"),
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# ---------------- RECONNAISSANCE (NMAP) ----------------

@app.get("/nmap")
async def read_nmap():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "nmap.html")
    )

class NmapRequest(BaseModel):
    args: str

@app.post("/run/nmap")
async def run_nmap(payload: NmapRequest):
    system_check()
    cmd = ["nmap"] + payload.args.split()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- ENUMERATION (NETCAT) ----------------

@app.get("/netcat")
async def read_netcat():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "netcat.html")
    )

# ---------------- EXPLOITATION AWARENESS ----------------

# SQLMap (guarded execution)
@app.get("/sqlmap")
async def read_sqlmap():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "sqlmap.html")
    )

class SQLMapRequest(BaseModel):
    url: str
    action: str = ""

def validate_sqlmap_input(url: str, action: str):
    if not re.match(r"^https?://.+\?.+=.+", url):
        raise HTTPException(
            status_code=400,
            detail="URL must include a parameter"
        )

    if action not in {"", "--dbs", "--tables"}:
        raise HTTPException(
            status_code=400,
            detail="Action not allowed"
        )

    dangerous = [
        "--os-shell", "--os-pwn", "--file-read", "--file-write",
        "--dump-all", "--passwords", "--privileges", "--is-dba"
    ]

    for d in dangerous:
        if d in url:
            raise HTTPException(
                status_code=400,
                detail="Dangerous option blocked"
            )

@app.post("/run/sqlmap")
async def run_sqlmap(payload: SQLMapRequest):
    system_check()
    validate_sqlmap_input(payload.url, payload.action)

    cmd = [
        "sqlmap",
        "-u", payload.url,
        "--batch",
        "--level=1",
        "--risk=1",
        "--timeout=10",
        "--threads=1",
        "--smart"
    ]

    if payload.action:
        cmd.append(payload.action)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "SQLMap timed out (safety stop)",
            "code": 124
        }

# ---------------- METASPLOIT (THEORY ONLY) ----------------

# New canonical route
@app.get("/exploitation/metasploit")
async def read_metasploit_exploitation():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "metasploit.html")
    )

# Backward compatibility redirect
@app.get("/metasploit")
async def redirect_metasploit():
    return RedirectResponse(
        url="/exploitation/metasploit",
        status_code=301
    )

# ---------------- CREDENTIAL ATTACKS ----------------

@app.get("/password_cracking")
async def read_password_cracking():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "password_cracking.html")
    )

@app.get("/hydra")
async def read_hydra():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "hydra.html")
    )

@app.get("/john")
async def read_john():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "john_the_ripper.html")
    )

# ---------------- QUIZ ----------------

@app.get("/quiz")
async def read_quiz():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "quiz.html")
    )

# ---------------- MAIN ----------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
