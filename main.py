# -*- coding: utf-8 -*-
# Skill de alexa en python explicada
# https://medium.com/disenando-para-la-voz/crear-una-skill-de-alexa-usando-python-2-2-d3bb1bbf95b5
# Para probar la skill podemos hacerlo de 3 formas:
# 1) Pruerbas locales con python-lambda-local index.py -f handler test/LaunchRequest.json
# 2) Utilizando el Test en el servicio Lambda de amazon
# 3) En el simulador de consola de Alexa
# Cuando hagamos la skill y queramos hacer pruebas desde AWS necesitamos
# comprimir toda la skill junto con todas las librerias y el JSON
# Para instalar todas las librerias en el directorio:
# pip3 install ask-sdk -t .

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

import logging
import six

sb = SkillBuilder()

# Creamos el logger para mostrar informacion en las pruebas
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) #Pones debug por que ahora son pruebas, cambiar a INFO

# Todas estas clases son necesarias para que Alexa se pueda iniciar, cerrar o decir las ayudas
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input): # handler_input es lo que dice el usuario
        return is_request_type("LaunchRequest")(handler_input) # Verifica si puede manejar la solicitud, si es de tipo iniciar

    def handle(self, handler_input): # saludamos al usuario
        speechText = "<say-as interpret-as=\"interjection\">Hey Exploradores!</say-as>, espero estéis listos para una nueva aventura. ¿Cuántos objetos queréis buscar hoy?"
        rePrompt = "<say-as interpret-as=\"interjection\">Venga exploradores!</say-as>. A la aventura, ¿Cuantos objetos queréis buscar hoy?"
        # interjection es un modo de hablar de aleja para que de mas enfasis, hay mas modos y se llama SSML

        return handler_input.response_builder.speak(speechText).ask(rePrompt).set_should_end_session(False).response
        # Devolvemos un JSON, speak es para que hable alexa, ask es para que alexa espere una respuesta despues de lo que diga
        # set_should_end_session() debe ser FALSE a menos que queramos que alexa cierre las sesion
        # Si no especificamos el set_should_end_session() alexa cerrara la sesion

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input) # Verifica si lo que dice el usuario es de tipo ayuda

    def handle(self, handler_input):
        speechText = "Bienvenidos a al ayuda de Exploradores Fantásticos!. Sólo debes decirme un número o dejar que decida yo el número de objetos"

        return handler_input.response_builder.speak(speechText).response


 # Clase para detener cualquier cosa que Alexa esté diciendo
class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or # Si cancela o para
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speechText =  "Hasta la próxima aventura!."

        return handler_input.response_builder.speak(speechText)

# Clase para ver si lo que dice el usuario no lo entiende alex o no dice nada
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.response # Cerrar la skill de esta forma no permite que Alexa hable

# Clase para gestionar todas las expecciones, todo lo que alexa no entienda
# Esta clase se usa cuando ninguna de las demás puede
class AllExceptionsHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True # Esto indica que gestionamos cualquier cosa que diga

    def can_handle(self, handler_input, exception):
        speechText = "Lo siento, no te he entendido."

        return handler_input.response_builder.speak(speechText).response

from random import sample

# Ahora hacemos nuestra propia clase, lo que queremos que haga
class ListItemsIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ListItemsIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots # La ruta del JSON donde estan los slots
        defaultObjsToSearch = 3 # El numero de objetos que dirá alexa por defecto

        for slotName, currentSlot in six.iteritems(slots): # Iteramos sobre slots que es la informacion importante que da el usuario
            if slotName == 'numObj': # Verificamos que el nombre de la variable es numObj
                if currentSlot.value: # Vemos si la variable numObj tiene un valor, el numero de objetos
                    objsToSearch = sample(searchObjects, int(currentSlot.value)) # Sacamos X objetos aleatorios
                else:
                    objsToSearch = sample(searchObjects, defaultObjsToSearch) # Sacamos Default objetos

        speechText = "<say-as interpret-as=\"interjection\">Magnífico!</say-as>. Aquí van, prestad atención: {0}. A divertirse!. <say-as interpret-as=\"interjection\">Suerte!</say-as>.".format(", ".join(objsToSearch))
        logger.info(objsToSearch) # Lo enviamos al log para verificar que todo funciona bien en las futuras pruebas
        logger.info(speechText)

        return handler_input.response_builder.speak(speechText).response

# Ahora toca añadir todas nuestras clases a la clase constructora de Skills
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ListItemsIntent())

sb.add_exception_handler(AllExceptionsHandler())

handler = sb.lambda_handler() # Le pasamos a nuestro lambda el metodo handler

# Lista de objetos para buscar
searchObjects = ["bandeja para hacer hielo",
"charco",
"altavoces",
"mando de tv",
"borrador",
"camara fotográfica",
"taza",
"camiseta",
"escritorio",
"patito de goma",
"frigorifico",
"bote de crema dental",
"ipod",
"muñeca",
"periódico",
"mopa",
"peine",
"reloj de pulsera",
"cordón de zapatilla",
"toalla",
"esponja de ducha",
"perfume",
"calcetines",
"tarjeta de felicitación",
"almohada",
"alfombra",
"ventana",
"plato hondo",
"platano",
"percha"]
