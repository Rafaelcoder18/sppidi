# r-condominium - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/r-condominium

### Descrição
    Serviço responsável por retornar dados de um condominio.

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
    DELETE http://server:port/v1/r-condominium
    messageId: {message-id}
    clientId: {client-id}

    {
        "condominium_id":"?"
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
    "client_id":"?",
    "condominium_id":"?",
    "first_contact_name":"?",
    "first_contact_phone_numer":"?",
    "second_contact_name":"?",
    "second_contact_phone_numer":"?",
    "zip_code":"?",
    "address_number":"?"
}
```


## Mapeamento de entrada

|        Tag SPPIDIMW         |              Desctição             |             Obrigatório            |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|------------------------------------|------------------------------------|----------------------|---------------------------------|-------|
| condominium_id              | Identificador do condominio        | Sim                                |  string              |  CONDOMINIUM_ID                 | -     |



## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|-------|
| client_id                   | Validador do cliente da requisição | Sim                |  string              | -     |
| condominium_id              | ID do condomínio                   | Sim                |  string              | -     |
| first_contact_name          | Nome do responsável 1              | Sim                |  string              | -     |
| first_contact_phone_nubmer  | Telefone do responsável 1          | Sim                |  char(13)            | -     |
| second_contact_name         | Nome do responsável 2              | Sim                |  string              | -     |
| second_contact_phone_number | Telefone do responsável 2          | Sim                |  char(13)            | -     |
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


