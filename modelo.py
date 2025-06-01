class cad_alunos:

    def __init__(self, nome:str, email:str):
        self.nome = nome
        self.email = email

class cursos:

    def __init__(self, nomecurso:str):
        self.nomecurso = nomecurso

class disciplinas:

    def __init__(self, nome_disciplina: str, nome_curso: str):
        self.nome_disciplina = nome_disciplina
        self.nome_curso = nome_curso

class matricula:

    def __init__(self, nome_aluno:str, nome_curso:str, data_matricula:str):
        self.nome_aluno = nome_aluno,
        self.nome_curso = nome_curso,
        self.data_matricula = data_matricula

class nota: 

    def __init__(self, nome_aluno: str, nome_curso: str, nota: float, data_avaliacao: str):
        self.nome_aluno = nome_aluno,
        self.nome_curso = nome_curso,
        self.nota = nota,
        self.data_avaliacao = data_avaliacao

