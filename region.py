import constant
import player
import tkinter as tk


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
        self.__can_buy = True

    # set region view.
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
        updated_price = sales_price
        if self.__owner is None: # 밑에 owner.get id != player.get id에서 owner가 None인 경우 애러가 나서 수정했습니다.
            is_success = _player.pay_money(sales_price)
        elif self.__owner.get_id() != _player.get_id():  # 소유자가 다른 경우에는 지역을 구매하는데 든 돈을 이전 소유자에게 지불.
            is_success = _player.pay_money(sales_price, self.__owner)
        else:  # 소유자가 없거나 혹은 소유자가 같은 경우에는 단순히 돈만 감소시킨다.
            is_success = _player.pay_money(sales_price)
            updated_price += self.__current_price

        if is_success:  # 구매가 성공한 경우
            self.__change_owner(_player)  # 소유자 변경
            self.__current_price = updated_price  # 현재 금액 업데이트
            self.__Rect.update_price(self.__current_price)
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

    def update_price(self, price):
        self.__price_label.config(text=price)

    def change_owner(self, color):
        self.__region_label.config(bg=color)