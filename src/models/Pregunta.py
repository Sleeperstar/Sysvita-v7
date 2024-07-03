from src.database.db import db

class Pregunta(db.Model):
  id_preg = db.Column(db.Integer, primary_key=True)
  pregunta = db.Column(db.Text)
  val_min = db.Column(db.Integer)
  val_max = db.Column(db.Integer)

  def __init__(self, pregunta, val_min, val_max) -> None:
    self.pregunta = pregunta
    self.val_min = val_min
    self.val_max = val_max
  
  def to_json(self):
    return {
      'id_preg': self.id_preg,
      'pregunta' : self.pregunta,
      'val_min': self.val_min,
      'val_max': self.val_max
    }