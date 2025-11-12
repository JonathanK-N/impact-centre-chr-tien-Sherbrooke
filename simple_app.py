from flask import Flask
import os
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def hello():
    logger.info('Route / accessed')
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Impact Centre Chrétien Sherbrooke</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #0F172A; text-align: center; }
            .status { background: #10B981; color: white; padding: 10px; border-radius: 5px; text-align: center; margin: 20px 0; }
            .info { background: #EFF6FF; padding: 20px; border-radius: 5px; border-left: 4px solid #3B82F6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏛️ Impact Centre Chrétien Sherbrooke</h1>
            <div class="status">✅ Application déployée avec succès sur Railway!</div>
            <div class="info">
                <h3>🚀 Statut du déploiement</h3>
                <p><strong>Environnement:</strong> Production</p>
                <p><strong>Version:</strong> 1.0.0</p>
                <p><strong>Plateforme:</strong> Railway</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    logger.info('Health check accessed')
    return {'status': 'OK', 'service': 'Impact Centre Chrétien Sherbrooke'}

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f'Starting app on port {port}')
    app.run(host='0.0.0.0', port=port, debug=False)