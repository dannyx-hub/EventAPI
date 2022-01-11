CREATE TABLE IF NOT EXISTS events(id SERIAL PRIMARY KEY,eventname TEXT NOT NULL,eventdate TIMESTAMP NOT NULL,eventpersoncreator VARCHAR(60) NOT NULL);
CREATE TABLE IF NOT EXISTS users(id SERIAL NOT NULL PRIMARY KEY,login TEXT NOT NULL,hash TEXT NOT NULL,role VARCHAR(10) NOT NULL);
Insert into events(eventname,eventdate,eventpersoncreator) VALUES('test3','2022-01-01','Damian');
Insert into users(login,hash,role) values('root','63a9f0ea7bb98050796b649e85481845','root');
