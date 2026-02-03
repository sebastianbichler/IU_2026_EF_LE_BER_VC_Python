from pymongo import MongoClient
from datetime import datetime

# Подключаемся к Atlas
client = MongoClient("mongodb+srv://admin:<db_password>@cluster0.f4xszpo.mongodb.net/?appName=Cluster0")
db = client.football_db  # имя базы

# Игры
db.games.insert_one({
    "_id": "game1",
    "team_1_id": "team1",
    "team_2_id": "team2",
    "competition_id": "comp1",
    "start_date": datetime(2026,2,3,15,0),
    "end_date": datetime(2026,2,3,17,0)
})

# Карточки
db.cards.insert_one({
    "game_id": "game1",
    "player_id": "player1",
    "color": "yellow",
    "time": datetime(2026,2,3,15,30)
})

# Голы
db.goals.insert_one({
    "game_id": "game1",
    "player_id": "player1",
    "team_id": "team1",
    "time": datetime(2026,2,3,15,45)
})

print("Seed completed!")
