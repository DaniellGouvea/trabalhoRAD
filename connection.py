import sqlite3 as conector
from datetime import date
from tkinter import messagebox

hoje = date.today()


def conectar ():
    return conector.connect("./EscolaNotasData.db")

def inserir_aluno(nome:str, email:str):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO cad_alunos(nome, email) VALUES (?,?)", (nome, email))
    conexao.commit()
    conexao.close()
    print("aluno inserido com sucesso")

def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM cad_alunos")
    alunos = cursor.fetchall()

    conexao.close()

    if not alunos:
        print("Nenhum aluno encontrado.")
    else:
        print("Lista de alunos:")
 
        return alunos

def deletar_aluno(id_aluno):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM cad_alunos WHERE aluno_id = ?", (id_aluno,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma aluno com ID {id_aluno} foi encontrada.")
    else:
        print(f"Aluno com ID {id_aluno} deletada com sucesso.")

    conexao.close()


def inserir_cursos(nomecurso:str):

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO cursos(nomecurso) VALUES (?)", (nomecurso,))
    conexao.commit()
    conexao.close()
    print("curso adicionado com sucesso")

def listar_cursos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()
    conexao.close()
    if not cursos:
        print("Nenhum curso encontrado.")
    else:
        print("Lista de Cursos:")
        return cursos

def deletar_curso(id_curso:int):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM cursos WHERE id_curso = ?", (id_curso,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma nota com ID {id_curso} foi encontrada.")
    else:
        print(f"Nota com ID {id_curso} deletada com sucesso.")

    conexao.close()

def inserir_disciplina(nome_disciplina: str, nome_curso: str):


    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (nome_curso,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("Curso não encontrado!")
    else:
        curso_id = resultado[0]     
        cursor.execute(
            "INSERT INTO disciplinas (nome_disciplina, curso_id) VALUES (?, ?)",
            (nome_disciplina, curso_id)
        )
        conexao.commit()
        print("Disciplina inserida com sucesso!")

    conexao.close()

def listar_disciplinas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM disciplinas")
    disciplinas = cursor.fetchall()
    conexao.close()

    if not disciplinas:
        print("Nenhuma disciplina encontrada.")
    else:
        print("Lista de Disciplinas:")
        return disciplinas

def deletar_disciplina(id_disciplina:int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM disciplinas WHERE id_disciplina = ?", (id_disciplina,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma disciplina com ID {id_disciplina} foi encontrada.")
    else:
        print(f"Disciplina com ID {id_disciplina} deletada com sucesso.")

    conexao.close()

def inserir_matricula(nome_aluno:str, nome_curso:str, data_matricula:str):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (nome_curso,))
    resultado_curso = cursor.fetchone()

    cursor.execute("SELECT aluno_id FROM cad_alunos WHERE nome = ?", (nome_aluno,))
    resultado_aluno = cursor.fetchone()

    if data_matricula is None:
        data_matricula = hoje.strftime("%Y-%m-%d")

    if resultado_curso is None:
        print("Curso não encontrado!")
    elif resultado_aluno is None:
        print("Aluno não encontrado!")
    else:
        curso_id = resultado_curso[0]    
        aluno_id = resultado_aluno[0] 
        cursor.execute(
            "INSERT INTO matriculas (aluno_id, curso_id, data_matricula) VALUES (?, ?, ?)",
            (aluno_id, curso_id, data_matricula)
        )
        conexao.commit()
        print("Matricula inserida com sucesso!")

    conexao.close()

def deletar_matricula_por_aluno(id_aluno):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM matriculas WHERE aluno_id = ?", (id_aluno,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma matricula com ID {id_aluno} foi encontrada.")
    else:
        print(f"Matricula com ID {id_aluno} deletada com sucesso.")

    conexao.close()

def deletar_matricula_por_curso(id_curso):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM matriculas WHERE curso_id = ?", (id_curso,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma Matricula com ID {id_curso} foi encontrada.")
    else:
        print(f"Matricula com ID {id_curso} deletada com sucesso.")

    conexao.close()

def inserir_nota(nome_aluno: str, nome_curso: str, nota: float, disciplina:str, data_avaliacao: str):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (nome_curso,))
    resultado_curso = cursor.fetchone()

    cursor.execute("SELECT aluno_id FROM cad_alunos WHERE nome = ?", (nome_aluno,))
    resultado_aluno = cursor.fetchone()

    cursor.execute("SELECT id_disciplina FROM disciplinas WHERE nome_disciplina = ?", (disciplina,))
    resultado_disciplina = cursor.fetchone()

    if data_avaliacao is None:
        hoje.strftime("%Y-%m-%d")

    if resultado_curso is None:
        print("Curso não encontrado!")
    elif resultado_aluno is None:
        print("Aluno não encontrado!")
    elif resultado_disciplina is None:
        print("Disciplina não encontrada")
    else:
        curso_id = resultado_curso[0]
        aluno_id = resultado_aluno[0]
        disciplina_id = resultado_disciplina[0]

        cursor.execute(
            "SELECT matricula_id FROM matriculas WHERE aluno_id = ? AND curso_id = ?",
            (aluno_id, curso_id)
        )
        resultado_matricula = cursor.fetchone()

        if resultado_matricula is None:
            print("Matrícula não encontrada!")
        else:
            matricula_id = resultado_matricula[0]

            cursor.execute("""
                SELECT 1 FROM notas 
                WHERE matricula_id = ? AND disciplina_id = ? AND data_avaliacao = ?
            """, (matricula_id, disciplina_id, data_avaliacao))

            if cursor.fetchone():
                messagebox.showwarning("Aviso", "Essa nota já está cadastrado.")
                print("Já existe uma nota cadastrada para essa avaliação.")
            else:
                cursor.execute("""
                    INSERT INTO notas (matricula_id, nota, data_avaliacao, disciplina_id) 
                    VALUES (?, ?, ?, ?)
                """, (matricula_id, nota, data_avaliacao, disciplina_id))
                conexao.commit()
                print("Nota inserida com sucesso!")
            
    conexao.close()

def listar_notas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""

    SELECT 
        notas.nota_id,
        cad_alunos.nome AS alunonome,
        cursos.nomecurso AS cursonome,
        disciplinas.nome_disciplina AS disciplinanome,
        notas.nota,
        notas.data_avaliacao
    FROM
        notas
    JOIN
        matriculas ON notas.matricula_id = matriculas.matricula_id
    JOIN
        cad_alunos ON matriculas.aluno_id = cad_alunos.aluno_id
    JOIN
        cursos ON matriculas.curso_id = cursos.id_curso
    JOIN
        disciplinas ON disciplinas.id_disciplina = notas.disciplina_id

    """)

    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def deletar_nota(id_nota:int):
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM notas WHERE nota_id = ?", (id_nota,))
    conexao.commit()

    if cursor.rowcount == 0:
        print(f"Nenhuma nota com ID {id_nota} foi encontrada.")
    else:
        print(f"Nota com ID {id_nota} deletada com sucesso.")

    conexao.close()

def buscar_curso_aluno(nome_aluno:str):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT aluno_id FROM cad_alunos WHERE nome = ?", (nome_aluno,))
    resultado_aluno = cursor.fetchone()

    if resultado_aluno is None:
        print("Aluno não encontrado!")
    else:
        aluno_id = resultado_aluno[0]     
        cursor.execute("SELECT curso_id FROM matriculas WHERE aluno_id= ?", (aluno_id,))
        resultado_curso = cursor.fetchone()
        
        if resultado_curso is None:
            print("Disciplina não encontrada")
        else:
            curso_id = resultado_curso[0]
            cursor.execute("SELECT nomecurso FROM cursos WHERE id_curso= ?", (curso_id,))
            resultado_curso = cursor.fetchone()
            conexao.close()
            return resultado_curso


    conexao.close()

def buscar_disciplina_curso(curso_nome:str):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (curso_nome,))
    resultado_curso = cursor.fetchone()

    

    if resultado_curso is None:
        print("Curso não encontrado!")
    else:
        curso_id = resultado_curso[0]     
        cursor.execute("SELECT nome_disciplina FROM disciplinas WHERE curso_id= ?", (curso_id,))
        resultado_disciplinas = cursor.fetchall()

        print(resultado_disciplinas)

        conexao.close()
        return resultado_disciplinas
    
    conexao.close()
