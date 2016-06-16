import constant
import tkinter as tk
import time

class Player:
    __no = 0  # total player number

    def __init__(self, player_name=None, canvas=None, color=None):
        Player.__no += 1
        self.__id = Player.__no  # player id
        self.__money = constant.START_MONEY  # player money
        self.__stop_times = 0  # turns to stop(in dessert)
        self.__marker = Marker(self.__id, canvas, color)  # player marker

        # player name setting. if player name is not defined, it is automatically set with player%d
        if player_name is None:
            self.__player_name = "Player%d" % self.__id
        else:
            self.__player_name = player_name
        self.__check_desert = False  # check if entering desert first time

    # get player's color
    def get_color(self):
        return self.__marker.get_color()

    # initialize player information. (when game resets)
    def reset(self):
        self.__money = constant.START_MONEY  # 소지 금액 초기화
        self.__stop_times = 0  # 멈춰야 할 턴의 수를 초기화
        self.__marker.reset_position()  # 말의 위치 초기화

    # return player id(0,1,..)
    def get_id(self):
        return self.__id

    # return player current money
    def get_current_money(self):
        return self.__money

    # return whether player is bankrupt
    def is_bankrupt(self):
        return self.__money < 0

    # return player current position
    def get_current_position(self):
        return self.__marker.get_position()

    # dice1, dice2 values make player move (dice1+dice2) region, and return new position
    # purchasing is not dealt with here
    def move(self, dice1: int, dice2: int):
        # if dice1 == dice2, player can escape desert
        if dice1 == dice2:
            self.__stop_times = 0
            self.__check_desert = False
        # check stop turn
        if self.is_stop():
            self.__stop_times -= 1
        else:
            # if not stop turn, move mark. when pass starting point again, player gets constant.SALARY
            self.__money += self.__marker.move(dice1 + dice2) * constant.SALARY
            self.__check_desert = False
        return self.get_current_position()

    # set player stop turn(when in desert)
    def set_stop(self):
        if not self.__check_desert:
            self.__stop_times = constant.STOP_TURN
            self.__check_desert = True

    # return if player is in stop turn
    def is_stop(self):
        return self.__stop_times > 0

    # check desert. if desert, return true
    def check_desert(self):
        return self.__check_desert

    # player give money to other player when buy region. if none has that region, only consumer player money decreases
    def pay_money(self, money, other_player=None):
        self.__money -= money
        if isinstance(other_player, Player):
            other_player.__money += money
        return True

    # return player name
    def get_player_name(self):
        return self.__player_name


# player marker class. marker is object for showing actual move
class Marker:
    def __init__(self, player_id, canvas:tk.Canvas, color=None):
        self.__id = player_id  # player id of marker
        self.__position = 0  # position of marker
        self.__canvas = canvas
        self.__start_x, self.__start_y = 20+(player_id-1)*30, 50
        self.__color = color
        if canvas is not None:
            self.__item = canvas.create_oval(0, 0, 20, 20)
            if color is not None:
                self.__canvas.itemconfig(self.__item, fill=color)
                self.__canvas.move(self.__item, self.__start_x, self.__start_y)
        self.__diff_x = 90
        self.__diff_y = 80

    # return maker's current position
    def get_position(self):
        return self.__position

    # reset marker's position
    def reset_position(self):
        self.__canvas.move(self.__item,
                           -constant.REGION_OF_X_POS[self.__position]*self.__diff_x,
                           -constant.REGION_OF_Y_POS[self.__position]*self.__diff_y)
        self.__position = 0

    # return the difference between `pos` & `pos`+1
    def get_move(self, pos):
        cur_pos = pos % constant.TOTAL_REGIONS
        next_pos = (pos + 1) % constant.TOTAL_REGIONS
        return constant.REGION_OF_X_POS[next_pos] - constant.REGION_OF_X_POS[cur_pos],\
                    constant.REGION_OF_Y_POS[next_pos] - constant.REGION_OF_Y_POS[cur_pos]

    # return the marker color
    def get_color(self):
        return self.__color

    # make marker move distance. and return number of passing starting point
    def move(self, distance):
        prev_pos = self.__position
        self.__position += distance
        while prev_pos < self.__position:
            mov_x, mov_y = self.get_move(prev_pos)
            self.__canvas.move(self.__item, mov_x*self.__diff_x, mov_y*self.__diff_y)
            self.__canvas.update()
            time.sleep(0.2) # For moving marker not fast.
            prev_pos += 1
        rotate_times = self.__position // constant.TOTAL_REGIONS
        self.__position = self.__position % constant.TOTAL_REGIONS
        return rotate_times

