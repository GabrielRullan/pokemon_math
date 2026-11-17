# Proyecto Curricular de Matemáticas Pokémon — Educación Primaria (LOMLOE)

![LOMLOE](https://img.shields.io/badge/Curr%C3%ADculo-LOMLOE%20RD%20157%2F2022-blue)
![Cursos](https://img.shields.io/badge/Cursos-2%C2%BA%20a%206%C2%BA%20Primaria-brightgreen)
![Problemas](https://img.shields.io/badge/Problemas-500%20(100%2Fcurso)-orange)
![Solucionario](https://img.shields.io/badge/Solucionario-100%25%20Paso%20a%20Paso-yellow)
![Tests](https://img.shields.io/badge/Pytest-162%20Tests%20Passing-success)
![Integridad](https://img.shields.io/badge/Mec%C3%A1nicas%20Pok%C3%A9mon-Gen%20III--IX%20Can%C3%B3nicas-red)

---

## 1. Visión General del Proyecto y Alineación Curricular LOMLOE

El **Proyecto Curricular de Matemáticas Pokémon** es una propuesta didáctica integral, estructurada y pedagógicamente rigurosa diseñada para la Educación Primaria española (desde 2º hasta 6º de Primaria). El proyecto toma como base legal y organizativa el **Real Decreto 157/2022, de 1 de marzo**, por el que se establecen la ordenación y las enseñanzas mínimas de la Educación Primaria en el marco de la **LOMLOE** (*Ley Orgánica 3/2020*).

A través de la gamificación contextualizada en el universo y las mecánicas competitivas de la franquicia Pokémon (fórmulas de daño, puntos de vida, curvas de experiencia, multiplicadores de tipos y economía del juego), se movilizan de forma significativa las competencias específicas del área de Matemáticas y los **cinco Sentidos Matemáticos** estipulados por el currículo oficial:

1. **Sentido Numérico**: Comprensión del sistema de numeración decimal, valor posicional, conteo, estimación, operaciones básicas con y sin llevada, cálculo mental, potencias, fracciones, números decimales, porcentajes y números enteros.
2. **Sentido de la Medida**: Estimación y cálculo de magnitudes físicas (longitud, masa, capacidad, superficie y volumen), tiempo (horas, minutos, segundos, calendarios) y el sistema monetario (Pokédólares / monedas aplicadas a transacciones).
3. **Sentido Espacial**: Reconocimiento de figuras geométricas planas (polígonos, círculos) y cuerpos tridimensionales (poliedros, prismas, pirámides, cuerpos de revolución), coordenadas cartesianas, distancias euclidianas y Manhattan, transformaciones, ángulos, perímetros y áreas.
4. **Sentido Algebraico**: Búsqueda de patrones, regularidades, relaciones funcionales, proporcionalidad directa e inversa, igualdades numéricas y modelización mediante fórmulas canónicas (como el cálculo de PS máximos o la ganancia de EXP).
5. **Sentido Estocástico**: Interpretación y elaboración de tablas y gráficos estadísticos (barras, líneas, sectores), medidas de tendencia central (media, moda) y cálculo formal o cualitativo de probabilidades (sucesos seguros, posibles o imposibles; probabilidades fraccionarias de captura y golpes críticos).

---

## 2. Resumen de Entregables del Repositorio

El repositorio está organizado como un sistema modular que combina recursos de aula listos para su impresión o integración digital, tablas técnicas de consulta para docentes y alumnos, una guía de recursos multimedia y una suite de pruebas automatizadas en Python.

| Entregable | Archivo | Descripción y Alcance |
|---|---|---|
| **2º de Primaria** | [`problemas_2_primaria.md`](problemas_2_primaria.md) | **100 problemas y 100 soluciones**: Dominio numérico 0–999. Sumas/restas con y sin llevada, figuras 2D, orientación, tiempo y dinero. |
| **3º de Primaria** | [`problemas_3_primaria.md`](problemas_3_primaria.md) | **100 problemas y 100 soluciones**: Dominio numérico 0–9.999. Tablas de multiplicar (1–10), división exacta e inexacta, unidades métricas y gráficos de barras. |
| **4º de Primaria** | [`problemas_4_primaria.md`](problemas_4_primaria.md) | **100 problemas y 100 soluciones**: Dominio numérico hasta 99.999 y 6 cifras. Multiplicación multidígito, división con resto, fracciones, decimales, perímetros y ángulos. |
| **5º de Primaria** | [`problemas_5_primaria.md`](problemas_5_primaria.md) | **100 problemas y 100 soluciones**: Dominio > 100.000. Operaciones con fracciones y decimales, porcentajes, áreas de polígonos y coordenadas en el primer cuadrante. |
| **6º de Primaria** | [`problemas_6_primaria.md`](problemas_6_primaria.md) | **100 problemas y 100 soluciones**: Fracciones complejas, porcentajes/proporcionalidad, números enteros, plano cartesiano de 4 cuadrantes, volúmenes y probabilidad. |
| **Tabla de Tipos** | [`referencia_tabla_tipos.md`](referencia_tabla_tipos.md) | **Matriz 18×18 completa**: 324 interacciones elementales, 11 multiplicadores canónicos (0x a 6x con STAB), tipos duales e Inverted Battles. |
| **Fórmulas de PS** | [`referencia_ps_evoluciones.md`](referencia_ps_evoluciones.md) | **Mecánicas de Puntos de Salud**: Fórmula canónica Gen III-IX, delta constante de 94 PS a nivel 100, anomalía de Shedinja, 18 líneas evolutivas y Eevee. |
| **Guía de Recursos** | [`guia_recursos_activos.md`](guia_recursos_activos.md) | **Fuentes y APIs oficiales**: PokeAPI REST v2, repositorios CDN de sprites y artwork oficial, Pokémon Showdown, base de datos Veekun CSV y guía legal. |
| **Cuadernillos HTML** | [`html/index.html`](html/index.html) | **Versión web e imprimible**: Cuadernillos HTML con estética de ficha infantil, imágenes locales en `html/assets/images/`, cuadrícula de operaciones y ficha curricular. |
| **Generador HTML** | [`build_html.py`](build_html.py) | **Script de compilación**: Convierte todos los documentos Markdown en cuadernillos HTML listos para imprimir en `html/`. |
| **Descarga de Activos** | [`download_assets.py`](download_assets.py) | **Caché offline de PokeAPI**: Descarga nombres/IDs en [`data/pokemon_species.json`](data/pokemon_species.json) y artworks PNG oficiales en `html/assets/images/`. |
| **Generador 2º Prim.** | [`generate_problemas_2.py`](generate_problemas_2.py) | **Script generador**: Script en Python utilizado para construir el banco de problemas de 2º de Primaria (`problemas_2_primaria.md`). |
| **Batería de Tests** | [`tests/`](tests/) | **Suite automatizada de 162 pruebas en Pytest**: Validación de conteo, biyección 1-a-1 de solucionarios, etiquetas LOMLOE, fórmulas y tests adversariales. |

---

## 3. Arquitectura y Esquema de los Bancos de Problemas

Cada archivo de curso (`problemas_X_primaria.md`) presenta una arquitectura bifásica rigurosamente estandarizada para garantizar su legibilidad tanto humana como computacional.

### 3.1 Estructura Interna del Documento
1. **Encabezado y Metadatos**: Identificación del curso, marco normativo LOMLOE y resumen de bloques competenciales.
2. **Parte 1: Enunciados de los Problemas (1 al 100)**: Diseñada para el alumnado. Cada problema incluye:
   - `### Problema N`
   - `- **Subcategoría**`: Una de las 7 subcategorías pedagógicas del curso.
   - `- **Sentido LOMLOE**`: Sentido matemático curricular principal al que responde el ejercicio.
   - `- **Contexto Pokémon**`: Ambientación narrativa inmersiva (entrenadores, rutas, gimnasios, combates, crianza).
   - `**Pregunta**`: Formulación clara, con datos cuantitativos explícitos y sin ambigüedades.
3. **Parte 2: Solucionario y Respuestas Razonadas (1 al 100)**: Diseñada para el docente o la autoevaluación guiada. Cada solución sigue un esquema de tres fases obligatorias:
   - `### Solución Problema N`
   - `- **Datos identificados**`: Extracción ordenada de los datos clave del enunciado.
   - `- **Planteamiento y Operaciones**`: Justificación didáctica, fórmula aplicada y desarrollo paso a paso del cálculo.
   - `- **Respuesta Final**`: Enunciado unívoco con la magnitud numérica y unidades físicas o del juego remarcadas en **negrita** (ej. **$1.850 \text{ Pokédólares}$**, **$45 \text{ PS}$**, **$\frac{3}{8}$**).

### 3.2 Distribución de las 7 Subcategorías Temáticas
Para garantizar una cobertura pedagógica equilibrada y representativa de todos los aspectos del juego, los 100 problemas de cada curso se distribuyen homogéneamente entre las siguientes 7 subcategorías:

```
┌────────────────────────────────────────────────────────────────────────┐
│             DISTRIBUCIÓN DE SUBCATEGORÍAS POR CURSO (100 PROBLEMAS)    │
├────┬──────────────────────────────────────────┬────────────────────────┤
│ 1. │ Aritmética y Operaciones de Combate      │ ~15 problemas / curso  │
│ 2. │ Captura, Crianza y Probabilidad          │ ~14 problemas / curso  │
│ 3. │ Economía Pokémon y Tiendas               │ ~14 problemas / curso  │
│ 4. │ Medida, Tiempo y Distancias              │ ~14 problemas / curso  │
│ 5. │ Geometría y Exploración Espacial         │ ~14 problemas / curso  │
│ 6. │ Puntos de Experiencia (EXP) y Nivel      │ >=15 problemas / curso │
│ 7. │ Estadísticas, Datos y Gráficos           │ ~14 problemas / curso  │
└────┴──────────────────────────────────────────┴────────────────────────┘
```

---

## 4. Progresión Pedagógica del Cálculo de Experiencia (EXP)

Uno de los requerimientos nucleares del proyecto es la inclusión de al menos 15 problemas dedicados por curso (77 en total a lo largo del proyecto) orientados al cálculo de la experiencia necesaria para subir de nivel y la obtenida tras derrotar oponentes. La complejidad matemática de estos problemas evoluciona en estricta sincronía con la madurez curricular del alumnado:

```
  2º Primaria (Lineal & Sumativo)
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

## 6. Uso Rápido, Generación HTML y Batería de Pruebas (Pytest)

### 6.1 Uso Rápido (Cuadernillos Listos para Imprimir)
No necesitas instalar nada para empezar a usar los cuadernillos:
1. Abre [`html/index.html`](html/index.html) directamente en cualquier navegador web.
2. Selecciona el curso (2º a 6º de Primaria) o el documento de referencia que quieras consultar.
3. Usa la función de impresión del navegador (`Ctrl+P`) para imprimir o guardar en PDF las fichas con sus ilustraciones locales y solucionarios.

### 6.2 Regeneración de Activos y HTML
Si modificas algún archivo Markdown y quieres regenerar la versión HTML o actualizar la caché de imágenes:
- **Requisitos**: Python 3.10+ y la librería `markdown` (`pip install markdown`).
```powershell
# (Opcional) Descargar/actualizar artworks oficiales y datos de especies en local
python download_assets.py

# Compilar todos los Markdown a HTML en la carpeta html/
python build_html.py
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

Para ejecutar la suite completa de 162 pruebas desde el directorio raíz del proyecto:
```powershell
# Ejecución completa con reporte detallado paso a paso
python -m pytest tests/ -v

# Ejecución en modo resumen rápido
python -m pytest tests/ -q
```

Para ejecutar de manera aislada la suite de pruebas adversariales y de estrés (Tier 5):
```powershell
python -m pytest tests/test_tier5_adversarial.py -v
```

### 6.5 Arquitectura de los 5 Tiers de Verificación

La suite de pruebas está organizada en 5 niveles de abstracción (*Tiers*), sumando un total de **162 pruebas automatizadas** que se ejecutan en aproximadamente 1 segundo:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DEL TEST HARNESS (162 TESTS)                │
├────────┬──────────────────────────────────┬───────┬─────────────────────────┤
│ Tier   │ Nombre del Módulo                │ Tests │ Objetivo Principal      │
├────────┼──────────────────────────────────┼───────┼─────────────────────────┤
│ Tier 1 │ test_tier1_problem_counts.py     │   21  │ Existencia de archivos, │
│        │                                  │       │ conteo (100/curso, 500  │
│        │                                  │       │ total) y numeración.    │
├────────┼──────────────────────────────────┼───────┼─────────────────────────┤
│ Tier 2 │ test_tier2_answer_keys.py        │   21  │ Biyección 1-a-1 de so-  │
│        │                                  │       │ luciones, bloques obli- │
│        │                                  │       │ gatorios y negritas.    │
├────────┼──────────────────────────────────┼───────┼─────────────────────────┤
│ Tier 3 │ test_tier3_lomloe_and_exp.py     │   26  │ Sentidos LOMLOE, >=15   │
│        │                                  │       │ EXP por curso y progre- │
│        │                                  │       │ sión pedagógica.        │
├────────┼──────────────────────────────────┼───────┼─────────────────────────┤
│ Tier 4 │ test_tier4_reference_tables.py   │   13  │ Integridad matriz 18x18,│
│        │                                  │       │ fórmulas de PS y URLs.  │
├────────┼──────────────────────────────────┼───────┼─────────────────────────┤
│ Tier 5 │ test_tier5_adversarial.py        │   81  │ Estrés adversarial,     │
│        │                                  │       │ límites numéricos RD    │
│        │                                  │       │ 157/2022, 2.754 combi-  │
│        │                                  │       │ naciones duales, 85 PS  │
│        │                                  │       │ benchmarks, bitwise     │
│        │                                  │       │ LF/CRLF y 100% HTTPS.   │
├────────┴──────────────────────────────────┴───────┴─────────────────────────┤
│ TOTAL AUTOMATED TESTS: 162 PASSED (Exit Code 0)                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Aviso Legal, Atribución y Licencia Educativa

Este proyecto ha sido desarrollado exclusivamente con fines educativos, de divulgación pedagógica e investigación didáctica sin ánimo de lucro, de acuerdo con las disposiciones sobre el derecho de cita y uso legítimo recogidas en la legislación internacional sobre propiedad intelectual (*Fair Use*).

- Las marcas, nombres de criaturas, habilidades, conceptos y elementos del juego Pokémon son propiedad registrada de **Nintendo**, **Creatures Inc.** y **Game Freak Inc.**
- Los textos de los problemas, las explicaciones didácticas, las soluciones paso a paso y la infraestructura de pruebas automatizadas han sido creados de forma original para este repositorio, quedando a disposición de la comunidad educativa bajo licencia de uso abierto para docentes y centros escolares.
