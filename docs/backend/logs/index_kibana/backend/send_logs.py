from elasticsearch7 import Elasticsearch as Elasticsearch7
from datetime import datetime

ES_HOST = 'http://192.168.15.4:9200'
INDEX_NAME = 'backend'  # Nome do índice a ser criado

# Função para enviar logs ao Elasticsearch
def send_log(client, author, text, doc_id):
    doc = {
        'author': author,
        'text': text,
        'timestamp': datetime.now(),
        "enviroment": '<valor>',
        "podName": '<valor>',
        "providerMsgReceived": '<valor>',
        "providerMsgSent": '<valor>',
        "providerHeaderReceived": '<valor>',
        "requestMethod": '<valor>',
        "requestPayloadReceived": '<valor>',
        "requestPayloadRturned": '<valor>',
        "responseHttpStatus": '<valor>',
        "tid": '<valor>',
        "serviceName": '<valor>',
    }
    try:
        # Enviar o documento para o índice especificado
        resp = client.index(index=INDEX_NAME, id=doc_id, document=doc)
        return resp['result']
    except Exception as e:
        print(f"Erro ao enviar log: {e}")
        return None
