# Proyecto Curricular de Matemáticas Pokémon — Educación Primaria (LOMLOE)

![LOMLOE](https://img.shields.io/badge/Curr%C3%ADculo-LOMLOE%20RD%20157%2F2022-blue)
![Cursos](https://img.shields.io/badge/Cursos-1%C2%BA%20a%206%C2%BA%20Primaria-brightgreen)
![Problemas](https://img.shields.io/badge/Problemas-720%20(120%2Fcurso)-orange)
![Solucionario](https://img.shields.io/badge/Solucionario-100%25%20Paso%20a%20Paso-yellow)
![Tests](https://img.shields.io/badge/Pytest-172%20Tests%20Passing-success)
![Diagramas](https://img.shields.io/badge/Diagramas-SVG%20Inline%20A4-purple)
![Integridad](https://img.shields.io/badge/Mec%C3%A1nicas%20Pok%C3%A9mon-Gen%20III--IX%20Can%C3%B3nicas-red)

---

## 1. Visión General del Proyecto y Alineación Curricular LOMLOE

El **Proyecto Curricular de Matemáticas Pokémon** es una propuesta didáctica integral, estructurada y pedagógicamente rigurosa diseñada para toda la Educación Primaria española (**desde 1º hasta 6º de Primaria**, cubriendo los tres ciclos: Primer Ciclo 1º–2º, Segundo Ciclo 3º–4º y Tercer Ciclo 5º–6º). El proyecto toma como base legal y organizativa el **Real Decreto 157/2022, de 1 de marzo**, por el que se establecen la ordenación y las enseñanzas mínimas de la Educación Primaria en el marco de la **LOMLOE** (*Ley Orgánica 3/2020*).

A través de la gamificación contextualizada en el universo y las mecánicas competitivas de la franquicia Pokémon (fórmulas de daño, puntos de salud, curvas de experiencia, multiplicadores de tipos y economía del juego), se movilizan de forma significativa las **ocho Competencias Específicas (CE1–CE8)** del área de Matemáticas y los **cinco Sentidos Matemáticos** estipulados por el currículo oficial:

1. **Sentido Numérico**: Comprensión del sistema de numeración decimal, valor posicional, conteo, estimación, operaciones básicas con y sin llevada, cálculo mental, potencias, fracciones, números decimales, porcentajes y números enteros.
2. **Sentido de la Medida**: Estimación y cálculo de magnitudes físicas (longitud, masa, capacidad, superficie y volumen), tiempo (horas en punto/media/cuarto, minutos, segundos, calendarios) y el sistema monetario (euros, céntimos y Pokédólares aplicados a transacciones).
3. **Sentido Espacial**: Reconocimiento de figuras geométricas planas (polígonos, círculos) y cuerpos tridimensionales (poliedros, prismas, pirámides, cuerpos de revolución), coordenadas cartesianas, distancias, simetrías, ángulos, perímetros y áreas.
4. **Sentido Algebraico**: Búsqueda de patrones, regularidades, relaciones funcionales, proporcionalidad directa e inversa, pensamiento computacional paso a paso y modelización mediante fórmulas canónicas (como el cálculo de PS máximos o la ganancia de EXP).
5. **Sentido Estocástico**: Interpretación y elaboración de tablas de recuento, pictogramas y gráficos estadísticos (barras, líneas, sectores), medidas de tendencia central (media, moda) y cálculo cualitativo o formal de probabilidades (sucesos seguros, posibles o imposibles; regla de Laplace en capturas y golpes críticos).

---

## 2. Resumen de Entregables del Repositorio

El repositorio está organizado como un sistema modular que combina bancos de problemas por curso, recursos imprimibles con diagramas vectoriales SVG, tablas técnicas de consulta para docentes y alumnado, una guía de recursos multimedia y una suite de pruebas automatizadas en Python.

| Entregable | Archivo | Descripción y Alcance |
|---|---|---|
| **1º de Primaria** | [`problemas_1_primaria.md`](problemas_1_primaria.md) | **120 problemas y 120 soluciones (100 base + 20 Retos Especiales)**: Dominio numérico 0–99. Sumas y restas sin llevada, formas 2D, horas en punto y media, monedas/billetes hasta 50 € y EXP inicial. |
| **2º de Primaria** | [`problemas_2_primaria.md`](problemas_2_primaria.md) | **120 problemas y 120 soluciones (100 base + 20 Retos Especiales)**: Dominio numérico 0–999. Sumas/restas con y sin llevada, figuras 2D, orientación, tiempo y dinero. |
| **3º de Primaria** | [`problemas_3_primaria.md`](problemas_3_primaria.md) | **120 problemas y 120 soluciones (100 base + 20 Retos Especiales)**: Dominio numérico 0–9.999. Tablas de multiplicar (1–10), división exacta e inexacta, unidades métricas y gráficos de barras. |
| **4º de Primaria** | [`problemas_4_primaria.md`](problemas_4_primaria.md) | **130 problemas y 130 soluciones (100 base + 30 Retos Especiales y Nivel TIMSS 2023)**: Dominio numérico hasta 99.999 y 6 cifras. Multiplicación multidígito, división con resto, fracciones, decimales, perímetros, ángulos, balanzas, desarrollos planos y escalas gráficas. |
| **5º de Primaria** | [`problemas_5_primaria.md`](problemas_5_primaria.md) | **120 problemas y 120 soluciones (100 base + 20 Retos Especiales)**: Dominio > 100.000. Operaciones con fracciones y decimales, porcentajes, áreas de polígonos y coordenadas en el primer cuadrante. |
| **6º de Primaria** | [`problemas_6_primaria.md`](problemas_6_primaria.md) | **120 problemas y 120 soluciones (100 base + 20 Retos Especiales)**: Fracciones complejas, porcentajes/proporcionalidad, números enteros, plano cartesiano de 4 cuadrantes, volúmenes y probabilidad. |
| **Tabla de Tipos** | [`referencia_tabla_tipos.md`](referencia_tabla_tipos.md) | **Matriz 18×18 completa**: 324 interacciones elementales, 11 multiplicadores canónicos (0x a 6x con STAB), tipos duales e Inverted Battles. |
| **Fórmulas de PS** | [`referencia_ps_evoluciones.md`](referencia_ps_evoluciones.md) | **Mecánicas de Puntos de Salud**: Fórmula canónica Gen III-IX, delta constante de 94 PS a nivel 100, anomalía de Shedinja, 18 líneas evolutivas y Eevee. |
| **Guía de Recursos** | [`guia_recursos_activos.md`](guia_recursos_activos.md) | **Fuentes y APIs oficiales**: PokeAPI REST v2, repositorios CDN de sprites y artwork oficial, Pokémon Showdown, base de datos Veekun CSV y guía legal. |
| **Cuadernillos HTML** | [`html/index.html`](html/index.html) | **Versión web e imprimible A4**: Cuadernillos anuales HTML de 1º a 6º Primaria (720 ejercicios) con portada, pasaporte de 8 medallas, índice, separadores de capítulo, diagramas SVG, filtros interactivos, andamiaje NEAE y rúbrica docente. |
| **Cuadernillos PDF** | [`html/pdf/`](html/pdf/) | **18 libros listos para imprimir y encuadernar**: Por cada curso (1º a 6º) se incluye Cuadernillo A4 Alumno, Folleto A5 impuesto 2-up en A4 apaisado (para doblar por la mitad) y Apéndice del Docente (sin páginas del alumno). |
| **Generador HTML** | [`build_html.py`](build_html.py) | **Script de compilación**: Convierte todos los Markdown en cuadernillos imprimibles en `html/`, integra diagramas SVG, pistas Rotom Dex, filtros docentes, modo A5, márgenes de encuadernación y la Ficha del Profesor Oak. |
| **Generador PDF** | [`build_pdfs.py`](build_pdfs.py) | **Exportador e impositor A4/A5**: Genera los 18 PDF (`cuadernillo_X_primaria_alumno.pdf`, `cuadernillo_X_primaria_alumno_a5_folleto.pdf` y `apendice_X_primaria_docente.pdf`) mediante Chrome/Edge y `pypdf`. |
| **Diagramas SVG** | [`svg_diagrams.py`](svg_diagrams.py) | **Motor gráfico vectorial**: Genera ilustraciones SVG en línea (`relojes analógicos`, `polígonos/3D/cuadrículas`, `gráficos estadísticos/urnas` y `rectas numéricas/termómetros`). |
| **Descarga de Activos** | [`download_assets.py`](download_assets.py) | **Caché offline de PokeAPI**: Descarga nombres/IDs en [`data/pokemon_species.json`](data/pokemon_species.json) y artworks PNG oficiales en `html/assets/images/`. |
| **Generador 1º Prim.** | [`generate_problemas_1.py`](generate_problemas_1.py) | **Script generador**: Script en Python utilizado para construir el banco de problemas de 1º de Primaria (`problemas_1_primaria.md`). |
| **Generador 2º Prim.** | [`generate_problemas_2.py`](generate_problemas_2.py) | **Script generador**: Script en Python utilizado para construir el banco de problemas de 2º de Primaria (`problemas_2_primaria.md`). |
| **Batería de Tests** | [`tests/`](tests/) | **Suite automatizada de 172 pruebas en Pytest**: 162 pruebas transversales (Tiers 1–5 para 2º–6º y referencia) más 10 pruebas en [`tests/test_grade1_primaria.py`](tests/test_grade1_primaria.py) para 1º Primaria. |

---

## 3. Arquitectura y Esquema de los Bancos de Problemas

Cada archivo de curso (`problemas_1_primaria.md` a `problemas_6_primaria.md`) reúne **120 ejercicios y 120 soluciones** organizados en una arquitectura estandarizada:

### 3.1 Estructura Interna del Documento
1. **Encabezado y Metadatos**: Identificación del curso, marco normativo LOMLOE y resumen de bloques competenciales.
2. **Parte 1: Enunciados de los Problemas (1 al 100)** + **Parte 1B: Retos Especiales (101 al 120)**: Diseñada para el alumnado. Cada ejercicio incluye:
   - `### Problema N: <Título>` (o `### Reto N: <Título>` para 101–120)
   - `- **Subcategoría**`: Una de las 7 subcategorías pedagógicas del curso (o categoría de Reto Especial).
   - `- **Sentido LOMLOE**`: Sentido matemático curricular principal al que responde el ejercicio.
   - `- **Contenido Específico**` *(presente en 5º y 6º)*: Concepto curricular detallado (reservado exclusivamente para el docente en la versión HTML).
   - `- **Contexto Pokémon**`: Ambientación narrativa inmersiva (entrenadores, rutas, gimnasios, combates, crianza).
   - `**Pregunta**`: Formulación clara de una o varias líneas, con datos cuantitativos explícitos y sin ambigüedades.
3. **Parte 2: Solucionario y Respuestas Razonadas (1 al 120)**: Diseñada para el docente o la autoevaluación guiada. Cada solución sigue un esquema de tres fases obligatorias:
   - `### Solución Problema N` / `### Solución al Reto N`
   - `- **Datos identificados**`: Extracción ordenada de los datos clave del enunciado.
   - `- **Planteamiento y Operaciones**`: Justificación didáctica, fórmula aplicada y desarrollo paso a paso del cálculo.
   - `- **Respuesta Final**`: Enunciado unívoco con la magnitud numérica y unidades físicas o del juego remarcadas en **negrita** (ej. **$1.850 \text{ Pokédólares}$**, **$45 \text{ PS}$**, **$\frac{3}{8}$**).

### 3.2 Distribución de las 7 Subcategorías Base + Retos Especiales (120 Ejercicios / Curso)
Para garantizar una cobertura pedagógica equilibrada y progresiva en cada curso de 1º a 6º de Primaria:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│            DISTRIBUCIÓN DE EJERCICIOS POR CURSO (120 / CURSO · 720 TOTAL)    │
├──────┬───────────────────────────────────────────────┬───────────────────────┤
│ Bloq │ Subcategoría Curricular                       │ Volumen / Curso       │
├──────┼───────────────────────────────────────────────┼───────────────────────┤
│  1.  │ Numeración, Descomposición y Valor Posicional │  15 problemas (1–15)  │
│  2.  │ Operaciones Aritméticas y Cálculo Mental      │  20 problemas (16–35) │
│  3.  │ Magnitudes, Medida, Tiempo y Dinero           │  15 problemas (36–50) │
│  4.  │ Geometría, Formas, Perímetros, Áreas y Esp.   │  15 problemas (51–65) │
│  5.  │ Patrones, Regularidades y Pens. Computacional │  10 problemas (66–75) │
│  6.  │ Tratamiento de Datos, Gráficos y Probabilidad │  10 problemas (76–85) │
│  7.  │ Mecánicas de Combate, Nivel y Experiencia     │  15 problemas (86–100)│
│  1B. │ Retos Especiales (Lógica, Criptografía, Liga) │  20 retos (101–120)   │
└──────┴───────────────────────────────────────────────┴───────────────────────┘
```

---

## 4. Progresión Pedagógica del Cálculo de Experiencia (EXP)

Uno de los requerimientos nucleares del proyecto es la inclusión de al menos 15 problemas dedicados por curso (más retos integradores adicionales en la Parte 1B) orientados al cálculo de la experiencia necesaria para subir de nivel y los PS en combate. La complejidad matemática evoluciona en estricta sincronía con el currículo LOMLOE:

```
  1º Primaria (Conteo, Decenas y Sumas/Restas sin Llevada)
  ├── Suma y resta simple de EXP y PS (Pociones +20 PS, Bayas Aranja +10 PS).
  ├── Comparación de niveles y barras hasta 99.
  └── Dominio numérico natural estrictamente acotado a [0, 99].
        │
        ▼
  2º Primaria (Lineal & Sumativo con/sin Llevada)
  ├── Sumas y restas lineales: EXP requerida = Base + Incremento fijo.
  ├── Caramelos Raros (+1 nivel directo) y barras de EXP simples.
  └── Dominio numérico natural acotado a [0, 999].
        │
        ▼
  3º Primaria (Multiplicativo & Reparto Exacto)
  ├── Reparto equitativo entre el equipo: División exacta sin resto (EXP / N).
  ├── Acumulación de experiencia por derrotas consecutivas (N victorias × EXP).
  └── Dominio numérico natural acotado a [0, 9.999].
        │
        ▼
  4º Primaria (Fracciones de Barra & División con Resto)
  ├── Fracciones de la barra de nivel (ej. 3/4 de 800 EXP).
  ├── Estimación de combates necesarios: Cociente y resto de la división entera.
  └── Multiplicadores de combate introductorios (Combate contra Entrenador × 1,5).
        │
        ▼
  5º Primaria (Fórmula Canónica de Derrota & Porcentajes)
  ├── Fórmula canónica simplificada de combate: EXP = floor((BaseEXP × Nivel) / 7).
  ├── Modificadores acumulativos: Huevo Suerte (+50%), Pokémon intercambiado (+50%).
  └── Porcentajes de avance de nivel y cálculo de porcentajes restantes.
        │
        ▼
  6º Primaria (Curvas Cúbicas L³ & Repartir Experiencia Moderno)
  ├── Modelos de crecimiento cúbico de nivel: Rápido (0,8·L³), Medio (L³), Lento (1,25·L³).
  ├── Repartir Experiencia moderno (Gen VI-IX): Activo 100% + 5 reservas al 50% = 350% total.
  └── Estadísticas compuestas, potencias cúbicas y sistemas de niveles límite (Nivel 100).
```

---

## 5. Índice y Guía de Documentos de Referencia Técnica

Los documentos de referencia proporcionan el marco formal y las tablas de consulta indispensables para que tanto docentes como alumnos contrasten los datos de los enunciados.

### 5.1 Matriz de Efectividad de Tipos (`referencia_tabla_tipos.md`)
- **Matriz 18×18 completa**: Cubre los 18 tipos elementales oficiales (*Acero, Agua, Bicho, Dragón, Eléctrico, Fantasma, Fuego, Hada, Hielo, Lucha, Normal, Planta, Psíquico, Roca, Siniestro, Tierra, Veneno, Volador*) totalizando 324 combinaciones individuales.
- **Tabla de Multiplicadores Canónicos**:
  * Inmunidad: **$0\times$**
  * Doble resistencia: **$0,25\times$**
  * Resistencia combinada con STAB: **$0,375\times$** y **$0,75\times$**
  * Resistencia simple: **$0,5\times$**
  * Daño neutro: **$1\times$**
  * Bonificación por mismo tipo (STAB): **$1,5\times$**
  * Súper eficaz simple: **$2\times$**
  * Súper eficaz con STAB: **$3\times$**
  * Cuádruple debilidad (doble tipo débil): **$4\times$**
  * Cuádruple debilidad con STAB: **$6\times$**
- **Álgebra de Tipos Duales**: Demostración del producto cartesiano $M_{\text{total}} = M(T_{\text{atk}} \to T_{\text{def1}}) \times M(T_{\text{atk}} \to T_{\text{def2}})$ verificado sobre las 2.754 combinaciones posibles.
- **Combates Inversos (*Inverse Battles*)**: Formalización de la mecánica donde las debilidades se tornan resistencias y las resistencias/inmunidades se tornan debilidades ($2\times$).

### 5.2 Fórmulas de PS y Progresión Evolutiva (`referencia_ps_evoluciones.md`)
- **Fórmula Canónica de Puntos de Salud (Generaciones III a IX)**:
  $$\text{PS}_{\max} = \left\lfloor \frac{(2 \cdot \text{Base} + \text{IV} + \lfloor \frac{\text{EV}}{4} \rfloor) \cdot \text{Nivel}}{100} \right\rfloor + \text{Nivel} + 10$$
  donde $\text{IV} \in [0, 31]$ y $\text{EV} \in [0, 252]$.
- **Invariante del Rango Genético**: Demostración analítica de que a nivel 100, la diferencia absoluta entre el PS máximo absoluto ($\text{IV}=31, \text{EV}=252$) y el mínimo ($\text{IV}=0, \text{EV}=0$) es **estrictamente igual a 94 PS** para cualquier valor de estadística base:
  $$\Delta \text{PS}(100) = (2 \cdot \text{Base} + 204) - (2 \cdot \text{Base} + 110) = 94\text{ PS}$$
- **La Anomalía de Shedinja**: Documentación matemática del invariante $\text{PS}_{\text{Shedinja}} \equiv 1$ en todos los niveles, justificado por su habilidad *Superguarda*.
- **Familias Evolutivas Documentadas**: 18 líneas representativas (Kanto a Paldea), incluyendo la matriz de ramificación de **Eevee** (8 evoluciones desde Base 55).
- **Tabla de Consulta Rápida (Sección 7)**: 85 valores exactos evaluados a niveles 10, 25, 50, 75 y 100 para verificación directa en el aula.

### 5.3 Guía de Fuentes de Activos y Multimedia (`guia_recursos_activos.md`)
- **Endpoints REST de PokeAPI v2**:
  * Datos generales: `https://pokeapi.co/api/v2/pokemon/{id_o_nombre}/`
  * Especie y cadena evolutiva: `https://pokeapi.co/api/v2/pokemon-species/{id_o_nombre}/`
  * Relaciones de tipos: `https://pokeapi.co/api/v2/type/{id_o_nombre}/`
  * Curvas de crecimiento: `https://pokeapi.co/api/v2/growth-rate/{id_o_nombre}/`
- **Repositorios CDN de Sprites y Arte Oficial**:
  * Artwork oficial en alta definición: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png`
  * Sprites animados Gen 5 (Pokémon Showdown): `https://play.pokemonshowdown.com/sprites/gen5/{slug}.png`
  * Iconos oficiales de tipos: `https://play.pokemonshowdown.com/sprites/types/{Tipo}.png`
- **Base de Datos Relacional Veekun CSV**: Tablas de referencia directa para minería masiva de datos en formato abierto.
- **Seguridad y Cumplimiento**: 100% de enlaces bajo protocolo seguro HTTPS y estricto encuadre en el derecho de cita didáctica y uso legítimo educativo.

---

## 6. Cuadernillos HTML, Herramientas Docentes y Batería de Pruebas (Pytest)

### 6.1 Uso Rápido y Cuadernillos Anuales Imprimibles (`html/index.html` y `html/pdf/`)
No necesitas instalar nada para empezar a usar los cuadernillos:
1. **Descarga directa en PDF (`html/pdf/`)**: En [`html/index.html`](html/index.html) o en [`html/pdf/`](html/pdf/) dispones de **18 documentos listos para imprimir y encuadernar** (tres por curso, de 1º a 6º de Primaria):
   - **Cuadernillo A4 Alumno (`cuadernillo_X_primaria_alumno.pdf`)**: Portada escolar, Pasaporte de 8 Medallas de Gimnasio, índice de progreso anual, 8 separadores de capítulo, márgenes alternos de encuadernación (`18 mm` en el lomo interior), numeración de páginas y amplia cuadrícula libre de respuesta (sin solucionario).
   - **Folleto A5 impuesto en A4 (`cuadernillo_X_primaria_alumno_a5_folleto.pdf`)**: Imposición automática 2-up en hojas A4 apaisadas; imprímelo en **A4 a doble cara volteando por el borde corto** y dobla las hojas por la mitad para encuadernar un cuadernillo en formato A5.
   - **Apéndice del Docente (`apendice_X_primaria_docente.pdf`)**: Contiene exclusivamente la *Ficha del Profesor Oak* (mapeo CE1–CE8 y rúbrica LOMLOE) y el solucionario completo paso a paso, **sin repetir las páginas del alumno**.
2. **Cuadernillos interactivos HTML (`html/index.html`)**: Abre [`html/index.html`](html/index.html) en cualquier navegador web y selecciona el curso (**1º a 6º de Primaria**, 720 ejercicios en total) o el documento de referencia que quieras consultar.
3. Aprovecha las herramientas integradas en la barra superior (ocultas automáticamente al imprimir con `Ctrl+P`):
   - **Impresión directa de cuadernillo anual o ficha**: Botones **«🖨️ Imprimir Cuadernillo Alumno»** (activa el modo sin soluciones y restablece los 120 ejercicios) y **«🖨️ Imprimir Actual / Docente»**, además de enlaces directos de descarga PDF y soporte de parámetro `?mode=alumno`.
   - **Maquetación de libro anual A4**: Cada curso incluye portada imprimible (`.workbook-cover`), índice con registro de progreso (`.workbook-toc`) y separadores por bloque (`.chapter-banner`, *Gimnasios 1–7 + Liga Pokémon*) con saltos de página automáticos por capítulo; al filtrar una ficha suelta, la portada y el índice se ocultan automáticamente para imprimir hojas de sesión limpias.
   - **Filtro interactivo de fichas imprimibles**: Filtra en tiempo real por **Subcategoría** (`1..7` o `Retos Especiales 101–120`), **Sentido LOMLOE**, rango **Desde–Hasta** (`1..120`), o utiliza el acceso rápido **«Ficha de sesión (5 ej.)»** y **«Restablecer»**. Oculta y muestra de forma sincronizada tanto los enunciados como sus soluciones asociadas para imprimir sesiones de una página en formato A4.
   - **Diagramas matemáticos SVG en línea (`svg_diagrams.py`)**: Ilustraciones vectoriales impresas a color con límite seguro para A4 (`max-height: 150px`) generadas según el enunciado: relojes analógicos, figuras geométricas 2D/3D y planos cartesianos, gráficos estadísticos/urnas de probabilidad y rectas numéricas o escalas termométricas.
   - **Andamiaje para Atención a la Diversidad (NEAE)**:
     * **Cuadrícula estructurada en 3 zonas** (`Datos` | `Operación / Planteamiento` | `Respuesta y unidades`) con mayor altura (`grade-early`: `115px` en pantalla / `95px` al imprimir) en los cuadernillos de **1º a 3º de Primaria** para facilitar la escritura infantil.
     * **Pistas de Rotom Dex (`💡 Pista de Rotom Dex`)**: Orientaciones heurísticas sin revelar resultados numéricos, con botón **«Ocultar/Mostrar pistas»** (`toggleHints()`).
   - **Tarjetas de 5º y 6º sin spoilers ni cortes**: El metadato `- **Contenido Específico**:` se extrae de la tarjeta del alumno y se traslada a las tarjetas del solucionario y a la *Ficha del Profesor Oak*; los bloques multi-línea de `**Pregunta**:` (incluidos apartados `a), b), c)` o tablas) y `**Contexto Pokémon**:` se renderizan íntegramente, y los encabezados de sección del solucionario (`### Soluciones — ...`) se muestran fuera de las tarjetas.
   - **Ficha del Profesor Oak con Mapeo CE1–CE8 y Rúbrica LOMLOE**: Incluye la tabla específica por ciclo (*Primer Ciclo 1º–2º*, *Segundo Ciclo 3º–4º*, *Tercer Ciclo 5º–6º*) vinculada a las **8 Competencias Específicas (CE1–CE8)** y **Criterios de Evaluación (RD 157/2022)**, junto con una **Rúbrica de Evaluación Competencial de 4 niveles** (*1. En inicio*, *2. En desarrollo*, *3. Adquirido*, *4. Excelente*) en cuatro dimensiones (*Comprensión y extracción de datos*, *Estrategia y modelización*, *Cálculo y precisión*, *Comunicación y unidades*).

### 6.2 Regeneración de Activos, HTML y PDFs
Si modificas algún archivo Markdown y quieres regenerar la versión HTML, actualizar la caché de imágenes o volver a exportar los 12 PDF:
- **Requisitos**: Python 3.10+, la librería `markdown` (`pip install markdown`) y Google Chrome o Microsoft Edge instalado para la exportación PDF.
```powershell
# (Opcional) Descargar/actualizar artworks oficiales y datos de especies en local
python download_assets.py

# Compilar todos los Markdown a HTML (con portadas, índices y diagramas SVG) en html/
python build_html.py

# Exportar los 12 cuadernillos anuales A4 en PDF (Alumno y Docente) en html/pdf/
python build_pdfs.py
```

### 6.3 Requisitos y Ejecución de Pruebas Automatizadas
El proyecto cuenta con un arnés de pruebas automatizadas independiente en Python (`pytest`) que valida de forma continua la integridad matemática, la estructura de los archivos Markdown y el cumplimiento curricular.

- Python 3.10 o superior.
- Paquete `pytest` (versión 7.0 o superior).

Instalación rápida de dependencias:
```powershell
pip install pytest
```

### 6.4 Comandos de Ejecución de Pruebas

Para ejecutar la suite completa desde el directorio raíz del proyecto:
```powershell
# Ejecución completa con reporte detallado paso a paso
python -m pytest tests/ -v

# Ejecución en modo resumen rápido
python -m pytest tests/ -q
```

Para ejecutar de manera aislada la suite de 1º de Primaria o la suite adversarial (Tier 5):
```powershell
python -m pytest tests/test_grade1_primaria.py -v
python -m pytest tests/test_tier5_adversarial.py -v
```

### 6.5 Arquitectura de Verificación en Pytest

La suite completa suma **172 pruebas automatizadas** en `pytest`: **5 Tiers transversales** (162 pruebas sobre 2º–6º y tablas de referencia) más **10 pruebas dedicadas a 1º de Primaria** (`test_grade1_primaria.py`):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA DEL TEST HARNESS (172 TESTS)                 │
├──────────┬──────────────────────────────────┬───────┬───────────────────────┤
│ Módulo   │ Archivo                          │ Tests │ Objetivo Principal    │
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ Tier 1   │ test_tier1_problem_counts.py     │   21  │ Existencia (2º–6º),   │
│          │                                  │       │ conteo (100/curso) y  │
│          │                                  │       │ numeración secuencial.│
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ Tier 2   │ test_tier2_answer_keys.py        │   21  │ Biyección 1-a-1, blo- │
│          │                                  │       │ ques y negritas.      │
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ Tier 3   │ test_tier3_lomloe_and_exp.py     │   26  │ Sentidos LOMLOE, >=15 │
│          │                                  │       │ EXP/curso y progre-   │
│          │                                  │       │ sión pedagógica.      │
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ Tier 4   │ test_tier4_reference_tables.py   │   13  │ Matriz 18x18, fórmu-  │
│          │                                  │       │ las PS y URLs.        │
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ Tier 5   │ test_tier5_adversarial.py        │   81  │ Límites RD 157/2022,  │
│          │                                  │       │ 2.754 duales, 85 PS,  │
│          │                                  │       │ LF/CRLF y 100% HTTPS. │
├──────────┼──────────────────────────────────┼───────┼───────────────────────┤
│ 1º Prim. │ test_grade1_primaria.py          │   10  │ 100 + 20 Retos, rango │
│          │                                  │       │ 0–99, 5 sentidos, EXP.│
├──────────┴──────────────────────────────────┴───────┴───────────────────────┤
│ TOTAL AUTOMATED TESTS: 172 PASSED (Exit Code 0)                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Aviso Legal, Atribución y Licencia Educativa

Este proyecto ha sido desarrollado exclusivamente con fines educativos, de divulgación pedagógica e investigación didáctica sin ánimo de lucro, de acuerdo con las disposiciones sobre el derecho de cita y uso legítimo recogidas en la legislación internacional sobre propiedad intelectual (*Fair Use*).

- Las marcas, nombres de criaturas, habilidades, conceptos y elementos del juego Pokémon son propiedad registrada de **Nintendo**, **Creatures Inc.** y **Game Freak Inc.**
- Los textos de los problemas, las explicaciones didácticas, las soluciones paso a paso y la infraestructura de pruebas automatizadas han sido creados de forma original para este repositorio, quedando a disposición de la comunidad educativa bajo licencia de uso abierto para docentes y centros escolares.
