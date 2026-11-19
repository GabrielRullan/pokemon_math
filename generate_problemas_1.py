# -*- coding: utf-8 -*-
"""
Generador del banco completo de 120 problemas matemáticos Pokémon para 1º de Primaria (LOMLOE):
- 100 problemas principales (1 al 100) distribuidos en las 7 subcategorías canónicas.
- 20 Retos Especiales (101 al 120).
- 120 soluciones razonadas en Parte 2 con Datos identificados, Planteamiento y Operaciones, y Respuesta Final.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Dict, List


SUBCAT_1 = "Subcategoría 1: Numeración, Descomposición y Valor Posicional"
SUBCAT_2 = "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental"
SUBCAT_3 = "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero"
SUBCAT_4 = "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio"
SUBCAT_5 = "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional"
SUBCAT_6 = "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad"
SUBCAT_7 = "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)"

SENSE_NUM = "Sentido Numérico"
SENSE_MED = "Sentido de la Medida"
SENSE_ESP = "Sentido Espacial"
SENSE_ALG = "Sentido Algebraico"
SENSE_EST = "Sentido Estocástico"


PROBLEMS: List[Dict[str, str | int]] = [
    # =========================================================================
    # Subcategoría 1: Numeración, Descomposición y Valor Posicional (1 al 15)
    # =========================================================================
    {
        "id": 1,
        "title": "El número de Pikachu en la Pokédex",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "El Profesor Oak entrega a Ash una Pokédex nueva en el laboratorio de Pueblo Paleta. "
            "Al enfocar a Pikachu, la pantalla muestra que ocupa el número 25."
        ),
        "question": "¿Cuántas decenas y cuántas unidades forman el número 25 de Pikachu?",
        "datos": "Número de Pikachu en la Pokédex: 25.",
        "operaciones": (
            "Separamos el número 25 en decenas y unidades:\n"
            "- La cifra de la izquierda (2) son las decenas: 2 decenas = 20 unidades.\n"
            "- La cifra de la derecha (5) son las unidades: 5 unidades.\n"
            "Así: 25 = 20 + 5."
        ),
        "respuesta": "El número 25 está formado por **2 decenas y 5 unidades**.",
    },
    {
        "id": 2,
        "title": "Los Caterpie del Bosque Verde",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Durante su paseo por el Bosque Verde, Ash y Pikachu cuentan con mucha calma todos los Caterpie "
            "que descansan sobre las hojas de los árboles. En total anotan 47 Caterpie."
        ),
        "question": "Descompón el número 47 en decenas y unidades y escribe la suma de sus valores.",
        "datos": "Cantidad de Caterpie contados: 47.",
        "operaciones": (
            "Observamos las dos cifras del número 47:\n"
            "- El 4 está en las decenas: 4 decenas = 40 unidades.\n"
            "- El 7 está en las unidades: 7 unidades.\n"
            "Descomposición en suma: 40 + 7 = 47."
        ),
        "respuesta": "El número 47 tiene **4 decenas y 7 unidades** (40 + 7 = **47 unidades**).",
    },
    {
        "id": 3,
        "title": "Las Bayas Aranja de Brock",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Brock ordena su mochila antes de salir de excursión y cuenta exactamente 59 Bayas Aranja "
            "para dar energía a sus Pokémon."
        ),
        "question": "¿Cuál es el número anterior y cuál es el número posterior a 59?",
        "datos": "Bayas Aranja en la mochila: 59.",
        "operaciones": (
            "Para hallar el número anterior restamos 1 y para hallar el posterior sumamos 1:\n"
            "- Número anterior: 59 - 1 = 58.\n"
            "- Número posterior: 59 + 1 = 60."
        ),
        "respuesta": "El número anterior es **58 bayas** y el número posterior es **60 bayas**.",
    },
    {
        "id": 4,
        "title": "La báscula del Gimnasio Plateada: ¿quién pesa más?",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Brock pesa a cuatro Pokémon amigos en la báscula del gimnasio: Pikachu pesa 6 kg, "
            "Growlithe pesa 19 kg, Geodude pesa 20 kg y Ponyta pesa 30 kg."
        ),
        "question": "Ordena los cuatro pesos de menor a mayor usando el signo < (menor que).",
        "datos": "Pesos: Pikachu 6 kg, Growlithe 19 kg, Geodude 20 kg y Ponyta 30 kg.",
        "operaciones": (
            "Comparamos las decenas de cada peso:\n"
            "- 6 tiene 0 decenas (es el menor).\n"
            "- 19 tiene 1 decena.\n"
            "- 20 tiene 2 decenas.\n"
            "- 30 tiene 3 decenas (es el mayor).\n"
            "Orden de menor a mayor: 6 < 19 < 20 < 30."
        ),
        "respuesta": "El orden de menor a mayor es **6 kg < 19 kg < 20 kg < 30 kg**.",
    },
    {
        "id": 5,
        "title": "Las cajas de Poké Balls de Gary",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Gary guarda en su estantería 8 cajas con 10 Poké Balls en cada caja, lo que hace un total "
            "de 80 Poké Balls listas para entrenar."
        ),
        "question": "¿Cuántas decenas y cuántas unidades tiene el número 80? ¿Qué indica la cifra 0?",
        "datos": "Total de Poké Balls de Gary: 80.",
        "operaciones": (
            "Analizamos las dos cifras de 80:\n"
            "- La cifra 8 está en las decenas: 8 decenas = 80 unidades.\n"
            "- La cifra 0 está en las unidades: indica que hay 0 unidades sueltas."
        ),
        "respuesta": "El número 80 tiene **8 decenas y 0 unidades**; el 0 indica que hay **0 unidades** sueltas.",
    },
    {
        "id": 6,
        "title": "La carrera de Ponyta en la pradera",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "En una divertida carrera de 10 Pokémon veloces, el Ponyta de Ash cruza la meta justo detrás "
            "del corredor que llegó en 4º lugar (cuarto puesto)."
        ),
        "question": "¿En qué lugar ordinal llegó a la meta el Ponyta de Ash?",
        "datos": "Puesto del corredor anterior: 4º lugar (cuarto).",
        "operaciones": (
            "Contamos los números ordinales en orden: 1º (primero), 2º (segundo), 3º (tercero), "
            "4º (cuarto), 5º (quinto). El puesto que va justo después del 4º es el 5º."
        ),
        "respuesta": "Ponyta llegó a la meta en **5º lugar** (quinto puesto).",
    },
    {
        "id": 7,
        "title": "Las cestas pares e impares de Bulbasaur",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Bulbasaur recoge bayas del bosque y coloca distintas cantidades en cinco cestas: "
            "12, 25, 38, 41 y 54 bayas."
        ),
        "question": "Clasifica cada uno de estos cinco números indicando cuáles son pares y cuáles son impares.",
        "datos": "Cantidades en las cestas: 12, 25, 38, 41 y 54.",
        "operaciones": (
            "Miramos la última cifra de cada número (las unidades):\n"
            "- Los números que terminan en 0, 2, 4, 6 u 8 son pares: 12 (termina en 2), 38 (en 8) y 54 (en 4).\n"
            "- Los números que terminan en 1, 3, 5, 7 o 9 son impares: 25 (termina en 5) y 41 (en 1)."
        ),
        "respuesta": "Los números pares son **12, 38 y 54** (**3 pares**), y los impares son **25 y 41** (**2 impares**).",
    },
    {
        "id": 8,
        "title": "Ordenando cartas Pokémon de Ritchie",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Ritchie colecciona cartas de combate con estos puntos escritos en la esquina: "
            "64, 46, 82 y 28 puntos."
        ),
        "question": "Ordena los cuatro números de menor a mayor utilizando el símbolo < (menor que).",
        "datos": "Puntuaciones de las cartas: 64, 46, 82 y 28.",
        "operaciones": (
            "Comparamos las decenas de cada número: 2 decenas (28) < 4 decenas (46) < 6 decenas (64) < 8 decenas (82).\n"
            "Escribimos la cadena ordenada: 28 < 46 < 64 < 82."
        ),
        "respuesta": "El orden de menor a mayor es **28 < 46 < 64 < 82** (**4 números**).",
    },
    {
        "id": 9,
        "title": "Las monedas brillantes de Meowth",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Meowth encuentra una bolsa con 73 monedas brillantes escondida debajo de un árbol "
            "y las cuenta muy contento."
        ),
        "question": "¿Cuál es el valor de la cifra 7 en el número 73 y cuántas unidades representa?",
        "datos": "Número total de monedas: 73.",
        "operaciones": (
            "Identificamos el lugar de cada cifra en 73:\n"
            "- El 3 ocupa las unidades y vale 3 unidades.\n"
            "- El 7 ocupa las decenas: 7 decenas = 70 unidades."
        ),
        "respuesta": "La cifra 7 ocupa las decenas y representa **70 unidades** (**7 decenas**).",
    },
    {
        "id": 10,
        "title": "El candado secreto del Profesor Oak",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "El maletín del Profesor Oak se abre con un código de 2 cifras. En una nota escribió esta pista: "
            "«El código tiene 6 decenas y 4 unidades»."
        ),
        "question": "¿Cuál es el número de 2 cifras que abre el maletín del Profesor Oak?",
        "datos": "Pista: 6 decenas y 4 unidades.",
        "operaciones": (
            "Convertimos las decenas en unidades y sumamos las unidades sueltas:\n"
            "- 6 decenas = 60 unidades.\n"
            "- 4 unidades = 4.\n"
            "Sumamos: 60 + 4 = 64."
        ),
        "respuesta": "El código que abre el maletín es el número **64** (**64 unidades**).",
    },
    {
        "id": 11,
        "title": "Las dos cartas de los Unown",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "En las Ruinas Alfa, dos Unown muestran dos cartas con las cifras 3 y 8. "
            "Debes usar las dos cartas una sola vez para formar números de 2 cifras."
        ),
        "question": "¿Cuál es el número más grande y cuál es el número más pequeño de 2 cifras que puedes formar con 3 y 8?",
        "datos": "Cifras disponibles: 3 y 8.",
        "operaciones": (
            "Con las cifras 3 y 8 podemos formar dos números de 2 cifras:\n"
            "- Ponemos el 8 en las decenas para lograr el mayor: 83.\n"
            "- Ponemos el 3 en las decenas para lograr el menor: 38."
        ),
        "respuesta": "El número mayor es **83** y el número menor es **38** (**2 números** posibles).",
    },
    {
        "id": 12,
        "title": "La fila del Centro Pokémon",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Diez entrenadores hacen fila en el Centro Pokémon para revisar a sus compañeros. "
            "La Enfermera Joy acaba de atender al 7º entrenador (séptimo)."
        ),
        "question": "¿Qué puesto ordinal ocupa el siguiente entrenador que va a entrar y quién va justo detrás de él?",
        "datos": "Último entrenador atendido: 7º (séptimo); total en la fila: 10.",
        "operaciones": (
            "Seguimos el orden de los números ordinales del 1º al 10º:\n"
            "- Después del 7º (séptimo) va el 8º (octavo).\n"
            "- Justo detrás del 8º va el 9º (noveno)."
        ),
        "respuesta": "El siguiente ocupa el **8º puesto** (octavo) y detrás va el **9º puesto** (noveno).",
    },
    {
        "id": 13,
        "title": "Comparando las bayas de Ash y Misty",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Al volver del bosque, Ash cuenta 57 bayas en su cesta y Misty cuenta 75 bayas en la suya."
        ),
        "question": "Compara 57 y 75 con el signo > o < y di quién recogió más bayas.",
        "datos": "Bayas de Ash: 57; bayas de Misty: 75.",
        "operaciones": (
            "Comparamos las decenas de ambos números:\n"
            "- 75 tiene 7 decenas y 57 tiene 5 decenas.\n"
            "- Como 7 decenas es mayor que 5 decenas, 75 > 57 (o 57 < 75)."
        ),
        "respuesta": "La comparación es **75 > 57**; recogió más **Misty** con **75 bayas**.",
    },
    {
        "id": 14,
        "title": "Los cromos del álbum de Ash",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "Ash pega con cuidado sus cromos de Pokémon en un álbum nuevo y ya ha reunido 68 cromos."
        ),
        "question": "Escribe con palabras cómo se lee el número 68 y descompónlo en decenas y unidades.",
        "datos": "Cantidad de cromos en el álbum: 68.",
        "operaciones": (
            "1. Lectura en palabras: 68 se lee «sesenta y ocho».\n"
            "2. Descomposición: 6 decenas (60) + 8 unidades (8) = 68."
        ),
        "respuesta": "Se lee **sesenta y ocho** y tiene **6 decenas y 8 unidades** (60 + 8 = **68 unidades**).",
    },
    {
        "id": 15,
        "title": "Entradas pares para el concierto de Jigglypuff",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "En la puerta del escenario reparten entradas con estos números: 19, 24, 30, 47 y 86. "
            "Solo las entradas con número par pasan a la primera fila."
        ),
        "question": "¿Cuáles de estos cinco números de entrada son pares y pasan a la primera fila?",
        "datos": "Números de entrada: 19, 24, 30, 47 y 86.",
        "operaciones": (
            "Revisamos si la cifra de las unidades termina en 0, 2, 4, 6 u 8:\n"
            "- 19 (termina en 9 -> impar).\n"
            "- 24 (termina en 4 -> par).\n"
            "- 30 (termina en 0 -> par).\n"
            "- 47 (termina en 7 -> impar).\n"
            "- 86 (termina en 6 -> par)."
        ),
        "respuesta": "Pasan a la primera fila las entradas **24, 30 y 86** (**3 números pares**).",
    },

    # =========================================================================
    # Subcategoría 2: Operaciones Aritméticas y Cálculo Mental (16 al 35)
    # =========================================================================
    {
        "id": 16,
        "title": "Las Poké Balls de Ash y Misty",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Antes de empezar su viaje, Ash saca 24 Poké Balls de su mochila y Misty saca 13 Poké Balls de la suya."
        ),
        "question": "¿Cuántas Poké Balls tienen entre los dos en total?",
        "datos": "Poké Balls de Ash: 24; Poké Balls de Misty: 13.",
        "operaciones": (
            "Sumamos sin llevada las unidades con las unidades y las decenas con las decenas:\n"
            "- Unidades: 4 + 3 = 7.\n"
            "- Decenas: 2 + 1 = 3.\n"
            "Total: 24 + 13 = 37 Poké Balls."
        ),
        "respuesta": "Entre los dos tienen **37 Poké Balls**.",
    },
    {
        "id": 17,
        "title": "Pacientes en el Centro Pokémon",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "La Enfermera Joy tiene mucho trabajo hoy: por la mañana cuida a 32 Pokémon cansados "
            "y por la tarde atiende a 15 Pokémon más."
        ),
        "question": "¿A cuántos Pokémon atiende la Enfermera Joy en todo el día?",
        "datos": "Atendidos por la mañana: 32; por la tarde: 15.",
        "operaciones": (
            "Sumamos 32 + 15:\n"
            "- Unidades: 2 + 5 = 7.\n"
            "- Decenas: 3 + 1 = 4.\n"
            "32 + 15 = 47 Pokémon."
        ),
        "respuesta": "La Enfermera Joy atiende en total a **47 Pokémon**.",
    },
    {
        "id": 18,
        "title": "La pirámide de bayas de Caterpie",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Caterpie construye una pirámide con bolsas de bayas. Cada bolsa de arriba tiene la suma "
            "de las dos bolsas que están justo debajo. En la fila de abajo hay 11, 12 y 14 bayas.\n\n"
            "```\n"
            "        ( ? )\n"
            "     ( ? ) ( ? )\n"
            "  (11)  (12)  (14)\n"
            "```"
        ),
        "question": "Calcula cuántas bayas van en las dos bolsas del medio y cuántas van en la bolsa de la cima.",
        "datos": "Fila inferior: 11, 12 y 14 bayas.",
        "operaciones": (
            "1. Bolsas del medio:\n"
            "   - Izquierda: 11 + 12 = 23.\n"
            "   - Derecha: 12 + 14 = 26.\n"
            "2. Bolsa de la cima: 23 + 26 = 49 bayas."
        ),
        "respuesta": "En el medio van **23 bayas** y **26 bayas**, y en la cima hay **49 bayas**.",
    },
    {
        "id": 19,
        "title": "Las Safari Balls de Ash",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Al salir de la Zona Safari, a Ash le quedan 23 Safari Balls en el bolsillo. "
            "El guarda le dice que lanzó 15 Safari Balls durante el paseo."
        ),
        "question": "¿Cuántas Safari Balls tenía Ash al entrar en la Zona Safari?",
        "datos": "Safari Balls que quedan: 23; Safari Balls lanzadas: 15.",
        "operaciones": (
            "Para saber cuántas tenía al principio, juntamos las que lanzó y las que le quedan:\n"
            "- Unidades: 3 + 5 = 8.\n"
            "- Decenas: 2 + 1 = 3.\n"
            "23 + 15 = 38 Safari Balls (comprobación: 38 - 15 = 23)."
        ),
        "respuesta": "Ash tenía **38 Safari Balls** al entrar.",
    },
    {
        "id": 20,
        "title": "Las galletas de Brock en el Bosque Verde",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Brock sale de viaje con 48 galletas Pokémon. Durante el descanso reparte 12 galletas "
            "a Geodude y luego encuentra un paquete nuevo con 10 galletas."
        ),
        "question": "¿Cuántas galletas tiene Brock al terminar la excursión?",
        "datos": "Galletas iniciales: 48; reparte: 12; encuentra: 10.",
        "operaciones": (
            "Resolvemos en dos pasos sin llevada:\n"
            "1. Restamos las que reparte: 48 - 12 = 36 galletas.\n"
            "2. Sumamos las que encuentra: 36 + 10 = 46 galletas."
        ),
        "respuesta": "Brock tiene al final **46 galletas**.",
    },
    {
        "id": 21,
        "title": "Puntos de Salud en el entrenamiento de Misty",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "El equipo de Misty comienza un entrenamiento amistoso con 68 Puntos de Salud (PS) en total. "
            "Durante los saltos en el agua pierden 24 PS."
        ),
        "question": "¿Cuántos Puntos de Salud (PS) le quedan al equipo de Misty?",
        "datos": "PS iniciales: 68; PS perdidos: 24.",
        "operaciones": (
            "Restamos sin llevada:\n"
            "- Unidades: 8 - 4 = 4.\n"
            "- Decenas: 6 - 2 = 4.\n"
            "68 - 24 = 44 PS."
        ),
        "respuesta": "Al equipo de Misty le quedan **44 PS**.",
    },
    {
        "id": 22,
        "title": "El doble de bayas Zreza para Raichu",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu recoge 7 bayas Zreza en un arbusto. Su amigo mayor Raichu recoge exactamente "
            "el doble de bayas que Pikachu."
        ),
        "question": "¿Cuántas bayas Zreza ha recogido Raichu?",
        "datos": "Bayas de Pikachu: 7; Raichu recoge el doble.",
        "operaciones": (
            "Calcular el doble de un número es sumarlo dos veces consigo mismo:\n"
            "7 + 7 = 14 bayas."
        ),
        "respuesta": "Raichu ha recogido **14 bayas**.",
    },
    {
        "id": 23,
        "title": "La mitad de las bayas Meloc para Eevee",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Serena lleva una cesta con 12 bayas Meloc y quiere darle exactamente la mitad a su Eevee."
        ),
        "question": "¿Cuántas bayas Meloc recibe Eevee?",
        "datos": "Total de bayas en la cesta: 12; parte para Eevee: la mitad.",
        "operaciones": (
            "Buscamos dos partes iguales que sumen 12:\n"
            "6 + 6 = 12, así que la mitad de 12 es 6."
        ),
        "respuesta": "Eevee recibe **6 bayas**.",
    },
    {
        "id": 24,
        "title": "Los nidos de Pidgey en el roble",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En las ramas de un gran árbol viven 4 familias de Pidgey. Cada uno de los 4 nidos "
            "tiene exactamente 2 huevos."
        ),
        "question": "¿Cuántos huevos de Pidgey hay en total en el árbol?",
        "datos": "Nidos: 4; huevos en cada nido: 2.",
        "operaciones": (
            "Sumamos 2 cuatro veces:\n"
            "2 + 2 + 2 + 2 = 8 huevos."
        ),
        "respuesta": "En total hay **8 huevos** en el árbol.",
    },
    {
        "id": 25,
        "title": "Las bandejas de bayas de Brock",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "A la hora de comer, Brock coloca 3 bandejas para sus Pokémon y pone 5 bayas en cada bandeja."
        ),
        "question": "¿Cuántas bayas prepara Brock en total?",
        "datos": "Bandejas: 3; bayas en cada bandeja: 5.",
        "operaciones": (
            "Sumamos 5 tres veces:\n"
            "5 + 5 + 5 = 15 bayas."
        ),
        "respuesta": "Brock prepara en total **15 bayas**.",
    },
    {
        "id": 26,
        "title": "Cajas de 10 Poké Balls en la estantería",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En la Tienda Pokémon hay 5 cajas iguales en una estantería. Dentro de cada caja hay 10 Poké Balls."
        ),
        "question": "¿Cuántas Poké Balls hay en total en las 5 cajas?",
        "datos": "Cajas: 5; Poké Balls en cada caja: 10.",
        "operaciones": (
            "Contamos de 10 en 10 cinco veces:\n"
            "10 + 10 + 10 + 10 + 10 = 50 Poké Balls."
        ),
        "respuesta": "Hay **50 Poké Balls** en total.",
    },
    {
        "id": 27,
        "title": "Completando la decena de huevos con Togepi",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En una cesta especial caben justo 10 huevos de juguete. Togepi ya ha guardado 6 huevos dentro."
        ),
        "question": "¿Cuántos huevos faltan para llenar la cesta hasta 10?",
        "datos": "Capacidad de la cesta: 10; huevos dentro: 6.",
        "operaciones": (
            "Buscamos el amigo del 10 para el 6:\n"
            "6 + 4 = 10, es decir, 10 - 6 = 4 huevos."
        ),
        "respuesta": "Faltan **4 huevos** para completar los 10.",
    },
    {
        "id": 28,
        "title": "El álbum de 50 pegatinas de Chansey",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "La Enfermera Joy tiene un álbum en el que caben 50 pegatinas de Chansey. "
            "Ya ha pegado 30 pegatinas."
        ),
        "question": "¿Cuántas pegatinas le faltan para completar el álbum?",
        "datos": "Pegatinas totales del álbum: 50; pegadas: 30.",
        "operaciones": (
            "Restamos las decenas:\n"
            "50 - 30 = 20 pegatinas (5 decenas menos 3 decenas son 2 decenas)."
        ),
        "respuesta": "Le faltan **20 pegatinas** para llenar el álbum.",
    },
    {
        "id": 29,
        "title": "La máquina numérica de Porygon",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Porygon ha inventado una máquina sencilla: cuando entra un número, primero suma 12 y luego resta 2.\n\n"
            "```\n"
            "ENTRA → ( +12 ) → ( −2 ) → SALE\n"
            "```"
        ),
        "question": "Si entran 24 puntos, ¿cuántos salen? Y si entran 35 puntos, ¿cuántos salen?",
        "datos": "Regla: primero +12, después -2; entradas: 24 y 35.",
        "operaciones": (
            "1. Con 24 puntos: 24 + 12 = 36; luego 36 - 2 = 34 puntos.\n"
            "2. Con 35 puntos: 35 + 12 = 47; luego 47 - 2 = 45 puntos."
        ),
        "respuesta": "Salen **34 puntos** y **45 puntos**.",
    },
    {
        "id": 30,
        "title": "El doble de puntos de Voltorb",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En la primera ronda del juego de luces, Voltorb consigue 20 puntos. "
            "En la segunda ronda consigue exactamente el doble de 20 puntos."
        ),
        "question": "¿Cuántos puntos consigue Voltorb en la segunda ronda?",
        "datos": "Puntos en la primera ronda: 20; segunda ronda: el doble.",
        "operaciones": (
            "El doble de 20 es sumar 20 dos veces:\n"
            "20 + 20 = 40 puntos."
        ),
        "respuesta": "Voltorb consigue **40 puntos** en la segunda ronda.",
    },
    {
        "id": 31,
        "title": "La mitad de los caramelos de Jigglypuff",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Jigglypuff tiene una bolsa con 20 caramelos de fresa y decide regalar exactamente la mitad a Clefairy."
        ),
        "question": "¿Cuántos caramelos le da Jigglypuff a Clefairy?",
        "datos": "Caramelos totales: 20; regalo: la mitad.",
        "operaciones": (
            "Repartimos 20 en dos grupos iguales:\n"
            "10 + 10 = 20, así que la mitad de 20 es 10 caramelos."
        ),
        "respuesta": "Jigglypuff le da **10 caramelos** a Clefairy.",
    },
    {
        "id": 32,
        "title": "¿A qué decena está más cerca? Los pasos de Eevee",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En una recta numérica pintada en el patio, Eevee se para en el número 28 y Charmander "
            "se para en el número 42."
        ),
        "question": "¿A qué decena está más cerca 28 (a 20 o a 30)? ¿Y 42 (a 40 o a 50)?",
        "datos": "Posición de Eevee: 28 pasos; posición de Charmander: 42 pasos.",
        "operaciones": (
            "Contamos la distancia en la recta numérica:\n"
            "- Del 28 al 30 hay solo 2 pasos, y al 20 hay 8 pasos -> 28 está más cerca de 30.\n"
            "- Del 42 al 40 hay solo 2 pasos, y al 50 hay 8 pasos -> 42 está más cerca de 40."
        ),
        "respuesta": "El 28 está más cerca de **30 pasos** y el 42 está más cerca de **40 pasos**.",
    },
    {
        "id": 33,
        "title": "Las bayas de los tres iniciales",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Los tres iniciales juntan sus meriendas sobre una manta: Bulbasaur pone 11 bayas, "
            "Charmander pone 12 bayas y Squirtle pone 15 bayas."
        ),
        "question": "¿Cuántas bayas han juntado entre los tres Pokémon?",
        "datos": "Bulbasaur: 11 bayas; Charmander: 12 bayas; Squirtle: 15 bayas.",
        "operaciones": (
            "Sumamos paso a paso sin llevada:\n"
            "1. 11 + 12 = 23 bayas.\n"
            "2. 23 + 15 = 38 bayas."
        ),
        "respuesta": "Han juntado **38 bayas** entre los tres.",
    },
    {
        "id": 34,
        "title": "¿Qué dos cestas suman 58 bayas?",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "En el campamento hay cuatro cestas con bayas: la cesta A tiene 21 bayas, la B tiene 30, "
            "la C tiene 37 y la D tiene 15. Ash necesita llevar exactamente 58 bayas usando solo dos cestas."
        ),
        "question": "¿Qué dos cestas tiene que elegir Ash para juntar exactamente 58 bayas?",
        "datos": "Cestas: A = 21, B = 30, C = 37, D = 15; objetivo: 58 bayas.",
        "operaciones": (
            "Probamos parejas sin pasarnos:\n"
            "- A + B: 21 + 30 = 51 (no llega).\n"
            "- A + C: 21 + 37 = 58 (unidades 1 + 7 = 8, decenas 2 + 3 = 5). ¡Exacto!\n"
            "- B + D: 30 + 15 = 45."
        ),
        "respuesta": "Debe elegir las cestas A (**21**) y C (**37**), que suman **58 bayas**.",
    },
    {
        "id": 35,
        "title": "El doble de fichas de Staryu y Starmie",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Staryu gana 13 fichas doradas en el juego acuático y Starmie gana exactamente el doble de fichas que Staryu."
        ),
        "question": "¿Cuántas fichas doradas gana Starmie?",
        "datos": "Fichas de Staryu: 13; fichas de Starmie: el doble.",
        "operaciones": (
            "Sumamos 13 + 13 sin llevada:\n"
            "- Unidades: 3 + 3 = 6.\n"
            "- Decenas: 1 + 1 = 2.\n"
            "13 + 13 = 26 fichas."
        ),
        "respuesta": "Starmie gana **26 fichas** doradas.",
    },

    # =========================================================================
    # Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero (36 al 50)
    # =========================================================================
    {
        "id": 36,
        "title": "Midiendo la altura de Bellsprout y Oddish",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "En el invernadero de Ciudad Azulona miden dos Pokémon tipo Planta: "
            "Bellsprout mide 70 cm de alto y Oddish mide 40 cm."
        ),
        "question": "¿Cuántos centímetros más alto es Bellsprout que Oddish?",
        "datos": "Altura de Bellsprout: 70 cm; altura de Oddish: 40 cm.",
        "operaciones": (
            "Restamos la altura menor de la mayor:\n"
            "70 - 40 = 30 cm."
        ),
        "respuesta": "Bellsprout es **30 cm** más alto que Oddish.",
    },
    {
        "id": 37,
        "title": "Pasos por el pasillo del Laboratorio Oak",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Pikachu mide el pasillo del laboratorio caminando con cuidado: de la puerta a la mesa "
            "hay 9 pasos. Luego vuelve caminando por el mismo sitio hasta la puerta."
        ),
        "question": "¿Cuántos pasos ha dado Pikachu en total entre la ida y la vuelta?",
        "datos": "Pasos de ida: 9; pasos de vuelta: 9.",
        "operaciones": (
            "Sumamos los pasos de la ida y de la vuelta:\n"
            "9 + 9 = 18 pasos."
        ),
        "respuesta": "Pikachu ha dado **18 pasos** en total.",
    },
    {
        "id": 38,
        "title": "Las mochilas en la báscula del Centro Pokémon",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Antes de subir a la montaña, Ash pesa su mochila y marca 12 kg. "
            "La mochila de Brock, que lleva más comida, marca 24 kg."
        ),
        "question": "¿Cuántos kilogramos pesan las dos mochilas juntas?",
        "datos": "Mochila de Ash: 12 kg; mochila de Brock: 24 kg.",
        "operaciones": (
            "Sumamos ambos pesos sin llevada:\n"
            "- Unidades: 2 + 4 = 6.\n"
            "- Decenas: 1 + 2 = 3.\n"
            "12 + 24 = 36 kg."
        ),
        "respuesta": "Las dos mochilas pesan **36 kg** juntas.",
    },
    {
        "id": 39,
        "title": "Las jarras de agua para Squirtle",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Misty llena una bañera pequeña para Squirtle echando una jarra de 5 litros y otra jarra de 3 litros. "
            "Squirtle salta dentro y salpica 2 litros fuera."
        ),
        "question": "¿Cuántos litros había al principio y cuántos litros quedan en la bañera después del salto?",
        "datos": "Jarra 1: 5 litros; jarra 2: 3 litros; salpicados: 2 litros.",
        "operaciones": (
            "1. Total echado al principio: 5 + 3 = 8 litros.\n"
            "2. Agua que queda tras salpicar: 8 - 2 = 6 litros."
        ),
        "respuesta": "Había **8 litros** al principio y quedan **6 litros** en la bañera.",
    },
    {
        "id": 40,
        "title": "La siesta de Pikachu en el reloj",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Pikachu se acuesta a dormir la siesta bajo un árbol cuando el reloj de agujas marca las 3:00 en punto. "
            "Se despierta muy contento a las 3:30 (las tres y media)."
        ),
        "question": "¿Cuántos minutos duró la siesta de Pikachu?",
        "datos": "Hora de inicio: 3:00; hora de despertar: 3:30.",
        "operaciones": (
            "Desde las 3 en punto (3:00) hasta las 3 y media (3:30) la aguja larga da media vuelta al reloj, "
            "que equivale a 30 minutos."
        ),
        "respuesta": "La siesta de Pikachu duró **30 minutos**.",
    },
    {
        "id": 41,
        "title": "La merienda en el Centro Pokémon",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "La Enfermera Joy empieza a preparar la merienda de los Pokémon cuando el reloj marca las 5:00 en punto "
            "y termina exactamente media hora (30 minutos) después."
        ),
        "question": "¿Qué hora marca el reloj cuando la Enfermera Joy termina la merienda?",
        "datos": "Inicio: 5:00 (5 horas); duración: media hora (30 minutos).",
        "operaciones": (
            "Si a las 5 en punto (5:00) le sumamos 30 minutos (media hora), "
            "la aguja pequeña sigue en el 5 y la aguja larga baja al 6: son las 5:30 (5 horas y 30 minutos)."
        ),
        "respuesta": "El reloj marca las **5:30** (**5 horas y 30 minutos**).",
    },
    {
        "id": 42,
        "title": "El tren hacia Ciudad Celeste",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Ash y Pikachu suben al tren en Pueblo Paleta cuando el reloj marca las 9:00 en punto. "
            "El viaje dura exactamente 2 horas."
        ),
        "question": "¿A qué hora en punto llega el tren a Ciudad Celeste?",
        "datos": "Hora de salida: 9:00; duración del viaje: 2 horas.",
        "operaciones": (
            "Sumamos 2 horas a las 9 en punto:\n"
            "9 + 2 = 11 -> las 11:00 (11 horas en punto)."
        ),
        "respuesta": "El tren llega a las **11:00** (**11 horas** en punto).",
    },
    {
        "id": 43,
        "title": "Comprando una Poké Ball y una Poción",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "En la Tienda Pokémon, una Poké Ball cuesta 2 € y una Poción cuesta 3 €. "
            "Ash compra una de cada y paga con un billete de 10 €."
        ),
        "question": "¿Cuántos euros gasta Ash en total y cuántos euros le devuelven?",
        "datos": "Poké Ball: 2 €; Poción: 3 €; pago: billete de 10 €.",
        "operaciones": (
            "1. Gasto total: 2 + 3 = 5 €.\n"
            "2. Dinero que le devuelven: 10 - 5 = 5 €."
        ),
        "respuesta": "Ash gasta **5 €** y le devuelven **5 €**.",
    },
    {
        "id": 44,
        "title": "Pagando la mochila con un billete de 50 euros",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Brock compra una tienda de campaña ligera para sus viajes que cuesta 30 €. "
            "En la caja entrega un billete de 50 €."
        ),
        "question": "¿Cuántos euros le tienen que devolver a Brock de cambio?",
        "datos": "Precio de la compra: 30 €; billete entregado: 50 €.",
        "operaciones": (
            "Restamos el precio al billete:\n"
            "50 - 30 = 20 €."
        ),
        "respuesta": "A Brock le devuelven **20 €**.",
    },
    {
        "id": 45,
        "title": "Las monedas de céntimos de Misty",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Una pegatina brillante de Staryu cuesta 70 céntimos. Misty saca de su monedero "
            "1 moneda de 50 céntimos y 1 moneda de 20 céntimos."
        ),
        "question": "¿Cuántos céntimos tiene Misty en total? ¿Cuánto dinero le sobra si compra la pegatina?",
        "datos": "Precio: 70 céntimos; monedas: 50 céntimos y 20 céntimos.",
        "operaciones": (
            "1. Dinero de Misty: 50 + 20 = 70 céntimos.\n"
            "2. Cambio tras pagar: 70 - 70 = 0 céntimos."
        ),
        "respuesta": "Misty tiene **70 céntimos** y le sobran **0 céntimos** (paga justo).",
    },
    {
        "id": 46,
        "title": "La hucha de billetes y monedas de Ash",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Ash abre su hucha de Pikachu para contar sus ahorros. Encuentra 1 billete de 20 €, "
            "1 billete de 5 € y 2 monedas de 2 €."
        ),
        "question": "¿Cuántos euros tiene ahorrados Ash en total?",
        "datos": "1 billete de 20 €, 1 billete de 5 €, 2 monedas de 2 €.",
        "operaciones": (
            "Sumamos todos los billetes y monedas:\n"
            "- Billetes: 20 + 5 = 25 €.\n"
            "- Monedas: 2 + 2 = 4 €.\n"
            "Total: 25 + 4 = 29 €."
        ),
        "respuesta": "Ash tiene ahorrados **29 €** en total.",
    },
    {
        "id": 47,
        "title": "Midiendo una hoja con la regla rota",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Bulbasaur quiere medir una hoja verde, pero su regla está rota por la punta y empieza en el 2 cm. "
            "Coloca la hoja desde el número 2 hasta el número 15."
        ),
        "question": "¿Cuántos centímetros mide de largo la hoja de Bulbasaur?",
        "datos": "Marca de inicio en la regla: 2 cm; marca final: 15 cm.",
        "operaciones": (
            "Restamos la marca inicial a la marca final para saber los centímetros reales:\n"
            "15 - 2 = 13 cm."
        ),
        "respuesta": "La hoja mide **13 cm** de largo.",
    },
    {
        "id": 48,
        "title": "Equilibrando la balanza de Geodude",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "En un plato de la balanza está sentado un Geodude que pesa 20 kg. "
            "En el otro plato Brock ya ha puesto una pesa de 10 kg."
        ),
        "question": "¿Cuántos kilogramos faltan en el segundo plato para equilibrar los dos platos?",
        "datos": "Peso de Geodude: 20 kg; pesa colocada: 10 kg.",
        "operaciones": (
            "Calculamos la diferencia entre 20 y 10:\n"
            "20 - 10 = 10 kg."
        ),
        "respuesta": "Faltan **10 kg** para equilibrar la balanza.",
    },
    {
        "id": 49,
        "title": "El horario de la mañana en el Gimnasio",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "El Gimnasio de Ciudad Celeste abre por la mañana a las 8:30 (ocho y media) "
            "y cierra para descansar a las 11:30 (once y media)."
        ),
        "question": "¿Cuántas horas seguidas está abierto el gimnasio durante la mañana?",
        "datos": "Hora de apertura: 8:30; hora de cierre: 11:30.",
        "operaciones": (
            "Como ambos horarios terminan en «y media» (:30), contamos las horas enteras de 8:30 a 11:30:\n"
            "9:30 (1 hora), 10:30 (2 horas), 11:30 (3 horas).\n"
            "11 - 8 = 3 horas."
        ),
        "respuesta": "El gimnasio está abierto **3 horas** seguidas.",
    },
    {
        "id": 50,
        "title": "El calendario de la semana de Pikachu",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Hoy es lunes, día 12 del mes. Ash apunta en su calendario que dentro de exactamente "
            "1 semana (7 días) se celebrará el festival de Pueblo Paleta."
        ),
        "question": "¿Qué día de la semana y qué número del mes se celebrará el festival?",
        "datos": "Día actual: lunes 12; tiempo hasta el festival: 1 semana (7 días).",
        "operaciones": (
            "1. Al pasar 1 semana entera (7 días), volvemos al mismo día de la semana: lunes.\n"
            "2. Sumamos 7 días al número 12: 12 + 7 = 19."
        ),
        "respuesta": "El festival será el **lunes** día **19** (**7 días** después).",
    },

    # =========================================================================
    # Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio (51 al 65)
    # =========================================================================
    {
        "id": 51,
        "title": "La silueta circular de la Poké Ball",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "El Profesor Oak dibuja en la pizarra la silueta plana de una Poké Ball vista de frente, "
            "formada por una línea curva cerrada perfectamente redonda."
        ),
        "question": "¿Qué figura geométrica plana es la silueta y cuántos lados rectos y vértices tiene?",
        "datos": "Figura plana formada por una línea curva cerrada redonda.",
        "operaciones": (
            "Una figura plana redonda limitada por una línea curva cerrada es un círculo.\n"
            "Como no tiene segmentos rectos, tiene 0 lados rectos y 0 vértices."
        ),
        "respuesta": "Es un **círculo** y tiene **0 lados** rectos y **0 vértices**.",
    },
    {
        "id": 52,
        "title": "La señal triangular del sendero",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Ash encuentra una señal triangular en el bosque. Dentro tiene dibujada una línea recta "
            "desde la esquina de arriba hasta la mitad del lado de abajo, partiéndola en dos partes iguales."
        ),
        "question": "¿Cuántos triángulos ves en total en la señal y cuántos lados tiene cada triángulo?",
        "datos": "Señal triangular dividida en 2 mitades por una línea recta.",
        "operaciones": (
            "1. Hay 2 triángulos pequeños (uno a la izquierda y otro a la derecha).\n"
            "2. La señal completa forma 1 triángulo grande: 2 + 1 = 3 triángulos.\n"
            "3. Cada triángulo tiene siempre 3 lados."
        ),
        "respuesta": "Se ven **3 triángulos** en total y cada triángulo tiene **3 lados**.",
    },
    {
        "id": 53,
        "title": "El campo cuadrado de Onix",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "El tapete donde entrena Onix tiene forma de cuadrado perfecto y cada uno de sus lados mide 4 metros."
        ),
        "question": "¿Cuántos lados y vértices tiene el cuadrado y cuántos metros mide todo su borde?",
        "datos": "Forma: cuadrado; medida de cada lado: 4 metros.",
        "operaciones": (
            "1. Un cuadrado tiene 4 lados iguales y 4 vértices.\n"
            "2. Sumamos los 4 lados: 4 + 4 + 4 + 4 = 16 metros."
        ),
        "respuesta": "Tiene **4 lados** y **4 vértices**, y su borde mide **16 metros**.",
    },
    {
        "id": 54,
        "title": "La pantalla rectangular de la Pokédex",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "La pantalla de la Pokédex de Ash tiene forma de rectángulo: sus lados largos miden 6 cm "
            "y sus lados cortos miden 4 cm."
        ),
        "question": "¿Cuántos vértices tiene la pantalla y cuántos centímetros suman todos sus lados?",
        "datos": "Forma: rectángulo; lados largos: 6 cm cada uno; lados cortos: 4 cm cada uno.",
        "operaciones": (
            "1. Todo rectángulo tiene 4 lados y 4 vértices.\n"
            "2. Suma de los 4 lados: 6 + 4 + 6 + 4 = 10 + 10 = 20 cm."
        ),
        "respuesta": "Tiene **4 vértices** y sus lados suman **20 cm**.",
    },
    {
        "id": 55,
        "title": "Líneas rectas y curvas en el cuaderno de Jigglypuff",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Jigglypuff dibuja con tizas de colores 2 cuadrados (hechos con líneas rectas) "
            "y 3 círculos (hechos con líneas curvas)."
        ),
        "question": "¿Cuántas figuras tienen líneas curvas y cuántos lados rectos dibujó Jigglypuff en total?",
        "datos": "Figuras dibujadas: 2 cuadrados y 3 círculos.",
        "operaciones": (
            "1. Los círculos están hechos con líneas curvas: son 3 círculos.\n"
            "2. Cada cuadrado tiene 4 lados rectos: 4 + 4 = 8 lados rectos en total."
        ),
        "respuesta": "Hay **3 círculos** con líneas curvas y dibujó **8 lados** rectos en total.",
    },
    {
        "id": 56,
        "title": "¿Dentro o fuera de la hierba alta?",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "En un claro del bosque hay una gran mancha redonda de hierba alta. "
            "Dentro de la hierba hay 6 Rattata escondidos, y fuera de la hierba hay 3 Pidgey saltando."
        ),
        "question": "¿Cuántos Pokémon hay dentro de la hierba alta y cuántos hay en total en el claro?",
        "datos": "Pokémon dentro de la hierba: 6; Pokémon fuera: 3.",
        "operaciones": (
            "1. Dentro de la hierba hay 6 Pokémon.\n"
            "2. Sumamos los de dentro y los de fuera: 6 + 3 = 9 Pokémon en total."
        ),
        "respuesta": "Hay **6 Pokémon** dentro y **9 Pokémon** en total.",
    },
    {
        "id": 57,
        "title": "A la izquierda y a la derecha de Pikachu",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Siete Pokémon hacen una fila mirando hacia delante. Pikachu está justo en el medio. "
            "A su izquierda están Bulbasaur, Charmander y Squirtle; a su derecha están Eevee, Psyduck y Meowth."
        ),
        "question": "¿Cuántos Pokémon están a la derecha de Pikachu y cuántos hay a ambos lados sin contar a Pikachu?",
        "datos": "A la izquierda: 3 Pokémon; a la derecha: 3 Pokémon; en el medio: Pikachu.",
        "operaciones": (
            "1. A la derecha de Pikachu están Eevee, Psyduck y Meowth: 3 Pokémon.\n"
            "2. Sumando los de la izquierda y los de la derecha: 3 + 3 = 6 Pokémon."
        ),
        "respuesta": "A su derecha hay **3 Pokémon** y a sus lados hay **6 Pokémon** en total.",
    },
    {
        "id": 58,
        "title": "Contando esquinas de cartulina",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Ash recorta 2 triángulos y 1 cuadrado en cartulina para decorar su cuaderno."
        ),
        "question": "¿Cuántos vértices (esquinas) tienen entre todas las figuras recortadas?",
        "datos": "Figuras: 2 triángulos y 1 cuadrado.",
        "operaciones": (
            "Cada triángulo tiene 3 vértices y cada cuadrado tiene 4 vértices:\n"
            "3 + 3 + 4 = 10 vértices."
        ),
        "respuesta": "Entre todas las figuras tienen **10 vértices**.",
    },
    {
        "id": 59,
        "title": "La valla triangular del jardín de Oddish",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Para proteger las flores de Oddish, Erika rodea un pequeño jardín triangular con una cuerda. "
            "Los tres lados del triángulo miden 5 metros, 6 metros y 4 metros."
        ),
        "question": "¿Cuántos metros de cuerda necesita en total para rodear todo el jardín?",
        "datos": "Lados del triángulo: 5 m, 6 m y 4 m.",
        "operaciones": (
            "Sumamos las longitudes de los 3 lados:\n"
            "5 + 6 = 11; 11 + 4 = 15 metros."
        ),
        "respuesta": "Necesita **15 metros** de cuerda en total.",
    },
    {
        "id": 60,
        "title": "Las baldosas cuadradas del Centro Pokémon",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "La entrada del Centro Pokémon tiene baldosas cuadradas ordenadas en 3 filas, "
            "con 5 baldosas en cada fila."
        ),
        "question": "¿Cuántas baldosas cuadradas hay en total en la entrada?",
        "datos": "Filas: 3; baldosas por fila: 5.",
        "operaciones": (
            "Sumamos las baldosas de las 3 filas:\n"
            "5 + 5 + 5 = 15 baldosas."
        ),
        "respuesta": "En la entrada hay **15 baldosas** cuadradas.",
    },
    {
        "id": 61,
        "title": "El mapa cuadriculado de Charmander",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "En una cuadrícula de columnas A, B, C, D (de izquierda a derecha) y filas 1, 2, 3, 4 (de abajo arriba), "
            "Charmander empieza en la casilla A1. Camina 2 casillas a la derecha y luego 2 casillas arriba."
        ),
        "question": "¿En qué casilla se detiene Charmander y cuántas casillas avanzó en total?",
        "datos": "Inicio: A1; movimientos: 2 a la derecha y 2 hacia arriba.",
        "operaciones": (
            "1. Desde A1 avanzamos 2 columnas a la derecha: A1 -> B1 -> C1.\n"
            "2. Subimos 2 filas hacia arriba: C1 -> C2 -> C3.\n"
            "3. Total de pasos: 2 + 2 = 4 casillas."
        ),
        "respuesta": "Se detiene en la casilla **C3** tras avanzar **4 casillas**.",
    },
    {
        "id": 62,
        "title": "Cuerpos redondos y cajas en el laboratorio",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Sobre la mesa hay una Poké Ball perfectamente redonda en el espacio y una caja de regalo "
            "que tiene 6 caras cuadradas iguales."
        ),
        "question": "¿Qué cuerpo geométrico es la Poké Ball, qué cuerpo geométrico es la caja y cuántas caras tiene la caja?",
        "datos": "Objeto 1: redondo como pelota; objeto 2: caja con 6 caras cuadradas iguales.",
        "operaciones": (
            "Identificamos los cuerpos geométricos:\n"
            "- Un objeto redondo como una pelota es una esfera.\n"
            "- Una caja con 6 caras cuadradas iguales es un cubo y tiene 6 caras."
        ),
        "respuesta": "La Poké Ball es una **esfera** y la caja es un **cubo** con **6 caras**.",
    },
    {
        "id": 63,
        "title": "Sumando lados de dos figuras",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Brock coloca sobre la mesa un rectángulo de madera y al lado un triángulo de madera, separados."
        ),
        "question": "¿Cuántos lados rectos hay en total contando los de las dos figuras?",
        "datos": "Figuras sobre la mesa: 1 rectángulo y 1 triángulo.",
        "operaciones": (
            "Contamos los lados de cada figura:\n"
            "- El rectángulo tiene 4 lados.\n"
            "- El triángulo tiene 3 lados.\n"
            "4 + 3 = 7 lados."
        ),
        "respuesta": "Entre las dos figuras suman **7 lados**.",
    },
    {
        "id": 64,
        "title": "Arriba y abajo en la estantería de Oak",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "En el estante de arriba de la librería hay 12 Poké Balls y en el estante de abajo hay 14 Poké Balls."
        ),
        "question": "¿Cuántas Poké Balls hay en total en la estantería y cuántas más hay abajo que arriba?",
        "datos": "Estante de arriba: 12 Poké Balls; estante de abajo: 14 Poké Balls.",
        "operaciones": (
            "1. Total en la estantería: 12 + 14 = 26 Poké Balls.\n"
            "2. Diferencia entre abajo y arriba: 14 - 12 = 2 Poké Balls."
        ),
        "respuesta": "Hay **26 Poké Balls** en total y **2 Poké Balls** más abajo.",
    },
    {
        "id": 65,
        "title": "La vuelta al recinto cuadrado de Growlithe",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Growlithe corre alrededor de un jardín cuadrado cuyos 4 lados miden 10 metros cada uno."
        ),
        "question": "¿Cuántos metros recorre Growlithe al dar una vuelta completa por todo el borde?",
        "datos": "Forma: cuadrado (4 lados); cada lado: 10 metros.",
        "operaciones": (
            "Sumamos los cuatro lados de 10 metros:\n"
            "10 + 10 + 10 + 10 = 40 metros."
        ),
        "respuesta": "Growlithe recorre **40 metros** en una vuelta.",
    },

    # =========================================================================
    # Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional (66 al 75)
    # =========================================================================
    {
        "id": 66,
        "title": "Las huellas de Pikachu de 2 en 2",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Pikachu camina dejando huellas numeradas de 2 en 2 en la arena: 2, 4, 6, 8, ?, 12."
        ),
        "question": "¿Qué número falta en la huella con interrogación y cuál es la regla?",
        "datos": "Serie de huellas: 2, 4, 6, 8, ?, 12.",
        "operaciones": (
            "Cada huella suma 2 unidades a la anterior (+2):\n"
            "2 + 2 = 4, 4 + 2 = 6, 6 + 2 = 8, 8 + 2 = 10, 10 + 2 = 12."
        ),
        "respuesta": "Falta el número **10** (**10 unidades**) siguiendo la regla de sumar **2 unidades**.",
    },
    {
        "id": 67,
        "title": "Los saltos de 5 en 5 de Ponyta",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Ponyta salta por piedras numeradas contando de 5 en 5: 5, 10, 15, 20, ?, 30."
        ),
        "question": "¿Qué número falta en la interrogación y qué número irá en la piedra siguiente al 30?",
        "datos": "Serie de 5 en 5: 5, 10, 15, 20, ?, 30.",
        "operaciones": (
            "Sumamos 5 en cada salto (+5):\n"
            "- Después de 20: 20 + 5 = 25.\n"
            "- Después de 30: 30 + 5 = 35."
        ),
        "respuesta": "Falta el **25** y después del 30 va el **35** (**25 unidades** y **35 unidades**).",
    },
    {
        "id": 68,
        "title": "La batería de Magnemite de 10 en 10",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "El medidor de energía de Magnemite sube de 10 en 10 puntos: 10, 20, 30, ?, 50, 60."
        ),
        "question": "¿Qué número falta en la pantalla y qué número marcará después del 60?",
        "datos": "Serie de 10 en 10: 10, 20, 30, ?, 50, 60.",
        "operaciones": (
            "La regla es sumar 10 puntos cada vez:\n"
            "- 30 + 10 = 40.\n"
            "- 60 + 10 = 70."
        ),
        "respuesta": "Falta el **40** y después del 60 marcará **70 puntos**.",
    },
    {
        "id": 69,
        "title": "El collar de Poké Balls de colores",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Ash coloca bolas de colores en fila repitiendo siempre este orden: "
            "Roja, Azul, Amarilla, Roja, Azul, Amarilla, Roja, ..."
        ),
        "question": "¿De qué color será la 8ª bola y de qué color será la 9ª bola de la fila?",
        "datos": "Patrón que se repite: [Roja, Azul, Amarilla] (de 3 en 3); la 7ª es Roja.",
        "operaciones": (
            "El ciclo tiene 3 colores: 1ª Roja, 2ª Azul, 3ª Amarilla; 4ª Roja, 5ª Azul, 6ª Amarilla; "
            "7ª Roja, así que la 8ª es Azul y la 9ª es Amarilla."
        ),
        "respuesta": "La **8ª posición** es **Azul** y la **9ª posición** es **Amarilla**.",
    },
    {
        "id": 70,
        "title": "Cuenta atrás de 2 en 2",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Un globo de juguete de Meowth despega cuando termina una cuenta atrás que baja de 2 en 2: "
            "20, 18, 16, 14, ?, 10."
        ),
        "question": "¿Qué número de segundos falta en la cuenta atrás?",
        "datos": "Cuenta atrás: 20, 18, 16, 14, ?, 10.",
        "operaciones": (
            "La regla es restar 2 cada vez:\n"
            "14 - 2 = 12 (y comprobamos: 12 - 2 = 10)."
        ),
        "respuesta": "Falta el número **12** (**12 segundos**).",
    },
    {
        "id": 71,
        "title": "¡Busca el intruso en la serie de 5 en 5!",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Togepi apunta en su pizarra una serie que debería sumar 5 cada vez: 10, 15, 20, 27, 30, 35. "
            "¡Uno de los números se ha colado por error!"
        ),
        "question": "¿Cuál es el número intruso y qué número debería estar en su lugar?",
        "datos": "Serie anotada: 10, 15, 20, 27, 30, 35; regla: +5.",
        "operaciones": (
            "Comprobamos sumando 5: 10 + 5 = 15, 15 + 5 = 20, 20 + 5 = 25.\n"
            "En lugar de 25 aparece 27, así que 27 es el intruso (25 + 5 = 30 y 30 + 5 = 35)."
        ),
        "respuesta": "El intruso es **27 unidades** y debería ir **25 unidades**.",
    },
    {
        "id": 72,
        "title": "Los 3 pasos para atrapar a Caterpie",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Ash ha desordenado las instrucciones para encontrar y capturar un Caterpie amigo:\n"
            "- A: Lanzar la Poké Ball.\n"
            "- B: Buscar entre la hierba alta.\n"
            "- C: Debilitar un poco a Caterpie."
        ),
        "question": "¿En qué orden (1º, 2º y 3º paso) debe seguir Ash las tres instrucciones?",
        "datos": "Instrucciones: A (Lanzar Poké Ball), B (Buscar), C (Debilitar).",
        "operaciones": (
            "Ordenamos los 3 pasos del primero al último:\n"
            "- 1º paso: Buscar entre la hierba alta (B).\n"
            "- 2º paso: Debilitar un poco a Caterpie (C).\n"
            "- 3º paso: Lanzar la Poké Ball (A)."
        ),
        "respuesta": "El orden de los **3 pasos** es **1º B, 2º C y 3º A**.",
    },
    {
        "id": 73,
        "title": "La máquina de sumar 10 puntos",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Una máquina del laboratorio siempre suma 10 al número que entra: si entra 14 sale 24, "
            "y si entra 25 sale 35."
        ),
        "question": "¿Qué número sale si entra 43 y qué número sale si entra 61?",
        "datos": "Regla: sumar 10; números que entran: 43 y 61.",
        "operaciones": (
            "Sumamos 1 decena (+10) a cada número:\n"
            "- 43 + 10 = 53.\n"
            "- 61 + 10 = 71."
        ),
        "respuesta": "Salen **53 puntos** y **71 puntos**.",
    },
    {
        "id": 74,
        "title": "La regla de saltos de Bulbasaur",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Bulbasaur juega siguiendo esta regla: SI ve una flor azul, da 2 saltos; "
            "SI ve una flor roja, da 1 salto. En su camino encuentra 3 flores azules y 2 flores rojas."
        ),
        "question": "¿Cuántas veces salta Bulbasaur en total al pasar junto a todas las flores?",
        "datos": "Flor azul: 2 saltos (ve 3); flor roja: 1 salto (ve 2).",
        "operaciones": (
            "1. Por las 3 flores azules: 2 + 2 + 2 = 6 saltos.\n"
            "2. Por las 2 flores rojas: 1 + 1 = 2 saltos.\n"
            "Total: 6 + 2 = 8 veces."
        ),
        "respuesta": "Bulbasaur salta en total **8 veces**.",
    },
    {
        "id": 75,
        "title": "Las bayas de Snorlax que bajan de 10 en 10",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Snorlax tiene una cesta con 80 bayas y cada hora se come 10. "
            "Así van bajando las bayas: 80, 70, 60, 50, ?, ?."
        ),
        "question": "¿Cuántas bayas quedarán en los dos pasos siguientes de la serie?",
        "datos": "Serie decreciente: 80, 70, 60, 50; regla: -10.",
        "operaciones": (
            "Restamos 10 bayas en cada paso:\n"
            "- 50 - 10 = 40 bayas.\n"
            "- 40 - 10 = 30 bayas."
        ),
        "respuesta": "Quedarán **40 bayas** y después **30 bayas**.",
    },

    # =========================================================================
    # Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad (76 al 85)
    # =========================================================================
    {
        "id": 76,
        "title": "La tabla de recuento de la Ruta 1",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Ash anota con una rayita (|) cada Pokémon que ve durante su paseo:\n\n"
            "| Pokémon | Rayitas |\n"
            "|---|---|\n"
            "| Pidgey | \\| \\| \\| \\| \\| |\n"
            "| Rattata | \\| \\| \\| |\n"
            "| Caterpie | \\| \\| \\| \\| \\| \\| |\n"
            "| Pikachu | \\| \\| |"
        ),
        "question": "¿Qué Pokémon vio más veces y cuántos Pokémon vio en total durante el paseo?",
        "datos": "Pidgey: 5; Rattata: 3; Caterpie: 6; Pikachu: 2.",
        "operaciones": (
            "1. Contamos las rayitas: Pidgey 5, Rattata 3, Caterpie 6, Pikachu 2.\n"
            "2. El número mayor es 6 -> Caterpie.\n"
            "3. Total: 5 + 3 = 8; 8 + 6 = 14; 14 + 2 = 16 Pokémon."
        ),
        "respuesta": "Vio más veces a **Caterpie** (**6 veces**) y en total vio **16 Pokémon**.",
    },
    {
        "id": 77,
        "title": "El pictograma de bayas de los iniciales",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "En un dibujo de la merienda, cada símbolo ★ vale exactamente 1 baya:\n\n"
            "| Pokémon | Bayas comidas |\n"
            "|---|---|\n"
            "| Pikachu | ★ ★ ★ |\n"
            "| Charmander | ★ ★ ★ ★ ★ |\n"
            "| Squirtle | ★ ★ |"
        ),
        "question": "¿Cuántas bayas comió Charmander más que Squirtle y cuántas comieron entre los tres?",
        "datos": "Pikachu: 3 bayas; Charmander: 5 bayas; Squirtle: 2 bayas.",
        "operaciones": (
            "1. Diferencia entre Charmander y Squirtle: 5 - 2 = 3 bayas.\n"
            "2. Total entre los tres: 3 + 5 + 2 = 10 bayas."
        ),
        "respuesta": "Charmander comió **3 bayas** más que Squirtle y entre los tres comieron **10 bayas**.",
    },
    {
        "id": 78,
        "title": "El gráfico de barras de la clase de 1º A",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "En la clase de 1º A hacen un gráfico de barras con su tipo de Pokémon favorito: "
            "la barra de Fuego llega a 8 votos, la de Agua a 6 votos, la de Planta a 5 votos y la de Eléctrico a 9 votos."
        ),
        "question": "¿Cuál es el tipo favorito de la clase y cuántos alumnos votaron en total?",
        "datos": "Votos: Fuego 8, Agua 6, Planta 5, Eléctrico 9.",
        "operaciones": (
            "1. La barra más alta es la de Eléctrico con 9 votos.\n"
            "2. Sumamos todos los votos: 8 + 6 = 14; 14 + 5 = 19; 19 + 9 = 28 alumnos."
        ),
        "respuesta": "El favorito es **Eléctrico** (**9 votos**) y votaron **28 alumnos** en total.",
    },
    {
        "id": 79,
        "title": "La bolsa sorpresa de Bayas Meloc",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "En la Tienda Pokémon, Ash recibe una bolsa opaca que contiene únicamente 8 Bayas Meloc rosadas "
            "y ninguna otra fruta. Mete la mano sin mirar para sacar 1 baya."
        ),
        "question": "Clasifica el suceso «sacar una Baya Meloc de la bolsa» como seguro, posible o imposible.",
        "datos": "Contenido de la bolsa: 8 Bayas Meloc (todas son iguales).",
        "operaciones": (
            "Como las 8 bayas que hay dentro son Bayas Meloc, cualquier baya que saque será siempre "
            "una Baya Meloc: es un suceso seguro."
        ),
        "respuesta": "Sacar una Baya Meloc es un suceso **seguro** (**8 bayas** de **8**).",
    },
    {
        "id": 80,
        "title": "¿Un Magikarp en el desierto seco?",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Ash camina por un desierto de arena muy seco donde no hay ríos, lagos ni charcos de agua. "
            "Se pregunta si podrá pescar un Magikarp salvaje nadando en la arena seca."
        ),
        "question": "Clasifica el suceso «pescar un Magikarp nadando en la arena seca» como seguro, posible o imposible.",
        "datos": "Lugar: desierto seco sin agua; Magikarp solo vive en el agua.",
        "operaciones": (
            "Como en la arena seca no hay agua y un pez no puede nadar sin agua, "
            "hay 0 posibilidades de que ocurra: es imposible."
        ),
        "respuesta": "Es un suceso **imposible** (**0 posibilidades**).",
    },
    {
        "id": 81,
        "title": "La caja de Poké Balls rojas y azules",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Dentro de una caja cerrada, Misty guarda 5 Poké Balls rojas y 2 Super Balls azules. "
            "Va a sacar una bola con los ojos cerrados."
        ),
        "question": "¿Sacar una Super Ball azul es seguro, posible o imposible? ¿Qué bola es más probable que salga?",
        "datos": "En la caja: 5 Poké Balls rojas y 2 Super Balls azules.",
        "operaciones": (
            "1. Como hay 2 Super Balls dentro de la caja, puede salir una (pero no siempre): es posible.\n"
            "2. Hay más Poké Balls rojas (5) que azules (2), así que es más probable sacar una Poké Ball roja."
        ),
        "respuesta": "Sacar una Super Ball es **posible**, y es **más probable** sacar una **Poké Ball** (**5** frente a **2**).",
    },
    {
        "id": 82,
        "title": "El pictograma de 2 en 2 del campamento",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "En el mural del campamento cada estrella ★ representa 2 Pokémon dibujados:\n\n"
            "| Entrenador | Estrellas |\n"
            "|---|---|\n"
            "| Brock | ★ ★ ★ |\n"
            "| Misty | ★ ★ ★ ★ |"
        ),
        "question": "¿Cuántos Pokémon dibujó Brock y cuántos dibujó Misty?",
        "datos": "Clave: 1 estrella = 2 Pokémon; Brock: 3 estrellas; Misty: 4 estrellas.",
        "operaciones": (
            "Contamos de 2 en 2:\n"
            "- Brock: 2 + 2 + 2 = 6 Pokémon.\n"
            "- Misty: 2 + 2 + 2 + 2 = 8 Pokémon."
        ),
        "respuesta": "Brock dibujó **6 Pokémon** y Misty dibujó **8 Pokémon**.",
    },
    {
        "id": 83,
        "title": "La tabla de caramelos de colores",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Los alumnos anotan en una tabla cuántos caramelos Pokémon hay en cuatro tarros: "
            "Rojos 12, Azules 10, Verdes 14 y Amarillos 11."
        ),
        "question": "¿De qué color hay más caramelos y cuántos caramelos Rojos y Azules hay entre los dos tarros?",
        "datos": "Rojos: 12; Azules: 10; Verdes: 14; Amarillos: 11.",
        "operaciones": (
            "1. Comparamos: 14 es el mayor -> color verde.\n"
            "2. Sumamos Rojos y Azules sin llevada: 12 + 10 = 22 caramelos."
        ),
        "respuesta": "Hay más de color **verde** (**14 caramelos**) y Rojos más Azules suman **22 caramelos**.",
    },
    {
        "id": 84,
        "title": "La ruleta de premios del Centro Pokémon",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "La Enfermera Joy tiene una ruleta dividida en 4 partes iguales: 3 partes tienen el dibujo de una Poción "
            "y 1 parte tiene el dibujo de una Baya."
        ),
        "question": "Al girar la ruleta, ¿qué premio es más probable que salga: una Poción o una Baya?",
        "datos": "Partes totales: 4; Poción: 3 partes; Baya: 1 parte.",
        "operaciones": (
            "Comparamos las partes de la ruleta:\n"
            "Poción ocupa 3 partes de 4, y Baya ocupa solo 1 parte de 4. Como 3 > 1, es más probable Poción."
        ),
        "respuesta": "Es **más probable** que salga una **Poción** (**3 partes** de **4**).",
    },
    {
        "id": 85,
        "title": "La tabla de puntos de los amigos",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Tres amigos apuntan sus puntos en la tabla del club:\n\n"
            "| Amigo | Puntos |\n"
            "|---|---|\n"
            "| Lucas | 21 |\n"
            "| Sara | 14 |\n"
            "| Leo | 11 |"
        ),
        "question": "¿Cuántos puntos consiguen entre los tres y cuántos puntos más tiene Lucas que Leo?",
        "datos": "Lucas: 21 puntos; Sara: 14 puntos; Leo: 11 puntos.",
        "operaciones": (
            "1. Suma total sin llevada: 21 + 14 = 35; 35 + 11 = 46 puntos.\n"
            "2. Diferencia entre Lucas y Leo: 21 - 11 = 10 puntos."
        ),
        "respuesta": "Consiguen **46 puntos** en total y Lucas tiene **10 puntos** más que Leo.",
    },

    # =========================================================================
    # Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP) (86 al 100)
    # =========================================================================
    {
        "id": 86,
        "title": "Primera victoria y EXP de Pikachu",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu empieza su entrenamiento con 24 puntos de experiencia (EXP). "
            "Después de ganar un combate amistoso contra un Pidgey, gana 15 puntos de EXP más."
        ),
        "question": "¿Cuántos puntos de experiencia (EXP) tiene Pikachu ahora?",
        "datos": "EXP inicial: 24; EXP ganada: 15.",
        "operaciones": (
            "Sumamos sin llevada:\n"
            "- Unidades: 4 + 5 = 9.\n"
            "- Decenas: 2 + 1 = 3.\n"
            "24 + 15 = 39 puntos de EXP."
        ),
        "respuesta": "Pikachu tiene ahora **39 puntos de EXP**.",
    },
    {
        "id": 87,
        "title": "Lo que falta a Charmander para el Nivel 5",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Charmander necesita juntar 50 puntos de experiencia (EXP) para subir al Nivel 5. "
            "En su ficha ya tiene acumulados 30 puntos de EXP."
        ),
        "question": "¿Cuántos puntos de EXP le faltan a Charmander para alcanzar el Nivel 5?",
        "datos": "Meta para Nivel 5: 50 puntos de EXP; EXP actual: 30.",
        "operaciones": (
            "Restamos la experiencia que ya tiene de la meta:\n"
            "50 - 30 = 20 puntos de EXP."
        ),
        "respuesta": "A Charmander le faltan **20 puntos de EXP** para subir de nivel.",
    },
    {
        "id": 88,
        "title": "La Poción curativa para Squirtle",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Después de correr por la playa, Squirtle tiene solo 15 Puntos de Salud (PS). "
            "Misty le da una Poción que le cura 20 PS."
        ),
        "question": "¿Cuántos Puntos de Salud (PS) tiene Squirtle después de tomar la Poción?",
        "datos": "PS actuales: 15; curación de la Poción: +20 PS.",
        "operaciones": (
            "Sumamos los PS de la Poción sin llevada:\n"
            "15 + 20 = 35 PS."
        ),
        "respuesta": "Squirtle tiene ahora **35 PS**.",
    },
    {
        "id": 89,
        "title": "La Baya Aranja de Bulbasaur",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "En mitad de un entrenamiento, Bulbasaur tiene 28 PS y se come una rica Baya Aranja "
            "que le devuelve 10 PS."
        ),
        "question": "¿Cuántos PS tiene Bulbasaur después de comer la Baya Aranja?",
        "datos": "PS antes de la baya: 28; curación de la Baya Aranja: +10 PS.",
        "operaciones": (
            "Sumamos 1 decena (+10) sin llevada:\n"
            "28 + 10 = 38 PS."
        ),
        "respuesta": "Bulbasaur tiene **38 PS** después de comer la baya.",
    },
    {
        "id": 90,
        "title": "El ataque Placaje contra Rattata",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Un Rattata salvaje comienza un duelo amistoso con 46 PS. Eevee usa Placaje y le hace 14 puntos de daño."
        ),
        "question": "¿Cuántos PS le quedan a Rattata después del ataque?",
        "datos": "PS iniciales de Rattata: 46; daño recibido: 14 PS.",
        "operaciones": (
            "Restamos el daño recibido sin llevada:\n"
            "- Unidades: 6 - 4 = 2.\n"
            "- Decenas: 4 - 1 = 3.\n"
            "46 - 14 = 32 PS."
        ),
        "respuesta": "A Rattata le quedan **32 PS**.",
    },
    {
        "id": 91,
        "title": "Dos combates seguidos en la Ruta 1",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu empieza el día con 12 puntos de EXP. Gana un combate de práctica (+21 EXP) "
            "y luego otro combate contra un Caterpie (+15 EXP)."
        ),
        "question": "¿Cuántos puntos de EXP tiene Pikachu al terminar los dos combates?",
        "datos": "EXP inicial: 12; 1er combate: +21 EXP; 2º combate: +15 EXP.",
        "operaciones": (
            "Sumamos paso a paso sin llevada:\n"
            "1. Tras el primer combate: 12 + 21 = 33 EXP.\n"
            "2. Tras el segundo combate: 33 + 15 = 48 puntos de EXP."
        ),
        "respuesta": "Pikachu termina con **48 puntos de EXP**.",
    },
    {
        "id": 92,
        "title": "¡Sin pasarse del máximo de PS de Jigglypuff!",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Jigglypuff tiene como máximo 45 PS (nunca puede tener más de 45 PS). Ahora mismo tiene 35 PS "
            "y la Enfermera Joy le aplica una Poción de 20 PS."
        ),
        "question": "¿Con cuántos PS se queda Jigglypuff y cuántos puntos de curación sobran sin usarse?",
        "datos": "PS máximos: 45; PS actuales: 35; Poción: +20 PS.",
        "operaciones": (
            "1. Si sumamos: 35 + 20 = 55 PS, pero se pasa del máximo.\n"
            "2. Como el tope es 45, Jigglypuff se queda con 45 PS.\n"
            "3. Sobran sin usarse: 55 - 45 = 10 PS."
        ),
        "respuesta": "Se queda con **45 PS** y sobran **10 PS** de la Poción.",
    },
    {
        "id": 93,
        "title": "El Caramelo Raro de Charmander",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Charmander está en el Nivel 6. Ash le da 1 Caramelo Raro que hace subir exactamente 1 nivel al instante, "
            "y después gana suficiente EXP en un combate para subir otro 1 nivel más."
        ),
        "question": "¿Qué nivel alcanza Charmander al terminar el día?",
        "datos": "Nivel inicial: 6; Caramelo Raro: +1 nivel; combate: +1 nivel.",
        "operaciones": (
            "Sumamos los niveles ganados:\n"
            "6 + 1 = 7; 7 + 1 = 8 (sube al Nivel 8)."
        ),
        "respuesta": "Charmander alcanza el **Nivel 8** (**8 niveles**).",
    },
    {
        "id": 94,
        "title": "Repartiendo EXP entre Pikachu y Eevee",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu y Eevee vencen juntos en un combate por parejas y consiguen un premio de 20 puntos de EXP "
            "para repartirse a partes iguales (la mitad cada uno)."
        ),
        "question": "¿Cuántos puntos de EXP recibe cada uno de los dos Pokémon?",
        "datos": "EXP total ganada: 20 puntos; reparto: mitad para Pikachu y mitad para Eevee.",
        "operaciones": (
            "Partimos 20 en dos mitades iguales:\n"
            "10 + 10 = 20, así que cada uno recibe 10 puntos de EXP."
        ),
        "respuesta": "Cada Pokémon recibe **10 puntos de EXP**.",
    },
    {
        "id": 95,
        "title": "Poción y Baya Aranja para Geodude",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "El Geodude de Brock tiene 23 PS tras un entrenamiento intenso. Para recuperarlo, "
            "Brock le da 1 Poción (+20 PS) y 1 Baya Aranja (+10 PS)."
        ),
        "question": "¿Cuántos PS tiene Geodude después de recibir la Poción y la baya?",
        "datos": "PS iniciales: 23; Poción: +20 PS; Baya Aranja: +10 PS.",
        "operaciones": (
            "Sumamos paso a paso sin llevada:\n"
            "1. Con la Poción: 23 + 20 = 43 PS.\n"
            "2. Con la Baya Aranja: 43 + 10 = 53 PS."
        ),
        "respuesta": "Geodude tiene ahora **53 PS**.",
    },
    {
        "id": 96,
        "title": "La meta del Nivel 8 para Squirtle",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Para alcanzar el Nivel 8 hacen falta 80 puntos de EXP. Squirtle ya tenía 40 puntos de EXP "
            "y acaba de ganar 20 puntos de EXP más."
        ),
        "question": "¿Cuántos puntos de EXP tiene Squirtle ahora y cuántos le faltan para el Nivel 8?",
        "datos": "Meta Nivel 8: 80 EXP; EXP previa: 40; EXP nueva: +20.",
        "operaciones": (
            "1. EXP actual: 40 + 20 = 60 puntos de EXP.\n"
            "2. EXP que falta: 80 - 60 = 20 puntos de EXP."
        ),
        "respuesta": "Tiene **60 puntos de EXP** y le faltan **20 puntos de EXP**.",
    },
    {
        "id": 97,
        "title": "La tabla de EXP de la Ruta 2",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "En la Ruta 2, Charmander vence a 2 Caterpie y a 1 Pidgey. Mira cuánta EXP da cada uno:\n\n"
            "| Pokémon | EXP por victoria |\n"
            "|---|---|\n"
            "| Caterpie | 10 |\n"
            "| Pidgey | 15 |"
        ),
        "question": "¿Cuántos puntos de EXP gana Charmander en total con las tres victorias?",
        "datos": "2 Caterpie (10 EXP cada uno) y 1 Pidgey (15 EXP).",
        "operaciones": (
            "1. Por los 2 Caterpie: 10 + 10 = 20 puntos de EXP.\n"
            "2. Sumamos el Pidgey: 20 + 15 = 35 puntos de EXP."
        ),
        "respuesta": "Charmander gana en total **35 puntos de EXP**.",
    },
    {
        "id": 98,
        "title": "El combate por turnos de Pikachu",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu empieza un combate con 48 PS. Turno 1: recibe un golpe de 12 PS. "
            "Turno 2: come una Baya Aranja (+10 PS). Turno 3: recibe otro golpe de 14 PS."
        ),
        "question": "¿Cuántos PS le quedan a Pikachu al terminar el turno 3?",
        "datos": "PS iniciales: 48; turno 1: -12; turno 2: +10; turno 3: -14.",
        "operaciones": (
            "Calculamos turno a turno sin llevada:\n"
            "- Turno 1: 48 - 12 = 36 PS.\n"
            "- Turno 2: 36 + 10 = 46 PS.\n"
            "- Turno 3: 46 - 14 = 32 PS."
        ),
        "respuesta": "A Pikachu le quedan **32 PS** al terminar el turno 3.",
    },
    {
        "id": 99,
        "title": "Comparando la EXP de Bulbasaur y Charmander",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Después de entrenar toda la semana, Bulbasaur tiene 67 puntos de EXP "
            "y Charmander tiene 52 puntos de EXP."
        ),
        "question": "¿Cuántos puntos de EXP tiene Bulbasaur más que Charmander?",
        "datos": "EXP de Bulbasaur: 67; EXP de Charmander: 52.",
        "operaciones": (
            "Restamos sin llevada:\n"
            "- Unidades: 7 - 2 = 5.\n"
            "- Decenas: 6 - 5 = 1.\n"
            "67 - 52 = 15 puntos de EXP."
        ),
        "respuesta": "Bulbasaur tiene **15 puntos de EXP** más que Charmander.",
    },
    {
        "id": 100,
        "title": "El gran salto de Pikachu al Nivel 9",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Pikachu tiene acumulados 54 puntos de EXP y necesita llegar a 95 puntos de EXP para subir al Nivel 9. "
            "En su combate final gana 31 puntos de EXP."
        ),
        "question": "¿Cuántos puntos de EXP tiene Pikachu después del combate y cuántos le faltan todavía para llegar a 95?",
        "datos": "EXP inicial: 54; EXP ganada: 31; meta Nivel 9: 95.",
        "operaciones": (
            "1. Nueva EXP tras el combate: 54 + 31 = 85 puntos de EXP.\n"
            "2. Puntos que faltan para 95: 95 - 85 = 10 puntos de EXP."
        ),
        "respuesta": "Pikachu tiene **85 puntos de EXP** y le faltan **10 puntos de EXP** para el Nivel 9.",
    },
]


RETOS: List[Dict[str, str | int]] = [
    {
        "id": 101,
        "title": "Pokédex misteriosa: ¿quién se esconde?",
        "subcategory": SUBCAT_1,
        "sense": SENSE_NUM,
        "context": (
            "La Pokédex muestra una sombra negra con estas pistas: «Mi número tiene 2 cifras. "
            "Tengo 2 decenas. Mi cifra de las unidades es 5». Sospechosos: Bulbasaur (1), "
            "Rattata (19), Ekans (23), Pikachu (25) y Meowth (52)."
        ),
        "question": "Usa las pistas para descartar sospechosos. ¿Qué Pokémon se esconde y qué número tiene?",
        "datos": "Pistas: 2 cifras, 2 decenas, 5 unidades. Lista: 1, 19, 23, 25, 52.",
        "operaciones": (
            "1. «2 cifras»: se descarta 1.\n"
            "2. «2 decenas»: quedan 23 y 25 (se descartan 19 y 52).\n"
            "3. «5 unidades»: entre 23 y 25, el único con 5 unidades es 25 (Pikachu)."
        ),
        "respuesta": "Se esconde **Pikachu**, que tiene el número **25** (**25 unidades**).",
    },
    {
        "id": 102,
        "title": "Deducción en el Laboratorio Oak",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Tres amigos, Sara, Leo y Lucas, eligen cada uno un inicial distinto: Bulbasaur (n.º 1, Planta), "
            "Charmander (n.º 4, Fuego) o Squirtle (n.º 7, Agua). Pistas: (1) Sara no elige ni Fuego ni Agua. "
            "(2) Leo no elige a Squirtle."
        ),
        "question": "¿Qué Pokémon elige cada niño y cuánto suman los tres números de Pokédex juntos?",
        "datos": "Iniciales: Bulbasaur (1, Planta), Charmander (4, Fuego), Squirtle (7, Agua).",
        "operaciones": (
            "1. Por la pista (1), Sara elige Planta -> Bulbasaur.\n"
            "2. Quedan Charmander y Squirtle. Por la pista (2), Leo elige a Charmander.\n"
            "3. Para Lucas queda Squirtle.\n"
            "4. Suma de números: 1 + 4 + 7 = 12."
        ),
        "respuesta": "**Sara: Bulbasaur, Leo: Charmander y Lucas: Squirtle**; los números suman **12 unidades**.",
    },
    {
        "id": 103,
        "title": "La cadena de pruebas de Misty",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Para ganar una medalla de entrenamiento empiezas con 20 puntos. Prueba 1: ganas 14 puntos. "
            "Prueba 2: pierdes 10 puntos. Prueba 3: ganas el doble de 5 puntos. Misty da el premio si terminas "
            "con un número par."
        ),
        "question": "¿Con cuántos puntos terminas la cadena y consigues la medalla?",
        "datos": "Inicio: 20; prueba 1: +14; prueba 2: -10; prueba 3: + doble de 5.",
        "operaciones": (
            "1. Prueba 1: 20 + 14 = 34 puntos.\n"
            "2. Prueba 2: 34 - 10 = 24 puntos.\n"
            "3. Prueba 3: el doble de 5 es 5 + 5 = 10; 24 + 10 = 34 puntos.\n"
            "4. Como 34 termina en 4, es un número par."
        ),
        "respuesta": "Terminas con **34 puntos** (número par), así que **sí consigues la medalla** (**1 medalla**).",
    },
    {
        "id": 104,
        "title": "De compras en la Tienda Pokémon con 20 euros",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "En la Tienda Pokémon los precios son: Poké Ball 2 €, Poción 3 €, Antídoto 1 € y Super Ball 5 €. "
            "Ash compra 2 Poké Balls y 2 Pociones, y paga en la caja con un billete de 20 €."
        ),
        "question": "¿Cuántos euros gasta Ash en total y cuántos euros le devuelven de cambio?",
        "datos": "2 Poké Balls (2 € cada una); 2 Pociones (3 € cada una); billete: 20 €.",
        "operaciones": (
            "1. 2 Poké Balls: 2 + 2 = 4 €.\n"
            "2. 2 Pociones: 3 + 3 = 6 €.\n"
            "3. Gasto total: 4 + 6 = 10 €.\n"
            "4. Cambio: 20 - 10 = 10 €."
        ),
        "respuesta": "Ash gasta **10 €** y le devuelven **10 €**.",
    },
    {
        "id": 105,
        "title": "El cuadro del torneo de 4 amigos",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Cuatro amigos juegan un torneo por eliminación. El ganador de cada pareja pasa a la final:\n\n"
            "```\n"
            "Semifinales      Final\n"
            "Ash   ─┐\n"
            "       ├─ ? ─┐\n"
            "Gary  ─┘     ├─ CAMPEÓN\n"
            "Misty ─┐     │\n"
            "       ├─ ? ─┘\n"
            "Brock ─┘\n"
            "```"
        ),
        "question": "¿Cuántos combates se juegan en todo el torneo y cuántos combates tiene que ganar el campeón?",
        "datos": "4 participantes en semifinales (2 parejas) y 1 final.",
        "operaciones": (
            "1. En semifinales hay 2 parejas -> 2 combates.\n"
            "2. En la final hay 1 pareja -> 1 combate.\n"
            "Total de combates: 2 + 1 = 3 combates.\n"
            "3. El campeón juega 1 combate en semifinales y 1 en la final: 1 + 1 = 2 combates."
        ),
        "respuesta": "Se juegan **3 combates** en total y el campeón gana **2 combates**.",
    },
    {
        "id": 106,
        "title": "El mapa cuadriculado del bosque",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Ash está en la casilla A1 de este mapa (columnas A–D, filas 1–4):\n\n"
            "| Fila | A | B | C | D |\n"
            "|---|---|---|---|---|\n"
            "| 4 | 🌳 | 🌿 | 🌊 | Eevee |\n"
            "| 3 | 🌿 | 🌿 | Caterpie | 🌿 |\n"
            "| 2 | 🌿 | 🌳 | 🌿 | Psyduck |\n"
            "| 1 | Ash | 🌿 | 🌿 | 🌳 |"
        ),
        "question": "Si Ash avanza → → ↑ ↑ desde A1, ¿a qué casilla llega y a quién encuentra? ¿Qué Pokémon está en D2 y cuántas casillas avanzó?",
        "datos": "Inicio: A1; flechas: 2 derecha y 2 arriba; Caterpie en C3; Psyduck en D2.",
        "operaciones": (
            "1. Dos a la derecha: A1 -> B1 -> C1. Dos arriba: C1 -> C2 -> C3 (ahí está Caterpie).\n"
            "2. En la columna D, fila 2 está Psyduck.\n"
            "3. Casillas avanzadas: 2 + 2 = 4 casillas."
        ),
        "respuesta": "Llega a **C3** con **Caterpie**, en D2 está **Psyduck** y avanzó **4 casillas**.",
    },
    {
        "id": 107,
        "title": "La cuenta atrás del huevo de Togepi",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "El huevo de Togepi necesita 50 pasos para abrirse. El lunes Ash da 20 pasos y el martes da 10 pasos. "
            "Después decide dar 10 pasos cada día (miércoles, jueves...)."
        ),
        "question": "¿Cuántos pasos faltan después del martes y cuántos días en total tarda en abrirse desde el lunes?",
        "datos": "Meta: 50 pasos; lunes: 20; martes: 10; luego 10 pasos al día.",
        "operaciones": (
            "1. Pasos lunes y martes: 20 + 10 = 30 pasos.\n"
            "2. Pasos que faltan: 50 - 30 = 20 pasos.\n"
            "3. A 10 pasos al día: miércoles (+10 = 40) y jueves (+10 = 50) -> 2 días más.\n"
            "4. Total de días desde el lunes: 2 + 2 = 4 días."
        ),
        "respuesta": "Le faltan **20 pasos** y tarda en total **4 días** en abrirse.",
    },
    {
        "id": 108,
        "title": "Impactrueno: dobles, mitades y ceros",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "El Impactrueno de Pikachu hace 10 puntos de daño normal. Contra Squirtle (Agua) hace el doble, "
            "contra Bulbasaur (Planta) hace la mitad y contra Diglett (Tierra) hace 0 de daño."
        ),
        "question": "¿Cuánto daño recibe cada uno de los tres Pokémon y cuánto suman los tres daños juntos?",
        "datos": "Daño normal: 10; Agua: doble; Planta: mitad; Tierra: 0.",
        "operaciones": (
            "1. Squirtle (doble de 10): 10 + 10 = 20 de daño.\n"
            "2. Bulbasaur (mitad de 10): 5 de daño (5 + 5 = 10).\n"
            "3. Diglett (Tierra): 0 de daño.\n"
            "4. Suma total: 20 + 5 + 0 = 25 de daño."
        ),
        "respuesta": "Reciben **20, 5 y 0 de daño**, y juntos suman **25 puntos** de daño.",
    },
    {
        "id": 109,
        "title": "Construye tu equipo de nivel 20",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Para jugar un torneo hay que formar un equipo de 3 Pokémon distintos cuyos niveles sumen exactamente 20. "
            "Disponibles: Pikachu (nivel 10), Bulbasaur (nivel 8), Charmander (nivel 7), Squirtle (nivel 5) y Caterpie (nivel 3)."
        ),
        "question": "Encuentra 2 equipos distintos de 3 Pokémon que sumen exactamente 20 niveles.",
        "datos": "Niveles: Pikachu 10, Bulbasaur 8, Charmander 7, Squirtle 5, Caterpie 3; objetivo: 20.",
        "operaciones": (
            "Buscamos tríos que sumen 20:\n"
            "- Con Pikachu (10): 10 + 7 + 3 = 20 -> Pikachu + Charmander + Caterpie.\n"
            "- Sin Pikachu: 8 + 7 + 5 = 20 -> Bulbasaur + Charmander + Squirtle."
        ),
        "respuesta": "Hay **2 equipos**: **Pikachu + Charmander + Caterpie** y **Bulbasaur + Charmander + Squirtle** (suman **20 niveles**).",
    },
    {
        "id": 110,
        "title": "El candado de 2 cifras del Team Rocket",
        "subcategory": SUBCAT_5,
        "sense": SENSE_ALG,
        "context": (
            "Meowth ha cerrado una caja de juguetes con un candado de 2 cifras. Cada cifra es el número que sigue en una serie:\n"
            "- Primera cifra: 2, 4, 6, ?\n"
            "- Segunda cifra: 20, 15, 10, ?"
        ),
        "question": "Descubre la regla de cada serie y escribe el código de 2 cifras que abre la caja.",
        "datos": "Serie 1: 2, 4, 6; serie 2: 20, 15, 10.",
        "operaciones": (
            "1. Serie 1 (suma 2 cada vez): 6 + 2 = 8.\n"
            "2. Serie 2 (resta 5 cada vez): 10 - 5 = 5.\n"
            "Unimos las 2 cifras: 85."
        ),
        "respuesta": "El código de **2 cifras** que abre la caja es el **85**.",
    },
    {
        "id": 111,
        "title": "¡Encuentra el error de Ash!",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Ash quiere sumar 34 bayas y 5 bayas. Al colocarlas en vertical pone el 5 debajo del 3 "
            "en vez de ponerlo debajo del 4, y dice muy seguro: «¡Tengo 84 bayas!»."
        ),
        "question": "¿En qué se equivocó Ash y cuántas bayas tiene en realidad al hacer bien la suma?",
        "datos": "Sumandos: 34 bayas y 5 bayas; resultado erróneo de Ash: 84.",
        "operaciones": (
            "Ash colocó el 5 (5 unidades) en la columna de las decenas como si fuera 50.\n"
            "Colocando unidades debajo de unidades:\n"
            "34 + 5 = 39 bayas (unidades: 4 + 5 = 9; decenas: 3)."
        ),
        "respuesta": "Ash puso el 5 en las decenas; en realidad tiene **39 bayas**.",
    },
    {
        "id": 112,
        "title": "¿Caben todos en el autobús escolar?",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "El autobús del campamento Pokémon tiene 49 lugares. Suben 21 alumnos de 1º A y 24 alumnos de 1º B."
        ),
        "question": "¿Cuántos alumnos suben en total? ¿Caben todos y cuántos lugares quedan libres?",
        "datos": "Lugares del autobús: 49; alumnos 1º A: 21; alumnos 1º B: 24.",
        "operaciones": (
            "1. Total de alumnos sin llevada: 21 + 24 = 45 alumnos.\n"
            "2. Como 45 < 49, caben todos.\n"
            "3. Lugares libres: 49 - 45 = 4 lugares."
        ),
        "respuesta": "Suben **45 alumnos**, sí caben todos y quedan **4 lugares** libres.",
    },
    {
        "id": 113,
        "title": "El pictograma de bayas de la semana",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Este pictograma muestra las bayas recogidas cada día. Cada dibujo ● vale 2 bayas:\n\n"
            "| Día | Bayas recogidas |\n"
            "|---|---|\n"
            "| Lunes | ● ● |\n"
            "| Martes | ● ● ● |\n"
            "| Miércoles | ● |\n"
            "| Jueves | ● ● ● ● |"
        ),
        "question": "¿Qué día recogieron más bayas y cuántas bayas recogieron en total entre los cuatro días?",
        "datos": "Clave: ● = 2 bayas; lunes 2, martes 3, miércoles 1, jueves 4 dibujos.",
        "operaciones": (
            "1. Calculamos de 2 en 2: lunes 4, martes 6, miércoles 2, jueves 8 bayas.\n"
            "2. El día mayor es el jueves con 8 bayas.\n"
            "3. Total: 4 + 6 = 10; 10 + 2 = 12; 12 + 8 = 20 bayas."
        ),
        "respuesta": "El día que más recogieron fue el jueves (**8 bayas**) y en total fueron **20 bayas**.",
    },
    {
        "id": 114,
        "title": "La bolsa opaca de Poké Balls de Brock",
        "subcategory": SUBCAT_6,
        "sense": SENSE_EST,
        "context": (
            "Brock mete en una bolsa opaca 4 Poké Balls rojas y 2 Super Balls azules (no hay ninguna Ultra Ball). "
            "Ash sacará una sin mirar."
        ),
        "question": "a) ¿Qué es más probable sacar? b) ¿Es seguro, posible o imposible sacar una Ultra Ball? c) ¿Cuántas Super Balls hay que añadir para que las dos sean igual de probables?",
        "datos": "En la bolsa: 4 Poké Balls, 2 Super Balls y 0 Ultra Balls.",
        "operaciones": (
            "a) Hay más Poké Balls (4) que Super Balls (2) -> es más probable una Poké Ball.\n"
            "b) Como no hay ninguna Ultra Ball, sacarla es imposible.\n"
            "c) Para empatar a 4: 4 - 2 = 2 Super Balls más."
        ),
        "respuesta": "a) Es más probable una **Poké Ball**; b) la Ultra Ball es **imposible**; c) hay que añadir **2 Super Balls**.",
    },
    {
        "id": 115,
        "title": "¿Cuánto crece Oddish al evolucionar?",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "Según la Pokédex de Erika, Oddish mide 50 cm de altura y al evolucionar a Gloom pasa a medir 80 cm. "
            "Después Gloom se sube encima de una piedra plana de 15 cm de altura."
        ),
        "question": "¿Cuántos centímetros crece Oddish al evolucionar a Gloom y a qué altura total llega sobre la piedra?",
        "datos": "Oddish: 50 cm; Gloom: 80 cm; piedra: 15 cm.",
        "operaciones": (
            "1. Crecimiento al evolucionar: 80 - 50 = 30 cm.\n"
            "2. Altura de Gloom sobre la piedra: 80 + 15 = 95 cm."
        ),
        "respuesta": "Crece **30 cm** al evolucionar y sobre la piedra alcanza **95 cm**.",
    },
    {
        "id": 116,
        "title": "La fila de atención del Centro Pokémon",
        "subcategory": SUBCAT_3,
        "sense": SENSE_MED,
        "context": (
            "El Centro Pokémon abre a las 9:00 en punto. La Enfermera Joy tarda media hora (30 minutos) en revisar a cada equipo "
            "y atiende uno tras otro: primero Ash, segundo Misty y tercero Brock."
        ),
        "question": "¿A qué hora termina la Enfermera Joy de revisar al equipo de Misty y a qué hora termina con el equipo de Brock?",
        "datos": "Apertura: 9:00; duración por equipo: media hora (30 minutos); orden: Ash, Misty, Brock.",
        "operaciones": (
            "Seguimos los turnos de media hora en media hora:\n"
            "- Ash: de 9:00 a 9:30.\n"
            "- Misty: de 9:30 a 10:00 (10 horas en punto).\n"
            "- Brock: de 10:00 a 10:30 (10 horas y 30 minutos)."
        ),
        "respuesta": "Termina con Misty a las **10:00** (**10 horas**) y con Brock a las **10:30** (**10 horas y 30 minutos**).",
    },
    {
        "id": 117,
        "title": "¿A qué nivel sube Pikachu con la tabla?",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "Esta tabla dice cuánta EXP necesita Pikachu para cada nivel. Ahora tiene 20 puntos de EXP (Nivel 2) "
            "y gana dos combates: uno de 10 EXP y otro de 30 EXP.\n\n"
            "| Nivel | EXP necesaria |\n"
            "|---|---|\n"
            "| 2 | 20 |\n"
            "| 3 | 40 |\n"
            "| 4 | 60 |\n"
            "| 5 | 80 |"
        ),
        "question": "¿Cuántos puntos de EXP tiene al final, a qué nivel sube y cuánta EXP le falta para el Nivel 5?",
        "datos": "EXP inicial: 20; combates: +10 EXP y +30 EXP; Nivel 4 = 60 EXP; Nivel 5 = 80 EXP.",
        "operaciones": (
            "1. EXP tras el primer combate: 20 + 10 = 30 EXP.\n"
            "2. EXP tras el segundo combate: 30 + 30 = 60 EXP -> alcanza justo el Nivel 4.\n"
            "3. Para el Nivel 5: 80 - 60 = 20 puntos de EXP."
        ),
        "respuesta": "Tiene **60 puntos de EXP**, sube al **Nivel 4** y le faltan **20 puntos de EXP** para el Nivel 5.",
    },
    {
        "id": 118,
        "title": "Los corrales de palos de Brock",
        "subcategory": SUBCAT_4,
        "sense": SENSE_ESP,
        "context": (
            "Brock construye corrales cuadrados con palos del mismo tamaño. Para 1 corral usa 4 palos; "
            "si pone 2 corrales pegados comparten un lado y usa 7 palos; para 3 corrales usa 10 palos.\n\n"
            "```\n"
            " _       _ _       _ _ _\n"
            "|_|     |_|_|     |_|_|_|\n"
            " 4        7         10\n"
            "```"
        ),
        "question": "¿Cuántos palos necesita para hacer 4 corrales pegados y cuántos para 5 corrales pegados?",
        "datos": "1 corral: 4 palos; 2 corrales: 7 palos; 3 corrales: 10 palos.",
        "operaciones": (
            "Cada corral nuevo comparte 1 lado y solo añade 3 palos (+3):\n"
            "- 4 corrales: 10 + 3 = 13 palos (unidades).\n"
            "- 5 corrales: 13 + 3 = 16 palos (unidades)."
        ),
        "respuesta": "Necesita **13 unidades** (palos) para 4 corrales y **16 unidades** (palos) para 5 corrales.",
    },
    {
        "id": 119,
        "title": "El reparto del doble de bayas",
        "subcategory": SUBCAT_2,
        "sense": SENSE_NUM,
        "context": (
            "Ash y Misty han recogido juntos 18 bayas. Como Ash cargó la cesta, acuerdan que Ash se queda el doble "
            "de bayas que Misty (1 parte para Misty y 2 partes iguales para Ash).\n\n"
            "```\n"
            "Misty: [ ▢ ]\n"
            "Ash:   [ ▢ ][ ▢ ]    Total: 18 bayas\n"
            "```"
        ),
        "question": "¿Cuántas bayas le tocan a Misty y cuántas bayas le tocan a Ash?",
        "datos": "Total: 18 bayas; 3 partes iguales (1 para Misty, 2 para Ash).",
        "operaciones": (
            "Buscamos 3 números iguales que sumen 18:\n"
            "6 + 6 + 6 = 18 -> cada cuadrito vale 6.\n"
            "- Misty (1 cuadrito): 6 bayas.\n"
            "- Ash (2 cuadritos): 6 + 6 = 12 bayas."
        ),
        "respuesta": "A Misty le tocan **6 bayas** y a Ash le tocan **12 bayas**.",
    },
    {
        "id": 120,
        "title": "Gran desafío final: Squirtle contra Charmander",
        "subcategory": SUBCAT_7,
        "sense": SENSE_NUM,
        "context": (
            "En el combate amistoso final, Squirtle tiene 38 PS y Charmander tiene 25 PS. Atacan por turnos "
            "y empieza Squirtle. Pistola Agua de Squirtle hace el doble de 10 (20 de daño) contra Fuego. "
            "Ascuas de Charmander hace la mitad de 10 (5 de daño) contra Agua. Quien deje al rival en 0 PS gana, "
            "y el ganador suma 25 puntos de EXP a los 42 puntos de EXP que ya tenía."
        ),
        "question": "¿Quién gana el combate, con cuántos PS termina el ganador y cuántos puntos de EXP tiene después de ganar?",
        "datos": "Squirtle: 38 PS (daño 20); Charmander: 25 PS (daño 5); EXP previa: 42; premio: +25 EXP.",
        "operaciones": (
            "1. Turno 1 (Squirtle ataca): Charmander pasa de 25 a 25 - 20 = 5 PS.\n"
            "2. Turno 2 (Charmander ataca): Squirtle pasa de 38 a 38 - 5 = 33 PS.\n"
            "3. Turno 3 (Squirtle ataca): Charmander pasa de 5 a 0 PS (5 < 20).\n"
            "4. Gana Squirtle con 33 PS. Nueva EXP: 42 + 25 = 67 puntos de EXP."
        ),
        "respuesta": "Gana **Squirtle** con **33 PS** y alcanza **67 puntos de EXP**.",
    },
]


INTRO_TEXT = """# Banco de Problemas Matemáticos Pokémon — 1º de Primaria (LOMLOE)

## Introducción Curricular y Pedagógica
El presente documento constituye el banco oficial y completo de 100 problemas matemáticos (más 20 Retos Especiales) contextualizados en el universo Pokémon para **1º de Educación Primaria**, diseñado en rigurosa consonancia con la normativa educativa española (**LOMLOE - Real Decreto 157/2022**).

Los problemas están adaptados didáctica y lingüísticamente a alumnos de 6 y 7 años de edad (inicio del Primer Ciclo de Primaria), con números naturales del **0 al 99**, sumas y restas **sin llevada**, dobles sencillos, aproximación a la decena más cercana, medidas básicas, reloj en punto y media, euros y céntimos, formas 2D y relaciones espaciales, series de +2/+5/+10, recuentos y probabilidad inicial, y mecánicas de combate/EXP adaptadas:
1. **Subcategoría 1 (Problemas 1 al 15)**: Numeración, Descomposición y Valor Posicional (números del 0 al 99, decenas y unidades, anterior/posterior, comparar con `<` y `>`, pares/impares, ordinales del 1º al 10º).
2. **Subcategoría 2 (Problemas 16 al 35)**: Operaciones Aritméticas y Cálculo Mental (sumas y restas sin llevada hasta 99, dobles sencillos, amigos del 10 y decena más cercana).
3. **Subcategoría 3 (Problemas 36 al 50)**: Magnitudes, Unidades de Medida, Tiempo y Dinero (palmos, pasos, cm, kg, litros, horas en punto y media, monedas y billetes de euro hasta 50 €).
4. **Subcategoría 4 (Problemas 51 al 65)**: Geometría, Formas, Perímetros, Áreas y Espacio (triángulo, cuadrado, rectángulo, círculo, líneas rectas/curvas, dentro/fuera, izquierda/derecha, conteo de lados y vértices).
5. **Subcategoría 5 (Problemas 66 al 75)**: Patrones, Regularidades y Pensamiento Computacional (series de +2, +5, +10, patrones de colores/Poké Balls, instrucciones paso a paso).
6. **Subcategoría 6 (Problemas 76 al 85)**: Tratamiento de la Información, Gráficos y Probabilidad (tablas de recuento sencillas, pictogramas, gráficos sencillos, seguro/posible/imposible).
7. **Subcategoría 7 (Problemas 86 al 100)**: Mecánicas de Combate, Nivel y Experiencia (EXP) (puntos de experiencia EXP, subir de nivel, PS, Pociones +20 PS y Bayas Aranja +10 PS con números hasta 99).

---
"""


SUBCAT_HEADERS = {
    1: "### Soluciones — Subcategoría 1: Numeración, Descomposición y Valor Posicional",
    16: "### Soluciones — Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
    36: "### Soluciones — Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
    51: "### Soluciones — Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
    66: "### Soluciones — Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
    76: "### Soluciones — Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
    86: "### Soluciones — Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
}


def build_markdown() -> str:
    lines: List[str] = [INTRO_TEXT.rstrip(), "", "## Parte 1: Enunciados de los Problemas (1 al 100)", ""]

    for p in PROBLEMS:
        lines.append(f"### Problema {p['id']}: {p['title']}")
        lines.append(f"- **Subcategoría**: {p['subcategory']}")
        lines.append(f"- **Sentido LOMLOE**: {p['sense']}")
        lines.append(f"- **Contexto Pokémon**: {p['context']}")
        lines.append(f"**Pregunta**: {p['question']}")
        lines.append("")

    lines.append("## Parte 1B: Retos Especiales (101 al 120)")
    lines.append("")
    for r in RETOS:
        lines.append(f"### Reto {r['id']}: {r['title']}")
        lines.append(f"- **Subcategoría**: {r['subcategory']}")
        lines.append(f"- **Sentido LOMLOE**: {r['sense']}")
        lines.append(f"- **Contexto Pokémon**: {r['context']}")
        lines.append(f"**Pregunta**: {r['question']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Parte 2: Solucionario y Respuestas Razonadas (1 al 100)")
    lines.append("")

    for p in PROBLEMS:
        pid = int(p["id"])
        if pid in SUBCAT_HEADERS:
            lines.append(SUBCAT_HEADERS[pid])
            lines.append("")
        lines.append(f"### Solución Problema {pid}: {p['title']}")
        lines.append("")
        lines.append(f"- **Datos identificados**: {p['datos']}")
        lines.append(f"- **Planteamiento y Operaciones**: {p['operaciones']}")
        lines.append(f"- **Respuesta Final**: {p['respuesta']}")
        lines.append("")

    lines.append("### Soluciones — Parte 1B: Retos Especiales (101 al 120)")
    lines.append("")
    for r in RETOS:
        rid = int(r["id"])
        lines.append(f"### Solución al Reto {rid}: {r['title']}")
        lines.append("")
        lines.append(f"- **Datos identificados**: {r['datos']}")
        lines.append(f"- **Planteamiento y Operaciones**: {r['operaciones']}")
        lines.append(f"- **Respuesta Final**: {r['respuesta']}")
        lines.append("")

    raw = "\n".join(lines).rstrip() + "\n"
    return unicodedata.normalize("NFC", raw)


def main() -> None:
    assert len(PROBLEMS) == 100, f"Expected 100 core problems, got {len(PROBLEMS)}"
    assert len(RETOS) == 20, f"Expected 20 Retos, got {len(RETOS)}"

    out_path = Path(__file__).resolve().parent / "problemas_1_primaria.md"
    content = build_markdown()
    out_path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Generated {out_path.name}: {len(content)} chars, {len(content.splitlines())} lines (100 problems + 20 retos).")


if __name__ == "__main__":
    main()
