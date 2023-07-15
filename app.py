from flask import Flask, render_template, request, session
import mysql.connector
import base64
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Conexão com o banco de dados MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="paguemais"
)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    salt = bcrypt.gensalt()
    usuario = request.args.get('usuario')
    session['username'] = usuario
    senha = request.args.get('senha')
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)

    consulta = "SELECT usuario, senha FROM funcionario WHERE usuario = %s"
    valores = (usuario, )
    cursor = mydb.cursor()
    cursor.execute(consulta, valores)
    resultado = cursor.fetchall()
    dados = []

    for linha in resultado:
        dicionario = {"usuario": linha[0],
                      "senha": linha[1]}
        dados.append(dicionario)

    # cursor.close()
    # mydb.close()
    if len(dados) == 0:
        mensagem = 'Usuário não encontrado'
        return render_template('login.html', mensagem=mensagem)
    else:
        usuario_armazenado = dados[0]['usuario']
        senha_armazenada = dados[0]['senha'].encode('utf-8')
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada) and usuario_armazenado == usuario:
            print("Senha correta!")
            return render_template('home.html', usuario=usuario)
        else:
            mensagem = 'Usuário ou senha incorretos'
            return render_template('login.html', mensagem=mensagem)


@app.route('/home', methods=['GET', 'POST'])
def home():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)


@app.route('/cancelarcadastrousuario', methods=['GET', 'POST'])
def cancelarcadastrousuario():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)


@app.route('/pagecaduser', methods=['GET', 'POST'])
def pagecaduser():
    return render_template('cadastrarusuario.html')


@app.route('/pagecadproduct', methods=['GET', 'POST'])
def pagecadproduct():
    return render_template('cadastrarproduto.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('Login.html')


@app.route('/trocasenha', methods=['GET', 'POST'])
def trocasenha():
    return render_template('trocasenha.html')


@app.route('/changepassword', methods=['GET', 'POST'])
def atualizasenha():
    salt = bcrypt.gensalt()
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    novasenha = request.args.get('novasenha')
    hashed_password = bcrypt.hashpw(novasenha.encode('utf-8'), salt)

    consulta = "SELECT senha FROM funcionario WHERE usuario = %s"

    valores = (usuario, )
    cursor = mydb.cursor()
    cursor.execute(consulta, valores)
    resultado = cursor.fetchall()

    dados = []

    for linha in resultado:
        dicionario = {"senha": linha[0]}
        dados.append(dicionario)

    # cursor.close()

    # mydb.close()

    senha_armazenada = dados[0]['senha'].encode('utf-8')
    if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):

        mycursor = mydb.cursor()

        sql = "UPDATE funcionario SET senha = %s where usuario = %s"
        valores = (hashed_password, usuario)
        mycursor.execute(sql, valores)
        mydb.commit()

        nome = session.get('username')
        return render_template('home.html', usuario=nome)
    else:
        mensagem = 'Senha atual incorreta'
        return render_template('trocasenha.html', mensagem=mensagem)


@app.route('/cancelatrocasenha', methods=['GET', 'POST'])
def cancelatrocasenha():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)


@app.route('/consultausuarios')
def consultausuarios():
    consulta = "SELECT * FROM funcionario where usuario <> 'master'"

    cursor = mydb.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    # cursor.close()

    # mydb.close()
    return render_template('consultausuarios.html', dados=resultado)


@app.route('/consultaprodutos')
def consultaprodutos():

    consulta = "SELECT * FROM produtos"

    cursor = mydb.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    # cursor.close()

    # mydb.close()
    return render_template('consultaprodutos.html', dados=resultado)

@app.route('/buscaproduto')
def buscaproduto():

    produto = "%" + request.args.get('produto') + "%"
    consulta = "SELECT id, descricao, setor, preco, codigodebarras FROM produtos WHERE descricao LIKE %s"
 
    valores = (produto, )
    cursor = mydb.cursor()
    cursor.execute(consulta, valores)
    resultado = cursor.fetchall()


    return render_template('consultaprodutos.html', produto=resultado)


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def cadastrarusuario():
    if request.method == 'POST':
        salt = bcrypt.gensalt()
        usuario = request.form['usuario']
        senha = request.form['senha']
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)

        cursor = mydb.cursor()

        sql = "INSERT INTO funcionario (usuario, senha) VALUES (%s, %s)"

        valores = (usuario, hashed_password)

        cursor.execute(sql, valores)

        mydb.commit()
        # mydb.close()
        return render_template('home.html', usuario='master')
    else:
        return render_template('home.html', usuario='master')


@app.route('/cadastrarproduto', methods=['POST'])
def cadastrarproduto():
    # Recebimento dos dados da requisição POST
    descricao = request.form.get('descricao')
    setor = request.form.get('setor')
    preco = float(request.form.get('preco'))
    codigo_barras = request.form.get('codigo_barras')
    imagem = request.files.get('imagem')
    # id_usuario = request.form.get('id_usuario')

    # # Verificar se o id_usuario está presente e não é uma string vazia ou o número inteiro zero
    # if not id_usuario or str(id_usuario).strip() == "0":
    #     return "Usuário não está logado. Faça o login antes de cadastrar um produto."

    # Validação dos campos obrigatórios
    if not (descricao and setor and preco and codigo_barras and imagem):
        mensagem = "Todos os campos são obrigatórios."
        return render_template('cadastrarproduto.html', mensagem=mensagem)

    # # Verificar a extensão do arquivo
    if not allowed_file(imagem.filename):
        mensagem = "Formato de imagem não suportado. Envie apenas JPG, JPEG ou PNG."
        return render_template('cadastrarproduto.html', mensagem=mensagem)

    # Ler e codificar a imagem em base64
    imagem_data = imagem.read()
    imagem_base64 = base64.b64encode(imagem_data).decode('utf-8')

    # Inserção dos dados na tabela "produtos"
    mycursor = mydb.cursor()
    sql = "INSERT INTO produtos (descricao, setor, preco, codigo_barras, imagem) VALUES (%s, %s, %s, %s, %s)"
    val = (descricao, setor, preco, codigo_barras, imagem_base64)
    mycursor.execute(sql, val)
    mydb.commit()

    # Retorno das mensagens personalizadas
    # return "Dados inseridos com sucesso!"
    nome = session.get('username')
    return render_template('home.html', usuario=nome)


@app.route('/exportar', methods=['GET'])
def exportar_dados():
    # Consulta os dados do banco de dados
    mycursor = mydb.cursor()
    sql = "SELECT * FROM produtos"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    # Cria uma pasta para armazenar os arquivos de exportação
    export_folder = 'export'
    os.makedirs(export_folder, exist_ok=True)

    for result in results:
        # Obtém os dados do resultado
        codigo = result[0]
        descricao = result[1]
        setor = result[2]
        preco = result[3]
        codigo_barras = result[4]
        imagem_base64 = result[5]

        # Decodifica a imagem base64
        imagem_data = base64.b64decode(imagem_base64)

        # Cria uma pasta com o nome do código
        codigo_pasta = f'{export_folder}/{codigo}'
        os.makedirs(codigo_pasta, exist_ok=True)

        # Cria um arquivo de texto com as informações
        txt_filename = f'{codigo_pasta}/{codigo_barras}.txt'
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(f'Código: {codigo_barras}\n')
            txt_file.write(f'Descrição: {descricao}\n')
            txt_file.write(f'Setor: {setor}\n')
            txt_file.write(f'Preço: {preco}\n')

        # Cria um arquivo de imagem
        img_filename = f'{codigo_pasta}/{codigo_barras}.jpg'
        with open(img_filename, 'wb') as img_file:
            img_file.write(imagem_data)

    return "Dados exportados com sucesso!"


def allowed_file(filename):
    # Verificar se a extensão do arquivo está entre as permitidas
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
