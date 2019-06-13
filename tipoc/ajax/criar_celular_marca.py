from base import sql

mysql = sql.SQL("root", "root", "test")

comando = "DROP TABLE IF EXISTS tb_celular;"

if mysql.executar(comando, ()):
   print ("Tabela de celular excluída com sucesso!")

comando = "DROP TABLE IF EXISTS tb_marca;"

if mysql.executar(comando, ()):
   print ("Tabela de marca excluída com sucesso!")

comando = "CREATE TABLE tb_marca (idt_marca INT AUTO_INCREMENT PRIMARY KEY, " + \
         "nme_marca VARCHAR(50) NOT NULL);"

if mysql.executar(comando, ()):
   print ("Tabela de marca criada com sucesso!")


comando = "CREATE TABLE tb_celular (idt_celular INT AUTO_INCREMENT PRIMARY KEY, nome_celular VARCHAR(50) NOT NULL, preco_celular INT NOT NULL, cod_marca INT NOT NULL, CONSTRAINT fk_marca_celular FOREIGN KEY (cod_marca) REFERENCES tb_marca(idt_marca));"

if mysql.executar(comando, ()):
   print ("Tabela de celular criada com sucesso!")


comando = "INSERT INTO tb_marca(nme_marca) VALUES " + \
         "('Apple'), ('Samsung'), ('Xiaomi'), ('Motorola'), ('Huawei'), ('LG');"

if mysql.executar(comando, ()):
   print ("Marcas cadastradas com sucesso!")

comando = "INSERT INTO tb_celular(nome_celular, preco_celular, cod_marca) VALUES " + \
         "('iPhone 7 Plus', 2599, 1), ('iPhone 6S', 2099, 1), ('iPhone X', 4399, 1), ('iPhone XR', 3899, 1), ('iPhone XS', 5699, 1), ('iPhone 5S', 1699, 1), ('iPhone 4S', 1059, 1), ('iPhone 8', 3099, 1), ('iPhone 8 Plus', 3199, 1), ('S10', 4499, 2), ('A10', 899, 2), ('Mi 9', 2399, 3), ('Redmi 6A', 599, 3), ('Mi 8', 1299, 3), ('Moto G4', 899, 4), ('Moto G4 Plus', 959, 4), ('Moto G5 Plus', 999, 4), ('Moto G6', 1059, 4), ('Moto G6 Plus', 1099, 4), ('Moto G7', 1159, 4), ('Y5', 649, 5), ('Honor 8X', 1149, 5), ('P20 Lite', 1559, 5), ('P30 Lite', 1699, 5), ('P30', 3269, 5), ('K10', 799, 6), ('K11 Plus', 600, 6), ('K12 Plus', 850, 6), ('Q6', 750, 6), ('Q7 Plus', 1150, 6);"

if mysql.executar(comando, ()):
   print("Celulares cadastrados com sucesso!")

comando = "DROP TABLE IF EXISTS tb_marca_empresa;"

if mysql.executar(comando, ()):
   print ("Tabela de celular excluída com sucesso!")

comando = "CREATE TABLE tb_marca_empresa (idt_empresa INT AUTO_INCREMENT PRIMARY KEY, nme_empresa VARCHAR(50) NOT NULL, lat_empresa DECIMAL(6,4) NOT NULL, long_empresa DECIMAL(7,4) NOT NULL);"

if mysql.executar(comando, ()):
   print ("Tabela de marca excluída com sucesso!")

comando = "INSERT INTO tb_marca_empresa(nme_empresa, lat_empresa, long_empresa) VALUES ('Apple', 37.3348544, -122.0112817), ('Samsung', 37.4926392, 127.025337), ('Xiaomi', 23.1267929, 113.2801879), ('Motorola', 23.114468, 113.3148367), ('Huawei', 31.215829, 121.5278043), ('LG', 37.565315, 126.8256347);"
