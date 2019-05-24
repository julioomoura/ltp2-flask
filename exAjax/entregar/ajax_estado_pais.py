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
   # Recuperando países existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_pais ORDER BY nme_pais;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='pais' id='idt'>"
   sel += "<OPTION VALUE='0'>Todos</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('consultar.html', paises=sel)

@app.route('/estados', methods=['POST'])
def softwares():
   # Pegando os dados de parâmetro vindos por ajax de consultar
   idtPais = request.form['pais']

   # Recuperando estados que satisfazem ao parâmetro de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT nme_estado, populacao_estado FROM tb_estado WHERE cod_pais = %s OR 0 = %s;"

   cs = mysql.consultar(comando, [idtPais, idtPais])
   estados = "<TABLE><TR><TH>Estado</TH><TH>População</TH></TR>"
   for [nome, populacao] in cs:
       estados += "<TR>"
       estados += "<TD>" + nome + "</TD>"
       estados += "<TD>" + str(populacao) + "</TD>"
       estados += "</TR>"
   cs.close()
   estados += "</TABLE>"

   return render_template('ajax.html', AJAX=estados)