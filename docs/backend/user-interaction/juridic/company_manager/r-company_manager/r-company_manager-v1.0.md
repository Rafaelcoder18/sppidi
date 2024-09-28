# r-company-manager - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/r-company-manager

### Descrição
    Serviço responsável por retornar dados de um responsável por empresa.

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
    GET http://server:port/v1/r-company-manager
    messageId: {message-id}
    clientId: {client-id}

    {
        cpf":"?"
    };

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
    "cnpj":"?",
    "social_reason":"?",
    "contract_id":"?",
    "email":"?",
    "user_name":"?",
    "user_password":"?",
    "zip_code":"?",
    "address_number":"?"
};

```


## Mapeamento de entrada

|        Tag SPPIDIMW         |              Desctição             |             Obrigatório            |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|------------------------------------|------------------------------------|----------------------|---------------------------------|-------|



## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|-------|
| document                    | Documento da empresa               | Sim                |  string              | -     |
| social_reason               | Nome da empresa                    | Sim                |  string              | -     |
| contract_id                 | ID do contrato vigente da empresa  | Sim                |  string              | -     |
| email                       | Email do responsável pela empresa  | Sim                |  string              | -     |
| user_name                   | Usuário de acesso ao sistema       | Sim                |  char(13)            | -     |
| user_password               | Senha de acesso ao sistema         | Sim                |  string              | -     |
| postcode                    | CEP do endereço da empresa         | Sim                |  string              | -     |
| address_number              | Número do endereço da empresa      | Sim                |  char(13)            | -     |





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


