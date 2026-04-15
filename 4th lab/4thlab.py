#%%
from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

# 1,2,16,17
class Player:
    def __init__(self, player_id: int, name: str, hp: int):
        self._id = player_id
        self._name = name.strip().title()
        self._hp = hp if hp >= 0 else 0
        self._inventory = Inventory()

    def __str__(self):
        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"

    def __del__(self):
        print(f"Player {self._name} удалён")

    @classmethod
    def from_string(cls, data: str):
        try:
            parts = data.strip().split(",")
            if len(parts) != 3:
                raise ValueError()
            return cls(int(parts[0]), parts[1], int(parts[2]))
        except:
            raise ValueError("Ошибка строки")

    @property
    def hp(self):
        return self._hp

    def change_hp(self, value):
        self._hp = max(0, self._hp + value)

    def get_inventory(self):
        return self._inventory

    #7
    def handle_event(self, event):
        if event.type == "ATTACK":
            damage = event.data.get("damage", 0)
            self.change_hp(-damage)
        elif event.type == "HEAL":
            heal = event.data.get("heal", 0)
            self.change_hp(heal)
        elif event.type == "LOOT":
            item = event.data.get("item")
            if item:
                self._inventory.add_item(item)


# добавили Warrior (минимально)
class Warrior(Player):
    pass


#3
class Item:
    def __init__(self, item_id: int, name: str, power: int):
        self.id = item_id
        self.name = name.strip()
        self.power = power

    def __str__(self):
        return f"Item(id={self.id}, name='{self.name}', power={self.power})"

    def __eq__(self, other):
        return isinstance(other, Item) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


#4
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        if not any(i.id == item.id for i in self.items):
            self.items.append(item)

    def remove_item(self, item_id: int):  # FIX
        self.items = [i for i in self.items if i.id != item_id]

    def get_items(self):
        return self.items

    def unique_items(self):
        return set(self.items)

    def to_dict(self):
        return {item.id: item for item in self.items}

    #5 FIX (перенесено внутрь класса)
    def get_strong_items(self, min_power):
        return list(filter(lambda x: x.power >= min_power, self.items))

    #18 FIX (перенесено сюда)
    def __iter__(self):
        return iter(self.items)


#6
class Event:
    def __init__(self, type_, data):
        self.type = type_
        self.data = data
        self.timestamp = datetime.now()  # FIX

    def __str__(self):
        return f"Event(type='{self.type}', data={self.data}, timestamp='{self.timestamp}')"


#8
class Logger:
    @staticmethod
    def log(event, player, filename):
        with open(filename, "a") as f:
            f.write(f"{event.timestamp};{player._id};{event.type};{event.data}\n")

#9
    @staticmethod
    def read_logs(filename):
        events = []
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                e = Event(parts[2], eval(parts[3]))
                events.append(e)
        return events


#10
class EventIterator:
    def __init__(self, events):
        self.events = events
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.events):
            raise StopIteration
        val = self.events[self.index]
        self.index += 1
        return val


#11
def damage_stream(events):
    for e in events:
        if e.type == "ATTACK":
            yield e.data.get("damage", 0)


#12
def generate_events(players, items, n):
    types = ["ATTACK", "HEAL", "LOOT"]

    events = []
    for _ in range(n):
        for p in players:
            t = random.choice(types)  # чуть проще

            if t == "ATTACK":
                events.append(Event(t, {"damage": random.randint(5, 20)}))
            elif t == "HEAL":
                events.append(Event(t, {"heal": random.randint(5, 15)}))
            else:
                events.append(Event(t, {"item": random.choice(items)}))

    return events


#13
def analyze_logs(events):
    total_damage = sum([e.data.get("damage", 0) for e in events if e.type == "ATTACK"])
    types = [e.type for e in events]
    most_common = max(set(types), key=types.count)

    return {
        "total_damage": total_damage,
        "most_common_event": most_common
    }


#14
decide_action = lambda p: "HEAL" if p.hp < 50 else "ATTACK"


#15
class Mage(Player):
    def handle_event(self, event):
        if event.type == "LOOT":
            item = event.data.get("item")
            if item:
                item.power = int(item.power * 1.1)
        super().handle_event(event)


#19
def analyze_inventory(inventories):
    all_items = [item for inv in inventories for item in inv]

    unique_items = set(all_items)
    top_item = max(all_items, key=lambda x: x.power)

    return {
        "unique_items": len(unique_items),
        "top_power": str(top_item)
    }


#20
@app.get("/")
def main():
    p1 = Warrior(1, "john", 100)
    p2 = Mage(2, "alice", 80)

    players = [p1, p2]

    items = [
        Item(1, "Sword", 50),
        Item(2, "Staff", 40)
    ]

    events = generate_events(players, items, 3)

    for e in events:
        for p in players:
            p.handle_event(e)

    for e in events:
        Logger.log(e, p1, "logs.txt")

    logs = Logger.read_logs("logs.txt")

    damages = list(damage_stream(logs))

    stats = analyze_logs(logs)

    inv_stats = analyze_inventory([p.get_inventory() for p in players])

    return {
        "players": [str(p) for p in players],
        "events_count": len(events),
        "damage_stream": damages,
        "stats": stats,
        "inventory_stats": inv_stats
    }
#%%