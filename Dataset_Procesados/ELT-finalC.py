import pandas as pd
import ast

# Cargar el dataset
credits = pd.read_csv('credits.csv')
# Seleccionar solo las columnas necesarias
credits = credits[['id', 'cast', 'crew']]

# Función para desanidar columnas
def desanidar_columna(df, columna, key):
    def obtener_valor(x):
        try:
            # Convertir la cadena en una lista de diccionarios
            data = ast.literal_eval(x)
            if isinstance(data, list):
                # Extraer los valores del key especificado
                return [d[key] for d in data if key in d]
            else:
                return None
        except (ValueError, SyntaxError):
            return None

    return df[columna].apply(obtener_valor)

# Desanidar la columna 'cast' para obtener los nombres de los actores
credits['cast_names'] = desanidar_columna(credits, 'cast', 'name')

# Desanidar la columna 'crew' para obtener los nombres de los directores
def obtener_directores(crew):
    try:
        # Convertir la cadena en una lista de diccionarios
        data = ast.literal_eval(crew)
        if isinstance(data, list):
            # Filtrar por el rol de director y extraer los nombres
            return [d['name'] for d in data if d.get('job') == 'Director']
        else:
            return None
    except (ValueError, SyntaxError):
        return None

credits['director_names'] = credits['crew'].apply(obtener_directores)

# Eliminar las columnas originales
credits = credits.drop(columns=['cast', 'crew'])

# Mostrar el dataset procesado
print(credits.head())
# Guardar el dataset procesado
credits.to_csv('processed_credits_dataset.csv', index=False)