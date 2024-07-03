from src.database.db import db

class Provincia(db.Model):
  id_prov = db.Column(db.Integer, primary_key=True)
  provincia = db.Column(db.Text)

  def __init__(self, provincia) -> None:
    self.provincia = provincia
  
  def to_json(self):
    return {
      'id_prov': self.id_prov,
      'provincia' : self.provincia
    }