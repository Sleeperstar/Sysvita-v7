from src.database.db import db

# Define el modelo del Cuestionario Resuelto
class CuestResuelto(db.Model):
    id_cuest_det = db.Column(db.Integer, primary_key=True)
    nom_completo = db.Column(db.Text)
    cuestionario = db.Column(db.Text)
    fecha = db.Column(db.Text)
    punt_total = db.Column(db.Integer)
    diagnostico = db.Column(db.Text)
    nivel = db.Column(db.Text)

    def __init__(self, nom_completo, cuestionario, fecha, punt_total, diagnostico, nivel) -> None:
        self.nom_completo = nom_completo
        self.cuestionario = cuestionario
        self.fecha = fecha
        self.punt_total = punt_total
        self.diagnostico = diagnostico
        self.nivel = nivel

    def to_json(self):
        return {
            'id_cuest_det': self.id_cuest_det,
            'nom_completo': self.nom_completo,
            'cuestionario': self.cuestionario,
            'fecha': self.fecha,
            'punt_total': self.punt_total,
            'diagnostico': self.diagnostico,
            'nivel': self.nivel
        }
