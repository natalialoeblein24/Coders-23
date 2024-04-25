BEGIN;

-- CRIAÇÃO DO MODELO FÍSICO

CREATE TABLE IF NOT EXISTS public.brand
(
	id smallserial PRIMARY KEY NOT NULL,
	name CHARACTER VARYING(30)
);

CREATE TABLE IF NOT EXISTS public.location
(
	id smallserial PRIMARY KEY NOT NULL,
	description CHARACTER VARYING(40) 	
);

CREATE TABLE IF NOT EXISTS public.model
(
	id smallserial PRIMARY KEY NOT NULL,
	model_type CHARACTER(6) NOT NULL,
	description CHARACTER VARYING(40), 
	engine_size REAL
);

CREATE TABLE IF NOT EXISTS public.machine
(
	id smallserial PRIMARY KEY NOT NULL,
	age SMALLINT NOT NULL,
	model_id SMALLINT REFERENCES public.model (id),
	location_id SMALLINT REFERENCES public.location (id),
	brand_id SMALLINT REFERENCES public.brand (id)
);
	
CREATE TABLE IF NOT EXISTS public.error_machine
(
	id smallserial PRIMARY KEY NOT NULL,
	error_type CHARACTER(6) NOT NULL,
	description CHARACTER VARYING(40)
);

CREATE TABLE IF NOT EXISTS public.register_error
(
	id smallserial PRIMARY KEY NOT NULL,
	datetime TIMESTAMP NOT NULL,
	machine_id SMALLINT REFERENCES public.machine (id),
	error_id SMALLINT REFERENCES public.error_machine (id)
);

CREATE TABLE IF NOT EXISTS public.component
(
	id smallserial PRIMARY KEY NOT NULL,
	comp_type CHARACTER(5) NOT NULL,
	description CHARACTER VARYING(40)
);

CREATE TABLE IF NOT EXISTS public.maintenance
(
	id smallserial PRIMARY KEY NOT NULL,
	datetime TIMESTAMP NOT NULL,
	comp_id SMALLINT REFERENCES public.component (id),
	machine_id SMALLINT REFERENCES public.machine (id)
);

CREATE TABLE IF NOT EXISTS public.failure
(
	id smallserial PRIMARY KEY NOT NULL,
	datetime TIMESTAMP NOT NULL,
	comp_id SMALLINT REFERENCES public.component (id),
	machine_id SMALLINT REFERENCES public.machine (id)
);

CREATE TABLE IF NOT EXISTS public.telemetry
(
	id serial PRIMARY KEY NOT NULL,
	datetime TIMESTAMP NOT NULL,
	volt double precision NOT NULL,
	rotate double precision NOT NULL,
	pressure double precision NOT NULL,
	vibration double precision NOT NULL,
	machine_id SMALLINT REFERENCES public.machine (id)
);

-- Comentamos as tabelas temporárias após as cargas serem feitas 

-- CREATE TABLE temp_PdM_machines
-- (
-- 	machine_id SMALLINT,
-- 	model CHARACTER(6),
-- 	age SMALLINT
-- );

-- CREATE TABLE temp_PdM_errors
-- (
-- 	datetime TIMESTAMP,
-- 	machine_id SMALLINT,
-- 	error_id CHARACTER(6)
-- );

-- CREATE TABLE temp_PdM_maint
-- (
-- 	datetime TIMESTAMP,
-- 	machine_id SMALLINT,
-- 	comp_id CHARACTER(5)
-- );

-- CREATE TABLE temp_PdM_failures
-- (
-- 	datetime TIMESTAMP,
-- 	machine_id SMALLINT,
-- 	failure_comp_id CHARACTER(5)
-- );

-- CREATE TABLE temp_PdM_telemetry
-- (
-- 	datetime TIMESTAMP,
-- 	machine_id SMALLINT,
-- 	volt double precision,
-- 	rotate double precision,
-- 	pressure double precision,
-- 	vibration double precision
-- );


-- DEMOS AS CARGAS DOS ARQUIVOS CSV DO KAGGLE NAS TABELAS TEMPORÁRIAS
-- INSERIMOS OS DADOS DAS TABELAS TEMPORÁRIAS NAS TABELAS DO NOSSO MODELO

INSERT INTO error_machine(error_type) SELECT DISTINCT error_id FROM temp_PdM_errors;
SELECT * FROM error_machine;

INSERT INTO component(comp_type) SELECT DISTINCT failure_comp_id FROM temp_PdM_failures;
SELECT * FROM component;

INSERT INTO model(model_type) SELECT DISTINCT model FROM temp_PdM_machines;
SELECT * FROM model;

INSERT INTO machine (id, age, model_id)
	SELECT machine_id, age, model.id FROM temp_PdM_machines
	INNER JOIN model ON temp_PdM_machines.model = model.model_type;

INSERT INTO telemetry (datetime, volt, rotate, pressure, vibration, machine_id)
	SELECT datetime, volt, rotate, pressure, vibration, machine.id FROM temp_PdM_telemetry
	INNER JOIN machine ON temp_PdM_telemetry.machine_id = machine.id;

INSERT INTO failure (datetime, comp_id, machine_id)
	SELECT datetime, component.id, machine_id FROM temp_PdM_failures
	INNER JOIN component ON temp_PdM_failures.failure_comp_id = component.comp_type;
	
INSERT INTO register_error (datetime, machine_id, error_id)
	SELECT datetime, machine_id, error_machine.id FROM temp_pdm_errors
	INNER JOIN error_machine ON temp_PdM_errors.error_id = error_machine.error_type;

INSERT INTO maintenance (datetime, comp_id, machine_id)
	SELECT datetime, component.id, machine_id FROM temp_pdm_maint
	INNER JOIN component ON temp_PdM_maint.comp_id = component.comp_type;
	

-- TESTANDO AS CARGAS NAS TABELAS DO NOSSO MODELO

SELECT * FROM machine;
SELECT * FROM register_error;
SELECT * FROM failure;
SELECT * FROM maintenance;
SELECT * FROM telemetry;


-- APAGANDO AS TABELAS TEMPORÁRIAS PÓS-CARGAS

-- DROP TABLE temp_PdM_machines;
-- DROP TABLE temp_PdM_errors;
-- DROP TABLE temp_PdM_maint;
-- DROP TABLE temp_PdM_failures;
-- DROP TABLE temp_PdM_telemetry;


-- CONSULTAS PARA RESPONDER ÀS PERGUNTAS DO PROJETO

-- 1. Qual modelo de máquina apresenta mais falhas?
SELECT model.model_type, COUNT(failure.id) AS num_failures
	FROM machine
	JOIN model ON machine.model_id = model.id
	JOIN failure ON machine.id = failure.machine_id
	GROUP BY machine.model_id, model.model_type
	ORDER BY (num_failures) DESC LIMIT 1;


-- 2. Qual a quantidade de falhas por idade da máquina?
SELECT age AS faixa_idade,
    COUNT(failure.id) AS total_falhas
	FROM machine
	JOIN failure ON machine.id = failure.machine_id
	GROUP BY age
	ORDER BY total_falhas DESC;
	

-- 3. Qual componente apresenta maior quantidade de falhas por máquina?
SELECT component.comp_type, COUNT(failure.id) AS num_failures
	FROM component
	JOIN failure ON component.id = failure.comp_id
	GROUP BY component.comp_type
	ORDER BY num_failures DESC;
	

-- 4. A média da idade das máquinas por modelo?
SELECT model.model_type, AVG(age) 
	FROM machine
	JOIN model ON machine.model_id = model.id
	GROUP BY model_type
	ORDER BY AVG(machine.age) DESC;


-- 5. Quantidade de erro por tipo de erro e modelo da máquina?
SELECT error_machine.error_type, model.model_type, COUNT(register_error.error_id) AS num_errors
    FROM error_machine
    JOIN register_error ON error_machine.id = register_error.error_id
    JOIN machine ON register_error.machine_id = machine.id
    JOIN model ON machine.model_id = model.id
    GROUP BY error_type, model.model_type
    ORDER BY error_type;


END;
