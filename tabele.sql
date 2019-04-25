DROP TABLE IF EXISTS Igralec CASCADE;
DROP TABLE IF EXISTS Prestop CASCADE;
DROP TABLE IF EXISTS Klub CASCADE;
DROP TABLE IF EXISTS Agent CASCADE;
DROP TABLE IF EXISTS SPORTNI_DIREKTOR CASCADE;

CREATE TABLE AGENT (
	id INT,
	Ime VARCHAR(50),
	Priimek VARCHAR(50)
);

CREATE TABLE SPORTNI_DIREKTOR (
	id INT,
	Ime VARCHAR(50),
	Priimek VARCHAR(50)
);

CREATE TABLE KLUB (
	id INT,
	Ime VARCHAR(50),
	Naslov VARCHAR(50)
);


GRANT ALL ON ALL TABLES IN SCHEMA public TO MatijaGH;
GRANT ALL ON ALL TABLES IN SCHEMA public TO oskarkregar;
GRANT ALL ON ALL TABLES IN SCHEMA public TO matevzraspet;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO MatijaGH;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO matevzraspet;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO oskarkregar;


/*Grant za javnost*/
GRANT CONNECT ON DATABASE sem2019_
GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO javnost;