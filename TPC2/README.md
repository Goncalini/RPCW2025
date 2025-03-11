# README - Readme para auxiliar na compreensão e servir de apoio para SPARQL


## Consultas e Explicações

### 1. Quantos triplos existem na Ontologia?

```sparql
SELECT (COUNT(*) AS ?count) WHERE {
  ?s ?p ?o .
}
```
**Explicação:**
Esta consulta conta o número total de triplos existentes na base de conhecimento RDF. O padrão `?s ?p ?o` captura todos os sujeitos (`?s`), predicados (`?p`) e objetos (`?o`), sem restrição, garantindo assim que todos os triplos sejam contabilizados.

---

### 2. Que classes estão definidas?

```sparql
SELECT DISTINCT ?class WHERE {
  ?class a owl:Class .
}
```
**Explicação:**
Aqui, estamos consultando todas as classes definidas na ontologia. A tripla `?class a owl:Class` seleciona os recursos que são instâncias da classe `owl:Class`, ou seja, as definições de categorias de entidades na ontologia.

---

### 3. Que propriedades tem a classe "Rei"?

```sparql
SELECT DISTINCT ?property WHERE {
  ?s a :Rei .
  ?s ?property ?o .
}
```
**Explicação:**
A consulta busca todas as propriedades associadas a instâncias da classe `:Rei`. O primeiro padrão `?s a :Rei` filtra os indivíduos que pertencem à classe `:Rei`, e a segunda linha `?s ?property ?o` recupera todas as propriedades que esses indivíduos possuem.

---

### 4. Quantos reis aparecem na ontologia?

```sparql
SELECT (COUNT(*) as ?count) WHERE {
  ?s a :Rei .
}
```
**Explicação:**
Conta o número total de indivíduos que pertencem à classe `:Rei`, ou seja, todos os reis registrados na ontologia.

---

### 5. Calcula uma tabela com o nome, data de nascimento e cognome dos reis.

```sparql
SELECT ?nome ?data ?cognome WHERE {
  ?s a :Rei .
  ?s :nome ?nome .
  ?s :nascimento ?data .
  ?s :cognomes ?cognome .
}

```
**Explicação:**
A consulta recupera informações detalhadas sobre os reis registrados na ontologia. Os padrões `?s :nome ?nome`, `?s :nascimento ?data` e `?s :cognomes ?cognome` filtram os atributos desejados.

---

### 6. Acrescenta à tabela anterior a dinastia de cada rei.

```sparql
SELECT ?nome ?data ?cognome ?dinastia WHERE {
  ?s a :Rei .
  ?s :nome ?nome .
  ?s :nascimento ?data .
  ?s :cognomes ?cognome .
  ?r :temMonarca ?s .
  ?r :dinastia ?dinastia .
}
```
**Explicação:**
A consulta amplia a anterior incluindo a dinastia de cada rei. A relação `?r :temMonarca ?s` conecta um reinado `?r` ao monarca correspondente `?s`, permitindo acessar a propriedade `?r :dinastia ?dinastia`.

---

### 7. Qual a distribuição de reis pelas 4 dinastias?

```sparql
SELECT ?dinastia (COUNT (DISTINCT ?monarca) as ?d) WHERE {
  ?r :dinastia ?dinastia .
  ?r :temMonarca ?monarca .
  ?monarca a :Rei .
} GROUP BY ?dinastia ORDER BY ?dinastia
```

**Explicação:**
Esta consulta agrupa os reis por dinastia e conta quantos reis pertencem a cada uma. O uso de `GROUP BY ?dinastia` e `COUNT(DISTINCT ?monarca)` garante que a contagem seja feita corretamente.

ou
```sparql
SELECT ?dinastia (count(distinct ?monarca) as ?d)WHERE {
  ?monarca a Rei .
  ?monarca :temReinado/:dinastia ?dinastia .

} group by ?dinastia order by ?dinastia
```

---

### 8. Lista os descobrimentos (sua descrição) por ordem cronológica.

```sparql
SELECT ?descobrimento ?descricao WHERE {
  ?descobrimento a :Descobrimento .
  ?descobrimento :data ?data .
  ?descobrimento :notas ?descricao .
} ORDER BY ?data
```

**Explicação:**
A consulta recupera os descobrimentos registrados, suas descrições e ordena os resultados pela data do evento.

---

### 9. Lista as várias conquistas, nome e data, com o nome do rei que reinava no momento.

```sparql
SELECT ?nome ?data ?nomeMonarca WHERE {
  ?conquista a :Conquista .
  ?conquista :nome ?nome .
  ?conquista :data ?data .
  ?conquista :temReinado ?reinado .
  ?reinado :temMonarca ?monarca .
  ?monarca :nome ?nomeMonarca .
} ORDER BY ?data
```
**Explicação:**
A consulta recupera informações sobre conquistas e os reis que estavam no poder no momento, conectando conquistas a reinados e reis.

---

### 10. Calcula uma tabela com nome, data de nascimento e número de mandatos de presidentes portugueses.

```sparql
SELECT ?nome ?nascimento (COUNT(DISTINCT ?mandato) as ?numMandatos) WHERE {
  ?presidente a :Presidente .
  ?presidente :nome ?nome .
  ?presidente :nascimento ?nascimento .
  ?presidente :mandato ?mandato .
} GROUP BY ?presidente ?nome ?nascimento
```
**Explicação:**
Conta quantos mandatos cada presidente teve, agrupando por presidente.

---

### 11. Quantos mandatos teve Sidónio Pais? Em que datas iniciaram e terminaram?

```sparql
SELECT (COUNT(DISTINCT ?mandato) as ?numMandatos) ?dataInicio ?dataFim WHERE {
  ?presidente a :Presidente .
  ?presidente :nome "Sidónio Bernardino Cardoso da Silva Pais" .
  ?presidente :mandato ?mandato .
  ?mandato :comeco ?dataInicio .
  ?mandato :fim ?dataFim .
} GROUP BY ?presidente ?dataInicio ?dataFim
```
**Explicação:**
Filtra especificamente o presidente Sidónio Pais e retorna quantos mandatos teve, além das datas de início e fim de cada um.

---

### 12-14. Partidos e militantes

Consultas similares analisam partidos e distribuição de militantes, seguindo a mesma lógica apresentada acima.

