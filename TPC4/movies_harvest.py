import json
import requests


endpoint_url = "https://dbpedia.org/sparql"

dataset = []

query1= """
SELECT DISTINCT ?film
WHERE {
    ?film a dbo:Film .
}
LIMIT 100
"""



def query_to_graphdb(sparql_query):

    header = {                              #Restrições/informação extra como o tipo de resposta esperado ou o que vai ser enviado
        "Accept": "application/json"
    }

#    parametros = {                          #Parâmetros da query
#        "query": "sparql_query",
#    }

    response = requests.get(endpoint_url, headers=header, params=sparql_query)  #Faz a query ao endpoint
    if response.status_code == 200:  # Se a query for bem sucedida
        return response.json()         # Retorna o resultado em formato JSON
    else:
        raise Exception(f"Query failed with status code {response.status_code}")  # Se falhar, levanta uma exceção
    
def get_name_from_url(url):
    return url.rsplit('/', 1)[-1].replace('_', ' ')


def populate():
    
    get_movies = query_to_graphdb(query1)
    
    movies = [film["film"]["value"] for film in get_movies.get("results", {}).get("bindings", [])]  # list comprehension

    for film in movies:
        query2 = f"""
	    SELECT DISTINCT ?title ?country ?releaseDate ?director ?abstract
	    WHERE {{
	    	<{film}> dbo:abstract ?abstract .
	    	<{film}> rdfs:label ?title .
	    	OPTIONAL {{ <{film}> dbo:country ?country . }}
	    	OPTIONAL {{ <{film}> dbo:releaseDate ?releaseDate . }}
	    	OPTIONAL {{ <{film}> dbo:director ?director . }}
	    	FILTER (lang(?abstract) = "en") .
	    	FILTER (lang(?title) = "en") .
	    }}
	    """
        
        get_movies_info = query_to_graphdb(query2)

        query3 = f"""
	    SELECT DISTINCT ?actor ?name ?birthDate ?nationality
	    WHERE {{
	    	<{film}> dbo:starring ?actor .
	    	OPTIONAL {{ ?actor rdfs:label ?name . FILTER (lang(?name) = "en") . }}
	    	OPTIONAL {{ ?actor dbo:birthDate ?birthDate . }}
	    	OPTIONAL {{ ?actor dbo:nationality ?nationality . }}
	    }}
	    """

        get_cast = query_to_graphdb(query3)

        actors_list = []

        actors = get_cast.get("results", {}).get("bindings", [])

        for actor in actors:
            actors_list.append(
                {
                    "id" : get_name_from_url(actor.get("actor", {}).get("value", "")),
                    "nome": actor.get("name", {}).get("value", ""),
	    			"dataNasc": actor.get("birthDate", {}).get("value", ""),
	    			"origem": actor.get("nationality", {}).get("value", "")
	    		}
	    	) 

        query4 = f"""
            SELECT DISTINCT ?genreLabel
            	WHERE {{
            		<{film}> dbo:genre ?genre .
            		?genre rdfs:label ?genreLabel .
            		FILTER (lang(?genreLabel) = "en") .
            	}}
            	"""
        get_genre = query_to_graphdb(query4)

        genres = [g["genreLabel"]["value"] for g in get_genre("results", {}).get("bindings", [])]

        if get_movies_info["results"]["bindings"]:
            binding = get_movies_info["results"]["bindings"][0]
            dataset.append(
	    		{
	    			"id": get_name_from_url(film),
	    			"titulo": binding["title"]["value"],
	    			"pais": get_name_from_url(binding.get("country", {}).get("value", "")),
	    			"data": binding.get("releaseDate", {}).get("value", ""),
	    			"realizador": get_name_from_url(binding.get("director", {}).get("value", "")),
	    			"elenco": actors_list,
	    			"genero": genres,
	    			"sinopse": binding["abstract"]["value"]
	    		}
	    	)
        else:
            dataset.append(
	    		{
	    			"id": get_name_from_url(film),
	    			"titulo": "",
	    			"pais": "",
	    			"data": "",
	    			"realizador": "",
	    			"elenco": actors_list,
	    			"genero": genres,
	    			"sinopse": ""
	    		}
	    	)

with open('filmes_result.json', 'w') as f:
	json.dump(dataset, f, indent=4)

print("Done!!!!!!!!!!!!!!!!")
    
populate()


