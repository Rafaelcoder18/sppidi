from flask import Flask, request, jsonify
import logging
from datetime import datetime
import random

# Configuração do logger com formatação personalizada
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        if record.levelname == 'INFO':
            color_code = '\033[34m' 
        elif record.levelname == 'WARNING':
            color_code = '\033[33m' 
        elif record.levelname == 'DEBUG':
            color_code = '\033[32m'
        elif record.levelname == 'ERROR':
            color_code = '\033[31m' 
        reset_code = '\033[0m'
        
        service_name = "MangoSC"
        domain = "sensor-pf-interaction | SPPIDI_ENV | b-prd"
        container_name = "orch-auth-user"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        action = record.getMessage()

        log_message = (
            f"{log_time}\t{color_code}{record.levelname}{reset_code}\t"
            f"{service_name} | {domain} | - | {container_name} | "
            f"{timestamp} | - | - | {action}"
        )
        
        return log_message

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(CustomFormatter())
logger.addHandler(file_handler)

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_message():
    level = request.json.get('level', 'INFO')
    message = request.json.get('message', 'No message provided')
    
    if level.upper() == 'INFO':
        logger.info(message)
    elif level.upper() == 'WARNING':
        logger.warning(message)
    elif level.upper() == 'DEBUG':
        logger.debug(message)
    elif level.upper() == 'ERROR':
        logger.error(message)
    else:
        return jsonify({"error": "Invalid log level"}), 400
    
    return jsonify({"status": "Logged", "level": level, "message": message}), 200

@app.route('/generate-logs', methods=['POST'])
def generate_logs():
    for _ in range(10):  # Gera 10 logs aleatórios
        level = random.choice(['DEBUG'])
        message = f"Random log message {random.randint(1, 100)}"
        logger.log(getattr(logging, level), message)
    return jsonify({"status": "Logs generated"}), 200

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True)
