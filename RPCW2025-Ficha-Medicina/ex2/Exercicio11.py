from rdflib import OWL, RDF, RDFS, Graph, Namespace, XSD, Literal

graph = Graph()
graph.parse("med_doentes.ttl")

q = """
SELECT (COUNT(DISTINCT ?disease) AS ?count)
WHERE {
    ?disease a :Disease .
}
"""

print("Total number of distinct diseases:")
for row in graph.query(q):
    print(row[0])

q2 = """
SELECT ?disease
WHERE {
    ?disease a :Disease .
    ?disease :hasSymptomD :yellowish_skin .
}
"""

print("\nDiseases with yellowish skin symptom:")
for row in graph.query(q2):
    print(row[0].rsplit("#")[-1])

q3 = """
SELECT ?disease
WHERE {
    ?disease a :Disease .
    ?disease :hasTreatment :exercise .
}
"""

print("\nDiseases with exercise as treatment:")
for row in graph.query(q3):
    print(row[0].rsplit("#")[-1])

q4 = """
Select ?nome
Where {
    ?nome a :Patient .
    ?nome :hasName ?name .
}
Order by ?name
"""
print("\nPatients sorted by name:")
for row in graph.query(q4):
    print(row[0].rsplit("#")[-1])