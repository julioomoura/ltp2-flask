from base import sql
import os
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:\\trabalho\\UniCEUB\\s_2019_1\ltp2_lp2\\PrjFlask\\galeria\\static\\imagens'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
   return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def menu():
   return render_template('menu.html')


@app.route('/upImgs')
def up_imgs():
   return render_template('up_imgs.html')


@app.route('/getImgs', methods=['POST'])
def get_imgs():
   if request.method == 'POST':
       # check if the post request has the file part
       print (request.files)
       if 'pImagem' not in request.files:
           msg = "Não existem arquivos no formulário"
       else:
           arq = request.files['pImagem']
           if arq.filename == '':
               msg = "Arquivo não selecionado no formulário"
           else:
               if arq and allowed_file(arq.filename):
                   arqname = secure_filename(arq.filename)
                   arq.save(os.path.join(app.config['UPLOAD_FOLDER'], arqname))
                   nome = request.form['pNome']
                   data = request.form['pData']
                   dsc = "/static/imagens/" + arqname

                   # Incluindo dados na tabela
                   mysql = sql.SQL("root", "root", "test")
                   comando = "INSERT INTO tb_imagem(nme_autor_imagem, dta_imagem, dsc_path_imagem) VALUES (%s, %s, %s);"

                   if mysql.executar(comando, [nome, data, dsc]):
                       msg = arqname + " armazenado com sucessso!!!"
                   else:
                       msg = "Falha na inclusão de imagem."

   return render_template('get_imgs.html', msg = msg)
