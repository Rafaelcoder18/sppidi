# r-cam-unique-person-info - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-sensor-interaction

Acessado por (Rota interna): POST /access/v1/r-cam-unique-person-info

### Descrição
    Serviço responsável por retornar informações de câmera de um cliente pessoa física.

Ambiente: Backend

Adaptador: DB Adapter

Paradigma: SYNC

Acessa: postgres relacional

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
        "equipament_id": "?",
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
    "equipament_id": "?",
    "client_id": "?"
    "cam_description": "?",
    "cam_model": "?",
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
| equipament_id               | Identificador unico do equipamento | Sim                |  string              |  -     |
| client_id                   | ID do cliente responsável          | Sim                |  string              |  -     |
| cam_description             | Descrição da câmera                | Sim                |  string              |  -     |
| cam_model                   | Modelo da câmera                   | Sim                |  string              |  -     |




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


