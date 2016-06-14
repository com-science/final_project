import player
import constant
import region
import dice

import random
from tkinter import messagebox
import tkinter as tk


class Game:
    def __init__(self, region_list=None, player_list=None, canvas:tk.Canvas=None):
        if player_list is None:
            # player_list 가 없는 경우에는 자동으로 constant.PLAYER_NO 에 해당하는 만큼 player 를 생성해서 넣는다.
            self.__player_list = []
            for i in range(constant.PLAYER_NO):
                self.__player_list.append(player.Player())
        else:
            # player_list 가 있는 경우에는 이것을 사용하고 알맞은 플레이어 수로 업데이트한다.
            self.__player_list = player_list
            constant.PLAYER_NO = len(player_list)

        self.__region_list = region_list  # 맵에 있는 모든 땅의 정보를 의미한다.
        assert len(region_list) == constant.TOTAL_REGIONS
        self.__current_turn = 0  # 현재 턴 수
        self.__canvas = canvas
        self.__dices_list = [dice.Dice(), dice.Dice()]
        canvas.create_image(275, 350, anchor=tk.NW, image=self.__dices_list[0])
        canvas.create_image(375, 350, anchor=tk.NW, image=self.__dices_list[1])


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
        return dice1, dice2

    # For testing player move method. (no random)
    """
    def test_player_move(self, _player: player.Player, dice1: int, dice2: int):
        current_region = self.__region_list[_player.move(dice1, dice2)]  # 현재 _player 가 있는 지역
        assert isinstance(current_region, region.Region)  # 적절한 값인지 체크
        _type = current_region.get_buy_type(_player.get_id())  # 구매 타입을 정한다. constant.py 에 있는 내용 참조.
        if current_region.is_desert() and not _player.check_desert():
            _player.set_stop()
        # 통행료 지급하는 부분
        if _player.get_id() != current_region.get_owner_id() and current_region.get_owner_id() is not None:
            _toll = current_region.get_toll()
            _player.pay_money(_toll, current_region.get_owner())
            print("%s gave $%d money to %s" % (_player.get_player_name(), _toll, current_region.get_owner().get_player_name()))

        # 지역 구매 여부 묻기
        current_region_price = current_region.get_sales_price(_player.get_id())
        if _player.get_current_money() >= current_region_price:
            ask = input(constant.ASK_BUY_MESSAGE[_type] % current_region_price)
            if ask is 'Y':
                    current_region.buy(_player)
            elif ask is 'N':
                pass
    """

    # 모든 플레이어가 한 턴 동안 하는 일.
    # 게임이 끝나지 않는 경우에는 None 을 리턴하고, 누군가가 파산해서 게임이 끝나는 경우에는 파산한 플레이어의 id 를 리턴한다.
    def one_turn(self):
        self.__current_turn += 1  # 한 턴을 증가시킨다.
        for _player in self.__player_list:  # 모든 플레이어에 대해서 각각 한 턴씩 진행하고, 파산 여부를 체크한다.
            assert isinstance(_player, player.Player)  # 적절한 타입인지 체크
            #self.player_move(_player)  # _player 가 한 턴 동안 하는 일을 시행한다.
            if _player.is_bankrupt():  # 파산했는지 여부를 체크한다.
                return _player.get_id()
        return None

    # 하나의 게임을 시행한다.
    def play(self):
        while self.__current_turn < constant.MAXIMUM_TURN:
            # TODO: 아래 메서드의 리턴 값에 따라서 게임을 계속 진행할지 혹은 끝낼 것인지를 결정하기
            self.one_turn()

        # 게임이 종료되었을 경우 이전 게임에 대한 내용을 모두 초기화한다.
        self.reset()


def main():
    region_name_list = ['정문', '법대', '규장각', '사회대', '문화관', '잔디밭', '학생회관', '자연대',
                    '농생대', '농식', '해동','아랫공대', '공대간이식당', '중도','관정', '인문대', '인문대신양',
                    '자하연', '음미대', '경영대,', '체육관', 'MOA', '대운동장', '두레문예관', '감골식당',
                    '사범대', '롯데리아', '느티나무', '기숙사', '버들골', '노천강당', '파스쿠치', '씨유','301동'
                    ,'녹두,', '서울대입구']
    region_price_list = [0, 500, 500, 500, 800, 800, 800, 1000, 1000, 1000, 1200, 1200, 1200, 1500, 1500, 1500, 1800,
                     1800, 1800, 2000, 2000, 2000, 2100, 2100, 2100, 2400, 2400, 2400, 2600, 2600, 2600, 2800, 2800, 2800,
                     3000, 3000]
    # 지역이름과 가격으로 리스트 작성
    region__list = [region.Region(region_name_list[i], region_price_list[i]) for i in range(36)]
    region__list[18].set_desert()
    player__list = [player.Player() for i in range(2)]
    New_game = Game(region__list, player__list)
    """
    New_game.test_player_move(player__list[0], 9, 9)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 7, 3)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 5, 2)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 5, 2)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 5, 2)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 6, 9)
    print(player__list[0].get_current_position())
    New_game.test_player_move(player__list[0], 2, 2)
    print(player__list[0].get_current_position())
    """



if __name__ == "__main__":
    main()
