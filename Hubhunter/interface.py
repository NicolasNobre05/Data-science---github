import customtkinter
import webbrowser
from hubhunter import consultardados
import re

def is_url(text):
    # Verifica se o texto corresponde a um padrão de URL
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.match(text) is not None

def on_consultar():
    # Recupera os dados dos campos de entrada
    nome = nome_entry.get()
    linguagem = linguagem_entry.get()
    localidade = localidade_entry.get()

    # Chama a função de processamento com os dados
    resultados = consultardados(nome, linguagem, localidade)

    # Limpa o conteúdo anterior da caixa de texto de resultados
    resultados_textbox.delete("1.0", "end")

    if resultados is not None:
        # Adiciona os novos resultados na caixa de texto
        for resultado in resultados:
            # Verifica se o texto é uma URL antes de adicionar a tag de link
            if is_url(resultado):
                resultados_textbox.insert("end", resultado + "\n", "link")
            else:
                resultados_textbox.insert("end", resultado + "\n")
    else:
        resultados_textbox.insert("end", "Nenhum resultado encontrado.\n")

def abrir_url(url):
    # Abre a URL no navegador padrão
    webbrowser.open_new_tab(url)

def criar_janela():
    janela = customtkinter.CTk()
    janela.title("interface")
    janela.geometry("1400x700")

    top_bar = customtkinter.CTkFrame(master=janela, fg_color="#0D1E40", width=1400, height=140, corner_radius=0)
    top_bar.pack_propagate(0)
    top_bar.pack(fill="x", anchor="n")

    frame_principal = customtkinter.CTkFrame(master=janela, fg_color="#D9D9D9", width=1400, height=700, corner_radius=0)
    frame_principal.pack_propagate(0)
    frame_principal.pack(anchor="n")

    instrucao = customtkinter.CTkLabel(master=frame_principal, text="Digite todas as informações necessárias para localizar o perfil do candidato(a).", font=("Arial Black", 25), text_color="#0D1E40")
    instrucao.pack(anchor="n", padx=20, pady=50)

    grid_entradas = customtkinter.CTkFrame(master=frame_principal, fg_color="transparent")
    grid_entradas.pack(fill="x", padx=250, pady=(50,0), anchor="n")

    global nome_entry
    nome_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Nome completo", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    nome_entry.grid(row=0, column=0, ipady=10, sticky="n", pady=(24,0))

    global linguagem_entry
    linguagem_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Linguagem de programação", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    linguagem_entry.grid(row=1, column=0, ipady=10, sticky="n", pady=(24,0))

    global localidade_entry
    localidade_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Localidade", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    localidade_entry.grid(row=0, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    consulta = customtkinter.CTkButton(master=grid_entradas, text="consultar", text_color="#D9D9D9", width=400, fg_color="#0D1E40", font=("Arial Bold", 17), hover_color="#144673", border_width=2, corner_radius=10, command=on_consultar)
    consulta.grid(row=1, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    # Adiciona uma caixa de texto para exibir os resultados
    global resultados_textbox
    resultados_textbox = customtkinter.CTkTextbox(master=frame_principal, width=1000, height=300, corner_radius=10, fg_color="#D9D9D9", text_color="#000000")
    resultados_textbox.pack(pady=20)

    # Adiciona uma tag de link clicável à caixa de texto
    resultados_textbox.tag_config("link", foreground="blue", underline=True)

    # Liga o evento de clique à função abrir_url apenas para o texto que é uma URL
    resultados_textbox.tag_bind("link", "<Button-1>", lambda event: abrir_url(event.widget.get("current linestart", "current lineend")))

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
