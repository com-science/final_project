import constant
import player
import tkinter as tk
# region id를 가져올 수 있는 get_region_id()를 추가했습니다


class Region:
    __no = 0  # 땅의 총 수를 의미한다.

    def __init__(self, name, initial_price=0, is_desert=False, root_view=None, _x=0, _y=0):
        Region.__no += 1
        self.__id = Region.__no  # 땅의 id
        self.__name = name  # 땅의 명칭
        self.__owner = None  # 소유자. 타입은 player.Player 로 한다.
        self.initial_price = initial_price  # 초기 구매 비용
        self.__current_price = initial_price  # 현재 구매 비용
        self.__is_desert = is_desert  # 무인도 여부
        self.set_view(root_view, _x, _y)
        """
        if root_view is not None:
            self.__Rect = RegionRect(root_view, name, self.__current_price)
            self.__Rect.grid(column=_x, row=_y)
        """
        self.__can_buy = True

    def set_view(self, root_view: tk.Canvas=None, _x=0, _y=0):
        if isinstance(root_view, tk.Canvas):
            self.__Rect = RegionRect(root_view, self.__name, self.__current_price)
            self.__Rect.grid(column=_x, row=2*_y)
            frame = tk.Frame(root_view, height=38, width=0)
            frame.grid(column=_x, row=2*_y+1)
            x,y=_x*90, _y*80
            root_view.create_rectangle(x,y, x+90, y+80, width=1, fill="white")

    # 지역을 구매할 수 없게 한다.
    def set_cannot_buy(self):
        self.__can_buy = False

    def can_buy(self):
        # __can_buy 변수를 변경할 수 없게 하기 위한 용도.
        return self.__can_buy is True

    # 지역의 속성을 초기화 한다. (게임을 재시작할 경우에 실행해야 한다.)
    def reset(self):
        self.__owner = None  # 소유자 초기화
        self.__current_price = self.initial_price  # 현재 땅의 금액을 초기화
        # Update view.
        self.__Rect.update_price(self.__current_price)
        self.__Rect.change_owner('green')

    def get_region_id(self):
        return self.__id

    # 그 지역의 통행료를 리턴한다.
    def get_toll(self):
        return int(self.__current_price * constant.TOLL_RATE)

    # 그 지역을 소유하고 있는 player 객체를 리턴한다.
    def get_owner(self):
        return self.__owner

    # 그 지역을 소유하고 있는 player 의 id 를 리턴한다. 만약 소유하고 있는 사람이 없는 경우엔 None 을 반환한다.
    def get_owner_id(self):
        if self.__owner is not None:
            return self.__owner.get_id()
        else:
            return None

    # 그 지역이 사막인지 여부를 리턴한다.
    def is_desert(self):
        return self.__is_desert

    # 지역을 무인도로 설정한다. 무인도의 경우 구입을 할 수 없게 한다.
    def set_desert(self):
        self.__is_desert = True
        self.set_cannot_buy()

    # 그 지역을 업그레이드를 하기 위해 필요한 금액을 리턴한다. 소수점은 버린다.
    def __get_upgrade_price(self):
        return int(self.__current_price * constant.UPGRADE_RATE)

    # 그 지역의 소유자를 변경 하기 위해 필요한 금액을 리턴한다. 소수점은 버린다.
    def __get_change_owner_price(self):
        return int(self.__current_price * constant.CHANGE_OWNER_RATE)

    # 그 지역을 구입하는데 필요한 금액을 리턴한다.
    # _player_id 를 통해서 자동으로 '처음 구매', '업그레이드', '소유자 변경'인지를 판단해서 적절한 금액을 리턴한다.
    def get_sales_price(self, _player_id: int):
        # 처음 구매
        if self.__owner is None:
            return self.__current_price
        # 소유자 변경
        elif self.__owner.get_id() != _player_id:
            return self.__get_change_owner_price()
        # 업그레이드
        else:
            return self.__get_upgrade_price()

    # 이 지역의 소유자를 _player 로 변경한다. 단 무인도의 경우에는 소유자가 없다고 생각한다.
    def __change_owner(self, _player: player.Player):
        # 사막 여부 판단
        if self.is_desert():
            return
        elif self.__owner is not _player:  # 이전 소유자와 다른 경우에는 업데이트한다.
            self.__owner = _player
            self.__Rect.change_owner(_player.get_color())

    def get_buy_type(self, _player_id: int):
        if self.__owner is None:
            return constant.REGION_FIRST_BUY
        elif self.__owner.get_id() != _player_id:
            return constant.REGION_CHANGE_OWNER
        else:
            return constant.REGION_UPGRADE

    # _player 가 그 지역을 구매한다. 구매에 성공한 경우에는 True 를 리런하고, 실패한 경우에는 False 를 리턴한다.
    def buy(self, _player: player.Player):
        # 사막 여부 판단
        if self.is_desert():
            return False
        sales_price = self.get_sales_price(_player.get_id())  # 판매 금액 얻기.
        if self.__owner is None: # 밑에 owner.get id != player.get id에서 owner가 None인 경우 애러가 나서 수정했습니다.
            is_success = _player.pay_money(sales_price)
        elif self.__owner.get_id() != _player.get_id():  # 소유자가 다른 경우에는 지역을 구매하는데 든 돈을 이전 소유자에게 지불.
            is_success = _player.pay_money(sales_price, self.__owner)
        else:  # 소유자가 없거나 혹은 소유자가 같은 경우에는 단순히 돈만 감소시킨다.
            is_success = _player.pay_money(sales_price)

        if is_success:  # 구매가 성공한 경우
            self.__change_owner(_player)  # 소유자 변경
            self.__current_price = sales_price  # 현재 금액 업데이트
            self.__Rect.update_price(sales_price)
        return is_success

    def get_current_price(self):
        return self.__current_price

class RegionRect(tk.Frame):
    def __init__(self, master=None, region_name="", price=0):
        tk.Frame.__init__(self, master=master, width=90, height=42)

        self.__region_label = tk.Label(self, text=region_name, bg="green")
        self.__region_label.pack(fill=tk.X)
        self.__price_label = tk.Label(self, text=price, bg="yellow")
        self.__price_label.pack(fill=tk.X)
        self.pack_propagate(0)
        """
        tk.Frame.__init__(self, master=master, width=90, height=42)
        self.__region_label = make_label(self, 90, 21, text=region_name, bg="red")
        self.__price_label = make_label(self, 90, 21, text=price, bg="yellow")
        self.__region_label.pack(fill=tk.X)
        self.__price_label.pack(fill=tk.X)
        self.pack_propagate(0)
        """
        """
        tk.Frame.__init__(self, master=master, width=90, height=80)#, bg="white", bd=2)
        self.__region_label = tk.Label(self, text=region_name, bg="red")
        self.__region_label.pack(fill=tk.X)
        self.__price_label = tk.Label(self, text=price, bg="yellow")
        self.__price_label.pack(fill=tk.X)
        self.pack_propagate(0)
        """

    def update_price(self, price):
        self.__price_label.config(text=price)

    def change_owner(self, color):
        self.__region_label.config(bg=color)

def test():
    root_view = tk.Tk()
    #w = tk.Label(root_view, text="Red", bg="red", fg="white")
    #RegionRect(root_view, "정문").grid(row=1, column=1)
    #RegionRect(root_view, "법대").grid(row=2, column=1)
    #RegionRect(root_view, "가나").grid(row=2, column=2)
    idx = 1
    price = 200
    for i in range(1, 6):
        rect = RegionRect(root_view, "r%d" % idx)
        rect.grid(row=i, column=1)
        rect.update_price(price*idx)
        idx+=1
    for i in range(2, 6):
        rect = RegionRect(root_view, "r%d" % idx)
        rect.grid(row=5, column=i)
        rect.update_price(price*idx)
        idx+=1
    for i in range(2, 6):
        rect = RegionRect(root_view, "r%d" % idx)
        rect.grid(row=6-i, column=5)
        rect.update_price(price*idx)
        idx+=1

    for i in range(1, 6):
        rect = RegionRect(root_view, "r%d" % idx)
        rect.grid(row=0, column=6-i)
        rect.update_price(price*idx)
        idx+=1

    root_view.mainloop()


def test2():
    region_name_list = ['정문', '법대', '규장각', '사회대', '문화관', '잔디밭', '학생회관', '자연대',
                    '농생대', '농식', '해동', '아랫공대', '공깡', '중도', '관정', '인문대', '인문신양',
                    '자하연', '음미대', '경영대', '체육관', 'MOA', '대운동장', '기숙사', '감골식당',
                    '사범대', '롯데리아', '느티나무']
    region_price_list = [0, 500, 1600, 2100, 1500, 800, 1800, 1000, 2000, 1400, 1200, 2500, 1200, 1500, 800, 1500, 2200,
                     1300, 1800, 800, 2000, 1200, 900, 1100, 2100, 1300, 1600, 2700]
    x_pos = [0 for i in range(constant.ROW_OF_REGIONS - 1)] + [i for i in range(constant.COLUMN_OF_REGIONS - 1)] + [constant.COLUMN_OF_REGIONS - 1 for i in range(constant.ROW_OF_REGIONS - 1)] + [(constant.COLUMN_OF_REGIONS - 1 - i) for i in range(constant.COLUMN_OF_REGIONS - 1)]
    print(x_pos)
    y_pos = [i for i in range(constant.ROW_OF_REGIONS - 1)] + [constant.ROW_OF_REGIONS - 1 for i in range(constant.COLUMN_OF_REGIONS - 1)] + [(constant.ROW_OF_REGIONS - 1 - i) for i in range(constant.ROW_OF_REGIONS - 1)] + [0 for i in range(constant.COLUMN_OF_REGIONS - 1)]
    print(y_pos)
    root = tk.Tk()
    root_view = tk.Canvas(root)
    root_view.pack()
    region__list = [Region(region_name_list[i], region_price_list[i], root_view=root_view, _x=x_pos[i], _y=y_pos[i]) for i in range(constant.TOTAL_REGIONS)]
    root.update_idletasks()
    #region__list[0].reset()
    #tk.Button(text="Button").place(x=250, y=500)
    root_view.mainloop()

if __name__ == "__main__":
    test2()