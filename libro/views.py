from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import libro
from django.db import transaction
import base64, json, os
from datetime import datetime

class Libro(APIView):
    # Obtener todos los libros
    # GET sin parámetros
    # http://127.0.0.1:8000/api-libro/libro/
    def get(self, request, format=None):
            if request.method == "GET":
                try:
                    json_libro = list()
                    if('id' in request.GET):
                        unLibro = libro.objects.get(id = request.GET['id'])
                        object_json = self.buildJsonLibro(unLibro)
                        if(object_json != None):
                            json_libro.append(object_json)
                            return Response({"libro": json_libro})
                        else:
                            raise Exception
                    elif('libro' in request.GET):
                        unLibro = libro.objects.get(nombre = request.GET['libro'])
                        object_json = self.buildJsonLibro(unLibro)
                        if(object_json != None):
                            json_libro.append(object_json)
                            return Response({"libro": json_libro})
                        else:
                            raise Exception
                    else:
                        for h in libro.objects.all():    
                            object_json = self.buildJsonLibro(h)
                            if(object_json != None):
                                json_libro.append(object_json)
                            else:
                                raise Exception
                        return Response({"libro": json_libro})
                except Exception as ex:
                    return Response({"mensaje": "Ups, sucedió un error al obtener los datos, por favor intente de nuevo."})

    def buildJsonLibro(self, libro):
        try:
            encoded_string = "data:image/PNG;base64," + str(base64.b64encode(open(str(libro.ruta_foto.url)[1:], "rb").read()))[2:][:-1]
            un_libro = {
                "libro_id": libro.id,
                "nombre": libro.nombre,
                "descripcion": libro.descripcion,
                "foto": encoded_string
            }
            return un_libro
        except Exception as e:
            return None
    
    # Registrar un libro
    # http://127.0.0.1:8000/api-libro/libro/
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unLibro = libro()
                    unLibro.nombre = json_data['nombre']
                    unLibro.descripcion = json_data['descripcion']
                    img_file = self.buildImage(json_data['foto'])
                    if(img_file != None):
                        unLibro.ruta_foto = img_file
                        unLibro.save()
                    else:
                        raise Exception
                    return Response({"confirmacion": "True"})
            except Exception as e:
                return Response({"confirmacion": "False"})

    # Modificar un libro
    # http://127.0.0.1:8000/api-libro/libro/
    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unLibro = libro.objects.get(id = json_data['libro_id'])
                    unLibro.nombre = json_data['nombre']
                    unLibro.descripcion = json_data['descripcion']
                    img_file = self.buildImage(json_data['foto'])
                    if(img_file != None):
                        unLibro.ruta_foto = img_file
                        unLibro.save()
                    else:
                        raise Exception
                    return Response({"confirmacion": "True"})
            except libro.DoesNotExist:
                return Response({"confirmacion": "False"})
            except Exception as e:
                return Response({"confirmacion": "False"})

    def buildImage(self, base64img):
        try:
            format, img_body = base64img.split(";base64,")
            extension = format.split("/")[-1]
            now = datetime.now()
            img_file = ContentFile(base64.b64decode(img_body), name = "libro_f_" + str(now.year) +"-" + str(now.month) + str(now.day) + "-h-" + str(now.hour) + "-m-" + str(now.minute) +"-s-" + str(now.second) + "." + extension)
            return img_file
        except Exception as e:
            return None

    # Eliminar un libro
    # http://127.0.0.1:8000/api-libro/libro/
    def delete(self, request, format = None):
        if request.method == 'DELETE':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unLibro = libro.objects.get(id = json_data['libro_id'])
                    ruta_img_borrar = unLibro.ruta_foto.url[1:]
                    os.remove(ruta_img_borrar)
                    unLibro.delete()
                    return Response({"confirmacion": "True"})
            except libro.DoesNotExist:
                return Response({"confirmacion": "False"})
            except Exception as e:
                return Response({"confirmacion": "False"})


