from SPARQLWrapper import SPARQLWrapper, JSON
import random

prefixes = """
        PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        """

sparql = SPARQLWrapper("http://localhost:7200/repositories/historia")

def execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# Function to fetch questions from DBpedia
def fetch_questions_from_dbpedia():
    questions = []
    questions.append(fetch_question_birth())
    questions.append(fetch_question_kings_per_dinasty())
    questions.append(fetch_question_dinasty())
    questions.append(fetch_question_kings_per_dinasty())
    questions.append(fetch_question_birth_president())
    questions.append(fetch_question_cognome())

    print(questions)
    return questions


# Function to fetch question of date of Birth of a King
def fetch_question_birth():
    results = execute_query(prefixes +
    """
        select ?nome ?dataNascimento where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :nascimento ?dataNascimento .
        } 
    """)

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    date = random_binding["dataNascimento"]["value"]
    question_text = f"What is the date of birth of {person}?"
    options = [date]
    while len(options) < 4:
        random_date = random.choice(results["results"]["bindings"])["dataNascimento"]["value"]
        if random_date not in options:
            options.append(random_date)
    random.shuffle(options)

    question = {
        "question": question_text,
        "options": options,
        "answer": date
    }

    return question


def fetch_question_dinasty():
    results = execute_query(prefixes +
    """
        select ?nome ?nomeDinastia where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :temReinado ?reinado .
            ?reinado :dinastia ?dinastia .
            ?dinastia :nome ?nomeDinastia . 
        } 
    """)

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    dinasty = random_binding["nomeDinastia"]["value"]
    question_text = f"What is the dinasty of {person}?"
    options = [dinasty]
    while len(options) < 4:
        random_dinasty = random.choice(results["results"]["bindings"])["nomeDinastia"]["value"]
        if random_dinasty not in options:
            options.append(random_dinasty)
    random.shuffle(options)

    question = {
        "question": question_text,
        "options": options,
        "answer": dinasty
    }

    return question

def fetch_question_kings_per_dinasty():
    results = execute_query(prefixes +
    """
        select ?nomeDinastia (COUNT(?rei) AS ?quantidadeReis) where {
        ?rei rdf:type :Rei .
        ?rei :temReinado ?reinado .
        ?reinado :dinastia ?dinastia .
    	?dinastia :nome ?nomeDinastia .
        }
        GROUP BY ?nomeDinastia
    """)

    random_binding = random.choice(results["results"]["bindings"])
    dinasty = random_binding["nomeDinastia"]["value"]
    quantity = random_binding["quantidadeReis"]["value"]

    answer = random.choice([True, False])

    if answer:
        question_text = f"The dinasty {dinasty} had {quantity} kings. True or False?"
        answer = "True"
        options = ["True", "False"]
    else:
        random_quantity = random.choice(results["results"]["bindings"])["quantidadeReis"]["value"]
        while random_quantity == dinasty:
            random_quantity = random.choice(results["results"]["bindings"])["quantidadeReis"]["value"]
        question_text = f"The dinasty {dinasty} had {random_quantity} kings. True or False?"
        answer = "False"
        options = ["True", "False"]

    question = {
        "question": question_text,
        "options": options,
        "answer": answer
    }

    return question

def fetch_question_birth_president():
    results = execute_query(prefixes +
    """
        select ?nome ?data where{
            ?s rdf:type :Presidente .
            ?s :nome ?nome .
            ?s :nascimento ?data .
        } 
    """)
    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    date = random_binding["data"]["value"]
    question_text = f"What is the date of birth of {person}?"

    options = [date]
    while len(options) < 4:
        random_date = random.choice(results["results"]["bindings"])["data"]["value"]
        if random_date not in options:
            options.append(random_date)
    random.shuffle(options)

    question = {
        "question": question_text,
        "options": options,
        "answer": date
    }

    return question

def fetch_question_cognome():
    results = execute_query(prefixes +
    """
        select ?nome ?cognome where {
            ?s rdf:type :Rei .
            ?s :nome ?nome .
            ?s :cognomes ?cognome .
        } 
    """)

    random_binding = random.choice(results["results"]["bindings"])
    person = random_binding["nome"]["value"]
    cognome = random_binding["cognome"]["value"]
    answer = random.choice([True, False])

    if answer:
        question_text = f"The cognome of {person} is {cognome}. True or False?"
        answer = "True"
        options = ["True", "False"]
    else:
        random_cognome = random.choice(results["results"]["bindings"])["cognome"]["value"]
        while random_cognome == cognome:
            random_cognome = random.choice(results["results"]["bindings"])["cognome"]["value"]

        question_text = f"The cognome of {person} is {random_cognome}. True or False?"
        answer = "False"
        options = ["True", "False"]

    question = {
        "question": question_text,
        "options": options,
        "answer": answer
    }

    return question