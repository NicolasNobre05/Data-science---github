import customtkinter  
import webbrowser 
from hubhuntertest2 import consultardados  
import re  
import requests  
from PIL import Image, ImageTk 
from io import BytesIO  

def is_url(text):
    # Função para verificar se o texto é uma URL válida
    url_pattern = re.compile(r'https?://\S+')  # Expressão regular para verificar URLs
    return url_pattern.match(text) is not None  # Retorna True se o texto for uma URL válida, caso contrário False

def load_image_from_url(image_url, size=(60, 60), border_color="#144673", border_width=2):
    # Função para carregar uma imagem a partir de uma URL
    response = requests.get(image_url)  # Faz uma solicitação HTTP para obter o conteúdo da imagem
    image = Image.open(BytesIO(response.content))  # Abre a imagem a partir do conteúdo da resposta
    image = image.resize(size, Image.LANCZOS)  # Redimensiona a imagem para o tamanho desejado

    # Cria uma borda em torno da imagem
    border_image = Image.new("RGB", (size[0] + 2 * border_width, size[1] + 2 * border_width), border_color)
    border_image.paste(image, (border_width, border_width))  # Coloca a imagem dentro da borda

    return ImageTk.PhotoImage(border_image)  # Retorna a imagem como um objeto PhotoImage do Tkinter

def on_consultar(contpag=1):
    # Função chamada ao consultar os dados
    global resultados_frame  # Define a variável global resultados_frame

    # Obtém os valores dos campos de entrada
    nome = nome_entry.get()
    linguagem = linguagem_entry.get()
    localidade = localidade_entry.get()

    # Consulta os dados com base nos valores fornecidos
    resultados = consultardados(nome, linguagem, localidade, contpag)
    
    # Limpa o frame de resultados
    for widget in resultados_frame.winfo_children():
        widget.destroy()

    # Exibe os resultados na interface gráfica
    if resultados is not None:
        for resultado in resultados:
            url, image_url = resultado.split(", ")  # Divide a string de resultado em URL e URL da imagem

            # Cria um frame para cada resultado
            frame = customtkinter.CTkFrame(master=resultados_frame, fg_color="#D9D9D9")
            frame.pack(fill="x", pady=5)

            try:
                image = load_image_from_url(image_url)  # Carrega a imagem da URL
                image_label = customtkinter.CTkLabel(master=frame, image=image, text="")
                image_label.image = image 
                image_label.pack(side="left", padx=10)
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")

            # Adiciona um label com a URL e a torna clicável
            text_label = customtkinter.CTkLabel(master=frame, text=url, fg_color="#D9D9D9", text_color="blue", cursor="hand2")
            text_label.pack(side="left", padx=10)
            text_label.bind("<Button-1>", lambda e, url=url: abrir_url(url))  # Liga a função abrir_url ao clique do mouse
        
        next_page_button.place(relx=1.0, rely=1.0, x=-100, y=-10, anchor='se')  # Posiciona o botão "Próxima Página"
    else:
        no_results_label = customtkinter.CTkLabel(master=resultados_frame, text="Nenhum resultado encontrado.", fg_color="#D9D9D9")
        no_results_label.pack()  # Exibe uma mensagem se nenhum resultado for encontrado

    canvas.yview_moveto(0)  # Move a visualização para o início

def abrir_url(url):
    # Função para abrir a URL em um navegador
    webbrowser.open_new_tab(url)  # Abre a URL em um novo guia do navegador

def on_next_page():
    # Função chamada ao avançar para a próxima página
    global current_page
    current_page += 1
    on_consultar(current_page)  # Chama a função on_consultar com a próxima página
    canvas.yview_moveto(0)  # Move a visualização para o início

def on_mouse_wheel(event):
    # Função chamada ao rolar o mouse
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")  # Rola a visualização para cima ou para baixo conforme o movimento do mouse

def criar_janela():
    # Função para criar a janela da interface gráfica
    global nome_entry, linguagem_entry, localidade_entry, resultados_frame, next_page_button, current_page, canvas

    janela = customtkinter.CTk()  # Cria uma instância da classe CTk
    janela.title("interface")  # Define o título da janela
    janela.geometry("1400x700")  # Define o tamanho da janela

    # Cria uma barra superior com cor personalizada
    top_bar = customtkinter.CTkFrame(master=janela, fg_color="#0D1E40", width=1400, height=140, corner_radius=0)
    top_bar.pack_propagate(0)
    top_bar.pack(fill="x", anchor="n")

    # Cria o frame principal da janela
    frame_principal = customtkinter.CTkFrame(master=janela, fg_color="#D9D9D9", width=1400, height=700, corner_radius=0)
    frame_principal.pack_propagate(0)
    frame_principal.pack(anchor="n")

    # Adiciona uma instrução na janela
    instrucao = customtkinter.CTkLabel(master=frame_principal, text="Digite todas as informações necessárias para localizar o perfil do candidato(a).", font=("Arial Black", 25), text_color="#0D1E40")
    instrucao.pack(anchor="n", padx=20, pady=50)

    # Cria um grid para os campos de entrada e botão de consulta
    grid_entradas = customtkinter.CTkFrame(master=frame_principal, fg_color="transparent")
    grid_entradas.pack(fill="x", padx=250, pady=(50,0), anchor="n")

    # Cria os campos de entrada para nome, linguagem e localidade
    nome_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Nome completo", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    nome_entry.grid(row=0, column=0, ipady=10, sticky="n", pady=(24,0))

    linguagem_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Linguagem de programação", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    linguagem_entry.grid(row=1, column=0, ipady=10, sticky="n", pady=(24,0))

    localidade_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Localidade", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    localidade_entry.grid(row=0, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    # Cria o botão de consulta
    consulta = customtkinter.CTkButton(master=grid_entradas, text="consultar", text_color="#D9D9D9", width=400, fg_color="#0D1E40", font=("Arial Bold", 17), hover_color="#144673", border_width=2, corner_radius=10, command=lambda: on_consultar(1))
    consulta.grid(row=1, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    # Cria um canvas para exibir os resultados
    canvas = customtkinter.CTkCanvas(frame_principal)
    canvas.config(width=1400, height=800, bg="#D9D9D9")  # Define a cor de fundo do canvas

    background_rect = canvas.create_rectangle(0, 0, 1400, 700, fill="#D9D9D9" ,outline="")
    canvas.tag_lower(background_rect)  # Coloca o retângulo atrás de outros itens no canvas

    # Cria uma scrollbar para o canvas
    scrollbar = customtkinter.CTkScrollbar(frame_principal, orientation="vertical", command=canvas.yview)
    resultados_frame = customtkinter.CTkFrame(canvas, fg_color="#D9D9D9", bg_color="#D9D9D9", border_color="blue")

    # Configura a scrollbar para acompanhar o tamanho do frame de resultados
    resultados_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Coloca o frame de resultados dentro do canvas
    canvas.create_window((0, 0), window=resultados_frame, anchor="nw", width=1400, height=800)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Liga a função on_mouse_wheel ao evento de rolar o mouse

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Cria o botão "Próxima Página"
    next_page_button = customtkinter.CTkButton(master=frame_principal, text="Próxima Página", text_color="#D9D9D9", width=200, fg_color="#0D1E40", font=("Arial Bold", 17), hover_color="#144673", border_width=2, corner_radius=10, command=on_next_page)
    next_page_button.place(relx=1.0, rely=1.0, x=-100, y=-10, anchor='se')

    current_page = 1  # Define a página atual como 1

    janela.mainloop()  # Inicia o loop principal da interface gráfica

if __name__ == "__main__":
    criar_janela()
