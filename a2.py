import customtkinter as ctk

# Configurações globais de aparência
ctk.set_appearance_mode("Light") 

class FigmaUnitConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal
        self.title("Conversor de Unidades - Cores Dinâmicas")
        self.geometry("900x750")
        
        # Cores Únicas por Categoria
        self.cores_categorias = {
            "Comprimento": "#3B82F6",   # Azul
            "Peso": "#22C55E",          # Verde
            "Temperatura": "#EF4444",   # Vermelho
            "Volume": "#06B6D4",        # Ciano
            "Área": "#A855F7"           # Roxo
        }
        
        self.current_bg = self.cores_categorias["Comprimento"]

        # --- A SOLUÇÃO AQUI: Frame de Fundo para forçar a cor no Windows ---
        self.bg_frame = ctk.CTkFrame(self, fg_color=self.current_bg, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Dados de Unidades
        self.dados_unidades = {
            "Comprimento": {
                "Quilômetro (km)": 1000, "Metro (m)": 1, "Centímetro (cm)": 0.01, 
                "Milímetro (mm)": 0.001, "Milha (mi)": 1609.34, "Pé (ft)": 0.3048, "Polegada (in)": 0.0254
            },
            "Peso": {
                "Tonelada (t)": 1000, "Quilograma (kg)": 1, "Grama (g)": 0.001, 
                "Miligrama (mg)": 0.000001, "Libra (lb)": 0.453592, "Onça (oz)": 0.0283495
            },
            "Temperatura": {
                "Celsius (°C)": "C", "Fahrenheit (°F)": "F", "Kelvin (K)": "K"
            },
            "Volume": {
                "Metro cúbico (m³)": 1000, "Litro (l)": 1, "Mililitro (ml)": 0.001, 
                "Galão (gal)": 3.78541, "Quarto (qt)": 0.946353, "Pinta (pt)": 0.473176
            },
            "Área": {
                "Quilômetro quadrado (km²)": 1000000, "Hectare (ha)": 10000, "Metro quadrado (m²)": 1, 
                "Centímetro quadrado (cm²)": 0.0001, "Milha quadrada (mi²)": 2589988.11, "Acre (ac)": 4046.86
            }
        }

        # Variáveis de Estado
        self.categoria_ativa = ctk.StringVar(value="Comprimento")
        self.unidade_de_var = ctk.StringVar()
        self.unidade_para_var = ctk.StringVar()
        self.valor_entrada_var = ctk.StringVar(value="1")
        self.valor_saida_var = ctk.StringVar()

        # Construir a UI dentro do bg_frame
        self.criar_ui()
        self.clicar_categoria("Comprimento") 
        
        # Rastrear mudanças para conversão em tempo real
        self.valor_entrada_var.trace_add("write", lambda *args: self.converter())
        self.unidade_de_var.trace_add("write", lambda *args: self.converter())
        self.unidade_para_var.trace_add("write", lambda *args: self.converter())

    def criar_ui(self):
        # Todos os elementos agora são filhos de self.bg_frame, não de self
        self.label_titulo = ctk.CTkLabel(self.bg_frame, text="Conversor de Unidades", font=("Inter Medium", 36), text_color="#FFFFFF")
        self.label_titulo.pack(pady=(40, 10))
        
        self.label_subtitulo = ctk.CTkLabel(self.bg_frame, text="Converta facilmente entre diferentes unidades de medida", font=("Inter", 16), text_color="#E5E7EB")
        self.label_subtitulo.pack(pady=(0, 30))

        # Card Principal Branco
        self.card = ctk.CTkFrame(self.bg_frame, fg_color="#FFFFFF", corner_radius=20)
        self.card.pack(padx=60, pady=(0, 40), fill="both", expand=True)
        self.card.grid_columnconfigure(0, weight=1)

        # Label Categoria
        self.frame_categoria_label = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_categoria_label.grid(row=0, column=0, pady=(25, 15), padx=30, sticky="ew")
        self.label_categoria = ctk.CTkLabel(self.frame_categoria_label, text="Categoria", font=("Inter", 14), text_color="#6B7280")
        self.label_categoria.pack(anchor="w")

        # Botões de Categoria
        self.frame_botoes = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_botoes.grid(row=1, column=0, padx=30, sticky="ew")
        self.frame_botoes.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="group1")

        self.botoes_info = [
            ("Comprimento", "📏"), ("Peso", "⚖️"), ("Temperatura", "🌡️"), ("Volume", "💧"), ("Área", "⏹️")
        ]
        self.botoes_widgets = []

        for i, (nome, icone) in enumerate(self.botoes_info):
            btn = ctk.CTkButton(
                self.frame_botoes,
                text=f"{icone}\n{nome}",
                font=("Inter", 12),
                compound="top",
                corner_radius=10,
                border_width=1,
                width=120,
                height=90,
                command=lambda n=nome: self.clicar_categoria(n)
            )
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            self.botoes_widgets.append((nome, btn))

        # Seção "De"
        self.frame_de_label = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_de_label.grid(row=2, column=0, pady=(20, 5), padx=30, sticky="ew")
        self.label_de = ctk.CTkLabel(self.frame_de_label, text="De", font=("Inter", 14), text_color="#6B7280")
        self.label_de.pack(anchor="w")

        self.frame_de_input = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_de_input.grid(row=3, column=0, padx=30, sticky="ew")
        self.frame_de_input.grid_columnconfigure(0, weight=3)
        self.frame_de_input.grid_columnconfigure(1, weight=1)

        self.entry_de = ctk.CTkEntry(self.frame_de_input, textvariable=self.valor_entrada_var, font=("Inter", 18), fg_color="#FFFFFF", border_color="#E5E7EB", border_width=1, corner_radius=10, height=55)
        self.entry_de.grid(row=0, column=0, padx=(0, 15), sticky="ew")

        self.combo_de = ctk.CTkOptionMenu(self.frame_de_input, variable=self.unidade_de_var, values=[], font=("Inter", 12), fg_color="#FFFFFF", button_color="#FFFFFF", button_hover_color="#F3F4F6", text_color="#111827", corner_radius=10, height=55)
        self.combo_de.grid(row=0, column=1, sticky="ew")

        # Botão Swap
        self.frame_swap = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_swap.grid(row=4, column=0, pady=15)
        
        self.btn_swap = ctk.CTkButton(self.frame_swap, text="⇆", font=("Inter", 24), width=46, height=46, corner_radius=23, fg_color="#3B82F6", hover_color="#2563EB", command=self.trocar_unidades)
        self.btn_swap.pack()

        # Seção "Para"
        self.frame_para_label = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_para_label.grid(row=5, column=0, pady=(0, 5), padx=30, sticky="ew")
        self.label_para = ctk.CTkLabel(self.frame_para_label, text="Para", font=("Inter", 14), text_color="#6B7280")
        self.label_para.pack(anchor="w")

        self.frame_para_input = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_para_input.grid(row=6, column=0, padx=30, pady=(0, 25), sticky="ew")
        self.frame_para_input.grid_columnconfigure(0, weight=3)
        self.frame_para_input.grid_columnconfigure(1, weight=1)

        self.entry_para = ctk.CTkEntry(self.frame_para_input, textvariable=self.valor_saida_var, font=("Inter", 18), fg_color="#FFFFFF", text_color="#6B7280", border_color="#E5E7EB", border_width=1, corner_radius=10, height=55, state="readonly")
        self.entry_para.grid(row=0, column=0, padx=(0, 15), sticky="ew")

        self.combo_para = ctk.CTkOptionMenu(self.frame_para_input, variable=self.unidade_para_var, values=[], font=("Inter", 12), fg_color="#FFFFFF", button_color="#FFFFFF", button_hover_color="#F3F4F6", text_color="#111827", corner_radius=10, height=55)
        self.combo_para.grid(row=0, column=1, sticky="ew")

    # --- Lógica de Transição de Cores ---
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"

    def animate_bg_transition(self, start_hex, end_hex, steps=20, delay=25, current_step=0):
        if current_step > steps:
            # Aplica a cor no Frame de fundo
            self.bg_frame.configure(fg_color=end_hex)
            return

        start_rgb = self.hex_to_rgb(start_hex)
        end_rgb = self.hex_to_rgb(end_hex)

        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (current_step / steps)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (current_step / steps)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (current_step / steps)
        
        new_color = self.rgb_to_hex((r, g, b))
        
        # AQUI É A MÁGICA: Mudar a cor do bg_frame, não do root
        self.bg_frame.configure(fg_color=new_color)
        
        self.after(delay, self.animate_bg_transition, start_hex, end_hex, steps, delay, current_step + 1)

    def clicar_categoria(self, nome_categoria):
        self.categoria_ativa.set(nome_categoria)
        target_color = self.cores_categorias[nome_categoria]
        
        # Dispara a animação
        self.animate_bg_transition(self.current_bg, target_color, steps=20, delay=25)
        self.current_bg = target_color

        # Atualiza o Botão Swap
        self.btn_swap.configure(fg_color=target_color, hover_color=target_color)
        
        # Atualiza as bordas e cores dos botões de categoria
        for nome, btn in self.botoes_widgets:
            if nome == nome_categoria:
                btn.configure(fg_color=target_color, text_color="#FFFFFF", border_color=target_color, hover_color=target_color)
            else:
                btn.configure(fg_color="#FFFFFF", text_color="#111827", border_color="#E5E7EB", hover_color="#F3F4F6")

        # Atualiza comboboxes
        unidades = list(self.dados_unidades[nome_categoria].keys())
        self.combo_de.configure(values=unidades)
        self.combo_para.configure(values=unidades)
        
        if unidades:
            self.unidade_de_var.set(unidades[0])
            self.unidade_para_var.set(unidades[1] if len(unidades) > 1 else unidades[0])
        
        self.converter()

    def trocar_unidades(self):
        de = self.unidade_de_var.get()
        para = self.unidade_para_var.get()
        self.unidade_de_var.set(para)
        self.unidade_para_var.set(de)

    def converter(self):
        try:
            valor_entrada_str = self.valor_entrada_var.get()
            if not valor_entrada_str:
                self.valor_saida_var.set("Resultado")
                return
            
            valor_entrada = float(valor_entrada_str)
            categoria = self.categoria_ativa.get()
            u_de = self.unidade_de_var.get()
            u_para = self.unidade_para_var.get()
            
            if categoria != "Temperatura":
                ratios = self.dados_unidades[categoria]
                valor_base = valor_entrada * ratios[u_de]
                valor_final = valor_base / ratios[u_para]
                
                if valor_final.is_integer():
                    self.valor_saida_var.set(f"{int(valor_final):,}".replace(",", "."))
                else:
                    self.valor_saida_var.set(f"{valor_final:,.6f}".replace(",", "."))
            else:
                simbolos = self.dados_unidades[categoria]
                de_sym = simbolos[u_de]
                para_sym = simbolos[u_para]
                
                if de_sym == para_sym: valor_final = valor_entrada
                elif de_sym == "C" and para_sym == "F": valor_final = (valor_entrada * 9/5) + 32
                elif de_sym == "C" and para_sym == "K": valor_final = valor_entrada + 273.15
                elif de_sym == "F" and para_sym == "C": valor_final = (valor_entrada - 32) * 5/9
                elif de_sym == "F" and para_sym == "K": valor_final = (valor_entrada - 32) * 5/9 + 273.15
                elif de_sym == "K" and para_sym == "C": valor_final = valor_entrada - 273.15
                elif de_sym == "K" and para_sym == "F": valor_final = (valor_entrada - 273.15) * 9/5 + 32
                
                if valor_final.is_integer():
                    self.valor_saida_var.set(f"{int(valor_final):,}".replace(",", "."))
                else:
                    self.valor_saida_var.set(f"{valor_final:,.2f}".replace(",", "."))
        except ValueError:
            self.valor_saida_var.set("Erro")

if __name__ == "__main__":
    app = FigmaUnitConverterApp()
    app.mainloop()
    