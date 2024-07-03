from src.database.db import connection

from src.models.DiagnosticoAuto import DiagnosticoAuto

def postRegistrarRespuestas(id_usu, id_cuest, respuestas):
    try:
        conn = connection()
        
        # Saber si el paciente tiene un expediente abierto
        inst = '''
            select max(ex.id_exp) as id_exp from expediente ex, pac_exp pe
	        where ex.id_exp = pe.id_exp and ex.estado = 'abierto' and pe.id_pac = %(id_usu)s;
        '''
        id_exp = None
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_usu':id_usu})
            for row in cursor.fetchall():
                id_exp = row[0]
            cursor.close()
        
        # Si no tiene expediente lo crea y asocia
        if id_exp == None:
            inst = '''
                insert into expediente(fecha_creacion, estado)
                values(to_date(current_date::text, 'YYYY-MM-DD'), 'abierto')
                returning id_exp;
            '''
            with conn.cursor() as cursor:
                cursor.execute(inst, )
                for row in cursor.fetchall():
                    id_exp = row[0]
                cursor.close()
            
            inst = '''
                insert into pac_exp(id_pac, id_exp)
                values (%(id_usu)s, %(id_exp)s);
            '''
            with conn.cursor() as cursor:
                cursor.execute(inst, {'id_usu':id_usu, 'id_exp':id_exp})
                cursor.close()
        
        # Crea la entidad cuest_det para guardar el cuestionario
        inst = '''
            insert into cuest_det(punt_total, fecha, id_cuest)
            values(0, to_date(current_date::text, 'YYYY-MM-DD'), %(id_cuest)s)
            returning id_cuest_det;
        '''
        id_cuest_det = None
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest':id_cuest})
            for row in cursor.fetchall():
                id_cuest_det = row[0]
            cursor.close()
        
        # Asocia la entidad cuest_det a el expediente
        inst = '''
            insert into exp_cuest_det(id_exp, id_cuest_det)
	        values(%(id_exp)s, %(id_cuest_det)s)
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_exp':id_exp, 'id_cuest_det':id_cuest_det})
            cursor.close()
        
        # Insertar los detalles de las preguntas
        inst_base = 'insert into det_preg (puntuacion, id_preg, id_cuest_det)\nvalues'
        inst_comp = ''
        for respuesta in respuestas:
            inst_comp += f'({respuesta.puntuacion}, {respuesta.id_preg}, {id_cuest_det}),'
        inst = inst_base + inst_comp
        inst = inst[:-1] + ";"
        with conn.cursor() as cursor:
            cursor.execute(inst, )
            cursor.close()
        
        # Actualizar el total del cuestionario del paciente
        inst = '''
            update cuest_det
            set punt_total = (select sum(puntuacion) from det_preg where id_cuest_det = %(id_cuest_det)s)
            where id_cuest_det = %(id_cuest_det)s;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest_det':id_cuest_det})
            conn.commit()
            cursor.close()
        
        # Devuelve su diagnostico de manera automática
        inst = '''
            select cd.id_cuest_det, c.titulo , cd.punt_total, concat('[', r.minimo, ', ', r.maximo, ']') as rango,
            da.descripcion, da.nivel, da.recomendacion
            from cuest_det cd, cuestionario c, cuest_ran cr, rango r, diag_auto da
            where cd.id_cuest = c.id_cuest and c.id_cuest = cr.id_cuest and r.id_ran = cr.id_ran
            and da.id_diag_auto = cr.id_diag_auto and r.minimo <= cd.punt_total and r.maximo>= cd.punt_total
            and id_cuest_det = %(id_cuest_det)s;
        '''
        diagnostico = ''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_cuest_det':id_cuest_det})
            for row in cursor.fetchall():
                diagnostico = DiagnosticoAuto(row[1], row[2], row[3], row[4], row[5], row[6])
                diagnostico.id_cuest_det = row[0]
            cursor.close()
        conn.close()
            
        return diagnostico.to_json()
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
