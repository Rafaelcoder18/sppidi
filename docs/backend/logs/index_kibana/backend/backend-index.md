## Criação de index Backend

```
Este indice é responsável por possuir os logs de serviços backend de interação com banco de dados
```

## Histórico de alterações
| Versão |    Data    |     Autor    |     Demanda     |    Descrição   | Revisor | Entrega em UAT |
|--------|------------|--------------|-----------------|----------------|---------|----------------|
| 1.0    | 18/09/2024 | Rafael Prado | Demanda inicial | Versão inicial | -       | -              |


## Criação do index

### Campos e tipos

|         nome           |    Tipo do campo    |             obervação           |
|------------------------|---------------------|---------------------------------|
| enviroment             | keyword             | ambiente                        |
| podName                | keyword             | nome do pod                     |
| providerMsgReceived    | text                | body recebido do provedor       |
| providerMsgSent        | text                | body enviado ao provedor        |
| providerHeaderReceived | text                | header recebida do provedor     |
| requestMethod          | keyword             | Método de chamada da request    |
| requestPayloadReceived | text                | Payload de requisição recebido  |
| requestPayloadReturned | text                | Payload de requisição retornado |
| responseHttpStatus     | keyword             | Status da execução              |
| tid                    | date                | Identificador da transação      |


### json

{
    "mappings": {
        "properties": {
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
