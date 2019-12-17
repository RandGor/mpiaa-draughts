from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox
import random
import time
import copy



windowMain=Tk()
m = Menu(windowMain) 
windowMain.config(menu=m)


windowMain.title('Английские Шашки')#заголовок окна


comp_moves=()#конечный список ходов компьютера
intelligence=1#количество предсказываемых компьютером ходов
countof_result=0#число сложений summary_result
summary_result=0#разница в очках между игроками
pos1_x=-1#клетка не задана
playersTurn=True#очередь ли игрока ходить

resolution=640#размер поля
screen_width, screen_height = windowMain.winfo_screenwidth(), windowMain.winfo_screenheight()#определение текущего разрешения экрана
if screen_width>810 and screen_height>810:#адаптация поля под разрешение экрана
    resolution=800
    if screen_width>1000 and screen_height>1000:
        resolution=1000

square_size=resolution//8#вывод размера клетки через размер поля
border_width=2#ширина выделения клетки
anim_frames=30#количество кадров в анимации передвижения фигуры на одну клетку
anim_shift=1/anim_frames#величина сдвига фигуры за каждый кадр
desk=Canvas(windowMain, width=resolution,height=resolution,bg='#FFFFFF')#запонение игрового поля белым цветом
desk.pack()

def load_images():#загружаем изображения пешек и изменяем размер под размер поля
    global checkers
    i1 = ImageTk.PhotoImage(Image.open(r"res\\black.png").resize((square_size,square_size), Image.ANTIALIAS))
    i2 = ImageTk.PhotoImage(Image.open(r"res\\black_king.png").resize((square_size,square_size), Image.ANTIALIAS))
    i3 = ImageTk.PhotoImage(Image.open(r"res\\white.png").resize((square_size,square_size), Image.ANTIALIAS))
    i4 = ImageTk.PhotoImage(Image.open(r"res\\white_king.png").resize((square_size,square_size), Image.ANTIALIAS))
    
    
    checkers=[0,i1,i2,i3,i4]

def new_Game():#начинаем новую игру
    global field

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
    x=0
    desk.delete('all')

    while x<8*square_size:#рисуем доску, нечётные строки
        y=1*square_size
        while y<8*square_size:
            desk.create_rectangle(x, y, x+square_size, y+square_size,fill="black")
            y+=2*square_size
        x+=2*square_size
    x=square_size
    while x<8*square_size:#рисуем доску, чётные строки
        y=0
        while y<8*square_size:
            desk.create_rectangle(x, y, x+square_size, y+square_size,fill="black")
            y+=2*square_size
        x+=2*square_size
    red_border=desk.create_rectangle(0,0,0,0,outline="red",width=border_width)
    green_border=desk.create_rectangle(0,0,0,0,outline="green",width=border_width)

    for y in range(8):#рисуем стоячие пешки
        for x in range(8):
            z=field[y][x]
            if z:
                if (x_pos_1,y_pos_1)!=(x,y):#стоячие пешки?
                    desk.create_image(x*square_size,y*square_size, anchor=NW, image=checkers[z])
    #рисуем активную пешку
    z=field[y_pos_1][x_pos_1]
    if z:
        desk.create_image(x_pos_1*square_size,y_pos_1*square_size, anchor=NW, image=checkers[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x_pos_1<x_pos_2 else -1
    ky = 1 if y_pos_1<y_pos_2 else -1
    for i in range(abs(x_pos_1-x_pos_2)):#анимация перемещения пешки
        for ii in range(anim_frames):
            desk.move('ani',anim_shift*square_size*kx,anim_shift*square_size*ky)
            desk.update()#обновление
            time.sleep(0.002)





fm = Menu(m) #создается пункт меню с размещением на основном меню (m)
m.add_cascade(label="Меню",menu=fm)

def destroy():#выход из игры
	exit()

def restart():#запуск игры
        global playersTurn
        new_Game()
        draw(-1,-1,-1,-1)#рисуем игровое поле
        playersTurn=True#ход игрока доступен

def author():#окно с авторами
    tkinter.messagebox.showinfo("Авторы", "Демидович Егор\nМуравьёв Михаил\nЦыганков Алексей")

    
fm.add_command(label="Новая игра",command=restart)
fm.add_command(label="Авторы",command=author)
fm.add_command(label="Выход",command=destroy)




def message(s):#окно с сообщением
    z='Игра завершена'
    if s==1:
        i=tkinter.messagebox.askyesno(title=z, message='Вы победили!\nНачать игру заново?',icon='info')
    if s==2:
        i=tkinter.messagebox.askyesno(title=z, message='Вы проиграли!\nНачать игру заново?',icon='info')
    if s==3:
        i=tkinter.messagebox.askyesno(title=z, message='Вы победили! У противника не осталось ходов.\nНачать игру заново?',icon='info')
    if s==4:
        i=tkinter.messagebox.askyesno(title=z, message='Вы проиграли! У вас не осталось ходов.\nНачать игру заново?',icon='info')
    if i:
        restart()

        

def pos_1(event):#выбор клетки для хода, ведение мышью
    x,y=(event.x)//square_size,(event.y)//square_size#вычисляем координаты клетки
    if 0<=x and x<=7 and 0<=y and y<=7:
        desk.coords(green_border,x*square_size+border_width//2,y*square_size+border_width//2,x*square_size+square_size,y*square_size+square_size)#рамка в выбранной клетке

def pos_2(event):#выбор клетки для хода, клик по клетке
    global pos1_x,pos1_y,pos2_x,pos2_y
    global playersTurn
    x,y=(event.x)//square_size,(event.y)//square_size#вычисляем координаты клетки
    if field[y][x]==1 or field[y][x]==2:#проверяем пешку игрока в выбранной клетке
        desk.coords(red_border,x*square_size,y*square_size,x*square_size+square_size+border_width//2,y*square_size+square_size+border_width//2)#рамка в выбранной клетке
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
            moves=turn(1,comp_moves[th][i][0],comp_moves[th][i][1],comp_moves[th][1+i][0],comp_moves[th][1+i][1])
        comp_moves=[]#очищаем список ходов
        playersTurn=True#ход игрока доступен

    #определяем победителя 
    count_white,count_black=scan()
    if not(count_black):
            message(2)
    elif not(count_white):
            message(1)
    elif playersTurn and not(moves_player()):
            message(4)
    elif not(playersTurn) and not(moves_comp()):
            message(3)

def moves_comp():#составляем список ходов компьютера
    moves=get_comp_turns([])#здесь проверяем обязательные ходы
    if not(moves):
        moves=get_comp_turns_extra([])#здесь проверяем оставшиеся ходы
    return moves

def check_comp(tur,n_moves,moves):#проверка ходов компьютера
    global field
    global comp_moves
    global best_result#лучший результат хода
    global countof_result,summary_result    
    if not(moves):#если список ходов пустой...
        moves=moves_comp()#заполняем

    if moves:
        k_field=copy.deepcopy(field)#копируем поле
        for ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:#проходим все ходы по списку
            t_moves=turn(0,pos1_x,pos1_y,pos2_x,pos2_y)
            if t_moves:#если существует ещё ход
                check_comp(tur,(n_moves+((pos1_x,pos1_y),)),t_moves)
            else:
                check_player(tur,[])
                if tur==1:
                    t_rez=summary_result/countof_result
                    if not(comp_moves):#записыаем если пустой
                        comp_moves=(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                        best_result=t_rez#сохряняем наилучший результат
                    else:
                        if t_rez==best_result:
                            comp_moves=comp_moves+(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                        if t_rez>best_result:
                            comp_moves=()
                            comp_moves=(n_moves+((pos1_x,pos1_y),(pos2_x,pos2_y)),)
                            best_result=t_rez#сохряняем наилучший результат
                    summary_result=0
                    countof_result=0

            field=copy.deepcopy(k_field)#возвращаем поле
    else:
        count_white,count_black=scan()#подсчёт результата хода
        summary_result+=(count_white-count_black)
        countof_result+=1

def moves_player():#составляем список ходов игрока
    moves=get_player_turns([])#здесь проверяем обязательные ходы
    if not(moves):
        moves=get_player_turns_extra([])#здесь проверяем оставшиеся ходы
    return moves
    
def check_player(tur,moves):#проверка ходов игрока
    global field,countof_result,summary_result
    global intelligence
    if not(moves):
        moves=moves_player()

    if moves:#проверяем наличие доступных ходов
        k_field=copy.deepcopy(field)#копируем поле
        for ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:                    
            t_moves=turn(0,pos1_x,pos1_y,pos2_x,pos2_y)
            if t_moves:#если существует ещё ход
                check_player(tur,t_moves)
            else:
                if tur<intelligence:
                    check_comp(tur+1,(),[])
                else:
                    count_white,count_black=scan()#подсчёт результата хода
                    summary_result+=(count_white-count_black)
                    countof_result+=1

            field=copy.deepcopy(k_field)#возвращаем поле
    else:#доступных ходов нет
        count_white,count_black=scan()#подсчёт результата хода
        summary_result+=(count_white-count_black)
        countof_result+=1

def scan():#подсчёт пешек на поле
    global field
    count_black=0#очки чёрных
    count_white=0#очки белых
    for i in range(8):
        for ii in field[i]:
            if ii==1:count_black+=1
            if ii==2:count_black+=3
            if ii==3:count_white+=1
            if ii==4:count_white+=3
    return count_white,count_black

def player_turn():#ход игрока
    global pos1_x,pos1_y,pos2_x,pos2_y
    global playersTurn
    playersTurn=False#считаем ход игрока выполненным
    moves=moves_player()
    if moves:
        if ((pos1_x,pos1_y),(pos2_x,pos2_y)) in moves:#проверяем ход на соответствие правилам игры
            t_moves=turn(1,pos1_x,pos1_y,pos2_x,pos2_y)#если всё хорошо, делаем ход            
            if t_moves:#если есть ещё ход той же пешкой
                playersTurn=True#считаем ход игрока невыполненным
        else:
            playersTurn=True#считаем ход игрока невыполненным
    desk.update()#!!!обновление

def turn(f,pos1_x,pos1_y,pos2_x,pos2_y):#делаем(f=1) или просматриваем(f=0) ход по заданным координатам
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

def get_comp_turn(moves,x,y):#проверка очередного хода компьютера
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

def get_player_turn(moves,x,y):#проверка очередного хода игрока
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
