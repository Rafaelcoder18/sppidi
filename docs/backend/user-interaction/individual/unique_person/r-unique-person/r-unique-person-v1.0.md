# c-unique-person - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/d-unique-person

### Descrição
    Serviço responsável por excluir um cliente pessoa física.

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
    DELETE http://server:port/v1/c-unique-person
    messageId: {message-id}
    clientId: {client-id}

    {
        "cpf":"?",
        "client_id":"?",
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

```bash
HTTP/1.1 200

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
```


## Mapeamento de entrada

|        Tag SPPIDIMW         |              Desctição             |             Obrigatório            |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|------------------------------------|------------------------------------|----------------------|---------------------------------|-------|
| document                    | Documento do cliente               | Sim (Se client_id não foi enviado) |  char(8)             |  CPF                            | -     |
| client_id                   | Validador do cliente da requisição | Sim (Se document não foi enviado)  |  string              |  CLIENT_ID                      | -     |



## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|-------|
| document                    | Documento do cliente               | Sim                |  char(8)             | -     |
| full_name                   | Nome completo do cliente           | Sim                |  string              | -     |
| phone_numer                 | Telefone do cliente                | Sim                |  char(13)            | -     |
| first_contact_name          | Nome do responsável 1              | Sim                |  string              | -     |
| first_contact_phone_nubmer  | Telefone do responsável 1          | Sim                |  char(13)            | -     |
| second_contact_name         | Nome do responsável 2              | Sim                |  string              | -     |
| second_contact_phone_number | Telefone do responsável 2          | Sim                |  char(13)            | -     |
| client_id                   | Validador do cliente da requisição | Sim                |  string              | -     |
| contract_id                 | ID do contrato em vigência         | Sim                |  string              | -     |
| user_name                   | Usuário de acesso do cliente       | Sim                |  string              | -     |
| user_password               | Credencial de acesso do cliente    | Sim                |  string              | -     |
| postcode                    | CEP da rua do imóvel do cliente    | Sim                |  char(8)             | -     |
| address_number              | Número do imóvel do cliente        | Sim                |  Integer             | -     |



## Códigos de Retorno
### Condição de Sucesso

| Codigo PMID | Condição / Código retornado do banco  |
|-------------|---------------------------------------|
| HTTP 200	  | SE DB_Response[OUT] == Sucesso        |

### Condição de Erro

| Codigo PMID |         Condição / Código retornado do banco          |
|-------------|-------------------------------------------------------|
| HTTP 404	  | Usuário deletado não foi encontrado no banco          |
| HTTP 550	  | Erro genérico                                         |


