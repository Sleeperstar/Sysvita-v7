from src.database.db import db

class PacienteUbigeo(db.Model):
    id_usu = db.Column(db.Integer, primary_key=True)
    id_per = db.Column(db.Integer)
    nom_completo = db.Column(db.Text)
    edad = db.Column(db.Integer)
    sexo = db.Column(db.Text)
    departamento = db.Column(db.Text)
    provincia = db.Column(db.Text)
    distrito = db.Column(db.Text)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    cuestionario = db.Column(db.Text)
    resultado = db.Column(db.Text)
    nivel = db.Column(db.Text)

    def __init__(self, id_per, nom_completo, edad, sexo, departamento, provincia, distrito, x, y, cuestionario, resultado, nivel) -> None:
        self.id_per = id_per
        self.nom_completo = nom_completo
        self.edad = edad
        self.sexo = sexo
        self.departamento = departamento
        self.provincia = provincia
        self.distrito = distrito
        self.x = x
        self.y = y
        self.cuestionario = cuestionario
        self.resultado = resultado
        self.nivel = nivel

    def to_json(self):
        return {
            'id_usu': self.id_usu,
            'id_per': self.id_per,
            'nom_completo': self.nom_completo,
            'edad': self.edad,
            'sexo': self.sexo,
            'departamento': self.departamento,
            'provincia': self.provincia,
            'distrito': self.distrito,
            'x': self.x,
            'y': self.y,
            'cuestionario': self.cuestionario,
            'resultado': self.resultado,
            'nivel': self.nivel
        }
