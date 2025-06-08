import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import connection
from datetime import date
import edicao as win

hoje = date.today()

# Formatação colunas
alunos = [{"nome":linha[1]} for linha in connection.listar_alunos()]
alunos_formatados = [f"{aluno['nome']}" for aluno in alunos]

cursos = [{"nomecurso":linha[1]} for linha in connection.listar_cursos()]
cursos_formatados = [f"{curso['nomecurso']}" for curso in cursos]

disciplinas = [{"nome_disciplina":linha[1]} for linha in connection.listar_disciplinas()]
disciplinas_formatados = [f"{disciplina['nome_disciplina']}" for disciplina in disciplinas]

def atualizar_alunos_combobox():
    alunos = [{"nome": linha[1]} for linha in connection.listar_alunos()]
    alunos_formatados = [f"{aluno['nome']}" for aluno in alunos]
    nome_cb['values'] = alunos_formatados

def atualizar_cursos_combobox():
    cursos = [{"nomecurso":linha[1]} for linha in connection.listar_cursos()]
    cursos_formatados = [f"{curso['nomecurso']}" for curso in cursos]
    curso_cb['values'] = cursos_formatados

def atualizar_combobox_curso_por_aluno(event):
    nome = nome_cb.get()
    curso = connection.buscar_curso_aluno(nome)
    if curso:
        curso_cb.config(values=curso)
        curso_cb.set(list(curso)[0])
        atualizar_combobox_disciplina_por_curso(None)  

def atualizar_disciplinas_combobox():
    disciplinas = [{"nome_disciplina":linha[1]} for linha in connection.listar_disciplinas()]
    disciplinas_formatados = [f"{disciplina['nome_disciplina']}" for disciplina in disciplinas]
    disciplina_cb['values'] = disciplinas_formatados

def atualizar_combobox_disciplina_por_curso(event):
    curso = curso_cb.get()
    disciplinas = connection.buscar_disciplina_curso(curso)
    disciplinas_formatadas = [disc[0] for disc in disciplinas]  
    disciplina_cb.config(values=disciplinas_formatadas)
    if disciplinas_formatadas:
        disciplina_cb.set(disciplinas_formatadas[0])

# Atualizar a tabela na interface
def display_data():
    for row in tree.get_children():
        tree.delete(row)
    
    dados_atualizados = connection.listar_notas()  

    for dado in dados_atualizados:
        tree.insert("", tk.END, values=dado)



# Adicionar novo registro
def add_nota():
    nome = nome_cb.get()
    curso = curso_cb.get()
    disciplina = disciplina_cb.get()
    try:
        nota = float(nota_entry.get())
        if nota < 0 or nota > 10:
            messagebox.showerror("Erro", "Nota deve estar entre 0 e 10.")
            return
    except ValueError:
        messagebox.showerror("Erro", "Nota deve ser um número.")
        return

    if nome and curso and disciplina:
        connection.inserir_nota(nome, curso, nota, disciplina, hoje.strftime("%Y-%m-%d"))
        display_data()
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")

def mostrar_menu(event):
    item = tree.identify_row(event.y)
    if item:
        tree.selection_set(item)  # seleciona a linha clicada
        menu_tabela.tk_popup(event.x_root, event.y_root)

def excluir_item():
    selecionado = tree.focus()
    if selecionado:
        valores = tree.item(selecionado, "values")
        connection.deletar_nota(valores[0])
        display_data()
        messagebox.showinfo("Excluir", f"Item excluído: {valores[0]}")
    else:
        messagebox.showwarning("Aviso", "Nenhum item selecionado")


# Interface gráfica
root = tk.Tk()
root.title("Notas dos Alunos")


#Tamanho janela
largura_janela = 1000
altura_janela = 750

largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")



# Criação da barra de Menu
menu_bar = tk.Menu(root)

# Menu "Adicionar"
menu_adicionar = tk.Menu(menu_bar, tearoff=0)
menu_adicionar.add_command(label="Aluno", command=lambda: win.tela_adicionar_aluno(atualizar_alunos_combobox))
menu_adicionar.add_command(label="Curso", command=lambda: win.tela_adicionar_curso(atualizar_cursos_combobox))
menu_adicionar.add_command(label="Disciplina", command=lambda: win.tela_adicionar_disciplina(atualizar_disciplinas_combobox))
menu_adicionar.add_command(label="Matrícula", command=win.tela_adicionar_matricula)
menu_bar.add_cascade(label="Adicionar", menu=menu_adicionar)

menu_deletar = tk.Menu(menu_bar, tearoff=0)
menu_deletar.add_command(label="Aluno", command=lambda: win.tela_deletar_aluno(atualizar_alunos_combobox))
menu_deletar.add_command(label="Curso", command=lambda: win.tela_deletar_curso(atualizar_cursos_combobox))
menu_deletar.add_command(label="Disciplina", command=lambda: win.tela_deletar_disciplina(atualizar_disciplinas_combobox))
menu_bar.add_cascade(label="Excluir", menu=menu_deletar)

# Adiciona a barra de menu na janela
root.config(menu=menu_bar)

menu_tabela = tk.Menu(root, tearoff=0)
menu_tabela.add_command(label="Editar")
menu_tabela.add_command(label="Excluir", command=excluir_item)


frame_top = tk.Frame(root, bg="#b2ebf2", height=180)
frame_top.pack(fill="x", pady=50, padx=30)
frame_top.pack_propagate(False)

# Labels e Comboboxes
tk.Label(frame_top, text="Nome:", font=("Arial", 14), bg="#b2ebf2").grid(row=0, column=0, padx=5, pady=5, sticky="e")
nome_cb = ttk.Combobox(frame_top, values=alunos_formatados, font=("Arial", 14), width=20, state="readonly")
nome_cb.grid(row=0, column=1, padx=5, pady=5)
nome_cb.bind("<<ComboboxSelected>>", atualizar_combobox_curso_por_aluno)


tk.Label(frame_top, text="Curso:", font=("Arial", 14), bg="#b2ebf2").grid(row=0, column=2, padx=5, pady=5, sticky="e")
curso_cb = ttk.Combobox(frame_top, values=cursos_formatados, font=("Arial", 14), width=20, state="readonly")
curso_cb.grid(row=0, column=3, padx=5, pady=5)


tk.Label(frame_top, text="Disciplina:", font=("Arial", 14), bg="#b2ebf2").grid(row=1, column=0, padx=5, pady=5, sticky="e")
disciplina_cb = ttk.Combobox(frame_top, values=disciplinas_formatados, font=("Arial", 14), width=20, state="readonly")
disciplina_cb.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_top, text="Nota:", font=("Arial", 14), bg="#b2ebf2").grid(row=1, column=2, padx=5, pady=5, sticky="e")
nota_entry = tk.Entry(frame_top, font=("Arial", 14), width=10)
nota_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Button(frame_top, text="Salvar Nota", command=add_nota, font=("Arial", 14)).grid(row=2, column=1, pady=10)

# Tabela

columns = ["ID", "Nome", "Curso", "Disciplina", "Nota", "Data"]
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Configuração visual
style = ttk.Style()
style.configure("Treeview", rowheight=35, font=("Arial", 11))

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.bind("<Button-3>", mostrar_menu)

display_data()
root.mainloop()