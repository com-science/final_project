import player
import constant
import region
import dice

import random
from tkinter import messagebox
import tkinter as tk

colorset = ["red", "blue"]


format_time = lambda seconds : "Elapsed time -> %02d:%02d"%(seconds//60, seconds % 60)

format_currency = lambda money: "${:,}".format(money)

class Game:
    def __init__(self, region_info=None, players_name=None, main_view=None):
        """
        if player_list is None:
            # player_list 가 없는 경우에는 자동으로 constant.PLAYER_NO 에 해당하는 만큼 player 를 생성해서 넣는다.
            self.__player_list = []
            for i in range(constant.PLAYER_NO):
                self.__player_list.append(player.Player())
        else:
            # player_list 가 있는 경우에는 이것을 사용하고 알맞은 플레이어 수로 업데이트한다.
            self.__player_list = player_list
            constant.PLAYER_NO = len(player_list)
        """
        #self.__region_list = region_info  # 맵에 있는 모든 땅의 정보를 의미한다.
        self.__main_view = main_view
        self.__canvas = main_view.map_canvas
        assert len(region_info) == constant.TOTAL_REGIONS
        self.__region_list = [region.Region(region_info[i][0], region_info[i][1], root_view=self.__canvas, _x=constant.REGION_OF_X_POS[i], _y=constant.REGION_OF_Y_POS[i]) for i in range(constant.TOTAL_REGIONS)]

        assert len(players_name) == constant.PLAYER_NO
        self.__player_list = [player.Player(players_name[i],self.__canvas, colorset[i]) for i in range(constant.PLAYER_NO)]

        self.__region_list[14].set_desert()
        self.__region_list[0].set_cannot_buy()

        self.__current_turn = 1  # 현재 턴 수
        self.__current_player_no = 0

        self.__dices_list = [dice.Dice(), dice.Dice()]
        self.__canvas.create_image(275, 350, anchor=tk.NW, image=self.__dices_list[0])
        self.__canvas.create_image(375, 350, anchor=tk.NW, image=self.__dices_list[1])

        self.dice_button = tk.Button(main_view.footer, text='roll dices', command=self.play)
        self.dice_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(main_view.footer, text='reset', command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=20)

        self.__elapsed_time = 0
        self.__timer_on = False
        self.__timer_label = tk.Label(self.__main_view.header, text=format_time(0))
        self.__timer_label.pack()
        self.__turn_label = tk.Label(self.__main_view.header, text="Turn #%2d" % self.__current_turn)
        self.__turn_label.pack()

        self.__players_name_label = [tk.Label(self.__main_view.frame_info,
                                              text=self.__player_list[i].get_player_name(),
                                              fg=self.__player_list[i].get_color(),
                                              font=("Helvetica", 16),
                                              width=10)
                                     for i in range(constant.PLAYER_NO)]
        self.__players_money_label = [tk.Label(self.__main_view.frame_info,
                                              text=format_currency(self.__player_list[i].get_current_money()),
                                               font=("Helvetica", 16))
                                     for i in range(constant.PLAYER_NO)]
        self.__display_current_player = self.__main_view.map_canvas.create_text(
            350, 300,
            text="%s turn" % self.__player_list[0].get_player_name(),
            font=("Helvetica", 16),
            fill=self.__player_list[0].get_color()
        )

        for i in range(constant.PLAYER_NO):
            self.__players_name_label[i].grid(row=2*i, column=1)
            self.__players_money_label[i].grid(row=2*i+1, column=1)

    def update_timer(self):
        if not self.__timer_on:
            return
        self.__elapsed_time += 1
        self.__timer_label.config(text=format_time(self.__elapsed_time))
        self.__main_view.after(1000, self.update_timer)

    def get_player_list(self):
        return self.__player_list

    def get_region_list(self):
        return self.__region_list

    # 게임을 재시작한다.
    def reset(self):
        # 플레이어 정보 초기화
        for _player in self.__player_list:
            assert isinstance(_player, player.Player)
            _player.reset()

        # 땅의 정보 초기화
        for _region in self.__region_list:
            assert isinstance(_region, region.Region)
            _region.reset()
        self.__elapsed_time = 0
        self.__current_turn = 1
        self.__current_player_no = 0
        self.__timer_on = False

        self.dice_button.config(state=tk.NORMAL)
        self.__timer_label.config(text=format_time(self.__elapsed_time))
        self.__turn_label.config(text="Turn #%2d" % self.__current_turn)
        for i in range(constant.PLAYER_NO):
            self.__players_money_label[i].config(text=format_currency(self.__player_list[i].get_current_money()))

        self.__main_view.map_canvas.itemconfig(self.__display_current_player, text="%s turn" % self.__player_list[0].get_player_name())
        self.__main_view.map_canvas.itemconfig(self.__display_current_player, fill=self.__player_list[0].get_color())

    # 주사위 2개를 던져서 나온 눈의 수를 tuple 형태로 리턴한다. 여기에서 주사위 이미지를 업데이트 하도록 한다.
    def roll_dice(self):
        (dice1, dice2) = (random.randint(1, 6), random.randint(1, 6))
        # TODO: 주사위 이미지를 화면에 출력하기
        self.__dices_list[0].update_dice_num(dice1)
        self.__dices_list[1].update_dice_num(dice2)
        return dice1, dice2

    # 한 플레이어가 한 턴 동안 하는 일. 주사위를 던져서 이동하고, 지역을 구매하는 것까지 포함한다.
    def player_move(self, _player: player.Player):
        dice1, dice2 = self.roll_dice()  # 주사위를 던진다.
        print(dice1, dice2)
        current_region = self.__region_list[_player.move(dice1, dice2)]  # 현재 _player 가 있는 지역
        assert isinstance(current_region, region.Region)  # 적절한 값인지 체크
        _type = current_region.get_buy_type(_player.get_id())  # 구매 타입을 정한다. constant.py 에 있는 내용 참조.
        if current_region.is_desert() and not _player.check_desert():
            _player.set_stop()
        # 통행료 지급하는 부분
        if _player.get_id() != current_region.get_owner_id() and current_region.get_owner_id() is not None:
            _toll = current_region.get_toll()
            _player.pay_money(_toll, current_region.get_owner())
            print("%s gave $%d money to %s"
                  % (_player.get_player_name(), _toll, current_region.get_owner().get_player_name()))
        # 지역 구매 여부 묻기
        current_region_price = current_region.get_sales_price(_player.get_id())
        if _player.get_current_money() >= current_region_price and current_region.can_buy():
            want_to_buy = messagebox.askyesno("Buy", constant.ASK_BUY_MESSAGE[_type] % current_region_price)
            if want_to_buy:
                    current_region.buy(_player)
        if dice1 != dice2:
            self.__current_player_no = (self.__current_player_no + 1) % constant.PLAYER_NO
        return dice1, dice2

    # 모든 플레이어가 한 턴 동안 하는 일.
    # 게임이 끝나지 않는 경우에는 None 을 리턴하고, 누군가가 파산해서 게임이 끝나는 경우에는 파산한 플레이어의 id 를 리턴한다.
    def one_turn(self):
        _player = self.__player_list[self.__current_player_no]
        self.player_move(_player)

        for i in range(constant.PLAYER_NO):
            self.__players_money_label[i].config(text=format_currency(self.__player_list[i].get_current_money()))

        if _player.is_bankrupt():
            return _player

        if self.__current_player_no == 0:
            self.__current_turn += 1  # 한 턴을 증가시킨다.
            self.__turn_label.config(text="Turn #%2d" % self.__current_turn)
        _player = self.__player_list[(self.__current_player_no) % constant.PLAYER_NO]
        self.__main_view.map_canvas.itemconfig(self.__display_current_player, text="%s turn" % _player.get_player_name())
        self.__main_view.map_canvas.itemconfig(self.__display_current_player, fill=_player.get_color())

        return None

    # 하나의 게임을 시행한다.
    def play(self):
        if not self.__timer_on:
            self.__timer_on = True
            self.update_timer()
        if self.__current_turn == constant.MAXIMUM_TURN:
            self.show_winner()
            return
        self.dice_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        result = self.one_turn()
        self.dice_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        # 게임이 종료되었을 경우 이전 게임에 대한 내용을 모두 초기화한다.
        if result is not None:
            assert isinstance(result, player.Player)
            print("%s is bankrupt!" % result.get_player_name())
            self.show_winner()
            return

        #self.reset()

    def show_winner(self):
        self.__timer_on = False
        scores = self.get_score()
        print(scores)
        if scores[0] == scores[1]:
            message = "Draw"
        elif scores[0] > scores[1]:
            message = "%s Win!" % self.__player_list[0].get_player_name()
        else:
            message = "%s Win!" % self.__player_list[1].get_player_name()
        self.dice_button.config(state=tk.DISABLED)
        messagebox.showinfo("Winner", message)

    def get_score(self):
        scores = [self.__player_list[i].get_current_money() for i in range(constant.PLAYER_NO)]
        for _region in self.__region_list:
            _id = _region.get_owner_id()
            if _id is not None:
                scores[_id-1] += _region.get_current_price()
        return scores

class MainView(tk.Tk):
    def __init__(self, title="Game 1.0"):
        super().__init__()
        self.title(title)
        self.resizable(0, 0)
        #self.wm_attributes("-topmost", 1)
        #self.canvas = tk.Canvas(self, width=950, height=700)
        #self.canvas.pack()
        self.header = tk.Frame(self)
        self.header.grid(row=0, column=0)
        self.map_canvas = tk.Canvas(self, width=950, heigh=700)
        self.map_canvas.grid(row=1, column=0)
        self.footer = tk.Frame(self)
        self.footer.grid(row=2, column=0)
        self.frame_info = tk.Frame(self)
        self.frame_info.grid(row=1, column=1)
        self.update()


def main():
    region_name_list = ['정문', '법대', '규장각', '사회대', '문화관', '잔디밭', '학생회관', '자연대',
                    '농생대', '농식', '해동', '아랫공대', '공깡', '중도', '관정', '인문대', '인문신양',
                    '자하연', '음미대', '경영대', '체육관', 'MOA', '대운동장', '기숙사', '감골식당',
                    '사범대', '롯데리아', '느티나무']

    region_price_list = [0, 500, 1600, 2100, 1500, 800, 1800, 1000, 2000, 1400, 1200, 2500, 1200, 1500, 800, 1500, 2200,
                     1300, 1800, 800, 2000, 1200, 900, 1100, 2100, 1300, 1600, 2700]
    # 지역이름과 가격으로 리스트 작성
    main_view = MainView()

    #region__list = [region.Region(region_name_list[i], region_price_list[i]) for i in range(constant.TOTAL_REGIONS)]
    #region__list = [region.Region(region_name_list[i], region_price_list[i], root_view=canvas, _x=constant.REGION_OF_X_POS[i], _y=constant.REGION_OF_Y_POS[i]) for i in range(constant.TOTAL_REGIONS)]
    regions_info = [(region_name_list[i], region_price_list[i]) for i in range(constant.TOTAL_REGIONS)]
    players_name = [None for i in range(2)]

    New_game = Game(regions_info, players_name, main_view)

    main_view.mainloop()


if __name__ == "__main__":
    main()
