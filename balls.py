from tkinter import *
from random import randrange as rnd, choice
import time


def main():
    global root, canvas
    root = Tk()
    root.geometry('800x600')
    canvas = Canvas(root,bg='white')
    canvas.pack(fill=BOTH,expand=1)


class Ball:
    def __init__(self):
        self.x, self.y, self.r = rnd(100, 700), rnd(100, 500), rnd(30, 50)
        self.dx, self.dy = rnd(2, 7), rnd(2, 5)
        self.live = 100
        self.color = choice(['red', 'orange', 'yellow', 'green', 'blue'])
        if rnd(1,10) > 7: # с небольшой вероятностью формируем пульсар
            self.value = 1000
            self.dr = 2
        else:
            self.value = 200
            self.dr = 0
        # случайно изменяем знаки dx и dy
        if rnd(1,10) >= 5:
            self.dx = -self.dx
        if rnd(1, 10) >=5:
            self.dy = -self.dy
        self.create_ball()


    def create_ball(self):
        ''' Создание мишени
        '''
        x, y, r = self.x, self.y, self.r
        self.id = canvas.create_oval(x-r, y-r, x+r, y+r,
                           fill = self.color, width=0)


    def move_ball(self):
        ''' Перемещение мишени с отражением от стенок
            При каждом шаге жизнь мишени (live) уменьшается на 1
        '''
        self.x += self.dx
        self.y += self.dy
        self.r += self.dr
        x, y, r = self.x, self.y, self.r
        if r < 30 or r > 50: # границы изменения пульсара
            self.dr = -self.dr
        canvas.coords(self.id, x-r, y-r, x+r, y+r)
        if x + r >= 800 or x - r <= 0:
            self.dx = -self.dx
        if y + r >= 600 or y - r <= 0:
            self.dy = -self.dy
        self.live -= 1
        return self.live


    def check_shot(self, x, y):
        ''' Проверка попадания щелчка в мишень
            При попадании возвращает стоимость мишени
        '''
        distance = (x - self.x) ** 2 + (y - self.y) ** 2
        if  distance <= self.r ** 2:
            return self.value


    def remove_ball(self):
        ''' Уничтожение мишени
        '''
        canvas.delete(self.id)


def start_game():
    global balls, total_balls, total_score
    canvas.bind('<Button-1>', click)
    total_balls = 10
    total_score = 1000
    balls = []
    balls.append(Ball())
    balls.append(Ball())
    total_balls -= 2
    while balls or total_balls:
        for ball in balls:
            live = ball.move_ball()
            if live <=0: # Мишень умерла. Штрафуем на 300 очков и меняем мишень
                replace_ball(ball, -300)
            canvas.update()
        time.sleep(0.03)


def replace_ball(ball, price):
    ''' Убиваем мишень, начисляя очки в случае попадания
    или вычитая штраф, если мишень умерла по тайм-ауту.
    Если ещё не все мишени вышли из игры, создаём новую.
    '''
    global balls, total_balls, total_score
    ball.remove_ball()
    balls.remove(ball)
    total_score += price
    if total_balls:
        balls.append(Ball())
        total_balls -= 1


def click(event):
    global balls, total_balls, total_score
    x, y = event.x, event.y
    total_score -= 100
    for ball in balls:
        shot = ball.check_shot(x, y)
        if shot:
            replace_ball(ball, shot)
    print('Total score = ', total_score)


time
main()
start_game()
root.mainloop()
