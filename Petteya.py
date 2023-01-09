from tkinter import *
from tkinter.messagebox import showinfo, askyesno
import copy

location_x1=-1
chech_move=True

#загруpка картинок шашек
def load_image():
    global checker
    white_checker=PhotoImage(file="White.png")
    black_checker=PhotoImage(file="Black.png")
    checker=[0,white_checker,black_checker]

#новая игра
def new_game():
    global board_checker
    #растановка шашек в начаое игры
    #0 - пустое поле
    #1 - белая шашка
    #2 - черная шашка

    board_checker=[[2,2,2,2,2,2,2,2],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0,0],
                   [1,1,1,1,1,1,1,1]]

#рисуем игровое поле
def draw_board(x1,y1,x2,y2):
    x=0
    global checker
    global board_checker
    global select_board_canvas,mouse_board_canvas
    #удаляем с канаваса
    board_canvas.delete('all')
    select_board_canvas=board_canvas.create_rectangle(-5, -5, -5, -5,outline="gray",width=5)
    mouse_board_canvas=board_canvas.create_rectangle(-5, -5, -5, -5,outline="gray",width=5)
    
    #масштаб шашки
    k=50
    
    #рисуем доску
    #четные поля
    while x<8*k:
        y=1*k
        while y<8*k:
            board_canvas.create_rectangle(x, y, x+k, y+k,fill="brown")
            y+=2*k
        x+=2*k
    x=1*k
    
    #не четные поля
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            board_canvas.create_rectangle(x, y, x+k, y+k,fill="brown")
            y+=2*k
        x+=2*k
    
    #рисуем шашки
    for y in range(8):
        for x in range(8):
            z=board_checker[y][x]
            if z:  
                if (x1,y1)!=(x,y):#стоячие шашки?
                    board_canvas.create_image(x*k,y*k, anchor=NW, image=checker[z])
    #рисуем активную шашку         
    z=board_checker[y1][x1]
    if z:
        board_canvas.create_image(x1*k,y1*k, anchor=NW, image=checker[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x1<x2 else -1
    ky = 1 if y1<y2 else -1
    #анимация перемещения шашки
    for i in range(abs(x1-x2)):
        for j in range(33):
            board_canvas.move('ani',0.03*k*kx,0.03*k*ky)
            board_canvas.update()

#движение мышкой по клеткам
def move_mouse(event):
    #опредлеем координаты клетки
    x,y=(event.x)//50,(event.y)//50
    #рамка в выбранной клетке
    board_canvas.coords(mouse_board_canvas,x*50,y*50,x*50+50,y*50+50)

#нажатие на клетку
def click_mouse(event):
    global location_x1,location_y1,location_x2,location_y2
    global chech_move
    x,y=(event.x)//50,(event.y)//50#вычисляем координаты клетки
    #print(x,y),
    #проверяем наличие шашки
    #проверяем шашку в выбранной клетке
    if board_checker[y][x]==1 or board_checker[y][x]==2:
        #рисуем рамку
        board_canvas.coords(select_board_canvas,x*50,y*50,x*50+50,y*50+50)
        location_x1,location_y1=x,y
    else:
        #клетка выбрана    
        if location_x1!=-1:
            location_x2,location_y2=x,y
            if chech_move:#ход игрока
                turn_player()
                if not(chech_move):
                    #если ход сделан проверяем все возможные исходы
                    check_game()
            #клетка не выбрана
            location_x1=-1
            #рамка вне поля
            board_canvas.coords(select_board_canvas,-5,-5,-5,-5)              

#проверка хода игрока
def turn_player ():
    global location_x1,location_y1,location_x2,location_y2
    global chech_move
    #ход произведен
    chech_move = False
    #создаем список возможных ходов для игроков
    list_white = check_moves_white([])
    list_black = check_moves_black([])
        
    #провеяем ход на возможность
    if list_white and list_black:
        #для белых проверяем ход на соответствие правилам игры
        if ((location_x1,location_y1),(location_x2,location_y2)) in list_white:
            #делаем ход
            do_move= turn_checkers(1,location_x1,location_y1,location_x2,location_y2)            
        #для черных проверяем ход на соответствие правилам игры        
        elif ((location_x1,location_y1),(location_x2,location_y2)) in list_black:
            #делаем ход    
            do_move= turn_checkers(1,location_x1,location_y1,location_x2,location_y2)                    
        else:
            #ход невыполнен
            chech_move=True
    board_canvas.update()
            
#меняем положение шашки
def turn_checkers(f,location_x1,location_y1,location_x2,location_y2):
    global board_checker
    if f:
        draw_board(location_x1,location_y1,location_x2,location_y2)  #рисуем игровое поле

    #делаем ход           
    board_checker[location_y2][location_x2]=board_checker[location_y1][location_x1]
    board_checker[location_y1][location_x1]=0

    #забираем шашку
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if board_checker[y][x]==1 and board_checker[location_y2][location_x2] != 1:
                if board_checker[y][x-1]==2 and board_checker[y][x+1]==2 or board_checker[y-1][x]==2 and board_checker[y+1][x]==2:
                    board_checker[y][x]=0
            if board_checker[y][x]==2 and board_checker[location_y2][location_x2] != 2:
                if board_checker[y][x-1]==1 and board_checker[y][x+1]==1 or board_checker[y-1][x]==1 and board_checker[y+1][x]==1:
                    board_checker[y][x]=0
                
    if f:draw_board(location_x1,location_y1,location_x2,location_y2)#рисуем игровое поле

#проверка наличия ходов
def check_moves_white(list_white):
    list_white=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            list_white=check_moves_whitep(list_white,x,y)
    return list_white

#проверка наличия ходов
def check_moves_whitep(list_white,x,y):
    if board_checker[y][x]==1: #шашка
        for new_x,new_y in (-1,0),(0,1),(1,0),(0,-1):
            if 0<=y+new_y<=7 and 0<=x+new_x<=7:
                if board_checker[y+new_y][x+new_x]==0:
                    list_white.append(((x,y),(x+new_x,y+new_y)))
    return list_white

#проверка наличия ходов
def check_moves_black(list_black):
    for y in range(8):#сканируем всё поле
        for x in range(8):
            list_black=check_moves_blackp(list_black,x,y)
    return list_black

#проверка наличия ходов
def check_moves_blackp(list_black,x,y):
    if board_checker[y][x]==2:
        for new_x,new_y in (-1,0),(0,1),(1,0),(0,-1):
            if 0<=y+new_y<=7 and 0<=x+new_x<=7:
                if board_checker[y+new_y][x+new_x]==0:
                        list_black.append(((x,y),(x+new_x,y+new_y)))  #запись хода в конец списка
    return list_black

#проверка шашек на поле
def check_checkers():
    global board_checker
    result_black=0
    result_white=0
    for i in range(8):
        for j in board_checker[i]:
            if j==1:result_white+=1
            if j==2:result_black+=3
    return result_white,result_black

#проверка исходов игры   
def check_game():#!!!
    global chech_move
    chech_move=True
    #определяем победителя 
    result_white,result_black=check_checkers()
    if not(result_black):
            end_game(2)
    elif not(result_white):
            end_game(1)

#конец игры
def end_game(s):
    global chech_move
    if s==1:
        i=askyesno(title='Игра завершена', message='Белые победили!\nНажми "Да" что бы начать заново.',icon='info')
    if s==2:
        i=askyesno(title='Игра завершена', message='Черные победили!\nНажми "Да" что бы начать заново.',icon='info')
    if i:
        new_game()
        #рисуем игровое поле
        draw_board(-1,-1,-1,-1)
        chech_move=True

#создаём окно
game_window=Tk()
#указываем заголовок окна
game_window.title('Петтейя')
#создадим конву для игры
board_canvas=Canvas(game_window, width=400,height=400,bg='#EEEEDD')
board_canvas.pack()
#загружаем изображения шашек
load_image()
#начинаем новую игру
new_game()
#рисуем игровое поле
draw_board(-1,-1,-1,-1)
#перемещение курсора мыши
board_canvas.bind("<Motion>", move_mouse)
#нажатие ЛКМ
board_canvas.bind("<Button-1>", click_mouse)
mainloop()