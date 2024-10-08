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

sam_one_host = os.environ.get('SAM-ONE-HOST', 'localhost')
sam_one_port = os.environ.get('SAM-ONE-PORT', '5001')
sam_one_uri = os.environ.get('SAM-ONE-URI', '/access/v1/valid-sam-one')

r_unique_person_host = os.environ.get('R-UNIQUE-PERSON-HOST', 'localhost')
r_unique_person_port = os.environ.get('R-UNIQUE-PERSON-PORT', '5002')
r_unique_person_uri = os.environ.get('R-UNIQUE-PERSON-URI', '/access/v1/r-unique-person')

r_cam_unique_person_host = os.environ.get('R-CAM-UNIQUE-PERSON-HOST', 'localhost')
r_cam_unique_person_port = os.environ.get('R-CAM-UNIQUE-PERSON-PORT', '5003')
r_cam_unique_person_uri = os.environ.get('R-CAM-UNIQUE-PERSON-URI', '/access/v1/r-cam-unique-person')

orch_fire_alarm_activated_host = os.environ.get('ORCH-FIRE-ALARM-ACTIVATED-HOST', 'localhost')
orch_fire_alarm_activated_port = os.environ.get('ORCH-FIRE-ALARM-ACTIVATED-PORT', '5004')
orch_fire_alarm_activated_uri = os.environ.get('ORCH-FIRE-ALARM-ACTIVATED-URI', '/access/v1/orch-fire-alarm-activated')

def send_logs_es(doc):
    client.index(index=es_index, document=doc)

@app.route('/access/v1/orch-fire-detection-alarm', methods=['POST'])
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
    if tokenJWT == None:
        error_message = {'error':'Missing Access Token'}
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
        
    
    if ('equipament_id' not in body) or ('client_id' not in body):
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
    equipament_id = body.get('equipament_id')
    request_client_id = body.get('client_id')
    logger.debug(f'{message_id} | - | body converted to variables')
    
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
        url = f'http://{sam_one_host}:{sam_one_port}/{sam_one_uri}'

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
            'alarmID': f'{equipament_id}'
        }

        # Enviando a requisição POST
        auth_token = requests.post(url, headers=headers, data=json.dumps(data))
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
    # Fim da execução do sam-one para validação do token, e dados do usuário
    # ========================================================================================================================
    # Inicio da execução do r-unique-person para coletar dados do usuário
    if auth_token.status_code == 204:
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
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
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
    
        logger.info(f'{message_id} | - | calling r-unique-person')
        
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'text': 'calling r-unique-person ',
            'tid': message_id,
            'serviceName': serviceName,
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
            
        try:

            # URL do endpoint
            url = f'http://{r_unique_person_host}:{r_unique_person_port}/{r_unique_person_uri}'

            # Headers
            headers = {
                'Content-Type': 'application/json',
                'messageId': f'{message_id}',
                'clientId': f'{header_client_id}'
            }

            # Corpo da requisição (payload)
            data = {
                'client_id': f'{request_client_id}'
            }

            # Enviando a requisição POST
            client_info = requests.post(url, headers=headers, data=json.dumps(data))
            
            logger.info(f'{message_id} | - | payloadReturn | - | ')
            logger.info(f'{message_id} | - | httpStatus | - | 204')
            logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')
            # Fim da execução do r-unique-person para validação do token, e dados do usuário
            # ========================================================================================================================
            # Inicio da execução do r-cam-unique-person para coletar dados do usuário
            if client_info.status_code == 200:
                client_data = client_info.json()['success']
                client_data = list(eval(client_data))
                contact_name_1, contact_phone_1 = client_data[3], client_data[4]
                contact_name_2, contact_phone_2 = client_data[5], client_data[6]
                
                logger.info(f'{message_id} | - | calling r-cam-unique-person')
        
                doc = {
                    'timestamp': datetime.now(),
                    'environment': 'b-prd',
                    'text': 'calling r-cam-unique-person ',
                    'tid': message_id,
                    'serviceName': serviceName,
                }
                thread = threading.Thread(target=send_logs_es, args=(doc,))
                thread.start()
                
                try:
                    url = f'http://{r_cam_unique_person_host}:{r_cam_unique_person_port}/{r_cam_unique_person_uri}'

                    # Headers
                    headers = {
                        'Content-Type': 'application/json',
                        'messageId': f'{message_id}',
                        'clientId': f'{header_client_id}'
                    }

                    # Corpo da requisição (payload)
                    data = {
                        'cam_id': f'{equipament_id}'
                    }

                    # Enviando a requisição POST
                    cam_info = requests.post(url, headers=headers, data=json.dumps(data))
                    if cam_info.status_code == 200:
                        logger.info(f'{message_id} | - | orcg-fire-alarm-activated')
        
                        doc = {
                            'timestamp': datetime.now(),
                            'environment': 'b-prd',
                            'text': 'orcg-fire-alarm-activated ',
                            'tid': message_id,
                            'serviceName': serviceName,
                        }
                        thread = threading.Thread(target=send_logs_es, args=(doc,))
                        thread.start()
                        
                        try:
                            url = f'http://{orch_fire_alarm_activated_host}:{orch_fire_alarm_activated_port}{orch_fire_alarm_activated_uri}'

                            # Headers
                            headers = {
                                'Content-Type': 'application/json',
                                'messageId': f'{message_id}',
                                'clientId': f'{header_client_id}'
                            }

                            # Corpo da requisição (payload)
                            data = {
                                'responsible_person': f'[
                                    
                                ]'
                            }
                            orch_fire_alarm_activated = requests.post(url, headers=headers, data=json.dumps(data))
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
                    else:
                        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
                        response = {
                            "description": f"{cam_info.text}",
                            "provider": {
                                "serviceName": "r-cam-unique-person",
                                "errorCode": "404",
                                "errorMessage": f"{cam_info.text}"
                            }
                        }
                        doc = {
                            'timestamp': datetime.now(),
                            'environment': 'b-prd',
                            'requestPayloadReturned': json.dumps(response),
                            'tid': message_id,
                            'serviceName': serviceName,
                            'totalTime': total_time,
                            'responseHttpStatus': 404
                        }
                        thread = threading.Thread(target=send_logs_es, args=(doc,))
                        thread.start()
                        logger.info(f'{message_id} | - | payloadReturn | - | {response}')
                        logger.info(f'{message_id} | - | httpStatus | - | 404')
                        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
                        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')

                        return response, 404
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
                return '', 204
            else:
                total_time = int((datetime.now() - start_time).total_seconds() * 1000)
                response = {
                    "description": f"{client_info.text}",
                    "provider": {
                        "serviceName": "r-unique-person",
                        "errorCode": "404",
                        "errorMessage": f"{client_info.text}"
                    }
                }
                doc = {
                    'timestamp': datetime.now(),
                    'environment': 'b-prd',
                    'requestPayloadReturned': json.dumps(response),
                    'tid': message_id,
                    'serviceName': serviceName,
                    'totalTime': total_time,
                    'responseHttpStatus': 404
                }
                thread = threading.Thread(target=send_logs_es, args=(doc,))
                thread.start()
                logger.info(f'{message_id} | - | payloadReturn | - | {response}')
                logger.info(f'{message_id} | - | httpStatus | - | 404')
                total_time = int((datetime.now() - start_time).total_seconds() * 1000)
                logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')

                return response, 404
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
    
    elif auth_token.status_code == 401:
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        response = {
            "description": f"{auth_token.text}",
            "provider": {
                "serviceName": "sam-one",
                "errorCode": "401",
                "errorMessage": f"{auth_token.text}"
            }
        }
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps(response),
            'tid': message_id,
            'serviceName': serviceName,
            'totalTime': total_time,
            'responseHttpStatus': 401
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.info(f'{message_id} | - | payloadReturn | - | {response}')
        logger.info(f'{message_id} | - | httpStatus | - | 401')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')

        return response, 401
    
    else:
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        response = {
            "description": f"{auth_token.text}",
            "provider": {
                "serviceName": "sam-one",
                "errorCode": "550",
                "errorMessage": f"{auth_token.text}"
            }
        }
        doc = {
            'timestamp': datetime.now(),
            'environment': 'b-prd',
            'requestPayloadReturned': json.dumps(response),
            'tid': message_id,
            'serviceName': serviceName,
            'totalTime': total_time,
            'responseHttpStatus': 550
        }
        thread = threading.Thread(target=send_logs_es, args=(doc,))
        thread.start()
        logger.info(f'{message_id} | - | payloadReturn | - | {response}')
        logger.info(f'{message_id} | - | httpStatus | - | 550')
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.info(f'{message_id} | - | totalExecutionTime | - | {total_time} ms')

        return response, 550

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
if __name__ == '__main__':
    app.run(debug=True)
