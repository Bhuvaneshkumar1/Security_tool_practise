import platform
import os
import subprocess
from fastapi import FastAPI, HTTPException
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
        os.path.join(BASE_DIR, "security_features.html")
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
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------- NETCAT (THEORY ONLY) ----------------

@app.get("/netcat")
async def read_netcat():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "netcat.html")
    )


# ---------------- OTHER TOOLS ----------------

@app.get("/metasploit")
async def read_metasploit():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "metasploit.html")
    )


@app.get("/sqlmap")
async def read_sqlmap():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "sqlmap.html")
    )


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


@app.get("/hydra")
async def read_hydra():
    system_check()
    return FileResponse(
        os.path.join(TRAINING_DIR, "hydra.html")
    )


# ---------------- MAIN ----------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
