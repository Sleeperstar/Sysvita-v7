from src.database.db import connection
from src.models.Departamento import Departamento

# Función para manejar la obtención de departamentos
def getDepartamentos():
    try:
        conn = connection()  # Conecta a la base de datos
        departamentos = []

        inst = '''
            select * from departamento;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst, )
            for row in cursor.fetchall():
                departamento = Departamento(row[1])
                departamento.id_dep = row[0]
                departamentos.append(departamento.to_json())
            cursor.close()
        conn.close()
        
        return departamentos  # Devuelve todos los departamentos
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
