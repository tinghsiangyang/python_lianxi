# 该模块用来在终端上显示图形界面
import curses 
# random 模块用来生成随机数
from random import randrange, choice 
# collection 提供了一个字典dict的子类 defaultdict，可以指定 key 的之不存在时，value 的默认值‘
from collections import defaultdict
# import debugpy
# 命令行调试的东西，还没搞懂怎么用
# debugpy.listen(('localhost', 5678))

# 定义游戏六种行为：上、左、下、有、重置游戏、退出
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
# 上述六种行为的有效键入最常见的是：W（上）、A（左）、S（下）、D（右）、R（重置）、Q（退出），在考虑大小写情况
letter_code = [ord(ch) for ch in 'WASDRQwasdrq']
# 将键入（letter_code）作为key，actions作为value使用字典进行关联
# 由于键入（letter_code）区分大小写，所以 actions 需要 * 2，即Up-->W & w 
actions_dict = dict(zip(letter_code, actions * 2))
# print(actions_dict)
# {87: 'Up', 65: 'Left', 83: 'Down', 68: 'Right', 82: 'Restart', 81: 'Exit', 119: 'Up', 97: 'Left', 115: 'Down', 100: 'Right', 114: 'Restart', 113: 'Exit'}

def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict: # 由于char第一次的值为N，肯定不在actions_dict中，用户键入的ASCII码值必定会赋值给char，然后判断用户键入的ASCII码值是否在actions_dict中
        char = keyboard.getch() # 当char不在actions_dict中，获取keyboard的ascii码值，并赋值给char
    return actions_dict[char] # 如果用户键入的ASCII码值在actions_dict中，即返回ASCII码值对应的操作

'''
field = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
'''
def transpose(field):
    return [list(row) for row in zip(*field)]  # *field是解包参数列表
'''
返回结果为：
[[1, 4, 7],
[2, 5, 8],
[3, 6, 9]]
'''
    
def invert(field):
    return [row[::-1] for row in field] # 列表的切片，反序
'''
返回结果为：
[[3, 2, 1],
[6, 5, 4],
[9, 8, 7]]
'''


class GameField(object):
    def __init__(self, height=4, width=4, win=2048): # 初始化函数，创建类实例默认调用该函数，height、width、win会传默认值
        self.height = height            # 高
        self.width = width              # 宽 
        self.win_value = 2048           # 过关分数
        self.score = 0                  # 当前分数
        self.high_score = 0             # 最高分
        self.reset()                    # 棋盘重置
    

    def spawn(self):
        # 从 100 中随机取一个数，如果这个随机数大于89，则new_element取4，否则取2        
        new_element = 4 if randrange(100) > 89 else 2
        # 得到一个位置为空白的随机坐标，坐标按照width和height生成二维数组，然后判断位置是否为空，最后使用choice随机取一个坐标
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):

        if self.score > self.high_score: # 记录游戏的最高分，当调用reset函数时，当前分数大于最高分，则更新最高分
            self.high_score = self.score
        self.score = 0 # 将当前分数重置为0，重新开始游戏

        self.field = [[0 for i in range(self.width)] for j in range(self.height)] # 将棋盘重置，全部位置初始化为0
        '''
        for i in range(self.width)
            for j in range(self.height):
                width_list[j] = 0
            height[i] = width_list
        
        field = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        '''
        self.spawn() # 调用spaw函数，在随机位置赋值为2或者4
        self.spawn() # 同上

    def move(self, direction):

        def move_row_left(row):
            def tighten(row):
                new_row = [i for i in row if i != 0] # 遍历row，将row中不为0的值添加到new_row
                new_row += [0 for i in range(len(row) - len(new_row))] # 按照row的长度，将剩余补0
                '''
                可理解为将row中的非0值前置，并赋值给new_row
                '''
                return new_row


            def merge(row):
                pair = False # 标记是否进行合并
                new_row = []
                for i in range(len(row)): # 遍历row
                    if pair: # 进行合并
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else: # 不进行合并，判断是否可以进行合并
                        if i + 1 < len(row) and row[i] == row[i + 1]: # 如果下一个值的位数在row内，并且当前值和下个值相等，则可以进行合并
                            pair = True
                            new_row.append(0) # 在new_row将当前位数的值设为0
                        else: # 当前值不能进行合并
                            new_row.append(row[i]) # 在new_row将当前位数的值设为当前值
                assert len(new_row) == len(row) # 判断一下原来的row和新的row是不是一样长
                return new_row
            return tighten(merge(tighten(row))) # 先将row中的非0值前置，然后进行合并，然后在将row中的非零值前置

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field] # 匿名函数，将field作为参数传入，遍历field将row传入move_row_left函数，将move_row_left函数的返回值作为列表返回
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        '''
        若field=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]，则将invert(field)=[[3, 2, 1], [6, 5, 4], [9, 8, 7]]作为参数传入moves['Left']匿名函数，
        最后将结果列表传入invert函数，
        '''
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field))) # 思路同上，通过更改棋盘数字位置，使用左移操作代码，达到右移，上移以及下移
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field))) # 思路同上

        if direction in moves: # direction 操作，上下左右
            if self.move_is_possible(direction): # 判断能否进行该操作
                self.field = moves[direction](self.field) # 如果可以进行，则更新棋盘，将操作后的棋盘赋值给现棋盘
                self.spawn() # 再随机生成一个数
                return True # 返回结果True
            else:
                return False # 不能进行操作，返回False

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)
        # i >= self.win_value for i in row 的返回结果时值为Ture和False的可迭代对象

        # for row in self.field:
        #     for i in row:
        #         if i >= self.win_value:
        #             return True
        #         else:
        #             return False
        
        
    def is_gameover(self):
        # 任何一个移动不能进行了，游戏结束，能进行返回移动False，不能进行返回移动True
        return not any(self.move_is_possible(move) for move in actions)

        
    def move_is_possible(self, direction): # 验证是否可以及逆行移动
        
        def row_is_left_moveable(row): # 验证是否可以左移
            def change(i): # 验证一行内是否可以左移或者合并
                if row[i] == 0 and row[i + 1] != 0: # 当左边为0，右边非0，则可以向左移动
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # 当左边的值和右边的值相等，则可以合并
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1)) # 判断每一行是否可以左移和合并
        
        check = {}
        check['Left'] = lambda field: any(row_is_left_moveable(row) for row in field) # 检查是否可以左移
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field) # 如果操作再check内，判断是否可以操作
        else:
            return False

    def draw(self, screen): # 在终端画出棋盘，和提示语

        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Quit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'

        def cast(string):
            screen.addstr(string + '\n') # 将string展示到终端

        
        def draw_hor_separator():
            line = '+' + ('+-------' * self.width + '+')[1:]
            cast(line)

        def draw_row(row):
            # 绘制每一行的竖线，以及每个位置的数字，如果数字大于0，则显示|和数字，如果不大于0，则显示|和空格
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear() # 清空终端屏幕

        cast('SCORE: ' + str(self.score)) # 在终端打印当前分数
        if 0 != self.high_score:
            # 如果最高分不等于0，则在终端打印最高分
            cast('HIGHSCORE: ' + str(self.high_score)) 

        for row in self.field:
            draw_hor_separator() # 遍历棋盘，每行画一条横线
            draw_row(row) # 遍历棋盘，在每行下面画出竖线和数字
        draw_hor_separator() # 最后在添加一行横线

        if self.is_win():
            # 调用is_win函数，返回bool值，如果为True，则打印胜利文案
            cast(win_string)
        else:
            if self.is_gameover(): # 如果游戏结束，则打印结束文案
                cast(gameover_string)
            else:
                cast(help_string1) 
        cast(help_string2)
        

def main(stdscr):

    print(stdscr)


    def init():
        ''' 初始化游戏棋盘 '''
        game_field.reset()
        return 'Game'


    def not_game(state):
        ''' 展示游戏结束界面。
            读取用户输入得到action，判断用户是重启游戏，还是退出游戏
        '''
        game_field.draw(stdscr)

        action = get_user_action(stdscr)

        responses = defaultdict(lambda: state) # state将作为默认的value值
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' # 添加重新开始和退出的键值对
        return responses[action] # 如果不是Restart和Exit，则返回默认的value值

    def game():
        ''' 画出当前棋盘状态
        读取用户输入得到action
        '''

        game_field.draw(stdscr)

        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    curses.use_default_colors()

    game_field = GameField(win=2048)

    state = 'Init'

    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)




                    
                    


    


    

