from init import collection

print(collection)
print(collection.find_one())
print(collection.count_documents({}))

"""
DPB - 5. Cvičení

Implementujte jednotlivé body pomocí PyMongo knihovny - rozhraní je téměř stejné jako v Mongo shellu.
Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru.

Pro pomoc je možné např. použít https://www.w3schools.com/python/python_mongodb_getstarted.asp

Funkce find vrací kurzor - pro vypsání výsledku je potřeba pomocí foru iterovat nad kurzorem:

cursor = collection.find(...)
for restaurant in cursor:
    print(restaurant) # případně print(restaurant['name'])

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!
"""


def print_delimiter(n):
    print("\n", "#" * 10, "Úloha", n, "#" * 10, "\n")


# 1. Vypsání všech restaurací
print_delimiter(1)
cursor = collection.find({}, {"name": 1, "_id": 1}).limit(10)
for restaurant in cursor:
    print(restaurant)


# 2. Vypsání všech restaurací - pouze názvů, abecedně seřazených
print_delimiter(2)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort("name", 1)
for restaurant in cursor.limit(10):
    print(restaurant)

# 3. Vypsání pouze 5 záznamů z předchozího dotazu
print_delimiter(3)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort("name", 1)
for restaurant in cursor.limit(5):
    print(restaurant)

# 4. Zobrazte dalších 10 záznamů
print_delimiter(4)
cursor = collection.find({}, {"name": 1, "_id": 0}).sort("name", 1)

for restaurant in cursor.skip(5).limit(10):
    print(restaurant)

# 5. #Vypsání restaurací ve čtvrti Bronx (čtvrť = borough)
print_delimiter(5)
cursor = collection.find(
    {"borough": "Bronx"}, {"name": 1, "_id": 0, "borough": 1}
).limit(10)
for restaurant in cursor:
    print(restaurant)

# 6. Vypsání restaurací, jejichž název začíná na písmeno M
print_delimiter(6)
cursor = collection.find({"name": {"$regex": "^M"}}, {"name": 1, "_id": 0}).limit(10)
for restaurant in cursor:
    print(restaurant)

# 7. Vypsání restaurací, které mají skóre větší než 80
print_delimiter(7)
cursor = collection.find(
    {"grades.score": {"$gt": 80}}, {"name": 1, "_id": 0, "grades.score": 1}
).limit(10)
for restaurant in cursor:
    print(restaurant)

# 8. Vypsání restaurací, které mají skóre mezi 80 a 90
print_delimiter(8)
cursor = collection.find(
    {"grades": {"$elemMatch": {"score": {"$gte": 80, "$lte": 90}}}},
    {"name": 1, "grades.score": 1, "cuisine": 1},
).limit(10)
for restaurant in cursor:
    print(restaurant)

"""
Bonusové úlohy:
"""

# 9. Vypsání všech restaurací, které mají skóre mezi 80 a 90 a zároveň nevaří americkou (American) kuchyni
print_delimiter(9)
cursor = collection.find(
    {
        "$and": [
            {"grades": {"$elemMatch": {"score": {"$gte": 80, "$lte": 90}}}},
            {"cuisine": {"$ne": "American"}},
        ]
    },
    {"name": 1, "grades.score": 1, "cuisine": 1},
)
for restaurant in cursor.limit(10):
    print(restaurant)

# 10. Vypsání všech restaurací, které mají alespoň osm hodnocení
print_delimiter(10)
cursor = collection.find(
    {"grades": {"$size": 8}}, {"name": 1, "grades.date": 1}
)
for restaurant in cursor.limit(10):
    print(restaurant, "\n")

# 11. Vypsání všech restaurací, které mají alespoň jedno hodnocení z roku 2014
import datetime
print_delimiter(11)
# cursor = collection.find(
#     {"grades.date": {"$regex": "2014"}}, {"name": 1, "grades.date": 1}
# )
cursor = collection.find({"grades.date": {"$gte": datetime.datetime(2014, 1, 1), "$lt": datetime.datetime(2015, 1, 1)}})
for restaurant in cursor.limit(10): 
    print(restaurant, "\n")

"""
V této části budete opět vytvářet vlastní restauraci.

Řešení:
Vytvořte si vaši restauraci pomocí slovníku a poté ji vložte do DB.
restaurant = {
    ...
}
"""

# 12. Uložte novou restauraci (stačí vyplnit název a adresu)
print_delimiter(12)
restaurant = {
    "name": "My Restaurant",
    "address": {
        "street": "My Street",
    }
}
collection.insert_one(restaurant)

# 13. Vypište svoji restauraci
print_delimiter(13)
cursor = collection.find({"name": "My Restaurant"})
for restaurant in cursor:
    print(restaurant)

# 14. Aktualizujte svoji restauraci - změňte libovolně název
print_delimiter(14)
collection.update_one({"name": "My Restaurant"}, {"$set": {"name": "My New Restaurant"}})


# 15. Smažte svoji restauraci
print_delimiter(15)
# 15.1 pomocí id (delete_one)
for restaurant in cursor:
    collection.delete_one({"_id": restaurant["_id"]})
    collection.delete_many({"$or": [{"name": "My Restaurant"}, {"name": "My New Restaurant"}]})

# 15.2 pomocí prvního nebo druhého názvu (delete_many, využití or)
cursor = collection.find({"name": "My Restaurant"})
for restaurant in cursor:
    collection.delete_one({"_id": restaurant["_id"]})


"""
Poslední částí tohoto cvičení je vytvoření jednoduchého indexu.

Použijte např. 3. úlohu s vyhledáváním čtvrtě Bronx. První použijte Váš již vytvořený dotaz a na výsledek použijte:

cursor.explain()['executionStats'] - výsledek si vypište na výstup a všimněte si položky 'totalDocsExamined'

Poté vytvořte index na 'borough', zopakujte dotaz a porovnejte hodnoty 'totalDocsExamined'.

S řešením pomůže https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
"""
print_delimiter(16)
    
collection.drop_indexes()

print_delimiter("Před vytvořením indexu")
explanation = collection.find({"borough": "Bronx"}).explain()['executionStats']
print(f"Total documents examined: {explanation['totalDocsExamined']}")

collection.create_index([("borough", 1)])

print_delimiter("Po vytvoření indexu")
explanation = collection.find({"borough": "Bronx"}).explain()['executionStats']
print(f"Total documents examined: {explanation['totalDocsExamined']}")
