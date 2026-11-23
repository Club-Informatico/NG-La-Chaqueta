## ============================================================================
##  LA CHAQUETA · Una leyenda de Copiapó
##  Definiciones: personajes, imágenes, transformaciones, sonido y estilo.
## ============================================================================

## Este archivo se carga después de gui.rpy y screens.rpy para poder
## ajustar algunos estilos sin tocar los archivos que genera Ren'Py.
init offset = 1


## ----------------------------------------------------------------------------
##  Personajes
## ----------------------------------------------------------------------------

## El nombre de la pasajera se revela recién en el cementerio.
default nombre_pasajera = "Pasajera"

define r = Character("Rodolfo", color="#e7b866")
define p = Character("[nombre_pasajera]", color="#e9a3a3", what_color="#f1e9e4")
define t = Character("Tomás", color="#d8c7a3")
define l = Character("Don Lucho", color="#9fc2de")
define a = Character("Don Arsenio", color="#b9cf9d")

## La carta se lee en modo NVL (pantalla completa), en cursiva.
define carta = Character(None, kind=nvl, what_italic=True, what_color="#f2e6cf")


## ----------------------------------------------------------------------------
##  Variables de la historia
## ----------------------------------------------------------------------------

default vio_foto = False          # ¿Rodolfo dio vuelta la foto en el prólogo?
default pistas = set()            # pistas que descubrió en el taxi
default opciones_taxi = set()     # opciones ya elegidas en el menú del taxi
default palabras = "silencio"     # lo que Rodolfo le dice a Inés al final


## ----------------------------------------------------------------------------
##  Imágenes
## ----------------------------------------------------------------------------

image negro = Solid("#000000")

## Fondos
image bg casa_noche = "images/bg/casa_noche.webp"
image bg plaza_noche = "images/bg/plaza_noche.webp"
image bg taxi_frente = "images/bg/taxi_frente.webp"
image bg taxi_frente_detenido = "images/bg/taxi_frente_detenido.webp"
image bg taxi_atras = "images/bg/taxi_atras.webp"
image bg avenida_noche = "images/bg/avenida_noche.webp"
image bg muro_cementerio = "images/bg/muro_cementerio.webp"
image bg paradero_noche = "images/bg/paradero_noche.webp"
image bg cementerio_reja = "images/bg/cementerio_reja.webp"
image bg cementerio_pasaje = "images/bg/cementerio_pasaje.webp"
image bg cementerio_alba = "images/bg/cementerio_alba.webp"

## Escenas especiales (CG)
image cg titulo = "images/cg/titulo.webp"
image cg foto = "images/cg/foto.webp"
image cg espejo_vacio = "images/cg/espejo_vacio.webp"
image cg espejo_ines = "images/cg/espejo_ines.webp"
image cg billete = "images/cg/billete.webp"
image cg chaqueta_asiento = "images/cg/chaqueta_asiento.webp"
image cg libro = "images/cg/libro.webp"
image cg nicho = "images/cg/nicho.webp"
image cg pasajes = "images/cg/pasajes.webp"
image cg recuerdo = "images/cg/recuerdo.webp"
image cg carta = "images/cg/carta.webp"
image cg nichos_final = "images/cg/nichos_final.webp"

## Personajes (sprites)
image ines neutral = "images/sprites/ines_neutral.png"
image ines triste = "images/sprites/ines_triste.png"
image ines sonrisa = "images/sprites/ines_sonrisa.png"
image ines sin = "images/sprites/ines_sin.png"
image lucho neutral = "images/sprites/lucho_neutral.png"
image lucho triste = "images/sprites/lucho_triste.png"
image arsenio neutral = "images/sprites/arsenio_neutral.png"
image tomas neutral = "images/sprites/tomas_neutral.png"
image tomas triste = "images/sprites/tomas_triste.png"


## ----------------------------------------------------------------------------
##  Transformaciones y transiciones
## ----------------------------------------------------------------------------

## La pasajera aparece lentamente y "respira" con un leve parpadeo.
transform fantasma_aparece(x=0.5):
    xalign x
    yalign 1.0
    alpha 0.0
    linear 2.5 alpha 0.92
    block:
        ease 3.0 alpha 0.74 yoffset -6
        ease 3.0 alpha 0.92 yoffset 0
        repeat

## Igual que la anterior, pero sin el fundido de entrada (para cambiar
## de expresión sin que el personaje desaparezca y vuelva a aparecer).
transform fantasma(x=0.5):
    xalign x
    yalign 1.0
    alpha 0.92
    block:
        ease 3.0 alpha 0.74 yoffset -6
        ease 3.0 alpha 0.92 yoffset 0
        repeat

## Sentada en el asiento trasero del taxi.
transform asiento:
    xalign 0.5
    yalign 1.0
    yoffset 90

## Desaparece con la luz del amanecer.
transform desvanecer_lento:
    xalign 0.5
    yalign 1.0
    alpha 0.92
    linear 5.0 alpha 0.0

define flash = Fade(0.08, 0.0, 0.6, color="#ffffff")
define fundido_lento = Dissolve(2.0)
define fundido_muy_lento = Dissolve(3.5)


## ----------------------------------------------------------------------------
##  Sonido
## ----------------------------------------------------------------------------

## Dos canales extra que se repiten en bucle: el ambiente nocturno y el motor.
init python:
    renpy.music.register_channel("ambiente", mixer="sfx", loop=True)
    renpy.music.register_channel("motor", mixer="sfx", loop=True)

define audio.tema_ines = "audio/tema_ines.ogg"
define audio.noche = "audio/noche_copiapo.ogg"
define audio.tension = "audio/tension.ogg"
define audio.amanecer = "audio/amanecer.ogg"
define audio.bolero = "audio/radio_bolero.ogg"

define audio.viento = "audio/viento_noche.ogg"
define audio.motor_taxi = "audio/motor.ogg"
define audio.puerta = "audio/puerta.ogg"
define audio.toc = "audio/toc.ogg"
define audio.tic = "audio/tic.ogg"
define audio.estatica = "audio/estatica.ogg"
define audio.latido = "audio/latido.ogg"
define audio.reja = "audio/reja.ogg"


## ----------------------------------------------------------------------------
##  Estilo de texto (letra con serifa, más "novela gráfica")
## ----------------------------------------------------------------------------

init python:
    config.font_replacement_map["fonts/DejaVuSerif.ttf", False, True] = ("fonts/DejaVuSerif-Italic.ttf", False, False)
    config.font_replacement_map["fonts/DejaVuSerif.ttf", True, False] = ("fonts/DejaVuSerif-Bold.ttf", False, False)

style say_dialogue:
    font "fonts/DejaVuSerif.ttf"

style say_label:
    font "fonts/DejaVuSerif-Bold.ttf"

style nvl_dialogue:
    font "fonts/DejaVuSerif.ttf"

style centered_text:
    font "fonts/DejaVuSerif.ttf"
    color "#e9e2d6"


## ----------------------------------------------------------------------------
##  Fondos del menú principal y de los menús internos
## ----------------------------------------------------------------------------
## gui.rpy ya define estas dos variables apuntando a gui/main_menu.png y
## gui/game_menu.png. Ren'Py vuelve a ejecutar los "define gui..." cada vez
## que aplica el idioma del proyecto, por eso se redefinen aquí con define:
## este archivo se carga después de gui.rpy y su valor es el que queda.
## (El Lint avisará que la variable "ya está definida en gui.rpy": es esperado.)

define gui.main_menu_background = "images/menu/menu_principal.png"
define gui.game_menu_background = "images/menu/menu_juego.png"
