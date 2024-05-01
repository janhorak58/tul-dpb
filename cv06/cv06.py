from init import collection

'''
DPB - 6. cvičení - Agregační roura a Map-Reduce

V tomto cvičení si můžete vybrat, zda ho budete řešit v Mongo shellu nebo pomocí PyMongo knihovny.

Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru - používáme stejná data jako v minulých cvičeních.

Pro pomoc je možné např. použít https://api.mongodb.com/python/current/examples/aggregation.html a přednášku.

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!

Struktura záznamu v db:
{
  "address": {
     "building": "1007",
     "coord": [ -73.856077, 40.848447 ],
     "street": "Morris Park Ave",
     "zipcode": "10462"
  },
  "borough": "Bronx",
  "cuisine": "Bakery",
  "grades": [
     { "date": { "$date": 1393804800000 }, "grade": "A", "score": 2 },
     { "date": { "$date": 1378857600000 }, "grade": "A", "score": 6 },
     { "date": { "$date": 1358985600000 }, "grade": "A", "score": 10 },
     { "date": { "$date": 1322006400000 }, "grade": "A", "score": 9 },
     { "date": { "$date": 1299715200000 }, "grade": "B", "score": 14 }
  ],
  "name": "Morris Park Bake Shop",
  "restaurant_id": "30075445"
}
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')


'''
Agregační roura
Zjistěte počet restaurací pro každé PSČ (zipcode)
 a) seřaďte podle zipcode vzestupně
 b) seřaďte podle počtu restaurací sestupně
Výpis limitujte na 10 záznamů a k provedení použijte collection.aggregate(...)
'''
print_delimiter('1 a)') 
results = collection.aggregate([
        {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$limit": 10}
])
for result in results:
   print(result)


print_delimiter('1 b)') 
results = collection.aggregate([
   {"$group": {"_id": "$address.zipcode", "count": {"$sum": 1}}},
   {"$sort": {"count": -1}},
   {"$limit": 10}
])
for result in results:
   print(result)
'''
Agregační roura

Restaurace obsahují pole grades, kde jsou jednotlivá hodnocení. Vypište průměrné score pro každou hodnotu grade.
V agregaci vynechte grade pro hodnotu "Not Yet Graded" (místo A, B atd. se může vyskytovat tento řetězec).

'''
print_delimiter(2) 
results = collection.aggregate([
   {"$unwind": "$grades"},
   {"$match": {"grades.grade": {"$ne": "Not Yet Graded"}}},
   {"$group": {"_id": "$grades.grade", "average_score": {"$avg": "$grades.score"}}},
   {"$sort": {"average_score": -1}},
   {"$limit": 10}
])
for result in results:
   print(result)


print_delimiter("BONUS 1")
results = collection.aggregate([
   {"$unwind": "$grades"},
   {"$match": {"grades.grade": "A"}},
   {"$group": {
      "_id": "$restaurant_id",
      "averageScore": {"$avg": "$grades.score"},
      "count": {"$sum": 1}
   }},
   {"$match": {"count": {"$gte": 3}}},
   {"$sort": {"averageScore": -1}},
   {"$limit": 5}
])

for result in results:
   print(f"ID: {result['_id']}, Prumerne Score: {result['averageScore']}, Pocet 'A': {result['count']}")

print_delimiter("BONUS 2")

results = collection.aggregate([
        {"$unwind": "$grades"},
        {"$match": {"grades.grade": "A"}},
        {"$group": {
            "_id": {"cuisine": "$cuisine", "restaurant_id": "$restaurant_id"},
            "averageScore": {"$avg": "$grades.score"},
            "count": {"$sum": 1}
        }},
        {"$match": {"count": {"$gte": 3}}},
        {"$sort": {"_id.cuisine": 1, "averageScore": -1}},
        {"$group": {
            "_id": "$_id.cuisine",
            "cuisine": {"$first": "$_id.cuisine"},
            "restaurant_id": {"$first": "$_id.restaurant_id"},
            "averageScore": {"$first": "$averageScore"}
        }},
        {"$sort": {"averageScore": -1}},
        {"$limit": 10}
    ])

for result in results:
        print(f"Kuchyn: {result['_id']}, ID restaurace: {result['restaurant_id']}, Nejvyssi skore: {result['averageScore']}")



print_delimiter("BONUS 3")

results = collection.aggregate([
   {"$match": {"name": {"$regex": "\\s"}}},
   {"$unwind": "$grades"},
   {"$group": {
      "_id": "$_id",
      "name": {"$first": "$name"},
      "count": {"$sum": 1},
      "high_scores": {"$sum": {"$cond": [{"$gt": ["$grades.score", 10]}, 1, 0]}}
   }},
   {"$match": {"count": {"$gte": 2}, "high_scores": {"$gte": 2}}},
   {"$limit": 10}
])

for result in results:
   print(f"Jmeno: {result['name']}, Pocet hodnoceni: {result['count']}, Pocet hodnoceni > 10: {result['high_scores']}")