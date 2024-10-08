# orch-intrusion-detection-alarm-pf - 1.0.0

#### Orquestra: sam-one
#### Orquestra: r-unique-person
#### Orquestra: r-alarm-unique-person 
#### Orquestra: orch-intrusion-alarm-activated

Acessado por: POST /access/v1/orch-intrusion-detection-alarm-pf

Ambiente: Middleware

Adaptador: HTTP Adapter

### Descrição

```bash
    Este orquestrador é responsável por receber o alarme de detecção de incêndio
```

### Consumidores
| Consumidor | Client-id  |
|------------|------------|
| Raspberry  | Raspyan-fd |

### Histórico de alterações
| Versão |    Data    |     Autor    |     Demanda     |    Descrição   | Revisor | Entrega em UAT |
|--------|------------|--------------|-----------------|----------------|---------|----------------|
| 1.0    | 18/09/2024 | Rafael Prado | Demanda inicial | Versão inicial | -       | -              |

### Mensagem MW

Mensagem (JSON) de requisição
```bash
    POST - http://{server}:{port}/access/v1/orch-intrusion-detection-alarm-pf
    messageId: {messageId}
    clientId: {clientId}
    token: {tokenJWT}

    body: {
        "clientID": "?",
        "alarmId": "?"
    }
```

Mensagem (JSON) de resposta
```bash
    HTTP/1.1 204

    body: {}
```

### Mapeamento de entrada

|        Tag SPPIDIMW         |                  Desctição                 |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|--------------------------------------------|--------------------|----------------------|-------|
| equipament_id               | ID do equipamento cadastrado               | Sim                |  string              | -     |
| client_id                   | ID do cliente responsável pelo equipamento | Sim                |  string              | -     |

### Mapeamento de saída

|        Tag SPPIDIMW         |                  Desctição                 |     Obrigatório    |     Tipo de dado     | Regra |
|-----------------------------|--------------------------------------------|--------------------|----------------------|-------|


### Fluxograma

![fluxograma-orch-intrusion-detection-alarm-pf](fluxograma-orch-intrusion-detection-alarm-pf.png)

### Diagrama
![diagrama-orch-intrusion-detection-alarm-pf](diagrama-orch-intrusion-detection-alarm-pf.png)


### Serviços executados

| Ordem execução |       Serviço executado        | Adaptador |                      Regra                      | Paradigma | Tipo da mensagem |
|----------------|--------------------------------|-----------|-------------------------------------------------|-----------|------------------|
| 1              | sam-one                        | HTTP      | Executar sempre                                 | SYNC      | request          |
| 2              | r-unique-person                | HTTP      | Executar se sucesso no step sam-one             | SYNC      | request          |
| 3              | r-alarm-unique-person          | HTTP      | Executar se sucesso no step r-unique-person     | SYNC      | request          |
| 4              | orch-intrusion-alarm-activated | HTTP      | Executar se sucesso no step r-alarm-unique-person | SYNC      | request          |

### Regras

|   Condição  |         Regra        |
|-------------|----------------------|
| Timeout     | 5s                   |
| Retentativa | 5x a cada 5 segundos |
| Repetição   | -                    |
| Intervalo   | -                    |

### Mapeamentos

### Request

sam-one
|   Mappeia de:  |   Mapeia para:   | Obrigatório |    Obervação    |
|----------------|------------------|-------------|-----------------|
| tokenJWT       | tokenJWT         | Sim         | Enviado no body |

r-unique-person
|   Mappeia de:  |   Mapeia para:   | Obrigatório |    Obervação    |
|----------------|------------------|-------------|-----------------|
| client_id      | client_id        | Sim         | Enviado no body |

r-alarm-unique-person
|   Mappeia de:  |   Mapeia para:   | Obrigatório |    Obervação    |
|----------------|------------------|-------------|-----------------|
| equipament_id  | equipament_id    | Sim         | Enviado no body |
| client_id      | client_id        | Sim         | Enviado no body |


#### Response

sam-one
|   Mappeia de:  |   Mapeia para:   | Obrigatório |    Obervação    |
|----------------|------------------|-------------|-----------------|

r-unique-person
|         Mappeia de:        |         Mapeia para:         | Obrigatório |    Obervação    |
|----------------------------|------------------------------|-------------|-----------------|
| cpf                        | cpf                          | Não         | -               |
| full_name                  | full_name                    | Sim         | -               |
| phone_numer                | phone_numer                  | Não         | -               |
| first_contact_name         | first_contact_name           | Sim         | -               |
| first_contact_phone_numer  | first_contact_phone_numer    | Sim         | -               |
| second_contact_name        | second_contact_name          | Sim         | -               |
| second_contact_phone_numer | second_contact_phone_numer   | Sim         | -               |
| client_id                  | client_id                    | Sim         | -               |
| contract_id                | contract_id                  | Não         | -               |
| user_name                  | user_name                    | Não         | -               |
| user_password              | user_password                | Não         | -               |
| zip_code                   | zip_code                     | Sim         | -               |
| address_number             | address_number               | Sim         | -               |

orch-intrusion-alarm-activated

|         Mappeia de:        |         Mapeia para:         | Obrigatório |    Obervação    |
|----------------------------|------------------------------|-------------|-----------------|


### Erros funcionais

Condições de sucesso

| Código MW | Descrição | Código retornado do provedor  |
|-----------|-----------|-------------------------------|
| 204       | Sucesso   | Todos os serviços com sucesso |

Condições de erro

| Código MW |                  Descrição                 |   Código retornado do provedor   |
|-----------|--------------------------------------------|----------------------------------|
| 401       | Token inválido                             | sam-one.http = 401               |
| 404       | Cliente não encontrado                     | r-unique-person.http = 404       |
| 404       | Câmera não encontrada                      | r-unique-person-alarm.http = 404 |
| 550       | 550 + erro retornado do serviço com falha  | Qualquer erro não mapeado        |

