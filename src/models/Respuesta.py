class Respuesta:
    def __init__(self, puntuacion, id_preg):
        self.puntuacion = puntuacion
        self.id_preg = id_preg

    def to_json(self):
        return {
            'puntuacion': self.puntuacion,
            'id_preg': self.id_preg
        }
