# PROYECTO INDIVIDUAL 1

---

**Autor:** Maria Carolina Blasco  
**Cohorte:** dataft27  

## Descripción general

En este proyecto se nos pidió realizar un MVP para una empresa que provee servicios de agregación de plataformas de streaming. El objetivo fue realizar transformaciones a los datos, crear un EDA (Análisis Exploratorio de Datos), desarrollar una API y un sistema de recomendación de películas.

---

## Transformaciones

### Dataset 1: Créditos de las películas
El primer dataset contenía los créditos de las películas (todo el cast completo que participó en cada película). Debido a su gran tamaño, no se podía subir a GitHub ni realizar el deployment adecuado en Render. Por este motivo, se creó un código aparte para analizar y transformar el contenido del dataset, dejando únicamente los datos necesarios para este proyecto.

### Dataset 2: Información de las películas
Para el segundo dataset, se realizaron las siguientes transformaciones específicas:

- Desanidar las columnas `belongs_to_collection` y `production_companies`.
- Rellenar valores nulos en los campos `revenue` y `budget` con el número `0`.
- Eliminar los valores nulos de la columna `release_date`.
- Formatear las fechas al formato `AAAA-MM-DD` y crear la columna `release_year` para extraer el año de la fecha de estreno.
- Crear la columna `return` (retorno de inversión) calculada como `revenue / budget`. Si no hay datos disponibles para calcularlo, se asigna el valor `0`.
- Eliminar las columnas innecesarias: `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage`.

---

## EDA (Análisis Exploratorio de Datos)

Después de procesar los datasets, se realizó un análisis exploratorio para obtener información útil para el sistema de recomendación de la API. Los análisis realizados fueron:

1. **Tendencia de películas estrenadas por año**  

2. **Presupuesto promedio por año**  

3. **Nube de palabras con las palabras más frecuentes en los títulos**  

---

## API

### Endpoints obligatorios

Se desarrollaron 6 endpoints obligatorios:

1. **Películas por mes:**  
   Al ingresar un mes en español, retorna la cantidad de películas estrenadas en ese mes.

2. **Películas por día:**  
   Al ingresar un día en español, retorna la cantidad de películas estrenadas ese día.

3. **Información de una película:**  
   Al ingresar el título de una filmación, retorna el título, el año de estreno y el score.

4. **Información de un director:**  
   Al ingresar el nombre de un director presente en el dataset, retorna:
   - El éxito del director medido a través del retorno.
   - El nombre de cada película dirigida, con su fecha de lanzamiento, retorno individual, costo y ganancia.

5. **Información de un actor:**  
   Al ingresar el nombre de un actor, retorna:
   - El éxito del actor medido a través del retorno.
   - La cantidad de películas en las que ha participado.
   - El promedio de retorno (sin incluir directores).


---

## Sistema de recomendación

El sistema de recomendación que he desarrollado se basa en un enfoque de filtrado de contenido. Esto significa que las recomendaciones se generan utilizando las características de las películas, en este caso, sus géneros. La función recomendacion recibe un título de película como entrada devuelve las cinco películas más similares, excluyendo la película original.Este enfoque permite a los usuarios recibir recomendaciones personalizadas basadas en los géneros de las películas que les gustan, lo que mejora su experiencia al buscar nuevas películas para ver.

---

**Maria Carolina Blasco**  
Cohorte: **dataft27**
