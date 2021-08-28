from usuario.models import usuarios
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json

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
    
    

