import psutil
import requests
import time
import json
from datetime import datetime

def collect_metrics():
    # Disk Usage für alle Partitionen
    disk_usage = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.mountpoint] = {
                'percent': round(usage.percent, 1),
                'used_gb': round(usage.used / (1024**3), 1),
                'total_gb': round(usage.total / (1024**3), 1)
            }
        except PermissionError:
            # Manchmal kann man nicht auf alle Laufwerke zugreifen
            continue

    return {
        'timestamp': datetime.now().isoformat(),
        'server_id': 'server-1',
        'cpu_percent': psutil.cpu_percent(interval=1),
        'ram_percent': psutil.virtual_memory().percent,
        'ram_used_gb': round(psutil.virtual_memory().used / (1024**3), 1),
        'disk_usage': disk_usage
    }

def send_metrics():
    server_url = "http://localhost:5000/api/metrics"  # Backend URL
    
    try:
        metrics = collect_metrics()
        response = requests.post(server_url, json=metrics)
        
        if response.status_code == 200:
            print(f"✅ Daten gesendet: CPU {metrics['cpu_percent']}%, RAM {metrics['ram_percent']}%")
        else:
            print(f"❌ Fehler beim Senden: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")

if __name__ == "__main__":
    print("🚀 Agent gestartet - Drücke Ctrl+C zum Stoppen")
    
    try:
        while True:
            send_metrics()
            time.sleep(30)  # Alle 30 Sekunden senden
    except KeyboardInterrupt:
        print("\n🛑 Agent gestoppt")