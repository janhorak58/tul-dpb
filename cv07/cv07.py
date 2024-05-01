from elasticsearch import Elasticsearch

INDEX_NAME = "person"


def print_delimiter(n):
    print("\n", "#" * 10, "Úloha", n, "#" * 10, "\n")


# Připojení k ES
from pswd import password


from elasticsearch import Elasticsearch


es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", password),
    verify_certs=False  
)


if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

# Index není potřeba vytvářet - pokud neexistuje, tak se automaticky vytvoří při vložení prvního dokumentu

# 1. Vložte osobu se jménem John
print_delimiter(1)
john_document = {"name": "John"}
john_id = es.index(index=INDEX_NAME, document=john_document)["_id"]
print(f"ID: {john_id}")


# 2. Vypište vytvořenou osobu (pomocí get a parametru id)
print_delimiter(2)
john_retrieved = es.get(index=INDEX_NAME, id=john_id)
print(john_retrieved)


# 3. Vypište všechny osoby (pomocí search)
print_delimiter(3)

all_people = es.search(index=INDEX_NAME, query={"match_all": {}})
print(all_people["hits"]["hits"])

# 4. Přejmenujte vytvořenou osobu na 'Jane'
print_delimiter(4)
updated_person = es.update(index=INDEX_NAME, id=john_id, doc={"doc": {"name": "Jane"}})
print(updated_person)


# 5. Smažte vytvořenou osobu
print_delimiter(5)
es.delete(index=INDEX_NAME, id=john_id)
print(john_id, "odstraněn")

# 6. Smažte vytvořený index
print_delimiter(6)
es.indices.delete(index=INDEX_NAME)

