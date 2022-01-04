#!/usr/bin/env python3

import csv
import os
import math
import random
import tabulate
import time

global inventory
global area_container
global loot

hero_loc = 0,0
count=0

def initialize():
    pass

def help():
    print("RPGF!  So great!  Many wow!\n")
    print("Available games:\n")
    print("qpb(c): Quick Party Battle (characters per party)")
    print("qpb2(c): Quick Party Battle 2 (characters per party)")
    print("hvm(h,m,t): Hero vs Mobs (heroes,mobs,team name)")
    print("chvm(m): Continue Hero vs Mobs (mobs)")
    print("dung(): Random Dungeon")
    
    




# ------------------------------- #
#            Databases            #
# ------------------------------- #


inventory = []
area_container = []
loot = []
roster = []
cartographer = []

roster2 = {
    "free": [],
    "parties": []
}


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


names = ["Alfred","Burt","Charlie","Dave","Erik","Frank","Gary","Herbert","Isaac","Jones","Keith",
        "Lars","Mike","Nigel","Omar","Pete","Quixote","Ryan","Steve","Tom","Uganda","Victor",
        "Walter","Xavier","Yankee","Zulu","Fry","Leela","Bender","Farnsworth","Hermes","Amy",
        "Donbot","Clamps","Joey Mouse-Pad","Calculon","Flexo","Wernstrom","Pazuzu","Zoidberg",
        "Kif","Zapp","Scruffy","Clarkson","Hammond","May","Stig","Frodo","Samwise","Merry",
        "Pippin","Gandalf","Aragorn","Gimli","Legolas","Boromir","Faramir","Denethor",
        "Theoden","Wormtongue","Sauramon","Sauron","Bilbo","Elrond","Galadriel","Harry",
        "Ronald","Hermione","Hagrid","Severus","Remus","Lily","James","Voldemort","Malfoy",
        "Bellatrix","Dumbeldore","Flickwit","Nick","McGonagall","Liszt","Brahms","Bach",
        "Beethoven","Mozart","Tsiachovsky","Tracer","Winston","Reaper","Widowmaker","Lucio",
        "Baptiste","Torbjorn","Sombra","Zarya","D.Va","Junkrat","Roadhog","Hanzo","Genji"]

party_names = ["Opel","VW","McLaren","Mastretta","Honda","Toyota","Nissan","Chrysler","Ford",
              "Dodge","Lotus","Ferrari","Lancia","Dacia","Renault","Peugot","Citroen","Skoda",
              "Audi","BMW","Mercedes","Porsche","Mini","Tesla","Alfa-Romeo","Acura","Buick",
              "Bentley","Bugatti","Aston-Martin","Cadillac","Fiat","GMC","Kia","Jaguar",
              "Hyundai","Infiniti","Jeep","Lexus","Lincoln","Maserati","Mazda","Mitsubishi",
              "Pagani","Pontiac","Rolls-Royce","Subaru","Vauxhall","Volvo"]



#Attack_Name,Damage_Multiplier,Stamina_Cost,Damage_Type("" for none)

class attack_list:
    t0 = [
        ["Attack",1,-1,""],
        ["Smash",1.6,8,""]
    ]
    t1 = [
        ["Burn",1.6,12,"fire"],
        ["Freeze",1.6,12,"ice"],
        ["Zap",1.6,12,"electricity"]
    ]
    t2 = [
        ["Blight",1.8,20,"dark"],
        ["Frenzy",2,24,""],
        ["Impale",1.6,20,"physical"],
        ["Firestorm",2,24,"fire"],
        ["Blizzard",2,24,"ice"],
        ["Thunderstorm",2,24,"electricity"]
    ]
    t3 = [
        ["Aggression",2.5,30,""],
        ["Berserk",2,30,"physical"],
        ["Fireblast",2.25,30,"fire"],
        ["Iceblast",2.25,30,"ice"],
        ["Thunderblast",2.25,30,"electricity"]
    ]


#Example weapon dict for reference:
#["Old Sword",2,1,2,[2,6,"physical"]],    
enchantments = [
    [" of Pain",1,10,1,[3,3,""]],
    [" of Extremes",1,10,1,[-4,6,""]],
    [" of Fire",1,10,1,[1,3,"fire"]],
    [" of Ice",1,10,1,[2,2,"ice"]],
    [" of Shock",1,10,1,[0,4,"electricity"]],
    [" of Darkness",1,10,1,[1,2,"dark"]],
    [" of Precision",1,10,1,[5,0,""]]
]


class arsenal:
    t0 = {
    "right_hand": [
        ["Broken Sword",2,1,2,[0,4,"physical"]],
        ["Rusty Axe",2,1,2,[-1,5,"physical"]],
        ["Bent Spear",2,1,2,[1,3,"physical"]]
    ],
    "left_hand": [
        ["Moldy Buckler",2,1,3,[2,0,0,0]],
        ["Wood Plank",2,1,3,[1,0,0,0]],
        ["",0,0,0,[0,0,0,0]]
    ],
    "armor": [
        ["Tattered Clothes",2,5,4,[1,0,0,0]],
        ["Old Tunic",2,5,4,[1,0,0,0]],
        ["Brittle Chainmail",2,5,4,[2,0,0,0]]
    ],
    "helmet": [
        ["Goblin Skull",2,5,5,[1,0,0,0]],
        ["Dented Cap",2,5,5,[1,0,0,0]],
        ["",0,0,0,[0,0,0,0]]
    ]
    }
    t1 = {
    "right_hand": [
        ["Small Sword",2,1,2,[2,6,"physical"]],
        ["Hand Axe",2,1,2,[1,7,"physical"]],
        ["Short Spear",2,1,2,[3,5,"physical"]]
    ],
    "left_hand": [
        ["Old Buckler",2,5,3,[5,0,0,0]],
        ["Worn Small Shield",2,5,3,[5,0,0,0]],
        ["Rusted Round Shield",2,5,3,[10,0,0,0]],
        ["Tattered Ward",2,5,3,[0,5,5,5]],
        ["Fire Buckler",2,5,3,[5,10,0,0]]
    ],
    "armor": [
        ["Ragged Leather Armor",2,5,4,[5,0,0,0]],
        ["Dented Bronze Cuirass",2,5,4,[10,0,0,0]],
        ["Rusted Chainmail",2,5,4,[10,0,0,0]],
        ["Tattered Robes",2,5,4,[0,10,10,10]],
        ["Frozen Cuirass",2,5,4,[5,0,10,0]]
    ],
    "helmet": [
        ["Dusty Skull Cap",2,5,5,[5,0,0,0]],
        ["Frayed Coif",2,5,5,[5,0,0,0]],
        ["Rusted Bascinet",2,5,5,[10,0,0,0]],
        ["Tattered Hood",2,5,5,[0,10,10,10]],
        ["Electric Mohawk",2,5,5,[5,0,0,10]]
    ]
    }


class bestiary:
    t0 = [
        {
            "name": "Goblin Whelp",
            "class": "Humanoid",
            "faction": "Savage",
            "coins": random.randrange(3,6),
            "max_health": 4,
            "max_stamina": 0,
            "strength": 1,
            "dexterity": -1,
            "intelligence": -2,
            "backpack": [],
            "right_hand": [random.choice(arsenal.t0["right_hand"])],
            "left_hand": [random.choice(arsenal.t0["left_hand"])],
            "armor": [random.choice(arsenal.t0["armor"])],
            "helmet": [random.choice(arsenal.t0["helmet"])],
            "attacks": [attack_list.t0[0],attack_list.t0[1]]
        },
        {
            "name": "Wolfdog Runt",
            "class": "Beast",
            "faction": "Wild",
            "coins": 0,
            "max_health": 3,
            "max_stamina": 0,
            "strength": 3,
            "dexterity": -1,
            "intelligence": -2,
            "backpack": [],
            "right_hand": [["Claws",2,1,2,[0,2,"physical"]]],
            "left_hand": [["",0,0,0,[0,0,0,0]]],
            "armor": [["Thick Fur",0,0,0,[5,0,0,0]]],
            "helmet": [["",0,0,0,[0,0,0,0]]],
            "attacks": [attack_list.t0[0],attack_list.t0[1]]
        },
        {
            "name": "Orc Whelp",
            "class": "Humanoid",
            "faction": "Savage",
            "coins": random.randrange(5,9),
            "max_health": 6,
            "max_stamina": 6,
            "strength": 2,
            "dexterity": -1,
            "intelligence": -2,
            "backpack": [],
            "right_hand": [random.choice(arsenal.t0["right_hand"])],
            "left_hand": [random.choice(arsenal.t0["left_hand"])],
            "armor": [random.choice(arsenal.t0["armor"])],
            "helmet": [random.choice(arsenal.t0["helmet"])],
            "attacks": [attack_list.t0[0],attack_list.t0[1]]
        }
    ]
    t1 = [
        {
            "name": "Goblin Shaman",
            "class": "Humanoid",
            "faction": "Savage",
            "coins": random.randrange(6,12),
            "max_health": 12,
            "max_stamina": 0,
            "strength": 2,
            "dexterity": -1,
            "intelligence": 2,
            "backpack": [],
            "right_hand": [random.choice(arsenal.t0["right_hand"])],
            "left_hand": [random.choice(arsenal.t0["left_hand"])],
            "armor": [random.choice(arsenal.t0["armor"])],
            "helmet": [random.choice(arsenal.t0["helmet"])],
            "attacks": [attack_list.t0[0],attack_list.t0[1],random.choice(attack_list.t1)]
            
        }
    ]
    
    
dungeons = [
    {
        "name": "Spooky Village",
        "short_desc": "A foggy village with strange creatues.",
        "long_desc": "Deep in the desolate countryside of Nirn, a foggy village sits quietly, though some say that at night, strange creatues prowl the grounds.",
        "events": [
            "The party approaches the village, feeling confident, when suddenly, enemies!!",
            "The party moves further on, and when passing a house, notices a shape move!!",
            "The party nears the center of the village, but there is something in the way!!",
            "At the town square, the party is treated to a ghastly sight!!"
        ],
        "fail": "The party collapses the the ground, overwhelmed by the dark forces.\n" +
        "Soon, their corpses will fade, but their sould will be forever trapped here.\n",
        "win": "Triumphantly, the party emerges from the fog, having defeated the evil " +
        "that lived within.\nPerhaps things will return to normal... for a while.\n"
    },
    {
        "name": "Swamp",
        "short_desc": "A misty swamp with mushrooms and trees.",
        "long_desc": "Not far from Highway 1 is a mysterious swamp where the trees walk.",
        "events": ["Hey look a rock", "Hey look a tree", "Hey look a branch"],
        "fail": "Damn dude, you messed up.",
        "win": "Dude.  You made it.\nNice."
    },
    
]
    
    
    

def party():
    return {
        "Name": "default",
        "Faction": "default",
        "Battles": 0,
        "Members": []
    }


## NOT IN USE YET ##
## WILL ALLOW CUSTOM DAMAGE TYPES ##
def resistance(name,value):
    return {
        name: value
    }








# ------------------------------- #
#         Container Stuff         #
# ------------------------------- #
    
def item_to_drop(item):
    area_container.append(item)
    inventory.remove(item)
    
def item_to_pick_up(item):
    inventory.append(item)
    area_container.remove(item)
    
def dump_inventory():
    area_container.extend(inventory)
    inventory.clear()
        
def dump_backpack_of(character):
    area_container.extend(character["backpack"])
    character["backpack"].clear()
        
def loot_drop():
    area_container.extend(loot)
    loot.clear()
        
def loot_all():
    inventory.extend(area_container)
    area_container.clear()
    
def loot_all_to(character):
    items_looted = 0
    for item in area_container:
        items_looted += 1
    character["backpack"].extend(area_container)
    area_container.clear()
    return(print("Looted {} items!".format(items_looted)))
    
def loot_drop_all_from(character):
    area_container.extend(character["backpack"])
    character["backpack"].clear()
    
def loot_to(character,item):
    character["backpack"].append(item)
    area_container.remove(item)
    
def loot_drop_from(character,item):
    area_container.append(item)
    character["backpack"].remove(item)
    
def loot_trade(sender,receiver,item):
    receiver["backpack"].append(item)
    sender["backpack"].remove(item)
    
def equip_right_hand(character,item):
    if len(character["equipment"]["right_hand"]) == 0:
        character["equipment"]["right_hand"].append(item)
        character["backpack"].remove(item)    
    else: 
        print("Error! Already equipped")
    
def unequip_right_hand(character):
    try:
        character["backpack"].append(character["equipment"]["right_hand"][0])
        character["equipment"]["right_hand"].remove(character["equipment"]["right_hand"][0])
    except:
        print("Already unequipped!")
        
def quick_equip(character):
    character["backpack"].append(["Sword",2,5,2])
    character["equipment"]["right_hand"].clear()
    try:
        equip_right_hand(character,["Sword",2,5,2])
        print("Sword equipped!")
    except:
        print("Something went wrong! Can't equip!")
    try:
        character["backpack"].remove(["Sword",2,5,2])
    except:
        pass
    
def show_inventory():
    print("Inventory:")
    print(inventory)
    print("\n")
    
def list_inventory():
    for item in inventory:
        print(item)
    
def show_area_container():
    print("Area Container:")
    print(area_container)
    print("\n")
    
def show_loot():
    print("Loot:")
    print(loot)
    print("\n")    
    
def show_containers():
    show_inventory()
    show_area_container()
    show_loot()
    
def loot_bag():
    loot.append(["Rock",1,2,1])
    loot.append(["Stick",2,1,1])
    loot.append(["Sword",2,5,2])
    
def inventory_weight():
    weight = 0
    value = 0
    for item in inventory:
        weight += item[1]
        value += item[2]
    print("*Total items: " +str(len(inventory)))
    print("*Total weight: " + str(weight))
    print("*Total value: " +str(value))
    print("Loot list: ")
    for item in inventory:
        print(item)
        
def inventory_weight_of(character):
    weight = 0
    value = 0
    for item in character["backpack"]:
        weight += item[1]
        value += item[2]
    print("*Total items: " +str(len(character["backpack"])))
    print("*Total weight: " + str(weight) + " kg")
    print("*Total value: " +str(value) + " coins")
    print(color.UNDERLINE+"Loot list:"+color.END)
    show_inv_items(character)
    
def loot_test():
    loot_bag()
    loot_drop()
    print("Created and dropped loot!")
    
def sell_all_from(character):
    value=0
    total_value=0
    items_sold=0
    for item in character["backpack"]:
        items_sold += 1
        value = item[2]
        total_value += value
        character["coins"] += value
    character["backpack"].clear()
    return(print("Sold {} items for {} coins!".format(items_sold,total_value)))
        
        
def show_inv_items(character):
    headers = ["Item Name","Weight","Value","Type"]
    table = []
    for item in character["backpack"]:
        table.append(item)
        
    print(tabulate.tabulate(table,headers))
            
    
    

    
    
    
    
# ------------------------------- #
#         Character Stuff         #
# ------------------------------- #



def new_character(default_name):   
    character = {        
        "id": "",
        "name": default_name,
        "class": "Peasant",
        "level": 0,
        "xp": 0,
        "coins": random.randrange(5,16),
        "health": 15,
        "max_health": 15,
        "stamina": 10,
        "max_stamina": 10,
        "strength": 1,
        "dexterity": 1,
        "intelligence": 1,
        "right_hand": [["Sharp Stick",2,1,2,[1,3,"physical"]]],
        "left_hand": [["Broke Shield",2,5,3,[2,0,0,0]]],
        "armor": [["Scuffed Cuirass",2,5,4,[3,0,0,0]]],
        "helmet": [["Cap",2,5,5,[2,0,0,0]]],
        "backpack": [[default_name+"'s Journal",1,1,1]],
        "attacks": [attack_list.t0[0],attack_list.t0[1]]
    }
    register_character(character)
    equip_character(character)

    
def register_character(character):
    roster.append(character)
    
    
def clear_equipment(character):
    character["right_hand"].clear()
    character["left_hand"].clear()
    character["armor"].clear()
    character["helmet"].clear()
    
    
def equip_character(character):
    clear_equipment(character)
    character["right_hand"].append(random.choice(arsenal.t1["right_hand"]))
    character["left_hand"].append(random.choice(arsenal.t1["left_hand"]))
    character["armor"].append(random.choice(arsenal.t1["armor"]))
    character["helmet"].append(random.choice(arsenal.t1["helmet"]))
    
    
def build_character(default_name):
    try:
        new_character(default_name)
    except:
        print("Error!  Couldn't build character!")

    
def clear_roster():
    try:
        roster.clear()
        print("Roster cleared!")
    except:
        print("Something went wrong!")

        
def show_character(character):
    print("\n\033[1m-- Info --\033[0m")
    try:
        #print(roster.index(character))
        print("id: " + str(roster.index(character)))
    except:
        pass
    print("Name: " + character["name"])
    print("Class: " + character["class"])
    print("Level: " + str(character["level"]))
    print("XP: " + str(character["xp"]))
    print("Coins: " + str(character["coins"]) + "\n")
    print("\033[1m-- Stats: --\033[0m")
    print("Health: {} / {}".format(str(character["health"]),str(character["max_health"])))
    print("Stamina: {} / {}".format(str(character["stamina"]),str(character["max_stamina"])))
    print("Strength: " + str(character["strength"]))
    print("Dexterity: " + str(character["dexterity"]))
    print("Intelligence: " + str(character["intelligence"]))
    print("\n\033[1m-- Backpack: --\033[0m")
    try:
        inventory_weight_of(character)
    except:
        print("Something wrong with the backpack! Printing items manually:")
        try:
            for item in character["backpack"]:
                print(item)
        except:
            print("That didn't work either!!")
    #for item in character["backpack"]:
    #    print(item)
    print("\n\033[1m-- Equipment: --\033[0m")
    print("Right Hand: " + str(character["right_hand"]))
    print("Left Hand: " + str(character["left_hand"]))
    print("Armor: " + str(character["armor"]))
    print("Helmet: " + str(character["helmet"]))
    print("\n\033[1m-- Resistances: --\033[0m")
    calc_armor(character)
    print("\n\033[1m-- Attacks: --\033[0m")
    try:
        show_attacks(character)
    except:
        print("Something went wrong!")
    print("\n")
        
        
    #save_roster almost works
def save_roster():
    filename = "roster.sav"
    keys=['id','name','class','level','xp','coins','health','max_health','stamina','max_stamina',
          'strength','dexterity','intelligence','right_hand','left_hand','armor',
          'helmet','backpack']
    with open(filename,"w") as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(roster)
    
    
    #save_roster2 almost works
def save_roster2():
    filename = "roster2.sav"
    keys=['id','name','class','level','xp','coins','health','max_health','stamina',
          'max_stamina','strength','dexterity','intelligence','right_hand','left_hand','armor',
          'helmet','backpack']
    with open(filename,"w") as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        for character in roster:
            writer.writerow(character)
    
    
    #load_roster almost works
def load_roster(filename):
    clear_roster()
    keys=['id','name','class','level','xp','coins','health','max_health','stamina','max_stamina',
          'strength','dexterity','intelligence','right_hand','left_hand','armor',
          'helmet','backpack']
    input_file=csv.DictReader(open(filename))
    print("\nReading file...:\n")
    for row in input_file:
        print(row)
        print("\n")
        roster.append(row)
    
    print("\nFinished reading file\n")    
            
            
def show_roster():
    print("\n--------------------\n")
    print("       ROSTER")
    print("{} characters present".format(len(roster)))
    print("\n--------------------\n")
    for character in roster:
        try:
            show_character(character)
            print("\n------------\n")
        except:
            print("Something went wrong!  Printing file:\n")
            print(roster)
        
        
def show_attacks(character):
    for attack in character["attacks"]:
        if attack[3] == "":
            print("%-15s %-5s damage  %10s stamina" % (
                attack[0],
                str(int(attack[1]*100)) + "%",
                attack[2]
            ))
        else:
            print("%-15s %-5s %-12s  %4s stamina" % (
                attack[0],
                str(int(attack[1]*100)) + "%",
                attack[3],
                attack[2]
            ))


def test_level(level):
    clear_roster()
    name = random.choice(names)
    build_character(name)
    print("Built character...")
    difference = level - roster[0]["level"]    
    print("-- Scaling level...")
    for rep in range(0,difference):
        level_up(roster[0])
    print("-- Level scaled!\n")
    show_roster()            


def new_party(members):
    newparty = {
    "name": random.choice(party_names),
    "faction": "default",
    "battles": 0,
    "members": []
    }
    if members > len(roster):
        difference = members - len(roster)
        for count in range(0,difference):
            new_character(random.choice(names))
    #Should have enough characters in roster to fill party
    count = 0
    for count in range(0,members):
        newparty["members"].append(roster[0])
        roster.remove(roster[0])
    roster2["parties"].append(newparty)
    print("Created new party!")
    show_party(newparty)
    

def augment_party(members):
    party = roster2["parties"][0]
    for count in range(0,members):
        new_character(random.choice(names))
        party["members"].append(roster[0])
        roster.remove(roster[0])
    print("Reinforced party with {} new members!".format(members))
    show_party(party)
    
        
def new_mob(mob):
    mobcopy = mob.copy()   
    character = {        
        "id": "",
        "level": 0,
        "xp": 0,
        "health": mobcopy["max_health"],
        "stamina": mobcopy["max_stamina"]
    }
    character.update(mobcopy)    
    register_character(character)
        
        
def build_mob():
    new_mob(random.choice(list(bestiary.t0)))
    

def new_mob_party(members):
    newparty = {
    "name": random.choice(party_names),
    "faction": "default",
    "battles": 0,
    "members": []
    }
    count = 0
    if members > len(roster):
        difference = members - len(roster)
        for count in range(0,int(difference)):
            build_mob()
    #Should have enough characters in roster to fill party
    count = 0
    for count in range(0,members):
        newparty["members"].append(roster[0])
        #print("Added {} to the party".format(roster[0]["name"]))
        roster.remove(roster[0])
    roster2["parties"].append(newparty)
    #print("Created new party!")
    assign_party_name(newparty)
    #show_party(newparty)
    
    
def show_party(party):
    print("\nTeam {}: {} battles, {} members:".format(
        party["name"],str(party["battles"]),str(len(party["members"]))
    ))
    #headers = ["name","level","health","max_health"]
    #table = []
    for character in party["members"]:
        print(character["name"] + ", Level " + str(character["level"]))
    print("\n")    
    
    
def show_parties():
    print("\nTotal parties: "+str(len(roster2["parties"]))+"\n")
    for party in roster2["parties"]:
        show_party(party)
    
    
def assign_party_name(party):
    faction_names = []
    for character in party["members"]:
        faction_names.append(character["class"])
    party["name"] = random.choice(faction_names)


def create_foes():
    for name in names:
        build_character(name)


def quick_parties(members):
    new_party(members)
    new_party(members)
    
    
def hero_party(heroes):
    roster2["parties"].clear()
    new_party(heroes)
    
    
def mob_party(mobs):
    new_mob_party(mobs)
    
    
def hero_v_mobs_parties(heroes,mobs):
    hero_party(heroes)
    new_mob_party(mobs)
    
    
    
    
        
        
        
# ------------------------------- #
#           Combat Stuff          #
# ------------------------------- #


        
def calc_damage(character):
    strength = character["strength"]
    min_damage = (character["right_hand"][0][4][0] + strength)
    max_damage = (character["right_hand"][0][4][1] + strength)
    damage_type = character["right_hand"][0][4][2]
    #print("{} - {} {} damage".format(min_damage,max_damage,damage_type))
    
    
def calc_armor(character):
    phys_resist = (
        character["left_hand"][0][4][0] +
        character["armor"][0][4][0] +
        character["helmet"][0][4][0]
    )
    fire_resist = (
        character["left_hand"][0][4][1] +
        character["armor"][0][4][1] +
        character["helmet"][0][4][1]
    )
    ice_resist = (
        character["left_hand"][0][4][2] +
        character["armor"][0][4][2] +
        character["helmet"][0][4][2]
    )
    electricity_resist = (
        character["left_hand"][0][4][3] +
        character["armor"][0][4][3] +
        character["helmet"][0][4][3]
    )
    print("{}% physical damage resistance".format(phys_resist))
    print("{}% fire damage resistance".format(fire_resist))
    print("{}% ice damage resistance".format(ice_resist))
    print("{}% electricity damage resistance".format(electricity_resist))
    
    
def roll_damage(character):
    strength = character["strength"]
    min_damage = (character["right_hand"][0][4][0] + strength)
    max_damage = (character["right_hand"][0][4][1] + strength)
    damage_type = character["right_hand"][0][4][2]
    damage = random.randrange(min_damage,max_damage+1)
    return { damage }
    #print("{} {} damage rolled".format(damage,damage_type))
    
    
def attack(attacker,defender):
    #Calculate attack damage
    strength = attacker["strength"]
    intelligence = attacker["intelligence"]
    min_damage = attacker["right_hand"][0][4][0]
    max_damage = attacker["right_hand"][0][4][1]
    damage_type = attacker["right_hand"][0][4][2]
    if damage_type == "physical":
        min_damage += strength
        max_damage += strength
    else:
        min_damage += intelligence
        max_damage += intelligence
    raw_damage = 0.0
    raw_damage = random.randrange(min_damage,max_damage+1)
    #Choose attack to use    
    if len(attacker["attacks"]) > 1:
        chosen_attack = random.choice(attacker["attacks"])
        if chosen_attack == attacker["attacks"][0]:
            chosen_attack = random.choice(attacker["attacks"])
        if attacker["stamina"] >= chosen_attack[2]:
            attacker["stamina"] = int(attacker["stamina"])-int(chosen_attack[2])
            raw_damage = raw_damage * float(chosen_attack[1])
        else:
            chosen_attack = attacker["attacks"][0]
        if attacker["stamina"] > attacker["max_stamina"]:
            attacker["stamina"] = attacker["max_stamina"]
    #Change damage type to that defined by attack
    if chosen_attack[3] != "":
        if chosen_attack[3] == damage_type:
            raw_damage = raw_damage * 1.5
        else:
            damage_type = chosen_attack[3]
    #Calculate armor value / damage resistances based on attackers damage_type
    if damage_type == "physical":
        resist = (
            defender["left_hand"][0][4][0] +
            defender["armor"][0][4][0] +
            defender["helmet"][0][4][0]
        )
    elif damage_type == "fire":
        resist = (
            defender["left_hand"][0][4][1] +
            defender["armor"][0][4][1] +
            defender["helmet"][0][4][1]
        )
    elif damage_type == "ice":
        resist = (
            defender["left_hand"][0][4][2] +
            defender["armor"][0][4][2] +
            defender["helmet"][0][4][2]
        )
    elif damage_type == "electricity":
        resist = (
            defender["left_hand"][0][4][3] +
            defender["armor"][0][4][3] +
            defender["helmet"][0][4][3]
        )
    else:
        resist = 0
    damage = int(((100-resist)/100)*raw_damage)
    if damage < 0:
        damage = 0
    #Apply damage and print message
    print("{} {}({},{}) deals {} {} damage to {} {}!".format(
        attacker["class"],
        attacker["name"],
        str(chosen_attack[0]),
        attacker["right_hand"][0][0],
        damage,
        damage_type,
        defender["class"],
        defender["name"]
    ))
    defender["health"] -= damage
    print("{} has {} health remaining!".format(         
        defender["name"],
        defender["health"]
    ))
    if (defender["health"] <= 0):
        print("\n-- {}{} {} has been slain by {} {}{}! --\n".format(
            color.BOLD,
            defender["class"],
            defender["name"],
            attacker["class"],
            attacker["name"],
            color.END
        ))
        reward_xp(attacker,defender)
        loot_coins(attacker,defender)
        behead(attacker,defender)
        try:
            kill_character(defender)
        except:
            pass
    print("\n")
    
    
def behead(attacker,defender):
    head = defender["name"]
    attacker["backpack"].append(["*"+head+"'s Head",2,0,1])


def kill_character(character):
    dump_backpack_of(character)
    roster.remove(character)

    
def pkill_character(character,party):
    party["members"].remove(character)


def heal(character):
    character["health"] = character["max_health"]
    character["stamina"] = character["max_stamina"] 
    print("{} {} healed to {} health!\n".format(
        character["class"],
        character["name"],
        character["max_health"]
    ))    


def loot_coins(attacker,defender):
    attacker["coins"] += defender["coins"]
    print("{} {} looted {} coins!\n  (Now at {} coins total.)".format(
        attacker["class"],
        attacker["name"],
        defender["coins"],
        attacker["coins"]
    ))


## ------------ FIX THIS! -------------- ##
## Only works for characters in base roster ##

def battle(attacker,defender):
    if len(roster) <= 1:
        return
    if attacker == defender:
        return #(print("Error!  Can't fight yourself!"))
    foes = len(roster)
    if foes != 1:
        attack(attacker,defender)
        if (len(roster)) == foes:
            attack(defender,attacker)
        try:
            if (len(roster)) == foes:
                battle(attacker,defender)
        except:
            print("Battle concluded!")
            heal(attacker)
    else:
        print("No one to fight!  Spawn more!")
        
        
def pbattle(attacker,defender):
    pass



## Only picks characters from base roster ##

def random_battle():
    if len(roster) <= 1:
        return(print("No one to fight! Spawn more!"))
    attacker = random.choice(roster)
    defender = random.choice(roster)
    if attacker == defender:
        random_battle()
    battle(attacker,defender)


def heal_roster():
    for character in roster:
        character["health"] = character["max_health"]
        character["stamina"] = character["max_stamina"]
        #print("{} healed to {} health!".format(character["name"],character["max_health"]))
        
        
def heal_party(party):
    for character in party["members"]:
        character["health"] = character["max_health"]
        character["stamina"] = character["max_stamina"]
        #print("{} healed to {} health!".format(character["name"],character["max_health"]))    
    
    
def assign_title(character, title):
    character["class"] = title            
    
    
def battle_royale():
    if len(roster) <= 1:        
        print("\nBattle Royale concluded after {} battles!\n".format(count)),
        kills = len(roster[0]["backpack"])-1
        print("{} won with {} kills using a {}!".format(
            roster[0]["name"],
            kills,
            roster[0]["right_hand"][0][0]
        ))        
        assign_title(roster[0],"Gladiator")
        confirm = input("Display winners character sheet?\n(Type y to accept) ")
        if confirm == "y":
            show_roster()
        else:
            return
        return        
    random_battle()
    heal_roster()
    battle_royale()


def party_battle_gui(party_a,party_b):
    unused = os.system("clear")
    totalhp = 0
    a_totalhp = 0
    b_totalhp = 0
    a_name = party_a["name"]
    b_name = party_b["name"]
    total_chars = 0
    party_a_members = 0
    for character in (party_a["members"]):
        total_chars += 1
        party_a_members +=1
    for character in (party_b["members"]):
        total_chars += 1
    for character in party_a["members"]:
        a_totalhp += character["health"]
    for character in party_b["members"]:
        b_totalhp += character["health"]
    #Determine how much GUI to show
    if party_a_members < 25:
        print(color.BOLD + "Team " + party_a["name"]  + color.END + " [" + str(a_totalhp) + "]")
        for character in party_a["members"]:
            colorset = decide_color(character)
            show_battle_line2(character,colorset)
        print("\n")        
    if total_chars < 25:    
        print(color.BOLD + "Team " + party_b["name"] + color.END + " [" + str(b_totalhp) + "]")
        for character in party_b["members"]:
            colorset = decide_color(character)
            show_battle_line2(character,colorset)
    print("\n")
    
    if a_totalhp > b_totalhp:
        first_color = color.BLUE
        second_color = color.RED
    elif a_totalhp < b_totalhp:
        first_color = color.RED
        second_color = color.BLUE
    else:
        first_color = color.YELLOW
        second_color = color.YELLOW
    
    print("{}{} [{}:{}] {}vs{} {} [{}:{}]{}\n".format(
        first_color,a_name,str(len(party_a["members"])),a_totalhp,color.END,
        second_color,b_name,str(len(party_b["members"])),b_totalhp,color.END
    ))
    
    
def show_battle_line(character,colorset):
    print("{}{}: {}/{} | {}/{}{}".format(
        colorset,character["name"],character["health"],character["max_health"],
        character["stamina"],character["max_stamina"],color.END
    ))
    
def show_battle_line2(character,colorset):
    print("%s %-15s: (%s) %4s/%-4s | %4s/%-4s %s" % (
        colorset,character["name"],character["level"],character["health"],character["max_health"],
        character["stamina"],character["max_stamina"],color.END
    ))
    
    
def decide_color(character):        
    test = character["max_health"]
    if character["health"] < (test/2):
        colorset = color.RED
    elif character["health"] < test:
        colorset = color.YELLOW
    else:
        colorset = color.END
    return colorset
    

def test_gui():
    quick_parties(6)
    party_battle_gui(roster2["parties"][0],roster2["parties"][1])
    

    
    
    
    


# ------------------------------- #
#         Battle Simulators       #
# ------------------------------- #            
    
    
    
def simulate_battle():
    clear_roster()
    create_foes()
    battle_royale()
    
    
def simulate_big_battle(x):
    clear_roster()
    if x > 10:
        print("Too high!  Script will crash.\nTry with a lower number.")
        return
    for reps in range(0,x):
        create_foes()
    confirm = input("Battle ready!\nEnter y to start: ")
    if confirm == "y":
        battle_royale()
    else:
        return
    return
 

def the_gauntlet():
    clear_roster()
    hero_name = input("Enter the name of your hero: ")
    if hero_name == "":
        hero_name = "Hiro"
    build_character(hero_name)
    hero = roster[0]
    random_enchant(hero)
    show_roster()
    confirm = input("Hit any key to continue to battle! ")
    confirm = ""
    create_foes()
    foes = len(roster)-1
    foes_slain = 0
    for reps in range(0,foes):
        if roster[0] != hero:
            print(hero_name + " has lost after defeating " + str(foes_slain) + " foes!")
            repeat = input("Enter r to retry, other to exit: ")
            if repeat == "r":
                the_gauntlet()
            else:
                return
            return
        else:
            if reps != 0:
                foes_slain += 1
                print(hero_name + " has defeated " + str(foes_slain) + " foes!")
        print("-- Battle {} of {}: --\n".format(reps+1,foes))
        foe = roster[1]
        level_scale(hero,foe)
        roll = random.randrange(0,4)
        if roll == 0:
            random_enchant(foe)
        heal(hero)
        battle(hero,foe)
    foes_slain += 1
    print(hero_name + " has defeated the gauntlet!  All " + str(foes_slain) + " foes were slain!")
    #assign_title(roster[0],"Gauntlet Runner")
    confirm = input("Display winners character sheet?\n(Type y to accept) ")
    if confirm == "y":
        show_roster()
    else:
        return
    return
         
    
def the_gauntlet_to_victory(gauntlet_attempts):
    os.system("clear")
    clear_roster()
    gauntlet_attempts += 1
    print(gauntlet_attempts)
    if gauntlet_attempts >= 1000:
        print("1000 attempts reached!  Aborting before python crashes!\nRun this again.")
        return
    hero_name = "Hiro"
    build_character(hero_name)
    hero = roster[0]
    random_enchant(hero)
    show_roster()
    create_foes()
    foes = len(roster)-1
    foes_slain = 0
    for reps in range(0,foes):
        if roster[0] != hero:
            print(hero_name + " has lost after defeating " + str(foes_slain) + " foes!")
            #repeat = input("Enter r to retry, other to exit: ")
            #if repeat == "r":
            the_gauntlet_to_victory(gauntlet_attempts)
            #else:
                #return
            return
        else:
            if reps != 0:
                foes_slain += 1
                print(hero_name + " has defeated " + str(foes_slain) + " foes!")
        print("-- Battle {} of {}: --\n".format(reps+1,foes))
        foe = roster[1]
        level_scale(hero,foe)
        roll = random.randrange(0,4)
        if roll == 0:
            random_enchant(foe)
        heal(hero)
        battle(hero,foe)
    if roster[0] != hero:
        print(hero_name + " has lost on the final battle!\nBad luck!\n")
        the_gauntlet_to_victory(gauntlet_attempts)
        return
    foes_slain += 1
    print("{} has defeated the gauntlet after {} attempts!  All {} foes were slain!".format(
        hero_name,
        gauntlet_attempts,
        str(foes_slain)
    ))
    gauntlet_attempts = 0
    #assign_title(roster[0],"Gauntlet Runner")
    confirm = input("Display winners character sheet?\n(Type y to accept) ")
    if confirm == "y":
        try:
            roster[0]["backpack"] = []
            roster[0]["backpack"].append([hero_name+"'s Journal",1,1,1])
            roster[0]["backpack"].append(["Gauntlet Runner Trophy",1,250,1])
            roster[0]["backpack"].append(["Gold Bar",10,1000,1])
        except:
            pass
        show_roster()
    else:
        return
    return


def pb_intro(party_a,party_b):
    print("\n{}Battle of {} vs {}!{}\nThis is a {}v{} battle!\nGood luck!!!\n".format(
        color.BOLD,party_a["name"],party_b["name"],color.END,
        str(len(party_a["members"])),str(len(party_b["members"]))
    ))
    for character in party_a["members"]:
        character["class"] = party_a["name"]
    for character in party_b["members"]:
        character["class"] = party_b["name"]
    time.sleep(1)
        
        
def pb_outro(party_a,party_b):
    if len(party_a["members"]) == 0:
        roster2["parties"].remove(party_a)
        heal_party(party_b)
    if len(party_b["members"]) == 0:
        roster2["parties"].remove(party_b)
        heal_party(party_a)
    os.system("clear")
    roster2["parties"][0]["battles"] += 1
    print("\n-- {}Battle concluded: Team {} wins!{} --\n".format(
        color.BOLD,roster2["parties"][0]["name"],color.END
    ))
    time.sleep(1)
    
    
def party_battle(party_a,party_b):
    pb_intro(party_a,party_b)
    time.sleep(1)
    # Very simple, pick a random from one side to attack the other, then switch
    # Also very kludge, lots of repeating code, can definitely be cleaned up
    while (len(party_a["members"]) > 0) & (len(party_b["members"]) > 0):  
        attacker = random.choice(party_a["members"])   
        defender = random.choice(party_b["members"])
        party_battle_gui(party_a,party_b)
        attack(attacker,defender)
        if attacker["health"] <= 0:
            pkill_character(attacker,party_a)
            time.sleep(1)
        if defender["health"] <= 0:
            pkill_character(defender,party_b)
            time.sleep(0.2)
        time.sleep(0.2)
        if (len(party_a["members"]) > 0) & (len(party_b["members"]) > 0):  
            attacker = random.choice(party_b["members"])   
            defender = random.choice(party_a["members"])
            party_battle_gui(party_a,party_b)
            attack(attacker,defender)
            if attacker["health"] <= 0:
                pkill_character(attacker,party_b)
                time.sleep(1)
            if defender["health"] <= 0:
                pkill_character(defender,party_a)
                time.sleep(0.2)
            time.sleep(0.2)
    # Main loop end
    pb_outro(party_a,party_b)
    show_parties()


def party_battle2(party_a,party_b):
    pb_intro(party_a,party_b)
    # This one should have all members of one team attack, then the other team, etc
    
    while (len(party_a["members"]) != 0) & (len(party_b["members"]) != 0):
        #Each surviving member of party_a attacks a random target from party_b
        for character in party_a["members"]: 
            if len(party_b["members"]) != 0:
                defender = random.choice(party_b["members"])
                party_battle_gui(party_a,party_b)
                attack(character,defender)
                if defender["health"] <= 0:
                    pkill_character(defender,party_b)
                    time.sleep(0.2)       
            time.sleep(0.2)
        #Each surviving member of party_b attacks a random target from party_a
        for character in party_b["members"]:       
            if len(party_a["members"]) != 0:
                defender = random.choice(party_a["members"])
                party_battle_gui(party_a,party_b)
                attack(character,defender)
                if defender["health"] <= 0:
                    pkill_character(defender,party_a)
                    time.sleep(0.2)
            time.sleep(0.2)
    
    # Main loop end
    pb_outro(party_a,party_b)
    show_parties()


def quick_party_battle(n):
    roster2["parties"].clear()
    quick_parties(n)
    party_battle(roster2["parties"][0],roster2["parties"][1])
    
    
def quick_party_battle2(n):
    roster2["parties"].clear()
    quick_parties(n)
    party_battle2(roster2["parties"][0],roster2["parties"][1])
    
    
def hero_v_mobs_battle(heroes,mobs,teamname):
    roster2["parties"].clear()
    hero_v_mobs_parties(heroes,mobs)
    roster2["parties"][0]["name"] = teamname
    party_battle2(roster2["parties"][0],roster2["parties"][1])
    
    
def continue_hero_v_mobs_battle(mobs):
    print("\n")
    heal_party(roster2["parties"][0])
    new_mob_party(mobs)
    party_battle2(roster2["parties"][0],roster2["parties"][1])
    
    
def party_gauntlet(heroes):
    battles = 0
    if (heroes > 1) & (heroes < 100):
        teamname = input("Please enter the name of your team: ")
        if teamname == "":
            teamname = random.choice(party_names)
        foes = heroes*2.5
        foes = int(foes)
        hvm(heroes,foes,teamname)
        battles += 1
        while (roster2["parties"][0]["name"] == teamname) & (battles < 20):
            chvm(foes)
            battles +=1
        if battles >= 20:
            print("{}Team {} has defeated the gauntlet after {} battles!\n\tCongrats!{}".format(
                color.BOLD,teamname,battles,color.END))
        else:
            print("{}Team {} has fallen after {} battles!{}".format(
                color.BOLD,teamname,battles,color.END))
    else:
        print(color.BOLD+"ERROR: "+color.END+"Heroes should be greater than 1 and less than 100!")
        
        
def dungeon(dungeon):
    # If no party is present, make one
    if len(roster2["parties"]) == 0:
        hero_party(6)
    
    party = roster2["parties"][0]
    partyname = party["name"]
    print("\n----------------------------------------")
    print(color.BOLD + str(dungeon["name"]).center(40) + color.END)
    print("----------------------------------------\n")
    print(dungeon["long_desc"])
    for event in dungeon["events"]:
        if party["name"] == roster2["parties"][0]["name"]:
            print(event)
            time.sleep(2)
            level = roster2["parties"][0]["members"][0]["level"]
            if level > 0:
                bonus = (level*0.8)
            else:
                bonus = 0
            chvm(int((len(party["members"])*2.5)+bonus))
        else:
            print(dungeon["fail"])
            return
    print(dungeon["win"])
    print("\n----------------------------------------")
    dung_string = str(dungeon["name"])+" completed!"
    print(color.BOLD+dung_string.center(40)+color.END)
    print("----------------------------------------\n")


## Shortcut commands
    
def qpb(n):
    quick_party_battle(n)
    
    
def qpb2(n):
    quick_party_battle2(n)

    
def hvm(heroes,mobs,teamname):
    hero_v_mobs_battle(heroes,mobs,teamname)
    
    
def chvm(mobs):
    continue_hero_v_mobs_battle(mobs)
    
    
def dung():
    dungeon(random.choice(dungeons))
    
    
        
        
        


# ------------------------------- #
#         Enchanting Stuff        #
# ------------------------------- #

 

def random_enchant(character):
    weapon = character["right_hand"][0]
    weapon_orig = weapon
    enchantment = random.choice(enchantments)
    min_damage = weapon[4][0]+enchantment[4][0]
    max_damage = weapon[4][1]+enchantment[4][1]
    new_weapon = [
        str(weapon[0] + enchantment[0]),
        int(weapon[1]),
        int(weapon[2]+enchantment[2]),
        int(weapon[3]),
        list(weapon[4])
    ]
    new_weapon[4][0] = min_damage
    new_weapon[4][1] = max_damage    
    if (str(enchantment[4][2]) != str(weapon[4][2])) & (str(enchantment[4][2]) != ""):
        new_weapon[4][2] = str(enchantment[4][2])
    else:
        pass
    #Sanity check the damage stats
    if new_weapon[4][0] < 0 :
        new_weapon[4][0] = 0
    if new_weapon[4][1] < new_weapon[4][0]:
        new_weapon[4][1] = new_weapon[4][0]
    character["right_hand"].remove(weapon_orig)
    character["right_hand"].append(new_weapon)    
    print("Enchanted {}s weapon!\n".format(character["name"]))
    return
                                     

 
    

        
        
# ------------------------------- #
#         Levelling Stuff         #
# ------------------------------- #



def reward_xp(attacker,defender):
    xp_gain = (10+(5*defender["level"]))
    attacker["xp"] += xp_gain
    print("{} {} gained {} xp!".format(attacker["class"],attacker["name"],xp_gain))
    level_check(attacker["level"],attacker["xp"],attacker)
    
    
def level_check(level,xp,character):
    xp_to_level = (50+(level*25))
    if (xp >= xp_to_level):
        level_up(character)
    
    
def level_up(character):
    character["level"] += 1
    character["xp"] = 0
    character["max_health"] += random.randrange(3,5)
    character["health"] = character["max_health"]
    character["max_stamina"] += random.randrange(2,4)
    character["stamina"] = character["max_stamina"]
    print(str(character["name"]) + " has reached level " + str(character["level"])+"!")
    choice = random.randrange(1,4)
    if choice == 1:
        character["strength"] += 1
        print("*Strength increased to {}!".format(character["strength"]))
    elif choice == 2:
        character["dexterity"] += 1
        print("*Dexterity increased to {}!".format(character["dexterity"]))
    else:
        character["intelligence"] += 1
        print("*Intelligence increased to {}!".format(character["intelligence"]))
    #Check for and apply titles as defined below
    class_title(character)
    new_attack(character)
    
    
def new_attack(character):
    if character["level"] == 2:
        attack = random.choice(attack_list.t1)
        if attack in character["attacks"]:
            new_attack(character)
            return
        else:
            character["attacks"].append(attack)
            print("*{} learned a new attack: {}!".format(character["name"],attack[0]))
        return
    if character["level"] == 5:
        attack = random.choice(attack_list.t2)
        if attack in character["attacks"]:
            new_attack(character)
            return
        else:
            character["attacks"].append(attack)
            print("*{} learned a new attack: {}!".format(character["name"],attack[0]))
        return
    if character["level"] == 10:
        attack = random.choice(attack_list.t3)
        if attack in character["attacks"]:
            new_attack(character)
            return
        else:
            character["attacks"].append(attack)
            print("*{} learned a new attack: {}!".format(character["name"],attack[0]))
        return
    
        
def class_title(character):
    #First title assignment at level 1
    if character["level"] == 1:
        if character["strength"] > 1:
            assign_title(character,"Farmer")
        elif character["dexterity"] > 1:
            assign_title(character,"Hunter")
        elif character["intelligence"] > 1:
            assign_title(character,"Student")
        else:
            pass
    #Second title assignment at level 5
    elif character["level"] == 5:
        if character["strength"] > 4:
            assign_title(character,"Strongman")
        elif character["dexterity"] > 4:
            assign_title(character,"Ranger")
        elif character["intelligence"] > 4:
            assign_title(character,"Apprentice")
        elif (character["strength"] > 2) & (character["dexterity"] > 2):
            assign_title(character,"Scout")
        elif (character["strength"] > 2) & (character["intelligence"] > 2):
            assign_title(character,"Acolyte")
        elif (character["dexterity"] > 2) & (character["intelligence"] > 2):
            assign_title(character,"Trickster")
        else:
            assign_title(character,"Wanderer")
    #Third title assignment at level 10
    elif character["level"] == 10:
        if character["strength"] > 8:
            assign_title(character,"Warrior")
        elif character["dexterity"] > 8:
            assign_title(character,"Rogue")
        elif character["intelligence"] > 8:
            assign_title(character,"Wizard")
        elif (character["strength"] > 4) & (character["dexterity"] > 4):
            assign_title(character,"Soldier")
        elif (character["strength"] > 4) & (character["intelligence"] > 4):
            assign_title(character,"Battlemage")
        elif (character["dexterity"] > 4) & (character["intelligence"] > 4):
            assign_title(character,"Sneak Thief")
        else:
            assign_title(character,"Adventurer")
            
        
        
def level_scale(attacker,defender):
    if attacker["level"] == defender["level"]:
        pass
    elif attacker["level"] > defender["level"]:
        difference = attacker["level"]-defender["level"]
        print("-- Scaling level...")
        for rep in range(0,difference):
            level_up(defender)
        print("-- Level scaled!\n")
    else:
        pass
    
    
    
        
# ------------------------------- #
#            Map Stuff            #
# ------------------------------- #

        
def new_map(default_name):
    map_data = {
        "name": default_name,
        "center_x": 0,
        "center_y": 0,
        "max_x": 10,
        "max_y": 10,
        "min_x": -10,
        "min_y": -10,
        "features": [],
        "characters": [],
        "stored_chars": {
            "char": [],
            "x": [],
            "y": []
        }
    }
    cartographer.append(map_data)
    return { 
        "Map '{}' generated!".format(map_data["name"])
    }


def store_char(map_index,character_index):
    try:
        cartographer[map_index]["stored_chars"]["char"].append(roster[character_index])
        cartographer[map_index]["stored_chars"]["x"].append(0)
        cartographer[map_index]["stored_chars"]["y"].append(0)
        print("Appended {} to {}!".format(
            roster[character_index]["name"],
            cartographer[map_index]["name"]
        ))
    except:
              print("Error! Could not store character!")

            
def show_maps():
    print("\n------------------\n")
    print("   CARTOGRAPHER")
    print("\n------------------\n")
    for map in cartographer:
        print("\n--- " + map["name"]+" ---")
        print("Map size: {} x {}\n".format(
            str(abs(map["min_x"])+abs(map["max_x"])),
            str(abs(map["min_y"])+abs(map["max_y"]))
        ))
        for feature in map["features"]:
            print("{} is located at {},{}".format(
                feature["name"],feature["x"],feature["y"])
            )    
        print("\n")
        for char in map["characters"]:
            print("{} is present".format(str(char["name"])))
        #for char in map["stored_chars"]:
        #    try:
        #        print("{} is located at {},{}".format(
        #            char["char"]["name"],
        #            char["x"],
        #            char["y"]
        #        ))
        #    except:
        #        print("Error!  Couldn't print stored_chars!")
        #        print(char)
    print("\n------------------\n")
    print("\n")
    
    
def new_feature(map_index, default_name):
    loc = cartographer[map_index]
    feature_data = {
        "name": default_name,
        "x": random.randrange(loc["min_x"],loc["max_x"]),
        "y": random.randrange(loc["min_y"],loc["max_y"])
    }
    try:
        cartographer[map_index]["features"].append(feature_data)
        print("{} generated at {},{}".format(
            feature_data["name"],
            feature_data["x"],
            feature_data["y"]
        ))
    except:
        print("Something went wrong!  Couldn't append to map!")
        
        
def find_feature(map_index,x,y):
    for features in cartographer[map_index]["features"]:
        if(features["x"] == x) & (features["y"] == y):
            print("Found {} at {},{}!".format(features["name"],features["x"],features["y"]))
                  

def char_to_map(map_index, roster_index):
    try:
        cartographer[map_index]["characters"].append(roster[roster_index])
        print("{} appended to {}!".format(
            roster[roster_index]["name"],
            cartographer[map_index]["name"]
        ))
    except:
        print("Couldn't append character to map!")
        
        
def hero_position():
    print("Hero at: {},{}".format(hero_loc[0],hero_loc[1]))
        
        
def move_up(hero_loc):
    hero_loc = hero_loc[0],hero_loc[1]-1
    hero_position()
    find_feature(0,hero_loc[0],hero_loc[1])
    
def move_down(hero_loc):
    hero_loc = hero_loc[0],hero_loc[1]+1
    hero_position()
    find_feature(0,hero_loc[0],hero_loc[1])
    
def move_left(hero_loc):
    hero_loc = hero_loc[0]-1,hero_loc[1]
    hero_position()
    find_feature(0,hero_loc[0],hero_loc[1])
    
def move_right(hero_loc):
    hero_loc = hero_loc[0]+1,hero_loc[1]
    hero_position()
    find_feature(0,hero_loc[0],hero_loc[1])

