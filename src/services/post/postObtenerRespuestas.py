from src.database.db import connection

def postObtenerRespuestas(id_cuest, id_preg):
    try:
        conn = connection()
        respuestas = []
        inst = '''
            SELECT respuesta FROM Respuesta
            WHERE id_cuest = %(id_cuest)s AND id_preg = %(id_preg)s;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest': id_cuest, 'id_preg': id_preg})
            for row in cursor.fetchall():
                respuesta = {
                    'respuesta': row[0]
                }
                respuestas.append(respuesta)
            conn.commit()
            cursor.close()
        conn.close()
        return respuestas
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
