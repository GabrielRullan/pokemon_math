# -*- coding: utf-8 -*-
"""
Script to generate the complete, genuine, high-quality math problem bank for 2º de Primaria:
problemas_2_primaria.md
"""

import os
import sys

problems_data = [
    # Subcategoría 1: Numeración, Descomposición y Valor Posicional (Problemas 1 al 15)
    {
        "id": 1,
        "title": "El número de Pikachu en la Pokédex",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "El Profesor Oak le entrega a Ash su nueva Pokédex electrónica en el laboratorio de Pueblo Paleta. Al escanear a su inseparable compañero Pikachu, el aparato muestra en la pantalla digital que está registrado con el número 25 de la región de Kanto.\n\n¿Cuántas decenas y cuántas unidades forman el número 25 de Pikachu?",
        "datos": "Número de Pikachu en la Pokédex: 25.",
        "operaciones": "En el sistema de numeración decimal, descomponemos el número 25 según el valor posicional de sus cifras:\n- La cifra de la izquierda (2) corresponde a las decenas: 2 decenas = 20 unidades.\n- La cifra de la derecha (5) corresponde a las unidades: 5 unidades.\nPor tanto: 25 = 20 + 5 = 2 decenas y 5 unidades.",
        "respuesta": "El número 25 de Pikachu está formado por **2 decenas y 5 unidades**."
    },
    {
        "id": 2,
        "title": "El avistamiento de Pidgey en la Ruta 1",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Durante su primer paseo por la soleada Ruta 1, Ash y Pikachu observan una gran bandada de Pidgey descansando entre las copas de los árboles. Tras contarlos con mucha paciencia, anotan en su cuaderno de campo un total de 134 Pidgey.\n\nDescompón el número 134 en centenas, decenas y unidades, y escribe su descomposición aditiva.",
        "datos": "Cantidad de Pidgey avistados: 134.",
        "operaciones": "Analizamos la posición de cada una de las tres cifras del número 134:\n- La cifra de las centenas es 1: 1 centena = 100 unidades.\n- La cifra de las decenas es 3: 3 decenas = 30 unidades.\n- La cifra de las unidades es 4: 4 unidades.\nLa descomposición aditiva es: 100 + 30 + 4 = 134.",
        "respuesta": "El número 134 se descompone en **1 centena, 3 decenas y 4 unidades** (100 + 30 + 4 = **134 Pidgey**)."
    },
    {
        "id": 3,
        "title": "Las Bayas Aranja de Brock",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Brock organiza con esmero los bolsillos de su mochila de montañero antes de partir de viaje. En el compartimento de alimentos guarda exactamente 459 Bayas Aranja, muy útiles para recuperar la vitalidad de sus compañeros.\n\n¿Cuál es el número anterior y cuál es el número posterior a 459?",
        "datos": "Cantidad de bayas en la mochila: 459.",
        "operaciones": "Para calcular el número anterior restamos 1 unidad, y para el número posterior sumamos 1 unidad:\n- Número anterior: 459 - 1 = 458.\n- Número posterior: 459 + 1 = 460.",
        "respuesta": "El número anterior es **458** y el número posterior es **460**."
    },
    {
        "id": 4,
        "title": "Comparando el peso de los Geodude",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "En el Gimnasio de Ciudad Plateada, Brock sube a la báscula a dos Geodude recién llegados para comprobar su estado de salud. El primer Geodude marca 215 kilogramos en la pantalla, mientras que el segundo Geodude marca 210 kilogramos.\n\nCompara ambos pesos utilizando el signo mayor que (>), menor que (<) o igual (=).",
        "datos": "Peso del primer Geodude: 215 kg; peso del segundo Geodude: 210 kg.",
        "operaciones": "Comparamos cifra a cifra de izquierda a derecha empezando por las centenas:\n- Centenas: ambos tienen 2 centenas (2 = 2).\n- Decenas: ambos tienen 1 decena (1 = 1).\n- Unidades: el primer número tiene 5 unidades y el segundo tiene 0 unidades. Como 5 es mayor que 0 (5 > 0), deducimos que 215 > 210.",
        "respuesta": "La comparación correcta de pesos es **215 kg > 210 kg**."
    },
    {
        "id": 5,
        "title": "La gran colección de Poké Balls de Gary Oak",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Gary Oak quiere impresionar a todos los entrenadores mostrando su arcón de entrenamiento, en el que guarda nada menos que 308 Poké Balls listas para ser utilizadas.\n\n¿Cuántas centenas, decenas y unidades tiene el número 308? ¿Qué valor representa la cifra 0?",
        "datos": "Total de Poké Balls coleccionadas: 308.",
        "operaciones": "Descomponemos el número 308 según sus órdenes de magnitud:\n- Cifra de las centenas: 3 (valor: 300 unidades).\n- Cifra de las decenas: 0 (indica que hay 0 decenas sueltas, valor: 0 unidades).\n- Cifra de las unidades: 8 (valor: 8 unidades).\nDescomposición aditiva: 300 + 0 + 8 = 308.",
        "respuesta": "El número 308 tiene **3 centenas, 0 decenas y 8 unidades**, donde la cifra 0 representa **0 decenas**."
    },
    {
        "id": 6,
        "title": "La carrera de Ponyta en la Llanura Verde",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "En la gran carrera anual de Pokémon veloces que se celebra en la Llanura Verde participan 10 corredores. El veloz Ponyta de Ash cruza la línea de meta justo detrás del participante que llegó en 4º lugar (cuarto puesto).\n\n¿En qué posición ordinal llegó a la meta el Ponyta de Ash?",
        "datos": "Posición del corredor anterior: 4º (cuarto).",
        "operaciones": "Los números ordinales indican orden o posición en una serie (1º primero, 2º segundo, 3º tercero, 4º cuarto, 5º quinto, etc.). Si el Ponyta de Ash entra inmediatamente después del 4º clasificado, le corresponde el ordinal siguiente: 4º + 1 = 5º.",
        "respuesta": "El Ponyta de Ash llegó a la meta en **5º lugar (quinto puesto)**."
    },
    {
        "id": 7,
        "title": "El enigma de las bayas pares e impares de Bulbasaur",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Bulbasaur recolecta bayas en el bosque y las reparte en cinco canastas. Cada canasta contiene una cantidad diferente de bayas: 14, 27, 36, 49 y 52 bayas.\n\nClasifica cada uno de estos cinco números indicando si es un número par o un número impar.",
        "datos": "Cantidades de bayas en las canastas: 14, 27, 36, 49 y 52.",
        "operaciones": "Para saber si un número es par o impar observamos únicamente su última cifra (la cifra de las unidades):\n- Es par si termina en 0, 2, 4, 6 u 8.\n- Es impar si termina en 1, 3, 5, 7 o 9.\nEvaluamos uno a uno:\n- 14: termina en 4 -> Par.\n- 27: termina en 7 -> Impar.\n- 36: termina en 6 -> Par.\n- 49: termina en 9 -> Impar.\n- 52: termina en 2 -> Par.",
        "respuesta": "Los números pares son **14, 36 y 52**, y los números impares son **27 y 49**."
    },
    {
        "id": 8,
        "title": "Ordenando las cartas Pokémon de Ritchie",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Ritchie tiene cuatro cartas especiales de combate con diferentes niveles de potencia numérica: 425, 245, 542 y 254 puntos de combate.\n\nOrdena estos cuatro números de menor a mayor utilizando el símbolo < (menor que).",
        "datos": "Puntuaciones de las cartas: 425, 245, 542 y 254.",
        "operaciones": "Comparamos las cifras de las centenas primero:\n- Los números con 2 centenas son 245 y 254. Comparamos sus decenas: 4 decenas es menor que 5 decenas, por lo que 245 < 254.\n- El número con 4 centenas es 425.\n- El número con 5 centenas es 542.\nUniendo las comparaciones de menor a mayor obtenemos: 245 < 254 < 425 < 542.",
        "respuesta": "El orden de menor a mayor es **245 < 254 < 425 < 542**."
    },
    {
        "id": 9,
        "title": "Las fichas del Casino de Ciudad Azulona",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Tras superar una serie de minijuegos lógicos en Ciudad Azulona, un entrenador consigue un premio de 742 fichas especiales para canjear por premios.\n\n¿Cuál es el valor posicional de la cifra 7 en el número 742? Explica cuántas unidades representa.",
        "datos": "Número total de fichas: 742.",
        "operaciones": "Identificamos la posición que ocupa cada dígito en el número 742:\n- El 2 ocupa la posición de las unidades: 2 unidades.\n- El 4 ocupa la posición de las decenas: 4 decenas = 40 unidades.\n- El 7 ocupa la posición de las centenas: 7 centenas = 700 unidades.",
        "respuesta": "La cifra 7 ocupa el lugar de las centenas y su valor es de **700 unidades (7 centenas)**."
    },
    {
        "id": 10,
        "title": "El número secreto del maletín del Profesor Oak",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "El maletín de campo del Profesor Oak está protegido por un candado numérico de 3 cifras. Para recordar la combinación, el profesor anotó la siguiente pista en su libreta: 'El código secreto está compuesto por 4 centenas, 6 decenas y 9 unidades'.\n\n¿Cuál es el número de 3 cifras que abre el maletín del Profesor Oak?",
        "datos": "Pista del candado: 4 centenas, 6 decenas y 9 unidades.",
        "operaciones": "Convertimos cada orden posicional a unidades y realizamos la suma:\n- 4 centenas = 400\n- 6 decenas = 60\n- 9 unidades = 9\nSumamos: 400 + 60 + 9 = 469.",
        "respuesta": "El número secreto que abre el maletín es el **469**."
    },
    {
        "id": 11,
        "title": "Los Caterpie del Bosque Verde",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "El guarda forestal del Bosque Verde lleva un censo exhaustivo de los Pokémon insecto. En su última revisión registró exactamente 699 Caterpie viviendo entre las ramas. Si hoy por la mañana ha eclosionado un huevo y ha nacido un nuevo Caterpie, ¿cuántos Caterpie hay ahora en total?\n\nCalcula el número posterior a 699 sumando 1 unidad.",
        "datos": "Caterpie iniciales en el censo: 699; nace 1 Caterpie más.",
        "operaciones": "Sumamos 1 unidad a 699 para encontrar su número consecutivo:\n  699 + 1 = 700\nAl sumar 1 unidad a 9 unidades obtenemos 10 unidades (0 y nos llevamos 1 decena). Al sumar 1 decena a 9 decenas obtenemos 10 decenas (0 y nos llevamos 1 centena). Al sumar 1 centena a 6 centenas obtenemos 7 centenas (700).",
        "respuesta": "Ahora hay en total **700 Caterpie** en el Bosque Verde."
    },
    {
        "id": 12,
        "title": "La fila de aspirantes en el Gimnasio Plateada",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Una docena de entrenadores novatos esperan pacientemente en fila para retar al Líder Brock. Brock acaba de felicitar al 7º aspirante (séptimo) tras finalizar su combate.\n\n¿Qué número ordinal le corresponde al siguiente entrenador que entrará a la arena de combate?",
        "datos": "Último aspirante atendido: 7º (séptimo).",
        "operaciones": "La sucesión de números ordinales del 1º al 10º es: primero (1º), segundo (2º), tercero (3º), cuarto (4º), quinto (5º), sexto (6º), séptimo (7º), octavo (8º), noveno (9º) y décimo (10º). El ordinal que sigue inmediatamente a séptimo (7º) es octavo (8º).",
        "respuesta": "Al siguiente entrenador le corresponde entrar en **8º lugar (octavo puesto)**."
    },
    {
        "id": 13,
        "title": "La balanza de Snorlax y sus provisiones",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "La Enfermera Joy comprueba en el registro médico que un Snorlax adulto pesa 850 kilogramos, mientras que un cargamento gigante de comida para Pokémon pesa 805 kilogramos.\n\nCompara los dos números, 850 y 805, utilizando el signo de mayor que (>) o menor que (<).",
        "datos": "Peso de Snorlax: 850 kg; peso del cargamento: 805 kg.",
        "operaciones": "Comparamos las cifras de izquierda a derecha:\n- Centenas: ambos números tienen 8 centenas (8 = 8).\n- Decenas: el primer número tiene 5 decenas y el segundo número tiene 0 decenas. Como 5 es mayor que 0 (5 > 0), el número 850 es mayor que 805.",
        "respuesta": "La comparación es **850 > 805** (850 kg es mayor que 805 kg)."
    },
    {
        "id": 14,
        "title": "Los sellos conmemorativos de la Liga Pokémon",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "Ash atesora un álbum con sellos conmemorativos de los torneos oficiales de Kanto y ha conseguido reunir 523 sellos diferentes.\n\nEscribe cómo se lee en palabras el número 523 y descompónlo según el valor de sus cifras.",
        "datos": "Cantidad de sellos coleccionados: 523.",
        "operaciones": "1. Escritura en palabras: 523 se escribe 'quinientos veintitrés'.\n2. Descomposición posicional:\n   - 5 centenas = 500 unidades\n   - 2 decenas = 20 unidades\n   - 3 unidades = 3 unidades\n   523 = 500 + 20 + 3.",
        "respuesta": "El número 523 se lee **quinientos veintitrés** y se descompone en **500 + 20 + 3** (**5 centenas, 2 decenas y 3 unidades**)."
    },
    {
        "id": 15,
        "title": "Entradas pares para el Torneo Añil",
        "subcategory": "Subcategoría 1: Numeración, Descomposición y Valor Posicional",
        "text": "La taquilla del estadio de la Meseta Añil reparte invitaciones especiales para ver los combates. Los números impresos en las entradas son: 88, 103, 240, 317 y 562. La organización anuncia por megafonía que solo las entradas con número par tienen acceso a la primera fila.\n\n¿Cuáles de estos cinco números de entrada permiten acceder a la primera fila?",
        "datos": "Números de entrada: 88, 103, 240, 317 y 562.",
        "operaciones": "Identificamos los números pares observando si su última cifra termina en 0, 2, 4, 6 u 8:\n- 88: termina en 8 -> Par (permite el acceso).\n- 103: termina en 3 -> Impar.\n- 240: termina en 0 -> Par (permite el acceso).\n- 317: termina en 7 -> Impar.\n- 562: termina en 2 -> Par (permite el acceso).",
        "respuesta": "Las entradas que permiten acceder a la primera fila son los números pares **88, 240 y 562**."
    },

    # Subcategoría 2: Operaciones Aritméticas y Cálculo Mental (Problemas 16 al 35)
    {
        "id": 16,
        "title": "La recolección de Poké Balls de Ash y Misty",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Ash y Misty revisan sus mochilas para ver cuántas Poké Balls tienen antes de adentrarse en la hierba alta. Ash tiene 142 Poké Balls y Misty tiene 35 Poké Balls.\n\n¿Cuántas Poké Balls tienen entre los dos en total? (Realiza una suma sin llevada).",
        "datos": "Poké Balls de Ash: 142; Poké Balls de Misty: 35.",
        "operaciones": "Colocamos los sumandos alineando unidades, decenas y centenas:\n   142\n +  35\n -----\nSumamos columna a columna sin llevada:\n- Unidades: 2 + 5 = 7\n- Decenas: 4 + 3 = 7\n- Centenas: 1 + 0 = 1\nResultado: 177.",
        "respuesta": "Entre los dos tienen en total **177 Poké Balls**."
    },
    {
        "id": 17,
        "title": "Atendiendo Pokémon en el Centro Pokémon de Ciudad Carmín",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "La Enfermera Joy del Centro Pokémon de Ciudad Carmín ha tenido un día muy ajetreado. Por la mañana atendió a 158 Pokémon heridos en combates de ruta, y por la tarde recibió a 27 Pokémon más traídos por otros entrenadores.\n\n¿A cuántos Pokémon atendió la Enfermera Joy a lo largo de todo el día?",
        "datos": "Pokémon atendidos por la mañana: 158; Pokémon atendidos por la tarde: 27.",
        "operaciones": "Planteamos la suma con llevada a la decena:\n   158\n +  27\n -----\n- Unidades: 8 + 7 = 15. Escribimos 5 en las unidades y nos llevamos 1 decena a la siguiente columna.\n- Decenas: 5 + 2 = 7, más 1 que nos llevábamos = 8 decenas.\n- Centenas: 1 centena.\nResultado: 185.",
        "respuesta": "La Enfermera Joy atendió en total a **185 Pokémon**."
    },
    {
        "id": 18,
        "title": "El botín de bayas del Team Rocket recuperado",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "La Agente Jenny intercepta al Team Rocket y recupera dos grandes sacos de bayas robadas. El primer saco contiene 264 bayas y el segundo saco contiene 183 bayas.\n\n¿Cuántas bayas recuperó la Agente Jenny en total?",
        "datos": "Bayas en el primer saco: 264; bayas en el segundo saco: 183.",
        "operaciones": "Planteamos la suma con llevada a la centena:\n   264\n + 183\n -----\n- Unidades: 4 + 3 = 7 unidades.\n- Decenas: 6 + 8 = 14 decenas. Escribimos 4 en las decenas y nos llevamos 1 centena.\n- Centenas: 2 + 1 = 3, más 1 que nos llevábamos = 4 centenas.\nResultado: 447.",
        "respuesta": "La Agente Jenny recuperó en total **447 bayas**."
    },
    {
        "id": 19,
        "title": "Gastando Safari Balls en la Zona Safari",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Ash entra a la Zona Safari de Ciudad Fucsia con 286 Safari Balls en su caja de explorador. Durante la expedición utiliza 54 Safari Balls intentando capturar una manada de Tauros.\n\n¿Cuántas Safari Balls le quedan a Ash al finalizar la jornada?",
        "datos": "Safari Balls iniciales: 286; Safari Balls utilizadas: 54.",
        "operaciones": "Realizamos la resta alineando los números por columnas (resta sin llevada):\n   286\n -  54\n -----\n- Unidades: 6 - 4 = 2\n- Decenas: 8 - 5 = 3\n- Centenas: 2 - 0 = 2\nResultado: 232.",
        "respuesta": "A Ash le quedan **232 Safari Balls**."
    },
    {
        "id": 20,
        "title": "El consumo de Pociones en el Monte Moon",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Brock parte a explorar las oscuras cavernas del Monte Moon llevando 145 frascos de poción en su mochila. Tras varios encuentros con Pokémon salvajes, utiliza 28 frascos para restaurar a sus amigos.\n\n¿Cuántos frascos de poción le quedan a Brock en la mochila?",
        "datos": "Pociones iniciales: 145; Pociones usadas: 28.",
        "operaciones": "Planteamos una resta con llevada en la cifra de las unidades:\n   145\n -  28\n -----\n- Unidades: Como a 5 no le podemos restar 8, transformamos 1 decena en 10 unidades: 15 - 8 = 7 unidades.\n- Decenas: En las decenas nos quedan 3 decenas. Restamos: 3 - 2 = 1 decena.\n- Centenas: 1 centena.\nResultado: 117.",
        "respuesta": "A Brock le quedan **117 frascos de poción**."
    },
    {
        "id": 21,
        "title": "Puntos de resistencia en el Gimnasio de Ciudad Celeste",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "El equipo de combate de Misty tiene un escudo defensivo especial que comienza con 324 puntos de resistencia. Durante un intenso combate contra un retador, el escudo recibe impactos que le restan 158 puntos.\n\n¿Cuántos puntos de resistencia le quedan al escudo defensivo?",
        "datos": "Puntos de resistencia iniciales: 324; Puntos restados: 158.",
        "operaciones": "Planteamos la resta con doble llevada:\n   324\n - 158\n -----\n- Unidades: a 4 no le podemos restar 8; cambiamos 1 decena (quedan 1 decena): 14 - 8 = 6 unidades.\n- Decenas: a 1 no le podemos restar 5; cambiamos 1 centena (quedan 2 centenas): 11 - 5 = 6 decenas.\n- Centenas: 2 - 1 = 1 centena.\nResultado: 166.",
        "respuesta": "Al escudo le quedan **166 puntos de resistencia**."
    },
    {
        "id": 22,
        "title": "El doble de bayas Zreza de Pikachu",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Pikachu ha recolectado 24 deliciosas bayas Zreza para preparar un refrigerio. Su amigo Raichu, que es más grande y rápido, ha recolectado exactamente el doble de bayas que Pikachu.\n\n¿Cuántas bayas Zreza ha recolectado Raichu?",
        "datos": "Bayas de Pikachu: 24; Raichu tiene el doble.",
        "operaciones": "Para calcular el doble de una cantidad sumamos el número consigo mismo dos veces (o multiplicamos por 2):\n  24 + 24 = 48 (o 24 x 2 = 48)\n- Unidades: 4 + 4 = 8\n- Decenas: 2 + 2 = 4\nTotal: 48.",
        "respuesta": "Raichu ha recolectado **48 bayas Zreza**."
    },
    {
        "id": 23,
        "title": "Compartiendo bayas Meloc con Eevee",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Serena tiene un cesto con 36 bayas Meloc recién cosechadas. Para premiar a su querido Eevee tras una gran exhibición, le regala exactamente la mitad de las bayas del cesto.\n\n¿Cuántas bayas Meloc recibe Eevee?",
        "datos": "Total de bayas: 36; Eevee recibe la mitad.",
        "operaciones": "Calcular la mitad consiste en repartir una cantidad en dos partes exactamente iguales:\n  36 = 18 + 18 (o 36 : 2 = 18)\nPodemos descomponer 36 en 30 + 6:\n- La mitad de 30 es 15.\n- La mitad de 6 es 3.\n- Sumamos: 15 + 3 = 18.",
        "respuesta": "Eevee recibe **18 bayas Meloc**."
    },
    {
        "id": 24,
        "title": "Los nidos de Pidgey en los robles de Pueblo Paleta",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "En un gran roble centenario de Pueblo Paleta hay 6 nidos de Pidgey bien resguardados del viento. Si en cada uno de los 6 nidos hay exactamente 2 pequeños huevos, ¿cuántos huevos hay en total en el árbol?\n\nExpresa el resultado mediante una suma repetida de sumandos iguales y mediante multiplicación.",
        "datos": "Cantidad de nidos: 6; huevos en cada nido: 2.",
        "operaciones": "Calculamos la suma repetida del número 2 un total de 6 veces:\n  2 + 2 + 2 + 2 + 2 + 2 = 12\nEn forma de multiplicación (tabla del 2): 6 x 2 = 12.",
        "respuesta": "En el árbol hay en total **12 huevos de Pidgey** (6 x 2 = **12**)."
    },
    {
        "id": 25,
        "title": "Las raciones de galletas Pokémon de Brock",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "A la hora de la merienda, Brock prepara 5 comederos individuales para los Pokémon del equipo. En cada comedero coloca exactamente 3 galletas energéticas con sabor a miel.\n\n¿Cuántas galletas energéticas sirvió Brock en total?",
        "datos": "Cantidad de comederos: 5; galletas por comedero: 3.",
        "operaciones": "Planteamos la suma repetida de 3 galletas en 5 platos:\n  3 + 3 + 3 + 3 + 3 = 15\nEn forma de multiplicación (tabla del 3): 5 x 3 = 15.",
        "respuesta": "Brock sirvió en total **15 galletas energéticas**."
    },
    {
        "id": 26,
        "title": "Cajas de Poké Balls en el almacén de Silph S.A.",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Un empleado de Silph S.A. en Ciudad Azafrán apila 7 cajas de material en una estantería del almacén. Cada una de las 7 cajas contiene en su interior 5 Poké Balls recién fabricadas.\n\n¿Cuántas Poké Balls hay en total en las 7 cajas?",
        "datos": "Cantidad de cajas: 7; Poké Balls por caja: 5.",
        "operaciones": "Aplicamos la suma repetida o la tabla del 5:\n  5 + 5 + 5 + 5 + 5 + 5 + 5 = 35\nMediante multiplicación: 7 x 5 = 35.",
        "respuesta": "En las 7 cajas hay en total **35 Poké Balls**."
    },
    {
        "id": 27,
        "title": "Los paquetes de pegatinas de la Enfermera Joy",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Para premiar a los entrenadores que cuidan con cariño a sus Pokémon, la Enfermera Joy tiene guardados 8 paquetes de pegatinas brillantes. Cada paquete contiene 10 pegatinas coleccionables.\n\n¿Cuántas pegatinas tiene en total la Enfermera Joy?",
        "datos": "Cantidad de paquetes: 8; pegatinas por paquete: 10.",
        "operaciones": "Contamos de 10 en 10 un total de 8 veces (tabla del 10):\n  10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 = 80\nMediante multiplicación: 8 x 10 = 80.",
        "respuesta": "La Enfermera Joy tiene en total **80 pegatinas brillantes**."
    },
    {
        "id": 28,
        "title": "Los amigos del 100 en la hucha de Ash",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Ash está ahorrando monedas para comprar un kit de mantenimiento de Poké Balls que cuesta exactamente 100 monedas. Al abrir su hucha con forma de Pikachu, cuenta que ya tiene 65 monedas reunidas.\n\n¿Cuántas monedas le faltan a Ash para alcanzar las 100 monedas?",
        "datos": "Monedas actuales en la hucha: 65; Meta a alcanzar: 100 monedas.",
        "operaciones": "Buscamos el complementario o amigo del 100 mediante una resta:\n  100 - 65\n- Pensamos por cálculo mental: de 65 a 70 van 5 monedas; de 70 a 100 van 30 monedas.\n- 30 + 5 = 35 monedas (o 100 - 65 = 35).",
        "respuesta": "A Ash le faltan **35 monedas** para alcanzar las 100 monedas."
    },
    {
        "id": 29,
        "title": "La reserva de medicinas de Ash",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "En el botiquín de viaje de Ash hay varios tipos de pociones organizadas por frascos: tiene 25 pociones normales, 14 superpociones y 31 pociones máximas.\n\n¿Cuántas pociones tiene Ash en total en su botiquín?",
        "datos": "Pociones normales: 25; superpociones: 14; pociones máximas: 31.",
        "operaciones": "Sumamos las tres cantidades alineándolas:\n   25\n   14\n + 31\n -----\n- Unidades: 5 + 4 = 9; 9 + 1 = 10 (escribimos 0 y nos llevamos 1 decena).\n- Decenas: 2 + 1 + 3 = 6; más 1 que nos llevábamos = 7 decenas.\nResultado: 70.",
        "respuesta": "Ash tiene en total **70 pociones** en su botiquín."
    },
    {
        "id": 30,
        "title": "El triple de bayas Safre para Vaporeon",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Vaporeon nada con entusiasmo en el lago y su entrenadora le da 12 bayas Safre de premio. Al día siguiente, tras completar un entrenamiento acuático extraordinario, su entrenadora le ofrece el triple de bayas.\n\n¿Cuántas bayas Safre recibe Vaporeon el segundo día?",
        "datos": "Bayas el primer día: 12; el segundo día recibe el triple.",
        "operaciones": "El triple de un número se calcula sumando dicho número tres veces consigo mismo (o multiplicándolo por 3):\n  12 + 12 + 12 = 36 (o 12 x 3 = 36)\n- Unidades: 2 + 2 + 2 = 6\n- Decenas: 1 + 1 + 1 = 3\nTotal: 36.",
        "respuesta": "Vaporeon recibe **36 bayas Safre** el segundo día."
    },
    {
        "id": 31,
        "title": "La mitad de la energía luminosa de Charmander",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "La llama de la cola de Charmander resplandece al comenzar la noche con 50 puntos de energía luminosa. Después de encender una hoguera en el campamento, su llama consume la mitad de esos puntos.\n\n¿Cuántos puntos de energía luminosa le quedan a la llama de Charmander?",
        "datos": "Puntos de energía iniciales: 50; se consume la mitad.",
        "operaciones": "Calculamos la mitad de 50 dividiendo en dos partes iguales:\n  50 = 25 + 25 (o 50 : 2 = 25)\n- La mitad de 5 decenas (50) son 2 decenas y media = 25 unidades.",
        "respuesta": "A la llama de Charmander le quedan **25 puntos de energía luminosa**."
    },
    {
        "id": 32,
        "title": "Donando medicinas al refugio de Pueblo Lavanda",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "El laboratorio central de Silph S.A. produce una remesa especial de 500 frascos de tónico reconstituyente. Para colaborar con el refugio de Pokémon huérfanos de Pueblo Lavanda, envían 135 frascos de donación.\n\n¿Cuántos frascos de tónico reconstituyente le quedan al laboratorio tras la donación?",
        "datos": "Frascos iniciales: 500; Frascos donados: 135.",
        "operaciones": "Planteamos una resta con ceros en el minuendo:\n   500\n - 135\n -----\n- Descomponemos 500 en 4 centenas, 9 decenas y 10 unidades:\n  * Unidades: 10 - 5 = 5\n  * Decenas: 9 - 3 = 6\n  * Centenas: 4 - 1 = 3\nResultado: 365.",
        "respuesta": "Al laboratorio le quedan **365 frascos de tónico reconstituyente**."
    },
    {
        "id": 33,
        "title": "Las filas de Magikarp en el Lago Furia",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "En las aguas tranquilas del Lago Furia nadan varios grupos de Magikarp alineados de forma sincronizada. Se forman 4 filas y en cada una de las 4 filas nadan exactamente 5 Magikarp.\n\n¿Cuántos Magikarp nadan en total formando las filas en el lago?",
        "datos": "Cantidad de filas: 4; Magikarp en cada fila: 5.",
        "operaciones": "Calculamos el producto mediante suma reiterada o la tabla del 5:\n  5 + 5 + 5 + 5 = 20\nMultiplicación: 4 x 5 = 20.",
        "respuesta": "En el lago nadan en total **20 Magikarp**."
    },
    {
        "id": 34,
        "title": "El inventario de Antídotos de la Tienda de Ciudad Verde",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "La Tienda Pokémon de Ciudad Verde recibe un gran cargamento de antídotos para tratar a los Pokémon picados por Beedrill. En una primera furgoneta llegan 387 antídotos y en una segunda furgoneta llegan 245 antídotos.\n\n¿Cuántos antídotos ha recibido en total la tienda?",
        "datos": "Antídotos en la primera furgoneta: 387; en la segunda furgoneta: 245.",
        "operaciones": "Planteamos la suma con llevadas en unidades y decenas:\n   387\n + 245\n -----\n- Unidades: 7 + 5 = 12 (escribimos 2 y nos llevamos 1 a las decenas).\n- Decenas: 8 + 4 = 12, más 1 que nos llevábamos = 13 (escribimos 3 y nos llevamos 1 a las centenas).\n- Centenas: 3 + 2 = 5, más 1 que nos llevábamos = 6 centenas.\nResultado: 632.",
        "respuesta": "La tienda ha recibido en total **632 antídotos**."
    },
    {
        "id": 35,
        "title": "Las bengalas del festival de Charizard",
        "subcategory": "Subcategoría 2: Operaciones Aritméticas y Cálculo Mental",
        "text": "Para dar comienzo a la ceremonia de clausura de la Liga Pokémon se han preparado 600 bengalas de chispas de colores. Durante el espectáculo de vuelo de los Charizard se encienden 240 bengalas.\n\n¿Cuántas bengalas quedan sin encender en las cajas de seguridad?",
        "datos": "Bengalas iniciales: 600; Bengalas encendidas: 240.",
        "operaciones": "Efectuamos la resta:\n   600\n - 240\n -----\n- Unidades: 0 - 0 = 0\n- Decenas: a 0 no le podemos restar 4; transformamos 1 centena en 10 decenas (quedan 5 centenas): 10 - 4 = 6 decenas.\n- Centenas: 5 - 2 = 3 centenas.\nResultado: 360.",
        "respuesta": "Quedan sin encender **360 bengalas**."
    },

    # Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero (Problemas 36 al 50)
    {
        "id": 36,
        "title": "Midiendo la altura de Bellsprout y Oddish en centímetros",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "En el invernadero de la Líder Erika, los alumnos miden con una regla graduada la altura de dos simpáticos Pokémon de tipo Planta. Bellsprout mide 70 centímetros de altura, mientras que Oddish mide 40 centímetros.\n\n¿Cuántos centímetros más alto es Bellsprout que Oddish?",
        "datos": "Altura de Bellsprout: 70 cm; Altura de Oddish: 40 cm.",
        "operaciones": "Restamos la altura menor de la mayor para hallar la diferencia:\n  70 - 40 = 30 centímetros.",
        "respuesta": "Bellsprout es **30 centímetros** más alto que Oddish."
    },
    {
        "id": 37,
        "title": "La cuerda de rescate en la Cueva Diglett",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Para descender por una grieta profunda de la Cueva Diglett, Brock une dos cuerdas de escalada resistentes. El primer tramo de cuerda mide 15 metros de longitud y el segundo tramo mide 25 metros de longitud.\n\n¿Cuánto mide la cuerda completa una vez atados ambos tramos?",
        "datos": "Longitud del primer tramo: 15 m; Longitud del segundo tramo: 25 m.",
        "operaciones": "Sumamos ambas longitudes en metros:\n  15 + 25 = 40 metros\n- Unidades: 5 + 5 = 10 (nos llevamos 1)\n- Decenas: 1 + 2 + 1 = 4.",
        "respuesta": "La cuerda completa mide **40 metros** de longitud."
    },
    {
        "id": 38,
        "title": "El peso de Snorlax en la báscula del Centro Pokémon",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Snorlax sube a la báscula de pesaje del Centro Pokémon y la aguja marca exactamente 460 kilogramos. Justo después, la Enfermera Joy le sirve un gran almuerzo de bayas y verduras que pesa 40 kilogramos, y Snorlax se lo come todo de inmediato.\n\n¿Cuántos kilogramos marca la báscula ahora con Snorlax y su comida en el estómago?",
        "datos": "Peso inicial de Snorlax: 460 kg; Peso de la comida: 40 kg.",
        "operaciones": "Sumamos los kilogramos:\n  460 + 40 = 500 kg\n- Decenas: 6 decenas + 4 decenas = 10 decenas = 1 centena.\n- 4 centenas + 1 centena = 5 centenas (500).",
        "respuesta": "La báscula marca ahora **500 kilogramos**."
    },
    {
        "id": 39,
        "title": "El cubo de agua fresca para Squirtle",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Misty quiere refrescar a Squirtle con un barreño grande que tiene una capacidad total de 10 litros de agua. Utilizando una jarra medidora, ya ha vertido 4 litros dentro del barreño.\n\n¿Cuántos litros de agua le faltan para llenar el barreño por completo?",
        "datos": "Capacidad del barreño: 10 litros; Agua vertida: 4 litros.",
        "operaciones": "Restamos la cantidad actual de la capacidad máxima:\n  10 - 4 = 6 litros.",
        "respuesta": "Le faltan **6 litros** de agua para llenar el barreño."
    },
    {
        "id": 40,
        "title": "La hora de salida hacia Ciudad Fucsia",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "El autobús de la línea regional parte de Ciudad Carmín en dirección a Ciudad Fucsia exactamente a las 9:00 en punto de la mañana. Según el panel de horarios, el trayecto dura exactamente 1 hora completa.\n\n¿A qué hora llegará el autobús a su destino en Ciudad Fucsia?",
        "datos": "Hora de partida: 9:00 en punto; Tiempo de viaje: 1 hora.",
        "operaciones": "Sumamos 1 hora a la hora inicial:\n  9:00 + 1:00 = 10:00.",
        "respuesta": "El autobús llegará a Ciudad Fucsia a las **10:00 en punto** de la mañana."
    },
    {
        "id": 41,
        "title": "La siesta de Pikachu",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Pikachu se queda profundamente dormido a la sombra de un manzano a las 3:00 en punto de la tarde. Se despierta descansado y lleno de energía cuando las agujas del reloj marcan las 3:30 (las tres y media).\n\n¿Cuántos minutos duró la siesta de Pikachu?",
        "datos": "Hora de inicio de la siesta: 3:00; Hora de despertar: 3:30.",
        "operaciones": "Calculamos la diferencia de tiempo en minutos:\n- A las 3:00 han transcurrido 0 minutos de la hora.\n- A las 3:30 han transcurrido 30 minutos.\n- 30 - 0 = 30 minutos (media hora = 30 minutos).",
        "respuesta": "La siesta de Pikachu duró **30 minutos** (media hora)."
    },
    {
        "id": 42,
        "title": "Comprando una Poké Ball en la Tienda Pokémon",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "En el mostrador de la Tienda Pokémon, una Poké Ball estándar cuesta 2 euros. Ash decide comprar una y le entrega al dependiente un billete de 5 euros.\n\n¿Cuánto dinero debe devolverle de cambio el dependiente?",
        "datos": "Precio de la Poké Ball: 2 euros; Dinero entregado: billete de 5 euros.",
        "operaciones": "Restamos el precio del artículo del dinero entregado:\n  5 - 2 = 3 euros.",
        "respuesta": "El dependiente debe devolverle **3 euros** de cambio."
    },
    {
        "id": 43,
        "title": "Monedas de céntimo para una Baya Aranja",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Una Baya Aranja cuesta 80 céntimos de euro en el puesto de frutas de Ciudad Azafrán. Misty revisa su monedero y saca 1 moneda de 50 céntimos y 2 monedas de 20 céntimos.\n\n¿Cuánto dinero tiene Misty en total y cuántos céntimos le sobrarán tras pagar la baya?",
        "datos": "Precio de la baya: 80 céntimos; Monedas de Misty: una de 50 céntimos y dos de 20 céntimos.",
        "operaciones": "1. Calculamos el dinero total que tiene Misty sumando las monedas:\n   50 + 20 + 20 = 90 céntimos de euro.\n2. Calculamos el cambio que le sobra:\n   90 - 80 = 10 céntimos de euro.",
        "respuesta": "Misty tiene en total 90 céntimos y le sobrarán **10 céntimos de euro**."
    },
    {
        "id": 44,
        "title": "Midiendo la cola de Pikachu con una regla",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Al comenzar la primavera, Ash midió la característica cola en forma de rayo de Pikachu y anotó que medía 18 centímetros. Al llegar el otoño, la cola ha crecido 5 centímetros más.\n\n¿Cuánto mide la cola de Pikachu ahora?",
        "datos": "Longitud inicial: 18 cm; Crecimiento: 5 cm.",
        "operaciones": "Sumamos ambas medidas en centímetros:\n  18 + 5 = 23 centímetros.",
        "respuesta": "La cola de Pikachu mide ahora **23 centímetros**."
    },
    {
        "id": 45,
        "title": "El peso de la mochila de montañero de Brock",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "La mochila de senderismo de Brock pesa 2 kilogramos cuando está completamente vacía. Brock introduce dentro 6 kilogramos de alimentos secos y una cantimplora llena de agua que pesa 3 kilogramos.\n\n¿Cuánto pesa en total la mochila de Brock con toda la carga dentro?",
        "datos": "Mochila vacía: 2 kg; Alimentos: 6 kg; Cantimplora: 3 kg.",
        "operaciones": "Sumamos los tres pesos en kilogramos:\n  2 + 6 + 3 = 11 kg\n- 2 + 6 = 8\n- 8 + 3 = 11.",
        "respuesta": "La mochila de Brock pesa en total **11 kilogramos**."
    },
    {
        "id": 46,
        "title": "Las jarras de poción líquida de la Enfermera Joy",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "La Enfermera Joy prepara medicina líquida concentrada para rellenar los dispensadores del hospital. Ha llenado 3 jarras grandes y en cada jarra caben exactamente 2 litros de medicina líquida.\n\n¿Cuántos litros de medicina líquida ha preparado en total?",
        "datos": "Cantidad de jarras: 3; Capacidad de cada jarra: 2 litros.",
        "operaciones": "Multiplicamos la cantidad de jarras por los litros de cada una (o suma repetida):\n  2 + 2 + 2 = 6 litros (o 3 x 2 = 6 litros).",
        "respuesta": "La Enfermera Joy ha preparado en total **6 litros** de medicina líquida."
    },
    {
        "id": 47,
        "title": "El horario del Gimnasio de Ciudad Carmín",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "El Gimnasio de Ciudad Carmín abre sus puertas a los retadores por la mañana a las 8:30 (ocho y media). Los combates matutinos se detienen a las 11:30 (once y media) para descansar y almorzar.\n\n¿Cuántas horas seguidas permanece abierto el gimnasio durante la mañana?",
        "datos": "Hora de apertura: 8:30; Hora de pausa: 11:30.",
        "operaciones": "Calculamos la diferencia entre las dos horas:\n- Como los minutos coinciden (:30), restamos las horas:\n  11 - 8 = 3 horas\n(De 8:30 a 9:30 es 1 hora; a 10:30 son 2 horas; a 11:30 son 3 horas).",
        "respuesta": "El gimnasio permanece abierto durante **3 horas** seguidas."
    },
    {
        "id": 48,
        "title": "Comprando una Super Ball y un Antídoto",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "En la Tienda Pokémon, una Super Ball cuesta 6 euros y un frasco de Antídoto cuesta 3 euros. Ash compra uno de cada y paga en caja entregando un billete de 10 euros.\n\n¿Cuánto dinero gasta Ash en total y cuánto le devuelven de cambio?",
        "datos": "Precio de la Super Ball: 6 €; Precio del Antídoto: 3 €; Paga con: billete de 10 €.",
        "operaciones": "1. Calculamos el gasto total sumando ambos precios:\n   6 + 3 = 9 euros.\n2. Calculamos el cambio restando el gasto del billete entregado:\n   10 - 9 = 1 euro.",
        "respuesta": "Ash gasta 9 euros en total y le devuelven **1 euro** de cambio."
    },
    {
        "id": 49,
        "title": "El calendario de entrenamiento semanal de Ash",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "Ash ha organizado su rutina semanal de modo que entrena intensamente de lunes a viernes, y descansa los sábados y los domingos para que sus Pokémon jueguen en el parque.\n\n¿Cuántos días entrena Ash a la semana y cuántos días se toma de descanso?",
        "datos": "Semana completa: 7 días.",
        "operaciones": "Contamos los días asignados a cada actividad:\n- Días de entrenamiento: Lunes, Martes, Miércoles, Jueves y Viernes = 5 días.\n- Días de descanso: Sábado y Domingo = 2 días.\nComprobación: 5 + 2 = 7 días de la semana.",
        "respuesta": "Ash entrena **5 días** y descansa **2 días** a la semana."
    },
    {
        "id": 50,
        "title": "La duración de la temporada clasificatoria de la Liga",
        "subcategory": "Subcategoría 3: Magnitudes, Unidades de Medida, Tiempo y Dinero",
        "text": "La temporada oficial de torneos de Kanto abre su plazo de inscripción el 1 de marzo y concluye las rondas el 31 de mayo.\n\n¿Durante cuántos meses completos se extiende la temporada clasificatoria? Nómbralos en orden.",
        "datos": "Fecha de inicio: 1 de marzo; Fecha de fin: 31 de mayo.",
        "operaciones": "Contamos los meses comprendidos entre ambas fechas:\n1. Marzo (mes completo)\n2. Abril (mes completo)\n3. Mayo (mes completo)\nTotal de meses: 3.",
        "respuesta": "La temporada se extiende durante **3 meses** completos (**marzo, abril y mayo**)."
    },

    # Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio (Problemas 51 al 65)
    {
        "id": 51,
        "title": "La silueta circular de la Poké Ball",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "El Profesor Oak dibuja en la pizarra la silueta plana de una Poké Ball vista de frente para explicar cómo funciona su botón central.\n\n¿Qué figura geométrica plana es la silueta de una Poké Ball? ¿Tiene lados rectos o vértices?",
        "datos": "Silueta plana perfectamente redonda.",
        "operaciones": "Una figura geométrica plana limitada por una línea curva cerrada cuyos puntos están a la misma distancia del centro se llama círculo.\n- Los círculos no tienen lados rectos.\n- Al no tener lados rectos que se corten, tampoco tienen vértices.",
        "respuesta": "La silueta es un **círculo**, el cual **no tiene lados rectos ni vértices** (0 lados rectos y 0 vértices)."
    },
    {
        "id": 52,
        "title": "La señal triangular de advertencia en la Ruta Volcán",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En el camino hacia la Isla Canela, Ash encuentra un cartel de advertencia de paso de Magmar. El cartel tiene forma de triángulo equilátero.\n\n¿Cuántos lados rectos y cuántos vértices tiene este cartel triangular?",
        "datos": "Forma geométrica del cartel: triángulo.",
        "operaciones": "Por definición geométrica, cualquier triángulo es un polígono de 3 lados rectos y 3 vértices (las esquinas donde se unen los lados).",
        "respuesta": "El cartel triangular tiene **3 lados rectos y 3 vértices**."
    },
    {
        "id": 53,
        "title": "La arena de combate cuadrada del Gimnasio Plateada",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "El cuadrilátero donde lucha Onix en el Gimnasio de Ciudad Plateada es una superficie plana con forma de cuadrado perfecto.\n\n¿Cuántos lados tiene el cuadrado, cómo son sus longitudes entre sí y cuántos vértices posee?",
        "datos": "Figura geométrica: cuadrado.",
        "operaciones": "Un cuadrado es un polígono de cuatro lados que posee propiedades fijas:\n- Tiene 4 lados de exactamente la misma longitud (4 lados iguales).\n- Tiene 4 vértices (4 esquinas en ángulo recto).",
        "respuesta": "El campo cuadrado tiene **4 lados iguales y 4 vértices**."
    },
    {
        "id": 54,
        "title": "La pantalla rectangular de la Pokédex",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "La pantalla luminosa donde Ash consulta los datos de los Pokémon tiene forma de rectángulo, con dos lados largos horizontales y dos lados cortos verticales.\n\n¿Cuántos lados y cuántos vértices tiene la pantalla rectangular?",
        "datos": "Forma geométrica de la pantalla: rectángulo.",
        "operaciones": "Un rectángulo es un cuadrilátero que tiene 4 lados rectos (iguales dos a dos) y 4 vértices.",
        "respuesta": "La pantalla rectangular tiene **4 lados y 4 vértices**."
    },
    {
        "id": 55,
        "title": "Perímetro del recinto cuadrado de Charmander",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "Charmander entrena en una zona cerrada con vallas que tiene forma de cuadrado. Cada uno de los 4 lados de la zona mide 5 metros de longitud.\n\n¿Cuál es el perímetro total del recinto de entrenamiento?",
        "datos": "Forma: cuadrado; Longitud de cada lado: 5 metros.",
        "operaciones": "El perímetro es la suma de las longitudes de todos los lados de la figura:\n  Perímetro = 5 + 5 + 5 + 5 = 20 metros (o 4 x 5 = 20 m).",
        "respuesta": "El perímetro total del recinto es de **20 metros**."
    },
    {
        "id": 56,
        "title": "Perímetro de la piscina de natación de Squirtle",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En el gimnasio acuático de Ciudad Celeste hay una piscina rectangular donde nada Squirtle. Los dos lados largos miden 8 metros cada uno y los dos lados cortos miden 4 metros cada uno.\n\n¿Cuál es el perímetro total de la piscina?",
        "datos": "Forma: rectángulo; Lados largos: 8 m cada uno; Lados cortos: 4 m cada uno.",
        "operaciones": "Sumamos la longitud de los 4 lados del rectángulo:\n  Perímetro = 8 + 4 + 8 + 4 = 24 metros\n- 8 + 4 = 12\n- 12 + 12 = 24.",
        "respuesta": "El perímetro total de la piscina es de **24 metros**."
    },
    {
        "id": 57,
        "title": "Perímetro del jardín triangular de Oddish",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "Erika ha delimitado un pequeño cantero triangular en el jardín botánico para que Oddish tome el sol. Los tres lados del triángulo miden 6 metros, 7 metros y 5 metros respectivamente.\n\n¿Cuál es el perímetro del jardín triangular?",
        "datos": "Longitudes de los lados del triángulo: 6 m, 7 m y 5 m.",
        "operaciones": "Sumamos los tres lados del triángulo:\n  Perímetro = 6 + 7 + 5\n- 6 + 7 = 13\n- 13 + 5 = 18 metros.",
        "respuesta": "El perímetro del jardín triangular es de **18 metros**."
    },
    {
        "id": 58,
        "title": "Conteo de vértices en las medallas de gimnasio",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "Ash observa en su estuche la Medalla Cascada (que tiene forma de triángulo) y la Medalla Trueno (que tiene forma de octógono regular u 8 vértices, pero en esta réplica de entrenamiento tiene forma de cuadrado con 4 esquinas).\n\nSi la medalla triangular tiene 3 vértices y la medalla cuadrada tiene 4 vértices, ¿cuántos vértices reúnen entre las dos medallas juntas?",
        "datos": "Medalla triangular: 3 vértices; Medalla cuadrada: 4 vértices.",
        "operaciones": "Sumamos los vértices de ambas figuras:\n  3 + 4 = 7 vértices.",
        "respuesta": "Entre las dos medallas reúnen en total **7 vértices**."
    },
    {
        "id": 59,
        "title": "Navegando por la cuadrícula de la Cueva Celeste",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En el mapa cuadriculado de la Cueva Celeste, Ash se sitúa en la casilla de entrada. Para llegar hasta un objeto brillante en el suelo, camina 3 casillas hacia el Norte (hacia arriba) y a continuación camina 2 casillas hacia el Este (hacia la derecha).\n\n¿Cuántas casillas ha recorrido Ash en total por la cuadrícula?",
        "datos": "Desplazamiento al Norte: 3 casillas; Desplazamiento al Este: 2 casillas.",
        "operaciones": "Sumamos el total de desplazamientos realizados sobre la cuadrícula:\n  3 + 2 = 5 casillas.",
        "respuesta": "Ash ha recorrido en total **5 casillas** sobre la cuadrícula."
    },
    {
        "id": 60,
        "title": "La posición de Pikachu en el tablero de entrenamiento",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En una cuadrícula de entrenamiento de 4 filas (A, B, C, D) y 4 columnas (1, 2, 3, 4), Pikachu está situado en la casilla de la Fila B, Columna 3. Si Pikachu da un salto de 1 casilla hacia la derecha, ¿en qué fila y columna se encontrará ahora?",
        "datos": "Posición inicial: Fila B, Columna 3; Movimiento: 1 casilla hacia la derecha.",
        "operaciones": "Moverse a la derecha cambia la columna hacia la siguiente casilla numérica, manteniendo la misma fila:\n- La fila sigue siendo la B.\n- La columna pasa de 3 a: 3 + 1 = 4.\nNueva posición: Fila B, Columna 4.",
        "respuesta": "Pikachu se encontrará en la **Fila B, Columna 4** (casilla **B4**)."
    },
    {
        "id": 61,
        "title": "¿Dentro o fuera de la zona de hierba?",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En un prado cercado hay una gran mancha de hierba alta. Dentro de la hierba alta se esconden 8 Pokémon salvajes, mientras que fuera de la hierba, descansando sobre el camino de arena, hay 5 Pokémon más.\n\n¿Cuántos Pokémon hay en total en el prado y cuántos se encuentran dentro de la hierba alta?",
        "datos": "Pokémon dentro de la hierba: 8; Pokémon fuera de la hierba: 5.",
        "operaciones": "1. Calculamos el total de Pokémon sumando los que están dentro y los que están fuera:\n   8 + 5 = 13 Pokémon.\n2. Identificamos los que están dentro: 8 Pokémon.",
        "respuesta": "En el prado hay en total 13 Pokémon y exactamente **8 Pokémon están dentro** de la hierba alta."
    },
    {
        "id": 62,
        "title": "El marco de madera para la foto del equipo",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "Brock quiere fabricar un marco de madera rectangular para colgar la foto de recuerdo de su viaje por Kanto. La foto mide 10 centímetros de largo y 6 centímetros de ancho.\n\n¿Cuántos centímetros de listón de madera necesitará en total para bordear todo el perímetro del marco?",
        "datos": "Largo de la foto: 10 cm; Ancho de la foto: 6 cm (rectángulo: dos lados de 10 cm y dos de 6 cm).",
        "operaciones": "Calculamos el perímetro del rectángulo sumando sus 4 lados:\n  Perímetro = 10 + 6 + 10 + 6 = 32 centímetros\n- 10 + 6 = 16\n- 16 + 16 = 32.",
        "respuesta": "Brock necesitará en total **32 centímetros** de listón de madera."
    },
    {
        "id": 63,
        "title": "Cuerpos geométricos en los paquetes de la Tienda",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "El repartidor de la Tienda Pokémon entrega dos paquetes en el laboratorio: el primero contiene una Poké Ball perfectamente redonda en el espacio, y el segundo contiene una caja de herramientas cúbica cuyas 6 caras son cuadrados exactamente iguales.\n\n¿Qué nombre recibe el cuerpo geométrico de la Poké Ball y cuál el de la caja de herramientas?",
        "datos": "Objeto 1: cuerpo redondo espacial; Objeto 2: caja con 6 caras cuadradas idénticas.",
        "operaciones": "Identificamos los cuerpos geométricos tridimensionales:\n- Una figura espacial delimitada por una superficie curva continua sin caras planas es una esfera.\n- Un cuerpo geométrico cerrado formado por 6 caras cuadradas iguales es un cubo.",
        "respuesta": "La Poké Ball representa una **esfera** y la caja representa un **cubo**."
    },
    {
        "id": 64,
        "title": "Conteo total de lados en el mural de triángulos",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "En la entrada del Centro Pokémon hay un bonito mural decorativo formado por 3 figuras triangulares independientes dibujadas una junto a otra.\n\nSi contamos los lados de los 3 triángulos por separado, ¿cuántos lados rectos hay en total?",
        "datos": "Cantidad de triángulos: 3; lados de cada triángulo: 3.",
        "operaciones": "Calculamos mediante suma reiterada o multiplicación:\n  3 + 3 + 3 = 9 lados (o 3 x 3 = 9 lados).",
        "respuesta": "En total hay **9 lados rectos** entre los 3 triángulos."
    },
    {
        "id": 65,
        "title": "El laberinto del jardín de Ciudad Azulona",
        "subcategory": "Subcategoría 4: Geometría, Formas, Perímetros, Áreas y Espacio",
        "text": "Para llegar hasta la arena de combate en el gimnasio de tipo Planta, los retadores deben recorrer un sendero entre setos. Ash avanza 4 metros en línea recta hacia adelante, gira hacia su derecha y avanza 3 metros más en línea recta hasta pisar la meta.\n\n¿Cuántos metros caminó Ash en total dentro del laberinto?",
        "datos": "Primer tramo: 4 metros; Segundo tramo: 3 metros.",
        "operaciones": "Sumamos los metros de ambos tramos del recorrido:\n  4 + 3 = 7 metros.",
        "respuesta": "Ash caminó en total **7 metros** dentro del laberinto."
    },

    # Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional (Problemas 66 al 75)
    {
        "id": 66,
        "title": "El sendero de huellas de Pikachu",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Pikachu corretea por la arena de la playa dejando un rastro de huellas numeradas que siguen una serie creciente de 2 en 2: 2, 4, 6, 8, ?, 12.\n\n¿Qué número corresponde a la huella marcada con el signo de interrogación?",
        "datos": "Serie numérica creciente: 2, 4, 6, 8, ?, 12.",
        "operaciones": "Identificamos el patrón de la regularidad:\n- 2 + 2 = 4\n- 4 + 2 = 6\n- 6 + 2 = 8\nEl patrón consiste en sumar 2 a cada término.\nCalculamos el término que falta: 8 + 2 = 10.\nComprobamos con el siguiente: 10 + 2 = 12.",
        "respuesta": "El número que corresponde a la huella es el **10**."
    },
    {
        "id": 67,
        "title": "La cosecha de bayas de 5 en 5 de Brock",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Brock recoge bayas y las va contando en grupos de 5 en 5 para guardarlas en bolsas: 5, 10, 15, 20, ?, 30 bayas.\n\n¿Qué número de bayas debe ir en el lugar de la interrogación?",
        "datos": "Serie creciente: 5, 10, 15, 20, ?, 30.",
        "operaciones": "Analizamos la regularidad de la serie:\n- Cada número se obtiene sumando 5 al anterior (+5).\n- 20 + 5 = 25.\nComprobamos: 25 + 5 = 30.",
        "respuesta": "El número de bayas que debe ir en ese lugar es **25 bayas**."
    },
    {
        "id": 68,
        "title": "El podómetro digital de la Guardería Pokémon",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "En la Guardería Pokémon, el podómetro registra los pasos que da Togepi para fortalecerse, emitiendo un sonido cada 10 pasos: 10, 20, 30, 40, ?, 60 pasos.\n\n¿Qué cifra mostrará la pantalla en la posición de la interrogación?",
        "datos": "Serie de decenas: 10, 20, 30, 40, ?, 60.",
        "operaciones": "Observamos que la serie aumenta de 10 en 10 (+10):\n- 40 + 10 = 50.\nComprobamos: 50 + 10 = 60.",
        "respuesta": "La pantalla mostrará la cifra de **50 pasos**."
    },
    {
        "id": 69,
        "title": "El descenso por la ladera rocosa de Onix",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Onix baja por una ladera rocosa y su altímetro digital va midiendo la altura en metros en una serie decreciente que baja de 5 en 5: 50, 45, 40, ?, 30 metros.\n\n¿Qué altura marcará el altímetro en el valor que falta?",
        "datos": "Serie decreciente: 50, 45, 40, ?, 30.",
        "operaciones": "Identificamos la regla de cambio:\n- 50 - 5 = 45\n- 45 - 5 = 40\nEl patrón es restar 5 unidades en cada paso (-5).\nCalculamos el valor: 40 - 5 = 35.\nComprobamos: 35 - 5 = 30.",
        "respuesta": "El altímetro marcará una altura de **35 metros**."
    },
    {
        "id": 70,
        "title": "La cuenta atrás para el despegue del globo del Team Rocket",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Jessie y James han programado una cuenta atrás decreciente que desciende de 2 en 2 para despegar en su globo Meowth: 20, 18, 16, 14, ?.\n\n¿Cuál es el siguiente número que sonará en la cuenta atrás?",
        "datos": "Serie decreciente: 20, 18, 16, 14, ?.",
        "operaciones": "Analizamos la relación entre números consecutivos:\n- 20 - 2 = 18\n- 18 - 2 = 16\n- 16 - 2 = 14\nLa regla es restar 2 unidades (-2).\nCalculamos el siguiente término: 14 - 2 = 12.",
        "respuesta": "El siguiente número en la cuenta atrás es el **12**."
    },
    {
        "id": 71,
        "title": "El patrón de colores de Poké Balls en la fábrica",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "En la línea de pintura de Silph S.A., las Poké Balls avanzan por la cinta transportadora siguiendo un patrón de colores ordenado y repetitivo: Roja, Azul, Amarilla, Roja, Azul, Amarilla, Roja, Azul, ...\n\n¿Qué color de Poké Ball corresponde a la siguiente posición en la cinta?",
        "datos": "Patrón repetitivo: Roja, Azul, Amarilla.",
        "operaciones": "El núcleo o ciclo del patrón está formado por 3 elementos: [Roja, Azul, Amarilla].\nObservamos la secuencia actual: Roja, Azul... tras el color Azul siempre sigue el color que cierra el ciclo: Amarilla.",
        "respuesta": "El color de la siguiente Poké Ball es **Amarilla**."
    },
    {
        "id": 72,
        "title": "El algoritmo de captura paso a paso de un Pidgey",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "El Profesor Oak explica a los entrenadores el algoritmo básico (secuencia ordenada de instrucciones) para capturar un Pokémon con éxito:\n- Instrucción A: Lanzar una Poké Ball con precisión.\n- Instrucción B: Buscar y encontrar al Pokémon salvaje en la hierba alta.\n- Instrucción C: Debilitar al Pokémon salvaje con un combate cuidadoso.\n\n¿En qué orden lógico (1º, 2º y 3º) deben ejecutarse estas instrucciones?",
        "datos": "Instrucciones: A (Lanzar Poké Ball), B (Buscar Pokémon), C (Debilitar al Pokémon).",
        "operaciones": "Razonamos la secuencia cronológica lógica necesaria para resolver el problema:\n1º Paso: Primero es necesario encontrar al Pokémon salvaje (Instrucción B).\n2º Paso: Después se debe combatir para reducir sus fuerzas (Instrucción C).\n3º Paso: Finalmente se lanza la Poké Ball para capturarlo (Instrucción A).",
        "respuesta": "El orden lógico del algoritmo es **B, C, A** (1º Buscar, 2º Debilitar, 3º Lanzar la Poké Ball)."
    },
    {
        "id": 73,
        "title": "La secuencia de potencia eléctrica en Ciudad Carmín",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "En la central eléctrica, los generadores de Voltorb aumentan su carga de 100 en 100 voltios: 100, 200, 300, ?, 500 voltios.\n\n¿Qué valor de carga eléctrica falta en la secuencia?",
        "datos": "Serie de centenas: 100, 200, 300, ?, 500.",
        "operaciones": "Identificamos que la serie aumenta sumando 1 centena (100 unidades) cada vez:\n- 100 + 100 = 200\n- 200 + 100 = 300\nCalculamos: 300 + 100 = 400 voltios.\nComprobamos: 400 + 100 = 500 voltios.",
        "respuesta": "El valor de carga que falta es **400 voltios**."
    },
    {
        "id": 74,
        "title": "Instrucciones condicionales para Bulbasaur en combate",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Ash le enseña a Bulbasaur una regla condicional muy clara: 'SI el rival realiza un ataque de agua, ENTONCES debes responder usando Látigo Cepa'. Durante el enfrentamiento, el rival utiliza ataques de agua 3 veces y ataques de contacto físico 2 veces.\n\n¿Cuántas veces ejecutó Bulbasaur el movimiento Látigo Cepa siguiendo la instrucción condicional?",
        "datos": "Condición: SI ataque de agua -> ENTONCES Látigo Cepa; Ataques de agua rivales: 3 veces.",
        "operaciones": "Aplicamos la regla condicional cada vez que se cumple la condición:\n- Cada uno de los 3 ataques de agua activa 1 respuesta de Látigo Cepa.\n- Los 2 ataques físicos no activan esta regla.\nTotal de ejecuciones: 3 veces.",
        "respuesta": "Bulbasaur ejecutó Látigo Cepa exactamente **3 veces**."
    },
    {
        "id": 75,
        "title": "La pirámide de piedras de entrenamiento de Geodude",
        "subcategory": "Subcategoría 5: Patrones, Regularidades y Pensamiento Computacional",
        "text": "Geodude entrena su puntería construyendo una pirámide de piedras de 3 niveles: coloca 1 piedra en la punta superior, 2 piedras en el nivel intermedio y 3 piedras en la base inferior.\n\n¿Cuántas piedras utilizó Geodude en total para construir toda la pirámide?",
        "datos": "Piedras en el nivel 1: 1; nivel 2: 2; nivel 3: 3.",
        "operaciones": "Sumamos las cantidades de piedras de cada nivel:\n  1 + 2 + 3 = 6 piedras\n- 1 + 2 = 3\n- 3 + 3 = 6.",
        "respuesta": "Geodude utilizó en total **6 piedras** para la pirámide."
    },

    # Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad (Problemas 76 al 85)
    {
        "id": 76,
        "title": "La tabla de recuento de insectos en el Bosque Verde",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "Ash registra en una tabla con marcas de recuento los Pokémon que avista en los senderos del Bosque Verde: anota 4 Caterpie (||||), 5 Weedle (|||||) y 3 Metapod (|||).\n\n¿Cuántos Pokémon insecto registró Ash en total en su cuaderno?",
        "datos": "Caterpie: 4; Weedle: 5; Metapod: 3.",
        "operaciones": "Sumamos los valores numéricos de las tres categorías registradas:\n  4 + 5 + 3\n- 4 + 5 = 9\n- 9 + 3 = 12 Pokémon.",
        "respuesta": "Ash registró en total **12 Pokémon insecto**."
    },
    {
        "id": 77,
        "title": "El pictograma de Poké Balls de Misty",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "En el tablón de anuncios del gimnasio hay un pictograma que muestra los suministros disponibles. Cada dibujo de una estrella dorada representa exactamente 2 Poké Balls. Al lado del casillero de Misty hay dibujadas 4 estrellas doradas.\n\n¿Cuántas Poké Balls tiene Misty en realidad?",
        "datos": "Clave del pictograma: 1 estrella = 2 Poké Balls; Estrellas de Misty: 4.",
        "operaciones": "Multiplicamos el número de símbolos por el valor de cada uno (o suma repetida):\n  4 x 2 = 8 Poké Balls (o 2 + 2 + 2 + 2 = 8).",
        "respuesta": "Misty tiene en realidad **8 Poké Balls**."
    },
    {
        "id": 78,
        "title": "El gráfico de barras del equipo de Ash",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "Ash elabora un gráfico de barras para clasificar a los miembros de su equipo por tipos elementales: la barra de Tipo Fuego alcanza una altura de 2 Pokémon, la de Tipo Agua 1 Pokémon, la de Tipo Planta 1 Pokémon y la de Tipo Eléctrico 1 Pokémon.\n\n¿Cuál es el tipo más frecuente en el equipo y cuántos Pokémon tiene en total?",
        "datos": "Fuego: 2; Agua: 1; Planta: 1; Eléctrico: 1.",
        "operaciones": "1. Observamos la barra más alta: la barra de Tipo Fuego alcanza el valor 2, que es la mayor frecuencia.\n2. Sumamos todas las alturas para obtener el total del equipo:\n   2 + 1 + 1 + 1 = 5 Pokémon.",
        "respuesta": "El tipo más frecuente es el **Tipo Fuego** y el equipo tiene en total **5 Pokémon**."
    },
    {
        "id": 79,
        "title": "La bolsa sorpresa de bayas en la Tienda Pokémon",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "El dependiente de la Tienda Pokémon entrega a Ash una bolsa de tela opaca que contiene únicamente 10 Bayas Meloc rojas. Ash mete la mano sin mirar para extraer una baya al azar.\n\nClasifica el suceso 'sacar una Baya Meloc' como seguro, posible o imposible.",
        "datos": "Contenido de la bolsa: 10 Bayas Meloc (no hay ningún otro tipo de baya).",
        "operaciones": "Un suceso es 'seguro' cuando ocurre siempre sin ninguna duda, es 'posible' cuando puede ocurrir o no, y es 'imposible' cuando jamás puede ocurrir.\nComo todas las bayas de la bolsa son Bayas Meloc, es completamente seguro que la baya extraída será una Baya Meloc.",
        "respuesta": "El suceso de sacar una Baya Meloc es un suceso **seguro**."
    },
    {
        "id": 80,
        "title": "El avistamiento imposible bajo el agua marina",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "Misty y Ash están buceando con escafandra en el fondo del mar de Ciudad Celeste observando cardúmenes de Goldeen. Ash se pregunta si nadando entre las algas del fondo marino podrían toparse con un Charizard salvaje viviendo bajo el agua.\n\nClasifica el suceso 'encontrar un Charizard salvaje viviendo bajo el agua marina' como seguro, posible o imposible.",
        "datos": "Charizard es un Pokémon de tipo Fuego y Volador cuya llama en la cola se apaga con el agua; no puede vivir sumergido en el fondo del mar.",
        "operaciones": "Un acontecimiento que no puede ocurrir bajo ninguna circunstancia según las normas de la naturaleza se clasifica como suceso imposible.",
        "respuesta": "El suceso es **imposible**."
    },
    {
        "id": 81,
        "title": "La ruleta de premios del Centro Pokémon",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "La Enfermera Joy invita a los entrenadores a girar una ruleta de la suerte dividida en 4 sectores de igual tamaño: 3 sectores son de color azul (premio: Poción) y 1 sector es de color dorado (premio: Superpoción).\n\nAl hacer girar la ruleta, ¿qué premio es más posible de obtener, una Poción o una Superpoción?",
        "datos": "Sectores de Poción: 3; Sectores de Superpoción: 1; Total de sectores: 4.",
        "operaciones": "Comparamos la cantidad de sectores de cada premio:\n- Poción: 3 sectores.\n- Superpoción: 1 sector.\nComo 3 es mayor que 1 (3 > 1), hay más opciones favorables de caer en la casilla de Poción.",
        "respuesta": "Es más posible obtener una **Poción**."
    },
    {
        "id": 82,
        "title": "Conteo de Pokémon de agua en la tarde de pesca",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "Misty pasa una tarde tranquila pescando en el muelle de Ciudad Carmín y anota en su lista de capturas los Pokémon avistados: 6 Magikarp traviesos, 4 Poliwag y 5 simpáticos Goldeen.\n\n¿Cuántos Pokémon de agua anotó Misty en total durante la tarde de pesca?",
        "datos": "Magikarp: 6; Poliwag: 4; Goldeen: 5.",
        "operaciones": "Sumamos las tres cantidades aplicando cálculo mental (agrupando amigos del 10):\n  (6 + 4) + 5 = 10 + 5 = 15 Pokémon.",
        "respuesta": "Misty anotó en total **15 Pokémon de agua**."
    },
    {
        "id": 83,
        "title": "Pictograma de cosecha de bayas con clave de 5",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "En el huerto de bayas del campamento, el cartel utiliza el dibujo de una cesta para representar 5 bayas cosechadas. Junto al manzano de Pikachu aparecen dibujadas 3 cestas completas.\n\n¿Cuántas bayas representa el dibujo en total?",
        "datos": "Clave: 1 cesta = 5 bayas; Cestas dibujadas: 3.",
        "operaciones": "Multiplicamos el número de símbolos por el valor unitario de la clave:\n  3 x 5 = 15 bayas (o 5 + 5 + 5 = 15).",
        "respuesta": "El dibujo representa en total **15 bayas** cosechadas."
    },
    {
        "id": 84,
        "title": "Comparando alturas en el gráfico de barras",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "Un gráfico de barras del laboratorio muestra la altura de tres compañeros de viaje: la barra de Bulbasaur mide 70 centímetros, la de Charmander mide 60 centímetros y la de Squirtle mide 50 centímetros.\n\n¿Cuántos centímetros más alta es la barra de Bulbasaur que la barra de Squirtle?",
        "datos": "Altura de Bulbasaur: 70 cm; Altura de Squirtle: 50 cm.",
        "operaciones": "Restamos la altura de Squirtle de la de Bulbasaur:\n  70 - 50 = 20 centímetros.",
        "respuesta": "La barra de Bulbasaur es **20 centímetros** más alta que la de Squirtle."
    },
    {
        "id": 85,
        "title": "La caja misteriosa de Poké Balls de Brock",
        "subcategory": "Subcategoría 6: Tratamiento de la Información, Gráficos y Probabilidad",
        "text": "En una caja opaca de metal, Brock guarda 5 Poké Balls clásicas y 3 Super Balls azules. Brock introduce la mano en la caja con los ojos cerrados para extraer una sola bola sin mirar.\n\nClasifica el suceso 'extraer una Super Ball' como seguro, posible o imposible.",
        "datos": "Contenido de la caja: 5 Poké Balls y 3 Super Balls.",
        "operaciones": "Analizamos la probabilidad del suceso:\n- ¿Puede ocurrir? Sí, porque hay 3 Super Balls en la caja.\n- ¿Ocurrirá con total certeza? No, porque también puede salir una de las 5 Poké Balls.\nPor tanto, es un suceso que puede ocurrir, es decir, es un suceso posible.",
        "respuesta": "Extraer una Super Ball es un suceso **posible**."
    },

    # Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP) (Problemas 86 al 100)
    {
        "id": 86,
        "title": "Primera victoria y ganancia de EXP de Pikachu",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Pikachu comienza su entrenamiento matutino con 40 puntos de experiencia (EXP) en su medidor personal. Tras derrotar a un Rattata en un combate amistoso en la Ruta 1, recibe 25 puntos de EXP adicionales.\n\n¿Cuántos puntos de experiencia tiene Pikachu ahora en su medidor?",
        "datos": "EXP inicial de Pikachu: 40 puntos; EXP ganada en el combate: 25 puntos.",
        "operaciones": "Sumamos los puntos de experiencia ganados a los que ya tenía acumulados:\n  40 + 25 = 65 puntos de EXP\n- Unidades: 0 + 5 = 5\n- Decenas: 4 + 2 = 6.",
        "respuesta": "Pikachu tiene ahora en total **65 puntos de EXP**."
    },
    {
        "id": 87,
        "title": "Charmander y los puntos necesarios para el Nivel 7",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Para que Charmander suba al Nivel 7, su barra de progreso debe llegar a 100 puntos de experiencia (EXP). En este momento, Charmander ya tiene acumulados 72 puntos de EXP.\n\n¿Cuántos puntos de experiencia le faltan a Charmander para alcanzar el Nivel 7?",
        "datos": "Meta de EXP para el Nivel 7: 100 puntos; EXP acumulada: 72 puntos.",
        "operaciones": "Calculamos la diferencia restando la EXP actual de la meta fijada:\n  100 - 72\n- 100 - 70 = 30\n- 30 - 2 = 28 puntos de EXP.",
        "respuesta": "A Charmander le faltan **28 puntos de EXP** para alcanzar el Nivel 7."
    },
    {
        "id": 88,
        "title": "Combate doble y suma de EXP de Squirtle",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Squirtle participa con éxito en dos asaltos consecutivos frente a otros entrenadores. En el primer asalto gana 30 puntos de experiencia (EXP) y en el segundo asalto gana 45 puntos de EXP.\n\n¿Cuántos puntos de experiencia sumó Squirtle en total en los dos asaltos?",
        "datos": "EXP del primer asalto: 30 puntos; EXP del segundo asalto: 45 puntos.",
        "operaciones": "Sumamos los puntos de ambos combates:\n  30 + 45 = 75 puntos de EXP\n- Unidades: 0 + 5 = 5\n- Decenas: 3 + 4 = 7.",
        "respuesta": "Squirtle sumó en total **75 puntos de EXP**."
    },
    {
        "id": 89,
        "title": "Experiencia compartida tras vencer a un Geodude",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Ash y Brock unen sus fuerzas para superar a un Geodude salvaje que bloqueaba el sendero. Al ser derrotado, el Geodude otorga 40 puntos de experiencia (EXP) en total, que se reparten a partes iguales (la mitad para cada uno) entre Pikachu y Onix.\n\n¿Cuántos puntos de experiencia recibe cada uno de los dos Pokémon?",
        "datos": "Total de EXP obtenida: 40 puntos; Reparto a partes iguales (mitad).",
        "operaciones": "Calculamos la mitad de 40 puntos repartiendo en 2 partes iguales:\n  40 : 2 = 20 (o 20 + 20 = 40).",
        "respuesta": "Cada uno de los dos Pokémon recibe **20 puntos de EXP**."
    },
    {
        "id": 90,
        "title": "Daño en combate y Puntos de Salud restantes de Bulbasaur",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Bulbasaur salta a la arena de combate con sus 45 Puntos de Salud (PS) totalmente llenos. Durante el enfrentamiento, un rival le asesta un ataque de Placaje que le inflige 15 puntos de daño.\n\n¿Cuántos Puntos de Salud (PS) le quedan a Bulbasaur tras recibir el impacto?",
        "datos": "PS iniciales de Bulbasaur: 45; Daño recibido: 15 PS.",
        "operaciones": "Restamos el daño recibido de los puntos de salud iniciales:\n  45 - 15 = 30 PS\n- Unidades: 5 - 5 = 0\n- Decenas: 4 - 1 = 3.",
        "respuesta": "A Bulbasaur le quedan **30 Puntos de Salud (PS)**."
    },
    {
        "id": 91,
        "title": "Curación con Poción en el Centro Pokémon",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Pikachu termina un combate agotador y llega al mostrador de la Enfermera Joy con solo 18 Puntos de Salud (PS). La enfermera le aplica una Poción medicinal que le cura exactamente 20 PS de salud.\n\n¿A cuántos Puntos de Salud (PS) asciende la energía de Pikachu tras la curación?",
        "datos": "PS actuales: 18; Curación aportada por la Poción: 20 PS.",
        "operaciones": "Sumamos los puntos curados a la salud actual de Pikachu:\n  18 + 20 = 38 PS\n- Unidades: 8 + 0 = 8\n- Decenas: 1 + 2 = 3.",
        "respuesta": "La energía de Pikachu asciende a **38 Puntos de Salud (PS)**."
    },
    {
        "id": 92,
        "title": "El efecto de la Superpoción en el combate contra Brock",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "En el combate oficial del gimnasio, el Geodude de Brock queda con solo 12 Puntos de Salud (PS) tras un potente ataque especial. Brock usa rápidamente una Superpoción, la cual restaura exactamente 50 PS de golpe.\n\n¿Cuántos Puntos de Salud (PS) tiene Geodude después de recibir la Superpoción?",
        "datos": "PS antes de curar: 12 PS; Restauración de la Superpoción: 50 PS.",
        "operaciones": "Sumamos los puntos restaurados por la medicina:\n  12 + 50 = 62 PS\n- Unidades: 2 + 0 = 2\n- Decenas: 1 + 5 = 6.",
        "respuesta": "Geodude tiene ahora **62 Puntos de Salud (PS)**."
    },
    {
        "id": 93,
        "title": "El desafío de EXP para alcanzar el Nivel 10",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "La Pokédex indica que Pikachu necesita acumular un total de 200 puntos de experiencia (EXP) para subir al Nivel 10. Si Pikachu ya ha conseguido 145 puntos de EXP en sus viajes, ¿cuántos puntos de EXP le faltan para subir al Nivel 10?",
        "datos": "EXP requerida para Nivel 10: 200 puntos; EXP actual: 145 puntos.",
        "operaciones": "Efectuamos la resta para hallar los puntos que faltan:\n  200 - 145\n- 200 - 100 = 100\n- 100 - 45 = 55 puntos de EXP.",
        "respuesta": "A Pikachu le faltan **55 puntos de EXP** para alcanzar el Nivel 10."
    },
    {
        "id": 94,
        "title": "Tres victorias consecutivas contra Pidgey salvajes",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Charmander entrena en la Ruta 2 y logra vencer consecutivamente a 3 Pidgey salvajes. Cada Pidgey derrotado le otorga exactamente 15 puntos de experiencia (EXP).\n\n¿Cuántos puntos de experiencia gana Charmander en total por las tres victorias?",
        "datos": "Victorias conseguidas: 3; EXP por cada victoria: 15 puntos.",
        "operaciones": "Calculamos la suma reiterada o producto (3 veces 15):\n  15 + 15 + 15 = 45 puntos de EXP (o 3 x 15 = 45).",
        "respuesta": "Charmander gana en total **45 puntos de EXP**."
    },
    {
        "id": 95,
        "title": "El efecto de nivel del Caramelo Raro",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "El Profesor Oak premia a Ash entregándole un delicioso y codiciado Caramelo Raro. Este objeto legendario hace que un Pokémon suba exactamente 1 nivel de golpe de forma instantánea. Si Ash se lo da a su Bulbasaur de Nivel 8, ¿qué nivel alcanzará Bulbasaur?",
        "datos": "Nivel inicial de Bulbasaur: Nivel 8; Incremento del Caramelo Raro: 1 nivel.",
        "operaciones": "Sumamos 1 nivel al nivel inicial:\n  8 + 1 = 9.",
        "respuesta": "Bulbasaur alcanzará el **Nivel 9**."
    },
    {
        "id": 96,
        "title": "Combate de gimnasio intenso contra Starmie",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "En el Gimnasio de Ciudad Celeste, el Geodude de Brock salta a la plataforma de roca con 78 Puntos de Salud (PS). El rápido Starmie de Misty le lanza un ataque Pistola Agua que le inflige 24 puntos de daño.\n\n¿Cuántos Puntos de Salud (PS) le quedan a Geodude tras el ataque?",
        "datos": "PS iniciales de Geodude: 78; Daño infligido por Starmie: 24 PS.",
        "operaciones": "Restamos el daño de los puntos de salud:\n  78 - 24 = 54 PS\n- Unidades: 8 - 4 = 4\n- Decenas: 7 - 2 = 5.",
        "respuesta": "A Geodude le quedan **54 Puntos de Salud (PS)**."
    },
    {
        "id": 97,
        "title": "Baya Aranja equipada en combate",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Eevee lleva equipada en su collar una Baya Aranja antes de comenzar el duelo. Eevee comienza con 35 PS. Durante el combate recibe un golpe que le resta 10 PS, pero de inmediato consume su Baya Aranja, que le recupera 10 PS en ese mismo instante.\n\n¿Cuántos Puntos de Salud (PS) tiene Eevee al finalizar el asalto?",
        "datos": "PS iniciales: 35; Daño recibido: 10 PS; Curación de la baya: 10 PS.",
        "operaciones": "Calculamos paso a paso:\n1. Restamos el daño: 35 - 10 = 25 PS.\n2. Sumamos la curación de la baya: 25 + 10 = 35 PS.\nComo se resta y se suma la misma cantidad (10 - 10 = 0), los PS se mantienen iguales.",
        "respuesta": "Al finalizar el asalto, Eevee tiene exactamente **35 Puntos de Salud (PS)**."
    },
    {
        "id": 98,
        "title": "Experiencia adicional por captura exitosa",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "En la región de Kanto, derrotar a un Pokémon salvaje otorga 50 puntos de experiencia (EXP) base, y si además el entrenador logra atraparlo dentro de una Poké Ball, la Pokédex concede un bono extra de 25 puntos de EXP por la captura.\n\n¿Cuántos puntos de experiencia gana Ash en total al debilitar y capturar al Pokémon salvaje?",
        "datos": "EXP base por combate: 50 puntos; Bono extra por captura: 25 puntos.",
        "operaciones": "Sumamos la experiencia base y el bono especial de captura:\n  50 + 25 = 75 puntos de EXP\n- Unidades: 0 + 5 = 5\n- Decenas: 5 + 2 = 7.",
        "respuesta": "Ash gana en total **75 puntos de EXP**."
    },
    {
        "id": 99,
        "title": "Comparando la experiencia de los iniciales",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Tras varios días de entrenamiento en el bosque, Charmander acumula 120 puntos de experiencia (EXP) y Squirtle acumula 95 puntos de EXP en sus fichas de entrenador.\n\n¿Cuántos puntos de experiencia más tiene Charmander que Squirtle?",
        "datos": "EXP acumulada por Charmander: 120 puntos; EXP acumulada por Squirtle: 95 puntos.",
        "operaciones": "Restamos la cantidad menor de la mayor:\n  120 - 95\n- 120 - 90 = 30\n- 30 - 5 = 25 puntos de EXP.",
        "respuesta": "Charmander tiene **25 puntos de EXP** más que Squirtle."
    },
    {
        "id": 100,
        "title": "El gran salto al Nivel 12 antes del desafío final",
        "subcategory": "Subcategoría 7: Mecánicas de Combate, Nivel y Experiencia (EXP)",
        "text": "Pikachu tiene acumulados 280 puntos de experiencia (EXP) y su meta para alcanzar el Nivel 12 son 350 puntos de EXP. En un emocionante combate final contra el Team Rocket, Pikachu consigue una gran victoria y gana 50 puntos de EXP adicionales.\n\n¿Cuántos puntos de experiencia tiene Pikachu tras el combate y cuántos puntos le faltan todavía para alcanzar el Nivel 12?",
        "datos": "EXP inicial: 280 puntos; EXP ganada en el combate: 50 puntos; Meta para el Nivel 12: 350 puntos.",
        "operaciones": "Resolvemos en dos pasos sencillos:\n1. Calculamos la nueva experiencia total sumando los puntos ganados:\n   280 + 50 = 330 puntos de EXP.\n2. Calculamos los puntos restantes restando la experiencia actual de la meta fijada:\n   350 - 330 = 20 puntos de EXP.",
        "respuesta": "Pikachu tiene ahora 330 puntos de EXP y le faltan todavía **20 puntos de EXP** para alcanzar el Nivel 12."
    }
]

def generate_markdown():
    lines = []
    lines.append("# Banco de Problemas Matemáticos Pokémon — 2º de Primaria (LOMLOE)")
    lines.append("")
    lines.append("## Introducción Curricular y Pedagógica")
    lines.append("El presente documento constituye el banco oficial y completo de 100 problemas matemáticos contextualizados en el universo Pokémon para **2º de Educación Primaria**, diseñado en rigurosa consonancia con la normativa educativa española (**LOMLOE - Real Decreto 157/2022**).")
    lines.append("")
    lines.append("Los problemas están adaptados didáctica y lingüísticamente a alumnos de 7 y 8 años de edad (final del Primer Ciclo de Primaria), estructurados en 7 subcategorías curriculares:")
    lines.append("1. **Subcategoría 1 (Problemas 1 al 15)**: Numeración, Descomposición y Valor Posicional (números hasta el 999, C-D-U, anterior/posterior, pares/impares, ordinales).")
    lines.append("2. **Subcategoría 2 (Problemas 16 al 35)**: Operaciones Aritméticas y Cálculo Mental (sumas y restas con/sin llevada hasta 999, iniciación a la multiplicación como suma repetida, dobles y mitades).")
    lines.append("3. **Subcategoría 3 (Problemas 36 al 50)**: Magnitudes, Unidades de Medida, Tiempo y Dinero (cm y m, kg, litros, reloj en punto y media, monedas y billetes de euro).")
    lines.append("4. **Subcategoría 4 (Problemas 51 al 65)**: Geometría, Formas, Perímetros, Áreas y Espacio (figuras 2D, lados y vértices, cuadrículas, recorridos y perímetros simples).")
    lines.append("5. **Subcategoría 5 (Problemas 66 al 75)**: Patrones, Regularidades y Pensamiento Computacional (series numéricas, algoritmos paso a paso, pensamiento lógico).")
    lines.append("6. **Subcategoría 6 (Problemas 76 al 85)**: Tratamiento de la Información, Gráficos y Probabilidad (tablas de recuento, pictogramas, gráficos de barras, nociones de azar: seguro, posible, imposible).")
    lines.append("7. **Subcategoría 7 (Problemas 86 al 100)**: Mecánicas de Combate, Nivel y Experiencia (EXP) (ganancia lineal de EXP, progreso de nivel, Puntos de Salud PS, daño y curación con Pociones).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Parte 1: Enunciados de los Problemas (1 al 100)")
    lines.append("")

    current_subcat = None
    for p in problems_data:
        if p["subcategory"] != current_subcat:
            current_subcat = p["subcategory"]
            lines.append(f"### {current_subcat}")
            lines.append("")
        lines.append(f"### Problema {p['id']}: {p['title']}")
        lines.append("")
        lines.append(p["text"])
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Parte 2: Solucionario y Respuestas Razonadas (1 al 100)")
    lines.append("")

    current_subcat = None
    for p in problems_data:
        if p["subcategory"] != current_subcat:
            current_subcat = p["subcategory"]
            lines.append(f"### Soluciones — {current_subcat}")
            lines.append("")
        lines.append(f"### Solución Problema {p['id']}: {p['title']}")
        lines.append("")
        lines.append(f"- **Datos identificados**: {p['datos']}")
        lines.append(f"- **Planteamiento y Operaciones**: {p['operaciones']}")
        lines.append(f"- **Respuesta Final**: {p['respuesta']}")
        lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    output_path = r"C:\Users\gabri\teamwork_projects\pokemon_math\problemas_2_primaria.md"
    content = generate_markdown()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {output_path} successfully. Total characters: {len(content)}")
