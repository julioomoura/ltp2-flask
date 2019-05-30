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

@app.route('/combos')
def combos():
   # Recuperando Estados existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_pais ORDER BY nme_pais;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='pasis' id='idtPais' onclick='execPaises()'>"
   sel += "<OPTION VALUE='0'>Escolha um País</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('combos.html', paises=sel)


@app.route('/estado', methods = ['POST'])
def soft():
   # Recuperando Estados existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_estado, nme_estado FROM tb_estado WHERE cod_pais=%s ORDER BY nme_estado;"
   idtPais = request.form['pais']
   cs = mysql.consultar(comando, [idtPais])
   sel = "<SELECT NAME='estado' id='idtEstado' onclick='execEstados()'>"
   sel += "<OPTION VALUE='0'>Escolha um Estado</OPTION>"
   for [idt, nome] in cs:
       sel += "<OPTION VALUE='" + str(idt) + "'>" + nome + "</OPTION>"
   sel += "</SELECT>"
   cs.close()
   return render_template('AJAX.html', AJAX=sel)


@app.route('/ver', methods = ['POST'])
def ver():
   # Recuperando Estados existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT populacao_estado FROM tb_estado WHERE idt_estado=%s;"
   idtEstado = request.form['estado']
   cs = mysql.consultar(comando, [idtEstado])
   dados = cs.fetchone()
   sel = dados[0]
   cs.close()
   return render_template('AJAX.html', AJAX=sel)

@app.route('/org')
def org():
   # Recuperando Estados existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_pais ORDER BY nme_pais;"

   cs = mysql.consultar(comando, ())
   comandoSoft = "SELECT nme_estado, populacao_estado FROM tb_estado WHERE cod_pais=%s ORDER BY nme_estado;"

   arv=""
   for [idt, nome] in cs:
       arv += ", [{v:'pais_" + str(idt) + "', f:'" + nome + "'}, 'paises', 'País: " + nome + "']"
       mysqlSoft = sql.SQL("root", "root", "test")
       csSoft = mysqlSoft.consultar(comandoSoft, [idt])
       for [estado, populacao] in csSoft:
           arv += ", ['" + estado + "', 'pais_" + str(idt) + "', '" + estado + " - " + str(populacao) + "']"
       csSoft.close()
   cs.close()

   return render_template('org.html', arvore=arv)


@app.route('/pizza')
def pizza():
   # Recuperando Estados existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT nme_pais, COUNT(idt_estado) AS qtd FROM tb_pais JOIN tb_estado ON idt_pais=cod_pais GROUP BY nme_pais;"

   cs = mysql.consultar(comando, ())

   grf = ""
   i = 0
   for [nome, qtd] in cs:
       grf += "['" + nome + "', " + str(qtd) + "],"
       i += 1
   cs.close()
   grf = grf[:-1]

   return render_template('pizza.html', pizza=grf)