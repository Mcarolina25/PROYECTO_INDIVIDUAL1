from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
app = FastAPI()
import locale

# Cargar los datasets
movies_df = pd.read_csv('Dataset_Procesados/processed_movies_dataset.csv')
credits_df = pd.read_csv('Dataset_Procesados/processed_credits_dataset.csv')
# Preprocesamiento de datos
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])
movies_df['month'] = movies_df['release_date'].dt.month_name()
movies_df['day'] = movies_df['release_date'].dt.day_name()
try:
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')  # Cambia a inglés si es necesario
except locale.Error:
    pass  # Ignora el error si no se puede establecer

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de películas"}
# ENDPOIN1:
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    mes_num = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    if mes.lower() not in mes_num:
        raise HTTPException(status_code=400, detail="Mes no válido")
    
    cantidad = movies_df[movies_df['release_date'].dt.month == mes_num[mes.lower()]].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en el mes de {mes}"}
# ENDPOIT2:
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dia_num = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    if dia.lower() not in dia_num:
        raise HTTPException(status_code=400, detail="Día no válido")
    
    cantidad = movies_df[movies_df['release_date'].dt.dayofweek == dia_num[dia.lower()]].shape[0]
    return {"message": f"{cantidad} películas fueron estrenadas en los días {dia}"}
# ENDPOIN3:
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if not pelicula.empty:
        return f"La película {titulo_de_la_filmacion} fue estrenada en el año {pelicula['release_year'].values[0]} con un score de popularidad de {pelicula['popularity'].values[0]}"
    raise HTTPException(status_code=404, detail="Película no encontrada")
# ENDPOIN4:
@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if not pelicula.empty:
        if pelicula['vote_count'].values[0] >= 2000:
            return f"La película {titulo_de_la_filmacion} fue estrenada en el año {pelicula['release_year'].values[0]}. La misma cuenta con un total de {pelicula['vote_count'].values[0]} valoraciones, con un promedio de {pelicula['vote_average'].values[0]}"
        return "La película no cumple con el mínimo de 2000 valoraciones."
    raise HTTPException(status_code=404, detail="Película no encontrada")
# ENDPOIN5:
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    # Verificar que credits_df no esté vacío
    if credits_df.empty:
        raise HTTPException(status_code=500, detail="Datos de películas no disponibles")

    # Filtrar las películas del actor
    actor_movies = credits_df[credits_df['cast_names'].str.contains(nombre_actor, na=False)]
    
    if not actor_movies.empty:
        total_peliculas = actor_movies.shape[0]
        total_retorno = movies_df['return'].sum()
        promedio_retorno = total_retorno / total_peliculas if total_peliculas > 0 else 0
        return {
            "mensaje": f"El actor {nombre_actor} ha participado de {total_peliculas} filmaciones, "
                       f"con un retorno total de {total_retorno} y un promedio de {promedio_retorno} por filmación."
        }
    
    raise HTTPException(status_code=404, detail="Actor no encontrado")
# ENDPOIN6:
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_movies = credits_df[credits_df['director_names'].str.lower() == nombre_director.lower()]
    if not director_movies.empty:
        resultados = []
        for _, row in director_movies.iterrows():
            resultados.append({
                "titulo": row['title'],
                "fecha_lanzamiento": row['release_date'],
                "retorno": row['return'],
                "costo": row['budget'],
                "ganancia": row['revenue']
            })
        return resultados
    raise HTTPException(status_code=404, detail="Director no encontrado")

# Limpiar datos
movies_df = movies_df[movies_df['title'].notna()]

