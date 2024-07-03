from src.database.db import connection

from src.models.PacienteUbigeo import PacienteUbigeo

def getPacienteUbigeo():
    try:
        conn = connection()
        ubigeos = []
        
        # Seleccionamos todos los pacientes que cuenten con ubigeo y cuestionarios resueltos
        inst =  '''
                select distinct u.id_usu, p.id_per, concat(p.nombres, ' ', p.apellidos) as nom_completo, p.edad, p.sexo, d.departamento, pr.provincia,
                ub.distrito, ub.x, ub.y
                from persona p, usuario u, tipo_usu tu, ubigeo ub, departamento d, dep_prov dp, provincia pr, prov_ubi pu, pac_exp pe, exp_cuest_det ecd
                where u.id_per = p.id_per and u.id_tipo_usu = tu.id_tipo_usu and ub.id_ubi = p.id_ubi and tu.id_tipo_usu = 1
                and d.id_dep = dp.id_dep and dp.id_prov = pr.id_prov and pr.id_prov = pu.id_prov and pu.id_ubi = ub.id_ubi
                and u.id_usu = pe.id_pac and pe.id_exp = ecd.id_exp;
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, )
            for row in cursor.fetchall():
                ubigeo = PacienteUbigeo(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], '',  '', '')
                ubigeo.id_usu = row[0]
                ubigeos.append(ubigeo)
            cursor.close()
            
        for ubigeo in ubigeos:
            #Obtener el ultimo test realizado por paciente y su respectivo nivel
            id_cuest_det = ''
            inst =  '''
                    select max(cd.id_cuest_det)
                    from cuest_det cd, pac_exp pe, exp_cuest_det ecd
                    where cd.id_cuest_det = ecd.id_cuest_det and ecd.id_exp = pe.id_exp and pe.id_pac = %(id_usu)s;
                    '''
            with conn.cursor() as cursor:
                cursor.execute(inst, {'id_usu': ubigeo.id_usu})
                for row in cursor.fetchall():
                    id_cuest_det = row[0]
                cursor.close()
            
            #Obtener los resultados de ese test
            inst =  '''
                    select cd.id_cuest_det, c.titulo as cuestionario, da.nivel as resultado ,r.nivel
                    from cuestionario c, cuest_det cd, cuest_ran cr, rango r, diag_auto da
                    where c.id_cuest = cd.id_cuest and c.id_cuest = cr.id_cuest and cr.id_ran = r.id_ran and cr.id_diag_auto = da.id_diag_auto
                    and cd.id_cuest_det = %(id_cuest_det)s and r.minimo<=cd.punt_total and r.maximo>=cd.punt_total;
                    '''
            with conn.cursor() as cursor:
                cursor.execute(inst, {'id_cuest_det':id_cuest_det})
                for row in cursor.fetchall():
                    ubigeo.cuestionario = row[1]
                    ubigeo.resultado = row[2]
                    ubigeo.nivel = row[3]
                cursor.close()
        
        conn.close()
            
        nuevo_ubigeos = []
        for ubigeo in ubigeos:
            nuevo_ubigeos.append(ubigeo.to_json())
        
        return nuevo_ubigeos
    except Exception as e:
        print("→ Error: "+str(e))
        return ''