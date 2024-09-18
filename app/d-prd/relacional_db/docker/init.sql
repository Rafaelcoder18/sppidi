/*
Esta tabela é responsável por manter os clientes pessoa física, que possuem acesso a
Câmeras e sensores. Cada gerente deve estar atrelado a um gerente, portanto, podem 
existir diversos clientes para cada gerente.

A tabela possui os seguintes campos
clientes pessoa física
    - CPF titular
    - Nome do titular
    - Telefone
    - Nome contato 1
    - Telefone contato 1
    - Nome contato 2
    - Telefone contato 2
    - Client ID
    - ID do contrato
    - Usuário
    - Senha
    - CEP
    - Número
*/

DROP TABLE IF EXISTIS unique_person;
CREATE TABLE IF NOT EXISTIS unique_person(
    cpf CHAR(8) PRIMARY KEY;
    full_name VARCHAR(255) REQUIRED,
    phone_numer CHAR(13) REQUIRED,
    first_contact_name VARCHAR(255) REQUIRED,
    first_contact_phone_numer CHAR(13) REQUIRED,
    second_contact_name VARCHAR(255) REQUIRED,
    second_contact_phone_numer CHAR(13) REQUIRED,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    contract_id VARCHAR(255) UNIQUE REQUIRED,
    user_name VARCHAR(255) UNIQUE REQUIRED,
    user_password VARCHAR(255) REQUIRED,
    zip_code CHAR(8) REQUIRED,
    address_number INT REQUIRED    
);

/*
Esta tabela é responsável por manter os sensoores relacionados a pessoa física. Cada 
cliente pode possuir um ou vários sensores. Os sensores possuem um prefixo como "BAR-" 
para sensores de barreira, e, "PRE-" para sensores de presença.

A tabela possui os seguintes campos
Sensores de presença & Sensor de barreira
    - Id do sensor (Prefixo definido como "BAR-" para sensores de barreira, e, "PRE-" para sensores de presença)
    - Client ID
    - Descrição do sensor
    - Modelo do sensor
    - Tempo de alarmistica
*/

DROP TABLE IF EXISTIS unique_person_sensor;
CREATE TABLE IF NOT EXISTIS unique_person_sensor(
    sensor_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    sensor_description VARCHAR(255) REQUIRED,
    sensor_model VARCHAR(255) REQUIRED,
    alarmistic_time TIMESTAMP REQUIRED  
);



/*
Esta tabela é responsável por manter as câmeras relacionados a pessoa física. Cada 
cliente pode possuir um ou várias câmeras.

A tabela possui os seguintes campos
Câmeras de segurança
    - Id da câmera
    - Client ID
    - Câmera ID
    - Descrição da câmera
*/

DROP TABLE IF EXISTIS unique_person_cam;
CREATE TABLE IF NOT EXISTIS unique_person_cam(
    cam_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    cam_description VARCHAR(255) REQUIRED,
    cam_model VARCHAR(255) REQUIRED
);


-- ===============================================
-- Tabelas de pessoa jurídica
-- ===============================================

/*
Esta tabela armazena informações de contratos vigentes, que posteriormente serão
utilizados para a permissão e viabilidade do contrato com o cliente.

A tabela possui os seguintes campos
Contrato PJ
    - ID do contrato
    - Nome do contrato
    - Empresa do contrato
    - Data de vigência
    - Descrição do contrato
*/

DROP TABLE IF EXISTIS business_contract;
CREATE TABLE IF NOT EXISTIS business_contract(
    contract_id BIGINT PRIMARY KEY,
    contract_name VARCHAR(255) REQUIRED,
    contract_company CHAR(14) UNIQUE REQUIRED,
    effective_date TIMESTAMP REQUIRED
);


/*
Esta tabela é responsável por manter os administradores do sistema, que são responsáveis
por cadastrar, e gerenciar os responsáveis por cada cliente. Cada empresa possui apenas 
uma conta, e deve ser acessada apenas pelo responsável designado.

A tabela possui os seguintes campos
Administradores
    - CNPJ
    - Razão social
    - Data de cadastro
    - ID do contrato
    - Email
    - Usuário
    - Senha
    - CEP
    - Número
*/

DROP TABLE IF EXISTIS company_manager;
CREATE TABLE IF NOT EXISTIS company_manager(
    cnpj CHAR(14) PRIMARY KEY;
    social_reason VARCHAR(255) UNIQUE,
    create_time TIMESTAMP REQUIRED,
    contract_id INT UNIQUE REQUIRED,
    email VARCHAR(255) UNIQUE REQUIRED,
    user_name VARCHAR(255) UNIQUE REQUIRED,
    user_password VARCHAR(255) REQUIRED,
    zip_code CHAR(8) REQUIRED,
    address_number INT REQUIRED
);

/*
Esta tabela é responsável por manter os gerentes, que são responsáveis por gerenciar os 
clientes(Pessoa jurídica e física), condominios, Câmeras e sensores. Cada gerente deve estar 
atrelado a uma empresa, portanto, podem existir diversos gerentes para cada empresa.

A tabela possui os seguintes campos
Gerentes
    - CPF
    - Nome do colaborador
    - Email
    - Usuário
    - Senha
    - CNPJ atrelado
*/

DROP TABLE IF EXISTIS customer_responsible;
CREATE TABLE IF NOT EXISTIS customer_responsible(
    cpf CHAR(8) PRIMARY KEY;
    full_name VARCHAR(255) REQUIRED,
    email VARCHAR(255) UNIQUE REQUIRED,
    user_name VARCHAR(255) UNIQUE REQUIRED,
    user_password VARCHAR(255) REQUIRED,
    company CHAR(14) REQUIRED,
);


/*
Esta tabela é responsável por manter os clientes pessoa jurídica, que possuem acesso a
condominios atrelados, câmeras e sensores. Cada cliente deve estar atrelado a um gerente, 
portanto, podem existir diversos clientes para cada gerente.

A tabela possui os seguintes campos
clientes pessoa jurídica
    - CNPJ 
    - Razão social
    - Telefone
    - Nome contato 1
    - Telefone contato 1
    - Client ID
    - ID do contrato
    - Usuário
    - Senha
    - CEP
    - Número
*/


DROP TABLE IF EXISTIS juridic_person;
CREATE TABLE IF NOT EXISTIS juridic_person(
    cnpj CHAR(14) PRIMARY KEY;
    social_reason VARCHAR(255) REQUIRED,
    phone_numer CHAR(13) REQUIRED,
    first_contact_name VARCHAR(255) REQUIRED,
    first_contact_phone_numer CHAR(13) REQUIRED,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    contract_id VARCHAR(255) UNIQUE REQUIRED,
    user_name VARCHAR(255) UNIQUE REQUIRED,
    user_password VARCHAR(255) REQUIRED,
    zip_code CHAR(8) REQUIRED,
    address_number INT REQUIRED    
);



/*
Esta tabela é responsável por manter os condominios, que organizam os condominios atrelados
a determinadas empresas. Cada condominio deve estar atrelado a uma pessoa jurídica, portanto, 
podem existir diversos condominios para cada empresa.

A tabela possui os seguintes campos
Condominios
    - Condominio ID
    - Client ID 
    - CEP
    - Número
    - Nome contato 1
    - Telefone contato 1
    - Nome contato 2
    - Telefone contato 2
*/


DROP TABLE IF EXISTIS condominium;
CREATE TABLE IF NOT EXISTIS condominium(
    client_id VARCHAR(255) UNIQUE REQUIRED,
    condominium_id VARCHAR(255) UNIQUE REQUIRED,
    first_contact_name VARCHAR(255) REQUIRED,
    first_contact_phone_numer CHAR(13) REQUIRED,
    second_contact_name VARCHAR(255) REQUIRED,
    second_contact_phone_numer CHAR(13) REQUIRED,
    zip_code CHAR(8) REQUIRED,
    address_number INT REQUIRED    
);

/*
Esta tabela é responsável por manter os sensoores relacionados a pessoa jurídica. Cada 
cliente pode possuir um ou vários sensores. Os sensores possuem um prefixo como "BAR-" 
para sensores de barreira, e, "PRE-" para sensores de presença.

A tabela possui os seguintes campos
Sensores de presença & Sensor de barreira
    - Id do sensor (Prefixo definido como "BAR-" para sensores de barreira, e, "PRE-" para sensores de presença)
    - Client ID
    - Descrição do sensor
    - Modelo do sensor
    - Tempo de alarmistica
*/

DROP TABLE IF EXISTIS juridic_person_sensor;
CREATE TABLE IF NOT EXISTIS juridic_person_sensor(
    sensor_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    sensor_description VARCHAR(255) REQUIRED,
    sensor_model VARCHAR(255) REQUIRED,
    alarmistic_time TIMESTAMP REQUIRED  
);



/*
Esta tabela é responsável por manter as câmeras relacionados a pessoa jurídica. Cada 
cliente pode possuir um ou várias câmeras.

A tabela possui os seguintes campos
Câmeras de segurança
    - Id da câmera
    - Client ID
    - Câmera ID
    - Descrição da câmera
*/

DROP TABLE IF EXISTIS juridic_person_cam;
CREATE TABLE IF NOT EXISTIS juridic_person_cam(
    cam_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE REQUIRED,
    cam_description VARCHAR(255) REQUIRED,
    cam_model VARCHAR(255) REQUIRED
);
