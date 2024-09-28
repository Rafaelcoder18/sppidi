from elasticsearch import Elasticsearch
from elasticsearch7 import Elasticsearch as Elasticsearch7
from datetime import datetime
import random

# Configuração do Elasticsearch
ES_HOST = 'http://192.168.15.4:9200'
INDEX_NAME = 'frontend'  # Nome do índice a ser criado

# Função para criar conexão com o Elasticsearch
def create_es_client(host):
    return Elasticsearch7([host])

# Função para criar um índice no Elasticsearch
def create_index(client, index_name):
    # Definindo um mapeamento básico para o índice
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

    # Verifica se o índice já existe
    if not client.indices.exists(index=index_name):
        try:
            client.indices.create(index=index_name, body=index_mapping)
            print(f"Índice '{index_name}' criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar índice: {e}")
    else:
        print(f"Índice '{index_name}' já existe.")
        
es_client = create_es_client(ES_HOST)
create_index(es_client, INDEX_NAME)