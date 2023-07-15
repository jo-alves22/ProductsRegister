import requests

url = 'http://localhost:5000/login'
myobj = {
    "usuario": "master",
    "senha": "fatec"
}

try:
    response = requests.get(url, data=myobj)
    response.raise_for_status()  # Lança uma exceção se ocorrer um erro de requisição
    print(response.text)  # Exibe a resposta do serviço
except requests.exceptions.RequestException as e:
    print("Erro na requisição:", e)
