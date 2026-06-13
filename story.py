# -*- coding: utf-8 -*-
import sys
import time

from colors import C
from characters import Warrior
from ui import clear_screen, box_top, box_div, box_bot, box_row, W


def _type_line(text: str, color: str = '', delay: float = 0.021):
    sys.stdout.write(f'║  {color}')
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    sys.stdout.write(f'{C.RESET}' + ' ' * max(0, W - 2 - len(text)) + '║\n')
    sys.stdout.flush()


def _subst(text: str, player) -> str:
    if not player: return text
    arma = 'espada' if isinstance(player, Warrior) else 'baculo magico'
    return (text.replace('[nombre]', player.name)
                .replace('[clase]',  player.CLASS_NAME)
                .replace('[arma]',   arma))


def story_screen(title: str, sections: list, player=None, delay: float = 0.021):
    pages, cur = [], []
    for color, text in sections:
        if color == '' and text == '':
            if cur: pages.append(cur); cur = []
        else:
            cur.append((color, text))
    if cur: pages.append(cur)

    for idx, page in enumerate(pages):
        clear_screen()
        box_top(f'  {title}  ')
        box_row()
        for color, text in page:
            if color == 'div': box_div()
            else: _type_line(_subst(text, player), color, delay)
        box_row()
        box_bot()
        sfx = f'({idx+1}/{len(pages)})' if idx < len(pages) - 1 else ''
        input(f'  {C.DIM}[ ENTER para continuar {sfx}]{C.RESET}')


# ── Textos de historia ────────────────────────────────

_STORY_OPENING = [
    (C.LRED,   'Las llamas de Valhart iluminan la noche como un sol negro.'),
    ('',''),
    (C.WHITE,  'Tu aldea -- que durante generaciones fue un lugar de paz --'),
    (C.WHITE,  'arde. Los gritos de tus vecinos se mezclan con el crujido'),
    (C.WHITE,  'de la madera ardiendo y el rugido de algo antiguo y terrible.'),
    ('',''),
    (C.DIM,    'Hace tres lunas, el Senor del Abismo --MALACHAR-- desperto.'),
    (C.DIM,    'Su aliento corrompio los bosques. Sus garras aplastaron ciudades.'),
    (C.DIM,    'Su magia negra resucito a los muertos para que le sirvieran.'),
    ('',''),
    (C.WHITE,  'Entre el caos, una mano te agarra del brazo.'),
    (C.WHITE,  'El Anciano Thariel. Sus ojos, siempre serenos, ahora arden.'),
    ('',''),
    (C.CYAN,   '  "Escucha. Las estrellas lo dijeron hace veinte anos."'),
    (C.CYAN,   '  "UN heroe. UN camino. Eldoria no puede ser salvada por ejercitos."'),
    ('',''),
    (C.WHITE,  'Te pone tu [arma] en las manos.'),
    ('',''),
    (C.CYAN,   '  "Malachar mora al norte. Bosques, Ruinas, Ciudadela. Y al final... el."'),
    (C.CYAN,   '  "No mires atras, [nombre]. Valhart ya no existe."'),
    (C.CYAN,   '  "Pero Eldoria... Eldoria todavia puede existir."'),
    ('',''),
    (C.DIM,    'Una viga ardiendo cae entre los dos. Cuando el humo se disipa,'),
    (C.DIM,    'Thariel ya no esta. Solo quedan las llamas. Y el camino norte.'),
    ('',''),
    (C.LYELLOW,'Sin mirar atras, te adentras en la oscuridad.'),
]

_ACT_INTROS = {
    1: [
        (C.LGRAY,  'Los Bosques de Grenmoor.'),
        ('',''),
        (C.WHITE,  'Hace dos semanas eran un lugar de belleza salvaje.'),
        (C.WHITE,  'Pajaros de cien colores. Arboles centenarios.'),
        (C.WHITE,  'Un rio de agua tan clara que veias el fondo a tres metros.'),
        ('',''),
        (C.WHITE,  'Ahora los arboles estan retorcidos. El suelo exhala vapor violaceo.'),
        (C.WHITE,  'El rio fluye negro. Y en las sombras...'),
        ('',''),
        (C.LRED,   '                  ...se mueven cosas.'),
        ('',''),
        (C.DIM,    'Aprietas tu [arma]. Y avanzas.'),
    ],
    2: [
        (C.LGRAY,  'Las Ruinas de Valdris.'),
        ('',''),
        (C.WHITE,  'Fue en su dia la ciudad mas grande de Eldoria.'),
        (C.WHITE,  'Torres de cristal. Los magos mas sabios del mundo conocido.'),
        ('',''),
        (C.DIM,    'Ahora no queda nada. Solo piedra negra y el eco'),
        (C.DIM,    'de los que vivieron aqui -- obligados a vagar sin descanso.'),
        ('',''),
        (C.LRED,   'Los muertos no descansan. Y pronto te encontraran.'),
    ],
    3: [
        (C.LGRAY,  'La Ciudadela Oscura.'),
        ('',''),
        (C.WHITE,  'Sus torres rasgan el cielo. Cadenas de cien metros cuelgan'),
        (C.WHITE,  'con criaturas sujetas. Muros de treinta metros de grosor.'),
        ('',''),
        (C.YELLOW, 'Llegaste hasta aqui, [nombre].'),
        (C.YELLOW, 'Atravesaste el bosque. Cruzaste las ruinas. Sobreviviste todo.'),
        ('',''),
        (C.LYELLOW,'Una batalla mas. La ultima. Exhalas. Y entras.'),
    ],
}

_MID_ACT = {
    1: [
        (C.WHITE,  'Entre la maleza, escuchas algo humano. Una tos.'),
        ('',''),
        (C.WHITE,  'Detras de un arbol caido: una mujer joven, herida, con capa de viajera.'),
        (C.WHITE,  'Al verte, su mano va instintivamente a un cuchillo.'),
        ('',''),
        (C.CYAN,   '  "Espera -- no soy una de esas cosas."'),
        ('',''),
        (C.CYAN,   '  "Soy Lyra. Exploradora del Rey. O lo era, antes de que"'),
        (C.CYAN,   '   el Rey ya no existiera. Llevo dias aqui."'),
        ('',''),
        (C.CYAN,   '  "Si vas al norte... la magia de Malachar se alimenta del miedo.'),
        (C.CYAN,   '   Si no tienes miedo... su poder sobre ti disminuye."'),
        ('',''),
        (C.DIM,    'Se pierde entre los arboles. Tu sigues hacia el norte.'),
    ],
    2: [
        (C.WHITE,  'Entre las ruinas de una torre, una figura aparece. Semi-transparente.'),
        ('',''),
        (C.WHITE,  'Un hombre anciano. Ojos blancos y puros. Un fantasma con paz.'),
        ('',''),
        (C.CYAN,   '  "Fui el Gran Archimago de Valdris. Malachar me mato hace dos semanas."'),
        (C.CYAN,   '  "Pero me niego a servir a ese monstruo."'),
        ('',''),
        (C.CYAN,   '  "La Ciudadela tiene una camara interior. El corazon de Malachar late ahi."'),
        (C.CYAN,   '  "Cuando llegues a el... usa todo lo que tienes. Sin reservas."'),
        ('',''),
        (C.DIM,    'La figura desaparece. Solo quedan las ruinas y el silencio.'),
    ],
    3: [
        (C.WHITE,  'En un calabozo, una voz debil te llama por tu nombre.'),
        ('',''),
        (C.WHITE,  'El General Aldric. Capturado hace una semana. Flaco pero con ojos encendidos.'),
        ('',''),
        (C.CYAN,   '  "Eres real. Gracias a los dioses, eres real."'),
        ('',''),
        (C.CYAN,   '  "Malachar puede hablar. Intentara convencerte de rendirte."'),
        (C.CYAN,   '  "NADA de lo que diga es verdad. No lo escuches."'),
        ('',''),
        (C.WHITE,  'Te da una pocion. Te estrecha la mano.'),
        ('',''),
        (C.CYAN,   '  "Vence por todos nosotros, [nombre]."'),
    ],
}

_ACT_OUTROS = {
    1: [
        (C.WHITE,  'Al salir del bosque encuentras a un guardia real tendido en el suelo.'),
        (C.WHITE,  'Una flecha negra en su costado. Todavia vivo. Por poco.'),
        ('',''),
        (C.CYAN,   '  "Tu... lograste cruzar el bosque solo."'),
        (C.CYAN,   '  "Las Ruinas de Valdris. Al norte. Los muertos caminan."'),
        (C.CYAN,   '  "Dile a mi familia... que mori bien."'),
        ('',''),
        (C.DIM,    'Cierra los ojos. Una ultima respiracion.'),
        ('',''),
        (C.LYELLOW,'Miras al norte. Las Ruinas aguardan.'),
    ],
    2: [
        (C.WHITE,  'Una anciana emerge de detras de un muro. Lampara de aceite en la mano.'),
        ('',''),
        (C.CYAN,   '  "Por los dioses... ALGUIEN LLEGO. ALGUIEN LLEGO."'),
        ('',''),
        (C.CYAN,   '  "Soy Marta, la bibliotecaria de Valdris. Llevo dos semanas escondida."'),
        (C.CYAN,   '  "Vi como mataban a todos. Vi como los muertos se levantaban."'),
        ('',''),
        (C.CYAN,   '  "Pero nunca... nunca perdi la esperanza."'),
        (C.CYAN,   '  "Llegaste hasta aqui, [nombre]. TU LLEGASTE."'),
        ('',''),
        (C.WHITE,  'Te da una pocion. La ultima que le quedaba.'),
        ('',''),
        (C.LYELLOW,'La Ciudadela Oscura corta el cielo al frente.'),
    ],
    3: [
        (C.WHITE,  'El ultimo guardian cae. El silencio es total.'),
        ('',''),
        (C.WHITE,  'Frente a ti: una puerta de obsidiana de cinco metros.'),
        (C.WHITE,  'Sin manija. Sin cerrojo. Empieza a abrirse sola.'),
        ('',''),
        (C.LRED,   'El calor que sale es insoportable. Olor a azufre.'),
        ('',''),
        (C.WHITE,  'Y desde las profundidades, una respiracion.'),
        (C.WHITE,  'Lenta. Profunda. Como truenos encadenados.'),
        ('',''),
        (C.RED,    '                  MALACHAR te espera.'),
    ],
}

_BOSS_INTRO = [
    (C.LGRAY,  'La camara es mas grande que cualquier sala que hayas visto.'),
    (C.LGRAY,  'El techo desaparece en la oscuridad arriba.'),
    ('',''),
    (C.WHITE,  'Y entonces... dos ojos se abren en la penumbra.'),
    ('',''),
    (C.LRED,   'Como soles incandescentes. Rojos. Antiguos. Hambrientos.'),
    ('',''),
    (C.WHITE,  'Una figura colosal se levanta. Despliega alas negras que bloquean la luz.'),
    (C.WHITE,  'Su cuerpo: armadura de escamas rojas con fuego interior.'),
    ('',''),
    (C.RED,    '  "...Un [clase]."'),
    ('',''),
    (C.RED,    '  "Eldoria me envia un [clase]. Llamado [nombre]."'),
    ('',''),
    (C.RED,    '  "Mate a reyes. Destrui ejercitos. Aplaste a los magos de Valdris."'),
    (C.RED,    '  "Y me envian a UN [clase]."'),
    ('',''),
    (C.WHITE,  'Abre las fauces. El fuego ilumina la camara de rojo sangriento.'),
    ('',''),
    (C.RED,    '  "Al menos tendre el honor de borrarte del mundo yo mismo."'),
    ('',''),
    (C.LYELLOW,'Empunas tu [arma]. No tienes miedo. Ya no importa si lo tienes.'),
]

_STORY_ENDING = [
    (C.WHITE,  'Malachar cae.'),
    ('',''),
    (C.WHITE,  'El impacto sacude la montana. Las cadenas de su maldicion se rompen'),
    (C.WHITE,  'con un sonido que sientes hasta en los huesos.'),
    ('',''),
    (C.LGRAY,  'El dragon te mira desde el suelo. Sus ojos ya no son brasas.'),
    (C.LGRAY,  'Solo un cansancio que trasciende los siglos.'),
    ('',''),
    (C.RED,    '  "Imposible..."'),
    ('',''),
    (C.RED,    '  "Cien anos de poder. Y un [clase] llamado [nombre]..."'),
    ('',''),
    (C.LGRAY,  'Sus escamas pierden el brillo carmesi, una a una. Como hojas en otono.'),
    ('',''),
    (C.RED,    '  "Eldoria... sobrevivira... despues de todo..."'),
    ('',''),
    (C.LGRAY,  'Y cierra los ojos para siempre.'),
    ('',''),
    (C.WHITE,  'Afuera, el cielo negro de Malachar comienza a disolverse.'),
    (C.WHITE,  'La luz del sol -- que no se habia visto en semanas -- rompe las nubes.'),
    ('',''),
    (C.WHITE,  'En Eldoria, la gente sale a las calles mirando al cielo con lagrimas.'),
    (C.WHITE,  'En Valdris, los muertos dejan de moverse. Uno a uno. Y caen.'),
    (C.WHITE,  'Esta vez para siempre. Esta vez con paz.'),
    ('',''),
    (C.YELLOW, 'Nadie sabe todavia tu nombre.'),
    (C.YELLOW, 'Nadie sabe lo que hiciste hoy.'),
    ('',''),
    (C.LYELLOW,'Pero muy pronto... todos lo sabran.'),
    ('',''),
    (C.BRIGHT, '                    F I N'),
]

_BETWEEN_BATTLE = {
    1: ['Te limpias el [arma]. El bosque continua.',
        'Dos menos. El corazon del bosque aun aguarda.',
        'Casi al otro lado. Solo queda uno mas.',
        'El bosque queda atras. Lo lograste.'],
    2: ['Los muertos no cesan. Pero su numero merma.',
        'Las ruinas se abren paso entre las sombras.',
        'Casi al otro lado. La Ciudadela es visible.',
        'El ultimo obstaculo de Valdris cae. Respiras.'],
    3: ['Un guardian menos. Las antorchas tiemblan.',
        'Los pasillos se hacen mas oscuros.',
        'La resistencia es feroz. Pero no suficiente.',
        'El camino a la camara de Malachar esta casi despejado.'],
}
