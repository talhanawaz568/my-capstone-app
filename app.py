kkfrom flask import Flask, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capstone App | {{ environment }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 48px;
            max-width: 560px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 24px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        h1 {
            font-size: 28px;
            margin-bottom: 8px;
            color: #f8fafc;
        }
        .subtitle {
            color: #94a3b8;
            font-size: 15px;
            margin-bottom: 32px;
        }
        .env-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 32px;
        }
        .env-dev { background: #1e3a8a; color: #93c5fd; }
        .env-staging { background: #78350f; color: #fcd34d; }
        .env-prod { background: #7f1d1d; color: #fca5a5; }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 24px;
        }
        .info-item {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 16px;
        }
        .info-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #64748b;
            margin-bottom: 6px;
        }
        .info-value {
            font-size: 14px;
            color: #e2e8f0;
            font-weight: 600;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }
        .footer {
            margin-top: 32px;
            padding-top: 24px;
            border-top: 1px solid #334155;
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }
        .footer strong { color: #94a3b8; }
    </style>
</head>
<body>
    <div class="card">
        <div class="status-badge">
            <span class="status-dot"></span>
            SERVICE HEALTHY
        </div>
        <span class="env-tag env-{{ environment }}">{{ environment }}</span>
        <h1>Capstone Deployment Pipeline</h1>
        <p class="subtitle">GitOps CI/CD powered by ArgoCD + Kustomize</p>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Version</div>
                <div class="info-value">{{ version }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Environment</div>
                <div class="info-value">{{ environment }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Pod Hostname</div>
                <div class="info-value">{{ hostname }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Server Time</div>
                <div class="info-value">{{ server_time }}</div>
            </div>
        </div>

        <div class="footer">
            Deployed via <strong>GitHub Actions</strong> → <strong>ArgoCD</strong> → <strong>Kubernetes</strong>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def hello():
    return render_template_string(
        HTML_TEMPLATE,
        version=os.environ.get('APP_VERSION', 'v1'),
        environment=os.environ.get('ENVIRONMENT', 'dev'),
        hostname=socket.gethostname(),
        server_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    )

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
