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

serviceName = os.environ.get('SVC-NAME', 'send-message')
servicePort = os.environ.get('SVC-PORT', '5001')

waapi_instance = os.environ.get('WAAP-INSTANCE', '21971')
waapi_token = os.environ.get('WAAPI-TOKEN', 'cMtj1lLbTbWddy6njIaSwQ8p3ccwimOtI9HcoHPV1a603f10')

def send_logs_es(doc):
    client.index(index=es_index, document=doc)
    

@app.route('/access/v1/send-message', methods=['POST'])
def svc_sam_one():
    start_time = datetime.now()  # Captura o início da execução
    message_id = request.headers.get('messageId', None)
    header_client_id = request.headers.get('clientId', None)
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        
    if 'responsible_person' not in body or len(body.get('responsible_person')) == 0:
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
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
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return jsonify(error_message), 400   
    
    logger.debug(f'{message_id} | - | starting body conversion to variables')
    responsible_person = body.get('responsible_person')
    logger.debug(f'{message_id} | - | body converted to variables')
    
    logger.info(f'{message_id} | - | calling WAAPI to send message')
    
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'text': 'calling WAAPI to send message',
        'tid': message_id,
        'serviceName': serviceName,
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
        
    try:
        for costumer in responsible_person:
            url = f"https://waapi.app/api/v1/instances/{waapi_instance}/client/action/send-message"

            payload = {
                "chatId": f"{costumer[1]}@c.us",
                f"message": costumer[2]
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {waapi_token}"
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                print(response.json())
                response = response.json()['data']
                if response['status'] != 'success':
                    response_error = 'Error to send message'
                    doc = {
                        'timestamp': datetime.now(),
                        'environment': 'b-prd',
                        'text': 'Error to send message',
                        'tid': message_id,
                        'serviceName': serviceName,
                        'responseHttpStatus': 500
                    }
                    thread = threading.Thread(target=send_logs_es, args=(doc,))
                    thread.start()
                    logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
                    logger.error(f'{message_id} | - | httpStatus | - | 500')
                    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
                    logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
                    return (response_error), 500
            except Exception as e:
                response_error = str(e)
                doc = {
                    'timestamp': datetime.now(),
                    'environment': 'b-prd',
                    'text': f"Error to send message",
                    'tid': message_id,
                    'serviceName': serviceName,
                    'responseHttpStatus': 500
                }
                thread = threading.Thread(target=send_logs_es, args=(doc,))
                thread.start()
                logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
                logger.error(f'{message_id} | - | httpStatus | - | 500')
                total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
                logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
                return (response_error), 500
        
    except Exception as e:
        response_error = str(e)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': f"Error to send message",
            'tid': message_id,
            'serviceName': serviceName,
            'responseHttpStatus': 500
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
        logger.error(f'{message_id} | - | httpStatus | - | 500')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return (response_error), 500

    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'requestPayloadReturned': '',
        'tid': message_id,
        'serviceName': serviceName,
        'totalTime': total_time,
        'responseHttpStatus': 204
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
    logger.info(f'{message_id} | - | payloadReturn | - | ')
    logger.info(f'{message_id} | - | httpStatus | - | 200')
    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
    logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
    return '', 204

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True, port=servicePort)
