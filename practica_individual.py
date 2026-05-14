import time
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Patch
from collections import deque


personas = [
    "Ana", "Luis", "Carlos", "Marta", "Elena", "Pedro",
    "Lucia", "Sofia", "Julia", "Raul", "Diego", "Nora",
    "Sara", "Hugo", "Mario", "Claudia", "Adrian", "Valeria"
]

rumores = {
    "Ana": "Luis le propuso montar un negocio secreto con Marta.",
    "Luis": "Ana ha rechazado una oferta de trabajo porque Marta le ofreció entrar en un proyecto oculto.",
    "Carlos": "Julia dice que Raúl tiene pruebas de algo que pasó en el último examen.",
    "Marta": "Elena cree que Pedro se va de viaje con alguien del grupo.",
    "Elena": "Pedro tenía algo raro en el móvil y Sofía ya lo sabe.",
    "Pedro": "Hugo descubrió algo que podría hacer que alguien se vaya de la ciudad.",
    "Lucia": "Nora dice que Ana y Mario no están invitados a una fiesta exclusiva.",
    "Sofia": "Diego y Julia están ocultando algo que Lucía ya sospecha.",
    "Julia": "Raúl ha recibido un mensaje misterioso y Carlos cree que Diego sabe quién lo envió.",
    "Raul": "Carlos y Nora esconden un secreto que Julia ya conoce.",
    "Diego": "Sofía está quedando con alguien a escondidas y Valeria también lo sabe.",
    "Nora": "Lucía y Diego tuvieron una discusión que acabó con varias fotos borradas.",
    "Sara": "Marta cree que Elena ya se ha enterado de una sorpresa preparada para Hugo.",
    "Hugo": "Pedro se enfadó porque Sara contó algo que no debía.",
    "Mario": "Lucía está organizando algo y Julia ha recibido un mensaje relacionado.",
    "Claudia": "Valeria dice que la última persona que habló con Adrián fue alguien del grupo.",
    "Adrian": "Valeria sabe un secreto sobre Claudia que no debía salir del grupo.",
    "Valeria": "Nora cree que el secreto de Adrián también afecta a Claudia."
}


def crear_red_social_aleatoria(personas):

    red_social = {}

    for persona in personas:
        red_social[persona] = []

    # red base: casi todos conectados, pero no todos
    relaciones_posibles = {
        "Ana": ["Luis", "Carlos", "Julia", "Marta"],
        "Luis": ["Ana", "Marta", "Raul", "Carlos", "Elena"],
        "Carlos": ["Ana", "Luis", "Lucia", "Diego", "Raul"],
        "Marta": ["Ana", "Luis", "Elena", "Sara", "Julia"],
        "Elena": ["Marta", "Pedro", "Sofia", "Sara", "Luis"],
        "Pedro": ["Elena", "Hugo", "Marta", "Sara"],
        "Lucia": ["Carlos", "Sofia", "Nora", "Mario", "Diego"],
        "Sofia": ["Lucia", "Elena", "Diego", "Mario", "Nora"],
        "Julia": ["Ana", "Raul", "Diego", "Valeria", "Marta"],
        "Raul": ["Luis", "Carlos", "Julia", "Diego"],
        "Diego": ["Carlos", "Raul", "Sofia", "Julia", "Nora"],
        "Nora": ["Lucia", "Diego", "Valeria", "Sofia"],
        "Sara": ["Marta", "Elena", "Hugo", "Pedro"],
        "Hugo": ["Pedro", "Sara", "Claudia"],
        "Mario": ["Lucia", "Sofia", "Valeria"],
        "Claudia": ["Hugo", "Adrian", "Valeria"],
        "Adrian": ["Claudia", "Valeria", "Hugo"],
        "Valeria": ["Adrian", "Claudia", "Julia", "Nora", "Mario"]
    }

    for persona in relaciones_posibles:

        amigos_posibles = relaciones_posibles[persona]

        numero_amigos = random.randint(2, min(4, len(amigos_posibles)))

        amigos = random.sample(amigos_posibles, numero_amigos)

        for amigo in amigos:

            if amigo not in red_social[persona]:
                red_social[persona].append(amigo)

            if persona not in red_social[amigo]:
                red_social[amigo].append(persona)

    # se eligen 2 o 3 personas que no se enterarán
    posibles_no_informados = personas.copy()

    if persona_inicial in posibles_no_informados:
        posibles_no_informados.remove(persona_inicial)

    numero_no_informados = random.randint(2, 3)

    personas_fuera = random.sample(posibles_no_informados, numero_no_informados)

    # se desconectan esas personas del resto
    for persona_fuera in personas_fuera:

        red_social[persona_fuera] = []

        for persona in red_social:

            if persona_fuera in red_social[persona]:
                red_social[persona].remove(persona_fuera)

    return red_social


def convertir_tiempo(minutos):
    if minutos < 60:
        return str(minutos) + " min"
    elif minutos < 1440:
        horas = minutos // 60
        minutos_restantes = minutos % 60
        return str(horas) + " h " + str(minutos_restantes) + " min"
    else:
        dias = minutos // 1440
        horas_restantes = (minutos % 1440) // 60
        return str(dias) + " días " + str(horas_restantes) + " h"


def propagacion_bfs(red_social, persona_inicial):
    inicio_real = time.time()

    tipos_usuario = {
        "Ana": "rapido", "Luis": "rapido", "Carlos": "normal",
        "Marta": "normal", "Elena": "lento", "Pedro": "lento",
        "Lucia": "rapido", "Sofia": "normal", "Julia": "rapido",
        "Raul": "normal", "Diego": "lento", "Nora": "normal",
        "Sara": "rapido", "Hugo": "lento", "Mario": "normal",
        "Claudia": "no_comparte", "Adrian": "lento", "Valeria": "rapido"
    }

    cola = deque()
    visitados = set()
    orden_propagacion = []
    niveles = {}
    tiempos_llegada = {}

    cola.append(persona_inicial)
    visitados.add(persona_inicial)

    niveles[persona_inicial] = 0
    tiempos_llegada[persona_inicial] = 0

    while cola:
        persona = cola.popleft()
        orden_propagacion.append(persona)

        if tipos_usuario[persona] == "no_comparte":
            continue

        for vecino in red_social[persona]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

                niveles[vecino] = niveles[persona] + 1

                tipo = tipos_usuario[persona]

                if tipo == "rapido":
                    retraso_base = random.randint(5, 60)
                elif tipo == "normal":
                    retraso_base = random.randint(60, 360)
                elif tipo == "lento":
                    retraso_base = random.randint(360, 1440)
                else:
                    retraso_base = random.randint(1440, 2880)

                nivel_vecino = niveles[vecino]

                retraso_por_nivel = nivel_vecino * random.randint(30, 180)

                retraso_total = retraso_base + retraso_por_nivel

                tiempos_llegada[vecino] = tiempos_llegada[persona] + retraso_total

    fin_real = time.time()
    tiempo_ejecucion = fin_real - inicio_real
    tiempo_total_simulado = max(tiempos_llegada.values())

    return orden_propagacion, niveles, tiempos_llegada, tiempo_total_simulado, tiempo_ejecucion, visitados
persona_inicial = None


def elegir_persona_graficamente():

    global persona_inicial

    fig = plt.figure(figsize=(13, 8))

    # color de fondo tipo red social
    fig.patch.set_facecolor("#f0f2f5")

    ax = plt.axes([0, 0, 1, 1])

    ax.set_facecolor("#f0f2f5")

    ax.axis("off")

    # -----------------------------
    # TÍTULO ESTILO RED SOCIAL
    # -----------------------------

    plt.text(
        0.5,
        0.93,
        "LinkUp",
        fontsize=30,
        fontweight="bold",
        color="#1877f2",
        ha="center"
    )

    plt.text(
        0.5,
        0.88,
        "¿Quién inicia el rumor?",
        fontsize=18,
        fontweight="bold",
        color="black",
        ha="center"
    )

    plt.text(
        0.5,
        0.84,
        "Selecciona un perfil de la red social",
        fontsize=11,
        color="gray",
        ha="center"
    )

    botones = []

    # -----------------------------
    # DISTRIBUCIÓN DE PERFILES
    # -----------------------------

    columnas = 3

    ancho = 0.22
    alto = 0.09

    espacio_x = 0.26
    espacio_y = 0.11

    x_inicial = 0.12
    y_inicial = 0.70

    # -----------------------------
    # FUNCIÓN SELECCIÓN
    # -----------------------------

    def seleccionar(nombre):

        def funcion(event):

            global persona_inicial

            persona_inicial = nombre

            plt.close(fig)

        return funcion

    # -----------------------------
    # CREAR BOTONES
    # -----------------------------

    for i, persona in enumerate(personas):

        fila = i // columnas

        columna = i % columnas

        x = x_inicial + columna * espacio_x

        y = y_inicial - fila * espacio_y

        # fondo tipo tarjeta
        tarjeta = plt.Rectangle(
            (x - 0.01, y - 0.01),
            ancho + 0.02,
            alto + 0.02,
            facecolor="white",
            edgecolor="#d3d6db",
            linewidth=1.5,
            zorder=0
        )

        ax.add_patch(tarjeta)

        ax_boton = plt.axes([x, y, ancho, alto])

        boton = Button(ax_boton, f"👤  {persona}")

        # colores tipo app
        boton.color = "#ffffff"
        boton.hovercolor = "#dbe7ff"

        boton.label.set_fontsize(11)
        boton.label.set_fontweight("bold")
        boton.label.set_color("#1c1e21")

        boton.on_clicked(seleccionar(persona))

        botones.append(boton)

    fig.botones = botones

    plt.show()


# variables globales de la simulación
red_social = None
G = None
niveles = None
tiempos_llegada = None
informados = None
no_informados = None
pos = None
nivel_actual = 0
max_nivel = 0
boton_siguiente = None


def preparar_simulacion():
    global red_social, G, niveles, tiempos_llegada
    global informados, no_informados, pos, max_nivel

    red_social = crear_red_social_aleatoria(personas)

    orden, niveles, tiempos_llegada, tiempo_total, tiempo_ejecucion, informados = propagacion_bfs(
        red_social,
        persona_inicial
    )

    no_informados = []

    for persona in red_social:
        if persona not in informados:
            no_informados.append(persona)

    G = nx.Graph()

    for persona, amigos in red_social.items():
        G.add_node(persona)

        for amigo in amigos:
            G.add_edge(persona, amigo)

    max_nivel = max(niveles.values())

    pos = {}

    separacion_horizontal = 3
    separacion_vertical = 3

    niveles_unicos = sorted(set(niveles.values()))

    for nivel in niveles_unicos:
        personas_nivel = []

        for persona in niveles:
            if niveles[persona] == nivel:
                personas_nivel.append(persona)

        cantidad = len(personas_nivel)

        for i, persona in enumerate(personas_nivel):
            x = (i - (cantidad - 1) / 2) * separacion_horizontal
            y = -nivel * separacion_vertical
            pos[persona] = (x, y)

    for i, persona in enumerate(no_informados):
        x = (i - (len(no_informados) - 1) / 2) * separacion_horizontal
        y = -(max_nivel + 2) * separacion_vertical
        pos[persona] = (x, y)

    print("\n------------------------------------")
    print("SIMULACIÓN PREPARADA")
    print("------------------------------------")
    print("Persona inicial:", persona_inicial)
    print("Rumor:", rumores[persona_inicial])

    print("\nNIVELES Y TIEMPOS:")
    for persona in niveles:
        print(
            persona,
            "-> nivel",
            niveles[persona],
            "-> llega en",
            convertir_tiempo(tiempos_llegada[persona])
        )

    print("\nPersonas no informadas:")
    print(no_informados)

    print("\nDuración total:", convertir_tiempo(tiempo_total))
    print("Tiempo real de ejecución:", round(tiempo_ejecucion, 5), "segundos")


def dibujar_hasta_nivel(nivel_mostrado):
    plt.clf()

    nodos_visibles = []

    for persona in niveles:
        if niveles[persona] <= nivel_mostrado:
            nodos_visibles.append(persona)

    if nivel_mostrado > max_nivel:
        for persona in no_informados:
            nodos_visibles.append(persona)

    aristas_visibles = []

    for arista in G.edges():
        persona1 = arista[0]
        persona2 = arista[1]

        if persona1 in nodos_visibles and persona2 in nodos_visibles:
            aristas_visibles.append(arista)

    G_visible = nx.Graph()
    G_visible.add_nodes_from(nodos_visibles)
    G_visible.add_edges_from(aristas_visibles)

    colores = []

    for persona in G_visible.nodes():
        if persona == persona_inicial:
            colores.append("blue")
        elif persona in informados:
            colores.append("green")
        else:
            colores.append("red")

    etiquetas = {}

    for persona in G_visible.nodes():
        if persona in tiempos_llegada:
            etiquetas[persona] = (
                f"{persona}\n"
                f"{convertir_tiempo(tiempos_llegada[persona])}"
            )
        else:
            etiquetas[persona] = f"{persona}\nNO"

    min_x = min(x for x, y in pos.values())
    max_x = max(x for x, y in pos.values())

    separacion_vertical = 3

    for nivel in range(0, min(nivel_mostrado, max_nivel) + 1):
        y = -nivel * separacion_vertical

        plt.axhline(
            y=y,
            color="lightgray",
            linestyle="--",
            linewidth=1
        )

        plt.text(
            min_x - 4,
            y,
            f"NIVEL {nivel}",
            fontsize=10,
            fontweight="bold",
            verticalalignment="center",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
        )

    if nivel_mostrado > max_nivel and no_informados:
        plt.text(
            min_x - 4,
            -(max_nivel + 2) * separacion_vertical,
            "NO INFORMADOS",
            fontsize=10,
            fontweight="bold",
            verticalalignment="center",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
        )

    nx.draw(
        G_visible,
        pos,
        labels=etiquetas,
        node_color=colores,
        node_size=2800,
        font_size=8,
        font_weight="bold",
        edge_color="gray",
        width=1.5
    )

    leyenda = [
        Patch(color="blue", label="Persona inicial"),
        Patch(color="green", label="Informados"),
        Patch(color="red", label="No informados")
    ]

    plt.legend(handles=leyenda, loc="upper left")

    if nivel_mostrado <= max_nivel:
        texto_nivel = f"Mostrando hasta el nivel {nivel_mostrado}"
    else:
        texto_nivel = "Simulación completa"

    plt.title(
        f"Propagación del rumor\n"
        f"Inicio: {persona_inicial} | {texto_nivel}",
        fontsize=15,
        fontweight="bold"
    )

    plt.figtext(
        0.5,
        0.02,
        f"Rumor: {rumores[persona_inicial]}",
        ha="center",
        fontsize=10,
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.5")
    )

    plt.xlim(min_x - 5, max_x + 5)
    plt.axis("off")

    ax_boton = plt.axes([0.78, 0.90, 0.18, 0.06])

    if nivel_mostrado <= max_nivel:
        texto_boton = "Siguiente nivel"
    else:
        texto_boton = "Fin"

    global boton_siguiente
    boton_siguiente = Button(ax_boton, texto_boton)
    boton_siguiente.on_clicked(siguiente_nivel)

    plt.gcf().boton_siguiente = boton_siguiente

    plt.draw()


def siguiente_nivel(event):
    global nivel_actual

    if nivel_actual <= max_nivel:
        nivel_actual = nivel_actual + 1
        dibujar_hasta_nivel(nivel_actual)


#simulación
elegir_persona_graficamente()

preparar_simulacion()

fig = plt.figure(figsize=(15, 10))

dibujar_hasta_nivel(0)

plt.show()