import constant
import tkinter as tk
import time

class Player:
    __no = 0  # 플레이어의 총 수를 나타낸다.

    def __init__(self, player_name=None, canvas=None, color=None):
        Player.__no += 1
        self.__id = Player.__no  # 플레이어 id
        self.__money = constant.START_MONEY  # 현재 소지하고 있는 금액
        self.__stop_times = 0  # 멈춰야 할 턴 수
        self.__marker = Marker(self.__id, canvas, color)  # 플레이어 말

        # 플레이어 이름 설정. 따로 정의되지 않는 경우 Player1, Player2, ...와 같이 자동으로 선언이 된다.
        if player_name is None:
            self.__player_name = "Player%d" % self.__id
        else:
            self.__player_name = player_name
        self.__check_desert = False  # 무인도에 처음으로 들어갔는지 체크

    def get_color(self):
        return self.__marker.get_color()

    # 플레이어의 속성을 초기화한다. (게임을 재시작할 경우에 실행해야 한다.)
    def reset(self):
        self.__money = constant.START_MONEY  # 소지 금액 초기화
        self.__stop_times = 0  # 멈춰야 할 턴의 수를 초기화
        self.__marker.reset_position()  # 말의 위치 초기화

    # 풀레이어 id값 반환
    def get_id(self):
        return self.__id

    # 플레이어가 현재 소지하고 있는 돈을 반환
    def get_current_money(self):
        return self.__money

    # 플레이어가 파산했는지 여부를 반환
    def is_bankrupt(self):
        return self.__money < 0

    # 플레이어의 현재 위치를 반환
    def get_current_position(self):
        return self.__marker.get_position()

    # 플레이어가 던진 주사위의 눈의 수가 각각 dice1, dice2 일 때 dice1+dice2 만큼 이동하게 하고 이동한 뒤의 위치를 반환한다.
    # 여기서는 구매와 관련된 부분을 처리하지 않는다.
    def move(self, dice1: int, dice2: int):
        # 만약 같은 눈이 나오면 탈출할 수 있다.
        if dice1 == dice2:
            self.__stop_times = 0
            self.__check_desert = False
        # 쉬어야 하는 턴인지 체크한다.
        if self.is_stop():
            self.__stop_times -= 1
        else:
            # 멈추지 않아도 된다면 말을 이동시키고, 한 바퀴 이상 돈 경우 constant.SALARY 만큼 추가를 해준다.
            self.__money += self.__marker.move(dice1 + dice2) * constant.SALARY
            self.__check_desert = False
        return self.get_current_position()

    # 플레이어가 멈춰야할 턴의 수를 넣어준다. (플레이어가 무인도에 도착했을 때 사용할 메서드)
    def set_stop(self):
        if not self.__check_desert:
            self.__stop_times = constant.STOP_TURN
            self.__check_desert = True

    # 플레이어가 멈춰있는 상태인지 여부를 반환
    def is_stop(self):
        return self.__stop_times > 0

    def check_desert(self):
        return self.__check_desert

    # 플레이어가 other_player 에게 money 만큼의 돈을 지불한다. 만약 other_player 가 정의되지 않는 경우에는 현재 플레이어의 돈만 감소한다.
    # 지불이 성공한 경우에는 True 를 반환하고, 지불이 실패한 경우에는 False 를 반환한다.
    def pay_money(self, money, other_player=None):
        if self.__money < money:
            print("%s is bankrupt" % self.__player_name)
        self.__money -= money
        if isinstance(other_player, Player):
            other_player.__money += money
        return True

    def get_player_name(self):
        return self.__player_name


class Marker:
    def __init__(self, player_id, canvas:tk.Canvas, color=None):
        self.__id = player_id  # 말을 소유하고 있는 플레이어의 id
        self.__position = 0  # 현재 말의 위치
        self.__text = str(player_id)
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

    # 현재 말의 위치를 반환한다.
    def get_position(self):
        return self.__position

    # 말의 위치를 초기화한다.
    def reset_position(self):
        self.__canvas.move(self.__item,
                           -constant.REGION_OF_X_POS[self.__position]*self.__diff_x,
                           -constant.REGION_OF_Y_POS[self.__position]*self.__diff_y)
        self.__position = 0

    def get_move(self, pos):
        cur_pos = pos % constant.TOTAL_REGIONS
        next_pos = (pos + 1) % constant.TOTAL_REGIONS
        return constant.REGION_OF_X_POS[next_pos] - constant.REGION_OF_X_POS[cur_pos],\
                    constant.REGION_OF_Y_POS[next_pos] - constant.REGION_OF_Y_POS[cur_pos]

    def get_color(self):
        return self.__color

    # 말을 distance 만큼 이동시킨다. 그리고 그 때 몇 바퀴를 돌았는지를 리턴한다.
    def move(self, distance):
        prev_pos = self.__position
        self.__position += distance
        while prev_pos < self.__position:
            mov_x, mov_y = self.get_move(prev_pos)
            self.__canvas.move(self.__item, mov_x*self.__diff_x, mov_y*self.__diff_y)
            self.__canvas.update()
            time.sleep(0.2)
            prev_pos += 1
        rotate_times = self.__position // constant.TOTAL_REGIONS
        self.__position = self.__position % constant.TOTAL_REGIONS
        return rotate_times


def main():
    player1 = Player()
    player2 = Player()

    print(player1.get_current_money())
    print(player2.get_current_money())

    player1.pay_money(2000, player2)

    print(player1.get_current_money())
    print(player2.get_current_money())


if __name__ == "__main__":
    main()

