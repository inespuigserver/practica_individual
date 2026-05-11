#objetivo: simular la propagación de un rumor a través de una red social representada con un grafo.
import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from timeit import timeit
from collections import deque

#definición del grafo (red social)
red_social = {
    "Ana": ["Luis", "Carlos", "Julia"],
    "Luis": ["Ana", "Marta", "Raul"],
    "Carlos": ["Ana", "Lucia", "Diego"],
    "Marta": ["Luis", "Elena", "Sara"],
    "Elena": ["Marta", "Pedro"],
    "Pedro": ["Elena", "Hugo"],
    "Lucia": ["Carlos", "Sofia", "Nora"],
    "Sofia": ["Lucia", "Mario"],
    "Julia": ["Ana", "Raul"],
    "Raul": ["Luis", "Julia", "Diego"],
    "Diego": ["Carlos", "Raul", "Nora"],
    "Nora": ["Lucia", "Diego"],
    "Sara": ["Marta", "Hugo"],
    "Hugo": ["Pedro", "Sara"],
    "Mario": ["Sofia"],
    "Claudia": [],
    "Adrian": ["Valeria"],
    "Valeria": ["Adrian"]
}
#pedir persona que inicia el rumor
persona_inicial = input("Ingrese el nombre de la persona que inicia el rumor: ").lower().capitalize()
if persona_inicial not in red_social:
    print("Error: la persona no existe en la red social.")
else:
    #diccionario de rumores creados por cada usuario:
    rumores = {
    "Ana": "Ha rechazado una oferta de trabajo en el extranjero por algo que nadie entiende",
    "Luis": "Está en conversaciones para montar un negocio secreto con alguien del grupo",
    "Carlos": "Dicen que ha copiado en el último examen y el profesor ya sospecha",
    "Marta": "Se va de viaje sin decir a nadie con quién… y eso está dando mucho que hablar",
    "Elena": "Ha encontrado algo raro en el móvil de alguien cercano y no ha dicho nada todavía",
    "Pedro": "Podría dejar la ciudad en cualquier momento sin avisar a nadie",
    "Lucia": "Está organizando una fiesta exclusiva pero no todo el mundo está invitado",
    "Sofia": "Ha empezado a hablar con alguien del grupo en secreto y ya hay teorías",
    "Julia": "Ha recibido un mensaje misterioso y no quiere enseñar de quién es",
    "Raul": "Dicen que sabe un secreto importante de alguien del grupo",
    "Diego": "Está quedando con alguien a escondidas y varios ya lo sospechan",
    "Nora": "Ha borrado todas sus fotos de una red social sin dar explicaciones",
    "Sara": "Podría estar preparando una sorpresa, pero nadie sabe para quién",
    "Hugo": "Le han visto discutiendo con alguien del grupo y no quiere hablar del tema",
    "Mario": "Está fingiendo que no sabe nada, pero parece que está metido en el asunto",
    "Claudia": "Ha desaparecido del grupo durante días y nadie sabe qué le pasa",
    "Adrian": "Ha contado algo a Valeria que no debía salir de ahí",
    "Valeria": "Sabe un secreto de Adrián y podría contarlo en cualquier momento"
}

    # obtener y mostrar el rumor
    mensaje = rumores.get(persona_inicial, "Tiene algo interesante que contar")

    print(f"{persona_inicial} dice: '{mensaje}'")

    #función para simular la propagación del rumor
    def propagacion_bfs(red_social, persona_inicial):
        inicio_tiempo = time.time()

        cola = deque()
        visitados = set()
        orden_propagacion = []
        niveles = {}

        cola.append(persona_inicial)
        visitados.add(persona_inicial)
        niveles[persona_inicial] = 0

        while cola:
            persona = cola.popleft()
            orden_propagacion.append(persona)

            for vecino in red_social[persona]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
                    niveles[vecino] = niveles[persona] + 1

        fin_tiempo = time.time()
        tiempo_total = fin_tiempo - inicio_tiempo

        return orden_propagacion, niveles, tiempo_total, visitados


    orden, niveles, tiempo, informados = propagacion_bfs(red_social, persona_inicial)

    print("\n--- SIMULACIÓN DE PROPAGACIÓN DEL RUMOR ---")
    print("Persona inicial:", persona_inicial)
    print("Rumor:", rumores[persona_inicial])

    print("\nOrden de propagación:")
    print(orden)

    print("\nNiveles de propagación:")
    for persona, nivel in niveles.items():
            print(persona, "-> nivel", nivel)

    # personas informadas
    print("\nPersonas informadas:")
    print(list(informados))

    # personas no informadas
    no_informados = []

    for persona in red_social:
        if persona not in informados:
         no_informados.append(persona)

    print("\nPersonas NO informadas:")
    print(no_informados)

    print("\nTiempo de propagación:")
    print(tiempo, "segundos")

    # representación del grafo por niveles
    G = nx.Graph()

    # añadir conexiones
    for persona, amigos in red_social.items():
        for amigo in amigos:
            G.add_edge(persona, amigo)

    # añadir personas sin conexiones
    for persona in red_social:
        G.add_node(persona)

    # nivel máximo de las personas informadas
    max_nivel = max(niveles.values())

    # crear posiciones ordenadas por niveles
    pos = {}

    niveles_unicos = sorted(set(niveles.values()))

    separacion_horizontal = 3
    separacion_vertical = 3

    # colocar personas informadas por niveles
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

    # colocar personas no informadas aparte
    for i, persona in enumerate(no_informados):

        x = (i - (len(no_informados) - 1) / 2) * separacion_horizontal
        y = -(max_nivel + 2) * separacion_vertical

        pos[persona] = (x, y)

    # límites automáticos
    min_x = min(x for x, y in pos.values())
    max_x = max(x for x, y in pos.values())

    # colores de nodos
    colores = []

    for persona in G.nodes():

        if persona == persona_inicial:
            colores.append("blue")

        elif persona in informados:
            colores.append("green")

        else:
            colores.append("red")

    # crear figura
    plt.figure(figsize=(15, 10))

    # líneas y etiquetas de niveles
    for nivel in niveles_unicos:

        y = -nivel * separacion_vertical

        plt.axhline(
            y=y,
            color="lightgray",
            linestyle="--",
            linewidth=1
        )

        plt.text(
            min_x - 3,
            y,
            f" NIVEL {nivel} ",
            fontsize=11,
            fontweight="bold",
            verticalalignment="center",
            bbox=dict(
                facecolor="white",
                edgecolor="black",
                boxstyle="round,pad=0.3"
            )
        )

    # etiqueta de no informados
    plt.text(
        min_x - 3,
        -(max_nivel + 2) * separacion_vertical,
        " NO INFORMADOS ",
        fontsize=11,
        fontweight="bold",
        verticalalignment="center",
        bbox=dict(
            facecolor="white",
            edgecolor="black",
            boxstyle="round,pad=0.3"
        )
    )

    # dibujar grafo
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colores,
        node_size=2200,
        font_size=9,
        font_weight="bold",
        edge_color="gray",
        width=1.5
    )

    # leyenda
    from matplotlib.patches import Patch

    leyenda = [
        Patch(color='blue', label='Persona inicial'),
        Patch(color='green', label='Informados'),
        Patch(color='red', label='No informados')
    ]

    plt.legend(handles=leyenda, loc="upper left")

    # título
    plt.title(
        "Propagación del rumor en la red social",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlim(min_x - 5, max_x + 3)

    plt.axis("off")

    plt.tight_layout()

    plt.show()