import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

# Função para obter os estados e suas siglas da API do IBGE
def get_estados():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response = requests.get(url)
    if response.status_code == 200:
        estados = response.json()
        return {estado['nome']: estado['sigla'] for estado in estados}
    else:
        print("Erro ao acessar a API do IBGE:", response.status_code)
        return {}

# Obter dicionário de estados e siglas
estados = get_estados()

def consultardados(nome, linguagem, localidade, contpag):
    resultados = []
    
    # Substituição de espaços por '+'
    nome = nome.replace(" ", "+")
    
    # Substituição de estado por sigla
    localidade = estados.get(localidade, localidade.replace(" ", "+"))

    # Substituição de linguagens especiais
    linguagem_map = {"C++": "C%2B%2B", "C#": "C%23"}
    if linguagem in linguagem_map:
        linguagem = linguagem_map[linguagem]
    else:
        linguagem = quote(linguagem)  # Codifica linguagem para URL

    # Função para construir a URL e obter dados
    def entrarsite(localidade, linguagem, nome, contpag):
        link = f"https://github.com/search?q=location%3A{localidade}+language%3A{linguagem}+fullname%3A{nome}&type=users&p={contpag}"
        try:
            res = requests.get(link)
            res.raise_for_status()
            dados = BeautifulSoup(res.text, 'html.parser').get_text()
            return dados, link
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o site: {e}")
            return "", link

    dados, link = entrarsite(localidade, linguagem, nome, contpag)

    # Extração de avatares e logins
    if dados:
        avatar = re.findall(r'"avatar_url":"(.*?)"', dados)
        logins = re.findall(r'"display_login":"(.*?)"', dados)
        for login, avatar_url in zip(logins, avatar):
            resultados.append(f"https://github.com/{login}, {avatar_url}")

    return resultados
