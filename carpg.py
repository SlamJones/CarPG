#!/usr/bin/env python3


## THIS IS THE EXPERIMENTAL BRANCH ##
## OR, AT LEAST IT SHOULD BE!! ##


##
##### PRIORITIES:
##### PRACTICE PROGRAMMING SKILLS IN AN ENJOYABLE ENVIRONMENT (THE ONLY THING HERE THAT MATTERS)
##### MODULARIZE CODE WHEREVER POSSIBLE
##### MOVE DATA TO SEPARATE FILE OF SOME SORT
##### MAKE CAR/VEHICLE REFERENCE CONSISTENT (USE ONE TERM OR THE OTHER: NOT BOTH!!!)
##### GROUP FUNCTIONS TOGETHER (IE ALL new_ FUNCTIONS TOGETHER, ALL calculate_ FUNCTIONS TOGETHER, ETC) ##
##### CREATE A SATISFYING USER EXPERIENCE
##


import os
import sys
import select
import random
import math
import subprocess
import time

from rpgf import color
from rpgf import names
from rpgf import party_names

from threading import Timer
from threading import Thread


## INITIALIZE SOME COMMON VARIABLES ##
seatroster = []
roster = []
garage = []
atlas = []
player = []
travel_log = []
answer = None


# GATHER TERMINAL SIZE AND SET BORDER SIZES ACCORDINGLY ##
terminal_size = 80
try:
    terminal_size = os.get_terminal_size()[0]
except:
    pass
long_border="-"*terminal_size
short_border="-"*int((terminal_size/4))



##
## GAME/PART DATA STORED HERE UNTIL I LEARN SQL OR SOMETHING LIKE THAT ##
## I ASSUME THAT STORING DATA IN A PYTHON SCRIPT IS A SILLY MOVE AT BEST ##
##

street_types = ["St", "Rd", "Ave", "Blvd", "Highway", "Lane"]
speed_limits = [40,50,60,70,80,90,100]
town_types = [" Town","ville"," City","shire","bury","borough","by","ford","ham","stead","ton",
             " Beach"," Mesa"," Castle","view","port","dorf","field","burg","dale","grad", 
             " Village"," Hamlet"," Market"," Temple","side"," Grove"," Garden"," Hills"]

amenities = ["Gas Station","Convenience Store","Junkyard","Rest Stop","Museum", "Auto Shop", "Garage","Library","Car Lot","Racetrack","Warehouse","Repair Shop","University","Casino","Parts Store"]
amenities2 = {
    "low": ["Gas Station","Garage","Junkyard","Warehouse"],
    "mid": ["Library","Auto Shop","Car Lot","Racetrack","Repair Shop","Parts Store"],
    "high": ["Univeristy","Museum","Casino"]
}

stops = ["Intersection","Field","Forest","Farm","Escarpment","Campsite","Gas Station","Garage", "Junkyard","Racetrack","Gas Station","Fissure","Cave","Volcano","Plateau","Salvage Yard"]
town_types2 = {
    "common": ["bury","borough","by","ford","ham","stead","ton","view","field","dale", "side"],
    "small": ["ville"," Village"," Hamlet"," Market"," Grove"," Garden","shire"," Meadows", 
             " Springs"],
    "medium": [" Town"," Hills"," Temple"," Beach"," Mesa","port",],
    "large": [" City"," Castle","dorf","burg","grad",]
}

help_string = long_border+"\nWelcome to CarPG!\n"+short_border+"\nYour goal is to gather currency!  You can do this by:\n Completing Warehouse Deliveries\n Collecting and Selling Science Samples\n Salvaging and Selling car parts, or\n Competing in Races and winning prize money!\n"+short_border+"\nThere is no win or lose condition yet: but you can consider running out of both currency and fuel to be a lose condition if you need one.\n"+short_border+"\nGood luck!!\n"+long_border


## -- PARTS -- ##
parts = {
    "chassis": [
        {"brand": "SlamTek",
         "model": "SlamChas",
         "type": "Chassis",
         "value": 100,
         "size": "1",
         "weight": 1000,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
         "weight_wear_factor": 1.0,
         "wheelbase": 3.0,
         "track": 1.5,
         "wheels": 4,
        },
        {"brand": "SlamTek",
         "model": "SlamChas2",
         "type": "Chassis",
         "value": 80,
         "size": "1",
         "weight": 1200,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
         "weight_wear_factor": 1.0,
         "wheelbase": 3.2,
         "track": 1.5,
         "wheels": 4,
        },
        {"brand": "Pigeon",
         "model": "Carrier",
         "type": "Chassis",
         "value": 200,
         "size": "1",
         "weight": 500,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.3,
         "weight_wear_factor": 1.5,
         "wheelbase": 1.5,
         "track": 1.2,
         "wheels": 3,
        },
        {"brand": "Flexx",
         "model": "Racer",
         "type": "Chassis",
         "value": 500,
         "size": "1",
         "weight": 800,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.3,
         "weight_wear_factor": 1.2,
         "wheelbase": 1.8,
         "track": 1.4,
         "wheels": 4,
        },
        {"brand": "Steelworks",
         "model": "2-ton Chassis",
         "type": "Chassis",
         "value": 250,
         "size": "2",
         "weight": 2000,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
         "weight_wear_factor": 1.0,
         "wheelbase": 4.0,
         "track": 1.7,
         "wheels": 4,
        },
        {"brand": "Universal",
         "model": "Bus Chassis 01",
         "type": "Chassis",
         "value": 250,
         "size": "3",
         "weight": 2500,
         "engine": "",
         "cabin": "",
         "fuel_tank": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 0.5,
         "weight_wear_factor": 0.5,
         "wheelbase": 8.0,
         "track": 1.9,
         "wheels": 8,
        }
    ],
    
    "engine": [
        {"brand": "SlamTek",
         "model": "Based v4",
         "type": "Engine",
         "value": 150,
         "size": "1",
         "weight": 200,
         "base_mpg": 20,
         "base_horsepower": 100,
         "base_torque": 200,
         "cylinders": 4,
         "bore": 4,
         "stroke": 3,
         "max_rpm": 4500,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "SlamTek",
         "model": "Based v6",
         "type": "Engine",
         "value": 200,
         "size": "1",
         "weight": 300,
         "base_mpg": 15,
         "base_horsepower": 150,
         "base_torque": 300,
         "cylinders": 6,
         "bore": 4,
         "stroke": 3,
         "max_rpm": 4500,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "SlamTek",
         "model": "Heavy v6",
         "type": "Engine",
         "value": 200,
         "size": "1",
         "weight": 300,
         "base_mpg": 15,
         "base_horsepower": 150,
         "base_torque": 300,
         "cylinders": 6,
         "bore": 4,
         "stroke": 4.5,
         "max_rpm": 3000,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Pigeon",
         "model": "Econo 24",
         "type": "Engine",
         "value": 500,
         "size": "1",
         "weight": 100,
         "base_mpg": 30,
         "base_horsepower": 50,
         "base_torque": 75,
         "cylinders": 4,
         "bore": 3,
         "stroke": 2.4,
         "max_rpm": 5000,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 0.75,
        },
        {"brand": "Rattatata",
         "model": "Thresher 145",
         "type": "Engine",
         "value": 650,
         "size": "1",
         "weight": 500,
         "base_mpg": 10,
         "base_horsepower": 300,
         "base_torque": 200,
         "cylinders": 6,
         "bore": 4.5,
         "stroke": 2.5,
         "max_rpm": 8500,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.6,
        },
        {"brand": "Steelworks",
         "model": "Steel 225",
         "type": "Engine",
         "value": 600,
         "size": "2",
         "weight": 550,
         "base_mpg": 18,
         "base_horsepower": 350,
         "base_torque": 600,
         "cylinders": 8,
         "bore": 5,
         "stroke": 4.5,
         "max_rpm": 4500,
         "compression": 1,
         "turbo": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Universal",
         "model": "vStroke 420",
         "type": "Engine",
         "value": 850,
         "size": "3",
         "weight": 600,
         "base_mpg": 8,
         "base_horsepower": 300,
         "base_torque": 1000,
         "cylinders": 10,
         "bore": 5,
         "stroke": 8.5,
         "max_rpm": 3500,
         "compression": 1,
         "turbo": "",
         "durability": 200,
         "max_durability": 200,
         "wear_rate": 0.5,
        },
    ],
    
    "turbo": [
        {"brand": "Yolo",
         "model": "Hurricane",
         "type": "Turbo",
         "value": 750,
         "size": 1,
         "weight": 50,
         "horsepower_factor": 1.2,
         "torque_factor": 1.2,
         "mpg_factor": 0.6,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.5,
        },
        {"brand": "Yolo",
         "model": "Breeze",
         "type": "Turbo",
         "value": 550,
         "size": 1,
         "weight": 25,
         "horsepower_factor": 1.1,
         "torque_factor": 1.1,
         "mpg_factor": 0.8,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.25,
        }
    ],

    "cabin": [
        {"brand": "SlamTek",
         "model": "Short Cab",
         "type": "Cabin",
         "value": 250,
         "size": "1",
         "weight": 200,
         "passengers": 2,
         "max_cargo": 100,
         "drag": 0.4,
         "frontal_area": 2.3,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "SlamTek",
         "model": "Long Cab",
         "type": "Cabin",
         "value": 350,
         "size": "1",
         "weight": 300,
         "passengers": 4,
         "max_cargo": 100,
         "drag": 0.9,
         "frontal_area": 3.3,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Pigeon",
         "model": "Nest",
         "type": "Cabin",
         "value": 550,
         "size": "1",
         "weight": 150,
         "passengers": 1,
         "max_cargo": 100,
         "drag": 0.4,
         "frontal_area": 1.3,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.3,
        },
        {"brand": "Steelworks",
         "model": "Shortbed Pick-Up Cab",
         "type": "Cabin",
         "value": 850,
         "size": "2",
         "weight": 750,
         "passengers": 2,
         "max_cargo": 400,
         "drag": 0.8,
         "frontal_area": 3.2,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Steelworks",
         "model": "Longbed Pick-Up Cab",
         "type": "Cabin",
         "value": 950,
         "size": "2",
         "weight": 950,
         "passengers": 2,
         "max_cargo": 600,
         "drag": 0.82,
         "frontal_area": 3.2,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Steelworks",
         "model": "Shortbed Crew Cab",
         "type": "Cabin",
         "value": 1050,
         "size": "2",
         "weight": 1200,
         "passengers": 4,
         "max_cargo": 300,
         "drag": 0.81,
         "frontal_area": 3.3,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Steelworks",
         "model": "Longbed Crew Cab",
         "type": "Cabin",
         "value": 1250,
         "size": "4",
         "weight": 1500,
         "passengers": 4,
         "max_cargo": 600,
         "drag": 0.83,
         "frontal_area": 3.3,
         "cargo": [],
         "seats": [],
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Universal",
         "model": "Bus Cab",
         "type": "Cabin",
         "value": 750,
         "size": "3",
         "weight": 800,
         "passengers": 20,
         "max_cargo": 1000,
         "drag": 0.9,
         "frontal_area": 4.3,
         "cargo": [],
         "seats": [],
         "durability": 200,
         "max_durability": 200,
         "wear_rate": 0.5,
        }
    ],
    
    "fuel_tank": [
        {"brand": "SlamTek",
         "model": "Fuel Tank 01",
         "type": "Fuel Tank",
         "value": 100,
         "weight": 5,
         "size": "1",
         "capacity": 40,
         "fuel": 0,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "SlamTek",
         "model": "Fuel Tank 02",
         "type": "Fuel Tank",
         "value": 250,
         "weight": 10,
         "size": "1",
         "capacity": 45,
         "fuel": 0,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Pigeon",
         "model": "Mini Tank",
         "type": "Fuel Tank",
         "value": 100,
         "weight": 2,
         "size": "1",
         "capacity": 20,
         "fuel": 0,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Steelworks",
         "model": "VentureTank",
         "type": "Fuel Tank",
         "value": 550,
         "weight": 50,
         "size": "2",
         "capacity": 80,
         "fuel": 0,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Steelworks",
         "model": "ExploreTank",
         "type": "Fuel Tank",
         "value": 950,
         "weight": 85,
         "size": "2",
         "capacity": 95,
         "fuel": 0,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Universal",
         "model": "EnduroTank",
         "type": "Fuel Tank",
         "value": 850,
         "weight": 100,
         "size": "3",
         "capacity": 500,
         "fuel": 0,
         "durability": 200,
         "max_durability": 200,
         "wear_rate": 0.5,
        }
    ],
    
    "seats": [
        {"brand": "SlamTek",
         "model": "Seat 01",
         "type": "Seat",
         "value": 50,
         "weight": 5,
         "size": "1",
         "capacity": 1,
         "comfort": 1,
         "characters": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "SlamTek",
         "model": "Seat 02",
         "type": "Seat",
         "value": 150,
         "weight": 10,
         "size": "1",
         "capacity": 1,
         "comfort": 2,
         "characters": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        },
        {"brand": "Universal",
         "model": "Basic Bus Seat",
         "type": "Seat",
         "value": 50,
         "weight": 5,
         "size": "1",
         "capacity": 1,
         "comfort": 0,
         "characters": "",
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
        }
    ],
    
    "wheels": [
        {"brand": "Universal",
         "model": "w1-20",
         "type": "wheel",
         "value": 50,
         "weight": 2.5,
         "size": 1,
         "durability": 100,
         "max_durability": 100,
         "wear_rate": 1.0,
         "diameter": 20,
         "width": 6,
         "camber": 0,
         "toe": 0,
         "tire": ""
        }
    ],
    
    "tires": [
        {"brand": "Universal",
         "model": "t1-20",
         "type": "tire",
         "value": 50,
         "weight": 2.5,
         "size": 1,
         "durability": 100,
         "max_durability": 100,
         # Drag rate decreases mpg
         "drag_rate": 1.0,
         "wear_rate": 1.0,
         "diameter": 20,
         "width": 6,
         "max_psi": 20,
         "psi": 20
        }
    ],
}
    
class jobs:
    JOBS = [
        "Driver","Scientist","Mechanic"
    ]
    SKILLS = [
        {
            "skill": "Drive",
            "tree": "Driver",
            "level": 0,
            "xp": 0
        },
        {
            "skill": "Repair",
            "tree": "Mechanic",
            "level": 0,
            "xp": 0
        },
        {
            "skill": "Salvage",
            "tree": "Mechanic",
            "level": 0,
            "xp": 0
        },
        {
            "skill": "Biology",
            "tree": "Scientist",
            "level": 0,
            "xp": 0
        },
        {
            "skill": "Engineering",
            "tree": "Scientist",
            "level": 0,
            "xp": 0
        }
    ]
    
    
    
    
    
##### COMMON FUNCTIONS LIST BELOW #####    
    
def random_town_name():
    return (random.choice(names)+random.choice(town_types))


## CHOOSE TOWN SUFFIX BASED ON TOWN SIZE ##
def size_town_name(town):
    name_choices=town_types2["common"].copy()    
    if town["size"] < 3:
        name_choices=name_choices+town_types2["small"]
    elif town["size"] < 6:
        name_choices=name_choices+town_types2["medium"]
    else:
        name_choices=name_choices+town_types2["large"]
    return(random.choice(names)+random.choice(name_choices))

    
## ALL new_ FUNCTIONS CREATE A 'DEFAULT' ITEM, WHICH IS THEN MODIFIED AS NEEDED ##
def new_road():
    return {
        "name": "default",
        "length": 0,
        "sections": [],
        "stops": [],
        "start": "",
        "end": ""
    }


def new_road_section():
    return {
        "direction": random.randrange(0,359),
            #direction in degrees
        "speed_limit": random.choice(speed_limits),
            #speed_limit in kmh
        "length": random.randrange(1,80),
            #length in km
        "vehicles": []
            #list of vehicles on the road section
    }
    

def new_stop():
    return {
        "name": random.choice(names),
        "type": random.choice(stops),
        "roads": []
    }
    
    
def new_town():
    population = random.randrange(100,21000)
    size = int(population/2000)
    if size == 0:
        size=1
    return {
        "name": "default",
        "type": "default",
        "population": population,
        "elevation": random.randrange(0,2500),
        "size": size,
        "amenities": [],
        "roads": []
    }


## OLD VERSION OF build_town WHICH HAD SOME ISSUES, KEEPING FOR POSTERITY, TO BE REMOVED LATER ##
def build_town_backup():
    town = new_town()
    town["name"] = random_town_name()
    try:
        town["name"]=size_town_name(town)
    except:
        pass
    for i in range(0,town["size"]):
        amen = random.choice(amenities)
        if amen in town["amenities"]:
            amen = random.choice(amenities)
        town["amenities"].append(amen)
    town["amenities"].append("Gas Station")
    town["amenities"].append("Warehouse")
    town["amenities"].sort()
    #display_town(town)
    return(town)


## BUILD TOWN WITH new_ FUNCTIONS, APPEND AMENITIES BASED ON SIZE OF TOWN ##
def build_town():
    town = new_town()
    town["name"] = random_town_name()
    try:
        town["name"]=size_town_name(town)
    except:
        pass
    amenities_list = []
    if town["size"] < 4:
        amenities_list = amenities2["low"]
    elif town["size"] < 7:
        amenities_list = amenities2["low"]
        amenities_list = amenities_list + amenities2["mid"]
    else:
        amenities_list = amenities2["low"]
        amenities_list = amenities_list + amenities2["mid"]
        amenities_list = amenities_list + amenities2["high"]
    for i in range(0,town["size"]):
        amen = random.choice(amenities)
        if amen in town["amenities"]:
            amen = random.choice(amenities)
        town["amenities"].append(amen)
    town["amenities"].append("Gas Station")
    for amenity in ["Warehouse","Garage"]:
        rng = random.choice([True,False])
        if rng:
            town["amenities"].append(amenity)
    town["amenities"].sort()
    #display_town(town)
    return(town)
    
    
## READABLE INFO FOR SPECIFIED TOWN ##    
def display_town(town):
    print("\n\n--- {}{}{} ---\nPopulation: {}, Elevation {}ft\n".format(
        color.BOLD,town["name"],color.END,town["population"],town["elevation"]))
    time.sleep(1)
    print("\n{}Amenities{}:".format(color.UNDERLINE,color.END))
    time.sleep(0.5)
    for amenity in town["amenities"]:
        print(amenity)
        time.sleep(0.1)
    time.sleep(0.5)
    print("\n{}Roads{}:".format(color.UNDERLINE,color.END))
    time.sleep(0.5)
    for road in town["roads"]:
        print(road)
        time.sleep(0.1)
    time.sleep(1)


## ALSO READABLE, BUT MUCH SHORTER ##
def summary_town(town):
    if len(town["roads"]) == 1:
        plural=""
    else:
        plural="s"
    print("{}: Pop {}, {} Amenities, {} Road{}".format(
        town["name"],town["population"],len(town["amenities"]),len(town["roads"]),plural))
    

## ARE town1 and town2 DIRECTLY CONNECTED?  IF SO, DISPLAY THE ROAD THEY ARE CONNECTED WITH ##
def towns_connected(network,town1,town2):
    towns=[town1,town2]
    for road in network["roads"]:
        if (road["start"] in towns) & (road["end"] in towns):
            display_road(road)
            #print("{} and {} are connected via {}".format(
            #    town1,town2,road["name"]))


## ARE town1_name and town2_name CONNECTED?  IF SO, RETURN THE ROAD THAT CONNECTS THEM ##           
def connected_by(network,town1_name,town2_name):
    towns=[town1_name,town2_name]
    for road in network["roads"]:
        if (road["start"] in towns) & (road["end"] in towns):
            #display_road(road)
            #print("{} and {} are connected via {}".format(
            #    town1_name,town2_name,road["name"]))
            return(road)
            

## GIVEN town_name, RETURN A LIST OF ALL TOWNS DIRECTLY CONNECTED TO THIS TOWN ##
## DEBUG TEXT COMMENTED OUT FOR NOW ##
def connected_to(network,town_name):
    reftown=find_town(network,town_name)
    connected_towns=[]
    if (type(reftown["roads"])==list):
        for road in reftown["roads"]:
            road=trim_road_connection_name(road)
            refroad=find_road(network,road)
            found_name=refroad["start"]
            connected_towns.append(found_name)
            found_name=refroad["end"]
            connected_towns.append(found_name)
            for town in connected_towns:
                if town == town_name:
                    connected_towns.remove(town)
    else:
        #print(road)
        pass
    #display_town(reftown)
    #print("\n{}{}{} is connected to:".format(color.UNDERLINE,reftown["name"],color.END))
    #print(connected_towns)
    return(connected_towns)


## A PATH IS A LIST OF CONNECTED TOWNS ##
## FOR EACH ROAD IN PATH, ADD TO LENGTH INT ##
## FINALLY RETURN FULL PATH LENGTH ##
def calculate_path_length(network,path):
    path_count = len(path)
    count = 0
    length = 0
    for i in range(0,path_count-1):
        start_town = path[i]
        end_town = path[i+1]
        road = connected_by(network,start_town,end_town)
        length += road["length"]
    return(length)
        

## I LOVE THIS FUNCTION! ##
## GIVEN TWO TOWN NAMES, FINDS A PATH BETWEEN THEM AND RETURNS THAT PATH ##
## ENDED UP BEING EASIER THAN I EXPECTED ##
## COULD UNDOUBTEDLY BE OPTIMIZED!!! ##
## PROBLEM!! DOES NOT FIND PATHS WITH LENGTH OF 1: IE START TOWN -> END TOWN ##
def find_route(network,start_town_name,end_town_name):
    # Qualifiers
    if start_town_name == end_town_name:
        return("It's the same town!")
    connected_towns_start = []
    connected_towns_end = []
    ## PATH ALWAYS STARTS AT START TOWN ##
    path = [start_town_name]
    possible_paths = []
    ## TRY TO GATHER A LIST OF TOWNS CONNECTED TO START TOWN ##
    try:
        connected_towns = connected_to(network,start_town_name)
        x = connected_to(network,end_town_name)
    except:
        return("ERROR! This town does not exist!")
    for town_name in connected_towns:
        if town_name not in possible_paths:
            possible_paths.append([start_town_name,town_name])
    final_path=find_route_loop(network,start_town_name,end_town_name,possible_paths)
    return(final_path)
        
        
## THE WORKHORSE FOR find_route ##
## FINDS INDIVIDUAL ROADS TO CREATE THE PATH ##
def find_route_loop(network,start_town_name,end_town_name,possible_paths):
    count=0
    for path in possible_paths:
        #print(path)
        #print(path[0]+" > "+path[1])
        start_town_name = path[-1]
        connected_towns = connected_to(network,start_town_name)
        for town_name in connected_towns:
            #print("For "+town_name+" in connected_towns")
            if town_name not in possible_paths:
                new_path = path.copy()
                new_path.append(town_name)
                possible_paths.append(new_path)
                #print("Appended "+town_name+" to path:")
                #for line in new_path:
                #    print(line)
                #print(short_border)
                if town_name == end_town_name:
                    #print("PATH FOUND!!!!")
                    #print(new_path)
                    return(new_path)
        count+=1
    return(new_path)
    #return(possible_paths)
    
    
## RETURNS A RANDOM AMENITY SOMEWHERE IN THE NETWORK ##
## USEFUL FOR DELIVERY MISSIONS, ETC ##
def random_network_amenity(network,amenity_name):
    possible_amenities = list_network_amenities(network,amenity_name)
    choice = random.choice(possible_amenities)
    chosen_amenity = [amenity_name, choice]
    return(chosen_amenity)


## RETURNS A DICTIONARY THAT DESCRIBES HOW MANY OF A TYPE OF AMENITY EXIST IN THE NETWORK ##
def list_network_amenities(network,amenity_name):
    if amenity_name not in amenities and amenity_name not in stops:
        return("No known amenity by that name!")
    possible_amenities = []
    stop_list = []
    for town in network["towns"]:
        if amenity_name in town["amenities"]:
            town_name = town["name"]
            possible_amenities.append(town["name"])
    count=0
    for road in network["roads"]:
        for stop in road["stops"]:
            stop_list.append(stop["type"])
        if amenity_name in stop_list:
            road_name = road["name"]
            possible_amenities.append(road["name"])
    return(possible_amenities)


## RETURNS A LIST OF DICTIONARIES DESCRIBING THE QUANTITY OF ALL AMENITIES IN THE NETWORK ##
def list_all_network_amenities(network):
    all_amenities = []
    name = ""
    for name in amenities:
        amenity_list = list_network_amenities(network,name)
        all_amenities.append([str(len(amenity_list)),name])
    for name in stops:
        if name not in amenities:
            amenity_list = list_network_amenities(network,name)
            all_amenities.append([str(len(amenity_list)),name])
    sub_list = all_amenities.copy()
    sub_list.sort()
    return(sub_list)


## PRINTS list_all_network_amenities IN A READABLE FASHION ##
def display_all_amenities(network):
    all_amenities = list_all_network_amenities(network)
    for amenity in all_amenities:
        print("{}x\t{}".format(amenity[0],amenity[1]))
        

## RETURNS A DICTIONARY OF A DEFAULT CARGO ITEM ##
## SIMILAR TO THE OTHER new_ FUNCTIONS ##
def new_cargo():
    return {
        "name": "default",
        "type": "default",
        "weight": 10,
        "value": 20,
        "origin": "",
        "destination": "",
    }


## TAKING new_cargo AND MODIFYING IT WITH INFORMATION TO MAKE IT USEFUL ##
def create_warehouse_crate(network,warehouse_location_name):
    cargo_list = []
    cargo = new_cargo()
    cargo["type"] = "Delivery"
    cargo["origin"] = warehouse_location_name
    destination = ["Warehouse",warehouse_location_name]
    while destination[1] == warehouse_location_name:
        destination = random_network_amenity(network,"Warehouse")
    cargo["destination"] = destination[1]
    cargo["name"] = "Delivery: bound for "+cargo["destination"]
    route = find_route(network,warehouse_location_name,cargo["destination"])
    cargo["distance"] = calculate_path_length(network,route)
    cargo["weight"] = random.randrange(20,100)
    #cargo["value"] = cargo["weight"]/4
    #cargo["value"] += cargo["distance"]/5
    cargo["value"] = (cargo["weight"])*(cargo["distance"])/200
    return(cargo)


## CHECKS CARGO TO SEE IF A VALID DELIVERY IS PRESENT ##
def complete_delivery(network,player,location_name):
    if len(player["vehicle"]["chassis"]["cabin"]["cargo"]) >= 1:
        for item in player["vehicle"]["chassis"]["cabin"]["cargo"]:
            destination_name = item["destination"]
            if item["type"] == "Delivery" and destination_name == location_name:
                string=("You have completed the delivery!  Well done!\n"+
                      "    Received $"+str(item["value"])+"!")
                print(string)
                player["currency"] += item["value"]
                player["travel_log"].append("  "+string)
                player["vehicle"]["chassis"]["cabin"]["cargo"].remove(item)
                return


## TAKES A new_cargo AND MODIFIES IT INTO A SCIENCE SAMPLE, WHICH IS STORED IN VEHICLE CARGO ##
def create_science_sample(network,player,stop_type,location_name):
    cargo = new_cargo()
    cargo["weight"] = 10
    cargo["value"] = 15
    cargo["type"] = "Science Samples"
    cargo["origin"] = stop_type+" of "+location_name
    cargo["name"] = cargo["type"]+" from "+cargo["origin"]
    return(cargo)
        
    
## CREATES A CONTRACT THAT IS ATTACHED TO PLAYER AND DESCRIBES WIN CONDITION FOR CONTRACT ##
## PLAYER CANNOT YET COMPLETE CONTRACT: FUNCTIONALITY NOT YET CREATED ##
def field_research_contract(network,start_town_name,player):
    science_stops = ["Plateau","Forest","Field","Volcano","Escarpment","Cave","Fissure"]
    stop_type = random.choice(science_stops)
    samples_needed = random.randrange(8,12)
    print("\n"+short_border)
    print("The University of {} needs {} samples from various {}s.".format(
        start_town_name,int(samples_needed),stop_type))
    cont = input("Accept this contract? (y/n) ")
    if cont == "y":
        player["field_research"] = {
            "origin": start_town_name,
            "stop_type": stop_type,
            "samples_needed": samples_needed,
            "samples_delivered": 0
        }
        string=("  Field Research contract accepted!\n"+
              "  Deliver to University of "+start_town_name+": "+str(samples_needed)+
              " samples from different "+stop_type+"s.\n")
        print(string)
        player["travel_log"].append(string)
    return

        
## REMOVE (end) or (start) FROM ROAD NAMES ##
def trim_road_connection_name(road_name):
    road_name=road_name.replace("(end)","")
    road_name=road_name.replace("(start)","")
    road_name=road_name.strip()
    return(road_name)


## CURRENT MAIN GAME LOOP ##
## SELECTS A RANDOM TOWN IN NETWORK, STARTS PLAYER THERE ##
def explore_test(network,player):
    start_town = random.choice(network["towns"])
    player["travel_log"].append("Starting in "+start_town["name"]+".")
    tank=player["vehicle"]["chassis"]["fuel_tank"]
    tank["fuel"]=tank["capacity"]
    display_town(start_town)
    player_select_road(network,start_town,player)
        
        
## FROM A TOWN, CHOOSE A RANDOM ROAD AND FOLLOW IT ##
def explore_random(network,start_town,player):
    print("\nStarting from {} ({} Amenities, {} Roads)".format(
        start_town["name"],len(start_town["amenities"]),len(start_town["roads"])))
    time.sleep(0.5)
    random_road_name=random.choice(start_town["roads"])
    random_road_name=trim_road_connection_name(random_road_name)
    road=find_road(network,random_road_name)
    if road["start"]==start_town["name"]:
        end_town_name=road["end"]
    elif road["end"]==start_town["name"]:
        end_town_name=road["start"]
    else:
        print("Something went wrong!  Couldn't find the town on other end of road!")
        return
    print("Taking {} towards {}".format(random_road_name,end_town_name))
    time.sleep(0.5)
    #print("Travelling {} km...".format(road["length"]))
    follow_road(network,road["name"],start_town["name"],player)
    #
    end_town=find_town(network,end_town_name)
    print("Arriving at {} ({} Amenities, {} Roads)".format(
        end_town["name"],len(end_town["amenities"]),len(end_town["roads"])))
    time.sleep(2)
    display_town(end_town)
    player_select_road(network,end_town,player)
    #player_chooses(network,end_town)
    return
        
        
## FROM A TOWN, EXPLORE THE PLAYER CHOSEN ROAD ##
def explore_chosen(network,start_town,end_town,player):
    road=connected_by(network,start_town["name"],end_town["name"])
    print("Taking {} towards {}".format(road["name"],end_town["name"]))
    time.sleep(0.5)
    print("Preparing to travel {} km...".format(road["length"]))
    follow_road(network,road["name"],start_town["name"],player)
    string = ("Arriving at {}{}{} ({} Amenities, {} Roads)".format(
        color.UNDERLINE,end_town["name"],color.END,len(end_town["amenities"]),len(end_town["roads"])))
    print(string)
    player["travel_log"].append(string)
    time.sleep(2)
    display_town(end_town)
    #print("{}Paths{}:".format(color.UNDERLINE,color.END))
    player_select_road(network,end_town,player)
    #player_chooses(network,end_town)
    return
    
    
## IN A TOWN, THIS IS THE MAIN LOOP FOR PLAYER INTERACTION ##
def player_select_road(network,start_town,player):
    destinations = connected_to(network,start_town["name"])
    destinationlist = []
    count=1
    for town_name in destinations:
        destinationlist.append([town_name,count])
        town=find_town(network,town_name)
        count+=1
    time.sleep(0.5)
    print("\n"+short_border+"\n")
    print("{}{}{} is connected to:".format(
        color.UNDERLINE,start_town["name"],color.END))
    for choice in destinationlist:
        end_town=find_town(network,choice[0])
        connecting_road=connected_by(network,start_town["name"],end_town["name"])
        print("{}: {} via {} ({}km)".format(
            str(choice[1]),str(choice[0]),connecting_road["name"],connecting_road["length"]))
        #print(str(choice[1])+": "+choice[0]+" via "+connecting_road["name"])
        #time.sleep(0.05)
    amenitieslist = []
    count=1
    for amenity_name in start_town["amenities"]:
        amenitieslist.append([amenity_name,count])
        count+=1
    time.sleep(0.2)
    print("\n{}Amenities{}:".format(color.UNDERLINE,color.END))
    for choice in amenitieslist:
        print("{}: {}".format(str(choice[1]),str(choice[0])))
        #time.sleep(0.05)
    
    summary_car(player["vehicle"])
    print("Currency: $"+str(round(player["currency"],2)))
    print("\n")
    time.sleep(0.5)
    player_choice=input("Will you:\n (e)xplore this town,\n (t)ake a path out of town,\n "+
                        "(c)ontinue at random,\n (r)efill your fuel tank,\n (v)iew your vehicle,\n "+
                        "read your travel (l)og, or\n (q)uit? ")
    if player_choice == "c":
        explore_random(network,start_town,player)
        
    elif player_choice == "t":
        path_choice = input("Which path will you take? (1-9) ")
        valid=False
        for choice in destinationlist:
            if str(path_choice)==str(choice[1]):
                print("\nYou have chosen "+choice[0]+"\n")
                time.sleep(0.5)
                end_town=find_town(network,choice[0])
                explore_chosen(network,start_town,end_town,player)
                valid=True
        if not valid:
            player_select_road(network,start_town,player)
        if valid:
            return
        
    elif player_choice == "e":
        amenity_choice = input("Which amenity will you use? (1-9) ")
        for choice in amenitieslist:
            if str(amenity_choice)==str(choice[1]):
                print("\nYou have chosen "+choice[0]+"\n")
                time.sleep(0.5)
                interact_with_stop(network,player,choice[0],start_town["name"])
        player_select_road(network,start_town,player)
        
    elif player_choice == "r":
        for amenity in start_town["amenities"]:
            if amenity=="Gas Station":
                gas_station = amenity
        interact_with_stop(network,player,gas_station,start_town["name"])
        player_select_road(network,start_town,player)
        
    elif player_choice == "v":
        display_vehicle(player["vehicle"])
        display_vehicle_durability(player["vehicle"])
        time.sleep(1)
        player_select_road(network,start_town,player)
        print("\n")
        
    elif player_choice == "l":
        print("\n"+short_border)
        for line in player["travel_log"]:
            print(line)
        print(short_border+"\n")
        i=input("Any key to continue ")
        player_select_road(network,start_town,player)
        
    elif player_choice == "q":
        return
    
    else:
        print("Invalid selection!")
        time.sleep(1)
        player_select_road(network,start_town,player)
    
    
## SELF-DESCRIPTIVE, RETURNS GALLONS PER MILE FOR GIVEN VEHICLE ##
def calculate_fuel_usage(vehicle):
    mpg = effective_mpg(vehicle)
    gpm = 1/mpg
    return(gpm)
    

## MAIN LOOP WHILE ON A ROAD ##
## INITIALIZES SOME VARIABLES, PERFORMS SOME BASIC SANITY CHECKS ##
## FIGUES OUT WHICH DIRECTION PLAYER IS COMING FROM, SETS ORDER/DISTANCE TO STOPS ##
## SEQUENCES ROAD SECTIONS TO PARSE TRAVEL DIRECTION AT EACH SECTION ##
def follow_road(network,road_name,start_town_name,player):
    driver = player["party"][0]
    road=find_road(network,road_name)
    player["travel_log"].append(" Followed "+road_name+" for "+str(road["length"])+"km.")
    reverse=False
    if road["start"]==start_town_name:
        reverse=False
    elif road["end"]==start_town_name:
        reverse=True
    else:
        print("Something went wrong!  Town not located on this road!")
        print("This usually happens when there are two roads with the same name")
        print("road_name: "+road_name)
        print("start_town: "+start_town_name)
        print("road['start']: "+road["start"])
        print("road['end']: "+road["end"])
        print("road['name']: "+road["name"])
        return
    path = []
    stops = []
    if not reverse:
        for section in road["sections"]:
            path.append(section)
        for stop in road["stops"]:
            stops.append(stop)
    else:
        for section in road["sections"]:
            newsection=section.copy()
            path.insert(0,newsection)
            path[0]["direction"]=u_turn(newsection["direction"])
        for stop in road["stops"]:
            newstop=stop.copy()
            stops.insert(0,newstop)
            distance=stops[0]["distance"]
            stops[0]["distance"]=road["length"]-distance
    for stop in stops:
        stop["e_distance"]=0
        stop["e_distance"]=(stop["distance"]-50)
        if stop["e_distance"] < 0:
            stop["e_distance"] = 0
    #
    sectionkm=[]
    kmcount=0
    for section in path:
        section["start"]=kmcount
        kmcount+=section["length"]
        section["end"]=kmcount
    #
    km=0
    kmmax=road["length"]
    start_town=find_town(network,road["start"])
    end_town=find_town(network,road["end"])
    current_section=""
    
    travel_speed_delay=travel_tick_rate(player)    
        
    fuel_tick = calculate_fuel_usage(player["vehicle"])
        
    ## MAIN LOOP START ##
    for km in range(0,kmmax):
        ## FIRST, CHECK FUEL USAGE ##
        no_fuel=False
        player["vehicle"]["chassis"]["fuel_tank"]["fuel"] -= fuel_tick
        ## IF NO FUEL, APPLY SLOW EFFET ##
        if player["vehicle"]["chassis"]["fuel_tank"]["fuel"] <= fuel_tick:
            max_speed=1
            no_fuel=True
            player["vehicle"]["chassis"]["fuel_tank"]["fuel"] = 0
        ## IF THERE IS FUEL, GIVE DRIVER XP ##
        else:
            skill = driver["skills"][0]
            skill["xp"] += 0.1
            if skill["xp"] >= 100:
                skill["xp"] -= 100
                skill["level"] += 1
                print("{}'s driving skill increased to {}!".format(driver["name"],str(skill["level"])))
        ## APPLY WEAR AND TEAR ##
        player["vehicle"] = wear_and_tear(player["vehicle"])
        ## DETERMINE TRAVEL SPEED ##
        travel_speed_delay=travel_tick_rate(player)
        for section in path:
            if (km >= section["start"]) & (km < section["end"]):
                current_section=section
        if not reverse:
            travel_gui(km,road,start_town,end_town,current_section,player)
        if reverse:
            travel_gui(km,road,end_town,start_town,current_section,player)
        if no_fuel:
            print("{}No fuel!!!{} Having to push car at minimum speed...\n".format(color.BOLD,color.END))
        for stop in stops:
            if (km >= stop["e_distance"]) & (km <= stop["distance"]):
                distance_to = stop["distance"] - km
                print("Approaching {} in {} km".format(stop["type"],distance_to))
            if km == stop["distance"]:
                print("Passed {} at {} km".format(stop["type"],stop["distance"]))
                #answer=stop_choice_timer(stop["type"])
                prompt="Stop here? "
                answer=None
                try:
                    answer = input_with_timeout(prompt, 3)
                except TimeoutExpired:
                    print("Continuing on...")
                else:
                    #print("Got %r" % answer)
                    pass
                if answer != None:
                    stop_here(network,stop,player,road_name)
                #time.sleep(1.2)
        time.sleep(travel_speed_delay)
    ## MAIN LOOP END ##
    
    for section in path:
        #print(section)
        pass
    for stop in stops:
        #print(stop)
        pass
    
    
## REDUCE DURABILITY OF PARTS DURING USE ##
def wear_and_tear(vehicle):
    # Roll for and apply damage on chassis
    rng=int(random.randrange(0,50)*vehicle["chassis"]["wear_rate"])
    if rng==0:
        vehicle["chassis"]["durability"] -= 1
    # Roll for and apply damage on parts
    for part in ["cabin","engine","fuel_tank"]:
        rng=int(random.randrange(0,50)*vehicle["chassis"][part]["wear_rate"])
        if rng==0:
            vehicle["chassis"][part]["durability"] -= 1
            step = vehicle["chassis"][part]["max_durability"]/100
            damage = vehicle["chassis"][part]["max_durability"] - vehicle["chassis"][part]["durability"]
            max_dur_damage_chance = step * damage
            roll = random.randrange(int(max_dur_damage_chance),100)
            if roll==max_dur_damage_chance:
                vehicle["chassis"][part]["max_durability"] -= 1
                print("Ping!")
        
    # Display damaged messages #    
    if vehicle["chassis"]["cabin"]["durability"] < 0:
        vehicle["chassis"]["cabin"]["durability"] = 0
        print(vehicle["chassis"]["cabin"]["model"]+" is very damaged!")
    if vehicle["chassis"]["engine"]["durability"] < 0:
        vehicle["chassis"]["engine"]["durability"] = 0
        print(vehicle["chassis"]["engine"]["model"]+" is very damaged!")
    if vehicle["chassis"]["fuel_tank"]["durability"] < 0:
        vehicle["chassis"]["fuel_tank"]["durability"] = 0
        print(vehicle["chassis"]["fuel_tank"]["model"]+" is very damaged!")
    return(vehicle)


## APPLY WEAR AND TEAR TO ALL PARTS ON GIVEN VEHICLE ##
def make_car_old(vehicle):
    new_dur = random.randrange(30,60)
    vehicle["chassis"]["max_durability"] = new_dur
    vehicle["chassis"]["durability"] = new_dur
    for part in ["cabin","engine","fuel_tank"]:
        new_dur = random.randrange(30,60)
        vehicle["chassis"][part]["max_durability"] = new_dur
        vehicle["chassis"][part]["durability"] = new_dur
    return(vehicle)


## APPLY WEAR AND TEAR TO A SINGLE GIVEN PART ##
def make_part_old(part):
    new_dur = random.randrange(30,60)
    if part["type"] == "chassis":
        part["max_durability"] = new_dur
        part["durability"] = new_dur
    elif part in ["cabin","engine","fuel_tank"]:
        new_dur = random.randrange(30,60)
        part["max_durability"] = new_dur
        part["durability"] = new_dur
    return(part)


## DETERMINE HOW QUICKLY EACH TRAVEL TICK OCCURS IN SECONDS ##
def travel_tick_rate(player):
    no_fuel = False
    max_speed=calculate_max_speed(player["vehicle"])
    if player["vehicle"]["chassis"]["fuel_tank"]["fuel"] <= 0:
        max_speed=1
        #print("{}No fuel!!!{} Having to push car at minimum speed...\n".format(color.BOLD,color.END))
        
    travel_speed=(1/max_speed)*5
    travel_speed = enforce_min_max(travel_speed,0.005,0.25)
    
    if (travel_speed <= 0.25) & (travel_speed >= 0.005):
        travel_speed_delay=travel_speed
        #print("Time delay: "+str(travel_speed)+" for "+str(max_speed)+" kmh")
    return(travel_speed_delay)
    
    
## MAKE SURE A GIVEN VALUE FALLS BETWEEN MINIMUM AND MAXIMUM AND RETURN IT ##
def enforce_min_max(value,minimum,maximum):
    if value > maximum:
        value = maximum
    if value < minimum:
        value = minimum
    return(value)


## WHAT THE PLAYER SEES WHILE TRAVELLING ON A ROAD ##
def travel_gui(km,road,start_town,end_town,current_section,player):
    heading=direction(current_section["direction"]).split()[-1]
    fuel_tick = calculate_fuel_usage(player["vehicle"])
    max_speed=calculate_max_speed(player["vehicle"])
    travel_tick = travel_tick_rate(player)
    if player["vehicle"]["chassis"]["fuel_tank"]["fuel"] == 0:
        max_speed = 1
        fuel_tick = 0
    x=os.system('clear')
    print(long_border)
    print("Travelling {} on {}{}{} from {} to {}".format(
        heading,color.BOLD,road["name"],color.END,start_town["name"],end_town["name"]))
    print("Distance: "+str(km+1)+" / "+str(road["length"])+" km \tat "+str(max_speed)+" kmh ("+
         str(round(travel_tick,4))+" tick rate)")
    print("Fuel: {} / {} gallons of fuel remaining ({} per km)".format(
        str(round(player["vehicle"]["chassis"]["fuel_tank"]["fuel"],2)), 
        str(player["vehicle"]["chassis"]["fuel_tank"]["capacity"]),
        str(round(fuel_tick,3))))
    print("Currency: $"+str(round(player["currency"],2)))
    print(long_border)


## REQUIRED FOR TIMED INPUT ##
class TimeoutExpired(Exception):
    pass
                   
                   
## REQUIRED FOR TIMED INPUT ##
## I NEED TO STUDY MORE ON THIS: I DON'T 100% GET HOW/WHY IT WORKS ##
def input_with_timeout(prompt,timeout,timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    raise TimeoutExpired
    

## TAKE A new_road AND MODIFY IT INTO A USABLE STATE ##
## ADD SECTIONS AND STOPS AS PER FORMULA ##
def build_road():
    road=new_road()
    namestring = random.choice(names) + " " + random.choice(street_types)
    road["name"] = namestring
    total_length = 0
    sections = random.randrange(3,12)
    for section in range(0,sections):
        newsection = new_road_section()
        total_length += newsection["length"]
        road["sections"].append(newsection)
    road_stops = random.randrange(0,4)+(sections/3)
    for stop in range(0,int(road_stops)):
        newstop = new_stop()
        distance = random.randrange(2,total_length-2)
        newstop["distance"] = distance
        road["stops"].append(newstop)
    newlist=sorted(road["stops"], key=lambda d: d["distance"])
    road["stops"]=newlist
    road["length"] = total_length
    #display_road(road)
    return(road)


## SELF-DESCRIPTIVE: GIVEN ROAD, CREATE A NEW NAME FROM NAME AND STREET_TYPE LISTS ##
def assign_random_road_name(road):
    namestring = random.choice(names) + " " + random.choice(street_types)
    road["name"] = namestring
    
    
## SELF-DESCRIPTIVE: MAKE A TOWN AND A ROAD, ADD ANOTHER TOWN TO THE OTHER END OF THE ROAD ##
## BOOM, A VERY BASIC ROAD NETWORK ##
def build_road_network():
    network = {
        "towns":[],
        "roads":[]
    }
    start_town=build_town()
    end_town=build_town()
    while end_town["name"]==start_town["name"]:
        end_town=build_town()
    road=build_road()
    connect_road(start_town,end_town,road)
    network["roads"].append(road)
    network["towns"].append(start_town)
    network["towns"].append(end_town)
    augment_network(network)
    summary_network(network)
    return(network)


## LIKE build_road_network, BUT WITH MORE TOWNS AND ROADS
def build_big_road_network():
    network=build_road_network()
    augmentations=random.randrange(16,32)
    connections=random.randrange(24,48)
    count=0
    for count in range(0,augmentations):
        augment_network(network)
    count=0
    for count in range(0,connections):
        connect_towns(network)
    augment_network(network)
    return(network)


## ALSO LIKE build_road_network, BUT WITH WAAAY MORE TOWNS AND ROADS ##
def build_mega_road_network():
    network=build_road_network()
    augmentations=random.randrange(40,64)
    connections=random.randrange(32,48)
    count=0
    for count in range(0,augmentations):
        augment_network(network)
    count=0
    for count in range(0,connections):
        connect_towns(network)
    augment_network(network)
    return(network)
    

## GIVEN A NETWORK, ADD A NEW TOWN AND CONNECT IT WITH A NEW ROAD TO AN EXISTING TOWN ##
def augment_network(network):
    newtown = build_town()
    newroad = build_road()
    townnamelist=compile_townnamelist(network)
    roadnamelist=compile_roadnamelist(network)
    while newroad["name"] in roadnamelist:
        assign_random_road_name(newroad)
    while newtown["name"] in townnamelist:
        newtown = build_town()
    start_town=random.choice(network["towns"])
    connect_road(start_town,newtown,newroad)
    network["roads"].append(newroad)
    network["towns"].append(newtown)
    summary_network(network)
    
    
## COMPILE A LIST OF ALL ROAD NAMES IN THE NETWORK ##
## USED TO PREVENT DUPLICATE ROAD NAMES ##
def compile_roadnamelist(network):
    roadnamelist=[]
    for road in network["roads"]:
        roadnamelist.append(road["name"])
    roadnamelist.sort()
    for road in roadnamelist:
        #print(road)
        pass
    return(roadnamelist)
    
    
## COMPILE A LIST OF ALL TOWN NAMES IN THE NETWORK ##
## USED TO PREVENT DUPLICATE TOWN NAMES ##
def compile_townnamelist(network):
    townnamelist=[]
    for town in network["towns"]:
        townnamelist.append(town["name"])
    townnamelist.sort()
    for town in townnamelist:
        #print(town)
        pass
    return(townnamelist)
    
    
## SELF-DECRIPTIVE: TAKE A NEW ROAD AND roadnamelist AND CHECK FOR DUPLICATES ##
def check_duplicate_road_name(network,road_name):
    roadnamelist=[]
    for road in network["roads"]:
        roadnamelist.append(road["name"])
    while road_name in roadnamelist:
        print("Duplicate found!  Randomizing name")
        assign_random_road_name(road_name)
    return(road_name)
    
    
## TAKE TWO TOWNS(REFERENCED BY NAME) AND CONNECT THEM WITH A NEW ROAD ##
def connect_road(start_town,end_town,road):
    road["start"]=start_town["name"]
    road["end"]=end_town["name"]
    start_town["roads"].append(road["name"]+" (start)")
    end_town["roads"].append(road["name"]+" (end)")
    
    
## TAKE TWO RANDOM TOWNS(REFERENCED BY NAME) AND CONNECT THEM WITH A ROAD BY CALLING connect_road ##
def connect_towns(network):
    newroad = build_road()
    roadnamelist=compile_roadnamelist(network)
    while newroad["name"] in roadnamelist:
        assign_random_road_name(newroad)
    if len(network["towns"]) < 3:
        print("Not enough towns!")
        return
    start_town = ""
    end_town = ""
    while start_town == end_town:
        start_town=random.choice(network["towns"])
        end_town=random.choice(network["towns"])
    
    newroad["start"]=start_town["name"]
    newroad["end"]=end_town["name"]
    newroad_townlist = [newroad["start"],newroad["end"]]
    #newroad_townlist.sort()
    for road in network["roads"]:
        townlist=[road["start"],road["end"]]
        #townlist.sort()
        #print("Townlist: "+str(townlist)+
        #      "\nNewRoad Townlist: "+str(newroad_townlist))
        #time.sleep(0.01)
        townlist.sort()
        newroad_townlist.sort()
        if (townlist==newroad_townlist):
            #print("DUPLICATE ROAD DETECTED!")
            #print("RESTARTING connect_towns FUNCTION")
            newroad=""
            roadnamelist=""
            start_town=""
            end_town=""
            newroad_townlist=""
            townlist=""
            #time.sleep(1)
            connect_towns(network)
            return
    
    connect_road(start_town,end_town,newroad)
    network["roads"].append(newroad)
    #print("Connected {} to {}".format(start_town["name"],end_town["name"]))
    #summary_network(network)
    #print("\n")
    
    
## PRINT A SORTED LIST OF ALL ROAD NAMES IN THE NETWORK ##
def roadlist_sorted(network):
    roadlist = []
    for road in network["roads"]:
        roadlist.append(road["name"])
    roadlist.sort()
    for road in roadlist:
        print(road)
    
## DISPLAY ENTIRE ROAD NETWORK IN READABLE FASHION ##
def display_network(network):
    towns=len(network["towns"])
    roads=len(network["roads"])
    for town in network["towns"]:
        display_town(town)
    for road in network["roads"]:
        display_road(road)
    print("{} Towns\n{} Roads".format(towns,roads))
    
    
## LIKE display_network BUT WITH LESS INFO PER TOWN ##
def summary_network(network):
    print("\n--- Summary ---")
    for road in network["roads"]:
        summary_road(road)
    print("---")
    for town in network["towns"]:
        summary_town(town)
    towns=len(network["towns"])
    roads=len(network["roads"])
    print("\n{} Towns\n{} Roads\n".format(towns,roads))
    
    
## PRINT A BRIEF DESCRIPTION OF GIVEN ROAD ##
def summary_road(road):
    print("{}: {}km: {} to {}".format(road["name"],road["length"],road["start"],road["end"]))
    
    
## PRINT A VERBOSE DESCRIPTION OF GIVEN ROAD ##
def display_road(road):
    print("\n")
    print(road["name"])
    print("{} km, {} sections".format(road["length"],len(road["sections"])))
    print("Starts at {}{}{}, ends at {}{}{}".format(
        color.BOLD,road["start"],color.END,color.BOLD,road["end"],color.END))
    speed_limit = road["sections"][0]["speed_limit"]
    hours = 0
    for section in road["sections"]:
        section_hours = section["length"]/section["speed_limit"]
        hours += section_hours
    print("{} hours to complete the journey at speed limit (average {} kmh)".format(
        round(hours,2),(round(road["length"]/hours,2))))
    count=1
    for section in road["sections"]:
        print("Section {}:\t{} degrees\t{} for {} km at {} kmh".format(
            count,section["direction"],direction(section["direction"]).split()[-1],
            section["length"],section["speed_limit"]))
        count+=1
    print("\n{}Stops{}:".format(color.UNDERLINE,color.END))
    for stop in road["stops"]:
        print("{} at {}km".format(stop["type"],stop["distance"]))
    print("\n")
    
    
## DISPLAY A GIVEN ROAD SECTION (NOT HOOKED UP YET OBVS) ##
def display_section(section):
    pass
    
    
## GIVEN ROAD NAME, RETURN ROAD ITSELF ##
def find_road(network,road_name):
    for road in network["roads"]:
        if road["name"]==road_name:
            #display_road(road)
            return(road)

            
## GIVEN TOWN NAME, RETURN TOWN ITSELF ##            
def find_town(network,town_name):
    for town in network["towns"]:
        if town["name"]==town_name:
            #display_town(town)
            return(town)
    
    
## MAKE SURE COMPASS HEADING IS IN LOGICAL RANGE ##
def fix_heading(heading):
    if heading < 0:
        heading = 0
    while heading >= 360:
        heading -= 360
    return(heading)
    

## RETURNS THE OPPOSITE OF CURRENT HEADING ##
def u_turn(heading):
    newheading = heading + 180
    newheading = fix_heading(newheading)
    #print("Flipped a U-turn!\nWas headed {}, now headed {}".format(
    #    direction(heading).split()[-1],direction(newheading).split()[-1]))
    return(newheading)
    
    
## RETURNS VERBOSE DESCRIPTION OF DIRECTION OF TRAVEL ##
def direction(heading):
    direction = ""
    #Make sure heading int is in expected range: if not, reduce until it is!
    while heading >= 360:
        heading-=360
    if ((heading >= 0) & (heading < 23)):
        direction = "North"
    elif ((heading >= 23) & (heading < 68)):
        direction = "North-East"
    elif ((heading >= 68) & (heading < 113)):
        direction = "East"
    elif ((heading >= 113) & (heading < 158)):
        direction = "South-East"
    elif ((heading >= 158) & (heading < 203)):
        direction = "South"
    elif ((heading >= 203) & (heading < 248)):
        direction = "South-West"
    elif ((heading >= 248) & (heading < 293)):
        direction = "West"
    elif ((heading >= 293) & (heading < 338)):
        direction = "North-West"
    elif ((heading >= 338) & (heading < 360)):
        direction = "North"
    else:
        direction = "Invalid"
    #Return a verbose string with heading and direction    
    return("A heading of {} degrees is {}".format(heading,direction))
    
    
    
    
    
    
    
    
    
## -- RANDOM FUNCTIONS -- ##


## PICK A RANDOM PART FROM PART LIST, MAKE IT OLD ##
def salvage_random_part():
    categories = []
    for category in parts:
        categories.append(category)
    category = random.choice(categories)
    part = random.choice(parts[category])
    part = make_part_old(part)
    part["durability"] = random.randrange(5,part["max_durability"])
    return(part)


def gas_station(player):
    print("You have ${}".format(round(player["currency"],2)))
    fuel_price = round(random.uniform(1.2,2.4),2)
    fill_fuel_tank(player,fuel_price)
        

def farm(player):
    work_available=False
    rng = random.randrange(0,2)
    pay = random.randrange(2,7)
    if rng == 0:
        work_available=True
    if work_available:
        choice = input("You can work a few hours in the field for ${}.  Deal?  (y/n) ".format(str(pay)))
        if choice == "y":
            print("You work a few hours and earn ${}".format(str(pay)))
            player["currency"] += pay
        else:
            print("Carry on, then")
    else:
        print("Sometimes day work is available at places like this")
            
            
def repair_vehicle(player):
    print("You can get your car maintained or fixed here")
    vehicle = player["vehicle"]
    chas = vehicle["chassis"]
    repair_total = 0
    damage = 0
    cont = input("Have the mechanic take a look at your vehicle? (y) ")
    if cont == "y":
        display_vehicle_durability(vehicle)
        time.sleep(1)
    else:
        return
    partslist = ["engine","cabin","fuel_tank"]
    print(short_border)
    for pname in partslist:
        damage = chas[pname]["max_durability"] - chas[pname]["durability"]
        repair_total += damage
        part = chas[pname]
        print("{} {} has taken {} damage since last repaired".format(
                part["brand"],part["model"],damage))
    damage = vehicle["chassis"]["max_durability"] - vehicle["chassis"]["durability"]
    print("{} {} has taken {} damage since last repaired".format(
            vehicle["chassis"]["brand"],vehicle["chassis"]["model"],damage))
    repair_total += damage
    repair_total = round(repair_total/4,2)
    print(short_border)
    if damage == 0:
        print("Your vehicle is in pretty good condition already!  No repairs needed.\n")
        time.sleep(0.5)
        return
    if player["currency"] < repair_total:
        print("You don't have enough money to repair the whole car!")
        return
    cont = input("Repair damaged parts for ${}? (y/n) ".format(repair_total))
    if cont == "y":
        player["currency"] -= repair_total
        if vehicle["chassis"]["durability"] != vehicle["chassis"]["max_durability"]:
            diff = int((vehicle["chassis"]["max_durability"] - vehicle["chassis"]["durability"])/20)
            if diff < 1:
                diff = 1
            vehicle["chassis"]["max_durability"] -= diff
            vehicle["chassis"]["durability"] = vehicle["chassis"]["max_durability"]
        part=""
        for part in ["engine","cabin","fuel_tank"]:
            if vehicle["chassis"][part]["durability"] != vehicle["chassis"][part]["max_durability"]:
                diff = int((vehicle["chassis"][part]["max_durability"] - vehicle["chassis"][part]["durability"])/30)
            if diff < 1:
                diff = 1
            vehicle["chassis"][part]["max_durability"] -= diff
            vehicle["chassis"][part]["durability"] = vehicle["chassis"][part]["max_durability"]
    else:
        return
    display_vehicle_durability(player["vehicle"])
    time.sleep(1)
        
        
        
def junkyard(player):
    print("You can search for salvage parts here with a skilled mechanic")
    mechanic_present=False
    sublist = []
    for character in player["party"]:
        if character["job"] == "Mechanic":
            mechanic_present=True
            sublist.append(character)
    if mechanic_present:
        #scientist = random.choice(sublist)
        choice=input("Search for salvagable parts? (y/n) ")
        if choice=="y":
            for mechanic in sublist:
                rng = random.randrange(0,5)-(mechanic["skills"][0]["level"]/2)
                if rng<=0:
                    part = salvage_random_part()
                    salvage_factor = 10-(mechanic["skills"][0]["level"])
                    if salvage_factor < 1:
                        salvage_factor = 1
                    value = round(part["value"]/salvage_factor,2)
                    print("{} found a {} {}, worth ${}!".format(
                            mechanic["name"],part["brand"],part["model"],value))
                    cont=input("(S)ell it or try to (i)nstall it in your vehicle? ")
                    try:
                        cont=cont.lower()
                    except:
                        pass
                    if cont == "i":
                        part_copy=part.copy()
                        player["vehicle"],part = replace_part(player["vehicle"],part)
                        if part_copy != part:
                            if part == "":
                                print("Installed {}!".format(part["type"]))
                                return
                            value = int(round(part["value"]/4,2))
                            print("Replaced the {} and sold the old one for {}!  Now at ${}".format(
                                part["type"],value,player["currency"]))
                            player["currency"] += value
                            return
                    player["currency"] += value
                    print("Sold!  Now at ${}".format(player["currency"]))
                else:
                    print("{} failed to find anything worthwhile".format(mechanic["name"]))
                for skill in mechanic["skills"]:
                    skill["xp"] += 10
                    if skill["xp"] >= 100:
                        skill["xp"] -= 100
                        skill["level"] += 1
                    display_character(mechanic)
                        
                        
def science_stop(network,player,stop,location_name):
        print("You can conduct field research here with a skilled scientist")
        scientist_present=False
        sublist = []
        for character in player["party"]:
            if character["job"] == "Scientist":
                scientist_present=True
                sublist.append(character)
        if scientist_present:
            #scientist = random.choice(sublist)
            choice=input("Attempt to gather samples? (y/n) ")
            if choice=="y":
                for scientist in sublist:
                    rng = random.randrange(0,2)-(scientist["skills"][0]["level"]/2)
                    if rng<=0:
                        #value=random.randrange(16,26)+scientist["skills"][0]["level"]
                        print("\n{} successfully gathered samples!  ".format(scientist["name"]))
                        #print("Converting directly to ${} cash for now".format(value))
                        cargo = create_science_sample(network,player,stop,location_name)
                        print(cargo)
                        player["vehicle"]["chassis"]["cabin"]["cargo"].append(cargo)
                        #player["currency"] += value
                    else:
                        print("\n{} failed to gather samples.  Better luck next time.".format(
                            scientist["name"]))
                    for skill in scientist["skills"]:
                        skill["xp"] += 10
                        if skill["xp"] >= 100:
                            skill["xp"] -= 100
                            skill["level"] += 1
                        display_character(scientist)
                        
                        
                        
def racetrack(player):
        print("You can earn currency here with a skilled driver")
        driver_present=False
        sublist = []
        for character in player["party"]:
            if character["job"] == "Driver":
                driver_present=True
                sublist.append(character)
        if driver_present:
            driver = random.choice(sublist)
            choice=input("Attempt to race? (y/n) ")
            if choice=="y":
                drivers = random.randrange(7,13)
                rng = random.randrange(0,drivers)
                print("\nRace is starting with {} racers!\n".format(drivers+1))
                if rng==0:
                    print(driver["name"]+" finished first!! Incredible!!  You win top prize: $100!")
                    player["currency"] += 100
                elif rng==1:
                    print(driver["name"]+" finished in second place!  You win podium prize: $20")
                    player["currency"] += 20
                elif rng==2:
                    print(driver["name"]+" finished in third place!  You win podium prize: $20")
                    player["currency"] += 20
                else:
                    print("{} finished the race in position {}.  Better luck next time!".format(
                        driver["name"],str(rng+1)))
                for skill in driver["skills"]:
                    skill["xp"] += 10
                    if skill["xp"] >= 100:
                        skill["xp"] -= 100
                        skill["level"] += 1
                    display_character(driver)
                    
                    
                    
def warehouse(network,player,location_name):
        print(short_border)
        print("You can accept or complete delivery contracts at places like this")
        for item in player["vehicle"]["chassis"]["cabin"]["cargo"]:
            if item["destination"] == location_name:
                print("Ah, looks like you have a delivery for us.")
                complete_delivery(network,player,location_name)
                player["travel_log"].append("  Delivered {} from {}".format(item["name"],item["origin"]))
        choice = input("Take on a new delivery? (y/n) ")
        if choice != "y":
            return
        choice_list = []
        items = random.randrange(3,6)
        for i in range(1,items+1):
            cargo = create_warehouse_crate(network,location_name)
            choice_list.append([i,cargo])
        for item in choice_list:
            index=str(item[0])
            cargo=item[1]
            print("{}: {}, {}kg, {}km,\t${}".format(
                index,cargo["name"],str(cargo["weight"]),str(cargo["distance"]),str(cargo["value"])))
        cont = input("Which delivery do you want to take? (1-9) ")
        for item in choice_list:
            if cont==str(item[0]):
                #index=str(item[0])
                cargo=item[1]
                player["vehicle"]["chassis"]["cabin"]["cargo"].append(cargo)
                print("You've loaded the cargo into your vehicle.  Good luck!")
                route = find_route(network,location_name,cargo["destination"])
                print("By the way, try this route:")
                print(route)
                player["travel_log"].append("  {} to {}".format(cargo["name"],cargo["destination"]))
                player["travel_log"].append("  "+str(route)+"\n")
        print(short_border)
    
    
    
def auto_shop(player):
        print("You can purchase vehicle resources and new components here")
        part_count = random.randrange(3,6)
        parts_list = []
        count=1
        part_type_list = ["Engine","Cabin","Turbo","Fuel Tank"]
        for i in range(0,part_count):
            part_type = random.choice(part_type_list)
            part_type = part_type.lower().replace(" ","_")
            new_part = random.choice(parts[part_type])
            parts_list.append([new_part,count])
            count += 1
        print(long_border)
        for part_boxed in parts_list:
            part = part_boxed[0]
            count = part_boxed[1]
            print("{}: ${}\t{} {} {}".format(
                count,part["value"],part["brand"],part["model"],part["type"]))
        print(short_border)
        choice = "a"
        while choice != "":
            choice=input("Wanna take a closer look at any of these parts? (1-9) ")
            for part_boxed in parts_list:
                if choice == str(part_boxed[1]):
                    if not part_compatible_with(player["vehicle"],part_boxed[0]):
                        display_part(part_boxed[0])
                        print("This part is not compatible with your vehicle!")
                        return
                    part2 = match_vehicle_part(player["vehicle"],part_boxed[0])
                    compare_parts(part_boxed[0],part2)
                    cont=input("Want to purchase this part and install it on your vehicle? (y/n) ")
                    if cont=="y":
                        if player["currency"] < part_boxed[0]["value"]:
                            print("You don't have enough money!")
                            return
                        else:
                            player["currency"] -= part_boxed[0]["value"]
                            player["vehicle"],part_boxed[0] = replace_part(player["vehicle"],part_boxed[0])
            if choice == "":
                break
        return
    
    
        
        
## MAIN LOOP FOR INTERACTING WITH STOPS OR AMENITIES ##
## OUTCOME DIFFERS BASED ON STOP NAME AND LOCATION ##
## TO BE SPLIT INTO DISCRETE FUNCTIONS BASED ON STOP TYPE ##
def interact_with_stop(network,player,stop,location_name):
    if stop == "Gas Station":
        gas_station(player)
        
    elif stop == "Farm":
        farm(player)
            
    elif stop == "Garage" or stop == "Repair Shop":
        repair_vehicle(player)
        
    elif stop == "Junkyard" or stop == "Salvage Yard":
        junkyard(player)
        
    elif stop == "Plateau" or stop == "Volcano" or stop == "Field" or stop == "Forest" or stop == "Escarpment" or stop == "Fissure" or stop == "Cave":
        science_stop(network,player,stop,location_name)
                    
    elif stop == "Intersection":
        print("A side road starts here.  It does not lead to a town.")
        
    elif stop == "Campsite" or stop == "Rest Stop":
        print("You can park here and rest for a while")
        
    elif stop == "Racetrack":
        racetrack(player)
        
    elif stop == "Warehouse":
        warehouse(network,player,location_name)
        
    elif stop == "Auto Shop" or stop == "Parts Store":
        auto_shop(player)
        
    elif stop == "Convenience Store":
        print("You can purchase food and other human resources here")
        
    elif stop == "Casino":
        print("You can bet currency here and try to win big")
        
    elif stop == "Library" or stop == "Museum":
        print("You can Study to earn a bit of xp for your skills here")
        print("You can also sell various Science Samples for currency")
        cash_offer = 0
        cargo_list = player["vehicle"]["chassis"]["cabin"]["cargo"].copy() 
        for item in player["vehicle"]["chassis"]["cabin"]["cargo"]:
            if item["type"] == "Science Samples":
                cont = input("Sell {} for ${}? (y/n) ".format(item["name"],item["value"]))
                if cont == "y":
                    player["currency"] += item["value"]
                    cargo_list.remove(item)
                    #print(cargo_list)
        player["vehicle"]["chassis"]["cabin"]["cargo"] = cargo_list
        print(short_border)

    elif stop == "University":
        field_research_contract(network,location_name,player)
        
    elif stop == "Car Lot":
        print("You can exchange your current vehicle (plus cash) for a different one here")
        car_lot()
        
    else:
        print("What the hell is this place?  It's not listed in my atlas...")
			
			
# GIVEN A VEHICLE AND A SPARE PART, FIND MATCHING PART IN VEHICLE			
def match_vehicle_part(vehicle,part1):
	chassis_parts = ["Engine","Cabin","Fuel Tank"]
	part_type = part1["type"]
	if part_type == "Chassis":
		part2 = vehicle["chassis"]
	elif part_type in chassis_parts:
		part2 = vehicle["chassis"][part_type.lower().replace(' ','_')]
	elif part_type == "Turbo":
		try:
			part2 = vehicle["chassis"]["engine"]["turbo"]
		except:
			part2 = ""
	else:
		print("This part cannot be matched!")
	return(part2)
			
			
## COMPARES TWO SIMILAR PARTS AND HIGHLIGHTS DIFFERENCES ##
def compare_parts(part1,part2):
    if part1 == "" or part2 == "":
        print("One of these parts is blank!")
        return
    if part1["type"] != part2["type"]:
        print("These parts are dissimilar.  Cannot compare them!")
        return
    for part in [part1,part2]:
        try:
            display_part(part)
        except:
            pass
        
        
## PRINTS A VERBOSE DESCRIPTION OF GIVEN PART ##
def display_part(part):
    print(short_border)
    print("{}{} {} {}{}\nSize: {} | Value: ${} | Weight: {}kg".format(
        color.BOLD,part["brand"],part["model"],part["type"],color.END,
        part["size"],part["value"],part["weight"]))
    print("{} / {} durability\n".format(part["durability"],part["max_durability"]))
    if part["type"] == "Engine":
        print("{} hp, {} torque".format(part["base_horsepower"],part["base_torque"]))
    elif part["type"] == "Turbo":
        print("{} hp factor, {} torque factor, {} mpg factor".format(
            part["horsepower_factor"],part["torque_factor"],part["mpg_factor"]))
    elif part["type"] == "Cabin":
        print("{} seats, {} kg of cargo space".format(part["passengers"],str(part["max_cargo"])))
    elif part["type"] == "Fuel Tank":
        print("{} liter capacity".format(str(part["capacity"])))
    print(short_border+"\n")
    
        # THIS DATA FOR REFERENCE ONLY
        #{"brand": "Yolo",
        # "model": "Hurricane",
        # "type": "Turbo",
        # "value": 750,
        # "size": 1,
        # "weight": 50,
        # "horsepower_factor": 1.2,
        # "torque_factor": 1.2,
        # "mpg_factor": 0.6,
        # "durability": 100,
        # "max_durability": 100
        #},
        
        
## CALLED WHEN PLAYER INITIATES A STOP DURING follow_road ##
def stop_here(network,stop,player,road_name):
    print("What a lovely place to stop, this {}!".format(stop["type"]))
    interact_with_stop(network,player,stop["type"],road_name)
    input("Any input to continue: ")
        
        
## GIVEN PLAYER CURRENCY AND VEHICLE, ATTEMPT TO FILL FUEL TANK ##
## IF CURRENCY LOW, FILL AS MUCH AS POSSIBLE ##
def fill_fuel_tank(player,price):
    print("This Gas Station sells fuel for ${} per gallon".format(price))
    capacity = player["vehicle"]["chassis"]["fuel_tank"]["capacity"]
    current_fuel = player["vehicle"]["chassis"]["fuel_tank"]["fuel"]
    amount_to_fill = capacity - current_fuel
    cost_to_fill = round((amount_to_fill * price),2)
    print("It will cost ${} to fill up with {} gallons".format(cost_to_fill,str(round(amount_to_fill,2))))
    confirm = input("Fill up here? (y/n) ")
    if confirm != "y":
        return
    if cost_to_fill > player["currency"]:
        print("Not enough money to fill up!\nWill fill as much as possible")
        amount_to_fill = player["currency"] / price
        cost_to_fill = round((amount_to_fill * price),2)
    player["currency"] -= cost_to_fill
    if player["currency"] < 0:
        player["currency"] = 0
    player["vehicle"]["chassis"]["fuel_tank"]["fuel"] += amount_to_fill
    if player["vehicle"]["chassis"]["fuel_tank"]["fuel"] > player["vehicle"]["chassis"]["fuel_tank"]["capacity"]:
        player["vehicle"]["chassis"]["fuel_tank"]["fuel"] = player["vehicle"]["chassis"]["fuel_tank"]["capacity"]
    print("\nFilled up fuel tank!")
    print("Currency remaining: ${}".format(round(player["currency"],2)))
    time.sleep(1)
    summary_car(player["vehicle"])
    print("\n")
    
    
## PRINT DURABILITY OF ALL VEHICLE PARTS ##
def display_vehicle_durability(vehicle):
    chas=vehicle["chassis"]
    eng=chas["engine"]
    cab=chas["cabin"]
    tank=chas["fuel_tank"]
    print("\n")
    for part in [chas,eng,cab,tank]:
        print("{} {} has {} / {} durability".format(
            part["brand"],part["model"],part["durability"],part["max_durability"]))
    

## DEFAULT PLAYER OBJECT ##
def new_player():
    vehicle = build_vehicle()
    party = []
    for seat in vehicle["chassis"]["cabin"]["seats"]:
        party.append(seat["characters"])
    summary_car(vehicle)
    return {
        "name": "Team "+random.choice(party_names),
        "vehicle": vehicle,
        "party": party,
        "currency": 100,
        "reputation": 0,
        "travel_log": [],
    }
    
    
## GIVEN A VEHICLE, RETURNS TOTAL VEHICLE WEIGHT ##
def calculate_weight(vehicle):
    passenger_weight = 0
    chas = vehicle["chassis"]
    cab = vehicle["chassis"]["cabin"]
    eng = vehicle["chassis"]["engine"]
    tank = vehicle["chassis"]["fuel_tank"]
    for seat in cab["seats"]:
        passenger_weight+=seat["weight"]
        try:
            passenger_weight+=seat["characters"]["weight"]
        except:
            pass
    weight = cab["weight"] + chas["weight"] + eng["weight"] + tank["weight"] + tank["fuel"] + passenger_weight
    try:
        for item in cab["cargo"]:
            weight += item["weight"]
    except:
        pass
    return(weight)


## GIVEN A VEHICLE, ATTEMPTS TO CALCULATE TOTAL VEHICLE VALUE BASED ON PART VALUES ##
def calculate_vehicle_value(vehicle):
    total_value = 0
    total_value += vehicle["chassis"]["value"]*(vehicle["chassis"]["max_durability"]/100)
    try:
        total_value += vehicle["chassis"]["cabin"]["value"]*(vehicle["chassis"]["cabin"]["max_durability"]/100)
        for seat in vehicle["chassis"]["cabin"]["seats"]:
            total_value += seat["value"]
    except:
        pass
    
    try:
        total_value += vehicle["chassis"]["engine"]["value"]*(vehicle["chassis"]["engine"]["max_durability"]/100)
        try:
            total_value += vehicle["chassis"]["engine"]["turbo"]["value"]*(vehicle["chassis"]["engine"]["turbo"]["max_durability"]/100)
        except:
            pass
    except:
        pass
    
    try:
        total_value += vehicle["chassis"]["fuel_tank"]["value"]*(vehicle["chassis"]["fuel_tank"]["max_durability"]/100)
    except:
        pass
    
    return(total_value)


## BORE AND STROKE LISTED IN INCHES, RETURNS CC OF ENGINE
## 88.98 WAS CALCULATED FROM FORMULA
def calculate_engine_displacement(engine):
    displacement  = engine['bore']*engine['stroke']*engine['cylinders']
    displacement = displacement*88.98
    return(displacement)


## FUNCTIONING VEHICLE BUT WITH NO CHARACTERS APPENDED ##
def build_empty_vehicle():
    vehicle = build_vehicle()
    for seat in vehicle["chassis"]["cabin"]["seats"]:
        seat["characters"] = ""
    return(vehicle)
    

## PRINT BRIEF DESCRIPTION OF GIVEN VEHICLE ##
def summary_car(car):
    car=update_car_engine(car)
    weight=calculate_weight(car)
    value = calculate_vehicle_value(car)
    #hpt = round(car["chassis"]["engine"]["base_horsepower"]/(weight/1000),2)
    max_speed=calculate_max_speed(car)
    mpg=effective_mpg(car)
    miles=round(mpg*car["chassis"]["fuel_tank"]["capacity"],2)
    emiles=round(mpg*car["chassis"]["fuel_tank"]["fuel"],2)
    
    print("\n{}{}{}: {} occupants, {} kg, {}kmh, {}mpg, {}({})miles, value: ${}".format(
        color.BOLD,car["name"],color.END,len(car["chassis"]["cabin"]["seats"]),round(weight,2),
        max_speed,mpg,emiles,miles,str(value)))
    character_list = []
    for seat in car["chassis"]["cabin"]["seats"]:
        try:
            character_list.append(seat["characters"]["name"]+", "+seat["characters"]["job"])
        except:
            pass
    string = ""
    for character in character_list:
        string += character+" | "
    print(string)
    
    
## PRINT VERBOSE DESCRIPTION OF GIVEN VEHICLE ##
def display_vehicle(vehicle):
    chas = vehicle["chassis"]
    cab = vehicle["chassis"]["cabin"]
    eng = vehicle["chassis"]["engine"]
    tank = vehicle["chassis"]["fuel_tank"]
    mpg = eng["base_mpg"]
    miles = mpg*tank["capacity"]
    weight = calculate_weight(vehicle)
    hpt = eng["base_horsepower"]/(weight/1000)
    empg = effective_mpg(vehicle)
    max_range = empg*tank["fuel"]
    emiles = round(empg*tank["capacity"],2)
    max_speed = calculate_max_speed(vehicle)
    
    print("\n")
    print("{}, the {} {}".format(vehicle["name"],vehicle["brand"],vehicle["model"]))
    print("{} kg, {} hp, {} mpg".format(weight,eng["base_horsepower"],empg))
    print("{} hp/t, {} kmh top speed".format(int(hpt),max_speed))
    print("{} {} produces {} hp, using {} mpg  ({}/{} dur)".format(
        eng["brand"],eng["model"],eng["base_horsepower"],eng["base_mpg"],
        eng["durability"],eng["max_durability"]))
    print("{} {} carries {} passengers and {} kg of cargo  ({}/{} dur)".format(
        cab["brand"],cab["model"],cab["passengers"],cab["max_cargo"],
        cab["durability"],cab["max_durability"]))
    print("{} {} carries {} gallons of fuel  ({}/{} dur)".format(
        tank["brand"],tank["model"],tank["capacity"],tank["durability"],tank["max_durability"]))
    print("{} km maximum possible on a full tank at {} mpg".format(emiles,empg))
    print("{} km currently possible with {} gallons".format(
        str(round(max_range,2)),str(round(tank["fuel"],2))))
    print("\n")
    count=1
    for seat in cab["seats"]:
        pweight = 0
        try:
            pweight=seat["characters"]["weight"]
            name=seat["characters"]["name"]
            job=seat["characters"]["job"]
            string=("{}, {}".format(name,job))
        except:
            pweight=0
            name=""
            job=""
            string="(Empty)"
        #print("Seat {}: {}".format(count, seat))
        print("Seat {}: {}\n  Weight: {} + {} kg".format(
            count,string,seat["weight"],pweight))
        count+=1
    cargo_weight = 0
    for item in cab["cargo"]:
        cargo_weight += item["weight"]
    print(short_border)
    print("Cargo: {} / {} kg".format(cargo_weight,cab["max_cargo"]))
    for item in cab["cargo"]:
        print("  "+item["name"])
    print(short_border)


## CALCULATE ACTUAL MPG OF GIVEN VEHICLE ##
def effective_mpg(car):
    weight = calculate_weight(car)
    weight_factor = weight/1000
    base_mpg=car["chassis"]["engine"]["base_mpg"]
    torque_factor,drag_factor=calculate_car_factors(car)
    mpg = round((base_mpg*torque_factor*drag_factor)-(weight_factor/torque_factor),2)
    return(mpg)
    
    
## RETURNS MAX SPEED FOR GIVEN VEHICLE ##
def calculate_max_speed(car):
    weight=calculate_weight(car)
    torque_factor,drag_factor=calculate_car_factors(car)
    horsepower = calculate_horsepower(car)
    max_speed=round(horsepower/(weight/1000)*drag_factor*torque_factor,2)
    return(max_speed)


## UPDATE ENGINE STATS BASED ON... ENGINE STATS ##
## NEED BETTER DESCRIPTION! ##
def update_engine(engine):
    engine["base_horsepower"] = calculate_base_horsepower(engine)
    engine["base_torque"] = calculate_base_torque(engine)
    return(engine)


## UPDATE ENGINE IN A GIVEN VEHICLE WITH CALCULATED STATS ##
def update_car_engine(car):
    eng = car["chassis"]["engine"]
    eng["base_horsepower"] = calculate_base_horsepower(eng)
    eng["base_torque"] = calculate_base_torque(eng)
    return(car)


## GIVEN ENGINE BORE, STROKE, RPM, & CYLINDERS, DETERMINE MAX HORSEPOWER OUTPUT ##
def calculate_base_horsepower(eng):
    #factor = 18000 is the 'realistic' setting
    factor = 12000
    horsepower = round(((eng["bore"]*eng["bore"])*eng["stroke"]*eng["max_rpm"]/factor)*eng["cylinders"],2)
    return(horsepower)


## GIVEN ENGINE, RETURN MAX TORQUE OUTPUT ##
def calculate_base_torque(eng):
    #factor = 63025 is the 'realistic' setting
    factor = 42000
    horsepower = calculate_base_horsepower(eng)
    torque = round(((horsepower / eng["max_rpm"])*factor)/12,2)
    return(torque)


## GIVEN ENGINE, CALCULATE WEIGHT BASED ON BORE, STROKE, CYLINDERS ##
def calculate_engine_weight(eng):
    weight = round((eng["bore"]*eng["bore"])*eng["stroke"]*eng["cylinders"],2)
    return(weight)
    

## SELF-DESCRIPTIVE ##
## PRINTS STATS FOR EVERY ENGINE IN DATABASE ##
def print_engine_stats():
    for engine in parts["engine"]:
        hp = calculate_base_horsepower(engine)
        kg = calculate_engine_weight(engine)
        torque = calculate_base_torque(engine)
        hpt = round(hp / (kg/1000),2)
        tpt = round(torque / (kg/1000),2)
        displacement = calculate_engine_displacement(engine)
        liters = round(displacement/1000,1)
        print("{}\t{}, {} l produces:\n{} horsepower,\t{} lb/ft torque,\tweighs {}kg\t{} hp/t\n".format(
            engine["brand"],engine["model"],str(liters),str(hp),str(torque),str(kg),str(hpt)))


## GIVEN A CHASSIS, RETURN HANDLING AND STABILITY VALUES ##
def calculate_handling(chassis):
    wheel_factor = chassis["wheels"]/4
    weight_factor = chassis["weight"]/1000
    aspect_ratio = (chassis["track"] / chassis["wheelbase"])
    ## As handling increases, stability decreases
    ## Stability: longitudinal resistance, better acceleration, slower cornering speeds
    ## Handling: lateral resistance, better cornering speed, less acceleration
    handling = round(aspect_ratio*3,2)
    stability = round(1/aspect_ratio*10,2)
    return(handling,stability)
        
        
## PRINT HANDLING STATS FOR ALL CHASSIS IN DATABASE ##
def print_handling_stats():
    for chassis in parts["chassis"]:
        handling,stability = calculate_handling(chassis)
        print("{} {}:\twheelbase {}m,\ttrack {}m,\twheels: {}".format(
            chassis["brand"],chassis["model"],chassis["wheelbase"],chassis["track"],chassis["wheels"]))
        print("\t{} handling,\t{} stability\n".format(str(handling),str(stability)))
        

## CALCULATE AND RETURN TOTAL HORSEPOWER OF VEHICLES ENGINE ##
def calculate_horsepower(car):
    eng = car["chassis"]["engine"]
    horsepower = car["chassis"]["engine"]["base_horsepower"] * eng["compression"]
    try:
        horsepower = horsepower * eng["turbo"]["horsepower_factor"]
    except:
        pass
    return(horsepower)


## CALCULATE SOME FACTORS TO BE USED IN DETERMING STATS ##
def calculate_car_factors(car):
    weight = calculate_weight(car)
    torque_factor = weight/car["chassis"]["engine"]["base_torque"]
    if torque_factor > 1:
        torque_factor = 1
    if torque_factor < 0.01:
        torque_factor = 0.01
    drag=car["chassis"]["cabin"]["drag"]
    drag_factor=1-(drag/2.5)
    return(torque_factor,drag_factor)
        
        
## ATTEMPTING TO CALCULATE A NUMBER TO COMPARE CAR PERFORMANCE WITH OTHER CARS ##
def calculate_car_rating(car):
    car["chassis"]["handling"],car["chassis"]["stability"] = calculate_handling(car["chassis"])
    weight = calculate_weight(car)
    acceleration = round((
        (car["chassis"]["engine"]["base_horsepower"]/weight)*car["chassis"]["stability"]),2)
    max_speed = round(calculate_max_speed(car)/10,2)
    handling = round((car["chassis"]["handling"]*5),2)
    print("{} {} Rated At:\n".format(car["brand"],car["model"]))
    print("Acceleration: {}\tMax Speed: {}\tHandling: {}\n".format(acceleration,max_speed,handling))


## GIVEN VEHICLE AND NEW PART, ATTEMPT TO INSTALL PART ##
## INCLUDES SANITY CHECKS TO ENSURE COMPATIBILITY ##
def replace_part(vehicle,new_part):
    if not part_compatible_with(vehicle,new_part):
        print("\n{} {} is not compatible with your vehicle!\nCannot install!\n".format(
            new_part["brand"],new_part["model"]))
        return(vehicle,new_part)
    partslist = ["Engine","Fuel Tank"]
    fuel = vehicle["chassis"]["fuel_tank"]["fuel"]
    if new_part["type"] == "Chassis":
        cont=input("Keep cabin, engine, and fuel tank? (y/n) ")
        if cont == "y":
            cab=vehicle["chassis"]["cabin"].copy()
            eng=vehicle["chassis"]["engine"].copy()
            tank=vehicle["chassis"]["fuel_tank"].copy()
            vehicle["chassis"]["cabin"]=""
            vehicle["chassis"]["engine"]=""
            vehicle["chassis"]["fuel_tank"]=""
            old_part=vehicle["chassis"].copy()
            vehicle["chassis"] = new_part.copy()
            vehicle["chassis"]["cabin"]=cab.copy()
            vehicle["chassis"]["engine"]=eng.copy()
            vehicle["chassis"]["fuel_tank"]=tank.copy()
        else:
            old_part=vehicle["chassis"].copy()
            vehicle["chassis"] = new_part.copy()
    elif new_part["type"] == "Cabin":
        cont=input("Keep seats? (y/n) ")
        if cont == "y":
            print("Sorry, can't yet!")
        old_part = vehicle["chassis"][new_part["type"]].copy()
        vehicle["chassis"][new_part["type"]]=new_part
        install_seats(vehicle)
    elif new_part["type"] == "Turbo":
        if vehicle["chassis"]["engine"]["turbo"] == "":
            old_part = ""
        else:
            old_part = vehicle["chassis"]["engine"]["turbo"].copy()
        vehicle["chassis"]["engine"]["turbo"] = new_part
    elif new_part["type"] in partslist: 
        part_type = new_part["type"].lower()
        if part_type == "fuel tank":
            part_type = "fuel_tank"
        old_part = vehicle["chassis"][part_type].copy()
        vehicle["chassis"][part_type]=new_part
    else:
        print("Something went wrong! {} not found in partslist!".format(new_part["type"]))
    if fuel > vehicle["chassis"]["fuel_tank"]["capacity"]:
        fuel = vehicle["chassis"]["fuel_tank"]["capacity"]
    vehicle["chassis"]["fuel_tank"]["fuel"] = fuel
    display_vehicle(vehicle)
    return(vehicle,old_part)


## GIVEN VEHICLE AND PART, DETERMINE IS PART CAN BE INSTALLED ##
def part_compatible_with(vehicle,part):
    partslist = ["Engine","Cabin","Fuel Tank","Turbo"]
    if part["type"] == "Chassis":
        return(True)
    elif part["type"] in partslist:
        if int(part["size"]) <= int(vehicle["chassis"]["size"]):
            return(True)
    return(False)
                
    
## PRINT CHARACTER INFO ##
def display_character(character):
    gender = ""
    if character["gender"] == "m":
        gender="Male"
    elif character["gender"] == "f":
        gender="Female"
    else:
        gender="Non-Binary"
    
    print("\n{}, {} year old {} {}".format(
        character["name"],character["age"],gender,character["job"]))
    print("Weight: {}kg,\tHeight: {}cm".format(character["weight"],character["height"]))
    
    for skill in character["skills"]:
        print("{}:\tLevel {},\t{}xp".format(skill["skill"],skill["level"],skill["xp"]))
    print("\n")
        
    
## RETURNS A NEW SLAMTEK VEHICLE ##
def build_vehicle():
    newcar = new_vehicle()
    newcar=random_car_parts(newcar)
    
    newcar=parts_by_parameter(newcar,"brand","SlamTek")
    newcar = make_car_old(newcar)
    newcar["name"] = random.choice(names)+"car"
    newcar["brand"] = "SlamTek"
    newcar["model"] = "Scrapper"
    
    install_seats(newcar)
    fill_vehicle(newcar)
    return(newcar)


## CREATES A NEW VEHICLE BASED ON PARAMETER AND VALUE ##
## EX: parameter "brand", value "Steelworks" RETURNS A VEHICLE WITH ALL STEELWORKS-BRAND PARTS ##
def parts_by_parameter(car,parameter,value):
    if verify_parameters(parameter,value):
        pass
    else:
        print("Parameter verification failed!!!")
        return(car)
    
    while car["chassis"][parameter]!=value:
        car = new_vehicle()
        car = random_car_parts(car)
        
    while car["chassis"]["engine"][parameter]!=value:
        car["chassis"]["engine"]=random.choice(parts["engine"]).copy()    
        
    while car["chassis"]["cabin"][parameter]!=value:
        car["chassis"]["cabin"]=random.choice(parts["cabin"]).copy()    
        
    while car["chassis"]["fuel_tank"][parameter]!=value:
        car["chassis"]["fuel_tank"]=random.choice(parts["fuel_tank"]).copy()
        
    install_seats(car)
    fill_vehicle(car)
    
    car["name"] = random.choice(names)+"car"
    car["brand"] = "Homebuilt"
    car["model"] = value
        
    return(car)
        
        
## MAKE SURE PARAMETER AND VALUE MAKE SENSE TO THE PROGRAM ##
def verify_parameters(parameter,value):
    verified_list = []
    for chas in parts["chassis"]:
        if value in chas[parameter]:
            verified_list.append(True)
            break
    for eng in parts["engine"]:
        if value in eng[parameter]:
            verified_list.append(True)
            break
    for cab in parts["cabin"]:
        if value in cab[parameter]:
            verified_list.append(True)
            break
    for tank in parts["fuel_tank"]:
        if value in tank[parameter]:
            verified_list.append(True)
            break
    if len(verified_list) >= 4:
        return(True)
    else:
        return(False)
        

## RETURN A NEW CAR WITH COMPLETELY RANDOM (POTENTIALLY INCOMPATIBLE) PARTS ##
def random_car_parts(car):
    car["chassis"]=random.choice(parts["chassis"]).copy()
    car["chassis"]["engine"]=random.choice(parts["engine"]).copy()
    car["chassis"]["cabin"]=random.choice(parts["cabin"]).copy()
    car["chassis"]["fuel_tank"]=random.choice(parts["fuel_tank"]).copy()
    return(car)
    
        
## ORIGINALLY INTENDED TO ALLOW CREATION OF SPECIFIC VEHICLE ##
## WILL REPLACE WITH MORE VERSATILE FUNCTION ##
def build_bus():
    pass
    
    
## CREATE A LIST OF CARS THAT THE PLAYER CAN PURCHASE ##
def car_lot():
    vehicle_count = random.randrange(2,6)
    vehicle_list = []
    for i in range(0,vehicle_count):
        new_vehicle = build_empty_vehicle()
        vehicle_list.append(new_vehicle)
    count=1
    
    print(long_border)
    print("\n{}Welcome to {}'s Used Car Lot!{}\n".format(color.BOLD,random.choice(names),color.END))
    print("Let's see what we have in stock today...\n")
    print(short_border)
    for vehicle in vehicle_list:
        print(str(count)+": "+color.UNDERLINE+vehicle["brand"]+" "+vehicle["model"]+color.END)
        summary_car(vehicle)
        count += 1
        print(short_border)
    print("\n  So!  Are you interested in purchasing any of these fine vehicles today?\n")
    print(long_border)
    

## GIVEN VEHICLE, GIVEN NUMBER OF SEATS, CREATE AND PLACE CHARACTERS ##
def fill_vehicle(vehicle):
    seats = len(vehicle["chassis"]["cabin"]["seats"])
    rosterlen = len(roster)
    diff = seats-rosterlen
    #print("{} seats open!".format(seats))
    driver=new_driver()
    roster.append(driver)
    for i in range(1,diff):
        c=random.choice(["M","S"])
        if c=="M":
            n=new_mechanic()
            roster.append(n)
        else:
            n=new_scientist()
            roster.append(n)
    for seat in vehicle["chassis"]["cabin"]["seats"]:
        seat["characters"] = roster[0]
        #print("Appending {} to seat {}".format(roster[0]["name"],seat["model"]))
        roster.remove(roster[0])
    
    
## ROSTER IS TEMPORARY HOLDING ZONE FOR NEW CHARACTERS ##
def show_roster():
    for char in roster:
        print(char)
    

## GIVEN VEHICLE, DETERMINE SEAT SLOTS AND INSTALL SEATS ACCORDINGLY ##
def install_seats(vehicle):
    seatslots = vehicle["chassis"]["cabin"]["passengers"]
    seatrosterlen = len(seatroster)
    diff = seatslots-seatrosterlen
    if diff == 0:
        diff = 1
    for i in range(0,diff):
        new_seat()
    vehicle["chassis"]["cabin"]["seats"].clear()
    for i in range(0,seatslots):
        seat = seatroster[0].copy()
        #print("Appending seat {} to cabin {}".format(
        #    seatroster[0]["model"],vehicle["chassis"]["cabin"]["model"]))
        vehicle["chassis"]["cabin"]["seats"].append(seat)
        seatroster.remove(seatroster[0])

            
## GIVEN CHARACTER, ASSIGN A SKILL BASED ON THEIR JOB ##
def assign_skills(character):
    tree = character["job"]
    skillchoices = []
    for skill in jobs.SKILLS:
        if (skill["tree"] == tree):
            skillchoices.append(skill)
    choice=random.choice(skillchoices)
    if len(character["skills"]) < 1:
        character["skills"].append(choice)
        
    
    

## ALL new_ FUNCTIONS RETURN A DEFAULT DICTIONARY OF SPECIFIED TYPE ##
def new_vehicle():
    return {
        "name": "default",
        "brand": "default",
        "model": "default",
        "chassis": "",
    }

def new_chassis():
    return {
        "type": "chassis",
        "name": "default",
        "brand": "default",
        "model": "default",
        "size": 0,
        "weight": 0,
        "engine": "",
        "cabin": "",
        "fuel_tank": ""
    }

def new_engine():
    return {
        "type": "engine",
        "name": "default",
        "brand": "default",
        "model": "default",
        "weight": 0,
        "base_horsepower": 0,
        "base_mpg": 0,
    }

def new_cabin():
    return {
        "type": "cabin",
        "name": "default",
        "brand": "default",
        "model": "default",
        "weight": 0,
        "passengers": 0,
        "cargo": 0,
        "seats": []
    }

def new_seat():
    seat = {
        "size": 0,
        "weight": 0,
        "comfort": 0,
        "character": ""
    }
    seat = random.choice(parts["seats"])
    seatroster.append(seat)

def new_fuel_tank():
    return {
        "brand": "default",
        "model": "default",
        "weight": 0,
        "size": 0,
        "capacity": 0,
        "fuel": 0
    }

def new_character():
    character = {
        "name": random.choice(names),
        "age": random.randrange(20,50),
        "gender": random.choice(["m","m","m","f","f","f","o"]),
        "weight": random.randrange(50,100),
        "height": random.randrange(140,190),
        "job": random.choice(jobs.JOBS),
        "skills": []
    }
    assign_skills(character)
    return(character)
    #roster.append(character)
    
def new_driver():
    char=new_character()
    while char["job"]!="Driver":
        char=new_character()
    return(char)

def new_mechanic():
    char=new_character()
    while char["job"]!="Mechanic":
        char=new_character()
    return(char)

def new_scientist():
    char=new_character()
    while char["job"]!="Scientist":
        char=new_character()
    return(char)


## NOT SURE WHY I MADE THIS ##
## WILL REMOVE IF IT IS NOT NECESSARY ##
def build_character():
    newchar = new_character()
    return(newchar)




    
    
    
    
    
    
## APPLY CALCULATIONS FOR PARTS THAT NEED IT ##
## SOME PARTS HAVE TWO SETS OF STATS: FIXED AND CALCULATED ##
## FIXED STATS ARE SET: BORE, STROKE, ETC ##
## CALCULATED ARE, YES!  CALCULATED FROM FIXED STATS ##
## IE DETERMINING HORSEPOWER AND TORQUE FROM BORE, STROKE, RPM, CYLINDERS ##

for engine in parts["engine"]:
    engine = update_engine(engine)
    
    
for chassis in parts["chassis"]:
    handling,stability = calculate_handling(chassis)
    chassis["handling"] = handling
    chassis["stability"] = stability


    
    
    
    
    
    
## MAIN FUNCTION, TO BE CALLED BY PLAYER ##
## NEEDS A UI WRAPPER TO LOOK NICE FOR END USER? ##
    
def play():
    p = new_player()
    n = build_big_road_network()
    print(help_string)
    cont = input("\nHit enter to start! ")
    explore_test(n,p)
    
##
##