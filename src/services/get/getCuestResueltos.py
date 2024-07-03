from src.database.db import connection
from src.models.CuestResuelto import CuestResuelto

# Función para manejar la obtención de cuestionarios resueltos
def getCuestResueltos():
    try:
        conn = connection()  # Conecta a la base de datos
        cuestionarios = []

        inst = '''
            select cd.id_cuest_det, concat(p.nombres, ' ', p.apellidos) as nom_completo, c.titulo as cuestionario,
            to_char(cd.fecha, 'DD-MM-YYYY') as fecha, cd.punt_total, da.nivel as diagnostico, r.nivel
            from cuest_det cd, exp_cuest_det ecd, expediente e, pac_exp pe, usuario u, persona p,
            cuestionario c, cuest_ran cr, rango r, diag_auto da
            where cd.id_cuest_det = ecd.id_cuest_det and ecd.id_exp = e.id_exp and pe.id_exp = e.id_exp
            and pe.id_pac = u.id_usu and u.id_per = p.id_per and cd.id_cuest = c.id_cuest and cr.id_cuest = c.id_cuest
            and cr.id_ran = r.id_ran and cr.id_diag_auto = da.id_diag_auto and cd.punt_total<=r.maximo and cd.punt_total>=r.minimo
            and cd.id_cuest_det not in (select decd.id_cuest_det from diag_esp_cuest_det decd);
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, )
            for row in cursor.fetchall():
                cuestionario = CuestResuelto(row[1], row[2], row[3], row[4], row[5], row[6])
                cuestionario.id_cuest_det = row[0]
                cuestionarios.append(cuestionario.to_json())
            cursor.close()
        conn.close()
        
        return cuestionarios  # Devuelve todos los cuestionarios resueltos
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
