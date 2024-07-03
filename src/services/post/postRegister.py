from src.database.db import connection

def postRegister(nombre, apellidos, num_cel, edad, sexo, id_ubi, correo, contra, id_tipo_usu):
    try:
        conn = connection()
        
        inst =  '''
                    insert into persona(nombres, apellidos, num_cel, edad, sexo, id_ubi)
                    values(%(nombre)s, %(apellidos)s, %(num_cel)s, %(edad)s, %(sexo)s, %(id_ubi)s)
                    returning id_per;
                '''
        id_per = None
        with conn.cursor() as cursor:
            cursor.execute(inst, {'nombre': nombre, 'apellidos': apellidos, 'num_cel': num_cel, 'edad':edad, 'sexo':sexo, 'id_ubi':id_ubi})
            for row in cursor.fetchall():
                id_per = row[0]
            cursor.close()
        
        inst =  '''
                    insert into usuario(correo, contra, id_per, id_tipo_usu)
	                values(%(correo)s, %(contra)s, %(id_per)s, %(id_tipo_usu)s);
                '''
        with conn.cursor() as cursor:
            cursor.execute(inst, {'correo': correo, 'contra':contra, 'id_per':id_per, 'id_tipo_usu':id_tipo_usu})
            conn.commit()
            cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print("→ Error: "+str(e))
        return False