from base import sql

mysql = sql.SQL("root", "root", "test")

comando = "DROP TABLE IF EXISTS tb_celular;"

if mysql.executar(comando, ()):
   print ("Tabela de celular excluída com sucesso!")


comando = "CREATE TABLE tb_celular (idt_celular INT AUTO_INCREMENT PRIMARY KEY, " + \
         "marca_celular VARCHAR(30) NOT NULL, " + \
         "nome_celular VARCHAR(30) NOT NULL, " + \
         "sistema_operacional VARCHAR(15) NOT NULL, " + \
         "preco_celular DECIMAL(10,2) NOT NULL);"

if mysql.executar(comando, ()):
   print ("Tabela de celular criada com sucesso!")