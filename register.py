import requests

url = 'http://localhost:5000/cadastrar'
myobj = {
    'descricao': 'produto',
    'setor': 'setor',
    'preco': 10.0,
    'codigo_barras': '123456789',
    'id_usuario': '1'
}

# Ler a imagem em formato binário
with open('produto.jpg', 'rb') as image_file:
    image_data = image_file.read()

# Adicionar a imagem ao objeto de requisição
files = {'imagem': ('imagem.jpg', image_data)}

try:
    response = requests.post(url, data=myobj, files=files)
    response.raise_for_status()  # Lança uma exceção se ocorrer um erro de requisição
    print(response.text)  # Exibe a resposta do serviço
except requests.exceptions.RequestException as e:
    print("Erro na requisição:", e)
