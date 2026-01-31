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

class NetcatListenRequest(BaseModel):
    port: int
    flags: str = ""

class NetcatConnectRequest(BaseModel):
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

sessions: Dict[str, Dict[str, WebSocket]] = {}

@app.websocket("/ws/netcat")
async def ws_netcat(websocket: WebSocket):
    await websocket.accept()

    role = websocket.query_params.get("role")
    host = websocket.query_params.get("host")
    port = websocket.query_params.get("port")

    if not port or role not in ("listener", "client"):
        await websocket.send_text("[error] invalid parameters")
        await websocket.close()
        return

    # session key = port
    session = sessions.setdefault(port, {})

    session[role] = websocket

    await websocket.send_text(f"[connected] role={role} port={port}")

    try:
        while True:
            msg = await websocket.receive_text()

            # pair routing
            if role == "listener" and "client" in session:
                await session["client"].send_text(msg)

            elif role == "client" and "listener" in session:
                await session["listener"].send_text(msg)

            else:
                await websocket.send_text("[waiting] peer not connected")

    except WebSocketDisconnect:
        session.pop(role, None)
        if not session:
            sessions.pop(port, None)

# ----------------- MAIN -----------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
