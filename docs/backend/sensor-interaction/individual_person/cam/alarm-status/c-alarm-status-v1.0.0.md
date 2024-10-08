# c-alarm-status - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-sensor-interaction

Acessado por (Rota interna): POST /access/v1/r-cam-unique-person-info

### Descrição
    Serviço responsável por criar um status de alarme no banco de dados, para controle de alarmistica.

Ambiente: Backend

Adaptador: DB Adapter

Paradigma: SYNC

Acessa: redis não relacional

|    Consumidor    |  Client-id  | 
|------------------|-------------|
| orch-unique-user | UNIQUE USER |

## Histórico de alterações
| Versão |    Data    |     Autor    |     Demanda     |    Descrição   | Revisor | Entrega em UAT |
|--------|------------|--------------|-----------------|----------------|---------|----------------|
| 1.0    | 18/09/2024 | Rafael Prado | Demanda inicial | Versão inicial | -       | -              |

### Mensagem Backend

## Mensagem de requisição

```bash
    POST http://server:port/v1/r-cam-unique-person-info
    messageId: {message-id}
    clientId: {client-id}

    {
        "cam_id": "?",
        "client_id": "?"
    }

    Obs.: O messageId e o clientId são parâmetros que devem ser enviado no Header Http.
    Obs.: O clientId enviado no body representa a credencial do cliente.
```

## Mensagem de erro

```
HTTP Status

{
    "description": "string",
    "provider": {
        "serviceName": "string",
        "errorCode": "string",
        "errorMessage": "string"
    }
}
```

## Mensagem de sucesso

```
HTTP/1.1 204

{

}
```


## Mapeamento de entrada

|        Tag SPPIDIMW         |                  Desctição                 |     Obrigatório    |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|--------------------------------------------|--------------------|----------------------|---------------------------------|-------|
| equipament_id               | ID do equipamento cadastrado               | Sim                |  string              |  SENSOR_ID                      | -     |
| client_id                   | ID do cliente responsável pelo equipamento | Sim                |  string              |  FULL_NAME                      | -     |


## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     |  Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|--------|




## Códigos de Retorno
### Condição de Sucesso

| Codigo PMID | Condição / Código retornado do banco  |
|-------------|---------------------------------------|
| HTTP 204	  | SE DB_Response[OUT] == Sucesso        |

### Condição de Erro

| Codigo PMID |         Condição / Código retornado do banco          |
|-------------|-------------------------------------------------------|
| HTTP 412	  | SE tags obrigatórias não foram enviadas               |
| HTTP 550	  | Erro genérico                                         |


