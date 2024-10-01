from flask import Flask, request, jsonify
from elasticsearch7 import Elasticsearch as Elasticsearch7
import logging
from datetime import datetime
import psycopg2
import os, json
import threading
from time import sleep

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

db_postgres_host = os.environ.get('POSTGRES-HOST', 'localhost')
db_postgres_port = os.environ.get('POSTGRES-PORT', '5432')
db_postgres_user = os.environ.get('POSTGRES-USER', 'sppidi')
db_postgres_password = os.environ.get('POSTGRES-PASSWORD', 'sppidi')
db_postgres_database = os.environ.get('POSTGRES-DATABASE', 'sppidi')

serviceName = os.environ.get('SVC-NAME', 'd-condominium')

db_connection = psycopg2.connect(host=db_postgres_host,
                                 port=db_postgres_port,
                                 user='root',
                                 password=db_postgres_password,
                                 database=db_postgres_database
                                )
db_connection.autocommit = True
cursor = db_connection.cursor()

def send_logs_es(doc):
    client.index(index=es_index, document=doc)

@app.route('/access/v1/d-condominium', methods=['POST'])
def svc_r_cam_info():
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
        
    
    if 'client_id' not in body:
        if 'condominium_id' not in body:   
            error_message = {'error':'Missing mandatory fields'}
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
            logger.error(f'{message_id} | - | payloadReturn | - | {error_message}')
            logger.error(f'{message_id} | - | httpStatus | - | 400')
            total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
            logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
            return jsonify(error_message), 400   
    
    logger.debug(f'{message_id} | - | starting body conversion to variables')
    if 'client_id' not in body:
        condominium_id = body.get('condominium_id')
    if 'condominium_id' not in body: 
        client_id = body.get('client_id')

       
    logger.debug(f'{message_id} | - | body converted to variables')
    
    logger.info(f'{message_id} | - | starting select data from database')
    
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'text': 'starting query into database',
        'tid': message_id,
        'serviceName': serviceName,
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
        
    try:
        if 'condominium_id' not in body: 
            cursor.execute(f"DELETE FROM condominium WHERE client_id='{client_id}'")
        if 'client_id' not in body: 
            cursor.execute(f"DELETE FROM condominium WHERE condominium_id='{condominium_id}'")
        try:
            client_response = cursor.fetchone()
        except:
            client_response = []
        if client_response == None:
            response_error = {"error":"cliente inexistente"}
            if 'condominium_id' not in body: 
                doc = {
                    'timestamp': datetime.now(),
                    'environment': 'b-prd',
                    'text': f"DELETE FROM condominium WHERE client_id='{client_id}'",
                    'tid': message_id,
                    'serviceName': serviceName,
                }
            else:
                doc = {
                    'timestamp': datetime.now(),
                    'environment': 'b-prd',
                    'text': f"DELETE FROM condominium WHERE condominium_id='{condominium_id}'",
                    'tid': message_id,
                    'serviceName': serviceName,
                }
            thread = threading.Thread(target=send_logs_es, args=(doc,))
            thread.start()
            sleep(0.001)
            doc = {
                'timestamp': datetime.now(),
                'environment': 'b-prd',
                'requestPayloadReturned': f"{response_error}",
                'tid': message_id,
                'serviceName': serviceName,
                'responseHttpStatus': 404
            }
            thread = threading.Thread(target=send_logs_es, args=(doc,))
            thread.start()
            logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
            logger.error(f'{message_id} | - | httpStatus | - | 404')
            total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
            logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
            return ({'response':f'{response_error}'}), 404
        if 'condominium_id' not in body: 
            doc = {
                'timestamp': datetime.now(),
                'environment': 'b-prd',
                'text': f"DELETE FROM condominium WHERE client_id='{client_id}'",
                'tid': message_id,
                'serviceName': serviceName,
            }
        else:
            doc = {
                'timestamp': datetime.now(),
                'environment': 'b-prd',
                'text': f"DELETE FROM condominium WHERE condominium_id='{condominium_id}'",
                'tid': message_id,
                'serviceName': serviceName,
            }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
    except Exception as e:
        response_error = str(e)
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': response_error,
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
        return ({'response':f'{response_error}'}), 500
         
    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
    response = {'success': f'{client_response}'}
    doc = {
        'timestamp': datetime.now(),
        'environment': 'b-prd',
        'requestPayloadReturned': json.dumps(response),
        'tid': message_id,
        'serviceName': serviceName,
        'totalTime': total_time,
        'responseHttpStatus': 200
    }
    thread = threading.Thread(target=send_logs_es, args=(doc,))
    thread.start()
    logger.info(f'{message_id} | - | payloadReturn | - | {response}')
    logger.info(f'{message_id} | - | httpStatus | - | 200')
    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
    logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
    return response, 200

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True)
