from flask import Flask, request, jsonify
from elasticsearch7 import Elasticsearch as Elasticsearch7
import logging
from datetime import datetime
import requests
import os, json
import threading

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

es_host = os.environ.get('ES-HOST', '192.168.15.4')
es_port = os.environ.get('ES-PORT', '9200')
es_index = os.environ.get('ES-INDEX', 'backend')
client = Elasticsearch7([f'http://{es_host}:{es_port}'])

valid_client_ids = os.environ.get('VALID-CLIENT-IDS', ['client1', 'client2', 'client3'])

serviceName = os.environ.get('SVC-NAME', 'orch-fire-detection-alarm')

c_alarm_status_host = os.environ.get('C-ALARM-STATUS-HOST', 'localhost')
c_alarm_status_port = os.environ.get('C-ALARM-STATUS-PORT', '5001')
c_alarm_status_uri = os.environ.get('C-ALARM-STATUS-URI', '/access/v1/c-alarm-status')

send_message_host = os.environ.get('SEND-MESSAGE-HOST', 'localhost')
send_message_port = os.environ.get('SEND-MESSAGE-PORT', '5002')
send_message_uri = os.environ.get('SEND-MESSAGE-URI', '/access/v1/send-message')


def send_logs_es(doc):
    client.index(index=es_index, document=doc)

@app.route('/access/v1/orch-fire-alarm-activated', methods=['POST'])
def svc_r_cam_info():
    start_time = datetime.now()  # Captura o início da execução
    message_id = request.headers.get('messageId', None)
    header_client_id = request.headers.get('clientId', None)
    tokenJWT = request.headers.get('token', None)
    logger.info(f'{message_id} | - | requestStarting')
    body = request.json
    headers = request.headers
    header_info = ''
    for header, value in headers.items():
        header_info += (f'"{header}":"{value}",')

    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'providerHeaderReceived': header_info,
        'requestMethod': 'POST',
        'tid': message_id,
        'serviceName': serviceName,
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
    if message_id == None:
        error_message = {'error':'Missing Transaction ID'}
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'providerHeaderReceived': header_info,
            'requestMethod': 'POST',
            'tid': message_id,
            'serviceName': serviceName,
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps({'response':f'{error_message}'}),
            'tid': message_id,
            'serviceName': serviceName,
            'totalTime': total_time,
            'responseHttpStatus': 400
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {error_message}')
        logger.error(f'{message_id} | - | httpStatus | - | 400')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return jsonify(error_message), 400  
    if header_client_id == None:
        error_message = {'error':'Missing Client ID'}
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'providerHeaderReceived': header_info,
            'requestMethod': 'POST',
            'tid': message_id,
            'serviceName': serviceName,
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps({'response':f'{error_message}'}),
            'tid': message_id,
            'serviceName': serviceName,
            'totalTime': total_time,
            'responseHttpStatus': 400
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {error_message}')
        logger.error(f'{message_id} | - | httpStatus | - | 400')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return jsonify(error_message), 400
    if header_client_id not in valid_client_ids:
        error_message = {'error':'Invalid Client ID'}
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'providerHeaderReceived': header_info,
            'requestMethod': 'POST',
            'tid': message_id,
            'serviceName': serviceName,
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps({'response':f'{error_message}'}),
            'tid': message_id,
            'serviceName': serviceName,
            'totalTime': total_time,
            'responseHttpStatus': 401
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {error_message}')
        logger.error(f'{message_id} | - | httpStatus | - | 401')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return jsonify(error_message), 401  
    

                
    logger.info(f'{message_id} | - | requestBodyReceive | - | {body}')
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'requestPayloadReceived': json.dumps(body),
        'tid': message_id,
        'serviceName': serviceName,
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
        
    print(body)
    if ('cam_id' not in body) or ('client_id' not in body) or ('responsible_person' not in body):
        error_message = 'missing mandatory fields'
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'providerHeaderReceived': header_info,
            'requestMethod': 'POST',
            'tid': message_id,
            'serviceName': f'{serviceName}',
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps({'response':f'{error_message}'}),
            'tid': message_id,
            'serviceName': f'{serviceName}',
            'totalTime': total_time,
            'responseHttpStatus': 400
        }
        error_message = {'error':'Missing mandatory fields'}
        logger.error(f'{message_id} | - | payloadReturn | - | {error_message}')
        logger.error(f'{message_id} | - | httpStatus | - | 400')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return jsonify(error_message), 400   
    
    logger.debug(f'{message_id} | - | starting body conversion to variables')
    cam_id = body.get('cam_id')
    request_client_id = body.get('client_id')
    responsible_person = body.get('responsible_person')
    logger.debug(f'{message_id} | - | body converted to variables')
    print(responsible_person)
    logger.info(f'{message_id} | - | calling sam-one')
    
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'text': 'calling sam-one ',
        'tid': message_id,
        'serviceName': serviceName,
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
    
    # Execução do sam-one para validação do token, e dados do usuário
    try:

        # URL do endpoint
        url = f'http://{c_alarm_status_host}:{c_alarm_status_port}/{c_alarm_status_uri}'

        # Headers
        headers = {
            'Content-Type': 'application/json',
            'messageId': f'{message_id}',
            'clientId': f'{header_client_id}'
        }

        # Corpo da requisição (payload)
        data = {
            'jwtToken': f'{tokenJWT}',
            'clientID': f'{request_client_id}',
            'alarmID': f'{cam_id}'
        }

        # Enviando a requisição POST
        #c_alarm = requests.post(url, headers=headers, data=json.dumps(data))
        c_alarm = 204
        
        try:

            # URL do endpoint
            url = f'http://{send_message_host}:{send_message_port}/{send_message_uri}'

            # Headers
            headers = {
                'Content-Type': 'application/json',
                'messageId': f'{message_id}',
                'clientId': f'{header_client_id}'
            }

            # Corpo da requisição (payload)
            data = {
                'responsible_person': f'{responsible_person}'
            }
            # Enviando a requisição POST
            c_alarm = requests.post(url, headers=headers, data=json.dumps(data))
            print(c_alarm)
            
        except Exception as e:
            response_error = str(e)
            doc = {
                'timestamp': datetime.now(),
                'environment': 'b-prd',
                'text': str(e),
                'tid': message_id,
                'serviceName': serviceName,
                'responseHttpStatus': 500
            }
            thread = threading.Thread(target=send_logs_es, args=(doc,))
            thread.start()
            logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
            logger.error(f'{message_id} | - | httpStatus | - | 500')
            total_time = int((datetime.now() - start_time).total_seconds() * 1000)
            logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
            return ({'response':f'{response_error}'}), 500

            return response, 550
    
    except Exception as e:
        response_error = str(e)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': str(e),
            'tid': message_id,
            'serviceName': serviceName,
            'responseHttpStatus': 500
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
        logger.error(f'{message_id} | - | httpStatus | - | 500')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return ({'response':f'{response_error}'}), 500

        return response, 550

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True, port='5004')
