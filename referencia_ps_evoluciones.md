# Mecánica de Puntos de Salud (PS / HP) y Progresión Evolutiva Pokémon: Guía de Referencia Matemática (LOMLOE)

**Proyecto:** Matemáticas Primaria con Pokémon (LOMLOE 2º a 6º de Educación Primaria)  
**Documento:** Referencia Técnica y Curricular de Puntos de Salud y Evolución (Requisito R2)  
**Marco Legal:** Real Decreto 157/2022 (LOMLOE) — Sentido Numérico, Medida, Álgebra y Funciones  
**Versión de Mecánicas:** Generaciones III a IX (Saga Principal)  

---

## 1. Introducción Conceptual a los Puntos de Salud (PS / HP)

Los **Puntos de Salud** (en inglés *Hit Points*, abreviados como **HP**, y en la traducción oficial en español **Puntos de Salud** o **Puntos de Vida**, abreviados como **PS**) representan la vitalidad física de un Pokémon durante el combate.

### 1.1 Dinámica de la Barra de Vida y Estados de Combate
En la interfaz del juego, los PS se visualizan como una barra de salud numérica y cromática:
- **Barra Verde:** Cuando el Pokémon conserva más del $50\%$ de sus PS máximos ($\text{PS}_{\text{actual}} > 0,5 \cdot \text{PS}_{\max}$).
- **Barra Amarilla:** Cuando el Pokémon se encuentra entre el $20\%$ y el $50\%$ de sus PS máximos ($0,2 \cdot \text{PS}_{\max} \le \text{PS}_{\text{actual}} \le 0,5 \cdot \text{PS}_{\max}$).
- **Barra Roja:** Cuando el Pokémon entra en estado crítico con menos del $20\%$ de sus PS máximos ($\text{PS}_{\text{actual}} < 0,2 \cdot \text{PS}_{\max}$).
- **Debilitamiento ($0$ PS):** Cuando los PS actuales caen a cero ($\text{PS} = 0$), el Pokémon queda fuera de combate (*fainted* / debilitado) y no puede seguir luchando hasta ser curado mediante objetos (Revivir, Poción) o en un Centro Pokémon.

Matemáticamente, los PS operan como una **variable de estado acumulativa y acotada**:
$$0 \le \text{PS}_{\text{actual}} \le \text{PS}_{\max}$$

Cada impacto recibido resta vida ($\text{PS}_{\text{nuevo}} = \text{PS}_{\text{actual}} - \text{Daño}$), mientras que los objetos curativos suman vida sin exceder nunca el límite máximo ($\text{PS}_{\text{nuevo}} = \min(\text{PS}_{\max}, \; \text{PS}_{\text{actual}} + \text{Curación})$).

---

## 2. La Fórmula Canónica de la Saga Principal (Generaciones III a IX)

Desde el lanzamiento de *Pokémon Rubí y Zafiro* (Generación III) hasta las entregas actuales de *Pokémon Escarlata y Púrpura* (Generación IX), el cálculo de los Puntos de Salud máximos de cualquier Pokémon viene determinado de forma universal por la siguiente fórmula aritmética:

$$\text{PS}_{\max} = \left\lfloor \frac{\left(2 \cdot \text{BaseHP} + \text{IV} + \left\lfloor \frac{\text{EV}}{4} \right\rfloor \right) \cdot \text{Nivel}}{100} \right\rfloor + \text{Nivel} + 10$$

### 2.1 Desglose Término a Término de las Variables

| Variable | Nombre Completo | Rango Canónico | Significado Matemático y de Juego |
|:---|:---|:---:|:---|
| **$\text{BaseHP}$** | *Base Hit Points* (PS Base) | $[1, \; 255]$ | Estadística intrínseca de la especie (ej. Charmander = 39, Snorlax = 160, Blissey = 255). Es constante para todos los miembros de la misma especie. |
| **$\text{IV}$** | *Individual Value* (Genética) | $[0, \; 31]$ | Valor individual inherente al Pokémon al nacer o ser capturado. Equivale a su "potencial genético". En nivel 100, cada punto de IV otorga exactamente 1 punto adicional de PS. |
| **$\text{EV}$** | *Effort Values* (Puntos de Esfuerzo) | $[0, \; 252]$ | Puntos obtenidos al derrotar adversarios mediante entrenamiento. Cada 4 puntos de EV equivalen a 1 punto adicional de estadística a nivel 100 ($\lfloor \text{EV}/4 \rfloor \in [0, \; 63]$). |
| **$\text{Nivel}$** ($L$) | Nivel de experiencia | $[1, \; 100]$ | Factor de escala lineal principal. Determina qué fracción porcentual del potencial base se manifiesta en la estadística. |
| **$\lfloor \dots \rfloor$** | Función Suelo (*Floor*) | $\mathbb{R} \to \mathbb{Z}$ | Redondeo por defecto hacia el número entero inferior más cercano. En la informática de las consolas de Nintendo, esto equivale a truncar la parte decimal de la división entera. |
| **Constante $+ \text{Nivel}$** | Progresión por nivel | $[1, \; 100]$ | Garantiza que subir de nivel siempre incremente los PS, independientemente de la base. |
| **Constante $+ 10$** | Vitalidad mínima garantizada | $+10$ | Asegura que incluso a nivel 1 con base muy baja, ningún Pokémon empiece con 0 PS. |

---

## 3. La Singular Excepción Canónica: Shedinja

Existe exactamente **una única excepción canónica** en toda la franquicia Pokémon a la fórmula universal de PS: **Shedinja** (Pokémon de tipo Bicho/Fantasma, número de Pokédex #292).

$$\text{PS}_{\text{Shedinja}} = 1 \quad \forall \; \text{Nivel} \in [1, \; 100]$$

- **Justificación de diseño y lore:** Shedinja nace de la muda o caparazón vacío que deja Nincada al evolucionar a Ninjask. Al carecer de cuerpo biológico real, posee exactamente **1 PS constante**.
- **Independencia de variables:** Aunque Shedinja tenga $\text{BaseHP} = 1$, $\text{IV} = 31$, $\text{EV} = 252$ y se encuentre a Nivel 100, el motor del juego sobreescribe cualquier cálculo matemático fijando siempre sus PS en $1$.
- **Mecánica de supervivencia:** Para compensar esta fragilidad extrema, Shedinja cuenta con la habilidad exclusiva **Superguarda** (*Wonder Guard*), la cual le otorga inmunidad absoluta frente a cualquier movimiento directo que no sea súper eficaz ($x2$).

---

## 4. Casos Límite y Valores Frontera

El análisis de extremos a Nivel 100 ($L = 100$) permite simplificar la fórmula de manera elegante, ya que la fracción $\frac{\dots \cdot 100}{100}$ cancela el denominador:

$$\text{PS}(100) = 2 \cdot \text{BaseHP} + \text{IV} + \left\lfloor \frac{\text{EV}}{4} \right\rfloor + 100 + 10$$

### 4.1 Valores Extremos a Nivel 100

1. **Mínimo Absoluto a Nivel 100 ($\text{IV} = 0, \; \text{EV} = 0$):**
   $$\text{PS}_{\min}(100) = 2 \cdot \text{BaseHP} + 0 + 0 + 110 = \mathbf{2 \cdot \text{BaseHP} + 110}$$
2. **Máximo Absoluto a Nivel 100 ($\text{IV} = 31, \; \text{EV} = 252 \implies \lfloor 252/4 \rfloor = 63$):**
   $$\text{PS}_{\max}(100) = 2 \cdot \text{BaseHP} + 31 + 63 + 110 = \mathbf{2 \cdot \text{BaseHP} + 204}$$
3. **Pokémon Salvaje Estándar a Nivel 100 ($\text{IV} = 15, \; \text{EV} = 0$):**
   $$\text{PS}_{\text{salvaje}}(100) = 2 \cdot \text{BaseHP} + 15 + 0 + 110 = \mathbf{2 \cdot \text{BaseHP} + 125}$$
4. **Rango de Variación Total por Genética y Esfuerzo:**
   $$\Delta \text{PS}_{\text{rango}} = \text{PS}_{\max}(100) - \text{PS}_{\min}(100) = 204 - 110 = \mathbf{94 \text{ PS}}$$
   *Insight didáctico:* Dos Pokémon de la misma especie a nivel 100 pueden diferenciarse en hasta 94 puntos de salud únicamente por sus IVs y su entrenamiento.

### 4.2 Valores a Nivel 50 ($L = 50$, Estándar de Torneos Competitivos)
A nivel 50, la fórmula reduce el producto a la mitad ($\frac{\dots \cdot 50}{100} = \frac{\dots}{2}$):
- **Mínimo ($\text{IV} = 0, \; \text{EV} = 0$):**
  $$\text{PS}_{\min}(50) = \left\lfloor \frac{2 \cdot \text{BaseHP}}{2} \right\rfloor + 50 + 10 = \mathbf{\text{BaseHP} + 60}$$
- **Máximo ($\text{IV} = 31, \; \text{EV} = 252$):**
  $$\text{PS}_{\max}(50) = \left\lfloor \frac{2 \cdot \text{BaseHP} + 31 + 63}{2} \right\rfloor + 60 = \left\lfloor \text{BaseHP} + 47 \right\rfloor + 60 = \mathbf{\text{BaseHP} + 107}$$

---

## 5. Progresión de PS en 18 Líneas Evolutivas Representativas

Cuando un Pokémon evoluciona, su $\text{BaseHP}$ sufre un salto discreto denominado incremento de salud ($\Delta \text{PS} = \text{Base}_{\text{evolucionada}} - \text{Base}_{\text{previa}}$). A continuación se analizan 18 líneas canónicas que ilustran distintos patrones de progresión aritmética, geométrica y casos atípicos:

| # | Línea Evolutiva | Fase Básica (PS) | Fase Intermedia (PS) | Fase Final (PS) | Incrementos ($\Delta \text{PS}$) | Factor Crecimiento Total | Patrón Matemático |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Charmander** | Charmander (39) | Charmeleon (58) | Charizard (78) | $+19, \; +20$ | $78 / 39 = \mathbf{2,00\times}$ | Crecimiento equilibrado (duplica exactamente la base) |
| **2** | **Bulbasaur** | Bulbasaur (45) | Ivysaur (60) | Venusaur (80) | $+15, \; +20$ | $80 / 45 \approx \mathbf{1,78\times}$ | Incremento acelerado ($+15$ luego $+20$) |
| **3** | **Squirtle** | Squirtle (44) | Wartortle (59) | Blastoise (79) | $+15, \; +20$ | $79 / 44 \approx \mathbf{1,80\times}$ | Idénticos deltas a Bulbasaur ($+15, +20$) partiendo de 44 |
| **4** | **Pichu** | Pichu (20) | Pikachu (35) | Raichu (60) | $+15, \; +25$ | $60 / 20 = \mathbf{3,00\times}$ | Salto triple en 3 fases |
| **5** | **Magikarp** | Magikarp (20) | *(Evolución directa)* | Gyarados (95) | $+75$ | $95 / 20 = \mathbf{4,75\times}$ | **Salto Extremo:** multiplicación casi por 5 en una sola evolución |
| **6** | **Dratini** | Dratini (41) | Dragonair (61) | Dragonite (91) | $+20, \; +30$ | $91 / 41 \approx \mathbf{2,22\times}$ | Pseudo-legendario: deltas múltiplos de 10 ($+20, +30$) |
| **7** | **Gastly** | Gastly (30) | Haunter (45) | Gengar (60) | $+15, \; +15$ | $60 / 30 = \mathbf{2,00\times}$ | **Progresión Aritmética Constante ($d = +15$)** |
| **8** | **Machop** | Machop (70) | Machoke (80) | Machamp (90) | $+10, \; +10$ | $90 / 70 \approx \mathbf{1,29\times}$ | **Progresión Aritmética Constante ($d = +10$)** |
| **9** | **Beldum** | Beldum (40) | Metang (60) | Metagross (80) | $+20, \; +20$ | $80 / 40 = \mathbf{2,00\times}$ | **Progresión Aritmética Constante ($d = +20$)** |
| **10** | **Caterpie** | Caterpie (45) | Metapod (50) | Butterfree (60) | $+5, \; +10$ | $60 / 45 \approx \mathbf{1,33\times}$ | Progresión temprana de insecto (incrementos suaves) |
| **11** | **Larvitar** | Larvitar (50) | Pupitar (70) | Tyranitar (100) | $+20, \; +30$ | $100 / 50 = \mathbf{2,00\times}$ | Línea pseudo-legendaria: alcanza exactamente 100 de base |
| **12** | **Ralts** | Ralts (28) | Kirlia (38) | Gardevoir (68) | $+10, \; +30$ | $68 / 28 \approx \mathbf{2,43\times}$ | Salto final triplicado ($+10$ en fase 2 y $+30$ en fase 3) |
| **13** | **Bagon** | Bagon (45) | Shelgon (65) | Salamence (95) | $+20, \; +30$ | $95 / 45 \approx \mathbf{2,11\times}$ | Estructura gemela de incrementos ($+20, +30$) |
| **14** | **Gible** | Gible (58) | Gabite (68) | Garchomp (108) | $+10, \; +40$ | $108 / 58 \approx \mathbf{1,86\times}$ | Gran salto final ($+40$ en la fase 3) superando los 100 PS |
| **15** | **Riolu** | Riolu (40) | *(Evolución directa)* | Lucario (70) | $+30$ | $70 / 40 = \mathbf{1,75\times}$ | Evolución por amistad: salto directo de $+30$ PS |
| **16** | **Happiny** | Happiny (100) | Chansey (250) | Blissey (255) | $+150, \; +5$ | $255 / 100 = \mathbf{2,55\times}$ | **Récord Histórico de Tanques:** Chansey suma $+150$ PS |
| **17** | **Eevee** | Eevee (55) | *(8 Ramas)* | *(Ver tabla 5.1)* | Variable | Hasta $\mathbf{2,36\times}$ | **Matriz de Ramificación Múltiple (8 evoluciones)** |
| **18** | **Nincada** | Nincada (31) | Ninjask (61) | Shedinja (1) | Ninjask: $+30$<br>Shedinja: $-30$ ($\text{Fijo } 1$) | Ninjask: $1,97\times$<br>Shedinja: $\mathbf{0,03\times}$ | **Bifurcación Anómala:** Ninjask duplica vida, Shedinja colapsa a 1 |

---

### 5.1 Matriz de Ramificación de Eevee (BaseHP = 55)

Eevee es el ejemplo paradigmático de divergencia estadística. A partir de una estadística base idéntica ($\text{BaseHP} = 55$), sus 8 evoluciones adoptan perfiles matemáticos totalmente distintos:

| Evolución | Tipo Elemental | PS Base | Incremento ($\Delta \text{PS}$) | Aumento Porcentual | Arquetipo de Combate |
|:---|:---|:---:|:---:|:---:|:---|
| **Vaporeon** | Agua | **130** | $+75$ | $+136,4\%$ | **Tanque de Salud Especializado** (Mayor incremento) |
| **Umbreon** | Siniestro | **95** | $+40$ | $+72,7\%$ | Muro Defensivo Mixto |
| **Sylveon** | Hada | **95** | $+40$ | $+72,7\%$ | Muro Defensivo Especial |
| **Jolteon** | Eléctrico | **65** | $+10$ | $+18,2\%$ | Atacante Rápido (*Sweeper*) |
| **Flareon** | Fuego | **65** | $+10$ | $+18,2\%$ | Atacante Físico |
| **Espeon** | Psíquico | **65** | $+10$ | $+18,2\%$ | Atacante Especial Rápido |
| **Leafeon** | Planta | **65** | $+10$ | $+18,2\%$ | Defensor Físico |
| **Glaceon** | Hielo | **65** | $+10$ | $+18,2\%$ | Atacante Especial / Muro de Nieve |

*Propiedad matemática:* Seis de las ocho evoluciones aumentan exactamente $+10$ PS (llegando a 65), dos aumentan $+40$ PS (llegando a 95) y una única evolución aumenta $+75$ PS (llegando a 130).

---

## 6. Modelos Pedagógicos de Escala Adaptados a Primaria (LOMLOE 2º a 6º)

Para conectar la matemática formal de Pokémon con el currículo de Primaria (Real Decreto 157/2022), se definen 5 modelos pedagógicos escalonados por curso escolar:

---

### 6.1 Nivel 2º de Primaria: Aritmética de Barras de Salud (0 a 100)
- **Marco Curricular:** Sentido numérico, operaciones de suma y resta sin llevada y con llevada hasta el 100 o 999.
- **Modelo Didáctico:** Se trabaja directamente con los PS en combate como una cantidad que sube y baja.
- **Fórmula de Aula:**
  $$\text{PS}_{\text{final}} = \text{PS}_{\text{actual}} - \text{Daño} + \text{Poción}$$
- **Ejemplo de Problema:**  
  *Pikachu tiene 45 PS máximos. Un Geodude le inflige 18 puntos de daño con Lanzarrocas. Luego, el entrenador usa una Poción que restaura 20 PS. ¿Cuántos PS le quedan a Pikachu?*  
  - Operación 1: $45 - 18 = 27$ PS tras el ataque.  
  - Operación 2: $27 + 20 = 47$, pero como su vida máxima es 45, se queda en $45$ PS.  
  - **Resultado:** **45 PS**.

---

### 6.2 Nivel 3º de Primaria: Modelo Lineal Directo por Nivel
- **Marco Curricular:** Multiplicación por una cifra (tablas 1 a 10), sumas reiteradas, iniciación a fracciones ($\frac{1}{2}$).
- **Modelo Didáctico:** Para evitar la división compleja entre 100, se asume un crecimiento regular de **2 PS por cada nivel subido**, sumados a la base del Pokémon.
- **Fórmula Didáctica de 3º:**
  $$\text{PS}(L) = \text{BaseHP} + (2 \times L)$$
- **Ejemplo de Problema:**  
  *Un Bulbasaur tiene una estadística base de 45 PS. Si sube al Nivel 7, ¿cuántos PS máximos tendrá según el modelo de crecimiento directo?*  
  - Operación: $\text{PS} = 45 + (2 \times 7) = 45 + 14 = 59$ PS.  
  - ¿Cuántos PS corresponden a la mitad de su vida (barra amarilla)? $59 \div 2 = 29$ con resto 1 ($29,5$ PS).  
  - **Resultado:** **59 PS máximos** (la mitad son **29 PS**).

---

### 6.3 Nivel 4º de Primaria: Incrementos Evolutivos ($\Delta \text{PS}$) y División con Resto
- **Marco Curricular:** Multiplicación por 2 y 3 cifras, algoritmo de la división con resto ($D = d \cdot c + r$), fracciones sencillas ($\frac{1}{4}, \frac{1}{2}, \frac{3}{4}$).
- **Modelo Didáctico:** Estudio de la diferencia absoluta entre evoluciones ($\Delta \text{PS}$) y cálculo de golpes necesarios para debilitar.
- **Fórmulas Didácticas de 4º:**
  $$\Delta \text{PS} = \text{Base}_{\text{evolucionada}} - \text{Base}_{\text{inicial}}$$
  $$\text{Turnos para debilitar} = \lceil \text{PS}_{\max} \div \text{Daño} \rceil$$
- **Ejemplo de Problema:**  
  *Charmander tiene 39 PS de base y evoluciona a Charizard (78 PS base). ¿Cuál es la ganancia total de PS? Si un rival causa 15 de daño por turno, ¿cuántos turnos enteros resiste Charizard a vida completa?*  
  - Diferencia evolutiva: $78 - 39 = 39$ PS (se duplica).  
  - Turnos de combate: $78 \div 15 = 5$ con resto $3$. Con 5 turnos recibe $5 \times 15 = 75$ de daño, sobreviviendo con 3 PS. Por tanto, resiste 5 ataques enteros y cae al $6^{\circ}$ ataque.  
  - **Resultado:** **39 PS de ganancia; resiste 5 turnos enteros**.

---

### 6.4 Nivel 5º de Primaria: Modelo Canónico Simplificado a Nivel 50 y Nivel 100
- **Marco Curricular:** Operaciones combinadas con jerarquía, multiplicación y división por 10 y 100, números decimales, porcentajes ($25\%, 50\%, 75\%$).
- **Modelo Didáctico:** Uso de las fórmulas canónicas reducidas donde el nivel 50 y 100 simplifican algebraicamente la división.
- **Fórmulas Didácticas de 5º:**
  $$\text{PS}_{L=50} \approx \text{BaseHP} + 60$$
  $$\text{PS}_{L=100} \approx (2 \times \text{BaseHP}) + 110$$
- **Ejemplo de Problema:**  
  *Un Garchomp tiene una Base de 108 PS. Calcula sus PS a Nivel 50 y a Nivel 100 usando el modelo neutro. Si a Nivel 100 le queda el $25\%$ de vida, ¿cuántos PS tiene?*  
  - A Nivel 50: $\text{PS}_{50} = 108 + 60 = 168$ PS.  
  - A Nivel 100: $\text{PS}_{100} = (2 \times 108) + 110 = 216 + 110 = 326$ PS.  
  - Cuarta parte ($25\%$ de 326): $326 \times 0,25 = 326 \div 4 = 81,5$ (o $81$ PS).  
  - **Resultado:** **168 PS a nivel 50, 326 PS a nivel 100, y 81 PS al 25%**.

---

### 6.5 Nivel 6º de Primaria: Evaluación Canónica Completa con Función Suelo
- **Marco Curricular:** Jerarquía formal de operaciones con corchetes y paréntesis anidados, potencias, números enteros, proporcionalidad y uso formal del redondeo por defecto ($\lfloor x \rfloor$).
- **Modelo Didáctico:** Aplicación de la fórmula canónica completa de la saga principal con valores reales de IVs y EVs.
- **Fórmula de Aula de 6º:**
  $$\text{PS} = \left\lfloor \frac{(2 \cdot \text{BaseHP} + \text{IV} + \lfloor \frac{\text{EV}}{4} \rfloor) \cdot L}{100} \right\rfloor + L + 10$$
- **Ejemplo de Problema:**  
  *Calcula los PS exactos de un Snorlax a Nivel 42 ($L = 42$), sabiendo que tiene $\text{BaseHP} = 160$, genes $\text{IV} = 28$ y puntos de esfuerzo $\text{EV} = 76$.*  
  - Paso 1 (EVs entre 4): $\lfloor 76 \div 4 \rfloor = 19$.  
  - Paso 2 (Corchete interior): $(2 \times 160) + 28 + 19 = 320 + 28 + 19 = 367$.  
  - Paso 3 (Multiplicación por Nivel): $367 \times 42 = 15.414$.  
  - Paso 4 (División entre 100 y función suelo): $\lfloor 15.414 \div 100 \rfloor = \lfloor 154,14 \rfloor = 154$.  
  - Paso 5 (Suma de constantes finales): $154 + 42 + 10 = 206$ PS.  
  - **Resultado:** **206 PS**.

---

## 7. Tabla de Consulta Rápida: PS Estándar por Nivel (Casos Emblemáticos)

La siguiente tabla recoge los PS exactos calculados bajo parámetros neutros estándar ($\text{IV} = 15, \; \text{EV} = 0$) a lo largo de los niveles clave de la aventura Pokémon:

| Pokémon | Tipo | Base HP | Nivel 10 | Nivel 25 | Nivel 50 | Nivel 75 | Nivel 100 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pikachu** | Eléctrico | 35 | 28 | 56 | 102 | 148 | 195 |
| **Charmander** | Fuego | 39 | 29 | 58 | 106 | 154 | 203 |
| **Charizard** | Fuego / Volador | 78 | 37 | 77 | 145 | 213 | 281 |
| **Bulbasaur** | Planta / Veneno | 45 | 30 | 61 | 112 | 163 | 215 |
| **Venusaur** | Planta / Veneno | 80 | 37 | 78 | 147 | 216 | 285 |
| **Squirtle** | Agua | 44 | 30 | 60 | 111 | 162 | 213 |
| **Blastoise** | Agua | 79 | 37 | 78 | 146 | 214 | 283 |
| **Gyarados** | Agua / Volador | 95 | 40 | 86 | 162 | 238 | 315 |
| **Gengar** | Fantasma / Veneno | 60 | 33 | 68 | 127 | 186 | 245 |
| **Dragonite** | Dragón / Volador | 91 | 39 | 84 | 158 | 232 | 307 |
| **Tyranitar** | Roca / Siniestro | 100 | 41 | 88 | 167 | 246 | 325 |
| **Garchomp** | Dragón / Tierra | 108 | 43 | 92 | 175 | 258 | 341 |
| **Lucario** | Lucha / Acero | 70 | 35 | 73 | 137 | 201 | 265 |
| **Vaporeon** | Agua | 130 | 47 | 103 | 197 | 291 | 385 |
| **Chansey** | Normal | 250 | 71 | 163 | 317 | 471 | 625 |
| **Blissey** | Normal | 255 | 72 | 166 | 322 | 478 | 635 |
| **Shedinja** | Bicho / Fantasma | 1 | **1** | **1** | **1** | **1** | **1** |

---

## 8. Aviso Legal y Atribución Educativa

**Aviso Legal y de Atribución Educativa:**  
*Pokémon y todas las marcas, nombres de personajes, criaturas y mecánicas asociadas son marcas registradas y propiedad intelectual exclusiva de Nintendo Co., Ltd., Creatures Inc. y GAME FREAK Inc. Este material de referencia ha sido diseñado y redactado exclusivamente con fines educativos, formativos y de divulgación matemática curricular sin ningún ánimo de lucro, de conformidad con el Artículo 32.2 (Ilustración de la enseñanza) del Real Decreto Legislativo 1/1996, de 12 de abril (Ley de Propiedad Intelectual de España), y la doctrina internacional de Uso Legítimo (Fair Use, 17 U.S.C. § 107).*
