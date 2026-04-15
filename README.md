# Security-SOAR 🧠🛡️

Advanced Security Orchestration, Automation, and Response (SOAR) engine. Designed to automate incident response by ingesting telemetry, validating threats via external intelligence, and executing containment protocols.

## 🔄 The Security Pipeline
Designed to work with **[SentinelSoc](https://github.com/Jorgeotero1998/SentinelSoc)**:
1. **Detection**: SentinelSoc identifies suspicious file activity.
2. **Orchestration**: `Security-SOAR` queries **VirusTotal API** and notifies via **Telegram**.
3. **Response**: Automatically suspends malicious processes.

## 🛠️ Tech Stack
- Python 3.x
- VirusTotal API
- Telegram Bot API
- Psutil
