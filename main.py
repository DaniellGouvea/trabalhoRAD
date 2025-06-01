import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from modelo import cad_alunos, disciplinas, cursos, matricula, nota
import connection

# Função chamada ao clicar no botão

def tela_criar_aluno():

    def enviar_dados():
        nome = entry_nome.get()
        email = entry_email.get()

        if nome and email:
            aluno = cad_alunos(nome, email)
            connection.inserir_aluno(aluno.nome, aluno.email)
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    # Janela principal
    root = tk.Tk()
    root.title("Cadastro de Aluno")
    root.geometry("300x200")

    # Rótulo e campo para o nome
    tk.Label(root, text="Nome do aluno:").pack(pady=(10, 0))
    entry_nome = tk.Entry(root, width=30)
    entry_nome.pack()

    # Rótulo e campo para o e-mail
    tk.Label(root, text="Email do aluno:").pack(pady=(10, 0))
    entry_email = tk.Entry(root, width=30)
    entry_email.pack()

    # Botão para enviar os dados
    tk.Button(root, text="Enviar", command=enviar_dados).pack(pady=20)

    # Inicia a aplicação
    root.mainloop()

def ver_alunos():
    # Criação da janela principal
    root = tk.Tk()
    root.title("Exemplo de ComboBox")
    root.geometry("300x150")

    # Lista de opções para o ComboBox
    alunos = [{"id":linha[0], "nome":linha[1]} for linha in connection.listar_alunos()]
    formatted_items = [f"{aluno['id']} - {aluno['nome']}" for aluno in alunos]

    # Criação do Combobox
    combo = ttk.Combobox(root, values=formatted_items, state="readonly")  # state="readonly" impede digitação livre
    combo.current(0)  # Define a opção inicial (índice 0)
    combo.pack(pady=20)

    # Função para exibir a opção selecionada
    def mostrar_opcao():
        opcao_selecionada = combo.get()
        print(f"Você selecionou: {opcao_selecionada}")

    # Botão para pegar a seleção
    botao = tk.Button(root, text="Mostrar Seleção", command=mostrar_opcao)
    botao.pack()

    # Inicia o loop da interface
    root.mainloop()

ver_alunos()