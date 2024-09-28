# c-unique-person - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/c-unique-person

### Descrição
    Serviço responsável por criar um cliente pessoa física.

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
    POST http://server:port/v1/c-unique-person
    messageId: {message-id}
    clientId: {client-id}

    {
        "cpf":"?",
        "full_name":"?",
        "phone_numer":"?",
        "first_contact_name":"?",
        "first_contact_phone_numer":"?",
        "second_contact_name":"?",
        "second_contact_phone_numer":"?",
        "client_id":"?",
        "contract_id":"?",
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
| document                    | Documento do cliente               | Sim                |  char(8)             |  CPF                            | -     |
| full_name                   | Nome completo do cliente           | Sim                |  string              |  FULL_NAME                      | -     |
| phone_numer                 | Telefone do cliente                | Sim                |  char(13)            |  PHONE_NUMER                    | -     |
| first_contact_name          | Nome do responsável 1              | Sim                |  string              |  FIRST_CONTACT_NAME             | -     |
| first_contact_phone_nubmer  | Telefone do responsável 1          | Sim                |  char(13)            |  FIRST_CONTACT_PHONE_NUMBER     | -     |
| second_contact_name         | Nome do responsável 2              | Sim                |  string              |  SECOND_CONTACT_NAME            | -     |
| second_contact_phone_number | Telefone do responsável 2          | Sim                |  char(13)            |  SECOND_CONTACT_PHONE_NUMBER    | -     |
| client_id                   | Validador do cliente da requisição | Sim                |  string              |  CLIENT_ID                      | -     |
| contract_id                 | ID do contrato em vigência         | Sim                |  string              |  CONTRACT_ID                    | -     |
| user_name                   | Usuário de acesso do cliente       | Sim                |  string              |  USER_NAME                      | -     |
| user_password               | Credencial de acesso do cliente    | Sim                |  string              |  USER_PASSWORD                  | -     |
| postcode                    | CEP da rua do imóvel do cliente    | Sim                |  char(8)             |  ZIP_CODE                       | -     |
| address_number              | Número do imóvel do cliente        | Sim                |  Integer             |  ADDRESS_NUMBER                 | -     |


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


