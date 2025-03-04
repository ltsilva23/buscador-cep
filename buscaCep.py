from tkinter import *
from tkinter import messagebox
import requests

# Criando a interface gráfica
janela = Tk()
janela.title("Buscando Endereço")
janela.geometry("800x550")
janela.resizable(False, False)  # Impede maximização
janela.configure(bg="#f0f0f0")  # Fundo claro


# Estilo do texto
fonte_titulo = ("Arial", 25, "bold")
fonte_texto = ("Arial", 16)

# Container para os campos de entrada (CEP e Número)
frame_inputs = Frame(janela, bg="#f0f0f0")
frame_inputs.pack(pady=10)

# Label e campo para CEP
Label(frame_inputs, text="CEP:", font=fonte_texto, bg="#f0f0f0").grid(row=0, column=0, padx=5)
campoDigitavelCEP = Entry(frame_inputs, font=fonte_texto, width=10, justify="center")
campoDigitavelCEP.grid(row=0, column=1, padx=5)

# Label e campo para Número (opcional)
Label(frame_inputs, text="Número (Opcional):", font=fonte_texto, bg="#f0f0f0").grid(row=0, column=2, padx=5)
campoNumero = Entry(frame_inputs, font=fonte_texto, width=5, justify="center")
campoNumero.grid(row=0, column=3, padx=5)

# Label para exibir o resultado
resultado_label = Label(janela, text="", font=fonte_texto, fg="black", bg="#f0f0f0", justify="left")
resultado_label.pack(pady=20)

# Função para buscar o CEP usando API ViaCEP
def pesquisaCEP():
    cep = campoDigitavelCEP.get().strip()
    numero = campoNumero.get().strip()

    if not cep.isnumeric() or len(cep) != 8:
        messagebox.showerror("Erro", "Digite um CEP válido com 8 dígitos.")
        return

    if numero and not numero.isnumeric():
        messagebox.showerror("Erro", "Digite um número válido ou deixe em branco.")
        return

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        if "erro" in dados:
            resultado_label.config(text="❌ Endereço não encontrado.", fg="red")
        else:
            endereco = f"📍 {dados['logradouro']}"
            if numero:
                endereco += f", Nº {numero}"
            endereco += f"\n🏘 {dados['bairro']}\n🌆 {dados['localidade']} - {dados['uf']}"
            resultado_label.config(text=endereco, fg="blue")
    else:
        resultado_label.config(text="Erro ao buscar o CEP.", fg="red")

# Botão de pesquisa estilizado
botaoPesquisar = Button(janela, text="🔍 Pesquisar", font=fonte_texto, bg="#007BFF", fg="white",
                        activebackground="#0056b3", activeforeground="white", padx=20, pady=5,
                        command=pesquisaCEP)
botaoPesquisar.pack(pady=10)

janela.mainloop()
