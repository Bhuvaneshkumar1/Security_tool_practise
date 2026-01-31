import platform
import os
import subprocess
import asyncio
from typing import Dict

from fastapi import (
    FastAPI,
    HTTPException,
    Body,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(BASE_DIR, "training")

# ----------------- SYSTEM CHECK -----------------

def system_check():
    if platform.system() == "Windows":
        raise HTTPException(status_code=400, detail="Tool not supported on Windows")

# ----------------- STATIC PAGES -----------------

@app.get("/")
async def read_root():
    system_check()
    return FileResponse(os.path.join(BASE_DIR, "security_features.html"))

@app.get("/nmap")
async def read_nmap():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "nmap.html"))

@app.get("/netcat")
async def read_netcat():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "netcat.html"))

# ----------------- NMAP -----------------

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

# ----------------- NETCAT (HTTP, ONE-SHOT) -----------------

class NetcatListenRequest(BaseModel): # type: ignore
    port: int
    flags: str = ""

class NetcatConnectRequest(BaseModel): # type: ignore
    host: str
    port: int
    flags: str = ""
    message: str = ""

@app.post("/run/netcat/listen")
async def netcat_listen(payload: NetcatListenRequest):
    system_check()
    cmd = ["nc", "-l", str(payload.port)]
    if payload.flags:
        cmd[1:1] = payload.flags.split()

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
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Listener timeout reached",
            "code": 124
        }

@app.post("/run/netcat/connect")
async def netcat_connect(payload: NetcatConnectRequest):
    system_check()
    cmd = ["nc", payload.host, str(payload.port)]
    if payload.flags:
        cmd[1:1] = payload.flags.split()

    try:
        result = subprocess.run(
            cmd,
            input=payload.message,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Connection timeout reached",
            "code": 124
        }

# ----------------- NETCAT (WEBSOCKET STREAMING) -----------------

@app.get("/netcat/listener")
async def netcat_listener():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "netcat.html"))

@app.get("/netcat/client")
async def netcat_client():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "netcat.html"))

# ---------- NETCAT BACKEND ----------

class NetcatListenRequest(BaseModel):
    port: int

class NetcatConnectRequest(BaseModel):
    host: str
    port: int
    message: str = ""

@app.post("/run/netcat/listen")
async def run_netcat_listen(payload: NetcatListenRequest):
    system_check()
    cmd = ["nc", "-l", str(payload.port)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode
    }

@app.post("/run/netcat/connect")
async def run_netcat_connect(payload: NetcatConnectRequest):
    system_check()
    cmd = ["nc", payload.host, str(payload.port)]
    result = subprocess.run(
        cmd,
        input=payload.message,
        capture_output=True,
        text=True,
        timeout=30
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode
    }
# ----------------- MAIN -----------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
