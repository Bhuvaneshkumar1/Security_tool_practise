import platform
import os
import subprocess
import re
import asyncio

from fastapi import FastAPI, HTTPException, Body, WebSocket
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(BASE_DIR, "training")

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

# ---------------- NMAP ----------------

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

# ---------------- HYDRA (THEORY + SIMULATION) ----------------

@app.get("/hydra")
async def read_hydra():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "hydra.html")
    )

@app.websocket("/ws/hydra/simulate/{mode}")
async def hydra_simulator(ws: WebSocket, mode: str):
    await ws.accept()

    simulations = {
        "normal": [
            "[INFO] Hydra v9.5 (simulation mode)",
            "[INFO] Target: ssh://192.168.1.10",
            "[INFO] Parallel tasks: 4",
            "",
            "[ATTEMPT] admin:admin → failed",
            "[ATTEMPT] admin:password → failed",
            "[ATTEMPT] test:test123 → failed",
            "[ATTEMPT] root:toor → SUCCESS",
            "",
            "[RESULT] Valid credentials found",
            "[RESULT] login: root   password: toor",
            "",
            "[INFO] Simulation complete",
            "[INFO] No real authentication was performed"
        ],

        "ratelimit": [
            "[INFO] Hydra v9.5 (simulation mode)",
            "[INFO] Target: ssh://192.168.1.10",
            "",
            "[ATTEMPT] admin:admin → failed",
            "[ATTEMPT] admin:password → failed",
            "[ATTEMPT] admin:123456 → failed",
            "",
            "[WARNING] Too many login attempts detected",
            "[WARNING] Server responded with rate-limit",
            "",
            "[ERROR] Authentication temporarily blocked",
            "[INFO] Further attempts stopped",
            "",
            "[INFO] Simulation complete",
            "[INFO] Defense success: Rate limiting"
        ],

        "mfa": [
            "[INFO] Hydra v9.5 (simulation mode)",
            "[INFO] Target: ssh://192.168.1.10",
            "",
            "[ATTEMPT] admin:password123 → SUCCESS",
            "",
            "[INFO] Password accepted",
            "[INFO] MFA challenge triggered",
            "[ERROR] Second factor required",
            "",
            "[RESULT] Access denied",
            "[INFO] Password-only attack failed",
            "",
            "[INFO] Simulation complete",
            "[INFO] Defense success: MFA"
        ]
    }

    output = simulations.get(mode)
    if not output:
        await ws.send_text("[ERROR] Invalid simulation mode")
        await ws.close()
        return

    try:
        for line in output:
            await ws.send_text(line)
            await asyncio.sleep(0.6)
    except Exception:
        pass
    finally:
        await ws.close()

# ---------------- NETCAT (THEORY ONLY) ----------------

@app.get("/netcat")
async def read_netcat():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "netcat.html")
    )

# ---------------- METASPLOIT (THEORY ONLY) ----------------

@app.get("/metasploit")
async def read_metasploit():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "metasploit.html")
    )

# ---------------- SQLMAP ----------------

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
        raise HTTPException(status_code=400, detail="URL must include a parameter")

    allowed_actions = {"", "--dbs", "--tables"}
    if action not in allowed_actions:
        raise HTTPException(status_code=400, detail="Action not allowed")

    dangerous = [
        "--os-shell", "--os-pwn", "--file-read", "--file-write",
        "--dump-all", "--passwords", "--privileges", "--is-dba"
    ]
    for d in dangerous:
        if d in url:
            raise HTTPException(status_code=400, detail="Dangerous option blocked")

@app.post("/run/sqlmap")
async def run_sqlmap(payload: SQLMapRequest = Body(...)):
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

# ---------------- PASSWORD CRACKING ----------------

@app.get("/password_cracking")
async def read_password_cracking():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "password_cracking.html")
    )

@app.get("/john")
async def read_john():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "john_the_ripper.html")
    )

# ---------------- MAIN ----------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
