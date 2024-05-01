import redis


r = redis.Redis(host='localhost', port=6379, db=0)

# hraci
r.zadd('leaderboard', {'Hrac1': 750, 'Hrac2': 650, 'Hrac3': 890, 'Hrac4': 901, 'Hrac5': 901, 'Hrac6': 1000, 'Hrac7': 9, 'Hrac8': 680, 'Hrac9': 3, 'Hrac10': 889, 'Alfred': 888})

# top 3
top = r.zrevrange('leaderboard', 0, 2, withscores=True)
print("Top 3:")
for player, score in top:
    print(f"{player}: {score}")

# nejhorsi
spatny = r.zrange('leaderboard', 0, 0, withscores=True)
print(f"nejhorsi: {spatny[0][1]}")

# 100-
p100 = r.zcount('leaderboard', '-inf', 99)
print(f"Players with less than 100 points: {p100}")

# 850+
p850 = r.zrangebyscore('leaderboard', 851, '+inf', withscores=True)
print("850+:")
for player, score in p850:
    print(f"{player}: {score}")

vsichni = r.zrange('leaderboard', 0, -1, withscores=True)
print("Vsechny:")
for player, score in vsichni:
    print(f"{player}: {score}")

# Alfred
a = r.zrank('leaderboard', 'Alfred')
print(f"Alfred poyice: {a}")

# Alfred +12
r.zincrby('leaderboard', 12, 'Alfred')
a_novy = r.zrank('leaderboard', 'Alfred')
print(f"Nova pozice: {a_novy}")