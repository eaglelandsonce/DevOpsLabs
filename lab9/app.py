limport os
from flask import Flask, jsonify
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def home():
    return {
        'message': 'Secure CI/CD Demo',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'timestamp': datetime.utcnow().isoformat()
    }


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'checks': {'database': 'ok'}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
