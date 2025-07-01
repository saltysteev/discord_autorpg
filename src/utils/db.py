"""
db.py
"""

import random
from datetime import datetime

import databases
import ormar
import sqlalchemy

from utils.config import DEBUG, DBTYPE, DBUSER, DBPASS, DBHOST, DBPORT, DBNAME

DBSTRING = f"{DBTYPE}://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"

metadata = sqlalchemy.MetaData()
database = (
    databases.Database(DBSTRING, force_rollback=True)
    if DEBUG
    else databases.Database(DBSTRING)
)
engine = sqlalchemy.create_engine(DBSTRING)
basemeta = ormar.OrmarConfig(
    database=database,
    metadata=metadata,
    engine=engine,
)


class Quest(ormar.Model):
    ormar_config = basemeta.copy(tablename="quests")

    qid: int = ormar.Integer(primary_key=True)
    players: str = ormar.Text()
    goal: str = ormar.Text()
    endxp: int = ormar.Integer()
    currentxp: int = ormar.Integer()
    deadline: int = ormar.Integer()


class Player(ormar.Model):
    ormar_config = basemeta.copy(tablename="users")

    uid: int = ormar.BigInteger(primary_key=True)
    name: str = ormar.String(max_length=100)
    level: int = ormar.Integer(default=1)
    job: str = ormar.String(max_length=100, default="Novice")
    align: int = ormar.Integer(default=0)
    nextxp: int = ormar.Integer(default=600)
    currentxp: int = ormar.Integer(default=0)
    totalxp: int = ormar.Integer(default=0)
    totalxplost: int = ormar.Integer(default=0)
    online: bool = ormar.Boolean(default=True)
    created: int = ormar.Integer(default=int(datetime.today().timestamp()))
    lastlogin: int = ormar.Integer(default=int(datetime.today().timestamp()))
    x: int = ormar.Integer(default=random.randint(1, 1000))
    y: int = ormar.Integer(default=random.randint(1, 1000))
    wins: int = ormar.Integer(default=0)
    loss: int = ormar.Integer(default=0)
    totalquests: int = ormar.Integer(default=0)
    onquest: bool = ormar.Boolean(default=False)
    qid: int = ormar.Integer(default=0)
    bid: int = ormar.BigInteger(default=0)
    optin: bool = ormar.Boolean(default=False)
    avatar_url: str = ormar.Text(default="")
    weapon: str = ormar.JSON(
        default={
            "name": "Fists",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 20,
            "rank": "Common",
            "flair": None,
        }
    )
    shield: str = ormar.JSON(
        default={
            "name": "Wooden Plank",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    helmet: str = ormar.JSON(
        default={
            "name": "Iron Helmet",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    chest: str = ormar.JSON(
        default={
            "name": "Rags",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    gloves: str = ormar.JSON(
        default={
            "name": "Wraps",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    boots: str = ormar.JSON(
        default={
            "name": "Clogs",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    ring: str = ormar.JSON(
        default={
            "name": "Iron Ring",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )
    amulet: str = ormar.JSON(
        default={
            "name": "Iron Necklace",
            "quality": "Basic",
            "condition": "Dusty",
            "prefix": "",
            "suffix": "",
            "dps": 10,
            "rank": "Common",
            "flair": None,
        }
    )


async def database_init(guild):
    # Database creation if not exists
    basemeta.metadata.create_all(engine)
    for player in guild.members:
        await Player.objects.get_or_create(
            uid=player.id,
            _defaults={"name": player.display_name},
        )
