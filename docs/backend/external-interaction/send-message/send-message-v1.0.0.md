# send-message - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-sensor-interaction

Acessado por (Rota interna): POST /access/v1/send-message

### Descrição
    Serviço responsável por enviar mensagens aos whatsapps responsáveis.

Ambiente: Backend External Interaction

Adaptador: HTTP Adapter

Paradigma: SYNC

Provedor: WAAPI

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
    POST http://server:port/v1/send-message
    messageId: {message-id}
    clientId: {client-id}

    {
        "responsible_person":"[
            full_name,
            phone,
            message
        ]"
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

|        Tag SPPIDIMW         |                  Desctição                 |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|--------------------------------------------|--------------------|----------------------|-------|
| responsible_person          | Lista contendo Nome, Telefone e mensagem   | Sim                |  string              | -     |


## Mapeamento de saída

|        Tag SPPIDIMW         | Desctição |     Obrigatório    |     Tipo de dado     |  Regra |
|-----------------------------|-----------|--------------------|----------------------|--------|




## Códigos de Retorno
### Condição de Sucesso

| Codigo PMID | Condição / Código retornado do banco  |
|-------------|---------------------------------------|
| HTTP 200	  | SE WAAPI[OUT] == Sucesso              |

### Condição de Erro

| Codigo PMID |         Condição / Código retornado do banco          |
|-------------|-------------------------------------------------------|
| HTTP 412	  | SE tags obrigatórias não foram enviadas               |
| HTTP 550	  | Erro genérico Ou qualquer erro não mapeado            |


