from flask import Blueprint, jsonify, request

# Modelos
from src.models.Respuesta import Respuesta

# Importa las funciones de servicio necesarias
from src.services.post.postLogin import postLogin
from src.services.post.postRegister import postRegister
from src.services.get.getCuestionarios import getCuestionarios
from src.services.post.postObtenerCuestionario import postObtenerCuestionario
from src.services.post.postRegistrarRespuestas import postRegistrarRespuestas
from src.services.get.getDepartamentos import getDepartamentos
from src.services.post.postProvincia import getProvincias
from src.services.post.postUbigeo import getUbigeo
from src.services.get.getCuestResueltos import getCuestResueltos
from src.services.post.postEvalCuestionario import postEvalCuestionario
from src.services.get.getPacienteUbigeo import getPacienteUbigeo

# Crea un Blueprint para agrupar rutas
main = Blueprint('index_blueprint', __name__)

# Ruta para iniciar sesión
@main.route("/iniciarSesion", methods=['POST'])
def iniciarSesion():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        email = data['email']
        contra = data['contra']
        usuario = postLogin(email, contra)  # Llama a la función de inicio de sesión
        if usuario != None:
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': usuario.to_json()})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

# Ruta para registrar un nuevo usuario
@main.route("/registrar", methods=['POST'])
def register():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        nombre = data['nombre']
        apellidos = data['apellidos']
        num_cel = data['num_cel']
        edad = data['edad']
        sexo = data['sexo']
        id_ubi = data['id_ubi']
        correo = data['email']
        contra = data['contra']
        id_tipo_usu = data['id_tipo_usu']
        registrado = postRegister(nombre, apellidos, num_cel, edad, sexo, id_ubi, correo, contra, id_tipo_usu)  # Llama a la función de registro
        if registrado:
            return jsonify({'message': 'COMPLETE', 'success': True})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})
    
# Ruta para obtener todos los cuestionarios
@main.route("/cuestionarios")
def cuestionarios():
    try:
        cuestionarios = getCuestionarios()  # Llama a la función para obtener cuestionarios
        if cuestionarios != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': cuestionarios})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

# Ruta para obtener un cuestionario completo dado su ID
@main.route("/cuestionarioCompleto", methods=['POST'])
def cuestionario():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        id_cuest = data['id_cuest']
        cuestionario = postObtenerCuestionario(id_cuest)  # Llama a la función para obtener el cuestionario
        if cuestionario != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': cuestionario})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

# Ruta para registrar respuestas
@main.route("/registrarRespuestas", methods=['POST'])
def registrarRespuestas():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        id_usu = data['id_usu']
        id_cuest = data['id_cuest']
        respuestas = data['respuestas']  # Lista de diccionarios con id_preg y respuesta
        respuestasArray = []
        for respuesta in respuestas:
            rpta = Respuesta(respuesta['puntuacion'], respuesta['id_preg'])
            respuestasArray.append(rpta)
        
        registrado = postRegistrarRespuestas(id_usu, id_cuest, respuestasArray)  # Llama a la función de registrar respuestas
        if registrado != '':
            data = registrado
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': data})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

# Ruta para obtener los departamentos
@main.route("/departamentos")
def departamentos():
    try:
        departamentos = getDepartamentos()  # Llama a la función para obtener departamentos
        if departamentos != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': departamentos})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

@main.route("/provincias", methods=['POST'])
def provincias():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        id_dep = data['id_dep']
        provincias = getProvincias(id_dep)  # Llama a la función para obtener provincias
        if provincias != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': provincias})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

@main.route("/ubigeos", methods=['POST'])
def ubigeos():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        id_prov = data['id_prov']
        ubigeos = getUbigeo(id_prov)  # Llama a la función para obtener ubigeos exactos
        if ubigeos != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': ubigeos})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

@main.route("/cuestResueltos")
def cuestResueltos():
    try:
        cuestionarios = getCuestResueltos()  # Llama a la función para obtener todos los cuestionarios resueltos
        if cuestionarios != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': cuestionarios})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

@main.route("/registrarDiagnostico", methods=['POST'])
def registrarDiagnostico():
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        id_cuest_det = data['id_cuest_det']
        id_usu = data['id_usu']
        descripcion = data['descripcion']
        nivel = data['nivel']
        observaciones = data['observaciones']
        recomendacion = data['recomendacion']
        result = postEvalCuestionario(id_cuest_det, id_usu, descripcion, nivel, observaciones, recomendacion)
        if result:
            return jsonify({'message': 'COMPLETE', 'success': True})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})

@main.route("/ubigeosPaciente")
def ubigeosPaciente():
    try:
        ubigeos = getPacienteUbigeo()
        if ubigeos != '':
            return jsonify({'message': 'COMPLETE', 'success': True, 'data': ubigeos})
        else:
            return jsonify({'message': 'NOT FOUND', 'success': True})
    except Exception as e:
        return jsonify({'message': 'ERROR', 'success': False})