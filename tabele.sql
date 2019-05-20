﻿DROP TABLE IF EXISTS igralec CASCADE;
DROP TABLE IF EXISTS prestop CASCADE;
DROP TABLE IF EXISTS klub CASCADE;
DROP TABLE IF EXISTS agent CASCADE;

CREATE TABLE agent (
	id SERIAL PRIMARY KEY,
	ime VARCHAR(50),
	priimek VARCHAR(50)
);


CREATE TABLE klub (
	id SERIAL PRIMARY KEY,
	Ime VARCHAR(50),
	Naslov VARCHAR(50)
);

CREATE TABLE prestop (
	id SERIAL PRIMARY KEY,
	cena INT,
	datum DATE,
	stanje BOOLEAN,
	igralec FOREIGN KEY REFERENCES igralec,
	iz_kluba FOREIGN KEY REFERENCES klub,
	v_klub FOREIGN KEY REFERENCES klub,
	agent FOREIGN KEY REFERENCES agent
);

CREAT TABLE igralci (
	id SERIAL PRIMARY KEY,
	ime VARCHAR(50),
	priimek VARCHAR(50),
	država VARCHAR(50),
	plača INT,
	vrednost INT,
	klub REFERENCES FOREIGN KEY klub,
	agent REFERENCES FOREIGN KEY agent
);
/*Omogočim povezavo sodelavcem*/

GRANT CONNECT ON DATABASE sem2019_matijagh TO matevzr WITH GRANT OPTION;
GRANT CONNECT ON DATABASE sem2019_matijagh TO oskark WITH GRANT OPTION;
GRANT CONNECT ON DATABASE sem2019_matijagh TO matijagh WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO matevzr WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO oskark WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO matijagh WITH GRANT OPTION;

/*Grant za sodelavce*/

GRANT ALL ON ALL TABLES IN SCHEMA public TO matevzr WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO oskark WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO matijagh WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO matevzr WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO oskark WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO matijagh WITH GRANT OPTION;

/*Grant za javnost*/

GRANT CONNECT ON DATABASE sem2019_matijagh TO javnost;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
