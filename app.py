from flask import Flask
from flask_cors import CORS
from settings import FLASK_DEBUG
from src.controller import init_app


# Create Flask app
#app = Flask(__name__)
app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS
CORS(app,origins="*", supports_credentials=True)
""" CORS(
    app,
    origins=[
        "http://10.204.0.22:3000",
        "http://localhost:3000",
        "http://a862de0c00aea498b8162d1a7c410d0b-1175022926.us-east-1.elb.amazonaws.com",
        "http://devops.altimetrik.io",
        "https://frontend-service.query-panel.svc.cluster.local:3000/query-ui",
        "http://frontend-service.query-panel.svc.cluster.local:3000/query-ui",
        "https://frontend-service.query-panel.svc.cluster.local:80/query-ui",
        "http://frontend-service.query-panel.svc.cluster.local:80/query-ui"
        
    ],
    supports_credentials=True
    ) """
# Initialize app
init_app(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=FLASK_DEBUG)
