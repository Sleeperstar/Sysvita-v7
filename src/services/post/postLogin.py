from src.database.db import connection
from src.models.Usuario import Usuario

# Función para manejar el inicio de sesión
def postLogin(correo, contra):
    try:
        conn = connection()  # Conecta a la base de datos
        usuario = None

        # Verifica en la tabla de Pacientes
        inst_paciente = '''
            select u.id_usu, p.id_per, concat(p.nombres, ' ', p.apellidos) as nom_completo, p.num_cel, p.edad, p.sexo, tu.tipo_usuario
            from persona p, usuario u, tipo_usu tu
            where p.id_per = u.id_per and tu.id_tipo_usu = u.id_tipo_usu
            and u.correo = %(email)s and u.contra = %(contra)s;
        '''
        with conn.cursor() as cursor:
            cursor.execute(inst_paciente, {'email': correo, 'contra': contra})
            row = cursor.fetchone()
            if row:
                usuario = Usuario(row[1], row[2], row[3], row[4], row[5], row[6])
                usuario.id_usu = row[0]
            cursor.close()
        conn.close()
        
        return usuario  # Devuelve el usuario encontrado
    except Exception as e:
        print("→ Error: " + str(e))
        return ''
