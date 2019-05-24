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

@app.route('/combos')
def combos():
   # Recuperando Tipos de Software existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_tipo ORDER BY nme_tipo;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='tipo' id='idtTipo' onclick='execTipos()'>"
   sel += "<OPTION VALUE='0'>Escolha um Tipo</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('combos.html', tipos=sel)


@app.route('/soft', methods = ['POST'])
def soft():
   # Recuperando Tipos de Software existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_software, nme_software FROM tb_software WHERE cod_tipo=%s ORDER BY nme_software;"
   idtTipo = request.form['tipo']
   cs = mysql.consultar(comando, [idtTipo])
   sel = "<SELECT NAME='soft' id='idtSoft' onclick='execSofts()'>"
   sel += "<OPTION VALUE='0'>Escolha um Software</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('AJAX.html', AJAX=sel)


@app.route('/ver', methods = ['POST'])
def ver():
   # Recuperando Tipos de Software existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT ver_software FROM tb_software WHERE idt_software=%s;"
   idtSoft = request.form['soft']
   cs = mysql.consultar(comando, [idtSoft])
   dados = cs.fetchone()
   sel = dados[0]
   cs.close()
   return render_template('AJAX.html', AJAX=sel)