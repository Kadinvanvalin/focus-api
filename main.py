# Docker-based API server (FastAPI)
# Hardcoded /focus response to start with

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import re

app = FastAPI()
import subprocess
import os
import re

REPO_PATH = "/app/notes"
MARKDOWN_PATH = f"{REPO_PATH}/TODO.md"

def parse_checklist():
    try:
        with open(MARKDOWN_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return { "status": "error", "message": f"Could not read markdown: {e}" }

    checklist = []
    for line in lines:
        match = re.match(r"- \[( |x)\] (.+)", line)
        if match:
            done = match.group(1) == "x"
            text = match.group(2).strip()
            checklist.append((done, text))

    total = len(checklist)
    completed = sum(1 for item in checklist if item[0])
    next_item = next((text for done, text in checklist if not done), None)

    return {
        "status": "ok",
        "total": total,
        "completed": completed,
        "next": next_item or "well done!"
    }
# Allow local development from Tronbyt app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
def parse_checklist(path=MARKDOWN_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read file: {e}"
        }

    checklist = []
    for line in lines:
        match = re.match(r"- \[( |x)\] (.+)", line)
        if match:
            done = match.group(1) == "x"
            text = match.group(2).strip()
            checklist.append((done, text))

    total = len(checklist)
    completed = sum(1 for item in checklist if item[0])
    next_item = next((text for done, text in checklist if not done), None)

    return {
        "status": "ok",
        "total": total,
        "completed": completed,
        "next": next_item or "well done!"
    }

@app.get("/")
def index():
    return {"ok": True, "version":"0.1.0", "hint": "use /focus or /healthz"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/focus")
def get_focus():
    return parse_checklist()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
