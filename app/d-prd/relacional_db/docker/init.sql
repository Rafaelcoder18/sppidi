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

DROP TABLE IF EXISTS unique_person;
CREATE TABLE IF NOT EXISTS unique_person(
    cpf CHAR(8) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone_numer CHAR(13) NOT NULL,
    first_contact_name VARCHAR(255) NOT NULL,
    first_contact_phone_numer CHAR(13) NOT NULL,
    second_contact_name VARCHAR(255) NOT NULL,
    second_contact_phone_numer CHAR(13) NOT NULL,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    contract_id VARCHAR(255) UNIQUE NOT NULL,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    zip_code CHAR(8) NOT NULL,
    address_number INT NOT NULL    
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

DROP TABLE IF EXISTS unique_person_sensor;
CREATE TABLE IF NOT EXISTS unique_person_sensor(
    sensor_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    sensor_description VARCHAR(255) NOT NULL,
    sensor_model VARCHAR(255) NOT NULL,
    alarmistic_time TIMESTAMP NOT NULL  
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

DROP TABLE IF EXISTS unique_person_cam;
CREATE TABLE IF NOT EXISTS unique_person_cam(
    cam_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    cam_description VARCHAR(255) NOT NULL,
    cam_model VARCHAR(255) NOT NULL
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

DROP TABLE IF EXISTS business_contract;
CREATE TABLE IF NOT EXISTS business_contract(
    contract_id BIGINT PRIMARY KEY,
    contract_name VARCHAR(255) NOT NULL,
    contract_company CHAR(14) UNIQUE NOT NULL,
    effective_date TIMESTAMP NOT NULL
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

DROP TABLE IF EXISTS company_manager;
CREATE TABLE IF NOT EXISTS company_manager(
    cnpj CHAR(14) PRIMARY KEY,
    social_reason VARCHAR(255) UNIQUE,
    create_time TIMESTAMP NOT NULL,
    contract_id INT UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    zip_code CHAR(8) NOT NULL,
    address_number INT NOT NULL
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

DROP TABLE IF EXISTS customer_responsible;
CREATE TABLE IF NOT EXISTS customer_responsible(
    cpf CHAR(8) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    company CHAR(14) NOT NULL
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


DROP TABLE IF EXISTS juridic_person;
CREATE TABLE IF NOT EXISTS juridic_person(
    cnpj CHAR(14) PRIMARY KEY,
    social_reason VARCHAR(255) NOT NULL,
    phone_numer CHAR(13) NOT NULL,
    first_contact_name VARCHAR(255) NOT NULL,
    first_contact_phone_numer CHAR(13) NOT NULL,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    contract_id VARCHAR(255) UNIQUE NOT NULL,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    zip_code CHAR(8) NOT NULL,
    address_number INT NOT NULL    
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


DROP TABLE IF EXISTS condominium;
CREATE TABLE IF NOT EXISTS condominium(
    client_id VARCHAR(255) UNIQUE NOT NULL,
    condominium_id VARCHAR(255) UNIQUE NOT NULL,
    first_contact_name VARCHAR(255) NOT NULL,
    first_contact_phone_numer CHAR(13) NOT NULL,
    second_contact_name VARCHAR(255) NOT NULL,
    second_contact_phone_numer CHAR(13) NOT NULL,
    zip_code CHAR(8) NOT NULL,
    address_number INT NOT NULL    
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

DROP TABLE IF EXISTS juridic_person_sensor;
CREATE TABLE IF NOT EXISTS juridic_person_sensor(
    sensor_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    sensor_description VARCHAR(255) NOT NULL,
    sensor_model VARCHAR(255) NOT NULL,
    alarmistic_time TIMESTAMP NOT NULL  
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

DROP TABLE IF EXISTS juridic_person_cam;
CREATE TABLE IF NOT EXISTS juridic_person_cam(
    cam_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    cam_description VARCHAR(255) NOT NULL,
    cam_model VARCHAR(255) NOT NULL
);
