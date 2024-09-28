from elasticsearch import Elasticsearch
from elasticsearch7 import Elasticsearch as Elasticsearch7
from datetime import datetime
import random
import threading
import time

# Configuração do Elasticsearch
ES_HOST = 'http://192.168.15.4:9200'
INDEX_NAME = 'backend'  # Nome do índice a ser criado

# Função para criar conexão com o Elasticsearch
def create_es_client(host):
    return Elasticsearch7([host])

# Função para criar um índice no Elasticsearch
def create_index(client, index_name):
    index_mapping = {
        "mappings": {
            "properties": {
                "serviceName": {
                    "type": "keyword"
                },
                "environment": {
                    "type": "keyword"
                },
                "podName": {
                    "type": "keyword"
                },
                "providerMsgReceived": {
                    "type": "text"
                },
                "providerMsgSent": {
                    "type": "text"
                },
                "providerHeaderReceived": {
                    "type": "text"
                },
                "requestMethod": {
                    "type": "keyword"
                },
                "requestPayloadReceived": {
                    "type": "text"
                },
                "requestPayloadReturned": {
                    "type": "text"
                },
                "responseHttpStatus": {
                    "type": "keyword"
                },
                "tid": {
                    "type": "keyword"
                },
                "timestamp": {
                    "type": "date"
                }
            }
        }
    }

    if not client.indices.exists(index=index_name):
        try:
            client.indices.create(index=index_name, body=index_mapping)
            print(f"Índice '{index_name}' criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar índice: {e}")
    else:
        print(f"Índice '{index_name}' já existe.")

# Função para enviar logs ao Elasticsearch
def send_log(client, doc_id):
    doc = {
        'author': f'author_{doc_id}',
        'text': f'Interesting content {random.randint(1, 100)}...',
        'timestamp': datetime.now(),
        'environment': 'test',
        'podName': 'pod_test',
        'providerMsgReceived': 'Message received',
        'providerMsgSent': 'Message sent',
        'providerHeaderReceived': 'Header received',
        'requestMethod': 'GET',
        'requestPayloadReceived': 'Payload received',
        'requestPayloadReturned': 'Payload returned',
        'responseHttpStatus': '200',
        'tid': 'transaction_id',
        'serviceName': 'teste',
    }
    try:
        resp = client.index(index=INDEX_NAME, id=doc_id, document=doc)
        print(f"Log enviado com sucesso: {resp['result']}")
    except Exception as e:
        print(f"Erro ao enviar log: {e}")

# Função para enviar logs em threads
def log_sender_thread(client, count, interval):
    for i in range(4053, count):
        send_log(client, i)
        time.sleep(interval)

# Função principal para criar o índice e enviar múltiplos logs
def main():
    es_client = create_es_client(ES_HOST)

    # Número de logs a enviar por segundo
    logs_per_second = 400
    total_logs = 500000  # Total de logs a enviar
    interval = 1 / logs_per_second  # Intervalo entre envios

    # Iniciar múltiplas threads para enviar logs
    threads = []
    for _ in range(1000):  # Número de threads
        thread = threading.Thread(target=log_sender_thread, args=(es_client, total_logs // 10, interval))
        threads.append(thread)
        thread.start()

    # Esperar todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
