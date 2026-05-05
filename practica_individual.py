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
    "Ana": ["Luis", "Carlos"],
    "Luis": ["Ana", "Marta", "Pedro"],
    "Carlos": ["Ana", "Marta", "Lucia"],
    "Marta": ["Luis", "Carlos", "Elena"],
    "Elena": ["Marta", "Pedro"],
    "Pedro": ["Luis", "Elena", "Lucia"],
    "Lucia": ["Carlos", "Pedro", "Sofia"],
    "Sofia": ["Lucia"]
}
#pedir persona que inicia el rumor
persona_inicial = input("Ingrese el nombre de la persona que inicia el rumor: ")
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
    "Sofia": "Ha empezado a hablar con alguien del grupo en secreto y ya hay teorías"
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

    print("\nPersonas informadas:")
    print(list(informados))

    print("\nTiempo de propagación:")
    print(tiempo, "segundos")