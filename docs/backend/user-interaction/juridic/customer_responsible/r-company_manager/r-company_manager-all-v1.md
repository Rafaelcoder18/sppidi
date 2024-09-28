# r-all-condominium - 1.0.0

Content-Type: application/jsom

Orquestrado por: Orch-user-interaction

Acessado por (Rota interna): GET /access/v1/r-all-condominium

### Descrição
    Serviço responsável por retornar todos os condominios cadastrados.

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
    GET http://server:port/v1/r-all-condominium
    messageId: {message-id}
    clientId: {client-id}

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
    "company_managers":
    {
        cpf":"?",
        full_name":"?",
        email":"?",
        user_name":"?",
        user_password":"?",
        company":"?"
    };
}
```


## Mapeamento de entrada

|        Tag SPPIDIMW         |              Desctição             |             Obrigatório            |     Tipo de dado     |        Tag banco de dados       | Regra |
|-----------------------------|------------------------------------|------------------------------------|----------------------|---------------------------------|-------|



## Mapeamento de saída

|        Tag SPPIDIMW         |              Desctição             |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|------------------------------------|--------------------|----------------------|-------|
| document                    | Documento do gerente da companhia  | Sim                |  string              | -     |
| full_name                   | Nome do gerente da companhia       | Sim                |  string              | -     |
| email                       | Email do gerente da companhia      | Sim                |  string              | -     |
| user_name                   | Usuário do gerente da companhia    | Sim                |  char(13)            | -     |
| user_password               | Senha do gerente da companhia      | Sim                |  string              | -     |
| company                     | Companhia do gerente               | Sim                |  char(13)            | -     |


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


