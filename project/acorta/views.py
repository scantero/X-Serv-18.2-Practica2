from django.shortcuts import render
from django.http import HttpResponse
from models import Url
from django.views.decorators.csrf import csrf_exempt
import urllib
# Create your views here.

@csrf_exempt
def inicio(request):
    # request.method, request.resource, request.body # ('GET', '/', '')

    urls = Url.objects.all()

    for url in urls:
        print str(url.url_corta) + "=" + url.url_larga

    if request.method == "GET":


        #si solo es el recurso /
        #   devuelvo el formulario como una pagina html

        respuesta = """
        <div align="center">
        <form action="" method="POST">
        <body bgcolor="blue/red"></body>
            Introduce una Url:<br>
            <input type="text" name="url" value=""
            style = "width:200px; height:50px; font-family:Comic Sans MS;
            border-width:thick; border-style:solid; border-color:yellow">
            <br><br>
            <input type="submit" value="Submit">
        </body>
        </form>
        """
        for url in urls:
            respuesta += str(url.url_corta) + " = " + url.url_larga + "<br>"


    elif request.method == "POST":

        #si lleva qs:
        #   aniado http:// si no lo lleva
        #   genero un nuevo numero (el siguiente)
        #   me apunto la correspondencia en los diccionarios
        #   y en el fichero...
        #   devuelvo url = url_acortada

        body = request.body.split('=',1)[1]
        body = urllib.unquote(body)

        if not (body.startswith("http://") or body.startswith("https://")):
            body = "http://" + body

        try:
            url_pedida = Url.objects.get(url_larga=body)

            respuesta  = """
            <div align="center">
            <body bgcolor="blue/red">
            """
            respuesta += "La entrada ya existe...<br>"
            respuesta += '<a href="' + url_pedida.url_larga + '">' + str(url_pedida.url_corta) + '</a>'
            respuesta += ": "
            respuesta += '<a href="' + url_pedida.url_larga + '">' + url_pedida.url_larga + '</a>'
            respuesta += "</body>"


        except Url.DoesNotExist:

            url_corta = 1 + len(urls)
            new_url = Url(url_larga=body, url_corta=url_corta)
            new_url.save()

            respuesta = """
            <div align="center">
            <body bgcolor="blue/red">
            """
            respuesta += "Se ha introducido una nueva entrada...<br>"
            respuesta += '<a href="' + new_url.url_larga + '">' + str(new_url.url_corta) + '</a>'
            respuesta += ": "
            respuesta += '<a href="' + new_url.url_larga + '">' + new_url.url_larga + '</a>'
            respuesta += "</body>"


    return HttpResponse(respuesta)

def redirige(request, url_acortada):

    if request.method == "GET":

        number = url_acortada
        print "numero introducido = " + number

        #si es el recurso /{numero}
        #   devuelvo la pagina html asociada (o pagina de error 404)
        if number.isdigit():

            try:

                num_pedido = Url.objects.get(url_corta=int(number))

                respuesta = '<html><head><meta http-equiv="refresh"'
                respuesta += 'content="1;url=' + num_pedido.url_larga
                respuesta +=  '" /></head>'
                respuesta += """
                <div align="center">
                <body bgcolor="blue/red">
                </body></html>
                """

            except Url.DoesNotExist:

                respuesta = """
                <div align="center">
                <body bgcolor="blue/red">
                """
                respuesta += "Not found</body>"

        else:

            respuesta = """
            <div align="center">
            <body bgcolor="blue/red">
            """
            respuesta += "Not a number</body>"

        return HttpResponse(respuesta)
