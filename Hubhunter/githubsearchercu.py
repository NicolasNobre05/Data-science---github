import customtkinter
import webbrowser
from Hubhunter import consultardados
import re
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Função para obter os estados e suas siglas da API do IBGE
def get_estados_ibge():
    try:
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        response = requests.get(url)
        response.raise_for_status()
        estados = response.json()
        return {estado['nome']: estado['sigla'] for estado in estados}
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do IBGE: {e}")
        return {}

# Obter dicionário de estados e siglas
estados_ibge = get_estados_ibge()

def is_url(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.match(text) is not None

def load_image_from_url(image_url, size=(60, 60), border_color="#144673", border_width=2):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image = image.resize(size, Image.LANCZOS)
    border_image = Image.new("RGB", (size[0] + 2 * border_width, size[1] + 2 * border_width), border_color)
    border_image.paste(image, (border_width, border_width))
    return ImageTk.PhotoImage(border_image)

def on_consultar(contpag=1):
    global resultados_frame

    nome = nome_entry.get()
    linguagem = linguagem_entry.get()
    localidade = localidade_entry.get()

    # Substituir localidade pelo código do estado do IBGE, se estiver na lista
    localidade = estados_ibge.get(localidade, localidade)

    resultados = consultardados(nome, linguagem, localidade, contpag)
    
    for widget in resultados_frame.winfo_children():
        widget.destroy()

    if resultados is not None and resultados:
        for resultado in resultados:
            url, image_url = resultado.split(", ")

            frame = customtkinter.CTkFrame(master=resultados_frame, fg_color="#D9D9D9")
            frame.pack(fill="x", pady=5)

            try:
                image = load_image_from_url(image_url)
                image_label = customtkinter.CTkLabel(master=frame, image=image, text="")
                image_label.image = image 
                image_label.pack(side="left", padx=10)
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")

            text_label = customtkinter.CTkLabel(master=frame, text=url, fg_color="#D9D9D9", text_color="blue", cursor="hand2")
            text_label.pack(side="left", padx=10)
            text_label.bind("<Button-1>", lambda e, url=url: abrir_url(url))
        
        next_page_button.place(relx=1.0, rely=1.0, x=-100, y=-10, anchor='se')
    else:
        no_results_label = customtkinter.CTkLabel(master=resultados_frame, text="Nenhum resultado encontrado.", fg_color="#D9D9D9")
        no_results_label.pack()
        next_page_button.place_forget()

    canvas.yview_moveto(0)

def abrir_url(url):
    webbrowser.open_new_tab(url)

def on_next_page():
    global current_page
    current_page += 1
    on_consultar(current_page)
    canvas.yview_moveto(0)

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def criar_janela():
    global nome_entry, linguagem_entry, localidade_entry, resultados_frame, next_page_button, current_page, canvas

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

    nome_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Nome completo", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    nome_entry.grid(row=0, column=0, ipady=10, sticky="n", pady=(24,0))

    linguagem_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Linguagem de programação", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    linguagem_entry.grid(row=1, column=0, ipady=10, sticky="n", pady=(24,0))

    localidade_entry = customtkinter.CTkEntry(master=grid_entradas, placeholder_text="Localidade", placeholder_text_color="#0D1E40", fg_color="transparent", border_color="#0D1E40", border_width=2, width=400, corner_radius=10, text_color="#000000")
    localidade_entry.grid(row=0, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    consulta = customtkinter.CTkButton(master=grid_entradas, text="consultar", text_color="#D9D9D9", width=400, fg_color="#0D1E40", font=("Arial Bold", 17), hover_color="#144673", border_width=2, corner_radius=10, command=lambda: on_consultar(1))
    consulta.grid(row=1, column=1, ipady=10, sticky="n", pady=(24,0), padx=(24,0))

    canvas = customtkinter.CTkCanvas(frame_principal)
    canvas.config(width=1400, height=800, bg="#D9D9D9")

    background_rect = canvas.create_rectangle(0, 0, 1400, 700, fill="#D9D9D9" ,outline="")
    canvas.tag_lower(background_rect)

    scrollbar = customtkinter.CTkScrollbar(frame_principal, orientation="vertical", command=canvas.yview)
    resultados_frame = customtkinter.CTkFrame(canvas, fg_color="#D9D9D9", bg_color="#D9D9D9", border_color="blue")

    resultados_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=resultados_frame, anchor="nw", width=1400, height=800)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    next_page_button = customtkinter.CTkButton(master=frame_principal, text="Próxima Página", text_color="#D9D9D9", width=200, fg_color="#0D1E40", font=("Arial Bold", 17), hover_color="#144673", border_width=2, corner_radius=10, command=on_next_page)
    next_page_button.place_forget()

    current_page = 1

    janela.mainloop()

if __name__ == "__main__":
    criar_janela()
