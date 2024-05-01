"""
ÚLOHY
• vyhledávání produktů (index products)
1. vytvořte dotaz pro vyhledávání výrazu (term) ‚coffee‘ v názvu produktu • kolik výsledků se vrátí?
2. upravte dotaz tak, aby fungoval i v případě jednoho uživatelského překlepu• např. stejné výsledky pro ‚cofee‘ nebo ‚coffe‘ • co se stane po povolení více než jednoho překlepu?
3. vytvořte dotaz, který vyhledá produkty s tagem ‚Coffee‘ (term) • liší se počet výsledků? pokud ano, který název nenalezl první dotaz a proč?
4. najděte produkty s tagem ‚Coffee‘ s 10 nebo méně kusy na skladě (in_stock)
5. najděte produkty, které v názvu mají ‚coffee‘, ale neobsahují ‚cup‘ • zobrazte jen názvy
6. vyfiltrujte všechny produkty, které byly přidány po roce 2000 • nebudou skórovány
7. full-textově vyhledejte produkty obsahující v názvu „Red Wine“
4CVIČENÍ VIII. | 22.4.2024 | DPB
BONUSOVÉ ÚLOHY
• vyhledávání produktů (index products)
8. vytvořte dotaz, který bude fungovat jako našeptávač při vyhledávání • začne vracet nejvíce relevantní výsledky během psaní • např. uživatel napíše pouze znak ‚c‘ a už jsou mu vráceny první výsledky • zadaný řetězec se může nacházet kdekoliv v názvu • doporučujte pouze 5 relevantních produktů • vyzkoušejte si postupně vyhledávat ‚c‘, ‚co‘, …, ‚coffee‘
• vyhledávání receptů (index recipes)
9. vytvořte dotaz, který bude vracet recepty, v nichž se nachází libovolný výraz • hledaný výraz může být v nadpisu, popisu nebo ingrediencích receptu • např. spaghetti
10. vytvořte dotaz, který bude v názvu hledat frázi „Pasta Carbonara“ • kolik je výsledků? • dotaz rozšiřte o hledání v blízkosti, aby výsledkem byl i výraz „Carbonara Pasta“
"""

import urllib3


urllib3.disable_warnings()
from elasticsearch import Elasticsearch


def print_delimiter(n):
    print("\n", "#" * 10, "Úloha", n, "#" * 10, "\n")


# Připojení k ES
from pswd import password


from elasticsearch import Elasticsearch



# es = Elasticsearch(
#     "https://localhost:9200",
#     basic_auth=("elastic", password),
#     ca_certs="/home/jan/Documents/school/tul/summer_2024/dpb/cv08/elasticsearch_cert.pem",
#     verify_certs=True
# )

es = Elasticsearch(
    "https://localhost:9200", basic_auth=("elastic", password), verify_certs=False
)

print_delimiter(1)
# 1. vytvořte dotaz pro vyhledávání výrazu (term) ‚coffee‘ v názvu produktu • kolik výsledků se vrátí?
coffee_query = {"query": {"term": {"name": "coffee"}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])

print_delimiter(2)
# 2. upravte dotaz tak, aby fungoval i v případě jednoho uživatelského překlepu• např. stejné výsledky pro ‚cofee‘ nebo ‚coffe‘ • co se stane po povolení více než jednoho překlepu?
coffee_query = {"query": {"fuzzy": {"name": {"value": "cofee", "fuzziness": "1"}}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])

coffee_query = {"query": {"fuzzy": {"name": {"value": "coffe", "fuzziness": "1"}}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])

coffee_query = {"query": {"fuzzy": {"name": {"value": "cofe", "fuzziness": "1"}}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])

print_delimiter(3)
# 3. vytvořte dotaz, který vyhledá produkty s tagem ‚Coffee‘ (term) • liší se počet výsledků? pokud ano, který název nenalezl první dotaz a proč?
coffee_query = {"query": {"term": {"tags": "Coffee"}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])
# vrátí 12, protože některé produkty mají tag Coffee, ale coffee není v názvu

print_delimiter(4)
# 4. najděte produkty s tagem ‚Coffee‘ s 10 nebo méně kusy na skladě (in_stock)
coffee_query = {
    "query": {
        "bool": {
            "must": [{"term": {"tags": "Coffee"}}, {"range": {"in_stock": {"lte": 10}}}]
        }
    }
}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(coffee_results["hits"]["total"]["value"])

print_delimiter(5)
# 5. najděte produkty, které v názvu mají ‚coffee‘, ale neobsahují ‚cup‘ • zobrazte jen názvy
coffee_query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"name": "coffee"}},
                {"bool": {"must_not": {"term": {"name": "cup"}}}},
            ]
        }
    },
    "_source": ["name"],
}
coffee_results = es.search(index="products", query=coffee_query["query"])
print([hit["_source"]["name"] for hit in coffee_results["hits"]["hits"]])

print_delimiter(6)
# 6. vyfiltrujte všechny produkty, které byly přidány po roce 2000 • nebudou skórovány
coffee_query = {"query": {"range": {"created": {"gte": "2000-01-01"}}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print(
    [
        hit["_source"]["name"] + " vytvoreno " + hit["_source"]["created"]
        for hit in coffee_results["hits"]["hits"]
    ]
)

print_delimiter(7)
# 7. full-textově vyhledejte produkty obsahující v názvu „Red Wine“
coffee_query = {"query": {"match": {"name": "Red Wine"}}}
coffee_results = es.search(index="products", query=coffee_query["query"])
print([hit["_source"]["name"] for hit in coffee_results["hits"]["hits"]])

print_delimiter(8)


# 8. vytvořte dotaz, který bude fungovat jako našeptávač při vyhledávání • začne vracet nejvíce relevantní výsledky během psaní • např. uživatel napíše pouze znak ‚c‘ a už jsou mu vráceny první výsledky • zadaný řetězec se může nacházet kdekoliv v názvu • doporučujte pouze 5 relevantních produktů • vyzkoušejte si postupně vyhledávat ‚c‘, ‚co‘, …, ‚coffee‘
def autocomplete_search(text):
    query = {
        "size": 5,
        "query": {
            "match_phrase_prefix": {
                "name": {
                    "query": text,
                }
            }
        },
    }
    response = es.search(index="products", query=query["query"], size=query["size"])
    # print(f"Výsledky pro '{text}':")
    hits = response["hits"]["hits"]
    for hit in hits:
        print(hit["_source"]["name"])


print_delimiter("pro autocomplete 'c'")
autocomplete_search("c")

print_delimiter("pro autocomplete 'co'")
autocomplete_search("co")

print_delimiter("pro autocomplete 'coffee'")
autocomplete_search("coffee")

print_delimiter(9)


# 9. vytvořte dotaz, který bude vracet recepty, v nichž se nachází libovolný výraz • hledaný výraz může být v nadpisu, popisu nebo ingrediencích receptu • např. spaghetti
def search_recipes(query):
    response = es.search(
        index="recipes",
        query={
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "ingredients.name"],
            }
        },
    )
    # print(f"Vyhledávání pro: {query}")
    for hit in response["hits"]["hits"]:
        print(hit["_source"]["title"])


print_delimiter("spaghetti")
search_recipes("spaghetti")

print_delimiter("pasta")
search_recipes("pasta")


print_delimiter(10)
# 10. vytvořte dotaz, který bude v názvu hledat frázi „Pasta Carbonara“ • kolik je výsledků? • dotaz rozšiřte o hledání v blízkosti, aby výsledkem byl i výraz „Carbonara Pasta“
text = "with pasta mushrooms"

word_list = text.split()
def permutations(word_list):
    if len(word_list) == 1:
        return [word_list]
    perms = []
    for i in range(len(word_list)):
        for perm in permutations(word_list[:i] + word_list[i + 1:]):
            perms.append([word_list[i]] + perm)
    return perms


def flexible_search(query):
    response = es.search(
        index="recipes",
        query={
            "bool": {
                "should": [
                    {"match_phrase": {"title": " ".join(permutation)}}
                    for permutation in permutations(query)
                ]
            }
        },
    )
    print(response["hits"]["total"]["value"])
    for hit in response["hits"]["hits"]:
        print(hit["_source"]["title"])

print_delimiter("Pasta Carbonara")
flexible_search(["Pasta", "Carbonara"])

print_delimiter("Carbonara Pasta")
flexible_search(["Carbonara", "Pasta"])

print_delimiter("with pasta mushrooms")
flexible_search(["with", "pasta", "mushrooms"])

print_delimiter("mushrooms pasta with")
flexible_search(["mushrooms", "pasta", "with"])