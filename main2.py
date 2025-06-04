import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import connection
from datetime import date

hoje = date.today()


# Formatação colunas
alunos = [{"nome":linha[1]} for linha in connection.listar_alunos()]
alunos_formatados = [f"{aluno['nome']}" for aluno in alunos]

cursos = [{"nomecurso":linha[1]} for linha in connection.listar_cursos()]
cursos_formatados = [f"{curso['nomecurso']}" for curso in cursos]

disciplinas = [{"nome_disciplina":linha[1]} for linha in connection.listar_disciplinas()]
disciplinas_formatados = [f"{disciplina['nome_disciplina']}" for disciplina in disciplinas]

def atualizar_combobox_curso(event):
    nome = nome_cb.get()
    curso = connection.buscar_curso_aluno(nome)
    if curso:
        curso_cb.config(values=curso)
        curso_cb.set(list(curso)[0])
        atualizar_combobox_disciplina(None)  

def atualizar_combobox_disciplina(event):
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
    except ValueError:
        messagebox.showerror("Erro", "Nota deve ser um número.")
        return

    if nome and curso and disciplina:
        connection.inserir_nota(nome, curso, nota, disciplina, hoje.strftime("%Y-%m-%d"))
        display_data()
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")


# Interface gráfica
root = tk.Tk()
root.title("Notas dos Alunos")
root.geometry("1000x750")

frame_top = tk.Frame(root, bg="#b2ebf2", height=180)
frame_top.pack(fill="x", pady=50, padx=30)
frame_top.pack_propagate(False)

# Labels e Comboboxes
tk.Label(frame_top, text="Nome:", font=("Arial", 14), bg="#b2ebf2").grid(row=0, column=0, padx=5, pady=5, sticky="e")
nome_cb = ttk.Combobox(frame_top, values=alunos_formatados, font=("Arial", 14), width=20, state="readonly")
nome_cb.grid(row=0, column=1, padx=5, pady=5)
nome_cb.bind("<<ComboboxSelected>>", atualizar_combobox_curso)


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

display_data()
root.mainloop()
