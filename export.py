import requests

url = 'http://localhost:5000/exportar'

try:
    response = requests.get(url)
    response.raise_for_status()  # Lança uma exceção se ocorrer um erro de requisição
    print(response.text)  # Exibe a resposta do serviço
except requests.exceptions.RequestException as e:
    print("Erro na requisição:", e)
