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
                "requestHeaderReceived": {
                    "type": "text"
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
                "totalTime": {
                    "type": "text"
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
def send_log(client):
    doc = {
        'author': f'author_',
        'text': f'Interesting content {random.randint(1, 100)}...',
        'timestamp': datetime.now(),
        'environment': 'test',
        'podName': 'pod_test',
        'providerMsgReceived': 'Message received',
        'providerMsgSent': 'Message sent',
        'providerHeaderReceived': 'Header received',
        'requestHeaderReceived': 'Header received',
        'requestMethod': 'GET',
        'requestPayloadReceived': 'Payload received',
        'requestPayloadReturned': 'Payload returned',
        'responseHttpStatus': '200',
        'tid': 'transaction_id',
        'serviceName': 'teste',
    }
    try:
        resp = client.index(index=INDEX_NAME, document=doc)
        print(f"Log enviado com sucesso: {resp['result']}")
    except Exception as e:
        print(f"Erro ao enviar log: {e}")

# Função principal para criar o índice e enviar múltiplos logs
def main():
    es_client = create_es_client(ES_HOST)
    create_index(es_client, INDEX_NAME)
if __name__ == "__main__":
    main()
