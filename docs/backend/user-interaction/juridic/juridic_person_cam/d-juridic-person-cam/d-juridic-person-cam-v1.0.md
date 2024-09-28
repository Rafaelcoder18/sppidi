# d-cam-juridic-person - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-cam-interaction

Acessado por (Rota interna): DELETE /access/v1/d-cam-juridic-person

### Descrição
    Serviço responsável por excluir a câmera de um cliente pessoa juridica.

Ambiente: Backend

Adaptador: DB Adapter

Paradigma: SYNC

Acessa: postgres relacional

|    Consumidor     |  Client-id   | 
|-------------------|--------------|
| orch-juridic-user | JURIDIC USER |

## Histórico de alterações
| Versão |    Data    |     Autor    |     Demanda     |    Descrição   | Revisor | Entrega em UAT |
|--------|------------|--------------|-----------------|----------------|---------|----------------|
| 1.0    | 18/09/2024 | Rafael Prado | Demanda inicial | Versão inicial | -       | -              |

### Mensagem Backend

## Mensagem de requisição

```bash
    DELETE http://server:port/v1/d-cam-juridic-person
    messageId: {message-id}
    clientId: {client-id}

    {
        "cam_id": "?"
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
| cam_id                      | ID do equipamento cadastrado               | Sim                |  string              |  CAM_ID                         | -     |


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
| HTTP 404	  | SE DB_Response[OUT] == Câmera não encontrada          |
| HTTP 412	  | SE tags obrigatórias não foram enviadas               |
| HTTP 550	  | Erro genérico                                         |


