DROP TABLE IF EXISTS clientes; 
CREATE TABLE  clientes( 
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre varchar(50) NOT NULL, 
    email varchar(50) NOT NULL); 
 
INSERT INTO clientes(nombre,email) VALUES("Brandon","patolucas.bbl@gmail.com"); 
INSERT INTO clientes(nombre,email) VALUES("Erick","Erickbabytaz@gmail.com"); 
INSERT INTO clientes(nombre,email) VALUES("Toño","TonyBalde@gmail.com"); 
 
.headers ON 
 
SELECT *FROM clientes;