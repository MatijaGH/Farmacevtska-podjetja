DROP TABLE IF EXISTS igralci CASCADE;
DROP TABLE IF EXISTS prestop CASCADE;
DROP TABLE IF EXISTS klub CASCADE;
DROP TABLE IF EXISTS agent CASCADE;
DROP TABLE IF EXISTS uporabnik CASCADE;

CREATE TABLE agent (
	    id SERIAL PRIMARY KEY,
	    ime VARCHAR(50),
	    priimek VARCHAR(50),
	    FOREIGN KEY (id) REFERENCES uporabnik(id)
        );


CREATE TABLE klub (
	    id SERIAL PRIMARY KEY,
	    Ime VARCHAR(50),
	    Naslov VARCHAR(50),
	    FOREIGN KEY (id) REFERENCES uporabnik(id)
        );

CREATE TABLE igralci (
	        id SERIAL PRIMARY KEY,
	        ime VARCHAR(50),
	        priimek VARCHAR(50),
	        država VARCHAR(50),
	        plača INT,
	        datum_rojstva VARCHAR(50),
	        vrednost INT,
	        klub INT,
	        agent INT,
	        FOREIGN KEY (klub) REFERENCES klub (id),
	        FOREIGN KEY (agent) REFERENCES agent (id),
	        FOREIGN KEY (id) REFERENCES uporabnik (id)
        );

CREATE TABLE prestop (
	        id SERIAL PRIMARY KEY,
	        cena INT,
		placa INT,
	        datum DATE,
	        igralec SERIAL,
	        iz_kluba SERIAL,
	        v_klub SERIAL,
	        agent SERIAL,
		stanje_agent INT,
		stanje_klub INT,
		stanje_igralec INT,
		renegotiable BOOLEAN,
	        FOREIGN KEY (igralec) REFERENCES igralci (id),
	        FOREIGN KEY (iz_kluba) REFERENCES klub (id),
	        FOREIGN KEY (v_klub) REFERENCES klub (id),
	        FOREIGN KEY (agent) REFERENCES agent(id)
        );

CREATE TABLE uporabnik (
	            id SERIAL PRIMARY KEY,
	            uporabnisko_ime VARCHAR(50),
	            geslo VARCHAR(50),
	            vloga VARCHAR(50)
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
