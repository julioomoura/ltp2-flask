from base import sql

mysql = sql.SQL("root", "root", "test")

comando = "DROP TABLE IF EXISTS tb_pais;"

if mysql.executar(comando, ()):
   print ("Tabela de país excluída com sucesso!")

comando = "DROP TABLE IF EXISTS tb_estado;"

if mysql.executar(comando, ()):
   print ("Tabela de estado excluída com sucesso!")

comando = "CREATE TABLE tb_pais (idt_pais INT AUTO_INCREMENT PRIMARY KEY, " + \
         "nme_pais VARCHAR(50) NOT NULL);"

if mysql.executar(comando, ()):
   print ("Tabela de pais criada com sucesso!")


comando = "CREATE TABLE tb_estado (idt_estado INT AUTO_INCREMENT PRIMARY KEY, " + \
         "nme_estado VARCHAR(50) NOT NULL, " + \
         "populacao_estado INT NOT NULL, " + \
         "cod_pais INT NOT NULL, " + \
         "CONSTRAINT fk_pais_estado FOREIGN KEY (cod_pais) REFERENCES tb_pais(idt_pais));"

if mysql.executar(comando, ()):
   print ("Tabela de estado criada com sucesso!")


comando = "INSERT INTO tb_pais(nme_pais) VALUES " + \
         "('Brasil'), ('Estados Unidos'), ('Alemanha');"

if mysql.executar(comando, ()):
   print ("Países cadastrados com sucesso!")

comando = "INSERT INTO tb_estado(nme_estado, populacao_estado, cod_pais) VALUES " + \
         "('Goiás', 6551322, 1), ('Piauí', 3198185, 1), ('Amapá', 756500, 1), ('Espírito Santo', 3894899, 1), ('Santa Catarina', 6734568, 1), ('Texas', 25674681, 2), ('California', 37691912, 2), ('Baviera', 7914000, 3), ('Hesse', 6066000, 3), ('Brandemburgo', 25000000, 3);"

if mysql.executar(comando, ()):
   print("Estados cadastrados com sucesso!")
