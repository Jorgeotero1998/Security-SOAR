import os
import requests
import psutil
import json

class SecurityOrchestrator:
    def __init__(self, vt_api_key, telegram_token, chat_id):
        self.vt_key = vt_api_key
        self.tg_token = telegram_token
        self.chat_id = chat_id

    def check_virus_total(self, file_hash):
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"x-apikey": self.vt_key}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                stats = response.json()['data']['attributes']['last_analysis_stats']
                return stats.get('malicious', 0)
        except Exception:
            pass
        return 0

    def alert_admin(self, message):
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

    def isolate_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.suspend()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def handle_incident(self, event_data):
        pid = event_data.get('pid')
        file_hash = event_data.get('hash')
        file_path = event_data.get('path')
        malicious_score = self.check_virus_total(file_hash)
        if malicious_score > 0:
            isolation_success = self.isolate_process(pid)
            status = "Suspended" if isolation_success else "Isolation Failed"
            alert = (f"🚨 *Critical Threat Detected*\n\n"
                     f"Path: `{file_path}`\n"
                     f"VT Malicious Score: {malicious_score}\n"
                     f"Action: Process {pid} {status}")
            self.alert_admin(alert)

if __name__ == "__main__":
    orchestrator = SecurityOrchestrator(
        vt_api_key=os.getenv("VT_API_KEY"),
        telegram_token=os.getenv("TG_TOKEN"),
        chat_id=os.getenv("TG_CHAT_ID")
    )
    try:
        with open('sentinel_alerts.json', 'r') as f:
            for line in f:
                event = json.loads(line)
                if event.get('risk_level') == 'high':
                    orchestrator.handle_incident(event)
    except FileNotFoundError:
        pass
