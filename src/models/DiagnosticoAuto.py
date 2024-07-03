from src.database.db import db

# Define el modelo del Diagnostico automático
class DiagnosticoAuto(db.Model):
    id_cuest_det = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Integer)
    punt_total = db.Column(db.Text)
    rango = db.Column(db.Integer)
    descripcion = db.Column(db.Integer)
    nivel = db.Column(db.Text)
    recomendacion = db.Column(db.Text)

    def __init__(self, titulo, punt_total, rango, descripcion, nivel, recomendacion) -> None:
        self.titulo = titulo
        self.punt_total = punt_total
        self.rango = rango
        self.descripcion = descripcion
        self.nivel = nivel
        self.recomendacion = recomendacion

    def to_json(self):
        return {
            'id_cuest_det': self.id_cuest_det,
            'titulo': self.titulo,
            'punt_total': self.punt_total,
            'rango': self.rango,
            'descripcion': self.descripcion,
            'nivel': self.nivel,
            'recomendacion': self.recomendacion
        }
