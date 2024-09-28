# u-sensor-juridic-person - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-sensor-interaction

Acessado por (Rota interna): PATCH /access/v1/u-sensor-juridic-person

### Descrição
    Serviço responsável por atualizar o sensor de um cliente pessoa jurídica.

Ambiente: Backend

Adaptador: DB Adapter

Paradigma: SYNC

Acessa: postgres relacional

|    Consumidor    |  Client-id  | 
|------------------|-------------|
| orch-juridic-user | UNIQUE USER |

## Histórico de alterações
| Versão |    Data    |     Autor    |     Demanda     |    Descrição   | Revisor | Entrega em UAT |
|--------|------------|--------------|-----------------|----------------|---------|----------------|
| 1.0    | 18/09/2024 | Rafael Prado | Demanda inicial | Versão inicial | -       | -              |

### Mensagem Backend

## Mensagem de requisição

```bash
    PATCH http://server:port/v1/u-sensor-juridic-person
    messageId: {message-id}
    clientId: {client-id}

    {
        "sensor_id": "?",
        "client_id": "?",
        "sensor_description": "?",
        "sensor_model": "?",
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
    "success":"?"
}
```


## Mapeamento de entrada

|        Tag SPPIDIMW         |                  Desctição                 |     Obrigatório    |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|--------------------------------------------|--------------------|----------------------|---------------------------------|-------|
| equipament_id               | ID do equipamento cadastrado               | Sim                |  string              |  SENSOR_ID                      | -     |
| client_id                   | ID do cliente responsável pelo equipamento | Sim                |  string              |  FULL_NAME                      | -     |
| sensor_description          | Descrição do equipamento                   | Sim                |  string              |  SENSOR_DESCRIPTION             | -     |
| sensor_model                | Modelo do equipamento                      | Sim                |  string              |  SENSOR_MODEL                   | -     |


## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     |  Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|--------|
| success                     | Descrição de sucesso               | Sim                |  string              |  -     |




## Códigos de Retorno
### Condição de Sucesso

| Codigo PMID | Condição / Código retornado do banco  |
|-------------|---------------------------------------|
| HTTP 204	  | SE DB_Response[OUT] == Sucesso        |

### Condição de Erro

| Codigo PMID |         Condição / Código retornado do banco          |
|-------------|-------------------------------------------------------|
| HTTP 409	  | SE DB_Response[OUT] == Constante única violada        |
| HTTP 412	  | SE tags obrigatórias não foram enviadas               |
| HTTP 550	  | Erro genérico                                         |


