import tkinter as tk
from tkinter import messagebox, ttk
import modelo
import connection
from datetime import date



hoje = date.today()



def tela_adicionar_aluno(callback_atualizar_alunos):

    root = tk.Tk()
    root.title("Cadastro de Aluno")

    #Tamanho janela
    largura_janela = 300
    altura_janela = 200

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    #Inserção de informações
    label_nome = tk.Label(root, text="Nome do aluno:")
    label_nome.pack(pady=(10, 0))

    entry_nome = tk.Entry(root, width=30)
    entry_nome.pack()

    label_email = tk.Label(root, text="Email do aluno:")
    label_email.pack(pady=(10, 0))

    entry_email = tk.Entry(root, width=30)
    entry_email.pack()

    def salvar_dados():
        nome = entry_nome.get()
        email = entry_email.get()

        if nome and email:
            aluno = modelo.cad_alunos(nome, email)
            connection.inserir_aluno(aluno.nome, aluno.email)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!", parent=root)
            callback_atualizar_alunos()
            entry_nome.delete(0, tk.END)
            entry_email.delete(0, tk.END)


        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=root)

    btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados)
    btn_salvar.pack(pady=20)

    root.mainloop()

def tela_adicionar_curso(callback_atualizar_cursos):
    root = tk.Tk()
    root.title("Cadastro de Curso")
    
    #Tamanho janela
    largura_janela = 300
    altura_janela = 130

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    #Inserção de informações
    label_nome = tk.Label(root, text="Nome do curso:")
    label_nome.pack(pady=(10, 0))

    entry_curso = tk.Entry(root, width=30)
    entry_curso.pack()

    def salvar_dados():
        curso = entry_curso.get()

        if curso:
            mod_curso = modelo.cursos(curso)
            connection.inserir_cursos(mod_curso.nomecurso)
            messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!", parent=root)
            callback_atualizar_cursos()
            entry_curso.delete(0, tk.END)

        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=root)

    btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados)
    btn_salvar.pack(pady=20)

    root.mainloop()

def tela_adicionar_disciplina(callback_atualizar_disciplinas):
    cursos = [{"nomecurso": linha[1]} for linha in connection.listar_cursos()]
    cursos_formatados = [curso["nomecurso"] for curso in cursos]

    root = tk.Toplevel()  
    root.title("Cadastro de Disciplina")

    largura_janela = 300
    altura_janela = 170
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_disc = tk.Label(root, text="Nome da Disciplina:")
    label_disc.pack(pady=(10, 0))

    entry_disc = tk.Entry(root, width=30)
    entry_disc.pack()

    label_curso = tk.Label(root, text="Nome do Curso:")
    label_curso.pack(pady=(10, 0))

    cb_curso = ttk.Combobox(root, values=cursos_formatados, width=27, state="readonly")
    cb_curso.pack()

    def salvar_dados():
        disciplina_nome = entry_disc.get()
        curso = cb_curso.get()
        if curso and disciplina_nome:
            mod_disc = modelo.disciplinas(disciplina_nome, curso)
            connection.inserir_disciplina(mod_disc.nome_disciplina, mod_disc.nome_curso)
            messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!", parent=root)
            callback_atualizar_disciplinas()
            entry_disc.delete(0, tk.END)
            cb_curso.set('')

        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=root)

    btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados)
    btn_salvar.pack(pady=20)

    root.mainloop()

def tela_adicionar_matricula():

    alunos = [{"nome":linha[1]} for linha in connection.listar_alunos()]
    alunos_formatados = [f"{aluno['nome']}" for aluno in alunos]

    cursos = [{"nomecurso": linha[1]} for linha in connection.listar_cursos()]
    cursos_formatados = [curso["nomecurso"] for curso in cursos]

    root = tk.Toplevel()  
    root.title("Cadastro de Matricula")

    largura_janela = 300
    altura_janela = 170
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_disc = tk.Label(root, text="Nome do aluno:")
    label_disc.pack(pady=(10, 0))

    cb_aluno = ttk.Combobox(root, values=alunos_formatados, width=27, state="readonly")
    cb_aluno.pack()

    label_curso = tk.Label(root, text="Nome do Curso:")
    label_curso.pack(pady=(10, 0))

    cb_curso = ttk.Combobox(root, values=cursos_formatados, width=27, state="readonly")
    cb_curso.pack()

    dia = hoje.strftime("%Y-%m-%d")

    def salvar_dados():
        aluno = cb_aluno.get()
        curso = cb_curso.get()
        if curso and aluno:
            mod_matricula = modelo.matricula(aluno, curso, dia)
            connection.inserir_matricula(mod_matricula.nome_aluno, mod_matricula.nome_curso, mod_matricula.data_matricula)
            messagebox.showinfo("Sucesso", "Matricula cadastrada com sucesso!", parent=root)
            cb_curso.set('')
            cb_aluno.set('')

        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=root)

    btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados)
    btn_salvar.pack(pady=20)

    root.mainloop()

def tela_deletar_aluno(callback_atualizar_combobox):
    alunos_raw = connection.listar_alunos()  # Exemplo: [(1, "João"), (2, "Maria")]
    alunos_dict = {linha[1]: linha[0] for linha in alunos_raw}  # {"João": 1, "Maria": 2}
    alunos_formatados = list(alunos_dict.keys())

    root = tk.Toplevel()  
    root.title("Deletar Aluno")

    largura_janela = 300
    altura_janela = 170
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_nome = tk.Label(root, text="Nome do aluno:")
    label_nome.pack(pady=20)

    # Frame centralizado para os widgets
    frame_center = tk.Frame(root)
    frame_center.pack(expand=True)

    cb_aluno = ttk.Combobox(frame_center, values=alunos_formatados, width=27, state="readonly")
    cb_aluno.pack(pady=(10, 10))

    def deletar_aluno():
        nome_selecionado = cb_aluno.get()
        if nome_selecionado:
            id_aluno = alunos_dict.get(nome_selecionado)
            if id_aluno:
                connection.deletar_aluno(id_aluno)
                connection.deletar_matricula_por_aluno(id_aluno)
                callback_atualizar_combobox()
                messagebox.showinfo("Sucesso", f"Aluno '{nome_selecionado}' deletado com sucesso!", parent=root)
                root.destroy()
            else:
                messagebox.showerror("Erro", "ID do aluno não encontrado.", parent=root)
        else:
            messagebox.showwarning("Aviso", "Selecione um aluno para deletar.", parent=root)

    btn_salvar = tk.Button(frame_center, text="Deletar", command=deletar_aluno)
    btn_salvar.pack(pady=(5, 10))

    root.mainloop()

def tela_deletar_curso(callback_atualizar_combobox):
    cursos_raw = connection.listar_cursos()  
    cursos_dict = {linha[1]: linha[0] for linha in cursos_raw}
    cursos_formatados = list(cursos_dict.keys())

    root = tk.Toplevel()  
    root.title("Deletar Curso")

    largura_janela = 300
    altura_janela = 170
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_nome = tk.Label(root, text="Nome do curso:")
    label_nome.pack(pady=(20, 10))

    # Frame centralizado para os widgets
    frame_center = tk.Frame(root)
    frame_center.pack(expand=True)

    cb_curso = ttk.Combobox(frame_center, values=cursos_formatados, width=27, state="readonly")
    cb_curso.pack(pady=(10, 10))

    def deletar_curso():
        curso_selecionado = cb_curso.get()
        if curso_selecionado:
            id_curso = cursos_dict.get(curso_selecionado)
            if id_curso:
                connection.deletar_curso(id_curso)
                connection.deletar_matricula_por_curso(id_curso)
                callback_atualizar_combobox()
                messagebox.showinfo("Sucesso", f"Curso '{curso_selecionado}' deletado com sucesso!", parent=root)
                root.destroy()
            else:
                messagebox.showerror("Erro", "ID do curso não encontrado.", parent=root)
        else:
            messagebox.showwarning("Aviso", "Selecione um curso para deletar.", parent=root)

    btn_salvar = tk.Button(frame_center, text="Deletar", command=deletar_curso)
    btn_salvar.pack(pady=(5, 10))

    root.mainloop()

def tela_deletar_disciplina(callback_atualizar_combobox):
    disc_raw = connection.listar_disciplinas()  
    disc_dict = {linha[1]: linha[0] for linha in disc_raw}
    disc_formatados = list(disc_dict.keys())

    root = tk.Toplevel()  
    root.title("Deletar Disciplina")

    largura_janela = 300
    altura_janela = 170
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    label_nome = tk.Label(root, text="Nome da Disciplina:")
    label_nome.pack(pady=(20, 10))

    # Frame centralizado para os widgets
    frame_center = tk.Frame(root)
    frame_center.pack(expand=True)

    cb_disc = ttk.Combobox(frame_center, values=disc_formatados, width=27, state="readonly")
    cb_disc.pack(pady=(0, 10))

    def deletar_disc():
        disc_selecionado = cb_disc.get()
        if disc_selecionado:
            id_disc = disc_dict.get(disc_selecionado)
            if id_disc:
                connection.deletar_disciplina(id_disc)
                callback_atualizar_combobox()
                messagebox.showinfo("Sucesso", f"Disciplina '{disc_selecionado}' deletado com sucesso!", parent=root)
                root.destroy()
            else:
                messagebox.showerror("Erro", "ID do disciplina não encontrado.", parent=root)
        else:
            messagebox.showwarning("Aviso", "Selecione um disciplina para deletar.", parent=root)

    btn_salvar = tk.Button(frame_center, text="Deletar", command=deletar_disc)
    btn_salvar.pack(pady=(5, 10))

    root.mainloop()
