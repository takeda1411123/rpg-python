import pygame
import sys
import random
from pygame.locals import *

from battle import init_battle, view_battle, battle_command
from dungeon import create_dungeon, view_dungeon

# define colour
from event import set_event
from move import move_ship
from ship_score import view_ship_score
from text import view_text

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (96, 96, 96)
BLINK = [
    (224, 255, 255),
    (192, 240, 255),
    (128, 224, 255),
    (64, 192, 255),
    (128, 224, 255),
    (192, 240, 255)
]

# back list
imgBack = [
    pygame.image.load("image/back/back0.png"),
    pygame.image.load("image/back/back1.png"),
    pygame.image.load("image/back/back2.png"),
    pygame.image.load("image/back/back3.png"),
]

# character image
imgLuffy = pygame.image.load("image/character/luffy.png")
imgLuffyL = pygame.image.load("image/character/luffyL.png")
imgChopperM = pygame.image.load("image/character/chopperM.png")
imgEnemy = pygame.image.load("image/character/enemy0.png")

# shipment image
imgShipment = [
    pygame.image.load("image/shipment/brook.png"),
    pygame.image.load("image/shipment/chopper.png"),
    pygame.image.load("image/shipment/franky.png"),
    pygame.image.load("image/shipment/jinbei.png"),
    pygame.image.load("image/shipment/nami.png"),
    pygame.image.load("image/shipment/robin.png"),
    pygame.image.load("image/shipment/sanji.png"),
    pygame.image.load("image/shipment/usopp.png"),
    pygame.image.load("image/shipment/zoro.png"),
]



# item image
imgItem = [
    pygame.image.load("image/character/chopper.png"),
    pygame.image.load("image/character/flag.png"),
    pygame.image.load("image/spoiled.png"),
    pygame.image.load("image/apple.png"),
    pygame.image.load("image/meat.png")
]

# effect image
imgEffect = [
    pygame.image.load("image/effect/attack.png"),
    pygame.image.load("image/effect/help_shipment.png")
]

# 変数の宣言
speed = 1
idx = 0
tmr = 0
floor = 0
fl_max = 1
welcome_message_time = 0
back_number = 0
shipment_number = 0

ship_xposition = 0  # ship x position
ship_ypostition = 0  # ship y position
ship_direction = 0  # ship direction
ship_animation = 0  # ship animation
ship_life_max = 0
ship_life = 0
ship_str = 0
food = 0
chopper_cure = 0
help_shipment = 0
treasure = 0

enemy_name = ""
enemy_skill = ""
enemy_life_max = 0
enemy_life = 0
enemy_str = 0
enemy_x = 0
enemy_y = 0
enemy_step = 0
enemy_blink = 0

dmg_eff = 0
btl_cmd = 0

COMMAND = ["[A]ttack", "[C]hopper Cure", "[H]lep Shipmate", "[R]un"]
TRE_NAME = ["Chopper Cure", "Help Shipmate", "Food spoiled.", "Food +20", "Food +100"]
ENEMY_NAME_LIST = [
    "Buggy", "Arlong", "Sir Crocodile", "Eneru", "Rob Lucci",
    "Gecko Moria", "Admiral of the Navye", "Doflamingo", "Big Mom&Kaido", "Marshall D. Teach"
]

# shipment Skill
SHIPMENT_SKILL = [
    "Humming Sancho Yahazu Slash",
    "Rhombus",
    "Ultimate Hammer",
    "5,000 tiles straight fist",
    "Thunder Lance = tempo",
    "four trees shock",
    "thigh meat",
    "heavenly dragon star",
    "Purgatory Demon Slayer",
]

SHIPMENT_NAME = [
    "brook",
    "chopper",
    "franky",
    "jinbei",
    "nami",
    "robin",
    "sanji",
    "usopp",
    "zoro",
]

# define map length
MAZE_WIDTH = 11
MAZE_HEIGHT = 9
DUNGEON_WIDTH = MAZE_WIDTH * 3
DUNGEON_HEIGHT = MAZE_HEIGHT * 3
DUNGEON = []


# 戦闘メッセージの表示処理
message_list = [""] * 10


def init_message():
    for i in range(10):
        message_list[i] = ""


def set_message(msg):
    for i in range(10):
        if message_list[i] == "":
            message_list[i] = msg
            return
    for i in range(9):
        message_list[i] = message_list[i + 1]
    message_list[9] = msg


def main():
    global DUNGEON, message_list
    global speed, idx, tmr, floor, fl_max, welcome_message_time, btl_cmd, back_number, shipment_number
    global ship_xposition, ship_ypostition, ship_direction, ship_animation
    global ship_life_max, ship_life, ship_str, food, chopper_cure, help_shipment, treasure
    global enemy_step, enemy_blink, dmg_eff
    global imgEnemy, enemy_name, enemy_skill, enemy_life_max, enemy_life, enemy_str, enemy_x, enemy_y
    dmg = 0
    lif_p = 0
    str_p = 0

    pygame.init()
    # title
    pygame.display.set_caption("The Road of The Pirates King")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    # define font
    font_skill = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 40)
    font_s = pygame.font.Font(None, 30)

    # se
    se = [
        pygame.mixer.Sound("sound/attack.ogg"),
        pygame.mixer.Sound("sound/blaze.ogg"),
        pygame.mixer.Sound("sound/potion.ogg"),
        pygame.mixer.Sound("sound/gameover.ogg"),
        pygame.mixer.Sound("sound/levup.ogg"),
        pygame.mixer.Sound("sound/win.ogg")
    ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # push s button, change speed
                if event.key == K_s:
                    speed = speed + 1
                    if speed == 4:
                        speed = 1

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        # top
        if idx == 0:
            if tmr == 1:
                pygame.mixer.music.load("sound/title.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            # view luffy
            screen.blit(imgLuffyL, [230, 60])
            # view title
            view_text(screen, "~~The Road of The Pirates King~~", 210, 450, font, RED)
            if fl_max >= 2:
                view_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, GRAY)
            view_text(screen, "Press space key", 320, 560, font, BLINK[tmr % 6])

            # start, if user push space
            if key[K_SPACE] == 1:
                # create dungeon
                DUNGEON = create_dungeon(
                    MAZE_WIDTH, MAZE_HEIGHT, DUNGEON_WIDTH, DUNGEON_HEIGHT
                )
                # set event
                DUNGEON, ship_xposition, ship_ypostition, ship_direction, ship_animation = \
                    set_event(DUNGEON_WIDTH, DUNGEON_HEIGHT, DUNGEON)

                # initiate data
                floor = 1
                welcome_message_time = 15
                ship_life_max = 300
                ship_life = ship_life_max
                ship_str = 100
                food = 300
                chopper_cure = 0
                help_shipment = 0
                # next map
                idx = 1
                pygame.mixer.music.load("sound/field.ogg")
                pygame.mixer.music.play(-1)

        # ship move
        elif idx == 1:
            # below option
            # 3 get item
            # 10 battle start
            # 2 next floor

            (
                DUNGEON,
                ship_xposition, ship_ypostition, ship_direction, ship_animation,
                ship_life, ship_life_max, chopper_cure, help_shipment, food,
                idx, tmr, treasure
            ) = move_ship(
                key,
                DUNGEON,
                ship_xposition, ship_ypostition, ship_direction, ship_animation,
                ship_life, ship_life_max, chopper_cure, help_shipment, food,
                idx, tmr,
                treasure
            )
            view_dungeon(
                screen,
                ship_xposition,
                ship_ypostition,
                DUNGEON,
                DUNGEON_WIDTH,
                DUNGEON_HEIGHT,
                ship_animation
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            view_text(screen, "floor {} ({},{})".format(floor, ship_xposition, ship_ypostition), 60, 40, font_s, WHITE)
            if welcome_message_time > 0:
                welcome_message_time = welcome_message_time - 1
                view_text(screen, "Welcome to floor {}.".format(floor), 300, 180, font, GRAY)

        # change screen
        elif idx == 2:
            view_dungeon(
                screen,
                ship_xposition,
                ship_ypostition,
                DUNGEON,
                DUNGEON_WIDTH,
                DUNGEON_HEIGHT,
                ship_animation
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if 1 <= tmr <= 5:
                h = 80 * tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if tmr == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                welcome_message_time = 15
                # create new floor
                DUNGEON = create_dungeon(
                    MAZE_WIDTH, MAZE_HEIGHT, DUNGEON_WIDTH, DUNGEON_HEIGHT
                )
                # put event
                DUNGEON, ship_xposition, ship_ypostition, ship_direction, ship_animation = \
                    set_event(DUNGEON_WIDTH, DUNGEON_HEIGHT, DUNGEON)

            if 6 <= tmr <= 9:
                h = 80 * (10 - tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if tmr == 10:
                # next ship move
                idx = 1
        # view item
        elif idx == 3:
            view_dungeon(
                screen,
                ship_xposition,
                ship_ypostition,
                DUNGEON,
                DUNGEON_WIDTH,
                DUNGEON_HEIGHT,
                ship_animation
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            screen.blit(imgItem[treasure], [320, 220])
            view_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
            if tmr == 10:
                idx = 1
        # game over
        elif idx == 9:
            # lose battle from 29
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                ship_animation = PL_TURN[tmr % 4]
                if tmr == 30:
                    # 9 lose image
                    ship_animation = 8
                view_dungeon(
                    screen,
                    ship_xposition,
                    ship_ypostition,
                    DUNGEON,
                    DUNGEON_WIDTH,
                    DUNGEON_HEIGHT,
                    ship_animation
                )
                view_ship_score(
                    screen, font_s,
                    ship_life, ship_life_max, ship_str, food,
                    chopper_cure, help_shipment, tmr
                )
            elif tmr == 31:
                se[3].play()
                # view text
                view_text(screen, "You died.", 360, 240, font, RED)
                view_text(screen, "Game over.", 360, 380, font, RED)
            # top
            elif tmr == 100:
                idx = 0
                tmr = 0

        # battle start
        elif idx == 10:
            # initiate battle filed
            if tmr == 1:
                pygame.mixer.music.load("sound/battle.ogg")
                pygame.mixer.music.play(-1)
                (
                    imgEnemy, enemy_name, enemy_skill,
                    enemy_life_max, enemy_life, enemy_str,
                    enemy_x, enemy_y,
                ) = init_battle(floor)
                init_message()
                back_number = random.randint(0, 3)
            # view back
            elif tmr <= 4:
                bx = (4 - tmr) * 220
                by = 0
                screen.blit(imgBack[back_number], [bx, by])
                view_text(screen, "Encounter!", 350, 200, font, WHITE)
            # effect & message
            elif tmr <= 16:
                dmg_eff, enemy_blink = view_battle(
                    screen, font_s, message_list, imgBack[back_number],
                    imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                    dmg_eff,
                )
                view_ship_score(
                    screen, font_s,
                    ship_life, ship_life_max, ship_str, food,
                    chopper_cure, help_shipment, tmr
                )
                view_text(screen, enemy_name + " appear!", 300, 200, font, WHITE)
            else:
                # next user turn
                idx = 11
                tmr = 0

        # user turn & input
        elif idx == 11:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("Your turn.")
            entry, btl_cmd = battle_command(screen, font_s, key, btl_cmd, tmr)
            if entry:
                if btl_cmd == 0:
                    # next attack
                    idx = 12
                    tmr = 0
                if btl_cmd == 1 and chopper_cure > 0 and ship_life < ship_life_max:
                    # next chopper cure
                    idx = 20
                    tmr = 0
                if btl_cmd == 2 and help_shipment > 0:
                    # next help shipment
                    idx = 21
                    tmr = 0
                if btl_cmd == 3:
                    # next run
                    idx = 14
                    tmr = 0
        # user attack
        elif idx == 12:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("Gum-Gum Pistol!!")
                se[0].play()
                dmg = ship_str + random.randint(0, 9)
            # attack effect
            if 2 <= tmr <= 6:
                screen.blit(imgEffect[0], [200, 200])
                view_text(screen, "Gum-Gum Pistol!", 250, 400, font_skill, RED)
            if tmr == 7:
                enemy_blink = 5
                set_message(str(dmg) + "pts of damage!")
            if tmr == 13:
                enemy_life = enemy_life - dmg
                if enemy_life <= 0:
                    enemy_life = 0
                    # next win
                    idx = 16
                    tmr = 0
            if tmr == 18:
                # next enemy turn
                idx = 13
                tmr = 0
        # enemy turn
        elif idx == 13:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("Enemy turn.")
            if tmr == 5:
                set_message(enemy_name + " attack!")
                set_message(enemy_skill + "!")
                se[0].play()
                # for enemy attack
                enemy_step = 30
            if 6 <= tmr <= 13:
                view_text(screen, enemy_skill + "!", 200, 400, font_skill, RED)
            if tmr == 14:
                dmg = enemy_str + random.randint(0, 9)
                set_message(str(dmg) + "pts of damage!")
                # for user damage effect
                dmg_eff = 7
                enemy_step = 0
            if tmr == 21:
                ship_life = ship_life - dmg
                if ship_life < 0:
                    ship_life = 0
                    # next lose
                    idx = 15
                    tmr = 0
            if tmr == 26:
                # next user turn & input
                idx = 11
                tmr = 0
        # run
        elif idx == 14:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("...")
            if tmr == 2:
                set_message("......")
            if tmr == 3:
                set_message(".........")
            if tmr == 4:
                set_message("............")
            if tmr == 5:
                if random.randint(0, 99) < 60:
                    # if run success, next finish battle
                    idx = 22
                else:
                    set_message("You failed to flee.")
            if tmr == 10:
                # if run fail, next enemy turn
                idx = 13
                tmr = 0
        # lose
        elif idx == 15:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.")
            if tmr == 11:
                # game over
                idx = 9
                tmr = 29
        # win
        elif idx == 16:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("You win!")
                pygame.mixer.music.stop()
                se[5].play()
            if tmr == 28:
                # next finish battle
                idx = 22
                if random.randint(0, enemy_life_max) > random.randint(0, ship_life_max):
                    # next level up
                    idx = 17
                    tmr = 0
        # level up
        elif idx == 17:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("Level up!")
                se[4].play()
                lif_p = random.randint(10, 20)
                str_p = random.randint(5, 10)
            if tmr == 21:
                set_message("Max life + " + str(lif_p))
                ship_life_max = ship_life_max + lif_p
            if tmr == 26:
                set_message("Str + " + str(str_p))
                ship_str = ship_str + str_p
            if tmr == 50:
                # next finish battle
                idx = 22
        # chopper cure
        elif idx == 20:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            if tmr == 1:
                set_message("Chopper Cure!")
                se[2].play()
            # chopper effect
            if 2 <= tmr <= 5:
                bx = (tmr-2) * 27
                screen.blit(imgChopperM, [bx, 100])
            if 6 <= tmr <= 10:
                screen.blit(imgChopperM, [90, 100])
                view_text(screen, "I'll cure Luffy!", 120, 100, font_skill, GREEN)
            if tmr == 11:
                recovery_amount = random.randint(100, 500)
                ship_life += recovery_amount
                if ship_life > ship_life_max:
                    ship_life = ship_life_max
                chopper_cure = chopper_cure - 1
                set_message("LIFE " + str(recovery_amount) + " UP!")
            if tmr == 17:
                # next enemy turn
                idx = 13
                tmr = 0
        # help shipment
        elif idx == 21:
            dmg_eff, enemy_blink = view_battle(
                screen, font_s, message_list, imgBack[back_number],
                imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
                dmg_eff,
            )
            view_ship_score(
                screen, font_s,
                ship_life, ship_life_max, ship_str, food,
                chopper_cure, help_shipment, tmr
            )
            # effect
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30 * tmr, (12 - tmr) / 8)
            X = 440 - img_rz.get_width() / 2
            Y = 360 - img_rz.get_height() / 2
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                shipment_number = random.randint(0, 8)
                set_message("Help Shipment! " + SHIPMENT_NAME[shipment_number])
                se[1].play()
            if 2 <= tmr <= 10:
                bx = (tmr-2) * 10
                screen.blit(imgShipment[shipment_number], [bx, 100])
                view_text(screen, "I'll help Luffy!", 120, 100, font, RED)
            if 11 <= tmr <= 19:
                screen.blit(imgShipment[shipment_number], [90, 100])
                view_text(screen, SHIPMENT_SKILL[shipment_number], 250, 400, font_skill, RED)
            if tmr == 20:
                set_message(SHIPMENT_SKILL[shipment_number]+"!")
                help_shipment = help_shipment - 1
                enemy_life = enemy_life - 1000
                if enemy_life <= 0:
                    enemy_life = 0
                    # next win
                    idx = 16
                    tmr = 0
            if tmr == 21:
                # next enemy turn
                idx = 13
                tmr = 0
        # battle end
        elif idx == 22:
            pygame.mixer.music.load("sound/field.ogg")
            pygame.mixer.music.play(-1)
            # next ship move
            idx = 1

        # view speed
        view_text(screen, "[S]peed " + str(speed), 740, 40, font_s, WHITE)

        pygame.display.update()
        # draw per minutes according to speed
        clock.tick(4 + 2 * speed)


if __name__ == '__main__':
    main()
