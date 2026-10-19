# Sidi Cisse 


import asyncio               
from pathlib import Path
import pygame

WIDTH, HEIGHT = 900, 600
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "Sound_Ghost" 
TEXT_DIR = BASE_DIR / "text.ghost"

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

    def add_neighbor(self, destination, room): 
        self.neighbors[destination] = room  
        
    def get_neighbor(self, destination): 
        return self.neighbors.get(destination) 
        
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
            'go past': pygame.mixer.Sound(ASSET_DIR / 'frat-001.ogg'),
        } 

        
        
        ATO = Room('Frat house', story('Monologue.txt'))
        past_ATO = Room('past frat house', story('futureATO.txt'), enter_sound= 'go past')
        Abbos_alley = Room('abbos alley', 'You are in Abbos alley') 
        Gailor = Room('gailor', 'You are in Gailor') 
        Dupont_libary = Room('dupont libary', 'You are in Dupont libary ') 
        All_saints_Church = Room('all saints', 'You are in All saints') 
        Johnson = Room('johnson hall', 'You are in Johnson') 
        Walsh_elliot = Room('walsh elliot', 'You are in Walsh elliot') 
        The_forest = Room('the forest', 'You are in the forest')

        ATO.add_neighbor('past', past_ATO)
        past_ATO.add_neighbor('future ato', ATO)
        past_ATO.add_neighbor('abbos alley', Abbos_alley) 
        Abbos_alley.add_neighbor('gailor', Gailor )
        Abbos_alley.add_neighbor('dupont libary', Dupont_libary)
        Abbos_alley.add_neighbor('all saints', All_saints_Church) 
        Abbos_alley.add_neighbor('johnson hall', Johnson)
        Abbos_alley.add_neighbor('walsh elliot', Walsh_elliot)
        Abbos_alley.add_neighbor('the forest', The_forest) 
        Johnson.add_neighbor('gailor', Gailor)
        Johnson.add_neighbor('dupont libary', Dupont_libary)
        Gailor.add_neighbor('johnson hall', Johnson)
        Gailor.add_neighbor('abbos alley', Abbos_alley) 
        All_saints_Church.add_neighbor('abbos alley', Abbos_alley) 
        Dupont_libary.add_neighbor('abbos alley', Abbos_alley) 
        Dupont_libary.add_neighbor('johnson hall', Johnson)
        Walsh_elliot.add_neighbor('abbos alley', Abbos_alley) 
        Walsh_elliot.add_neighbor('the forest', The_forest)
        The_forest.add_neighbor('abbos alley', Abbos_alley) 
        The_forest.add_neighbor('future ato', ATO) 


        past_ATO.treasure = (Treasure('map', 2, story('map.txt')))
        
        
        
         
        self.current_room = ATO 
        self.say('Welcome this is ATO.')
        self.say('To get started enter start and valid commands throughout the game \n' 
        'include: attack, grab, go, look, and talk. For additional help enter help. ')


    

    def say(self, message):
            self.messages.append(message)

    def newspaper(self):
         self.say(story('newspaper.txt'))
    
    def map(self): 
        self.say(f'Your current location is: {self.current_room.name}')
        self.say(story('map.txt'))
    
    def announce_room(self):
        self.say(f'You are in: {self.current_room.name}') 
        self.say(self.current_room.description)
    
    def play_sound(self, name): 
        if name in self.sounds: 
            self.sounds[name].play()

    def start(self):
        self.started = False
        self.say(self.current_room.description)
        
    def go(self, destination):
        destination = self.current_room.get_neighbor(destination)
        if destination == None: 
            self.say('Error! Enter your destination. ') 
            return 
             
        self.current_room = destination
        if self.current_room.enter_sound is not None:
                    self.play_sound(self.current_room.enter_sound)
        self.announce_room()
        
    
    def help(self):
        self.say('''Try commands like look, attack, grab, newspaper, talk, read or go and make sure  
        that you enter who you are going to attack, or grab and where you are going to for go.''') 

    def attack(self, name): 
        monster = self.current_room.monster 
        if monster is not None and monster.name == name: 
            if self.best_weapon_damage > monster.armor: 
                self.say('You successfully exorsized it!')
            else: 
                 self.say('Your attack did nothing.')
                 self.say(f'The {monster.name} violently ate you in one gulp')
                 self.say('YOU LOST')
                 self.game_over = True
        else: 
            self.say('Youre safe nothing is here')

    def grab(self,name):
         treasure = self.current_room.treasure
         weapon = self.current_room.weapon 
         if treasure is not None and treasure.name == name: 
              self.current_room.treasure = None 
              self.score += treasure.value 
              self.say(f'Your score is now {self.score} out of 100')
              if self.score == 100: 
                   self.say('YOU WIN THE GAME')
                   self.game_over = True 
         elif weapon is not None and weapon.name == name:
              self.current_room.weapon = None 
              if weapon.damage > self.best_weapon_damage: 
                    self.best_weapon_damage = weapon.damage 
                    self.say('You can defeat stronger foes with this')
         else: 
              self.say(f'There is no {name} here')
              
               
        
    def look(self): 
        self.say(f'You are in {self.current_room.name}')
        if self.current_room.monster is not None: 
            self.say(f'There is {self.current_room.monster.description} here')
        if self.current_room.treasure is not None: 
            self.say(f'There is a {self.current_room.treasure.name} here') 
        if self.current_room.weapon is not None: 
            self.say(f'There is {self.current_room.weapon.description} here')
        self.say(f'Exits: {self.current_room.list_exits()}')
       
    def talk(self): 
        ()
        
    
    def handle_command(self, line):
        self.say(f'> {line}')
        words = line.lower().split() 
        if not words: 
           return 
        command = words[0]

        if command == 'start': 
            self.start()
        elif command == 'go' and len(words) > 1:
            self.go(' '.join(words[1:]))
        elif command == 'help':
            self.help()
        elif command == 'look': 
            self.look()
        elif command == 'map':
            self.map() 
        elif command == 'newspaper':
             self.newspaper()
        elif command == 'grab' and len(words) > 1: 
             self.grab(words[1])
        else:
            self.say('I dont understand that. Enter help for more information. ') 
            return 
             
def draw_game(screen, font, small_font, game):
    screen.fill((24, 24, 28))
    screen.blit(font.render("Ghost game", True, (235, 235, 240)), (30, 20))

    lines = []
    for message in game.messages:
        lines.extend(wrap_text(message, small_font, WIDTH - 60))
    lines = lines[-20:]

    y = 70
    for line in lines:
        screen.blit(small_font.render(line, True, (220, 220, 225)), (30, y))
        y += 23

    pygame.draw.line(screen, (100, 100, 110), (30, HEIGHT - 70), (WIDTH - 30, HEIGHT - 70), 2)
    screen.blit(small_font.render("> " + game.current_input, True, (255, 255, 255)), (30, HEIGHT - 50))

def wrap_text(text, font, max_width): 
        if not text:
                return [""]
        words = text.split()
        lines, current = [], ""
        for word in words:
                test = word if not current else current + " " + word
                if font.size(test)[0] <= max_width:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
        if current:
                lines.append(current)
        return lines
        
async def main(): 
    pygame.init() 
    pygame.mixer.init() 


    game = Game()
    running = True 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)

    while running: 
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_RETURN:
                            if not game.game_over:
                                command = game.current_input.strip()
                                game.current_input = ""
                                game.handle_command(command)
                        elif event.key == pygame.K_BACKSPACE:
                            game.current_input = game.current_input[:-1]
                        elif event.unicode and event.unicode.isprintable():
                            game.current_input += event.unicode 
        draw_game(screen, font, small_font, game)
        pygame.display.flip()       
        await asyncio.sleep(0) 
       
    pygame.quit()
    
    
asyncio.run(main())



            

   








