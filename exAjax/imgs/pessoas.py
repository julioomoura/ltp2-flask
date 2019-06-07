from base import sql
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/temp/julio/projFlask/exAjax/imgs/static/imagens'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def menu():
   return render_template('menu.html')


@app.route('/upfoto')
def up_foto():
   return render_template('up_foto.html')


@app.route('/getfoto', methods=['POST'])
def get_foto():
   if request.method == 'POST':
       # check if the post request has the file part
       print (request.files)
       if 'pFoto' not in request.files:
           msg = "Não existem arquivos no formulário"
       else:
           arq = request.files['pFoto']
           if arq.filename == '':
               msg = "Arquivo não selecionado no formulário"
           else:
               if arq and allowed_file(arq.filename):
                   arqname = secure_filename(arq.filename)
                   arq.save(os.path.join(app.config['UPLOAD_FOLDER']))
                   nome = request.form['pNome']
                   endereco = request.form['pEndereco']
                   telefone = request.fomr['pTelefone']
                   dsc = "/static/imagens/" + arqname

                   # Incluindo dados na tabela
                   mysql = sql.SQL("root", "root", "test")
                   comando = "INSERT INTO tb_pessoa(nme_pessoa, end_pessoa, tel_pessoa ,dsc_foto_pessoa) VALUES (%s, %s, %s, %s);"

                   if mysql.executar(comando, [nome, endereco, telefone, dsc]):
                       msg = arqname + " armazenado com sucessso!!!"
                   else:
                       msg = "Falha na inclusão de pessoa."

   return render_template('get_foto.html', msg = msg)

@app.route('/showfoto')
def show_foto():
   # Recuperando todos os identificadores de imagens
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT idt_pessoa FROM tb_pessoa;"
   cs = mysql.consultar(comando, ())
   codigos = ""
   for [idt] in cs:
       codigos = codigos + str(idt) + ","
   codigos = codigos[0:len(codigos)-1]
   cs.close()

   return render_template('show_foto.html', codigos=codigos)

@app.route('/foto', methods=['POST'])
def foto():
   # Pegando o identificador da imagem
   idt = request.form['idt']

   # Recuperando os detalhes textuais da imagem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT dsc_foto_pessoa FROM tb_pessoa WHERE idt_pessoa=%s;"
   cs = mysql.consultar(comando, [idt])
   dados=cs.fetchone()
   foto = "<IMG SRC='" + dados[0] + "' STYLE='width:600px; height:400px'/>"
   cs.close()

   return render_template('foto.html', foto=foto)


@app.route('/getDetail', methods=['POST'])
def get_detail():
   # Pegando o identificador da imagem
   idt = request.form['idt']

   # Recuperando os detalhes textuais da imagem
   mysql = sql.SQL("root", "root", "test")
   comando = "SELECT nme_pessoa, end_pessoa, tel_pessoa FROM tb_pessoa WHERE idt_pessoa=%s;"
   cs = mysql.consultar(comando, [idt])
   dados=cs.fetchone()
   cs.close()

   return render_template('get_detail.html', nome=dados[0], endereco=dados[1], telefone=dados[2])
