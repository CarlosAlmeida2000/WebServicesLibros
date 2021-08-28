from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import libro
from django.db import transaction
import base64, json
from datetime import datetime

class Libro(APIView):
    # Obtener todos los libros
    # GET sin parámetros
    # http://127.0.0.1:8000/api-libro/libro/
    def get(self, request, format=None):
            if request.method == "GET":
                try:
                    json_libro = list()
                    for h in libro.objects.all():    
                        object_json = self.buildJsonLibro(h)
                        if(object_json != None):
                            json_libro.append(object_json)
                        else:
                            raise Exception
                    return Response({"consulta": json_libro})
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
                    image_b64 = json_data['foto']
                    format, img_body = image_b64.split(";base64,")
                    extension = format.split("/")[-1]
                    now = datetime.now()
                    img_file = ContentFile(base64.b64decode(img_body), name = "libro_f_" + str(now.year) +"-" + str(now.month) + str(now.day) + "-h-" + str(now.hour) + "-m-" + str(now.minute) +"-s-" + str(now.second) + "." + extension)
                    unLibro.ruta_foto = img_file
                    unLibro.save()
                    return Response({"confirmacion": "True"})
            except Exception as e:
                return Response({"confirmacion": "False"})



