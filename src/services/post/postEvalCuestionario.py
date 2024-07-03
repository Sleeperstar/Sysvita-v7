from src.database.db import connection

def postEvalCuestionario(id_cuest_det, id_usu, descripcion, nivel, observaciones, recomendacion):
    try:
        conn = connection()
        
        # Se crea el diagnostico del especialista
        id_diag_esp = ''
        inst =  '''
                    insert into diag_esp(descripcion, nivel, observaciones, recomendacion, fecha)
                    values(%(descripcion)s, %(nivel)s, %(observaciones)s, %(recomendacion)s, to_date(current_date::text, 'YYYY-MM-DD'))
                    returning id_diag_esp;
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'descripcion':descripcion, 'nivel':nivel, 'observaciones':observaciones, 'recomendacion':recomendacion})
            for row in cursor.fetchall():
                id_diag_esp = row[0]
            cursor.close()
        
        # Se asocia el diagnostico al cuestionario
        inst =  '''
                    insert into diag_esp_cuest_det(id_diag_esp, id_cuest_det)
                    values(%(id_diag_esp)s, %(id_cuest_det)s);
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_diag_esp': id_diag_esp, 'id_cuest_det':id_cuest_det})
            cursor.close()
        
         # Se asocia el diagnostico al especialista
        inst =  '''
                    insert into esp_diag_esp(id_esp, id_diag_esp)
                    values(%(id_esp)s, %(id_diag_esp)s);
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_diag_esp': id_diag_esp, 'id_esp':id_usu})
            conn.commit()
            cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print("→ Error: "+e)
        return False