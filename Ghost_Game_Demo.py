# Sidi Cisse 
# short demo of my groups game so far
# Some code that was included on the example games program is not here because I cant add 
# Everything yet as this is just a demo but I used the example code mostly because it gave
# me something to start with I still do not know all these things like TEXT_DIR to heart yet
# so I am pretty dependent on seeing what everythign does on the main.py folder and using it 
# in my program if it makes sense 

# import asyncio               took out some things because I could not figure out 
# how to make it show the screen for pygame but it is all in the example code I just 
# wouldnt have much time to debug it and actually finish it if I did all of that right now
# so asyncio is here for now just unused 
from pathlib import Path
import pygame

# WIDTH, HEIGHT = 900, 600
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets" 
TEXT_DIR = BASE_DIR / "text"

def story(filename):
    return (TEXT_DIR / filename).read_text(encoding="utf-8").strip()


class Monster: 
    def __init__(self, name, armor, description): 
        self.name = name 
        self.armor = armor 
        self.description = description  


class Treasure: 
    def __init__(self, name, value, description): 
        self.name = name 
        self.description = description 
        self.value = value  


class Weapon: 
    def __init__(self, name, damage, description): 
        self.name = name 
        self.damage = damage 
        self.description = description 


class Room: 
    def __init__(self, name, description, enter_sound=None): 
        self.name = name 
        self.description = description 
        self.enter_sound = enter_sound 
        self.neighbors = {} 
        self.monster = None  
        self.treasure = None 
        self.weapon = None  

    def add_neighbor(self, direction, room): 
        self.neighbors[direction] = room  
        
    def get_neighbor(self, direction): 
        return self.neighbors.get(direction) 
        
    def list_exits(self): 
        return ', '.join(self.neighbors.keys()) 


class Game: 
    def __init__(self): 
        self.messages = []
        self.current_input = '' 
        self.score = 0 
        self.best_weapon_damage = 1
        self.game_over = False 
        self.sounds = { 
            'go future': pygame.mixer.Sound(ASSET_DIR / 'frat-001.wav'),
        } 

        
        
        ATO = Room('Frat house', story('Monologue.txt'))
        future_ATO = Room('future frat house', story('futureATO.txt'))

        ATO.add_neighbor('future', future_ATO)
         
        self.current_room = ATO  

    def say(self, message):
        self.messages 
        print(message)
    
    def announce_room(self):
        self.say(f'You are in: {self.current_room.name}') 
        self.say(self.current_room.description)
    
    def play_sound(self, name): 
        if name in self.sounds: 
            self.sounds[name].play()

    def start(self):
        self.started = False
        self.say(self.current_room.description)
        
    def go(self, direction):
        destination = self.current_room.get_neighbor(direction)
        if destination == None: 
            self.say('Error! Enter your destination. ') 
             
        self.current_room = destination
        self.play_sound('go future')
        self.announce_room()
    
    def help(self):
        self.say('Try go future')
    
    def handle_command(self, line):
        self.say(f'> {line}')
        words = line.lower().split() 
        if not words: 
           return 
        command = words[0]

        if command == 'start': 
            self.start()
        elif command == 'go' and len(words) > 1:
            self.go(words[1])
        elif command == 'help':
            self.help()
        else: 
            self.say('I dont understand that. Try commands like: go future ') 
             


        

pygame.init() 
pygame.mixer.init()
game = Game() 
game.say("Welcome, try using the commands: start to start the game and '\n' " \
"go future. After reading the text")
while not game.game_over:
            line = input("> ")
            if line.lower() == "quit":
                break 
            game.handle_command(line)
            

   








