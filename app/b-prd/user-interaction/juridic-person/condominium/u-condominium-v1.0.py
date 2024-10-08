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
db_postgres_user = os.environ.get('POSTGRES-USER', 'postgres')

db_postgres_password = os.environ.get('POSTGRES-PASSWORD', 'sppidi')
db_postgres_database = os.environ.get('POSTGRES-DATABASE', 'sppidi')

serviceName = os.environ.get('SVC-NAME', 'u-unique-person')

db_connection = psycopg2.connect(host=db_postgres_host,
                                 port=db_postgres_port,
                                 user=db_postgres_user,
                                 password=db_postgres_password,
                                 database=db_postgres_database
                                )
db_connection.autocommit = True
cursor = db_connection.cursor()

def send_logs_es(doc):
    client.index(index=es_index, document=doc)

@app.route('/access/v1/u-unique-person', methods=['POST'])
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
        
    
    if ('client_id' not in body) or ('condominium_id' not in body) or ('first_contact_name' not in body) or ('first_contact_phone_numer' not in body) or ('second_contact_name' not in body) or ('second_contact_phone_numer' not in body) or ('client_id' not in body) or ('contract_id' not in body) or ('user_name' not in body) or ('user_password' not in body) or ('zip_code' not in body) or ('address_number' not in body):   
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
    client_id = body.get('client_id')
    condominium_id = body.get('condominium_id')
    first_contact_name = body.get('first_contact_name')
    first_contact_phone_numer = body.get('first_contact_phone_numer')
    second_contact_name = body.get('second_contact_name')
    second_contact_phone_numer = body.get('second_contact_phone_numer')
    client_id = body.get('client_id')
    contract_id = body.get('contract_id')
    user_name = body.get('user_name')
    user_password = body.get('user_password')
    zip_code = body.get('zip_code')
    address_number = body.get('address_number')
       
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
        cursor.execute(f"UPDATE condominium SET condominium_id='{condominium_id}', first_contact_name='{first_contact_name}', first_contact_phone_numer='{first_contact_phone_numer}', second_contact_name='{second_contact_name}', second_contact_phone_numer='{second_contact_phone_numer}', contract_id='{contract_id}', user_name='{user_name}', user_password='{user_password}', zip_code='{zip_code}', address_number='{address_number}' WHERE client_id='{client_id}' AND client_id='{client_id}'")
        db_connection.commit()
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': f"UPDATE condominium SET condominium_id='{condominium_id}', first_contact_name='{first_contact_name}', first_contact_phone_numer='{first_contact_phone_numer}', second_contact_name='{second_contact_name}', second_contact_phone_numer='{second_contact_phone_numer}', contract_id='{contract_id}', user_name='{user_name}', user_password='{user_password}', zip_code='{zip_code}', address_number='{address_number}' WHERE client_id='{client_id}' AND client_id='{client_id}'",
            'tid': message_id,
            'serviceName': serviceName,
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
    except psycopg2.errors.UniqueViolation as e:
        response_error = {"error":"cliente já cadastrado"}
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': f"UPDATE condominium SET condominium_id='{condominium_id}', first_contact_name='{first_contact_name}', first_contact_phone_numer='{first_contact_phone_numer}', second_contact_name='{second_contact_name}', second_contact_phone_numer='{second_contact_phone_numer}', contract_id='{contract_id}', user_name='{user_name}', user_password='{user_password}', zip_code='{zip_code}', address_number='{address_number}' WHERE client_id='{client_id}' AND client_id='{client_id}'",
            'tid': message_id,
            'serviceName': serviceName,
            'responseHttpStatus': 409
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
            'responseHttpStatus': 409
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.error(f'{message_id} | - | payloadReturn | - | {response_error}')
        logger.error(f'{message_id} | - | httpStatus | - | 409')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
        return ({'response':f'{response_error}'}), 409
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
    logger.info(f'{message_id} | - | httpStatus | - | 204')
    total_time = int((datetime.now() - start_time).total_seconds() * 1000)  # Calcula o tempo total de execução em ms
    logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
    return '', 204

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True)
