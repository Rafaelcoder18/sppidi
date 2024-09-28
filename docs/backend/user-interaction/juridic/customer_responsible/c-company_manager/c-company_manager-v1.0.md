# c-company-manager - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): POST /access/v1/c-company-manager

### Descrição
    Serviço responsável por criar um gerente de compania.

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
        cpf":"?",
        full_name":"?",
        email":"?",
        user_name":"?",
        user_password":"?",
        company":"?"
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
| document                    | Documento do gerente da companhia  | Sim                |  string              |  CPF                            | -     |
| full_name                   | Nome do gerente da companhia       | Sim                |  string              |  FULL_NAME                      | -     |
| email                       | Email do gerente da companhia      | Sim                |  string              |  EMAIL                          | -     |
| user_name                   | Usuário do gerente da companhia    | Sim                |  char(13)            |  USER_NAME                      | -     |
| user_password               | Senha do gerente da companhia      | Sim                |  string              |  USER_PASSWORD                  | -     |
| company                     | Companhia do gerente               | Sim                |  char(13)            |  COMPANY                        | -     |



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


