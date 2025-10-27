from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Flask server is running'})

@app.route('/api/leads', methods=['POST'])
def create_lead():
    return jsonify({'success': True, 'message': 'Lead received'})

if __name__ == '__main__':
    print("Starting simple Flask server on http://localhost:5050")
    app.run(host='127.0.0.1', port=5050, debug=True)


