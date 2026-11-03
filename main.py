# Sidi Cisse 
# add a use input and figure out how to implement additional text add to existing text if necessary

import asyncio               
from pathlib import Path
import pygame

WIDTH, HEIGHT = 900, 600
GAME_TITLE = "GHOST"
INTERFACE = "menu" 
BACKGROUND = (30, 45, 55)
PANEL_COLOR = (39, 49, 65)
TEXT_COLOR = (235, 235, 240)
MUTED_COLOR = (185, 195, 205)
ACCENT_COLOR = (244, 197, 102)
TITLE_SIZE = 38
TEXT_SIZE = 22
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
        
class Interactive: 
    def __init__(self, name, value, description, follow_up=None): 
        self.name = name 
        self.value = value
        self.description = description 
        self.follow_up = follow_up or []

class Character: 
     def __init__(self, name, description): 
          self.name = name 
          self.description = description 

class Weapon: 
    def __init__(self, name, damage, description): 
        self.name = name 
        self.damage = damage 
        self.description = description
    

class Room: 
    def __init__(self, name, description, enter_sound=None, follow_up=None): 
        self.name = name 
        self.description = description 
        self.enter_sound = enter_sound 
        self.neighbors = {} 
        self.follow_up = follow_up or [] 
        self.interactive = None  
        self.monster = None  
        self.treasure = None
        self.character = None
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
        self.active = None
        self.step = 0  
        self.started = False
        self.ran = False 
        self.inventory = []
        self.pending = []
        self.best_weapon_damage = 1
        self.game_over = False 
        self.sounds = { 
            'go past': pygame.mixer.Sound(ASSET_DIR / 'frat-001.ogg'),
        } 

        
        
        ATO = Room('Frat house', story('Monologue.txt'))
        past_ATO = Room('past frat house', story('PastATO.txt'), enter_sound= 'go past', 
                        follow_up= [story('PastATOfollowup.txt')])
        Abbos_alley = Room('abbos alley', story('abbos.txt')) 
        All_saints_Church = Room('all saints', story('allsaints.txt')) 
        Johnson = Room('johnson hall', story('johnson.txt'), 
                       follow_up= [story ('johnsonFollowup.txt')]) 
        Walsh_elliot = Room('walsh elliot', story('Walshelliot.txt'), 
                            follow_up= [story('WalshelliotFollowup.txt')]) 
        Walsh_elliot_office = Room('vice chancellors office', story('office.txt'))
        The_forest = Room('the forest', story('theforest.txt'))
 
        ATO.add_neighbor('past', past_ATO)
        past_ATO.add_neighbor('future ato', ATO)
        past_ATO.add_neighbor('abbos alley', Abbos_alley) 
        Abbos_alley.add_neighbor('all saints', All_saints_Church) 
        Abbos_alley.add_neighbor('johnson hall', Johnson)
        Abbos_alley.add_neighbor('walsh elliot', Walsh_elliot)
        Abbos_alley.add_neighbor('the forest', The_forest) 
        Walsh_elliot.add_neighbor('vice chancellors office', Walsh_elliot_office)
        Walsh_elliot_office.add_neighbor('abbos alley', Abbos_alley)
        Johnson.add_neighbor('all saints', All_saints_Church)
        All_saints_Church.add_neighbor('the forest', The_forest)

        past_ATO.treasure = (Treasure('newspaper', 2, story('newspaper.txt')))
        Abbos_alley.treasure = (Treasure('map', 10, story('map.txt')))
        

        The_forest.monster = (Monster('skinwalker', 5, story('skinwalker.txt')))
        Walsh_elliot.monster = (Monster('ghost', 5, story('ghost.txt')))

        Johnson.weapon = (Weapon('rifle', 5, story('rifle.txt')))
        All_saints_Church.weapon = (Weapon('holywater', 20, story('holywater.txt')))

        The_forest.interactive = (Interactive('trampoline', 90, story('jump1.txt'), 
                                  follow_up= [story('jump2.txt'), story('jump3.txt')]))

        Walsh_elliot_office.character = (Character('vice chancellor', story('vicechancellor.txt',)))
        
         
        self.current_room = ATO 
        self.say('Welcome this is ATO.')
        self.say('''To get started enter start''')


    

    def say(self, message):
            self.messages.append(message)

    def newspaper(self):
         self.say(story('newspaper.txt'))

    def use(self, name): 
         obj = self.current_room.interactive
         if obj is not None and obj.name == name:
              self.say(obj.description)
              if obj.value > 0:
               self.score += obj.value
               obj.value = 0
               self.say(f'Your score is now {self.score} out of 100')
               if obj.follow_up:
                self.pending = list(obj.follow_up)
               self.say('(Press enter to jump...)')
               if self.score >= 100 and not self.pending:
                self.say('YOU WIN THE GAME')
                self.game_over = True
         else:
            self.say(f'There is no {name} here')
            
    
    def map(self): 
        self.say(f'Your current location is: {self.current_room.name}')
        self.say(story('map.txt'))

    
    def announce_room(self):
        self.say(f'You are in: {self.current_room.name}') 
        self.say(self.current_room.description)
        if self.current_room.follow_up:
             self.pending = list(self.current_room.follow_up)
             self.say('(Press enter to continue...)')
    
    def play_sound(self, name): 
        if name in self.sounds: 
            self.sounds[name].play()

    def start(self):
        self.started = True 
        self.say(self.current_room.description)
        
    def go(self, destination):
        destination = self.current_room.get_neighbor(destination)
        if destination == None: 
            self.say('Error! Enter your destination. ') 
            return 

        self.current_room = destination
        self.ran = False
        if self.current_room.enter_sound is not None:
                    self.play_sound(self.current_room.enter_sound)
        self.announce_room()
        
    
    def help(self):
        self.say('''Make sure to talk to the vice chancellor once you get to his office
        in walsh elliot. running away from the ghost in walsh elliot will make the attack 
        option inaffective. Without the rifle and the holy water you cannot defeat the
        final monster, so make sure to get both before going to the forest. And always
        look around in the room your in for information on whats in there.''') 

    def attack(self, name): 
        monster = self.current_room.monster 
        if monster is not None and monster.name == name: 
            if self.best_weapon_damage > monster.armor: 
                self.say('You successfully exorsized it!')
                self.say(monster.description)
                self.current_room.monster = None
            elif self.ran == True: 
                self.current_room.monster = None
            else: 
                 self.say('Your attack did nothing.')
                 self.say(f'The {monster.name} violently ate you in one gulp')
                 self.say('YOU LOST')
                 self.game_over = True 
        else: 
            self.say('Youre safe nothing is here')

    def run(self): 
         monster = self.current_room.monster 
         if monster is not None: 
              self.say(monster.description)
              self.ran = True 
              

   
    def talk(self, name): 
         character = self.current_room.character
         if character is not None and character.name == name: 
            self.say(self.current_room.character.description)
         else: 
              self.say('There is no human here but you')
         

    def grab(self,name):
         treasure = self.current_room.treasure
         weapon = self.current_room.weapon 
         if treasure is not None and treasure.name == name: 
              self.current_room.treasure = None 
              self.score += treasure.value 
              self.say(f'Your score is now {self.score} out of 100')
              self.inventory.append(treasure.name)
              if self.score >= 100: 
                   self.say('YOU WIN THE GAME')
                   self.game_over = True 
         elif weapon is not None and weapon.name == name:
              self.current_room.weapon = None 
              self.say(weapon.description)
              if weapon.damage > self.best_weapon_damage: 
                    self.best_weapon_damage = weapon.damage 
                    self.say('You can defeat stronger foes with this')
         else: 
              self.say(f'There is no {name} here')
              
               
        
    def look(self): 
        self.say(f'You are in {self.current_room.name}')
        if self.current_room.monster is not None: 
            self.say(f'There is {self.current_room.monster.name} here')
        if self.current_room.interactive is not None: 
            self.say(f'There is a {self.current_room.interactive.name} here')
        if self.current_room.treasure is not None: 
            self.say(f'There is a {self.current_room.treasure.name} here') 
        if self.current_room.character is not None: 
            self.say(f'There is someone named {self.current_room.character.name} here')
        if self.current_room.weapon is not None: 
            self.say(f'There is {self.current_room.weapon.name} here')
        self.say(f'Exits: {self.current_room.list_exits()}')
    
    def handle_command(self, line):
        if self.pending: 
             self.say(self.pending.pop(0))
             if self.score >= 100 and not self.pending:
                self.say('YOU WIN THE GAME')
                self.game_over = True
             return  
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
        elif command == 'use' and len(words) > 1:
             self.use(' '.join(words[1:]))
        elif command == 'look': 
            self.look()
        elif command == 'map':
            self.map() 
        elif command == 'newspaper':
             self.newspaper()
        elif command == 'talk' and len(words) > 1: 
             self.talk(' '.join(words[1:]))
        elif command == 'grab' and len(words) > 1: 
             self.grab(''.join(words[1:]))
        elif command == 'attack' and len(words) > 1:
             self.attack(''.join(words[1:])) 
        elif command == 'run': 
             self.run()
        else:
            self.say('I dont understand that. Enter help for more information. ') 
            return 
        
def draw_game(screen, title_font, text_font, game, selected):
    screen.fill(BACKGROUND)
    screen.blit(title_font.render(GAME_TITLE, True, ACCENT_COLOR), (20, 30))

    choices = menu_commands(game) if INTERFACE == "menu" else []
    line_height = text_font.get_linesize() + 3
    input_height = max(75, (len(choices) + 1) * line_height + 20) if choices else 75
    panel_top = HEIGHT - input_height
    lines = []
    for message in game.messages:
        lines.extend(wrap_text(message, text_font, WIDTH - 60))
    available_lines = max(1, (panel_top - 75) // line_height)
    for index, line in enumerate(lines[-available_lines:]):
        screen.blit(text_font.render(line, True, TEXT_COLOR), (30, 70 + index * line_height))

    pygame.draw.rect(screen, PANEL_COLOR, (0, panel_top, WIDTH, input_height))
    if game.game_over:
        screen.blit(text_font.render("Game over. Press Esc to quit.", True, TEXT_COLOR), (30, panel_top + 20))
    elif INTERFACE == "menu":
        screen.blit(text_font.render("Up/Down: choose   Enter: select", True, MUTED_COLOR), (30, panel_top + 8))
        for index, (label, _) in enumerate(choices):
            prefix = "> " if index == selected else "  "
            color = ACCENT_COLOR if index == selected else TEXT_COLOR
            screen.blit(text_font.render(prefix + label, True, color), (30, panel_top + 8 + (index + 1) * line_height))
    else:
        screen.blit(text_font.render("> " + game.current_input, True, TEXT_COLOR), (30, panel_top + 20))

def menu_commands(game):
    if game.game_over:
        return []
    if game.pending:
        return [('Continue', '')]
    if game.started is not True: 
        return[('Start', 'start')]

    room = game.current_room
    choices = [('Look around', 'look')]
    if room.monster:
      choices.append((f'Attack {room.monster.name}', f'attack {room.monster.name}'))
    if not game.ran:
      choices.append(('run', 'run'))
        
    if not room.monster or game.ran:
        for name in room.neighbors:
         choices.append((f'Go {name}', f'go {name}'))
        if room.weapon:
          choices.append((f'Grab {room.weapon.name}', f'grab {room.weapon.name}')) 
        if room.treasure:
         choices.append((f'Grab {room.treasure.name}', f'grab {room.treasure.name}'))
        if room.interactive: 
            choices.append((f'Use {room.interactive.name}', f'use {room.interactive.name}'))
        if room.character:
         choices.append((f'Talk to {room.character.name}', f'talk {room.character.name}'))
        if 'newspaper' in game.inventory:
         choices.append(('Read newspaper', 'newspaper'))
        if 'map' in game.inventory: 
         choices.append(('use map', 'map'))
    choices.append(('Help', 'help'))
    return choices


def draw_title(screen, title_font, text_font):
    screen.fill(BACKGROUND)
    title = title_font.render(GAME_TITLE, True, ACCENT_COLOR)
    prompt = text_font.render("Press Enter to begin", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))

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
    selected = 0

    while running: 
        choices = menu_commands(game) if INTERFACE == "menu" else []
        selected = min(selected, max(len(choices) - 1, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif INTERFACE == "menu":
                    if event.key == pygame.K_UP and choices:
                        selected = (selected - 1) % len(choices)
                    elif event.key == pygame.K_DOWN and choices:
                        selected = (selected + 1) % len(choices)
                    elif event.key == pygame.K_RETURN and choices and not game.game_over:
                        game.handle_command(choices[selected][1])
                        selected = 0
                else:
                    if event.key == pygame.K_RETURN:
                        if not game.game_over:
                            command = game.current_input.strip()
                            game.current_input = ""
                            game.handle_command(command)
                    elif event.key == pygame.K_BACKSPACE:
                        game.current_input = game.current_input[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        game.current_input += event.unicode 
        draw_game(screen, font, small_font, game, selected)
        pygame.display.flip()       
        await asyncio.sleep(0) 
       
    pygame.quit()
    
    
asyncio.run(main())



            

   








