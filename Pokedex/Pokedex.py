import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import random

pokemonimg = []
pokemonname = []
pokemonid = []
pokemonstats = []
pokemontypes = []
hp = []
atk = []
deff = []
spatk = []
spdef = []
speed = []
indices_originais = []
current_index = 0  # Índice inicial para exibir a primeira imagem

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
} 

pageL ="https://pokemondb.net/pokedex/all"
pageTreeL = requests.get(pageL, headers=headers)
pageSoupL = BeautifulSoup(pageTreeL.content, "html.parser")
p = pageSoupL.find_all("td")

for pk in p:
    if "type" in str(pk) and len(str(pk).split("type-icon type-",1)) > 1 and len((str(pk).split("type-icon type-",1)[1])) < 60:
        pokemontypes.append((str(pk).split("type-icon type-",1)[1]).split('" href')[0])
    elif "type" in str(pk) and len(str(pk).split("type-icon type-",1)) > 1 and len((str(pk).split("type-icon type-",1)[1])) > 60:
        pokemontypes.append("{}/{}".format((str(pk).split("type-icon type-",1)[1]).split('" href')[0],str(pk).split("type-icon type-",1)[1].split("type-icon type-",1)[1].split('" href',1)[0]))
    
    if "num" in str(pk):
        pok = str(pk).split('num">',1)
        if len(pok) >= 2:
            pokemonstats.append(pok[1].split("</td>",1)[0])
    if "png" in str(pk):
        pokemonimg.append(str(pk.find("img")).split('src="',1)[1].split('" width',1)[0])
    if "alt" in str(pk):
        pk = str(pk).split('img alt="',1)
        if len(pk) >= 2:
            pokemonname.append(pk[1].split('" class=',1)[0])
    if "value" in str(pk):
        pokemonid.append(str(pk).split('value="',1)[1].split('"><span',1)[0])
for c in range(len(pokemonstats)):
    if c == 0 or c % 6 == 0:
        hp.append(pokemonstats[c])
    if c == 1 or c % 6 == 1:
        atk.append(pokemonstats[c])
    if c == 2 or c % 6 == 2:
        deff.append(pokemonstats[c])
    if c == 3 or c % 6 == 3:
        spatk.append(pokemonstats[c])
    if c == 4 or c % 6 == 4:
        spdef.append(pokemonstats[c])
    if c == 5 or c % 6 == 5:
        speed.append(pokemonstats[c])

def carregar_icone_tipo(tipo):
    try:
        icone_path = f"Pokedex\\images\\{str(tipo).title()} type.png"
        icone = tk.PhotoImage(file=icone_path)
        
        # Redimensionar a imagem para o tamanho desejado (por exemplo, 32x32 pixels)
        icone = icone.subsample(7, 7)  # 2x menor, você pode ajustar conforme necessário
        
        return icone
    except Exception as e:
        print(f"Erro ao carregar ícone para o tipo {str(tipo).title()}")
        return None
    
def desenhar_barras():
    global current_index

    # Limpe o Canvas antes de desenhar novas barras
    canvas_barras.delete("all")

    # Valores de HP, Attack, Defense, Special Attack, Special Defense e Speed
    valores = [int(hp[current_index]), int(atk[current_index]), int(deff[current_index]),
               int(spatk[current_index]), int(spdef[current_index]), int(speed[current_index])]

    nomes_stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

    x1, y1 = 10, 18
    espaco_entre_barras = 30

    for i, valor in enumerate(valores):
        # Calcula a largura da barra proporcional ao valor máximo (255 é o valor máximo para as estatísticas)
        largura_barra = (valor / 255) * 180

        # Desenha o retângulo da barra
        if valor < 30:
            canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='red')
            canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
        elif valor < 60:
            canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='orange')
            canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
        elif valor < 90:
            canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='yellow')
            canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
        elif valor < 120:
            canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='lime')
            canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
        else:
            canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='green')
            canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
                     
        # Atualize as coordenadas para a próxima barra
        y1 += espaco_entre_barras

def buscar_pokemon():
    global current_index
    
    nome_pesquisado = entrada_busca.get().lower()
    
    resultados = []
    indices_originais.clear()
    for index, nome in enumerate(pokemonname):
        if nome_pesquisado in nome.lower():
            resultados.append(index)
            indices_originais.append(index)
    
    if len(resultados) == 0:
        label_busca_resultado.config(text="No results for this search.")
    elif len(resultados) == 1:
        current_index = resultados[0]
        mostrar_imagem_selecionada()
        label_busca_resultado.config(text="")
    else:
        label_busca_resultado.config(text="Multiple Pokémon encountered. Choose one:")
        lista_resultados.delete(0, tk.END)
        for index in resultados:
            lista_resultados.insert(tk.END, "{} {}".format(pokemonid[index], pokemonname[index]))
        lista_resultados.pack(pady=50)
        lista_resultados.bind("<<ListboxSelect>>", atualizar_pokemon_selecionado)

def atualizar_pokemon_selecionado(event):
    global current_index
    selecionado = lista_resultados.curselection()
    if selecionado:
        index_na_lista_original = int(selecionado[0])
        current_index = indices_originais[index_na_lista_original]
        mostrar_imagem_selecionada()
        label_busca_resultado.config(text="")

def mostrar_imagem_selecionada():
    global current_index
    
    try:
        url = pokemonimg[current_index] 
        response = requests.get(url)
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img = ImageTk.PhotoImage(img)
        
        label_imagem.config(image=img)
        label_imagem.image = img
       
        label_id.config(text="{} {}".format(pokemonid[current_index], pokemonname[current_index]))
        label_stats.config(text="Stats Total:{}\n\nHP: {}\n\nAttack: {}\n\nDefense: {}\n\nSp.Attack: {}\n\nSp.Defense: {}\n\nSpeed: {}\n\n".format(int(hp[current_index]) + int(atk[current_index]) + int(deff[current_index]) + int(spatk[current_index]) + int(spdef[current_index]) + int(speed[current_index]),hp[current_index], atk[current_index], deff[current_index], spatk[current_index], spdef[current_index], speed[current_index]))
        desenhar_barras()

        # Limpar labels de tipos anteriores
        for label_tipo in labels_tipos:
            label_tipo.config(image=None)
            label_tipo.image = None

        # Exibir ícones de tipos correspondentes
        tipos = pokemontypes[current_index].split('/')
        for i, tipo in enumerate(tipos):
            icone = carregar_icone_tipo(tipo)
            if icone:
                labels_tipos[i].config(image=icone)
                labels_tipos[i].image = icone
    except Exception as e:
        label_imagem.config(text="Erro ao carregar imagem")

def proxima_imagem():
    global current_index
    if current_index == (len(pokemonimg) - 1):
        current_index = -1
    
    if current_index < len(pokemonimg) - 1:
        current_index += 1
        mostrar_imagem_selecionada()

def imagem_anterior():
    global current_index
    if current_index > 0:
        current_index -= 1
    else:
        current_index = len(pokemonimg) - 1
    mostrar_imagem_selecionada()

def aleatorio():
    global current_index
    current_index = random.randint(0,len(pokemonimg))
    mostrar_imagem_selecionada()
# Criar a janela principal
root = tk.Tk()
root.title("Pokedex")
root.iconbitmap("Pokedex/images/Pokedex.ico")
root.geometry("450x525")

label_busca = tk.Label(root,text="Insert the Pokemon name:")
label_busca.pack()

entrada_busca = tk.Entry(root)
entrada_busca.pack()

botao_busca = tk.Button(root, text="Search", command=buscar_pokemon)
botao_busca.pack()
gerar_aleatorio = tk.Button(root,text="Generate Random Pokemon",command=aleatorio)
gerar_aleatorio.pack()
label_busca_resultado = tk.Label(root, text="")
label_busca_resultado.pack()

label_imagem = tk.Label(root)
label_imagem.pack()

frame_tipos = tk.Frame(root)
frame_tipos.pack()
labels_tipos = [tk.Label(frame_tipos), tk.Label(frame_tipos)]
for label_tipo in labels_tipos:
    label_tipo.pack(side=tk.LEFT)
label_types = tk.Label(root)
label_types.pack()

label_id = tk.Label(root)
label_id.pack()  

botao_anterior = tk.Button(root, text="Previous", command=imagem_anterior)
botao_anterior.pack()
botao_proxima = tk.Button(root, text="Next", command=proxima_imagem)
botao_proxima.pack()

# Crie um Frame para conter label_id e canvas_barras lado a lado
frame_info = tk.Frame(root)
frame_info.pack()


label_stats = tk.Label(frame_info)
label_stats.pack(side=tk.LEFT)

canvas_barras = tk.Canvas(frame_info, width=200, height=200)
canvas_barras.pack(side=tk.LEFT)  

lista_resultados = tk.Listbox(frame_info)
mostrar_imagem_selecionada()
root.mainloop()
