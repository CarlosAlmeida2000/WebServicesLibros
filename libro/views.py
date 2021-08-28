from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

class Libro(APIView):

    def get(self, request, format=None):
            if request.method == "GET":
                try:
                   
                    return Response({"consulta": ""})
                except Exception as ex:
                    return Response({"mensaje": "Ups, no se encuentra registrado el libro...."})


