from src.database.db import connection
from src.models.Ubigeo import Ubigeo

# Función para manejar la obtención de provincias por departamento
def getUbigeo(id_prov):
    try:
        conn = connection()  # Conecta a la base de datos
        ubigeos = []

        inst = '''
            select u.* from ubigeo u, prov_ubi pu where pu.id_ubi = u.id_ubi and pu.id_prov = %(id_prov)s;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_prov':id_prov})
            
            for row in cursor.fetchall():
                ubigeo = Ubigeo(row[1], row[2], row[3], row[4], row[5], row[6])
                ubigeo.id_ubi = row[0]
                ubigeos.append(ubigeo.to_json())
            cursor.close()
        conn.close()
        
        return ubigeos  # Devuelve todos los ubigeos
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
