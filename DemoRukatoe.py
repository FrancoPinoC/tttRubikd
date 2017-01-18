from Rukube import *
from Inits import *
import math
from Auxiliary import *
# Factor de ampliacion de imagen (entre menor es, mas grande se ve el objeto modelado)
zmK = 1.6
w = 700
h = 700
init_pygame((w, h), "woooo")
init_opengl((w, h), zmK)

glLoadIdentity()
# Miramos hacia el centro, desde el lado negativo de Z, con un UP en el eje Y
gluLookAt(200.0, 200.0, -2000.0, 0.0, 0.0, 0.0, 0, 1, 0)
t0 = pygame.time.get_ticks()

# Variable bandera
flog = 0

# Angulos de giro
# ~      Y
# ~      ^
# ~      |  (para ejes 3D-mensionales)
# ~      |
# ~ X<---(Z hacia dentro)
roAngs = [0.0, 0.0, 0.0]

# Factor de velocidad de giro en relacion a velocidad del mouse (entre mas grande mas rapido gira el cubo)
rotK = 130

# Iniciar cubo(s)
ladoc1 = 200
ruk = Rukube(ladoc1)
# cubeColors=(front, L, back, R, top, bottom)
cubeColors = [ylw] + [green] + [red] + [prpl] + [cyan] + [orng]
cube2Colors = [ylw] + [green] + [grey] + [cyan] + [red] + [orng]
moves = ''
# Da el lado "adyacente" usado en atan2 !*!
trigoY = ladoc1
Player = 1
instrucciones1 = "- Click and drag to rotate the whole cube around.\n" \
                 "- Hover your mouse over the cell you want to mark,\n" \
                 "  then press the spacebar to do so. P1 is red, P2 is green.\n" \
                 "- How to rotate individual faces \n" \
                 "   f: Front face (the one that faces you when the cube is still)\n" \
                 "   r: Right\n" \
                 "   l: Left\n" \
                 "   d: Down\n" \
                 "   t: Top\n" \
                 "   e: Equator (horizontal line)\n" \
                 "   m: Middle (vertical line)\n" \
                 "  Clockwise rotations by default.\n" \
                 "  Right click while pressing the buttons to make it counterclockwise.\n" \
                 "(unfinished demo)"
tu1 = "Turno de jugador 1"
tu2 = "Turno de jugador 2"
print instrucciones1
print tu1
run = True
while run:
    t1 = pygame.time.get_ticks()
    dt = (t1 - t0)
    t0 = t1
    # ~ o1+=w1*dt
    # ~ o2+=w2*dt
    keystate = pygame.key.get_pressed()
    clickstate = pygame.mouse.get_pressed()
    if clickstate[0]:
        if flog == 0:
            pos0 = mousePos(w, h)
            flog = 1
        else:
            pos1 = mousePos(w, h)
            # Mov horizontal provoca giro horizontal, que se aplica sobre el eje Y (por lo que se usa roAng[1]=ang en Y)
            roAngs[1] += (math.atan2(pos0[0], trigoY) - math.atan2(pos1[0], trigoY)) * rotK  # !*!
            # Un giro vertical se aplica en el eje X
            roAngs[0] += (math.atan2(pos0[1], trigoY) - math.atan2(pos1[1], trigoY)) * rotK
            pos0 = pos1
    else:
        flog = 0
        roAngs = [0.0, 0.0, 0.0]
    # If the cube is not being moved, see if the mouse is over any of the front cells and if so, color that cell blue
    ind = mouseOverQ(zmK, ladoc1, w, h, offset) if not flog else None
    ruk.setMultiColors(range(26), [egg] * 6, False)
    if ind != None:
        ruk.setSingleColors(ind, [blue] + [egg] * 5)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE and ind != None and ruk.FV[ind] == 0:
                ruk.marcar(k=ind, P=Player)
                Player = Player % 2 + 1
                if Player == 1:
                    print tu1
                else:
                    print tu2
            if event.key == K_t:
                moves = 't'
            if event.key == K_l:
                moves = 'l'
            if event.key == K_r:
                moves = 'r'
            if event.key == K_d:
                moves = 'd'
            if event.key == K_f:
                moves = 'f'
            if event.key == K_e:
                moves = 'e'
            if event.key == K_m:
                moves = 'm'
            if event.key == K_c:
                moves = 'color'
                print 'colores! \n Presione ENTER para cancelar'
            if event.key == K_RETURN:
                moves = ''

        if event.type == QUIT:
            run = False

    ruk.paintAllMarkedFaces([[red], [green]])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)

    if moves == '':
        ruk.draw(cExploreRot=True, cAngs=roAngs, cRot=[1, -1, 0])
    elif moves == 'color':
        ruk.draw(cRGBL=cube2Colors, cExploreRot=True, cAngs=roAngs, cRot=[1, -1, 0])
    else:
        ruk.draw(cExploreRot=True, cAngs=roAngs, cRot=[1, -1, 0])
        #ruk.draw(move=moves)
        # Meaning: If right click is pressed, make it counter-clockwise
        isClockwise = not clickstate[2]
        if moves == 't':
            ruk.turnUp(isClockwise)
        elif moves == 'l':
            ruk.turnLeft(isClockwise)
        elif moves == 'r':
            ruk.turnRight(isClockwise)
        elif moves == 'd':
            ruk.turnDown(isClockwise)
        elif moves == 'f':
            ruk.turnFront(isClockwise)
        elif moves == 'e':
            ruk.turnEquator(isClockwise)
        elif moves == 'm':
            ruk.turnMiddle(isClockwise)
        moves = ''
    glPolygonMode(GL_FRONT, GL_LINE)
    glPolygonMode(GL_BACK, GL_LINE)
    ruk.draw(cRGBL=[black] * 6, cExploreRot=True, cAngs=roAngs, cRot=[1, -1, 0])

    pygame.display.flip()
    pygame.time.wait(1000 / 100)
pygame.quit()
sys.exit
