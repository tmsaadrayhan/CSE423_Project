from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from random import randint
from time import sleep
import numpy as np

player_name = input("Enter your name: ")
while not player_name.isalpha():
    print("Only alphabets are allowed!")
    player_name = input("Enter your name: ")



#Functions

def roll_dice():
    return randint(1, 6)

# Deaws point (x, y)
def draw_points(x, y):
   glPointSize(3)
   glBegin(GL_POINTS)
   glVertex2f(x, y)
   glEnd()




def transform(x, y, t):
   if t[0] < 0:
       x = -x
   if t[1] < 0:
       y = -y
   if abs(t[0]) == 2:
       x, y = y, x
   return (x, y)


# Line drawing funcitn, form (x0, y0) to (x1, y1)
def draw_lines(x0, y0, x1, y1):
   dx = x1 - x0
   dy = y1 - y0
   t = [1, 2]
   if dx < 0:
       dx = -dx
       x0 =  -x0
       x1 = -x1
       t[0] = -t[0]
   if dy < 0:
       dy = -dy
       y0 = -y0
       y1 = -y1
       t[1] = -t[1]
   if dy > dx:
       t = t[1], t[0]
       dx, dy = dy, dx
       x0, y0 = y0, x0
       x1, y1 = y1, x1

   d = 2*dy - dx
   incE = 2*dy
   incNE = 2*(dy - dx)
   y = y0
   for x in range(x0, x1):
       draw_points(*transform(x, y, t))
       if d >= 0:
           d += incNE
           y += 1
       else:
           d += incE
   draw_points(*transform(x1, y1, t))


def seven_seg(x, y, z, scale):
   for i in range(3):
       if i in z:
           draw_lines(x, y+scale*i, x+scale, y+scale*i)
   for i in range(2):
       if 3+i in z:
           draw_lines(x+scale*i, y, x+scale*i, y+scale)
       if 5+i in z:
           draw_lines(x+scale*i, y+scale, x+scale*i, y+scale*2)


def big_seg(x, y, z, scale):
    if 1 in z: draw_lines(x, y, x, y+scale)
    if 2 in z: draw_lines(x+scale, y, x+scale, y+scale)
    if 3 in z: draw_lines(x, y+scale, x, y+2*scale)
    if 4 in z: draw_lines(x+scale, y+scale, x+scale, y+scale*2)
    if 5 in z: draw_lines(x, y, x+scale, y)
    if 6 in z: draw_lines(x, y+scale, x+scale, y+scale)
    if 7 in z: draw_lines(x, y+2*scale, x+scale, y+2*scale)
    if 8 in z: draw_lines(x, y+2*scale, x+scale//2, y+scale)
    if 9 in z: draw_lines(x+scale//2, y+scale, x+scale, y+2*scale)
    if 10 in z: draw_lines(x+scale//2, y+scale, x+scale, y)
    if 11 in z: draw_lines(x+scale//2, y+scale, x, y)
    if 12 in z: draw_lines(x+scale//2, y, x+scale//2, y+2*scale)
        


#Digit draw, (x, y) postion of the bottom-left corner of the digit, d
def draw_digit(x, y, d, scale):
   if d in [0, 1, 3, 4, 7, 8, 9]:
       seven_seg(x, y, [4, 6], scale)
   if d in [0, 2, 3, 5, 6, 8, 9]:
       seven_seg(x, y, [0, 2], scale)
   if d in [2, 3, 4, 5, 6, 8, 9]:
       seven_seg(x, y, [1], scale)
   if d in [0, 6, 8]:
       seven_seg(x, y, [3, 5], scale)
   if d in [4, 5, 9]:
       seven_seg(x, y, [5], scale)
   if d == 2:
       seven_seg(x, y, [3, 6], scale)
   if d in [5, 6]:
       seven_seg(x, y, [4], scale)
   if d == 7:
       seven_seg(x, y, [2], scale)

alphabets={
    "A":[1,3,7,4,2,6],
    "B":[1,3,7,5,9,10],
    "C":[7,3,1,5],
    "D":[3,1,8,11],
    "E":[7,3,1,5,6],
    "F":[7,3,1,6],
    "G":[7,3,1,5,10],
    "H":[3,1,4,2,6],
    "I":[12],
    "J":[7,4,2,5,1],
    "K":[12,9,10],
    "L":[3,1,5],
    "M":[1,3,8,9,4,2],
    "N":[1,3,8,10,2,4],
    "O":[1,3,7,4,2,5],
    "P":[1,3,7,4,6],
    "Q":[1,3,7,4,2,5,10],
    "R":[1,3,7,4,6,10],
    "S":[7,3,6,2,5],
    "T":[7,12],
    "U":[3,1,5,2,4],
    "V":[3,1,11,9],
    "W":[3,1,11,10,2,4],
    "X":[8,9,10,11],
    "Y":[8,9,11],
    "Z":[7,9,11,5]
}

dice_position = {}
player_position = 1
ai_position = 1
current_move_no = 0

def alphabet_draw(x, y, c, scale):
    if 'a'<=c<='z' or 'A'<=c<='Z':
        big_seg(x, y, alphabets[c.upper()], scale)
    else:
        print("Enter only alphabets.")

#Draw circle, (a, b) center, r radius
def draw_circles(a, b, r):
   x = 0
   y = r
   d = 1-r
   points = []
   while x<=y:
       points.append((x, y))
       if d<0:
           d += 2*x + 3
       else:
           d += 2*x - 2*y +5
           y -= 1
       x += 1

   for p in points:
       x, y = p
       for i in [x, -x]:
           for j in [y, -y]:
               draw_points(i + a, j + b)
               draw_points(j + a, i + b)


def draw_arrow(x0, y0, x1, y1):
    s = np.array([[0], [0], [1]])
    e = np.array([[10], [0], [1]])
    c1 = np.array([[8], [1], [1]])
    c2 = np.array([[8], [-1], [1]])

    angle = np.pi/2
    if x1 != x0:
        angle = np.arctan((y1-y0)/(x1-x0)) - np.pi*((x1-x0)/abs(x1-x0)-1)/2
    elif y1 < y0:
        angle = -angle
    scale = np.sqrt((x1-x0)**2+(y1-y0)**2)/10
    ts = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
    tr = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    ttm = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]])
    ttc = np.array([[1, 0, -10], [0, 1, 0], [0, 0, 1]])
    ttcb = np.array([[1, 0, x1], [0, 1, y1], [0, 0, 1]])

    tmain = np.matmul(ttm, np.matmul(tr, ts))
    tc = np.matmul(ttcb, np.matmul(tr, np.matmul(ts, ttc)))
    l1p1 = np.matmul(tmain, s)
    l1p2 = np.matmul(tmain, e)
    l2p2 = np.matmul(tc, c1)
    l2p3 = np.matmul(tc, c2)
    z11x = int(l1p1[0][0])
    z11y = int(l1p1[1][0])
    z12x = int(l1p2[0][0])
    z12y = int(l1p2[1][0])
    z22x = int(l2p2[0][0])
    z22y = int(l2p2[1][0])
    z23x = int(l2p3[0][0])
    z23y = int(l2p3[1][0])
    draw_lines(z11x, z11y, z12x, z12y)
    draw_lines(z12x, z12y, z22x, z22y)
    draw_lines(z12x, z12y, z23x, z23y)




def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    global current_move_no, player_position, ai_position, player_name

    if player_position < 100 and ai_position < 100:
        glColor3f(1, 0.0, 0)
        for i in range(1, 31):
            draw_circles(50, 700, i)
        alphabet_draw(100, 670, "A", 30)
        alphabet_draw(140, 670, "I", 30)


        glColor3f(0, 1, 0)
        for i in range(1, 31):
            draw_circles(200, 700, i)
        for c in range(len(player_name[:7])):
            alphabet_draw(250 + 40*c, 670, player_name[c], 30)
        

        glColor3f(0.8, 0.8, 0.8)
        dice = "ICE"
        alphabet_draw(575, 670, "D", 30)
        for c in range(3):
            alphabet_draw(600+c*40, 670, dice[c], 30)


        glColor3f(0.0, 1, 1)
        dice_val = roll_dice()
        draw_digit(750, 670, dice_val, 30)


        glColor3f(0.1, 0.0, 5.0)


        for i in range(11):
            draw_lines(100+i*60, 40, 100+i*60, 640)
            draw_lines(100, 40+i*60, 700, 40+i*60)
        
        glColor3f(1, 1, 1)
        y_change = -52
        x_change = 8
        for i in range(10):
            for j in range(10):
                if i==9 and j==9:
                    dice_position[100] = (112+x_change, 650+y_change)
                    draw_digit(86+x_change, 650+y_change, 1 , 12)
                    draw_digit(112+x_change, 650+y_change, 0 , 12)
                    draw_digit(135+x_change, 650+y_change, 0 , 12)
                else:
                    if i== 0 and j!= 9:
                        dice_position[(j+1)%10] = (120+j*60+x_change, 110+y_change)
                        draw_digit(120+j*60+x_change, 110+y_change, (j+1)%10 , 12)
                    else:
                        if i%2==0:
                            draw_digit(130+j*60+x_change, 110+i*60+y_change, (j+1)%10 , 12)
                            if j==9:
                                dice_position[10*(i+1)+(j+1)%10] = (105+j*60+x_change, 110+i*60+y_change)
                                draw_digit(105+j*60+x_change, 110+i*60+y_change, i+1 , 12)
                            else:
                                dice_position[10*i+(j+1)%10] = (105+j*60+x_change, 110+i*60+y_change)
                                draw_digit(105+j*60+x_change, 110+i*60+y_change, i , 12)
                        else:
                            draw_digit(670-j*60+x_change, 110+i*60+y_change, (j+1)%10 , 12)
                            if j==9:
                                dice_position[10*(i+1)+(j+1)%10] = (645-j*60+x_change, 110+i*60+y_change)
                                draw_digit(645-j*60+x_change, 110+i*60+y_change, i+1 , 12)
                            else:
                                dice_position[10*i+(j+1)%10] = (645-j*60+x_change, 110+i*60+y_change)
                                draw_digit(645-j*60+x_change, 110+i*60+y_change, i , 12)
        #arrows
        #snakes
        glColor3f(1, 0, 0)
        draw_arrow(413, 178, 308, 58) #26 to 4
        draw_arrow(173, 598,293, 418 ) #99 to 64
        draw_arrow(413, 538,593, 238)  #86 to 32
        draw_arrow(653, 178, 593, 118) #30 to 12
        draw_arrow(293, 298, 293, 178) #44 to 24

        #ladder
        glColor3f(0, 1, 0)

        draw_arrow(188, 58, 173, 178)#2 to 22
        draw_arrow(413, 238, 533, 418 )# 35 to 68
        draw_arrow(353, 538,353, 598) #85 to 96
        draw_arrow(113, 298,173, 478)#41 to 79


        arrows = [(26, 4), (99, 64), (86, 32), (30, 12), (44, 24), (2, 22), (35, 68), (85, 96), (41, 79)]

        if current_move_no > 0 and current_move_no%2==1:
            if player_position + dice_val <= 100:
                player_position += dice_val
            for i in arrows:
                if player_position == i[0]:
                    player_position = i[1]
        x, y = dice_position[player_position]
        glColor3f(0, 1, 0)
        for j in range(1, 14):
            draw_circles(x+13, y+13, j)

        if current_move_no > 0 and current_move_no%2==0:
            if dice_val + ai_position <= 100:
                ai_position += dice_val
            for i in arrows:
                if ai_position == i[0]:
                    ai_position = i[1]
        x, y = dice_position[ai_position]
        glColor3f(1, 0, 0)
        for j in range(1, 14):
            draw_circles(x+16, y+16, j)
        current_move_no += 1
    else:
        winner = player_name[:8]
        glColor3f(0, 1, 0)
        if ai_position == 100:
            winner = 'AI'
            glColor3f(1, 0, 0)
        for i in range(len(winner)):
            alphabet_draw(100+50*i, 350, winner[i], 40)
        wins = 'WINS'
        for i in range(len(wins)):
            alphabet_draw(100+50*len(winner)+60+60*i, 350, wins[i], 40)
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 800) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Snakes & Ladder") #window name
glutDisplayFunc(showScreen)

glutMainLoop()