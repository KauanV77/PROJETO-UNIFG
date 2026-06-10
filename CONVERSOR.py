import customtkinter as ctk

# CONFIGURAÇÕES DA APARÊNCIA
ctk.set_appearance_mode("light")

# CONFIGURAÇÕES DA JANELA
janela = ctk.CTk()
janela.title("CONVERSOR DE UNIDADES")
janela.geometry("700x700")

# OPÇÕES DO FRAME
frame_opcoes = ctk.CTkFrame(
    janela,
    width=600,
    height=600,
    corner_radius=20
)

# CENTRALIZAR O FRAME
frame_opcoes.place(relx=0.5, rely=0.5, anchor="center")

#TEXTO DENTRO DO FRAME 

label = ctk.CTkLabel(
    frame_opcoes,
    text="CONVERSOR DE UNIDADES",
    font=("Arial", 24, "bold")
)
label.pack()

label.place(relx= 0.5, rely=0.1, anchor="center")

janela.mainloop()