from flask import Flask, jsonify, request, render_template
from collections import deque
import threading
import time

app = Flask(__name__)

# In-Memory Datenspeicherung
metrics_data = {}
MAX_ENTRIES = 1000

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    data = request.json
    server_id = data['server_id']
    
    if server_id not in metrics_data:
        metrics_data[server_id] = deque(maxlen=MAX_ENTRIES)
    
    metrics_data[server_id].append(data)
    print(f"Empfangen von {server_id}: CPU {data['cpu_percent']}%")
    return jsonify({'status': 'success'})

@app.route('/api/metrics/<server_id>')
def get_metrics(server_id):
    if server_id in metrics_data:
        return jsonify(list(metrics_data[server_id]))
    return jsonify([])

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)