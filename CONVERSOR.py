import customtkinter

# --- Configurações da Janela Principal ---
janela = customtkinter.CTk()
janela.title("Conversor De Unidades")
janela.geometry("500x600")

# Variáveis Globais (Iniciantes usam muito isso)
cor_fundo_atual = "#E0E7FF" # Começa com azul claro
janela.configure(fg_color=cor_fundo_atual)

categoria_atual = "Comprimento"

# --- Funções do Programa ---

# Função clunky (mas que funciona) para mudar a cor aos poucos
def mudar_cor_suave(cor_destino, passo=0):
    global cor_fundo_atual
    
    # Cores fixas em RGB só para não ter que fazer cálculos complexos na hora
    cores_rgb = {
        "#E0E7FF": (224, 231, 255), # Azul
        "#DCFCE7": (220, 252, 231), # Verde
        "#FFEDD5": (255, 237, 213)  # Laranja
    }
    
    if passo <= 10:
        # Pega o RGB da cor atual e da cor que a gente quer chegar
        r1, g1, b1 = cores_rgb[cor_fundo_atual]
        r2, g2, b2 = cores_rgb[cor_destino]
        
        # Faz uma continha básica para achar o meio termo
        r = int(r1 + (r2 - r1) * (passo / 10))
        g = int(g1 + (g2 - g1) * (passo / 10))
        b = int(b1 + (b2 - b1) * (passo / 10))
        
        # Transforma de volta para Hexadecimal (Aquele código com #)
        nova_cor = f"#{r:02x}{g:02x}{b:02x}"
        janela.configure(fg_color=nova_cor)
        
        # Chama a função de novo depois de 20 milissegundos
        janela.after(20, mudar_cor_suave, cor_destino, passo + 1)
    else:
        # Quando terminar, atualiza a variável global
        cor_fundo_atual = cor_destino

# Funções para os botões de categoria
def clica_comprimento():
    global categoria_atual
    categoria_atual = "Comprimento"
    mudar_cor_suave("#E0E7FF") # Azul
    
    # Atualiza as opções das caixinhas
    opcoes = ["Metro", "Centimetro", "Quilometro"]
    caixa_de.configure(values=opcoes)
    caixa_para.configure(values=opcoes)
    caixa_de.set("Metro")
    caixa_para.set("Centimetro")
    
    # Limpa as caixas de texto
    entrada_valor.delete(0, 'end')
    entrada_resultado.delete(0, 'end')
