import player
import constant
import region
import random


class Game:
    def __init__(self, region_list=None, player_list=None):
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
        return dice1, dice2

    # 한 플레이어가 한 턴 동안 하는 일. 주사위를 던져서 이동하고, 지역을 구매하는 것까지 포함한다.
    def player_move(self, _player: player.Player):
        dice1, dice2 = self.roll_dice()  # 주사위를 던진다.
        current_region = self.__region_list[_player.move(dice1, dice2)]  # 현재 _player 가 있는 지역
        assert isinstance(current_region, region.Region)  # 적절한 값인지 체크
        _type = current_region.get_buy_type(_player.get_id())  # 구매 타입을 정한다. constant.py 에 있는 내용 참조.
        # TODO: 지역 구매 여부 묻기
        # 만약 지역을 구매한다면 current_region.buy(_player) 를 호출

    # 모든 플레이어가 한 턴 동안 하는 일.
    # 게임이 끝나지 않는 경우에는 None 을 리턴하고, 누군가가 파산해서 게임이 끝나는 경우에는 파산한 플레이어의 id 를 리턴한다.
    def one_turn(self):
        self.__current_turn += 1  # 한 턴을 증가시킨다.
        for _player in self.__player_list:  # 모든 플레이어에 대해서 각각 한 턴씩 진행하고, 파산 여부를 체크한다.
            assert isinstance(_player, player.Player)  # 적절한 타입인지 체크
            self.player_move(_player)  # _player 가 한 턴 동안 하는 일을 시행한다.
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
    pass

if __name__ == "__main__":
    main()
