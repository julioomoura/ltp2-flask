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
   # Recuperando modelos existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_tipo ORDER BY nme_tipo;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='tipo' id='idt'>"
   sel += "<OPTION VALUE='0'>Todos</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('consultar.html', tipos=sel)

@app.route('/softwares', methods=['POST'])
def softwares():
   # Pegando os dados de parâmetro vindos por ajax de consultar
   idtTipo = request.form['tipo']

   # Recuperando softwares que satisfazem ao parâmetro de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT nme_software, ver_software FROM tb_software WHERE cod_tipo = %s OR 0 = %s;"

   cs = mysql.consultar(comando, [idtTipo, idtTipo])
   softs = "<TABLE><TR><TH>Software</TH><TH>Versão</TH></TR>"
   for [nome, versao] in cs:
       softs += "<TR>"
       softs += "<TD>" + nome + "</TD>"
       softs += "<TD>" + versao + "</TD>"
       softs += "</TR>"
   cs.close()
   softs += "</TABLE>"

   return render_template('ajax.html', AJAX=softs)