# External File Modules
from sys import float_repr_style
import login
import txtinput
import ptext
import imagekit
import selector

# External Download Modules
# Login.py > dnspython, cryptography, pymongo
import pygame
import pymongo
import pygame_menu

# Internal Moudles
import sys
import traceback
import platform
import logging
import os
from os import write

# Main Code

def init() :
    global screen, clock
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("RGX 5.0")
    os.remove('game.log')
    logging.basicConfig(format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s', filename="game.log", level=logging.DEBUG)
    logging.info("[RGX 5.0 Game Log]")
    logging.info("Game Init Finished!")

def txtin(str=None, strpos=(10,10), mode=0, pos=(10,10)) :
    global screen, clock
    textinput = txtinput.TextInput()
    if(mode == 0):
        textinput.password = False
    else :
        textinput.password = True
    pygame.display.flip()
    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(textinput.get_surface(), pos)
        
        if textinput.update(events):
            return textinput.get_text()
        ptext.draw(str, (10,10), fontsize=textinput.font_size, fontname='assets/NanumBarunGothic.ttf', color="#000000")
        pygame.display.update()
        clock.tick(30)

def popup(str1, pos, alpha=100, color=(255,0,0)):
    c = ptext.draw(str1, pos, fontsize=40, fontname='assets/NanumBarunGothic.ttf')
    s = pygame.Surface((int(c[0].get_rect()[2])+20, int(c[0].get_rect()[3])+20))
    s.set_alpha(alpha)
    s.fill(color) 
    screen.blit(s, (pos[0]-10,pos[1]-10))
    pygame.display.update()
    c = ptext.draw(str1, pos, fontsize=40, fontname='assets/NanumBarunGothic.ttf')
    pygame.display.update()

def popup1(str1, alpha=100, color=(255,0,0)) :
    j = len(str1)
    j = int((j / 2) * 12)
    if(450 - j < 0): j = 450
    for i in range(0, 200, 10) :
        screen.fill((0,0,0))
        popup(str1, (450-j, 800-i), alpha, color)
        pygame.display.update()
    pygame.time.delay(1000)
    for i in range(200, 0, -10) :
        screen.fill((0,0,0))
        popup(str1, (450-j, 800-i), alpha, color)
        pygame.display.update() 

def log() :
    id = txtin("Enter ID",(10,10), 0, (10,50))
    pw = txtin("Enter PW",(10,10), 1, (10,50))

    if id == "guest" : # offline guest login
        if pw == "guest" :
            return {'id' : 'guest', 'pw' : 'guest', 'level' : '1', 'exp' : '0'}
        else :
            return -2

    login1 = login.login1()
    try :
        data = login1.main(id, pw)
    except pymongo.errors.ServerSelectionTimeoutError :
        logging.critical('Login Error : Received From Login : %s', str(sys.exc_info()[0]))
        logging.warning('Can\'t connect to Login Server. (TimeOut) Please try again.')
        data = -6
    except pymongo.errors.ConfigurationError :
        logging.critical('Login Error : Received From Login : %s', str(sys.exc_info()[0]))
        logging.warning('Can\'t connect to Login Server. (TimeOut) Please try again.')
        data = -6
    except :
        logging.critical('Login Error : Received From Login : %s', str(sys.exc_info()[0]))
        logging.critical('More Detailed Info : ')
        logging.critical(str(traceback.format_exc()))
        logging.warning('Can\'t connect to Login Server. Please try again.')
        data = None
    return data

def displaymain() :
    global menu
    image = imagekit.BACKGROUND
    screen.blit(image,(0,0))
    ptext.draw("RhythmGameX", (30,150), fontsize=50, fontname="assets/CookieRun Bold.ttf", italic=True)
    ptext.draw("Ver. 5.0 | 1.0b", (250,215), fontsize=20, fontname="assets/NanumBarunGothic.ttf")
    ptext.draw("< " + menu.print() + " >", (50, 550), fontsize=40, fontname="assets/CookieRun Bold.ttf")
    pygame.display.update()
def main() :
    try :
        global screen, clock, m1, menu
        scene = 0
        r = None
        menu = None
        while True :
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RETURN :
                        if scene == -2:
                            r = log()
                            if(type(r) == type({'a' : '1'})) :
                                scene = -3
                            elif r == -1 :
                                #ptext.draw("Connection Time Out. Please Retry.", (250,300), fontsize=40, fontname="assets/NanumbarunGothic.ttf", color="#ffffff")
                                pygame.display.flip()
                                pygame.time.delay(2000)
                                scene = -1
                            else :
                                #print("Login ERR : Code " + str(r))
                                logging.warning('Login Error : Received From Login : %s' % str(r))
                                scene = -1
                        elif scene == 3:
                            if menu.rptr() == 0 :
                                logging.info('Entering Login Session...')
                                r = log()
                                if(type(r) == type({'a' : '1'})) :
                                    logging.info('Login Success')
                                    logging.debug('UserID : %s'% r['id'])
                                    scene = 10
                                elif r == -1 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Unexpected Error.')
                                    popup1('Unexpected Error.')
                                    scene = 10
                                elif r == -2 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('\'guest\' is the password of the default account (\'guest\'). ')
                                    popup1('Login Error : \'guest\' is the password of the default account (\'guest\').')
                                    scene = 1
                                elif r == -3 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Inappropriate ID. No Space is allowed.')
                                    popup1('Login Error : Inappropriate ID. No Space is allowed.')
                                    scene = 1
                                elif r == -4 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Password should be more than 4 characters.')
                                    popup1('Login Error : Password should be more than 4 characters.')
                                    scene = 1
                                elif r == -5 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Register Failed') 
                                    popup1('Login Error : Register Failed')
                                    scene = 1
                                elif r == -6 :
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Connection Time Out')
                                    popup1('Login Error : Connection Time Out')
                                    scene = 1           
                                elif r == 1 :
                                    #logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.warning('Login Error : Received From Login : %s' % str(r))
                                    logging.info('Login Error : Password Incorrect')
                                    popup1('Login Error : Password Incorrect')
                                    scene = 1                                 
                            elif menu.rptr() == 1 :
                                scene = 5
                            elif menu.rptr() == 2 : 
                                scene = 7            

                    elif event.key == pygame.K_RIGHT :
                        if scene == 3:
                            menu.right()
                            scene = 2
                    elif event.key == pygame.K_LEFT :
                        if scene == 3:
                            menu.left()
                            scene = 2
                if scene == 0 :
                    for i in range(0,255,20) :
                        screen.fill((255,255,255))
                        #img("assets/Logo.png", 450, 50, 400, 400,(0,0,0), i)
                        image = imagekit.LOGO.convert()
                        image.set_alpha(i)
                        screen.blit(image, image.get_rect().move((450,50)))
                        ptext.draw("Made by sfcatz", (350,400), fontsize=80, fontname="assets/CookieRun Bold.ttf", color="#000000")
                        pygame.display.update()
                        pygame.event.pump()
                        pygame.time.delay(20)
                    pygame.time.delay(2000)
                    #scene = 1
                    #scene = -1
                    scene = 1

                elif scene == -1:
                    screen.fill((0,0,0))
                    #print("Entering Test Page...")
                    logging.info('Entering Login Page | Scenenum = %s' % str(scene))
                    ptext.draw("Press Enter to Login.\nThis is test page.", (20, 550), fontsize=60, fontname="assets/NanumBarunGothic.ttf", color="#FFFFFF")
                    pygame.display.flip()
                    scene = -2
                elif scene == -2 :
                    pass
                elif scene == -3 :
                    screen.fill((0,0,0))
                    logging.info('Loggin Sucess! | Scenenum = %s' % str(scene))
                    ptext.draw("Hello, %s\nCurrent Score : %d"% (str(r['id']), int(r['score'])), (20,550), fontsize=60, fontname='assets/NanumBarunGothic.ttf', color="#FFFFFF")
                    pygame.display.flip()
                    scene = -4
                elif scene == -4 :
                    pass
                elif scene == 1 :
                    menu = selector.selector(['Play', 'Options', 'Credits'])
                    logging.info("Entering Main Page...")
                    scene = 2
                elif scene == 2 :
                    displaymain()
                    scene = 3
                elif scene == 3 :
                    pass
                elif scene == 4 :
                    pass
                elif scene == 5 :
                    # Options
                    logging.info('Entering Options Page...')
                    scene = 1
                elif scene == 7 :
                    # Credits
                    logging.info('Entering Credits Page...')
                    scene = 1
                elif scene == 10 :
                    screen.fill((0,0,0))
                    pygame.display.flip()
                    logging.info('Entering Select Page...')
                    popup1('SelectPage / Scenenum : 10', 100, (0,255,0))
                    
    except SystemExit:
        logging.info('Received Exit Signal. Process Terminated.')
        sys.exit(0)
    except :
        logging.critical('Unexpected Error From Main : Error Data : %s' % sys.exc_info()[0])
        logging.critical('More Detailed Info :')
        logging.critical(str(traceback.format_exc()))
        logging.critical('Game Crashed!')
        logging.info('Send this log File to Developer')
        logging.info('=' * 100)
        logging.info('System Info : %s / %s' % (str(platform.platform()), str(platform.machine())))
        return
init()
main()