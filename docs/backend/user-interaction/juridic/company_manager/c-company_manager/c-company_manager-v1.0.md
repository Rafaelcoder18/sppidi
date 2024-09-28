# c-company-manager - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/c-company-manager

### Descrição
    Serviço responsável por criar um responsável de determinada empresa.

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
    POST http://server:port/v1/c-company-manager
    messageId: {message-id}
    clientId: {client-id}

    {
        "cnpj":"?",
        "social_reason":"?",
        "contract_id":"?",
        "email":"?",
        "user_name":"?",
        "user_password":"?",
        "zip_code":"?",
        "address_number":"?"
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

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|---------------------------------|-------|
| document                    | Documento da empresa               | Sim                |  string              |  CNPJ                           | -     |
| social_reason               | Nome da empresa                    | Sim                |  string              |  SOCIAL_REASON                  | -     |
| contract_id                 | ID do contrato vigente da empresa  | Sim                |  string              |  CONTRACT_ID                    | -     |
| email                       | Email do responsável pela empresa  | Sim                |  string              |  EMAIL                          | -     |
| user_name                   | Usuário de acesso ao sistema       | Sim                |  char(13)            |  USER_NAME                      | -     |
| user_password               | Senha de acesso ao sistema         | Sim                |  string              |  USER_PASSWORD                  | -     |
| postcode                    | CEP do endereço da empresa         | Sim                |  string              |  ZIP_CODE                       | -     |
| address_number              | Número do endereço da empresa      | Sim                |  char(13)            |  ADDRESS_NUMBER                 | -     |



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


