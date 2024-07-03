from src.database.db import db

# Define el modelo del Usuario (Paciente o Especialista)
class Usuario(db.Model):
    id_usu = db.Column(db.Integer, primary_key=True)
    id_per = db.Column(db.Integer)
    nom_completo = db.Column(db.Text)
    num_cel = db.Column(db.Integer)
    edad = db.Column(db.Integer)
    sexo = db.Column(db.Text)
    tipo_usuario = db.Column(db.Text)

    # Constructor para inicializar una instancia de Usuario
    def __init__(self, id_per, nom_completo, num_cel, edad, sexo, tipo_usuario) -> None:
        self.id_per = id_per
        self.nom_completo = nom_completo
        self.num_cel = num_cel
        self.edad = edad
        self.sexo = sexo
        self.tipo_usuario = tipo_usuario

    # Método para convertir una instancia de Usuario a formato JSON
    def to_json(self):
        return {
            'id_usu': self.id_usu,
            'id_per': self.id_per,
            'nom_completo': self.nom_completo,
            'num_cel': self.num_cel,
            'edad': self.edad,
            'sexo': self.sexo,
            'tipo_usuario': self.tipo_usuario
        }
