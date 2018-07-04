class Aluno:
    def __init__(self, row):
        self.name = row[0]
        self.email = row[1]
        self.endereco = row[2]
        try:
            self.matricula = row[3]
        except IndexError:
            self.matricula = None
