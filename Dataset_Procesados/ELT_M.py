import pandas as pd
import ast

# Cargar el dataset
movies = pd.read_csv('Movies/movies_dataset.csv', low_memory=False)
# Función para desanidar columnas
def desanidar_columna(df, columna, key):
    def obtener_valor(x):
        if pd.notnull(x) and x != 'nan':
            try:
                data = ast.literal_eval(x)
                # Verificar si data es un diccionario antes de usar .get()
                return data.get(key) if isinstance(data, dict) else None
            except (ValueError, SyntaxError):
                return None
        return None

    df[columna] = df[columna].apply(obtener_valor)

# Desanidar columnas específicas
columnas_a_desanidar = ['belongs_to_collection', 'production_companies', 'production_countries', 'spoken_languages']
for columna in columnas_a_desanidar:
    desanidar_columna(movies, columna, 'name')
    # Convertir revenue y budget a tipo numérico y rellenar nulos
movies['revenue'] = pd.to_numeric(movies['revenue'], errors='coerce').fillna(0)
movies['budget'] = pd.to_numeric(movies['budget'], errors='coerce').fillna(0)
# Eliminar filas con valores nulos en release_date
movies = movies.dropna(subset=['release_date'])
# Convertir release_date al formato AAAA-mm-dd y extraer el año
movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
movies['release_year'] = movies['release_date'].dt.year
# Crear la columna de retorno de inversión
movies['return'] = movies.apply(lambda x: x['revenue'] / x['budget'] if x['budget'] > 0 else 0, axis=1)
# Seleccionar solo las columnas necesarias para la API
columnas_necesarias = ['title', 'release_date', 'release_year', 'revenue', 'budget', 'return', 
                       'belongs_to_collection', 'production_companies', 'production_countries', 'spoken_languages', 'id','vote_average','vote_count', 'popularity']
movies = movies[columnas_necesarias]
# Guardar el dataset procesado
movies.to_csv('Dataset_Procesados/processed_movies_dataset.csv', index=False)
