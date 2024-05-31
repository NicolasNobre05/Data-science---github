import requests
from bs4 import BeautifulSoup
import re
import time


contpag = 1
def consultardados(nome, linguagem, localidade):
    resultados = []
    contpag = 0
    if " " in nome:             #Se nome tiver espaço
        nome = nome.replace(" ","+") #Substituir por +

    if " " in localidade:       #Se localidade tiver espaço
        localidade = localidade.replace(" ","+")  #Substituir por +

    if "C++" in linguagem:      #Se linguagem tiver C++
        linguagem = linguagem.replace("C++","C%2B%2B")  #Substituir por C%2B%2B 

    if " " in linguagem:     #Se linguagem tiver espaço
        linguagens = linguagem.split(" ") #Quebrar a string depois do espaço
        for lang in linguagens: 
            linguagem = "+".join(f"language%3A{lang}") #unir as strings quebradas com a estrutura da url


    def entrarsite(localidade, linguagem, nome, contpag): #função de construir a url, entrar no site, interpretar as informações 
        link = f"https://github.com/search?q=location%3A{localidade}+language%3A{linguagem}+fullname%3A{nome}&type=users&p={contpag}"
        time.sleep(1) 
        res = requests.get(link)   #fazer requisição
        if res.status_code == 200: #Verifica se a conexão foi bem sucedida.
            dados = BeautifulSoup(res.text, 'html.parser') #Organizar e ler HTML
            dados = dados.get_text()  #Remover a parte HTML
            pagina = re.findall(r'"page_count":(\d+)', dados)   #Encontrar o padrão page_count 
            pagina = int(pagina[0]) #Transforma a var de string para int
        else:
            print("Falha ao acessar o site:", res.status_code)
            pagina, dados, link = entrarsite(localidade, linguagem, nome, contpag)
        return pagina, dados, link #Retornar os dados

    pagina, dados, link = entrarsite(localidade, linguagem, nome, contpag) #definir as variáveis 
    print("Total de páginas:", pagina) 
    for contpag in range(1, pagina + 1):
        pagina, dados, link = entrarsite(localidade, linguagem, nome, contpag)
        print(link)
        logins = re.findall(r'"display_login":"(.*?)"', dados)
        for cont in logins:
            resultados.append(f"https://github.com/{cont}")
            
    return resultados
