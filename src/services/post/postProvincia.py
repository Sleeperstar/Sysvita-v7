from src.database.db import connection
from src.models.Provincia import Provincia

# Función para manejar la obtención de provincias por departamento
def getProvincias(id_dep):
    try:
        conn = connection()  # Conecta a la base de datos
        provincias = []

        inst = '''
            select p.* from provincia p, dep_prov dp where dp.id_prov = p.id_prov and dp.id_dep = %(id_dep)s;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'id_dep':id_dep})
            
            for row in cursor.fetchall():
                provincia = Provincia(row[1])
                provincia.id_prov = row[0]
                provincias.append(provincia.to_json())
            cursor.close()
        conn.close()
        
        return provincias  # Devuelve todas las provincias
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
