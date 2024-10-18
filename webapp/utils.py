import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from joblib import dump, load
from sklearn.preprocessing import normalize




def recomienda_tf(new_basket,cestas,productos): 
    # Cargar la matriz TF y el modelo
    tf_matrix = load('tf_matrix.joblib')
                      
    count = load('count_vectorizer.joblib')
    # Convertir la nueva cesta en formato TF (Term Frequency)
    new_basket_str = ' '.join(new_basket)
    new_basket_vector = count.transform([new_basket_str])
    new_basket_tf = normalize(new_basket_vector, norm='l1')  # Normalizamos la matriz count de la cesta actual
    # Comparar la nueva cesta con las anteriores
    similarities = cosine_similarity(new_basket_tf, tf_matrix)
    # Obtener los índices de las cestas más similares
    similar_indices = similarities.argsort()[0][-4:]  # Las 4 más similares
    # Crear un diccionario para contar las recomendaciones
    recommendations_count = {}
    total_similarity = 0
    # Recomendar productos de cestas similares
    for idx in similar_indices:
        sim_score = similarities[0][idx]
        total_similarity += sim_score  # Suma de las similitudes
        products = cestas.iloc[idx]['Cestas'].split()
        # Usar un conjunto para evitar contar productos múltiples veces en la misma cesta
        unique_products = set(products)  # Usar un conjunto para obtener productos únicos
        # Con esto evitamos que la importancia crezca por las unidades
        for product in unique_products:
            if product.strip() not in new_basket:  # Evitar recomendar lo que ya está en la cesta
                recommendations_count[product.strip()] = recommendations_count.get(product.strip(), 0) + sim_score
                # Almacena el conteo de la relevancia de cada producto basado en cuántas veces aparece en las cestas similares, ponderado por la similitud de cada cesta.
    # Calcular la probabilidad relativa de cada producto recomendado
    recommendations_with_prob = []
    if total_similarity > 0:  # Verificar que total_similarity no sea cero
        recommendations_with_prob = [(product, score / total_similarity) for product, score in recommendations_count.items()]
    else:
        print("No se encontraron similitudes suficientes para calcular probabilidades.")
     
    recommendations_with_prob.sort(key=lambda x: x[1], reverse=True)  # Ordenar por puntuación
    # Crear un nuevo DataFrame para almacenar las recomendaciones
    recommendations_data = []
    
    for product, score in recommendations_with_prob:
        # Buscar la descripción en el DataFrame de productos
        description = productos.loc[productos['ARTICULO'] == product, 'DESCRIPCION']
        if not description.empty:
            recommendations_data.append({
                'ARTICULO': product,
                'DESCRIPCION': description.values[0],  # Obtener el primer valor encontrado
                'RELEVANCIA': score
            })
    recommendations_df = pd.DataFrame(recommendations_data)
    
    return recommendations_df