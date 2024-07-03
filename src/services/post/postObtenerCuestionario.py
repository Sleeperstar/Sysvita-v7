from src.database.db import connection

from src.models.Cuestionario import Cuestionario
from src.models.Pregunta import Pregunta

def postObtenerCuestionario(id_cuest):
    try:
        conn = connection()
        cuestionario = ''
        inst =  '''
                    SELECT CUEST.* FROM Cuestionario CUEST
                    WHERE CUEST.id_cuest = %(id_cuest)s;
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest': id_cuest})
            for row in cursor.fetchall():
                cuestionario = Cuestionario(row[1], row[2])
                cuestionario.id_cuest = row[0]
            cursor.close()
        
        preguntas = []
        inst =  '''
                    select p.* from pregunta p, cuest_preg cp where cp.id_preg = p.id_preg and cp.id_cuest = %(id_cuest)s
	                order by id_preg;
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest': id_cuest})
            for row in cursor.fetchall():
                pregunta = Pregunta(row[1], row[2], row[3])
                pregunta.id_preg = row[0]
                preguntas.append(pregunta.to_json())
            conn.commit()
            cursor.close()
        conn.close()
        
        result = {"cuestionario": cuestionario.to_json(), "preguntas":preguntas}
        return result
    except Exception as e:
        print("→ Error: "+e)
        return ''