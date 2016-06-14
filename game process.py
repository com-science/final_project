import game
import constant
import player
import region

# dice_num 이라는 변수를 추가하여 두 dice 숫자가 같을 때 턴을 한번 더 반복
from tkinter import *


class Map:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Game 1.0")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=950, height=700)
        self.canvas.pack()
        self.tk.update()

# 지역 이름과 가격의 목록. 시작지점은 가격이 0원이고 구입할 수 없도록 추가해야 함.
region_name_list = ['정문', '법대', '규장각', '사회대', '문화관', '잔디밭', '학생회관', '자연대',
                    '농생대', '농식', '해동', '아랫공대', '공깡', '중도', '관정', '인문대', '인문신양',
                    '자하연', '음미대', '경영대', '체육관', 'MOA', '대운동장', '기숙사', '감골식당',
                    '사범대', '롯데리아', '느티나무']

region_price_list = [0, 500, 1600, 2100, 1500, 800, 1800, 1000, 2000, 1400, 1200, 2500, 1200, 1500, 800, 1500, 2200,
                     1300, 1800, 800, 2000, 1200, 900, 1100, 2100, 1300, 1600, 2700]


# 지역이름과 가격으로 리스트 작성
region__list = [region.Region(region_name_list[i], region_price_list[i]) for i in range(28)]
region__list[14].set_desert()
region__list[0].set_cannot_buy()

START_MONEY = 10000
g = Map()
tiles = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,1,1,1,1,1,1,1,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,1,1,1,1,1,1,1,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0],]


background = PhotoImage(file='back.png')

for y in range(0, 10):
    for x in range(0, 14):
        if tiles[y][x] == 0:
            if x < 10:
                g.canvas.create_image(70*x, 70*y, anchor=NW, image=background)
        elif tiles[y][x] == 1:
            if x == 8 and y > 0:
                g.canvas.create_text(70*x, 70*y, anchor=NW, text=region_name_list[8-y])
            if y == 8 and x < 8:
                g.canvas.create_text(70*x, 70*y, anchor=NW, text=region_name_list[x+20])
            if x == 1 and y < 8:
                g.canvas.create_text(70*x, 70*y, anchor=NW, text=region_name_list[y+13])
            if y == 1 and x > 0:
                g.canvas.create_text(70*x, 70*y, anchor=NW, text=region_name_list[15-x])

g.canvas.create_text(800, 0, anchor=NW, text='player 1', font=25)
g.canvas.create_text(800, 100, anchor=NW, text='money')
g.canvas.create_text(800, 250, anchor=NW, text='player 2', font=25)
g.canvas.create_text(800, 350, anchor=NW, text='money')
# g.canvas.create_arc(260,260,430,360,extent=359,style=ARC)
g.canvas.pack()
print_players_money = [g.canvas.create_text(800, 150+250*i, anchor=NW, text=constant.START_MONEY) for i in range(2)]
# 아래 두 변수는 삭제 예정..
print_player_1_money = print_players_money[0]
print_player_2_money = print_players_money[1]
g.canvas.update()

# 현재는 2명을 전제로 하므로 player number를 고정
player__number = constant.PLAYER_NO

# 임의의 플레이어 2명을 생성. 후에 player 수를 사용자가 입력할 수 있을 때 Player 이름 입력란도 추가할 예정
player1 = player.Player('A', g.canvas, 'red')
player2 = player.Player('B', g.canvas, 'blue')
player__list = [player1, player2]

# 새로운 게임 생성, 위에서 작성한 region list와 player list를 이용
New_game = game.Game(region__list, player__list, g.canvas)
player_dice_result = g.canvas.create_text(275, 300, anchor=NW, text="player %d turn" % 1)


def one_player_move(_no):
    global dice_num
    if isinstance(dice_button, Button):
        dice_button.configure(state=DISABLED)
    current__player = player__list[_no]  # 게임 진행 순서에 따라 현재 플레이어를 변수화
    print("player %d turn" % (_no + 1))

    dice_num = New_game.player_move(current__player)  # 현재 플레이어의 이동, 한바퀴 돌았을 때 돈을 지급하는 기능이 여기 포함되어 있음

    _current_player = player__list[_no]
    print('player%d current money : %d' % (_no + 1, _current_player.get_current_money()))
    # Update money...
    for _player_id in range(constant.PLAYER_NO):
        g.canvas.itemconfig(print_players_money[_player_id], text=str(player__list[_player_id].get_current_money()))

    g.canvas.update()
    print('player%d current position : %s' % (_no + 1, _current_player.get_current_position()))

    _owned_region = []
    for region_id in range(constant.TOTAL_REGIONS):
        if region__list[region_id].get_owner_id() == _current_player.get_id():
            _owned_region.append(region_id)
    print('owned_region', _owned_region)

    # 각 플레이어가 이동을 마치고 턴을 하나씩 증가, 파산한 플레이어가 있는지 여부를 검사
    if _no == 2:
        if New_game.one_turn() is not None:
            print(current__player.get_id())

    if isinstance(dice_button, Button):
        dice_button.configure(state=NORMAL)
    print("player %d turn" % ((_no + 1) % constant.PLAYER_NO + 1))
    g.canvas.itemconfig(player_dice_result, text="player %d turn" % ((_no + 1) % constant.PLAYER_NO + 1))

    g.canvas.update()
    return (_no + 1) % constant.PLAYER_NO

iter_num = 0  # 20턴이 모두 지났을 때 중단하는 역할

# test
_current_player_id = 0


def game_test():
    global iter_num
    global _current_player_id
    global player_1
    global player_2
    global owned_region
    iter_num = iter_num + 1
    if iter_num == 21:  # 20턴이 모두 지났을 때 중단하는 역할
        print('game over')
        return
    # player_1과 player_2는 New game의 player list에서 각 플레이어를 가져 오는 변수
    player_1 = New_game.get_player_list()[0]
    player_2 = New_game.get_player_list()[1]
    # owned_region은 New game의 지역 정보. 각각 플레이어가 어떤 지역들을 소유하고 있는지 나타내는데 이용
    owned_region = New_game.get_region_list()

    START_MONEY = 10000
    _current_player_id = one_player_move(_current_player_id)
    if dice_num[0] == dice_num[1]:
        _current_player_id -= 1
    # _current_player_id = (_current_player_id + 1) % constant.PLAYER_NO

i = 0
# game_test를 실행하는 버튼을 만듬, 이 버튼을 누르면 각 player들이 주사위를 던짐
dice_button = Button(g.tk, text='roll dices', command=game_test)
dice_button.pack()
g.tk.mainloop()

