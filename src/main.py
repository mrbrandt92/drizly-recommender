import json

from src.utils import dbsearch, recommender

def processRecommendations(user_data):

    try:
        cats_df, user_row_df = dbsearch.search(user_data)
        print('done!')
    except Exception as e:
        print(e)

    response = recommender.cosine_similarity_T(cats_df, user_row_df)

    return response

