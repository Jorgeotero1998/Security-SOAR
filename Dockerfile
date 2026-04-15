FROM python:3.11-slim`nWORKDIR /app`nCOPY requirements.txt .`nRUN pip install --no-cache-dir -r requirements.txt`nCOPY . .`nCMD ["python", "orchestrator.py"]
