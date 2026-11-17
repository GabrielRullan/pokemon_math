# Guía de Recursos, Fuentes de Datos y Activos Visuales Pokémon: Manual de Integración Educativa (LOMLOE)

**Proyecto:** Matemáticas Primaria con Pokémon (LOMLOE 2º a 6º de Educación Primaria)  
**Documento:** Guía de Aprovisionamiento de Activos y Fuentes de Datos (Requisito R3)  
**Marco Legal:** Real Decreto 157/2022 (LOMLOE) & Real Decreto Legislativo 1/1996 (Art. 32.2 LPI)  
**Destinatarios:** Docentes de Educación Primaria, Diseñadores de Material Didáctico y Desarrolladores  

---

## 1. Introducción y Propósito del Documento

El presente documento constituye la guía canónica de referencia para la obtención, consulta e incrustación de datos estadísticos, tablas mecánicas y recursos gráficos del universo Pokémon en fichas de trabajo, exámenes y materiales didácticos de matemáticas de Educación Primaria (cursos 2º a 6º de Primaria bajo el marco LOMLOE).

Todas las fuentes, APIs REST y redes de distribución de contenidos (CDNs) documentadas en esta guía han sido verificadas empíricamente, son de **acceso público y gratuito**, y permiten su utilización directa sin requerir claves de API (*API keys*) privadas.

---

## 2. PokeAPI REST v2 (Especificaciones y Endpoints Verificados)

[PokeAPI](https://pokeapi.co/) es la mayor base de datos abierta y estructurada sobre Pokémon en formato JSON.

### 2.1 Especificaciones Técnicas y Parámetros de Red
- **URL Base:** `https://pokeapi.co/api/v2/`
- **Protocolo:** HTTPS con soporte HTTP/2 y compresión gzip/brotli.
- **Cabeceras CORS:** Totalmente permisivas (`Access-Control-Allow-Origin: *`). Permite peticiones directas desde aplicaciones web cliente, navegadores y libretas Jupyter.
- **Políticas de Caché:** Cabecera `Cache-Control: public, max-age=86400` (los recursos se conservan 24 horas en caché).
- **Límites de Petición (*Rate Limiting*):** Aproximadamente 100 peticiones por minuto por dirección IP.
- **Recomendación para Aula:** Para generar bancos de problemas o trabajar sin conexión en el aula, se recomienda descargar las tablas CSV de respaldo o consultar directamente las URLs de la CDN de GitHub Raw, las cuales carecen de límites de tasa.

---

### 2.2 Catálogo de Endpoints REST Clave

#### 1. Endpoint de Especie y Estadísticas de Combate: `GET /pokemon/{id_o_nombre}`
- **Ejemplo:** `https://pokeapi.co/api/v2/pokemon/1` (Bulbasaur) o `https://pokeapi.co/api/v2/pokemon/pikachu`
- **Campos esenciales para problemas matemáticos:**
  - `id`: Número en la Pokédex Nacional (entero).
  - `name`: Nombre en inglés (cadena en minúsculas).
  - `height`: Altura en **decímetros (dm)**. *(Ver sección 2.3 para su aplicación didáctica)*.
  - `weight`: Peso en **hectogramos (hg)**. *(Ver sección 2.3 para su aplicación didáctica)*.
  - `base_experience`: Experiencia base obtenida al derrotarlo en combate ($b$).
  - `stats`: Matriz con los valores base de las 6 características de combate:
    - `stats[0]` (`hp`): Puntos de Salud base ($\text{BaseHP}$).
    - `stats[1]` (`attack`): Ataque físico base.
    - `stats[2]` (`defense`): Defensa física base.
    - `stats[3]` (`special-attack`): Ataque especial base.
    - `stats[4]` (`special-defense`): Defensa especial base.
    - `stats[5]` (`speed`): Velocidad base.
  - `types`: Tipos elementales (ranuras 1 y 2).
  - `sprites`: Objeto con punteros a las imágenes oficiales.

#### 2. Endpoint de Especie y Lore Multilingüe: `GET /pokemon-species/{id_o_nombre}`
- **Ejemplo:** `https://pokeapi.co/api/v2/pokemon-species/25` (Pikachu)
- **Campos esenciales para problemas matemáticos:**
  - `names`: Nombres localizados. Filtrando por `language.name == "es"` se obtiene la denominación oficial en español.
  - `flavor_text_entries`: Textos de la Pokédex en español (`language.name == "es"`), ideales para redactar el contexto narrativo de los problemas.
  - `capture_rate`: Ratio base de captura ($3$ a $255$), indispensable para problemas de fracciones y probabilidad en 5º y 6º de Primaria.
  - `base_happiness`: Amistad base ($0$ a $255$), empleada en evoluciones por afecto.
  - `growth_rate`: Referencia a la curva de crecimiento de experiencia.
  - `evolution_chain`: Enlace al árbol genealógico evolutivo.

#### 3. Endpoint de Tipos Elementales: `GET /type/{id_o_nombre}`
- **Ejemplo:** `https://pokeapi.co/api/v2/type/10` (Fuego) o `https://pokeapi.co/api/v2/type/water`
- **Campos esenciales:**
  - `damage_relations`: Contiene las listas completas de interacciones:
    - `double_damage_to` ($x2$, súper eficaz)
    - `half_damage_to` ($x0.5$, poco eficaz)
    - `no_damage_to` ($x0$, inmune)
    - `double_damage_from` ($x2$, debilidad)
    - `half_damage_from` ($x0.5$, resistencia)
    - `no_damage_from` ($x0$, inmunidad defensiva)
  - `names`: Nombre traducido al español (`Fuego`, `Agua`, `Planta`, etc.).

#### 4. Endpoint de Curvas de Experiencia: `GET /growth-rate/{id_o_nombre}`
- **Ejemplo:** `https://pokeapi.co/api/v2/growth-rate/2` (`medium`, Medio Rápido)
- **Campos esenciales:**
  - `formula`: Expresión algebraica en notación matemática / LaTeX de la curva.
  - `levels`: Lista de 100 elementos con el total exacto de EXP requerida para cada nivel desde el 1 hasta el 100.

#### 5. Endpoint de Cadena Evolutiva: `GET /evolution-chain/{id}`
- **Ejemplo:** `https://pokeapi.co/api/v2/evolution-chain/1` (Línea de Bulbasaur)
- **Campos esenciales:**
  - `chain.species.name`: Fase básica inicial.
  - `chain.evolves_to`: Árbol con las fases intermedias y finales.
  - `evolution_details.min_level`: Nivel mínimo requerido para desencadenar la evolución (ej. Nivel 16 para Ivysaur, Nivel 32 para Venusaur).

#### 6. Endpoint de Objetos y Economía: `GET /item/{id_o_nombre}`
- **Ejemplo:** `https://pokeapi.co/api/v2/item/4` (`poke-ball`) o `https://pokeapi.co/api/v2/item/potion`
- **Campos esenciales:**
  - `cost`: Precio oficial de compra en Pokédólares / Pokécuartos (₽).
  - `names`: Nombre del objeto en español (`language.name == "es"`).
  - `sprites.default`: URL directa del icono del objeto.

---

### 2.3 Nota Didáctica Esencial: Unidades Métricas en PokeAPI

Uno de los aspectos pedagógicamente más potentes de PokeAPI para el currículo LOMLOE de Matemáticas (Sentido de la Medida) reside en sus unidades de almacenamiento:

1. **Altura (`height`):** Se almacena en **decímetros (dm)**.
   - Para convertir a **metros (m)**: Dividir entre $10$ (desplazar la coma un lugar a la izquierda).
   - Para convertir a **centímetros (cm)**: Multiplicar por $10$.
   - *Ejemplo en Bulbasaur:* `height = 7` $\implies 7\text{ dm} = 0,7\text{ m} = 70\text{ cm}$.
   - *Ejemplo en Charizard:* `height = 17` $\implies 17\text{ dm} = 1,7\text{ m} = 170\text{ cm}$.
   - *Ejemplo en Wailord:* `height = 145` $\implies 145\text{ dm} = 14,5\text{ m} = 1.450\text{ cm}$.

2. **Peso (`weight`):** Se almacena en **hectogramos (hg)**.
   - Para convertir a **kilogramos (kg)**: Dividir entre $10$.
   - Para convertir a **gramos (g)**: Multiplicar por $100$.
   - *Ejemplo en Bulbasaur:* `weight = 69` $\implies 69\text{ hg} = 6,9\text{ kg} = 6.900\text{ g}$.
   - *Ejemplo en Pikachu:* `weight = 60` $\implies 60\text{ hg} = 6,0\text{ kg} = 6.000\text{ g}$.
   - *Ejemplo en Snorlax:* `weight = 4600` $\implies 4600\text{ hg} = 460,0\text{ kg} = 460.000\text{ g}$.

*Aplicación LOMLOE:* Esta característica permite plantear de forma nativa problemas reales de conversión entre múltiplos y submúltiplos del Sistema Internacional de Unidades para 3º, 4º y 5º de Primaria.

---

## 3. Red CDN de Sprites de GitHub Raw (PokeAPI/sprites)

PokeAPI almacena todo su catálogo visual en el repositorio público de GitHub [`PokeAPI/sprites`](https://github.com/PokeAPI/sprites). Al ser servidas a través de `raw.githubusercontent.com`, estas URLs **no tienen límite de tasa**, admiten incrustación directa en documentos Markdown y páginas web, y garantizan una alta disponibilidad global.

### 3.1 Plantillas de URLs de la CDN

| Variedad de Activo | Plantilla de URL Directa | Formato y Dimensiones | Ejemplo Verificado (#1 Bulbasaur) |
|:---|:---|:---:|:---|
| **Ilustración Oficial (*Official Artwork*)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png` | PNG $475 \times 475$ px (Fondo transparente) | `.../official-artwork/1.png` |
| **Ilustración Oficial Variocolor (*Shiny*)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{id}.png` | PNG $475 \times 475$ px | `.../official-artwork/shiny/1.png` |
| **Sprite Frontal Clásico (Pixel Art)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png` | PNG $96 \times 96$ px | `.../sprites/pokemon/1.png` |
| **Sprite Trasero Clásico** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{id}.png` | PNG $96 \times 96$ px | `.../sprites/pokemon/back/1.png` |
| **Sprite Frontal Variocolor (*Shiny*)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{id}.png` | PNG $96 \times 96$ px | `.../sprites/pokemon/shiny/1.png` |
| **Vectorial Dream World (SVG)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/{id}.svg` | Vectorial SVG escalable (Gen 1 a 5) | `.../dream-world/1.svg` |
| **Modelo 3D Pokémon HOME** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{id}.png` | PNG $512 \times 512$ px | `.../other/home/1.png` |
| **GIF Animado Showdown (Frente)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{id}.gif` | GIF Animado | `.../other/showdown/1.gif` |
| **GIF Animado Showdown (Espalda)** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/{id}.gif` | GIF Animado | `.../other/showdown/back/1.gif` |
| **GIF Animado Gen 5 B/N** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{id}.gif` | GIF Animado 2D | `.../generation-v/black-white/animated/1.gif` |
| **Sprite de Objeto / Ítem** | `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{item_slug}.png` | PNG $32 \times 32$ px | `.../sprites/items/poke-ball.png` |

*Nota sobre IDs:* El parámetro `{id}` corresponde siempre al número de Pokédex Nacional sin ceros a la izquierda (por ejemplo, `1` para Bulbasaur, `25` para Pikachu, `150` para Mewtwo).

---

## 4. Repositorio de Activos de Pokémon Showdown (`play.pokemonshowdown.com`)

[Pokémon Showdown](https://pokemonshowdown.com/) es el simulador de combate competitivo de código abierto de referencia mundial. Su servidor de contenidos proporciona activos visuales estáticos y animados de todas las generaciones, insignias de tipo e iconos de objetos.

### 4.1 Regla Canónica de Normalización de Nombres (*Slugs*)
A diferencia de PokeAPI (que utiliza identificadores numéricos enteros), Pokémon Showdown organiza sus archivos mediante nombres en texto (*slugs*). Para garantizar una llamada correcta sin errores 404, es **obligatorio** aplicar la siguiente regla:

$$\text{Slug} = \text{minusculas}(\text{filtrar\_alfanumerico}(Nombre)) \in [a\text{-}z0\text{-}9]$$

1. Transformar todo el texto a **minúsculas estrictas**.
2. **Eliminar por completo** espacios, puntos, guiones, apóstrofes y signos de puntuación:
   - `Mr. Mime` $\to$ `mrmime`
   - `Farfetch'd` $\to$ `farfetchd`
   - `Type: Null` $\to$ `typenull`
   - `Tapu Koko` $\to$ `tapukoko`
   - `Ho-Oh` $\to$ `hooh`
   - `Porygon-Z` $\to$ `porygonz`
   - `Jangmo-o` $\to$ `jangmoo`
3. **Casos especiales de género:**
   - `Nidoran♀` $\to$ `nidoranf`
   - `Nidoran♂` $\to$ `nidoranm`

---

### 4.2 Catálogo de Directorios y URLs de Showdown

- **URL Base:** `https://play.pokemonshowdown.com/sprites/`

| Directorio y Ruta | Formato y Contenido | Ejemplo de URL Completa |
|:---|:---|:---|
| `gen5/{slug}.png` | Sprite estático 2D estilo Blanco/Negro | `https://play.pokemonshowdown.com/sprites/gen5/pikachu.png` |
| `gen5ani/{slug}.gif` | Sprite animado 2D pixel art | `https://play.pokemonshowdown.com/sprites/gen5ani/pikachu.gif` |
| `ani/{slug}.gif` | Modelo 3D animado oficial (Gen 6 a 9) | `https://play.pokemonshowdown.com/sprites/ani/pikachu.gif` |
| `ani-back/{slug}.gif` | Modelo 3D animado de espalda | `https://play.pokemonshowdown.com/sprites/ani-back/pikachu.gif` |
| `ani-shiny/{slug}.gif` | Modelo 3D animado variocolor (*shiny*) | `https://play.pokemonshowdown.com/sprites/ani-shiny/pikachu.gif` |
| `dex/{slug}.png` | Icono miniatura de la Pokédex | `https://play.pokemonshowdown.com/sprites/dex/pikachu.png` |
| `types/{Type}.png` | Insignia oficial de tipo elemental (*Title-Case*) | `https://play.pokemonshowdown.com/sprites/types/Electric.png` |
| `categories/{Cat}.png` | Insignia de categoría física/especial/estado | `https://play.pokemonshowdown.com/sprites/categories/Physical.png` |
| `itemicons/{item}.png` | Icono de objeto con guiones | `https://play.pokemonshowdown.com/sprites/itemicons/ultra-ball.png` |
| `trainers/{trainer}.png` | Sprite de entrenador para narrativa | `https://play.pokemonshowdown.com/sprites/trainers/red.png` |

*Nota sobre Badges de Tipos:* En el directorio `types/`, los nombres de archivo inician con mayúscula: `Normal.png`, `Fire.png`, `Water.png`, `Grass.png`, `Electric.png`, `Ice.png`, `Fighting.png`, `Poison.png`, `Ground.png`, `Flying.png`, `Psychic.png`, `Bug.png`, `Rock.png`, `Ghost.png`, `Dragon.png`, `Dark.png`, `Steel.png`, `Fairy.png`.

---

## 5. Base de Datos Relacional Veekun (Distribución CSV en GitHub)

La base de datos [Veekun](https://github.com/veekun/pokedex) (creada por Alex Munroe) es la fuente relacional de código abierto que sirve de cimiento para PokeAPI. Se distribuye como una colección de archivos CSV en texto plano, lo que permite su descarga directa o análisis con librerías como Pandas, Python o Excel para validar problemas matemáticos en masa.

- **Repositorio GitHub:** `https://github.com/veekun/pokedex`
- **Ruta Base de Descarga Raw:** `https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/`

### 5.1 Tablas Maestras para Matemáticas Escolares

1. **`pokemon.csv`**
   - **Columnas:** `id, identifier, species_id, height, weight, base_experience, order, is_default`
   - **Utilidad:** Datos canónicos de altura ($dm$), peso ($hg$) y rendimiento base de experiencia ($b$) para todas las especies.
2. **`pokemon_stats.csv`**
   - **Columnas:** `pokemon_id, stat_id, base_stat, effort`
   - **Clave de atributos:** `1` = PS, `2` = Ataque, `3` = Defensa, `4` = At. Especial, `5` = Def. Especial, `6` = Velocidad.
   - **Utilidad:** Consulta rápida y verificación de estadísticas base para problemas de progresión de PS.
3. **`experience.csv`**
   - **Columnas:** `growth_rate_id, level, experience`
   - **Utilidad:** Tabla precalculada con los $600$ registros exactos de experiencia acumulada para cada uno de los 100 niveles en las 6 curvas de crecimiento. Previene errores de coma flotante en las soluciones del solucionario.
4. **`growth_rates.csv`**
   - **Columnas:** `id, identifier, formula`
   - **Utilidad:** Definición matemática formal de las curvas cúbicas y polinómicas:
     - ID 1 (`slow` / Lento): $EXP = \frac{5 x^3}{4}$ ($1.250.000$ a nivel 100).
     - ID 2 (`medium` / Medio Rápido): $EXP = x^3$ ($1.000.000$ a nivel 100).
     - ID 3 (`fast` / Rápido): $EXP = \frac{4 x^3}{5}$ ($800.000$ a nivel 100).
     - ID 4 (`medium-slow` / Medio Lento): $EXP = \frac{6 x^3}{5} - 15 x^2 + 100 x - 140$ ($1.059.860$ a nivel 100).
5. **`type_efficacy.csv`**
   - **Columnas:** `damage_type_id, target_type_id, damage_factor`
   - **Factores:** `0` ($x0$), `50` ($x0.5$), `100` ($x1.0$), `200` ($x2.0$).
   - **Utilidad:** Los $324$ registros que componen la matriz completa de $18 \times 18$ interacciones elementales.
6. **`pokemon_species.csv`**
   - **Columnas:** `id, identifier, generation_id, evolves_from_species_id, evolution_chain_id, capture_rate, base_happiness...`
   - **Utilidad:** Mapeo de progenitores evolutivos y ratios de captura ($3$ a $255$).

---

## 6. Pokémon Database (`pokemondb.net`) y Pokédex Oficial (`pokemon.com`)

### 6.1 Pokémon Database
- **Portal Principal:** `https://pokemondb.net/`
- **CDN de Ilustraciones:** `https://img.pokemondb.net/artwork/{slug}.jpg` (ej. `https://img.pokemondb.net/artwork/charizard.jpg`).
- **CDN de Modelos HOME:** `https://img.pokemondb.net/sprites/home/normal/{slug}.png`.

### 6.2 Pokédex Oficial de The Pokémon Company International
- **Portal Oficial en Español:** `https://www.pokemon.com/es/pokedex/{slug}` (descripciones y fichas técnicas oficiales revisadas en castellano).
- **CDN Oficial de Ilustraciones en Alta Resolución:**
  - **URL Base:** `https://assets.pokemon.com/assets/cms2/img/pokedex/full/`
  - **Regla Estricta de Relleno con Ceros (*Zero-Padding*):**
    - Para números del $1$ al $999$: Se deben rellenar con ceros a la izquierda hasta completar **3 dígitos exactos** (`001.png`, `004.png`, `025.png`, `150.png`, `999.png`).
    - Para números del $1000$ en adelante: Se utilizan **4 dígitos** (`1000.png` para Gholdengo, `1008.png` para Miraidon).
  - **Ejemplo Verificado (#25 Pikachu):**  
    `https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png`

---

## 7. Ejemplos Prácticos de Incrustación en Markdown y HTML

### 7.1 Imagen Estándar en Markdown (Diseño Responsivo Básico)
Ideal para enunciados limpios en fichas de trabajo digitales:
```markdown
![Pikachu](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png)
```

---

### 7.2 Incrustación en HTML con Control Explícito de Dimensiones
Recomendada para maquetaciones impresas, fichas en PDF o pantallas de tableta donde se requiera fijar el ancho y alto exactos:
```html
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png" 
     alt="Pikachu" 
     width="100" 
     height="100" 
     style="vertical-align: middle; display: inline-block;" />
```

---

### 7.3 Renderizado Pixelado Nítido (Evitar Desenfoque Bilineal en Sprites Retro)
Por defecto, los motores de renderizado de los navegadores web modernos aplican un filtro bilineal o bicúbico al reescalar imágenes pequeñas de pixel art (como los sprites clásicos de $96 \times 96$ px), provocando un efecto borroso.

Para conservar los píxeles nítidos y definidos al ampliar los sprites, es **imprescindible** aplicar las siguientes propiedades CSS:

```html
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png" 
     alt="Charmander Pixel Art" 
     width="96" 
     height="96" 
     style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; image-rendering: crisp-edges;" />
```

---

### 7.4 Tabla Didáctica de Problemas con Sprites Incrustados
Plantilla lista para su integración en bancos de problemas:

```markdown
| Pokémon | Sprite Pixel Art | Tipo Elemental | PS Base | Altura (dm $\to$ m) | Peso (hg $\to$ kg) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Charmander** | <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png" width="48" height="48" style="image-rendering: pixelated;"/> | Fuego | 39 | $6\text{ dm} = 0,6\text{ m}$ | $85\text{ hg} = 8,5\text{ kg}$ |
| **Squirtle** | <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png" width="48" height="48" style="image-rendering: pixelated;"/> | Agua | 44 | $5\text{ dm} = 0,5\text{ m}$ | $90\text{ hg} = 9,0\text{ kg}$ |
| **Bulbasaur** | <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png" width="48" height="48" style="image-rendering: pixelated;"/> | Planta / Veneno | 45 | $7\text{ dm} = 0,7\text{ m}$ | $69\text{ hg} = 6,9\text{ kg}$ |
```

---

### 7.5 Tarjeta de Batalla (*Battle Card Showcase*) con Diseño Flexbox
Plantilla visualmente atractiva para problemas de comparación de vida o turnos:

```html
<div style="display: flex; align-items: center; justify-content: space-around; background-color: #f8fafc; border: 2px solid #cbd5e1; border-radius: 12px; padding: 16px; margin: 16px 0;">
  <div style="text-align: center;">
    <img src="https://play.pokemonshowdown.com/sprites/ani/pikachu.gif" alt="Pikachu" style="height: 80px;" /><br>
    <strong>Pikachu (Nv. 25)</strong><br>
    <span style="color: #16a34a; font-weight: bold;">PS: 56 / 56</span><br>
    <small>Velocidad: 60</small>
  </div>
  <div style="font-size: 28px; font-weight: 900; color: #dc2626; padding: 0 20px;">
    VS
  </div>
  <div style="text-align: center;">
    <img src="https://play.pokemonshowdown.com/sprites/ani/gyarados.gif" alt="Gyarados" style="height: 100px;" /><br>
    <strong>Gyarados (Nv. 25)</strong><br>
    <span style="color: #16a34a; font-weight: bold;">PS: 86 / 86</span><br>
    <small>Velocidad: 52</small>
  </div>
</div>
```

---

## 8. Diccionario Terminológico Español - Inglés

Para facilitar el desarrollo de problemas bajo la LOMLOE manteniendo la coherencia con PokeAPI y las fuentes internacionales, se proporciona la siguiente correspondencia unívoca de términos:

### 8.1 Estadísticas y Atributos de Combate

| Término en Español (LOMLOE) | Abreviatura (ES) | Clave PokeAPI (EN) | Significado Matemático Curricular |
|:---|:---:|:---|:---|
| **Puntos de Salud** / Puntos de Vida | **PS** | `hp` | Cantidad escalar acotada; sustracción de daño, sumas de poción, progresión evolutiva |
| **Ataque** (Físico) | **Atq** | `attack` | Factor multiplicativo del daño físico |
| **Defensa** (Física) | **Def** | `defense` | Divisor de reducción del daño físico |
| **Ataque Especial** | **At. Esp.** | `special-attack` | Factor multiplicativo del daño energético/especial |
| **Defensa Especial** | **Def. Esp.** | `special-defense` | Divisor de reducción del daño especial |
| **Velocidad** | **Vel** | `speed` | Relación de orden ($>$, $<$, $=$) y prioridad temporal en turnos de combate |
| **Altura** | **Alt** | `height` | Longitud en decímetros ($dm$); conversión métrica a metros y centímetros |
| **Peso** | **Peso** | `weight` | Masa en hectogramos ($hg$); conversión métrica a kilogramos y gramos |
| **Experiencia Base** | **EXP Base** | `base_experience` | Coeficiente $b$ en la fórmula canónica de derrota en combate |

---

### 8.2 Tipos Elementales y URLs de Badges

| # | Nombre en Español (Oficial) | Identificador PokeAPI (EN) | URL de la Insignia Showdown (*Badge*) |
|:---:|:---|:---|:---|
| 1 | **Normal** | `normal` | `https://play.pokemonshowdown.com/sprites/types/Normal.png` |
| 2 | **Lucha** | `fighting` | `https://play.pokemonshowdown.com/sprites/types/Fighting.png` |
| 3 | **Volador** | `flying` | `https://play.pokemonshowdown.com/sprites/types/Flying.png` |
| 4 | **Veneno** | `poison` | `https://play.pokemonshowdown.com/sprites/types/Poison.png` |
| 5 | **Tierra** | `ground` | `https://play.pokemonshowdown.com/sprites/types/Ground.png` |
| 6 | **Roca** | `rock` | `https://play.pokemonshowdown.com/sprites/types/Rock.png` |
| 7 | **Bicho** | `bug` | `https://play.pokemonshowdown.com/sprites/types/Bug.png` |
| 8 | **Fantasma** | `ghost` | `https://play.pokemonshowdown.com/sprites/types/Ghost.png` |
| 9 | **Acero** | `steel` | `https://play.pokemonshowdown.com/sprites/types/Steel.png` |
| 10 | **Fuego** | `fire` | `https://play.pokemonshowdown.com/sprites/types/Fire.png` |
| 11 | **Agua** | `water` | `https://play.pokemonshowdown.com/sprites/types/Water.png` |
| 12 | **Planta** | `grass` | `https://play.pokemonshowdown.com/sprites/types/Grass.png` |
| 13 | **Eléctrico** | `electric` | `https://play.pokemonshowdown.com/sprites/types/Electric.png` |
| 14 | **Psíquico** | `psychic` | `https://play.pokemonshowdown.com/sprites/types/Psychic.png` |
| 15 | **Hielo** | `ice` | `https://play.pokemonshowdown.com/sprites/types/Ice.png` |
| 16 | **Dragón** | `dragon` | `https://play.pokemonshowdown.com/sprites/types/Dragon.png` |
| 17 | **Siniestro** | `dark` | `https://play.pokemonshowdown.com/sprites/types/Dark.png` |
| 18 | **Hada** | `fairy` | `https://play.pokemonshowdown.com/sprites/types/Fairy.png` |

---

### 8.3 Objetos Comunes de la Poké Tienda

| Nombre en Español (Oficial) | Nombre en Inglés (PokeAPI Slug) | Precio de Compra (₽) | Precio de Venta (₽) | Efecto Matemático en Juego |
|:---|:---|:---:|:---:|:---|
| **Poké Ball** | `poke-ball` | 200 ₽ | 100 ₽ | Multiplicador de captura $1,0\times$ (1 Honor Ball gratis por cada 10) |
| **Super Ball** | `great-ball` | 600 ₽ | 300 ₽ | Multiplicador de captura $1,5\times$ |
| **Ultra Ball** | `ultra-ball` | 1.200 ₽ | 600 ₽ | Multiplicador de captura $2,0\times$ |
| **Poción** | `potion` | 200 ₽ | 100 ₽ | Suma $+20$ PS de vitalidad |
| **Superpoción** | `super-potion` | 700 ₽ | 350 ₽ | Suma $+60$ PS de vitalidad |
| **Hiperpoción** | `hyper-potion` | 1.500 ₽ | 750 ₽ | Suma $+120$ PS de vitalidad |
| **Poción Máxima** | `max-potion` | 2.500 ₽ | 1.250 ₽ | Restaura el $100\%$ de los PS máximos |
| **Restaurar Todo** | `full-restore` | 3.000 ₽ | 1.500 ₽ | Restaura el $100\%$ de los PS y cura estados |
| **Revivir** | `revive` | 1.500 ₽ | 750 ₽ | Recupera del debilitamiento con el $50\%$ de los PS máximos |
| **Antídoto** | `antidote` | 100 ₽ | 50 ₽ | Elimina el estado de envenenamiento |
| **Cura Total** | `full-heal` | 600 ₽ | 300 ₽ | Elimina cualquier problema de estado |
| **Repelente** | `repel` | 400 ₽ | 200 ₽ | Protege durante 100 pasos ($4,0$ ₽/paso) |
| **Superrepelente** | `super-repel` | 500 ₽ | 250 ₽ | Protege durante 200 pasos (**$2,5$ ₽/paso; opción más económica**) |
| **Máximo Repelente**| `max-repel` | 700 ₽ | 350 ₽ | Protege durante 250 pasos ($2,8$ ₽/paso) |

---

### 8.4 Términos de Combate y Mecánicas

| Término en Español | Término en Inglés | Concepto Matemático LOMLOE |
|:---|:---|:---|
| **Nivel** | *Level* ($L$) | Variable discreta acotada $L \in [1, 100]$ |
| **Daño** | *Damage* ($D$) | Cantidad sustraída en operaciones aritméticas |
| **Súper eficaz** | *Super effective* | Multiplicador $\times 2$ o $\times 4$ (dobles y cuádruples) |
| **Poco eficaz** | *Not very effective* | Multiplicador $\times 0,5$ o $\times 0,25$ (mitades y cuartas partes) |
| **Sin efecto / Inmune** | *No effect / Immune* | Multiplicador $\times 0$ (elemento absorbente de la multiplicación) |
| **STAB (Bonificación por Tipo)** | *Same-Type Attack Bonus* | Multiplicador $\times 1,5$ (aumento del $50\%$ o fracción $\frac{3}{2}$) |
| **Golpe Crítico** | *Critical Hit* | Multiplicador $\times 1,5$ (Gen 6+) |
| **Ratio de Captura** | *Catch Rate* ($a$) | Probabilidad, razones, fracciones irreducibles y porcentajes |
| **Monedas / Pokécuartos** | *Poké Dollars* (₽) | Sistema monetario, cálculo de vueltas y presupuestos |
| **Ciclo de Huevo** | *Egg Cycle* | Bloque de $256$ pasos por ciclo para eclosionar |
| **Evolución** | *Evolution* | Discontinuidad y salto discreto de estadísticas ($\Delta \text{PS}$) |

---

### 8.5 Curvas de Experiencia (*Growth Rates*)

| Denominación en Español | Identificador PokeAPI | Fórmula Matemática | EXP Acumulada a Nivel 100 |
|:---|:---|:---|:---:|
| **Rápido** | `fast` | $\text{EXP}(n) = \lfloor \frac{4 n^3}{5} \rfloor$ | $800.000$ |
| **Medio Rápido** (Normal) | `medium` | $\text{EXP}(n) = n^3$ | $1.000.000$ |
| **Medio Lento** (Parabólico) | `medium-slow` | $\text{EXP}(n) = \lfloor \frac{6 n^3}{5} - 15 n^2 + 100 n - 140 \rfloor$ | $1.059.860$ |
| **Lento** | `slow` | $\text{EXP}(n) = \lfloor \frac{5 n^3}{4} \rfloor$ | $1.250.000$ |
| **Errático** | `erratic` | Función polinómica a trozos (*piecewise*) | $600.000$ |
| **Fluctuante** | `fluctuating` | Función polinómica a trozos (*piecewise*) | $1.640.000$ |

---

## 9. Marco Legal, Propiedad Intelectual y Uso Legítimo Educativo

### 9.1 Titularidad de Derechos
Pokémon, los nombres de los personajes y criaturas, las marcas comerciales asociadas, las ilustraciones oficiales y los sprites son propiedad intelectual exclusiva y derechos reservados de **Nintendo Co., Ltd.**, **Creatures Inc.** y **GAME FREAK Inc.**

Este proyecto curricular es una **iniciativa educativa, abierta y sin ánimo de lucro** destinada de forma exclusiva al apoyo didáctico del profesorado y al aprendizaje del alumnado de Educación Primaria.

---

### 9.2 Marco Normativo Español y Europeo (Ilustración de la Enseñanza)
La integración de activos gráficos y referencias en este proyecto se ampara de forma rigurosa en el **Real Decreto Legislativo 1/1996, de 12 de abril**, por el que se aprueba el texto refundido de la **Ley de Propiedad Intelectual de España**, y sus posteriores modificaciones transpositivas de directivas europeas:

- **Artículo 32.2 (Ilustración de la enseñanza):**
  > *"Es lícita la utilización de pequeños fragmentos de obras o de obras aisladas de carácter plástico o fotográfico figurativo [...] cuando se realice para el profesorado de la educación reglada para ilustrar sus actividades docentes, en la medida justificada por la finalidad no comercial perseguida, y siempre que se trate de obras ya divulgadas y, salvo en los casos en que resulte imposible, se incluyan el nombre del autor y la fuente."*

- **Garantías de Cumplimiento en este Proyecto:**
  1. **Finalidad estrictamente no comercial:** El material se distribuye de forma abierta y totalmente gratuita.
  2. **Proporcionalidad y fragmentación:** Únicamente se referencian miniaturas (*sprites* y avatares de baja resolución) e ilustraciones aisladas con el fin exclusivo de motivar y facilitar la comprensión visual de los problemas matemáticos.
  3. **No sustitución del mercado original:** En ningún caso este material sustituye ni compite con los videojuegos, productos comerciales o servicios ofrecidos por The Pokémon Company.

---

### 9.3 Doctrina de Uso Legítimo Internacional (*Fair Use*, 17 U.S.C. § 107)
En el ámbito internacional, el uso de estos activos cumple plenamente con los cuatro factores de la doctrina del *Fair Use*:
1. **Propósito y Carácter del Uso:** Transformador, educativo y pedagógico, sin ningún fin lucrativo.
2. **Naturaleza de la Obra Protegida:** Ficción fantástica empleada como metáfora contextual para el aprendizaje de las ciencias exactas.
3. **Cantidad y Sustancialidad Empleada:** Inclusión mínima de activos visuales secundarios e hipervínculos; no se distribuye código ejecutable, emuladores ni ROMs de los juegos.
4. **Efecto sobre el Mercado Potencial:** Nulo impacto comercial adverso sobre las ventas de la obra original.

---

### 9.4 Texto Preceptivo de Atribución Educativa

Todo documento de trabajo, examen o ficha didáctica que incorpore activos referenciados en esta guía debe incluir al pie de página el siguiente aviso formal:

> **Aviso Legal y de Atribución Educativa:**  
> *Pokémon y los nombres de las criaturas y personajes son marcas comerciales y derechos reservados de Nintendo, Creatures Inc. y Game Freak Inc. Este material didáctico ha sido desarrollado exclusivamente con fines educativos y de divulgación matemática escolar sin ánimo de lucro, al amparo del artículo 32.2 del Real Decreto Legislativo 1/1996 de la Ley de Propiedad Intelectual de España y la doctrina internacional de Uso Legítimo (Fair Use, 17 U.S.C. § 107). Este proyecto no está respaldado, afiliado ni patrocinado por Nintendo ni The Pokémon Company.*
