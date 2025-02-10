from rdflib import Graph, URIRef, Literal, XSD, RDF
import json

URI = "http://www.semanticweb.org/gonca/ontologies/2025/tpc1/"

g = Graph()
g.parse("setup.ttl", format="ttl")

with open("emd.json", "r", encoding="utf-8") as f:  # Garante leitura correta
    dataset = json.load(f)

_id = URIRef(URI + "_id")
primeiroNome = URIRef(URI + "primeiroNome")
ultimoNome = URIRef(URI + "ultimoNome")
idade = URIRef(URI + "idade")
genero = URIRef(URI + "genero")
morada = URIRef(URI + "morada")
email = URIRef(URI + "email")
federado = URIRef(URI + "federado")
resultado = URIRef(URI + "resultado")
dataEMD = URIRef(URI + "dataEMD")
nome_Modalidade = URIRef(URI + "nome_Modalidade")
clube = URIRef(URI + "clube")

fezExame = URIRef(URI + "fezExame")
pratica = URIRef(URI + "pratica")



def populate(g, id, primeiro_nome, ultimo_nome, idade_value, genero_value, morada_value, email_value, federado_value, clube_value, modalidade_uri, exame_uri):

    own_uri = URIRef(URI + "Pessoa/" + id)

    g.add((own_uri, RDF.type, URIRef(URI + "Pessoa")))
    g.add((own_uri, _id, Literal(id, datatype=XSD.string)))
    g.add((own_uri, primeiroNome, Literal(primeiro_nome, datatype=XSD.string)))
    g.add((own_uri, ultimoNome, Literal(ultimo_nome, datatype=XSD.string)))
    g.add((own_uri, idade, Literal(idade_value, datatype=XSD.integer)))
    g.add((own_uri, genero, Literal(genero_value, datatype=XSD.string)))
    g.add((own_uri, morada, Literal(morada_value, datatype=XSD.string)))
    g.add((own_uri, email, Literal(email_value, datatype=XSD.string)))
    g.add((own_uri, federado, Literal(federado_value, datatype=XSD.boolean)))
    g.add((own_uri, clube, Literal(clube_value, datatype=XSD.string)))

    g.add((own_uri, pratica, modalidade_uri))
    g.add((own_uri, fezExame, exame_uri))


for data in dataset:
    modalidade_uri = URIRef(URI + "Modalidade/" + data["modalidade"])
    exame_uri = URIRef(URI + "Exame/" + data["_id"])
    #print(json.dumps(data["nome"], indent=4, ensure_ascii=False))

    populate(g, data["_id"], data["nome"]["primeiro"], data["nome"]["último"], data["idade"], data["género"], data["morada"], data["email"], data["federado"], data["clube"], modalidade_uri, exame_uri)
    
    g.add((exame_uri, RDF.type, URIRef(URI + "Exame")))
    g.add((exame_uri, _id, Literal(data["_id"], datatype=XSD.string)))
    g.add((exame_uri, dataEMD, Literal(data["dataEMD"], datatype=XSD.string)))
    g.add((exame_uri, resultado, Literal(data["resultado"], datatype=XSD.boolean)))

    g.add((modalidade_uri, RDF.type, URIRef(URI + "Modalidade")))
    g.add((modalidade_uri, nome_Modalidade, Literal(data["modalidade"], datatype=XSD.string)))
    
    g.serialize(destination="result.ttl", format="turtle")




