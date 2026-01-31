import platform
import os
from fastapi import FastAPI, HTTPException, Body
import subprocess
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DIR = os.path.join(BASE_DIR, "training")

def system_check():
    if platform.system() == "Windows":
        raise HTTPException(status_code=400, detail="Tool not supported on Windows")

@app.get("/")
async def read_root():
    system_check()
    return FileResponse(os.path.join(BASE_DIR, "security_features.html"))




@app.get("/nmap")
async def read_nmap():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "nmap.html"))

@app.post("/run/nmap")
async def run_nmap(args: str = Body(...)):
    system_check()
    cmd = ["nmap"] + args.split()
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


@app.get("/metasploit")
async def read_metasploit():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "metasploit.html"))




@app.get("/netcat")
async def read_netcat():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "netcat.html"))




@app.get("/sqlmap")
async def read_sqlmap():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "sqlmap.html"))




@app.get("/password_cracking")
async def read_password_cracking():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "password_cracking.html"))




@app.get("/john")
async def read_john():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "john_the_ripper.html"))




@app.get("/hydra")
async def read_hydra():
    system_check()
    return FileResponse(os.path.join(TRAINING_DIR, "hydra.html"))




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
