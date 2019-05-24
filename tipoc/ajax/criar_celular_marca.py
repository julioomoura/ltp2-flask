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
         "('Apple'), ('Samsung'), ('Xiaomi');"

if mysql.executar(comando, ()):
   print ("Marcas cadastradas com sucesso!")

comando = "INSERT INTO tb_celular(nome_celular, preco_celular, cod_marca) VALUES " + \
         "('iPhone 7 Plus', 2599, 1), ('iPhone 6S', 2099, 1), ('iPhone X', 4399, 1), ('iPhone XR', 3899, 1), ('iPhone XS', 5699, 1), ('S10', 4499, 2), ('A10', 899, 2), ('Mi 9', 2399, 3), ('Redmi 6A', 599, 3), ('Mi 8', 1299, 3);"

if mysql.executar(comando, ()):
   print("Celulares cadastrados com sucesso!")