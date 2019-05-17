import mysql.connector
import locale
from base import sql
from flask import Flask, render_template, request


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
  sigla = request.form['sigla']
  nome = request.form['nome']
  data = request.form['data']
  creditos = int(request.form['creditos'])
  ementa = request.form['ementa']

  # Incluindo dados no SGBD
  mysql = sql.SQL("root", "root", "test")
  comando = "INSERT INTO tb_curso(sigla_curso, nome_curso, data_abertura, numero_creditos, ementa_curso) VALUES (%s, %s, %s, %s, %s);"

  if mysql.executar(comando, [sigla, nome, data, creditos, ementa]):
      msg="Curso " + nome + " cadastrado com sucesso!"
  else:
      msg="Falha na inclusão de curso."

  return render_template('incluir.html', msg=msg)

@app.route('/parconsultar')
def parConsultar():
   # Recuperando cursos existentes na base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT DISTINCT nome_curso FROM tb_curso ORDER BY nome_curso;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='curso'>"
   sel += "<OPTION>Todos</OPTION>"
   for [curso] in cs:
       sel += "<OPTION>" + curso + "</OPTION>"
   sel += "</SELECT>"
   cs.close()

   # Recuperando menor e maior numero de creditos
   comando="SELECT MIN(numero_creditos) AS menor, MAX(numero_creditos) AS maior FROM tb_curso;"
   cs = mysql.consultar(comando, ())
   dados = cs.fetchone()
   menor = dados[0]
   maior = dados[1]

   return render_template('parConsultar.html', curso=sel, menor=menor, maior=maior)


@app.route('/consultar', methods=['POST'])
def consultar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   curso = request.form['curso']
   menor = float(request.form['ini'])
   maior = float(request.form['fim'])

   # Testando se é para considerar todos os cursos
   curso = "" if curso=="Todos" else curso

   # Recuperando cursos que satisfazem aos parâmetros de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_curso WHERE nome_curso LIKE CONCAT('%', %s, '%') AND numero_creditos BETWEEN %s AND %s ORDER BY numero_creditos;"

   locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

   cs = mysql.consultar(comando, [curso, menor, maior])
   cursos = ""
   for [idt, sigla, nome, data, creditos, ementa] in cs:
       cursos += "<TR>"
       cursos += "<TD>" + nome + "</TD>"
       cursos += "<TD>" + sigla + "</TD>"
       cursos += "<TD>" + str(data) + "</TD>"
       cursos += "<TD>" + str(creditos) + "</TD>"
       cursos += "<TD>" + ementa + "</TD>"
       cursos += "</TR>"
   cs.close()

   return render_template('consultar.html', cursos=cursos)

@app.route('/paralterar')
def parAlterar():
   return render_template('parAlterar.html')

@app.route('/formalterar', methods=['POST'])
def formAlterar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   sigla = request.form['sigla']

   # Recuperando modelos que satisfazem aos parâmetros de filtragem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT * FROM tb_curso WHERE sigla_curso=%s;"

   cs = mysql.consultar(comando, [sigla])
   dados = cs.fetchone()
   cs.close()

   return render_template('formAlterar.html', idt=dados[0], sigla=dados[1], nome=dados[2], data=dados[3], creditos=dados[4], ementa=dados[5])

@app.route('/alterar', methods=['POST'])
def alterar():
   # Recuperando dados do formulário de formAlterar()
   idt = int(request.form['idt'])
   sigla = request.form['sigla']
   nome = request.form['nome']
   data = request.form['data']
   creditos = int(request.form['creditos'])
   ementa = request.form['ementa']

   # Alterando dados no SGBD
   mysql = sql.SQL("root", "root", "test")
   comando = "UPDATE tb_curso SET sigla_curso=%s, nome_curso=%s, data_abertura=%s, numero_creditos=%s, ementa_curso=%s WHERE idt_curso=%s;"

   if mysql.executar(comando, [sigla, nome, data, creditos, ementa, idt]):
       msg="Curso " + sigla + " alterado com sucesso!"
   else:
       msg="Falha na alteração de curso."

   return render_template('alterar.html', msg=msg)

@app.route('/parexcluir')
def parExcluir():
   # Recuperando todos os cursos da base de dados
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_curso, sigla_curso, nome_curso, numero_creditos, ementa_curso FROM tb_curso ORDER BY sigla_curso;"

   cs = mysql.consultar(comando, ())
   cursos = ""
   for [idt, sigla, nome, creditos, ementa] in cs:
       cursos += "<TR>"
       cursos += "<TD>" + sigla + " (" + nome + ")" + "</TD>"
       cursos += "<TD>" + str(creditos) + "</TD>"
       cursos += "<TD><BUTTON ONCLICK=\"jsExcluir('" + sigla + " (" + nome + ")" + "', " + str(idt) + ")\">Excluir" + "</BUTTON></TD>"
       cursos += "</TR>"
   cs.close()

   return render_template('parExcluir.html', cursos=cursos)

@app.route('/excluir', methods=['POST'])
def excluir():
   # Recuperando dados do formulário de parExcluir()
   idt = int(request.form['idt'])

   # Alterando dados no SGBD
   mysql = sql.SQL("root", "root", "test")
   comando = "DELETE FROM tb_curso WHERE idt_curso=%s;"

   if mysql.executar(comando, [idt]):
       msg="Curso excluído com sucesso!"
   else:
       msg="Falha na exclusão de curso."

   return render_template('excluir.html', msg=msg)
