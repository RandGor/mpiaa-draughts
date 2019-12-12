from tkinter import *
import tkinter.messagebox
import random
import time
import copy



windowMain=Tk()
m = Menu(windowMain) 
windowMain.config(menu=m)



windowMain.title('Английские Шашки')#заголовок окна
desk=Canvas(windowMain, width=800,height=800,bg='#FFFFFF')
desk.pack()

comp_moves=()#конечный список ходов компьютера
intelligence=1#количество предсказываемых компьютером ходов
k_rez=0#!!!
o_rez=0
pos1_x=-1#клетка не задана
playersTurn=True#определение хода игрока(да)


def load_images():#загружаем изображения пешек
    global checkers
    i1=PhotoImage(file="res\\1h.gif")
    i2=PhotoImage(file="res\\1hk.gif")
    i3=PhotoImage(file="res\\1b.gif")
    i4=PhotoImage(file="res\\1bk.gif")
    checkers=[0,i1,i2,i3,i4]

def new_Game():#начинаем новую игру
    global field

    field=[[0,0,0,0,0,0,0,0],
          [0,0,0,0,1,0,4,0],
          [0,0,0,0,0,0,0,0],
          [3,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,2,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]]
    field=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def draw(x_pos_1,y_pos_1,x_pos_2,y_pos_2):#рисуем игровое поле
    global checkers
    global field
    global red_border,green_border
    k=100
    x=0
    desk.delete('all')

    while x<8*k:#рисуем доску
        y=1*k
        while y<8*k:
            desk.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            desk.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    red_border=desk.create_rectangle(-2, -2, -2, -2,outline="red",width=2)
    green_border=desk.create_rectangle(-2, -2, -2, -2,outline="green",width=2)

    for y in range(8):#рисуем стоячие пешки
        for x in range(8):
            z=field[y][x]
            if z:
                if (x_pos_1,y_pos_1)!=(x,y):#стоячие пешки?
                    desk.create_image(x*k,y*k, anchor=NW, image=checkers[z])
    #рисуем активную пешку
    z=field[y_pos_1][x_pos_1]
    if z:
        desk.create_image(x_pos_1*k,y_pos_1*k, anchor=NW, image=checkers[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x_pos_1<x_pos_2 else -1
    ky = 1 if y_pos_1<y_pos_2 else -1
    for i in range(abs(x_pos_1-x_pos_2)):#анимация перемещения пешки
        for ii in range(33):
            desk.move('ani',0.03*k*kx,0.03*k*ky)
            desk.update()#обновление
            time.sleep(0.002)





fm = Menu(m) #создается пункт меню с размещением на основном меню (m)
m.add_cascade(label="Меню",menu=fm)

def destroy():
	exit()

def restart():
        global playersTurn
        new_Game()
        draw(-1,-1,-1,-1)#рисуем игровое поле
        playersTurn=True#ход игрока доступен

def author():
    tkinter.messagebox.showinfo("Авторы", "Демидович Егор\nМуравьёв Михаил\nЦыганков Алексей")


def rules():
    tkinter.messagebox.showinfo("Правила", "*****")

    
fm.add_command(label="Новая игра",command=restart)
fm.add_command(label="Правила",command=rules)
fm.add_command(label="Авторы",command=author)
fm.add_command(label="Выход",command=destroy)




def message(s):
    z='Игра завершена'
    if s==1:
        i=tkinter.messagebox.askyesno(title=z, message='Вы победили!\nНажмите "Да" что бы начать заново.',icon='info')
    if s==2:
        i=tkinter.messagebox.askyesno(title=z, message='Вы проиграли!\nНажмите "Да" что бы начать заново.',icon='info')
    if s==3:
        i=tkinter.messagebox.askyesno(title=z, message='Ходов больше нет.\nНажмите "Да" что бы начать заново.',icon='info')
    if i:
        restart()

        

def pos_1(event):#выбор клетки для хода 1
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    desk.coords(green_border,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке

def pos_2(event):#выбор клетки для хода 2
    global pos1_x,pos1_y,pos2_x,pos2_y
    global playersTurn
    x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
    if field[y][x]==1 or field[y][x]==2:#проверяем пешку игрока в выбранной клетке
        desk.coords(red_border,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке
        pos1_x,pos1_y=x,y
    else:
        if pos1_x!=-1:#клетка выбрана
            pos2_x,pos2_y=x,y
            if playersTurn:#ход игрока?
                player_turn()
                if not(playersTurn):
                    comp_turn()#передаём ход компьютеру
            pos1_x=-1#клетка не выбрана
            desk.coords(red_border,-5,-5,-5,-5)#рамка вне поля              
     
def comp_turn():#ход компьютера
    global playersTurn
    global comp_moves
    check_comp(1,(),[])
    if comp_moves:#проверяем наличие доступных ходов
        kh=len(comp_moves)#количество ходов
        th=random.randint(0,kh-1)#случайный ход
        dh=len(comp_moves[th])#длина хода
        for i in range(dh-1):
            #выполняем ход
            moves=hod(1,comp_moves[th][i][0],comp_moves[th][i][1],comp_moves[th][1+i][0],comp_moves[th][1+i][1])
        comp_moves=[]#очищаем список ходов
        playersTurn=True#ход игрока доступен

    #определяем победителя 
    s_k,s_i=scan()
    if not(s_i):
            message(2)
    elif not(s_k):
            message(1)
    elif playersTurn and not(moves_player()):
            message(3)
    elif not(playersTurn) and not(moves_comp()):
            message(3)

def moves_comp():#составляем список ходов компьютера
    moves=get_comp_turns([])#здесь проверяем обязательные ходы
    if not(moves):
        moves=get_comp_turns_extra([])#здесь проверяем оставшиеся ходы
    return moves

def check_comp(tur,n_moves,moves):#!!!
    global field
    global comp_moves
    global l_rez,k_rez,o_rez
    if not(moves):#если список ходов пустой...
        moves=moves_comp()#заполняем

    if moves:
        k_field=copy.deepcopy(field)#копируем поле
        for ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:#проходим все ходы по списку
            t_moves=hod(0,pos1_x,pos1_y,pos2_x,pos2_y)
            if t_moves:#если существует ещё ход
                check_comp(tur,(n_moves+((pos1_x,pos1_y),)),t_moves)
            else:
                check_player(tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(comp_moves):#записыаем если пустой
                        comp_moves=(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                        l_rez=t_rez#сохряняем наилучший результат
                    else:
                        if t_rez==l_rez:
                            comp_moves=comp_moves+(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                        if t_rez>l_rez:
                            comp_moves=()
                            comp_moves=(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                            l_rez=t_rez#сохряняем наилучший результат
                    o_rez=0
                    k_rez=0

            field=copy.deepcopy(k_field)#возвращаем поле
    else:
        s_k,s_i=scan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def moves_player():#составляем список ходов игрока
    moves=get_player_turns([])#здесь проверяем обязательные ходы
    if not(moves):
        moves=get_player_turns_extra([])#здесь проверяем оставшиеся ходы
    return moves
    
def check_player(tur,moves):
    global field,k_rez,o_rez
    global intelligence
    if not(moves):
        moves=moves_player()

    if moves:#проверяем наличие доступных ходов
        k_field=copy.deepcopy(field)#копируем поле
        for ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:                    
            t_moves=hod(0,pos1_x,pos1_y,pos2_x,pos2_y)
            if t_moves:#если существует ещё ход
                check_player(tur,t_moves)
            else:
                if tur<intelligence:
                    check_comp(tur+1,(),[])
                else:
                    s_k,s_i=scan()#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            field=copy.deepcopy(k_field)#возвращаем поле
    else:#доступных ходов нет
        s_k,s_i=scan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def scan():#подсчёт пешек на поле
    global field
    s_i=0
    s_k=0
    for i in range(8):
        for ii in field[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def player_turn():
    global pos1_x,pos1_y,pos2_x,pos2_y
    global playersTurn
    playersTurn=False#считаем ход игрока выполненным
    moves=moves_player()
    if moves:
        if ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:#проверяем ход на соответствие правилам игры
            t_moves=hod(1,pos1_x,pos1_y,pos2_x,pos2_y)#если всё хорошо, делаем ход            
            if t_moves:#если есть ещё ход той же пешкой
                playersTurn=True#считаем ход игрока невыполненным
        else:
            playersTurn=True#считаем ход игрока невыполненным
    desk.update()#!!!обновление

def hod(f,pos1_x,pos1_y,pos2_x,pos2_y):
    global field
    if f:draw(pos1_x,pos1_y,pos2_x,pos2_y)#рисуем игровое поле
    #превращение
    if pos2_y==0 and field[pos1_y][pos1_x]==1:
        field[pos1_y][pos1_x]=2
    #превращение
    if pos2_y==7 and field[pos1_y][pos1_x]==3:
        field[pos1_y][pos1_x]=4
    #делаем ход           
    field[pos2_y][pos2_x]=field[pos1_y][pos1_x]
    field[pos1_y][pos1_x]=0

    #рубим пешку игрока
    kx=ky=1
    if pos1_x<pos2_x:kx=-1
    if pos1_y<pos2_y:ky=-1
    x_poz,y_poz=pos2_x,pos2_y
    while (pos1_x!=x_poz) or (pos1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if field[y_poz][x_poz]!=0:
            field[y_poz][x_poz]=0
            if f:draw(-1,-1,-1,-1)#рисуем игровое поле
            #проверяем ход той же пешкой...
            if field[pos2_y][pos2_x]==3 or field[pos2_y][pos2_x]==4:#...компьютера
                return get_comp_turn([],pos2_x,pos2_y)#возвращаем список доступных ходов
            elif field[pos2_y][pos2_x]==1 or field[pos2_y][pos2_x]==2:#...игрока
                return get_player_turn([],pos2_x,pos2_y)#возвращаем список доступных ходов
    if f:draw(pos1_x,pos1_y,pos2_x,pos2_y)#рисуем игровое поле

def get_comp_turns(moves):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            moves=get_comp_turn(moves,x,y)
    return moves

def get_comp_turn(moves,x,y):
    if field[y][x]==3:#пешка
        for ix,iy in (-1,1),(1,1):
            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                if field[y+iy][x+ix]==1 or field[y+iy][x+ix]==2:
                    if field[y+iy*2][x+ix*2]==0:
                        moves.append(((x,y),(x+ix+ix,y+iy*2)))#запись хода в конец списка
    if field[y][x]==4:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy<=7 and 0<=x+ix<=7:
                if field[y+iy][x+ix]==1 or field[y+iy][x+ix]==2:
                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                        if field[y+iy*2][x+ix*2]==0:
                            moves.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
    return moves

def get_comp_turns_extra(moves):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if field[y][x]==3:#пешка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            moves.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if field[y+iy][x+ix]==1 or field[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if field[y+iy*2][x+ix*2]==0:
                                    moves.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
            if field[y][x]==4:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            moves.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
    return moves

def get_player_turns(moves):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            moves=get_player_turn(moves,x,y)
    return moves

def get_player_turn(moves,x,y):
    if field[y][x]==1:#пешка
        for ix,iy in (-1,-1),(1,-1):
            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                if field[y+iy][x+ix]==3 or field[y+iy][x+ix]==4:
                    if field[y+iy*2][x+ix*2]==0:
                        moves.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
    if field[y][x]==2:#пешка с короной
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy<=7 and 0<=x+ix<=7:
                if field[y+iy][x+ix]==3 or field[y+iy][x+ix]==4:
                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                        if field[y+iy*2][x+ix*2]==0:
                            moves.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
    return moves

def get_player_turns_extra(moves):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if field[y][x]==1:#пешка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            moves.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if field[y+iy][x+ix]==3 or field[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if field[y+iy*2][x+ix*2]==0:
                                    moves.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
            if field[y][x]==2:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            moves.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
    return moves

load_images()#здесь загружаем изображения пешек
restart()#начинаем новую игру
desk.bind("<Motion>", pos_1)#движение мышки по полю
desk.bind("<Button-1>", pos_2)#нажатие левой кнопки

mainloop()
