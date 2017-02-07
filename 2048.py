#!/usr/bi/env python3
# -*- coding:utf-8 -*-

import curses
from random import  randrange,choice
from collections import  defaultdict

#设置‘上，下，左，右，重置，退出’6种状态
actions  = ['Up','Left','Down','Right','Restart','Exit']

#有效的输入键，考虑大小写的
letter_codes =  [ord(ch) for  ch in 'WASDRQwasdrq']

#输入与行为相关联
actions_dict = dict(zip(letter_codes, actions * 2))

#用户输入处理，用于获得有效的用户输入
def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return  actions_dict[char]

#矩阵转置
def transpose(field):
    return[list(row) for row in zip(*field)]
#矩阵逆转
def  invert(field):
    return [row[::-1] for row in field]

#创建棋盘
class GameField(object):
    def __init__(self,height=4, width=4, win=2048):
        self.hight = height       #高
        self.width = width        #宽
        self.win   = 2048         #过关分数
        self.score = 0            #当前分数
        self.highscore = 0        #最高分
        self.reset()              #棋盘重置

    # 重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        self.spwan()
        self.spwan()

        # 棋盘走一步
        def move(self, direction):
            def move_row_left(row):
                # 一行向左合并
                def tighten(row):  # 把零散的非零单元挤到一块
                    new_row = [i for i in row if i != 0]
                    new_row += [0 for i in range(len(row) - len(new_row))]
                    return new_row

            def merge(row):  # 对邻近元素进行合并
                pair = False
                new_now = []
                for i in range(len(row)):
                    if pair:
                        new_now.append(2 * row[i])
                        self.secore += 2 * row[i]
                        pair = False
                    else:
                        new_now.append(row[i])
                assert len(new_now) == len(row)
                return new_now
                # 先挤到一块在合并为一块
                return tighten(merge(tighten(row)))

            # 判断输赢
            def is_win(self):
                return any(any(i >= self.win_value for i in row) for row in self.field)

            def is_gameover(self):
                return not any(self.move_is_possible(move) for move in actions)


#棋盘操作,随机生成2或4
def spaen(self):
    new_element = 4 if randrange(100) > 89 else 2
    (i,j) = choice([i,j]  for i in range(self.width)
                           for j in range(self.height)
                           if self.field[i][j] == 0
                   )
    self.field[i][j] = new_element
#绘制游戏界面
def draw(self, screen):
    help_string1 = '(W)Up (S)Wown (A)Left (D)Right'
    help_string2 = '(R)Restart (Q)Exit'
    gameover_string = '         GAMEOVER'
    win_string      = '         YOUWIN!'
    def cast(string):
        screen.addstr(string + '\n')

    #绘制水平分割线
    def draw_hor_separator():
        line = '+' + ('+-----------' * self.width + '+')[1:]
        separator = defaultdict(lambda: line)
        if not hasattr(draw_hor_separator, "counter"):
            draw_hor_separator.counter = 0
        cast(separator[draw_hor_separator.counter])
        draw_hor_separator.counter += 1

    def draw_row(row):
        cast(''.join('|{:^5}'.format(num) if num >0 else '|         'for num in row)+'|')
    screen.clear()
    cast('SCORE: '+ str(self.score))
    if 0 != self.highscore:
        cast('HGHSCORE: '+str(self.highscore))

    for row in self.field:
        draw_hor_separator()
        draw_row(row)

    draw_hor_separator()

    if self.is_win():
        cast(win_string)
    else:
        if self.is_gameover():
            cast(gameover_string)
        else:
            cast(help_string1)
    cast(help_string2)

#判断能否移动
def  move_is_possible(self, direction):
    def row_is_left_movable(row):
        def change(i):
            if row[i] == 0 and row[i + 1] != 0: # 可以移动
                return True
            if row[i] != 0 and row[i + 1] == row[i]: #可以合并
                return True
            return False
        return any(change(i) for i in  range(len(row) - 1))
    check = {}
    check['Left'] = lambda field: \
        any(row_is_left_movable(row) for row in field)
    check['Right'] = lambda field:\
        check['Left'](invert(field))
    check['Up']    = lambda field: \
        check['Left'](transpose(field))
    check['Down']  = lambda field: \
        check['Right'](transpose(field))

    if direction in check:
        return check[direction](self.field)
    else:
        return False



#主逻辑
def main(stdscr):
    def init():
        #重置游戏棋盘
        return 'Game'

    def not_game(state):
        #画出GameOver 或者 Win的画面
        game_field.draw(stdscr)
        #读取用户的action，判断重置游戏还是结束游戏
        action = get_user_action()
        responses = defaultdict(lambda: state)  #默认当前状态，没有行为一直停留在当前页面
        responses['Restart'],responses['Exit'] = 'Init', 'Exit'  #对应不同行为转换不同状态
        return responses[action]

    def game():
        #画出当前的棋盘状态
        game_field.draw(stdscr)
        #读取用户输入的action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
                return 'Exit'
        if game_field.move(action):  # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game }

    curses.use_default_colors()
    game_field = GameField(win=32)


    state = 'Init'
    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)


