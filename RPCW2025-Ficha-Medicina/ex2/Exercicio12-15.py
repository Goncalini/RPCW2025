from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD


g = Graph()
g.parse("med_doentes.ttl")

q12 ="""
CONSTRUCT {
    ?patient :hasDisease ?disease .
}
WHERE{
    ?patient :hasSymptomP ?symptom1, ?symptom2, ?symptom3 .
    ?disease :hasSymptomD ?symptom1, ?symptom2, ?symptom3 .
    FILTER (?symptom1 != ?symptom2 && ?symptom1 != ?symptom3 && ?symptom2 != ?symptom3)
}
""" 

print("Constructing graph with patients and their diseases based on symptoms...")

n = Namespace("http://www.example.org/disease-ontology#")

for r in g.query(q12):
    g.add((r))

g.serialize("exercicio12.ttl", format="turtle")