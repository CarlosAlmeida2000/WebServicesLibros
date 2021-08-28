from usuario.models import usuarios
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
import json

class Usuario(APIView):

    # GET con parámetro id
    # http://127.0.0.1:8000/api-usuario/usuario/?id=5
    # GET con parámetro nombre
    # http://127.0.0.1:8000/api-usuario/usuario/?usuario=carlos
    # GET sin parámetros
    # http://127.0.0.1:8000/api-usuario/usuario/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                json_usuario = list()
                if('id' in request.GET):
                    unUsuario = usuarios.objects.get(id = request.GET['id'])
                    object_json = self.buildJsonUsuario(unUsuario)
                    if(object_json != None):
                        json_usuario.append(object_json)
                        return Response({"usuario": json_usuario})
                    else:
                        raise Exception
                elif('usuario' in request.GET):
                    unUsuario = usuarios.objects.get(usuario = request.GET['usuario'])
                    object_json = self.buildJsonUsuario(unUsuario)
                    if(object_json != None):
                        json_usuario.append(object_json)
                        return Response({"usuario": json_usuario})
                    else:
                        raise Exception
                else:
                    for u in usuarios.objects.all():
                        object_json = self.buildJsonUsuario(u)
                        if(object_json != None):
                            json_usuario.append(object_json)
                        else:
                            raise Exception
                    return Response({"usuario": json_usuario})
            except usuarios.DoesNotExist:
                return Response({"mensaje": "No existe el usuario."})
            except Exception as e:  
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})
    
    def buildJsonUsuario(self, usuario):
        try:
            un_usuario = {
                "usuario_id": usuario.id,
                "nombre": usuario.nombre,
                "rol": usuario.rol,
                "usuario": usuario.usuario,
                "clave": usuario.clave,
            }
            return un_usuario
        except Exception as e:
            return None

    # Registrar un usuario
    # http://127.0.0.1:8000/api-usuario/usuario/
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    if('usuario_id' not in json_data):
                        unUsuario = usuarios()
                        unUsuario = self.buildUsuario(unUsuario, json_data)
                        if(unUsuario != None):
                            if(unUsuario  != "repetido"):
                                unUsuario.save()
                                return Response({"usuario_id": unUsuario.id}) 
                            else:
                                return Response({"mensaje": "Usuario repetido."})   
                        else:
                            raise Exception
                    else:
                        return Response({"mensaje": "Ups... al parecer no envió el json correcto para el método POST, no se requiere de un id."})  
            except Exception as e: 
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})

    # Modificar un usuario
    # http://127.0.0.1:8000/api-usuario/usuario/
    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    if('usuario_id' in json_data):
                        unUsuario = usuarios.objects.get(id = json_data['usuario_id'])
                        unUsuario = self.buildUsuario(unUsuario, json_data)
                        if(unUsuario != None):
                            if(unUsuario  != "repetido"):
                                unUsuario.save()
                                return Response({"confirmacion": "True"})    
                            else:
                                return Response({"mensaje": "Usuario repetido."})  
                        else:
                            raise Exception
                    else:
                        return Response({"confirmacion": "False"})    
            except usuarios.DoesNotExist:
                return Response({"mensaje": "No existe el usuario."})
            except Exception as e: 
                return Response({"confirmacion": "False"})    

    def buildUsuario(self, unUsuario, json_data):
        try:
            if('nombre' in json_data):
                unUsuario.nombre = json_data['nombre']
            if('rol' in json_data):
                unUsuario.rol = json_data['rol']
            if('usuario' in json_data):
                try:
                    newUsuario = usuarios.objects.get(usuario__icontains = json_data['usuario'])
                    if(newUsuario):
                        if('usuario_id' in json_data):
                            if(str(newUsuario.id) == str(json_data['usuario_id'])):
                                unUsuario.usuario = json_data['usuario']
                            else:
                                return "repetido"
                        else:
                            return "repetido"
                except usuarios.DoesNotExist:
                    unUsuario.usuario = json_data['usuario']
            if('clave' in json_data):
                unUsuario.clave = json_data['clave']
            return unUsuario
        except Exception as e: 
            return None


class Login(APIView):

    # Iniciar sesión
    # http://127.0.0.1:8000/api-usuario/login/
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_usuario = list()
                json_data = json.loads(request.body.decode('utf-8'))
                unUsuario = usuarios.objects.get(usuario = json_data['usuario'])
                if(unUsuario.estado != False):
                    if(unUsuario.clave == json_data['clave']):
                        apiViewUsuario = usuarios()
                        object_json = apiViewUsuario.buildJsonUsuario(unUsuario)
                        if(object_json != None):
                            json_usuario.append(object_json)
                            return Response({"usuario": json_usuario})
                        else:
                            raise Exception
                    else:
                        return Response({"mensaje": "La clave es incorrecta."})
                else:
                    return Response({"mensaje": "El usuario se encuentra deshabilitado."})
            except usuarios.DoesNotExist:
                return Response({"mensaje": "No existe el usuario."})
            except Exception as e:  
                return Response({"mensaje": "Sucedió un error al verificar el usuario, por favor intente nuevamente."})
    
    

