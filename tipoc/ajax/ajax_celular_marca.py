import mysql.connector
import locale
from base import sql
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def menu():
   return render_template('menu.html')

@app.route('/consultar')
def consultar():
   # Recuperando marcas existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_marca ORDER BY nme_marca;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='marca' id='idt'>"
   sel += "<OPTION VALUE='0'>Todos</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('consultar.html', marcas=sel)

@app.route('/celulares', methods=['POST'])
def softwares():
   # Pegando os dados de parâmetro vindos por ajax de consultar
   idtMarca = request.form['marca']

   # Recuperando celulares que satisfazem ao parâmetro de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT nome_celular, preco_celular FROM tb_celular WHERE cod_marca = %s OR 0 = %s;"

   cs = mysql.consultar(comando, [idtMarca, idtMarca])
   celulares = "<TABLE><TR><TH>Nome</TH><TH>Preço</TH></TR>"
   for [nome, preco] in cs:
       celulares += "<TR>"
       celulares += "<TD>" + nome + "</TD>"
       celulares += "<TD>" + str(preco) + "</TD>"
       celulares += "</TR>"
   cs.close()
   celulares += "</TABLE>"

   return render_template('ajax.html', AJAX=celulares)

@app.route('/combos')
def combos():
   # Recuperando Celulares existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_marca ORDER BY nme_marca;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='marca' id='idtMarca' onclick='execMarcas()'>"
   sel += "<OPTION VALUE='0'>Escolha uma Marca</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('combos.html', marcas=sel)


@app.route('/celular', methods = ['POST'])
def celular():
   # Recuperando celulares existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_celular, nome_celular FROM tb_celular WHERE cod_marca=%s ORDER BY nome_celular;"
   idtMarca = request.form['marca']
   cs = mysql.consultar(comando, [idtMarca])
   sel = "<SELECT NAME='celular' id='idtCelular' onclick='execCelulares()'>"
   sel += "<OPTION VALUE='0'>Escolha um Celular</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('AJAX.html', AJAX=sel)


@app.route('/ver', methods = ['POST'])
def ver():
   # Recuperando celulares existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT preco_celular FROM tb_celular WHERE idt_celular=%s;"
   idtCelular = request.form['celular']
   cs = mysql.consultar(comando, [idtCelular])
   dados = cs.fetchone()
   sel = dados[0]
   cs.close()
   return render_template('AJAX.html', AJAX=sel)

@app.route('/org')
def org():
   # Recuperando Celulares existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_marca ORDER BY nme_marca;"

   cs = mysql.consultar(comando, ())
   comandoCelular = "SELECT nome_celular, preco_celular FROM tb_celular WHERE cod_marca=%s ORDER BY nome_celular;"

   arv=""
   for [idt, nome] in cs:
       arv += ", [{v:'marca_" + str(idt) + "', f:'" + nome + "'}, 'marcas', 'Marca: " + nome + "']"
       mysqlCelular = sql.SQL("root", "root", "test")
       csCelular = mysqlCelular.consultar(comandoCelular, [idt])
       for [celular, preco] in csCelular:
           arv += ", ['" + celular + "', 'marca_" + str(idt) + "', '" + celular + " R$ " + str(preco) + "']"
       csCelular.close()
   cs.close()

   return render_template('org.html', arvore=arv)