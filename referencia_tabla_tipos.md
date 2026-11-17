# Tabla de Tipos Pokémon y Multiplicadores de Daño: Guía de Referencia Matemática (LOMLOE)

**Proyecto:** Matemáticas Primaria con Pokémon (LOMLOE 2º a 6º de Educación Primaria)  
**Documento:** Referencia Técnica y Curricular de Tipos Elementales (Requisito R2)  
**Marco Legal:** Real Decreto 157/2022 (LOMLOE) — Sentido Numérico, Operaciones y Proporcionalidad  
**Versión de Mecánicas:** Generaciones VI a IX (Saga Principal)  

---

## 1. Introducción Didáctica y Marco Matemático

En el universo de Pokémon, cada criatura y cada movimiento de combate posee una o dos afinidades elementales denominadas **Tipos**. El sistema de combate está regido por una matriz de interacciones de tipo que determina la eficacia del daño infligido. Desde la introducción del tipo Hada en la 6ª Generación (Pokémon X/Y), el sistema cuenta con exactamente **18 tipos canónicos**.

Desde el punto de vista matemático y didáctico, la tabla de tipos constituye una aplicación real y motivadora del **álgebra de operadores multiplicativos**, el estudio de **fracciones**, **números decimales** y **sistemas de proporcionalidad**:

1. **Elemento Neutro de la Multiplicación ($x1$):** Cuando un movimiento impacta contra un Pokémon sin ventajas ni desventajas elementales, el daño base se multiplica por $1$.
2. **Duplicación y Cuadruplicación ($x2$ y $x4$):** Los ataques "Súper eficaces" multiplican el daño por $2$. Si el defensor posee un tipo dual con debilidad en ambos tipos, se aplica la propiedad asociativa de la multiplicación: $2 \times 2 = 4$ ($400\%$ del daño base).
3. **Fracciones y Reducción a la Mitad ($x0.5$ y $x0.25$):** Los ataques "Poco eficaces" reducen el daño a la mitad, operando como un factor de $\frac{1}{2}$ o decimal $0,5$. En tipos duales con doble resistencia, la fracción se multiplica: $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$ ($0,25$ o $25\%$ del daño base).
4. **Elemento Absorbente / Inmunidad ($x0$):** Ciertas interacciones anulan por completo el impacto, comportándose exactamente como la multiplicación por cero: cualquier cantidad multiplicada por cero resulta en cero ($D \times 0 = 0$).
5. **Bonificación por Mismo Tipo (STAB - Same-Type Attack Bonus, $x1.5$):** Cuando un Pokémon ejecuta un movimiento que coincide con alguno de sus tipos propios, el ataque recibe un multiplicador adicional de $\frac{3}{2}$ ($1,5$ o $+50\%$).

---

## 2. Escala Canónica de Multiplicadores de Daño

La siguiente tabla resume todos los multiplicadores posibles que pueden producirse en un combate Pokémon según la combinación de tipos y la bonificación STAB:

| Multiplicador Numérico | Notación Fraccionaria | Notación Porcentual | Denominación en el Juego | Efecto Matemático en el Daño ($D$) |
|:---:|:---:|:---:|:---|:---|
| **$x0$** | $\frac{0}{1}$ | $0\%$ | **Inmune / Sin efecto** | Anulación total: $D \times 0 = 0$ |
| **$x0.25$** | $\frac{1}{4}$ | $25\%$ | **Doble resistencia** | Reducción a la cuarta parte: $D \div 4$ |
| **$x0.375$** | $\frac{3}{8}$ | $37,5\%$ | **Doble resistencia + STAB** | $D \times \frac{1}{4} \times \frac{3}{2} = \frac{3}{8} D$ |
| **$x0.5$** | $\frac{1}{2}$ | $50\%$ | **Poco eficaz / Resistencia** | Reducción a la mitad: $D \div 2$ |
| **$x0.75$** | $\frac{3}{4}$ | $75\%$ | **Resistencia simple + STAB** | $D \times \frac{1}{2} \times \frac{3}{2} = \frac{3}{4} D$ |
| **$x1$** | $\frac{1}{1}$ | $100\%$ | **Daño neutro / Normal** | Daño estándar sin alteración: $D \times 1$ |
| **$x1.5$** | $\frac{3}{2}$ | $150\%$ | **Daño neutro + STAB** | Incremento del cincuenta por ciento: $D \times 1,5$ |
| **$x2$** | $\frac{2}{1}$ | $200\%$ | **Súper eficaz / Debilidad** | Daño duplicado: $D \times 2$ |
| **$x3$** | $\frac{3}{1}$ | $300\%$ | **Súper eficaz + STAB** | Triple de daño: $D \times 2 \times 1,5 = 3D$ |
| **$x4$** | $\frac{4}{1}$ | $400\%$ | **Doble debilidad** | Cuádruple de daño: $D \times 2 \times 2 = 4D$ |
| **$x6$** | $\frac{6}{1}$ | $600\%$ | **Doble debilidad + STAB** | Séxtuple de daño: $D \times 4 \times 1,5 = 6D$ |

---

## 3. Matriz Completa de Efectividad de Tipos 18×18

A continuación se presenta la matriz canónica completa de $18 \times 18$ interacciones individuales (Generaciones VI a IX).

- **Filas (Vertical):** Tipo del movimiento atacante (*Attacking Type*).
- **Columnas (Horizontal):** Tipo elemental del Pokémon defensor (*Defending Type*).
- **Valores en la tabla:**
  - `2`: Súper eficaz ($x2$, daño doble)
  - `½`: Poco eficaz ($x0.5$, daño a la mitad)
  - `0`: Sin efecto / Inmune ($x0$, daño nulo)
  - *(casilla vacía)*: Daño neutro ($x1$, daño normal estándar)

| Atacante ↓ / Defensor → | Nor | Fue | Agu | Pla | Ele | Hie | Luc | Ven | Tie | Vol | Psi | Bic | Roc | Fan | Dra | Sin | Ace | Had |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Normal** (Normal) | | | | | | | | | | | | | ½ | **0** | | | ½ | |
| **Fuego** (Fire) | | ½ | ½ | 2 | | 2 | | | | | | 2 | ½ | | ½ | | 2 | |
| **Agua** (Water) | | 2 | ½ | ½ | | | | | 2 | | | | 2 | | ½ | | | |
| **Planta** (Grass) | | ½ | 2 | ½ | | | | ½ | 2 | ½ | | ½ | 2 | | ½ | | ½ | |
| **Eléctrico** (Electric) | | | 2 | ½ | ½ | | | | **0** | 2 | | | | | ½ | | | |
| **Hielo** (Ice) | | ½ | ½ | 2 | | ½ | | | 2 | 2 | | | | | 2 | | ½ | |
| **Lucha** (Fighting) | 2 | | | | | 2 | | ½ | | ½ | ½ | ½ | 2 | **0** | | 2 | 2 | ½ |
| **Veneno** (Poison) | | | | 2 | | | | ½ | ½ | | | | ½ | ½ | | | **0** | 2 |
| **Tierra** (Ground) | | 2 | | ½ | 2 | | | 2 | | **0** | | ½ | 2 | | | | 2 | |
| **Volador** (Flying) | | | | 2 | ½ | | 2 | | | | | 2 | ½ | | | | ½ | |
| **Psíquico** (Psychic) | | | | | | | 2 | 2 | | | ½ | | | | | **0** | ½ | |
| **Bicho** (Bug) | | ½ | | 2 | | | ½ | ½ | | ½ | 2 | | | ½ | | 2 | ½ | ½ |
| **Roca** (Rock) | | 2 | | | | 2 | ½ | | ½ | 2 | | 2 | | | | | ½ | |
| **Fantasma** (Ghost) | **0** | | | | | | | | | | 2 | | | 2 | | ½ | | |
| **Dragón** (Dragon) | | | | | | | | | | | | | | | 2 | | ½ | **0** |
| **Siniestro** (Dark) | | | | | | | ½ | | | | 2 | | | 2 | | ½ | | ½ |
| **Acero** (Steel) | | ½ | ½ | | ½ | 2 | | | | | | | 2 | | | | ½ | 2 |
| **Hada** (Fairy) | | ½ | | | | | 2 | ½ | | | | | | | 2 | 2 | ½ | |

---

## 4. Desglose Exhaustivo por Tipo (18 Fichas Individuales)

A continuación se detalla el perfil ofensivo y defensivo completo de cada uno de los 18 tipos elementales:

---

### 4.1 Tipo Normal (Normal)
- **Identificador PokeAPI:** `normal`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Normal.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Ninguno (único tipo sin ventajas ofensivas).
  - **Poco eficaz contra ($x0.5$):** Roca, Acero.
  - **Ineficaz contra ($x0$):** Fantasma.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Lucha.
  - **Resistente a ($x0.5$):** Ninguno.
  - **Inmune a ($x0$):** Fantasma.
- **Aspecto Matemático Destacado:** Es el arquetipo más equilibrado para introducir el concepto de daño neutro ($x1$) y la inmunidad absoluta ($x0$).

---

### 4.2 Tipo Fuego (Fire)
- **Identificador PokeAPI:** `fire`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Fire.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Planta, Hielo, Bicho, Acero (4 tipos).
  - **Poco eficaz contra ($x0.5$):** Fuego, Agua, Roca, Dragón (4 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Agua, Tierra, Roca (3 tipos).
  - **Resistente a ($x0.5$):** Fuego, Planta, Hielo, Bicho, Acero, Hada (6 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Excelente ratio defensivo con 6 resistencias ($50\%$ de daño), ideal para problemas de división y fracciones.

---

### 4.3 Tipo Agua (Water)
- **Identificador PokeAPI:** `water`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Water.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Fuego, Tierra, Roca (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Agua, Planta, Dragón (3 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Eléctrico, Planta (2 debilidades).
  - **Resistente a ($x0.5$):** Fuego, Agua, Hielo, Acero (4 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Presenta simetría $3 \times 3$ en su faceta ofensiva (3 súper eficaces y 3 poco eficaces).

---

### 4.4 Tipo Planta (Grass)
- **Identificador PokeAPI:** `grass`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Grass.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Agua, Tierra, Roca (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Fuego, Planta, Veneno, Volador, Bicho, Dragón, Acero (7 tipos; máxima resistencia ofensiva del juego).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Fuego, Hielo, Veneno, Volador, Bicho (5 debilidades; comparte el récord negativo junto a Roca).
  - **Resistente a ($x0.5$):** Agua, Eléctrico, Planta, Tierra (4 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Su alta cantidad de resistencias ofensivas ($7/18 \approx 38,9\%$) permite ejercicios de fracciones y porcentajes.

---

### 4.5 Tipo Eléctrico (Electric)
- **Identificador PokeAPI:** `electric`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Electric.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Agua, Volador (2 tipos).
  - **Poco eficaz contra ($x0.5$):** Eléctrico, Planta, Dragón (3 tipos).
  - **Ineficaz contra ($x0$):** Tierra.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Tierra (única debilidad en todo el juego).
  - **Resistente a ($x0.5$):** Eléctrico, Volador, Acero (3 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Posee exactamente 1 debilidad defensiva ($1/18 \approx 5,56\%$), lo que lo convierte en un modelo perfecto de minimalismo probabilístico.

---

### 4.6 Tipo Hielo (Ice)
- **Identificador PokeAPI:** `ice`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Ice.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Planta, Tierra, Volador, Dragón (4 tipos clave).
  - **Poco eficaz contra ($x0.5$):** Fuego, Agua, Hielo, Acero (4 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Fuego, Lucha, Roca, Acero (4 debilidades).
  - **Resistente a ($x0.5$):** Hielo (única resistencia propia).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Es el tipo defensivamente más frágil ($1$ sola resistencia frente a $4$ debilidades), generando contrastes matemáticos de supervivencia.

---

### 4.7 Tipo Lucha (Fighting)
- **Identificador PokeAPI:** `fighting`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Fighting.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Normal, Hielo, Roca, Siniestro, Acero (5 tipos; récord ofensivo empatado con Tierra).
  - **Poco eficaz contra ($x0.5$):** Veneno, Volador, Psíquico, Bicho, Hada (5 tipos).
  - **Ineficaz contra ($x0$):** Fantasma.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Volador, Psíquico, Hada (3 tipos).
  - **Resistente a ($x0.5$):** Bicho, Roca, Siniestro (3 tipos).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Récord de $5$ ventajas ofensivas ($5/18 \approx 27,8\%$), excelente para problemas de probabilidad y conjuntos disjuntos.

---

### 4.8 Tipo Veneno (Poison)
- **Identificador PokeAPI:** `poison`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Poison.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Planta, Hada (2 tipos).
  - **Poco eficaz contra ($x0.5$):** Veneno, Tierra, Roca, Fantasma (4 tipos).
  - **Ineficaz contra ($x0$):** Acero.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Tierra, Psíquico (2 debilidades).
  - **Resistente a ($x0.5$):** Planta, Lucha, Veneno, Bicho, Hada (5 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Perfil defensivo altamente favorable ($5$ resistencias y solo $2$ debilidades), ideal para razones y proporciones ($5:2$).

---

### 4.9 Tipo Tierra (Ground)
- **Identificador PokeAPI:** `ground`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Ground.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Fuego, Eléctrico, Veneno, Roca, Acero (5 tipos; récord ofensivo empatado con Lucha).
  - **Poco eficaz contra ($x0.5$):** Planta, Bicho (2 tipos).
  - **Ineficaz contra ($x0$):** Volador.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Agua, Planta, Hielo (3 tipos).
  - **Resistente a ($x0.5$):** Veneno, Roca (2 tipos).
  - **Inmune a ($x0$):** Eléctrico.
- **Aspecto Matemático Destacado:** El único tipo que golpea súper eficaz a Eléctrico y Acero simultáneamente.

---

### 4.10 Tipo Volador (Flying)
- **Identificador PokeAPI:** `flying`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Flying.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Planta, Lucha, Bicho (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Eléctrico, Roca, Acero (3 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Eléctrico, Hielo, Roca (3 debilidades).
  - **Resistente a ($x0.5$):** Planta, Lucha, Bicho (3 resistencias).
  - **Inmune a ($x0$):** Tierra.
- **Aspecto Matemático Destacado:** Simetría reflexiva: los 3 tipos a los que golpea súper eficaz (Planta, Lucha, Bicho) son exactamente los 3 tipos a los que resiste defensivamente.

---

### 4.11 Tipo Psíquico (Psychic)
- **Identificador PokeAPI:** `psychic`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Psychic.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Lucha, Veneno (2 tipos).
  - **Poco eficaz contra ($x0.5$):** Psíquico, Acero (2 tipos).
  - **Ineficaz contra ($x0$):** Siniestro.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Bicho, Fantasma, Siniestro (3 debilidades).
  - **Resistente a ($x0.5$):** Lucha, Psíquico (2 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Inmunidad del tipo Siniestro ante ataques de tipo Psíquico ($D \times 0 = 0$).

---

### 4.12 Tipo Bicho (Bug)
- **Identificador PokeAPI:** `bug`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Bug.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Planta, Psíquico, Siniestro (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Fuego, Lucha, Veneno, Volador, Fantasma, Acero, Hada (7 tipos; empatado con Planta en mayor número de resistencias en contra).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Fuego, Volador, Roca (3 debilidades).
  - **Resistente a ($x0.5$):** Planta, Lucha, Tierra (3 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Ofensivamente resistido por $7/18$ tipos ($\approx 38,9\%$).

---

### 4.13 Tipo Roca (Rock)
- **Identificador PokeAPI:** `rock`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Rock.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Fuego, Hielo, Volador, Bicho (4 tipos).
  - **Poco eficaz contra ($x0.5$):** Lucha, Tierra, Acero (3 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Agua, Planta, Lucha, Tierra, Acero (5 debilidades; máximo del juego junto a Planta).
  - **Resistente a ($x0.5$):** Normal, Fuego, Veneno, Volador (4 resistencias).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Rango polarizado: $4$ ventajas ofensivas y $5$ debilidades defensivas.

---

### 4.14 Tipo Fantasma (Ghost)
- **Identificador PokeAPI:** `ghost`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Ghost.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Psíquico, Fantasma (2 tipos).
  - **Poco eficaz contra ($x0.5$):** Siniestro.
  - **Ineficaz contra ($x0$):** Normal.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Fantasma, Siniestro (2 debilidades).
  - **Resistente a ($x0.5$):** Veneno, Bicho (2 resistencias).
  - **Inmune a ($x0$):** Normal, Lucha (2 inmunidades; único tipo con doble inmunidad natural).
- **Aspecto Matemático Destacado:** Único tipo elemental con dos factores de anulación total ($x0$) en su defensa natural.

---

### 4.15 Tipo Dragón (Dragon)
- **Identificador PokeAPI:** `dragon`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Dragon.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Dragón (únicamente contra sí mismo).
  - **Poco eficaz contra ($x0.5$):** Acero.
  - **Ineficaz contra ($x0$):** Hada.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Hielo, Dragón, Hada (3 tipos).
  - **Resistente a ($x0.5$):** Fuego, Agua, Eléctrico, Planta (los 4 elementos clásicos).
  - **Inmune a ($x0$):** Ninguno.
- **Aspecto Matemático Destacado:** Resiste a los 4 tipos iniciales elementales a la vez, representando una probabilidad de resistencia acumulada del $4/18 \approx 22,2\%$.

---

### 4.16 Tipo Siniestro (Dark)
- **Identificador PokeAPI:** `dark`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Dark.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Psíquico, Fantasma (2 tipos).
  - **Poco eficaz contra ($x0.5$):** Lucha, Siniestro, Hada (3 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Lucha, Bicho, Hada (3 debilidades).
  - **Resistente a ($x0.5$):** Fantasma, Siniestro (2 resistencias).
  - **Inmune a ($x0$):** Psíquico.
- **Aspecto Matemático Destacado:** Factor cero absoluto frente a ataques Psíquicos ($D \times 0 = 0$).

---

### 4.17 Tipo Acero (Steel)
- **Identificador PokeAPI:** `steel`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Steel.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Hielo, Roca, Hada (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Fuego, Agua, Eléctrico, Acero (4 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Fuego, Lucha, Tierra (3 debilidades).
  - **Resistente a ($x0.5$):** Normal, Planta, Hielo, Volador, Psíquico, Bicho, Roca, Dragón, Acero, Hada (**10 resistencias; récord absoluto indiscutido**).
  - **Inmune a ($x0$):** Veneno.
- **Aspecto Matemático Destacado:** La fortaleza defensiva del tipo Acero protege contra $11$ de los $18$ tipos ($10$ resistencias $+ 1$ inmunidad), lo que equivale al $\frac{11}{18} \approx 61,1\%$ de todos los tipos existentes.

---

### 4.18 Tipo Hada (Fairy)
- **Identificador PokeAPI:** `fairy`
- **Icono / Badge Showdown:** `https://play.pokemonshowdown.com/sprites/types/Fairy.png`
- **Perfil Ofensivo (Al atacar):**
  - **Súper eficaz contra ($x2$):** Lucha, Dragón, Siniestro (3 tipos).
  - **Poco eficaz contra ($x0.5$):** Fuego, Veneno, Acero (3 tipos).
  - **Ineficaz contra ($x0$):** Ninguno.
- **Perfil Defensivo (Al defender):**
  - **Débil contra ($x2$):** Veneno, Acero (2 debilidades).
  - **Resistente a ($x0.5$):** Lucha, Bicho, Siniestro (3 resistencias).
  - **Inmune a ($x0$):** Dragón.
- **Aspecto Matemático Destacado:** Introducido en la Generación VI para reequilibrar la balanza probabilística, posee inmunidad completa contra el tipo Dragón ($D \times 0 = 0$).

---

## 5. Guía Matemática de Tipos Dobles (Multiplicación y Fracciones)

Aproximadamente la mitad de todas las especies de Pokémon poseen **dos tipos simultáneos** (por ejemplo, Charizard es Fuego/Volador; Swampert es Agua/Tierra). Cuando un ataque elemental impacta contra un Pokémon de tipo dual ($T_1 / T_2$), el multiplicador total es el **producto directo de los dos multiplicadores individuales**:

$$M_{\text{total}} = M(\text{Ataque} \to T_1) \times M(\text{Ataque} \to T_2)$$

El conjunto de valores posibles que puede tomar este producto forma un conjunto discreto de factores:

$$\mathcal{M} = \left\{ 0, \; \frac{1}{4}, \; \frac{1}{2}, \; 1, \; 2, \; 4 \right\} = \{ 0; \; 0,25; \; 0,5; \; 1; \; 2; \; 4 \}$$

### 5.1 Tabla de Operaciones de Multiplicadores Combinados

| Multiplicador en Tipo 1 ($M_1$) | Multiplicador en Tipo 2 ($M_2$) | Operación Aritmética | Multiplicador Total ($M_{\text{total}}$) | Efecto en Batalla | Denominación Didáctica |
|:---:|:---:|:---:|:---:|:---|:---|
| $2$ | $2$ | $2 \times 2$ | **$x4$** ($400\%$) | Doble debilidad | Cuádruple de daño |
| $2$ | $1$ | $2 \times 1$ | **$x2$** ($200\%$) | Debilidad simple | Doble de daño |
| $2$ | $0,5$ ($\frac{1}{2}$) | $2 \times \frac{1}{2} = \frac{2}{2}$ | **$x1$** ($100\%$) | Cancelación neutra | Daño normal estándar |
| $2$ | $0$ | $2 \times 0$ | **$x0$** ($0\%$) | Inmunidad absorbente | Daño nulo |
| $1$ | $1$ | $1 \times 1$ | **$x1$** ($100\%$) | Neutralidad pura | Daño normal estándar |
| $1$ | $0,5$ ($\frac{1}{2}$) | $1 \times \frac{1}{2}$ | **$x0.5$** ($50\%$) | Resistencia simple | Mitad de daño |
| $1$ | $0$ | $1 \times 0$ | **$x0$** ($0\%$) | Inmunidad absorbente | Daño nulo |
| $0,5$ ($\frac{1}{2}$) | $0,5$ ($\frac{1}{2}$) | $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$ | **$x0.25$** ($25\%$) | Doble resistencia | Cuarto de daño |
| $0,5$ ($\frac{1}{2}$) | $0$ | $\frac{1}{2} \times 0$ | **$x0$** ($0\%$) | Inmunidad absorbente | Daño nulo |
| $0$ | $0$ | $0 \times 0$ | **$x0$** ($0\%$) | Doble inmunidad | Daño nulo |

---

### 5.2 Casos de Estudio Canónicos de Combate

#### Caso 1: Doble Debilidad Cuádruple ($2 \times 2 = 4$)
- **Defensor:** Swampert (Tipo dual: **Agua / Tierra**).
- **Ataque entrante:** Hoja Aguda (Tipo **Planta**, potencia base $90$).
- **Cálculo del multiplicador:**
  - Planta contra Agua: $M_1 = 2$ (Súper eficaz).
  - Planta contra Tierra: $M_2 = 2$ (Súper eficaz).
  - Multiplicador total: $M_{\text{total}} = 2 \times 2 = \mathbf{4}$ ($x4$).
- **Consecuencia:** Swampert recibe el cuádruple ($400\%$) del daño base. Si el daño base estimado era $85$, el daño final resultante es $85 \times 4 = \mathbf{340}$ puntos de vida.

#### Caso 2: Doble Resistencia Cuarta ($0,5 \times 0,5 = 0,25$)
- **Defensor:** Kingdra (Tipo dual: **Agua / Dragón**).
- **Ataque entrante:** Lanzallamas (Tipo **Fuego**, potencia base $90$).
- **Cálculo del multiplicador:**
  - Fuego contra Agua: $M_1 = 0,5$ ($\frac{1}{2}$).
  - Fuego contra Dragón: $M_2 = 0,5$ ($\frac{1}{2}$).
  - Multiplicador total: $M_{\text{total}} = \frac{1}{2} \times \frac{1}{2} = \frac{1}{4} = \mathbf{0,25}$ ($x0.25$).
- **Consecuencia:** Kingdra absorbe el ataque reduciéndolo a la cuarta parte ($25\%$). Si el ataque infligiría $100$ PS a un objetivo neutro, Kingdra recibe únicamente $100 \times 0,25 = \mathbf{25}$ PS.

#### Caso 3: Cancelación Neutra ($2 \times 0,5 = 1$)
- **Defensor:** Ludicolo (Tipo dual: **Agua / Planta**).
- **Ataque entrante:** Rueda Fuego (Tipo **Fuego**, potencia base $60$).
- **Cálculo del multiplicador:**
  - Fuego contra Agua: $M_1 = 0,5$ (Resistencia).
  - Fuego contra Planta: $M_2 = 2,0$ (Debilidad).
  - Multiplicador total: $M_{\text{total}} = 0,5 \times 2 = \frac{1}{2} \times 2 = \frac{2}{2} = \mathbf{1,0}$ ($x1$).
- **Consecuencia:** Los dos factores se compensan mutuamente. Ludicolo recibe daño neutro estándar ($100\%$).

#### Caso 4: Inmunidad Absoluta que Anula Debilidad ($2 \times 0 = 0$)
- **Defensor:** Gliscor (Tipo dual: **Tierra / Volador**).
- **Ataque entrante:** Rayo (Tipo **Eléctrico**, potencia base $90$).
- **Cálculo del multiplicador:**
  - Eléctrico contra Volador: $M_1 = 2$ (Súper eficaz).
  - Eléctrico contra Tierra: $M_2 = 0$ (Inmune / Sin efecto).
  - Multiplicador total: $M_{\text{total}} = 2 \times 0 = \mathbf{0}$ ($x0$).
- **Consecuencia:** A pesar de que el tipo Volador es débil a Eléctrico, la propiedad absorbente del cero en el tipo Tierra anula completamente el ataque. Daño total infligido = $\mathbf{0}$ PS.

#### Caso 5: La Bonificación por Mismo Tipo (STAB) en Tipo Dual
- **Atacante:** Charizard (Fuego / Volador) usando Lanzallamas (Tipo Fuego).
- **Defensor:** Venusaur (Planta / Veneno).
- **Factores intervinientes:**
  - STAB: Al ser Charizard de tipo Fuego, recibe factor $\times 1,5$.
  - Fuego contra Planta: $M_1 = 2$ (Súper eficaz).
  - Fuego contra Veneno: $M_2 = 1$ (Neutro).
  - Multiplicador total de combate: $M = 1,5 \times (2 \times 1) = 1,5 \times 2 = \mathbf{3}$ ($x3$).
- **Consecuencia:** El daño final se triplica exactamente ($300\%$).

---

## 6. Conexión Pedagógica con el Currículo LOMLOE de Primaria

| Nivel Educativo | Saberes Básicos LOMLOE (Real Decreto 157/2022) | Aplicación con la Tabla de Tipos Pokémon | Ejemplo Didáctico de Aula |
|:---|:---|:---|:---|
| **2º de Primaria** | - Sentido Numérico: El concepto de doble y mitad.<br>- Suma repetida como iniciación al producto.<br>- Comparación y ordenación de números naturales hasta 999. | - Identificar ataques "Súper eficaces" como **el doble** ($2 \times D = D + D$).<br>- Identificar ataques "Poco eficaces" como **la mitad** de la cantidad base.<br>- El concepto de cero como "no recibir nada" ($0$). | "Pikachu usa Impactrueno contra Squirtle (daño doble). Si el ataque normal causa 14 puntos de daño, ¿cuánto daño hace el doble? $14 + 14 = 28$ puntos". |
| **3º de Primaria** | - Tablas de multiplicar (del 1 al 10).<br>- Multiplicación por una cifra.<br>- División exacta como reparto en partes iguales.<br>- Fracción elemental: un medio ($\frac{1}{2}$). | - Aplicar formalmente el factor $x2$ y la división $\div 2$.<br>- Tablas de doble entrada: lectura de filas y columnas en la matriz elemental. | "Un ataque de tipo Agua de 36 puntos de potencia impacta contra un Geodude (Roca). Al ser súper eficaz ($x2$), ¿cuál es el daño total? $36 \times 2 = 72$". |
| **4º de Primaria** | - Multiplicación de números de dos y tres cifras.<br>- División entera con resto.<br>- Fracción de una cantidad ($\frac{1}{2}$ y $\frac{1}{4}$).<br>- Números decimales: décimas y centésimas ($0,5$ y $0,25$). | - Multiplicar por factores combinados de tipo dual ($x4$ y $x0.25$).<br>- Demostrar que dividir entre $4$ equivale a calcular la cuarta parte ($\frac{1}{4}$). | "Kingdra recibe un ataque de tipo Fuego de 80 puntos de daño. Si su resistencia es $\frac{1}{4}$ ($x0.25$), ¿cuánto daño recibe? $80 \div 4 = 20$ puntos". |
| **5º de Primaria** | - Operaciones combinadas y jerarquía de operaciones.<br>- Multiplicación de fracciones: $\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$.<br>- Números decimales: multiplicación por $1,5$ (STAB).<br>- Porcentajes elementales ($25\%$, $50\%$, $150\%$, $200\%$, $400\%$). | - Cálculo simultáneo de debilidad de tipo y bonificación STAB: $\text{Daño} \times 1,5 \times 2$.<br>- Conversión entre multiplicador decimal y porcentaje de daño. | "Un ataque con daño base de 50 puntos tiene STAB ($x1.5$) y es súper eficaz ($x2$). Calcula: $50 \times 1,5 \times 2 = 50 \times 3 = 150$ puntos ($300\%$)". |
| **6º de Primaria** | - Jerarquía de operaciones con paréntesis y corchetes.<br>- Proporcionalidad directa y cálculo de porcentajes sucesivos.<br>- Estructura de matrices y conjuntos discretos de operadores.<br>- Operaciones con números racionales y decimales periódicos/exactos. | - Modelización algebraica formal del daño elemental: $D_f = D_b \cdot \text{STAB} \cdot \prod_{i=1}^{k} M_i$.<br>- Análisis combinatorio de los 18 tipos: ¿cuántas combinaciones duales existen? $\binom{18}{2} + 18 = 153 + 18 = 171$ tipos posibles. | "Si existen 18 tipos elementales simples, ¿cuántas combinaciones duales únicas existen sin importar el orden? $\frac{18 \times 17}{2} = 153$ combinaciones duales". |

---

## 7. Aviso Legal y Atribución Educativa

**Aviso Legal y de Atribución Educativa:**  
*Pokémon y todas las marcas, nombres de personajes, criaturas y tipos asociados son marcas registradas y propiedad intelectual exclusiva de Nintendo Co., Ltd., Creatures Inc. y GAME FREAK Inc. Este material de referencia ha sido diseñado y redactado exclusivamente con fines educativos, formativos y de divulgación matemática curricular sin ningún ánimo de lucro, de conformidad con el Artículo 32.2 (Ilustración de la enseñanza) del Real Decreto Legislativo 1/1996, de 12 de abril (Ley de Propiedad Intelectual de España), y la doctrina internacional de Uso Legítimo (Fair Use, 17 U.S.C. § 107).*
