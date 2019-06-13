import locale

from flask import Flask, render_template, request

from base import sql

app = Flask(__name__)

@app.route('/')
def menu():
   return render_template('menu.html')

@app.route('/formincluir')
def formIncluir():
   return render_template('formIncluir.html')

@app.route('/incluir', methods=['POST'])
def incluir():
   # Recuperando dados do formulário de formIncluir()
   marca = request.form['marca']
   nome = request.form['nome']
   sistema = request.form['sistema']
   preco = float(request.form['preco'])

   # Incluindo dados no SGBD
   mysql = sql.SQL("root", "root", "test")
   comando = "INSERT INTO tb_celular_crud(marca_celular, nome_celular, sistema_operacional, preco_celular) VALUES (%s, %s, %s, %s);"

   if mysql.executar(comando, [marca, nome, sistema, preco]):
       msg="Celular " + nome + " cadastrado com sucesso!"
   else:
       msg="Falha na inclusão de celular."

   return render_template('incluir.html', msg=msg)

@app.route('/parconsultar')
def parConsultar():
   # Recuperando modelos existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT DISTINCT nome_celular FROM tb_celular_crud ORDER BY nome_celular;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='nome'>"
   sel += "<OPTION>Todos</OPTION>"
   for [celular] in cs:
       sel += "<OPTION>" + celular + "</OPTION>"
   sel += "</SELECT>"
   cs.close()

   # Recuperando menor e maior valor de celular
   comando="SELECT MIN(preco_celular) AS menor, MAX(preco_celular) AS maior FROM tb_celular_crud;"
   cs = mysql.consultar(comando, ())
   dados = cs.fetchone()
   menor = dados[0]
   maior = dados[1]

   return render_template('parConsultar.html', celular=sel, menor=menor, maior=maior)


@app.route('/consultar', methods=['POST'])
def consultar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   celular = request.form['nome']
   menor = float(request.form['ini'])
   maior = float(request.form['fim'])

   # Testando se é para considerar todos os nomes
   celular = "" if celular == "Todos" else celular

   # Recuperando nomes que satisfazem aos parâmetros de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_celular_crud WHERE nome_celular LIKE CONCAT('%', %s, '%') AND preco_celular BETWEEN %s AND %s ORDER BY preco_celular;"

   locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

   cs = mysql.consultar(comando, [celular, menor, maior])
   celulares = ""
   for [idt, marca, celular, sistema, preco] in cs:
       celulares += "<TR>"
       celulares += "<TD>" + marca + "</TD>"
       celulares += "<TD>" + celular + "</TD>"
       celulares += "<TD>" + sistema + "</TD>"
       celulares += "<TD>" + locale.currency(preco) + "</TD>"
       celulares += "</TR>"
   cs.close()

   return render_template('consultar.html', celulares=celulares)

@app.route('/paralterar')
def parAlterar():
   return render_template('parAlterar.html')

@app.route('/formalterar', methods=['POST'])
def formAlterar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   nome = request.form['nome']

   # Recuperando modelos que satisfazem aos parâmetros de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_celular_crud WHERE nome_celular=%s;"

   cs = mysql.consultar(comando, [nome])
   dados = cs.fetchone()
   cs.close()

   return render_template('formAlterar.html', idt=dados[0], marca=dados[1], nome=dados[2], sistema=dados[3], preco=dados[4])

@app.route('/alterar', methods=['POST'])
def alterar():
   # Recuperando dados do formulário de formAlterar()
   idt = int(request.form['idt'])
   marca = request.form['marca']
   nome = request.form['nome']
   sistema = request.form['sistema']
   preco = float(request.form['preco'])

   # Alterando dados no SGBD
   mysql = sql.SQL("root", "root", "test")
   comando = "UPDATE tb_celular_crud SET marca_celular=%s, nome_celular=%s, sistema_operacional=%s, preco_celular=%s WHERE idt_celular=%s;"

   if mysql.executar(comando, [marca, nome, sistema, preco, idt]):
       msg="Celular " + marca + " alterado com sucesso!"
   else:
       msg="Falha na alteração de celular."

   return render_template('alterar.html', msg=msg)

@app.route('/parexcluir')
def parExcluir():
   # Recuperando todos os celulares da base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_celular, marca_celular, nome_celular, sistema_operacional, preco_celular FROM tb_celular_crud ORDER BY preco_celular;"

   cs = mysql.consultar(comando, ())
   celulares = ""
   for [idt, marca, nome, sistema, preco] in cs:
       celulares += "<TR>"
       celulares += "<TD>" + marca + " " + nome  + "</TD>"
       celulares += "<TD>" + str(preco) + "</TD>"
       celulares += "<TD><BUTTON ONCLICK=\"jsExcluir('" + marca + " (" + nome + ")" + "', " + str(idt) + ")\">Excluir" + "</BUTTON></TD>"
       celulares += "</TR>"
   cs.close()

   return render_template('parExcluir.html', celulares=celulares)

@app.route('/excluir', methods=['POST'])
def excluir():
   # Recuperando dados do formulário de parExcluir()
   idt = int(request.form['idt'])

   # Alterando dados no SGBD
   mysql = sql.SQL("root", "root", "test")
   comando = "DELETE FROM tb_celular_crud WHERE idt_celular=%s;"

   if mysql.executar(comando, [idt]):
       msg="Celular excluído com sucesso!"
   else:
       msg="Falha na exclusão de celular."

   return render_template('excluir.html', msg=msg)
