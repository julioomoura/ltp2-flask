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