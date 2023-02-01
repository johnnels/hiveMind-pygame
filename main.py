import pygame
from sys import exit
import random
import math

# Screen/systems setup
tile_size = 64
screen_width = 18*tile_size
screen_height = 14*tile_size
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption('hive')
clock = pygame.time.Clock()

spriteMenu = [
"Graphics\pausebox-001.png",
"Graphics\pausestats.png",
"Graphics\excite.png"
]

for count in range(len(spriteMenu)):
    print(str(count) + ': ' + str(spriteMenu[count]))
    spriteMenu[count] = pygame.image.load(spriteMenu[count]).convert_alpha()

spriteMenu[2] = pygame.transform.scale(spriteMenu[count], (32, 32))
spriteMenu[2].fill("RED", special_flags=pygame.BLEND_MULT)

tileMenu = [
"Graphics\iles\wallbrick-001.png",
"Graphics\iles\door-001.png"
]
for count in range(len(tileMenu)):
    tileMenu[count] = pygame.image.load(tileMenu[count])
    tileMenu[count] = pygame.transform.scale(tileMenu[count], (64, 64))



select_frames_import= [
    "Graphics\select\selectedc1.png",
    "Graphics\select\selectedc2.png",
    "Graphics\select\selectedc3.png",
    "Graphics\select\selectedc4.png",
    "Graphics\select\selectedc5.png",
    "Graphics\select\selectedc6.png",
    "Graphics\select\selectedc7.png",
    "Graphics\select\selectedc8.png",
    "Graphics\select\selectedc9.png",
    "Graphics\select\selectedc10.png",
    "Graphics\select\selectedc11.png",
    "Graphics\select\selectedc12.png",
    "Graphics\select\selectedc13.png",
    "Graphics\select\selectedc14.png",
    "Graphics\select\selectedc15.png",
    "Graphics\select\selectedc16.png",
    "Graphics\select\selectedc17.png",
    "Graphics\select\selectedc18.png",
    "Graphics\select\selectedc19.png"

]
select_frames = []
for count in range(len(select_frames_import)):
    select_frames.append(pygame.image.load(select_frames_import[count]).convert_alpha())
    select_frames[count] = pygame.transform.scale(select_frames[count], (72, 72))
    select_frames[count].fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

minionTypes = [# name, image,special, speed, hp, atk, range
    ['squee',"Graphics\Companion\squee-001.png", 'atkMeld', 1, 3, 1, 148, 64],
    ['bee',"Graphics\Companion\dee-001.png", 'atkSting', 2, 1, 1, 0, 32],
    ['dog', "Graphics\Companion\dog-001.png", 'atkBark', 1, 2, 1, 200, 64]
]
# Sprite storage
bg_img = pygame.Surface((screen_width, screen_height))
bg_img.fill('Black')

# fonts
pix_font = pygame.font.Font('graphics/Pixeltype.ttf', 32)
pause_font = pygame.font.Font('graphics/Pixeltype.ttf', 94)
selector_frame = 0
global selected
selected = 1

def keyCheck():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        playerStorage[selected-1].xvel = -playerStorage[selected-1].speed
    if keys[pygame.K_d]:
        playerStorage[selected-1].xvel = playerStorage[selected-1].speed
    if keys[pygame.K_w]:
        playerStorage[selected-1].yvel = -playerStorage[selected-1].speed
    if keys[pygame.K_s]:
        playerStorage[selected-1].yvel = playerStorage[selected-1].speed

# tools
def get_distance(point_one, point_two):
    perpendicular = point_one[1] - point_two[1]
    base = point_one[0] - point_two[0]
    distance = math.hypot(perpendicular, base)
    return int(distance)



def move_rads(point_one, point_two):
    dx = point_two.rect.center[0] - point_one.rect.center[0]
    dy = point_two.rect.center[1] - point_one.rect.center[1]
    rads = math.atan2(dx, dy)
    return rads


def ran(number):
    return(int(random.random()*number)+1)


def ranStats(dice):
    diceStorage = []
    x= 0
    while x <= dice:
        x += 1
        diceStorage.append(math.ceil(random.random()*6))

    return(sum(diceStorage))

def drawSelector():
    global selector_frame
    global selected
    selector_frame += 0.2
    if selector_frame > len(select_frames):
        selector_frame = 0
    try:
        screen.blit(select_frames[int(selector_frame)],(playerStorage[selected-1].rect.center[0]-38, playerStorage[selected-1].rect.center[1]-38))
    except IndexError:
        selected = 0

def pauseScreen():
    screen.blit(spriteMenu[0], (screen_width / 2 - (spriteMenu[1].get_width() / 2), screen_height / 2 - (spriteMenu[1].get_height() / 2)))
    pause_text = pause_font.render("PAUSE", False, 'white')
    screen.blit(pause_text, ((screen_width / 2 - (pause_text.get_width() / 2), 8 + screen_height / 2 - (pause_text.get_height() / 2))))

    screen.blit(spriteMenu[1], (72, 72))
    # name, image,special, speed, hp, atk, range
    statText = [
        'type: ' + str(minionTypes[playerStorage[selected - 1].type][0]),
        'max hp: ' + str(playerStorage[selected - 1].maxhp),
        'atk: ' + str(playerStorage[selected - 1].atk),
        'range: ' + str(playerStorage[selected - 1].range),
        'special: ' + str(minionTypes[playerStorage[selected - 1].type][2])
    ]
    for i in range(len(statText)):
        stat_surface = pix_font.render(statText[i], False, 'white')
        screen.blit(stat_surface, (102, 108+(i*24)))

    screen.blit(spriteMenu[2], (64, 64))

class Minion:
    def __init__(self, type, x, y, player):
        self.type = type
        self.size = minionTypes[type][7]
        self.img = pygame.image.load(minionTypes[type][1])
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.x = x
        self.y = y
        self.xvel = 0
        self.yvel = 0
        self.special = globals()[minionTypes[type][2]]
        self.speed = 1 + math.floor((ranStats(minionTypes[type][3])/3))
        self.hp = ranStats(minionTypes[type][4])
        self.atk = ranStats(minionTypes[type][5])
        self.maxhp = self.hp
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.rect.width = self.size * .75
        self.rect.height = self.size * .75
        self.player = player
        self.target = None
        self.invincible = 0
        self.direction = 0
        self.range = minionTypes[type][6]
        self.sucker = False

        if self.player:
            self.img.fill("ORANGE", special_flags=pygame.BLEND_MULT)

    def update(self):
        global selected
        if self.hp <= 0 :
            if self in playerStorage:
                if playerStorage.index(self) == playerStorage[selected-1]: selected = 1
                playerStorage.remove(self)
            else:
                minionStorage.remove(self)


        # make bots move
        if self.target and self.target.hp > 0:
            self.direction = move_rads(self, self.target)
            for i in range(len(minionStorage)):
                if minionStorage[i] != self and get_distance(self.rect.center, minionStorage[i].rect.center) < 64:
                    self.direction -= move_rads(self,minionStorage[i])/10

            ix = math.sin(self.direction)
            iy = math.cos(self.direction)
            self.x += ix*(self.speed*.66)
            self.y += iy*(self.speed*.66)
            screen.blit(spriteMenu[2], (self.rect.x + 16, self.rect.y -24))

        self.xvel = self.xvel * .85
        self.yvel = self.yvel * .85
        if abs(self.xvel) < 0.2:
            self.xvel = 0
        if abs(self.yvel) < 0.2:
            self.yvel = 0

        for i in range(len(currentMap)):
            if self.rect.colliderect(currentMap[i].rect):
                if currentMap[i].tile == tileMenu[1]:
                    print(str(round(currentMap[i].x)))


        self.x += self.xvel
        self.y += self.yvel

        if self.invincible > 0:
            self.invincible -= 1

        if self.special == atkSting:
            self.special(self)

        self.rect.center = (self.x, self.y)

        if self.hp > 0:
            hpx = self.rect.topleft[0]-16
            hpy = self.rect.topleft[1]-24
            pygame.draw.line(screen, "GREEN", (hpx, hpy),(hpx + (self.hp / self.maxhp) * 72, hpy), 6)

        if self.player:
            self.slot_text = pix_font.render(str(self.player), False, 'white')
            screen.blit(self.slot_text, (self.x-8, self.y-8)), pix_font.render(str(self.player), False, 'white')

        screen.blit(self.img, (self.rect.x - (self.size*.125), self.rect.y - (self.size*.125)))

        #hitbox
        pygame.draw.rect(screen, "RED", self.rect, 4)

        #Make player equal to place in the array
        if self in playerStorage:
            self.player = playerStorage.index(self)+1

# attacks
def atkSting(owner):
    if owner.player:
     for count in range(len(minionStorage)):
        if owner.rect.colliderect(minionStorage[count]):
            if minionStorage[count].invincible < 1:
                minionStorage[count].invincible = 30
                minionStorage[count].hp -= owner.atk
                minionStorage[count].target = owner

            if minionStorage[count].rect.top < owner.rect.top:
                minionStorage[count].yvel = -6
            elif minionStorage[count].rect.bottom > owner.rect.bottom:
                minionStorage[count].yvel = 6

            if minionStorage[count].rect.left < owner.rect.left:
                minionStorage[count].xvel = -6
            elif minionStorage[count].rect.right > owner.rect.right:
                minionStorage[count].xvel = 6

    elif not owner.player:
     for count in range(len(playerStorage)):
        if owner.rect.colliderect(playerStorage[count]) and owner.target == playerStorage[count]:
            if playerStorage[count].invincible < 1:
                playerStorage[count].invincible = 30
                playerStorage[count].hp -= owner.atk
            print('sting!')

            if playerStorage[count].rect.top < owner.rect.top:
                playerStorage[count].yvel = -6
            elif playerStorage[count].rect.bottom > owner.rect.bottom:
                playerStorage[count].yvel = 6

            if playerStorage[count].rect.left < owner.rect.left:
                playerStorage[count].xvel = -6
            elif playerStorage[count].rect.right > owner.rect.right:
                playerStorage[count].xvel = 6


# TEST VARIABLES

rope_size = 6
rope_grow = .15

def atkBark(owner):
    for i in range(len(minionStorage)):
        distance = get_distance(owner.rect.center, minionStorage[i].rect.center)
        if distance < owner.range:
            minionStorage[i].target = owner

def atkMeld(owner):
    nearestEnemy = None
    enemyDistance = None
    for i in range(len(minionStorage)):
        distance = get_distance(owner.rect.center, minionStorage[i].rect.center)
        if distance < owner.range:
            if not nearestEnemy or distance < enemyDistance:
                enemyDistance = distance
                nearestEnemy = minionStorage[i]
    if nearestEnemy:
        owner.sucker = nearestEnemy

minionStorage = []
playerStorage = []
playerStorage.append(Minion(0, 320, 320, 1))
playerStorage[0].atk = 1
playerStorage[0].speed = 3
# Create Minions and players \\ SPAWN

# test map
testMap = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '%', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'm', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', 'm', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'm', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]
def mapGenerator(stage):
    newMap = []
    row = 14
    col = 18
    for x in range(row):
        newMap.append([])
        for y in range(col):
            if x == row-1 or y == col-1 or x == 0 or y == 0:
                newMap[x].append('#')
            else:
                newMap[x].append(' ')
        newMap[0][7] = '%'


    return(newMap)

testMap = mapGenerator(0)

currentMap = []
class TileObject:
    def __init__(self, tile, x, y):
        self.tile = tile
        self.rect = self.tile.get_rect(topleft=(x, y))
        self.x = x/tile_size
        self.y = y/tile_size

    def draw(self):
        screen.blit(self.tile, self.rect.topleft)
        #hitbox
        pygame.draw.rect(screen, "RED", self.rect, 4)


def loadMap(mapName):
    tx = 0
    ty = 0
    for row in mapName:
        for col in row:
            if col == '#':
                currentMap.append(TileObject(tileMenu[0], tx*tile_size, ty*tile_size))
            if col == '%':
                currentMap.append(TileObject(tileMenu[1], tx*tile_size, ty*tile_size))
            if col == 'p':
                playerStorage[0].x = tx*tile_size
                playerStorage[0].y = ty*tile_size
            if col == 'm':
                type = random.randrange(1, len(minionTypes), 1)
                minionStorage.append(Minion(type, tx*tile_size, ty*tile_size, None))

            tx += 1
        tx = 0
        ty +=1


loadMap(testMap)
pause = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quiting')
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for count in range(len(playerStorage)):
                    if playerStorage[count].rect.collidepoint(pygame.mouse.get_pos()):
                        selected = count + 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if selected >= len(playerStorage):
                    selected = 1
                else:
                    selected += 1
            if event.key == pygame.K_q:
                if selected == 1:
                    selected = len(playerStorage)
                else:
                    selected -= 1
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pygame.K_SPACE:
                if playerStorage[selected-1].range > 0:
                    playerStorage[selected-1].special(playerStorage[selected-1])



    if not pause:
        # draw bg
        screen.blit(bg_img,(0,0))
        for i in range(len(currentMap)):
            currentMap[i].draw()


        # make rope thing pulse
        if rope_size > 8 or rope_size < 4:
            rope_grow *= -1
        rope_size += rope_grow
        playerStorage[selected-1].target = None
        # Update/draw objects ,
        for x in range(len(playerStorage)):
            try:
                playerStorage[x].update()

                if playerStorage[x].sucker:
                    pygame.draw.line(screen, "WHITE", playerStorage[x].rect.center, playerStorage[x].sucker.rect.center, int(rope_size))

                    if playerStorage[x].sucker.invincible < 1:
                        playerStorage[x].sucker.hp -= playerStorage[x].atk
                        playerStorage[x].sucker.invincible = 30


                    if playerStorage[x].sucker.hp < 1 and playerStorage[x].hp >1:
                        playerStorage[x].hp -= 1
                        playerStorage[x].sucker.hp +=1
                        playerStorage[x].sucker.img = pygame.image.load(minionTypes[playerStorage[x].sucker.type][1])
                        playerStorage[x].sucker.img = pygame.transform.scale(playerStorage[x].sucker.img, (playerStorage[x].sucker.size, playerStorage[x].sucker.size))
                        playerStorage[x].sucker.img.fill("ORANGE", special_flags=pygame.BLEND_MULT)
                        playerStorage.append(playerStorage[x].sucker)
                        minionStorage.pop(minionStorage.index(playerStorage[x].sucker))
                        playerStorage[x].sucker = False
                        break




                    if get_distance(playerStorage[x].rect.center,playerStorage[x].sucker.rect.center) > int(playerStorage[x].range):
                        playerStorage[x].sucker = False
            except IndexError:
                break


        for x in range(len(minionStorage)):
            try:
                minionStorage[x].update()
            except IndexError:
                break
        alpha_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        drawSelector()
        if playerStorage[selected - 1].range:
            pygame.draw.circle(alpha_surface, (255, 255, 255, 90), playerStorage[selected - 1].rect.center,
                               playerStorage[selected - 1].range - 10, 3)

            screen.blit(alpha_surface, (0, 0))

        #Draw selected number
        selected_text = pix_font.render(str(selected), False, 'white')
        screen.blit(selected_text, (screen_width-85, 85))

        keyCheck()

    else:
        pauseScreen()

    pygame.display.update()
    clock.tick(60)