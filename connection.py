import sqlite3 as conector


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

    if not alunos:
        print("Nenhum aluno encontrado.")
    else:
        print("Lista de alunos:")
        return alunos

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

    if not cursos:
        print("Nenhum curso encontrado.")
    else:
        print("Lista de Cursos:")
        return cursos

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

    if not disciplinas:
        print("Nenhuma disciplina encontrada.")
    else:
        print("Lista de Disciplinas:")
        return disciplinas

    conexao.close()
 

def inserir_matricula(nome_aluno:str, nome_curso:str, data_matricula:str):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (nome_curso,))
    resultado_curso = cursor.fetchone()

    cursor.execute("SELECT aluno_id FROM cad_alunos WHERE nome = ?", (nome_aluno,))
    resultado_aluno = cursor.fetchone()

    if data_matricula is None:
        data_matricula = "24-05-2025"

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

def inserir_nota(nome_aluno: str, nome_curso: str, nota: float, data_avaliacao: str):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_curso FROM cursos WHERE nomecurso = ?", (nome_curso,))
    resultado_curso = cursor.fetchone()

    cursor.execute("SELECT aluno_id FROM cad_alunos WHERE nome = ?", (nome_aluno,))
    resultado_aluno = cursor.fetchone()

    if data_avaliacao is None:
        data_avaliacao = "2025-05-24"

    if resultado_curso is None:
        print("Curso não encontrado!")
    elif resultado_aluno is None:
        print("Aluno não encontrado!")
    else:
        curso_id = resultado_curso[0]
        aluno_id = resultado_aluno[0]

        cursor.execute(
            "SELECT matricula_id FROM matriculas WHERE aluno_id = ? AND curso_id = ?",
            (aluno_id, curso_id)
        )
        resultado_matricula = cursor.fetchone()

        if resultado_matricula is None:
            print("Matrícula não encontrada!")
        else:
            matricula_id = resultado_matricula[0]
            print("Matrícula encontrada com sucesso!")

            cursor.execute(
                "INSERT INTO notas (matricula_id, nota, data_avaliacao) VALUES (?, ?, ?)",
                (matricula_id, nota, data_avaliacao)
            )
            conexao.commit()
            print("Nota inserida com sucesso!")

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

        return resultado_disciplinas

    conexao.close()