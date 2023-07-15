# Projeto SOA

## Como rodar o projeto?

* Instale as dependências. (pip install mysql-connector-python, bcrypt, flask)
* Abra o terminal e rode o arquivo server.py (python server.py)
* Acesse http://127.0.0.1:5000

No arquivo server.py estão configuradas as rotas para funcionamento da página de login, que acessa o banco de dados para verificação do usuário, senha, além da possibilidade de inclusão de novos usuários e alteração de senhas.
Implementei um frontend em html onde as paginas ficam na pasta /templates e o css na pasta /static/css.

Na tela home ja existe um menu simples feito com bootstrap com as opções e funcionalidades do usuário e produto. A opção de consulta aos produtos cadastrados no banco de dados já esta implementada no frontend, mas ainda precisa de melhoria na tela.
