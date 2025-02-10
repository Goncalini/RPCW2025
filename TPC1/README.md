# Conversão de JSON para RDF com RDFlib

## Descrição
Este projeto tem como objetivo converter dados armazenados em um ficheiro JSON (`emd.json`) para o formato RDF utilizando a biblioteca **RDFlib** em Python. O script lê os dados do JSON, estrutura-os como um grafo RDF e salva o resultado em um ficheiro **Turtle (`result.ttl`)**.

## Tecnologias Utilizadas
- **Python 3**
- **RDFlib** (para manipulação do grafo RDF)
- **JSON** (para leitura dos dados)

## Estrutura do Código
O script segue as seguintes etapas:
1. **Carregamento do Grafo RDF**:
   - O grafo é inicializado e é carregado um ficheiro de configuração (`setup.ttl`).
2. **Leitura do JSON**:
   - Os dados são lidos a partir do ficheiro `emd.json`.
3. **Definição de URIs**:
   - São definidas URIs para as diferentes propriedades da ontologia (ex: `primeiroNome`, `idade`, `clube`, etc.).
4. **Processamento e Inserção de Dados**:
   - Para cada entrada no JSON:
     - Cria-se um recurso para a Pessoa, Modalidade e Exame.
     - As relações entre os recursos são adicionadas ao grafo.
5. **Exportação para RDF (Turtle)**:
   - O grafo resultante é serializado e salvo em `result.ttl`.


## Estrutura Esperada do `emd.json`
O JSON deve conter entradas com a seguinte estrutura:
```json
{
    "_id": "60b3ee0e4a1e0233af16ac8c",
    "dataEMD": "2020-12-29",
    "nome": {
        "primeiro": "Bernard",
        "último": "Stokes"
    },
    "idade": 34,
    "género": "M",
    "morada": "Sussex",
    "modalidade": "Badminton",
    "clube": "AVCfamalicão",
    "email": "bernard.stokes@avcfamalicão.biz",
    "federado": false,
    "resultado": false
}
```

## Resultado RDF
O ficheiro `result.ttl` conterá os dados estruturados em **RDF (Turtle)**, algo semelhante a:
```ttl
@prefix ex: <http://www.semanticweb.org/gonca/ontologies/2025/tpc1/> .

ex:Pessoa/60b3ee0e4a1e0233af16ac8c a ex:Pessoa ;
    ex:primeiroNome "Bernard" ;
    ex:ultimoNome "Stokes" ;
    ex:idade 34 ;
    ex:genero "M" ;
    ex:morada "Sussex" ;
    ex:email "bernard.stokes@avcfamalicão.biz" ;
    ex:federado false ;
    ex:pratica ex:Modalidade/Badminton ;
    ex:fezExame ex:Exame/60b3ee0e4a1e0233af16ac8c .
```

## Notas
- Certifique-se de que o ficheiro `emd.json` está corretamente formatado.
- Se houver problemas com caracteres especiais, certifique-se de que o ficheiro JSON está em **UTF-8**.
- O script pode ser expandido para suportar mais propriedades e relações.

---
**Autor:** gonca | **Ano:** 2025

