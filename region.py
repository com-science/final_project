import constant
import player
import tkinter as tk


class Region:
    __no = 0  # total numbers of region(initial value)

    def __init__(self, name, initial_price=0, is_desert=False, root_view=None, _x=0, _y=0):
        Region.__no += 1
        self.__id = Region.__no  # region id
        self.__name = name  # region name
        self.__owner = None  # owner. type is player.Player
        self.initial_price = initial_price  # initial price of region
        self.__current_price = initial_price  # current price of region
        self.__is_desert = is_desert  # whether desert or not
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

    # setting region unable to buy
    def set_cannot_buy(self):
        self.__can_buy = False
        
    # method for encapsulation __can_by
    def can_buy(self):
        return self.__can_buy is True

    # reset region information(when restart a game)
    def reset(self):
        self.__owner = None  # reset owner
        self.__current_price = self.initial_price  # reset region price
        # Update view.
        self.__Rect.update_price(self.__current_price)
        self.__Rect.change_owner('green')

    # return region id
    def get_region_id(self):
        return self.__id

    # return toll of region
    def get_toll(self):
        return int(self.__current_price * constant.TOLL_RATE)

    # return owner of region(player.Player type)
    def get_owner(self):
        return self.__owner

    # return owner's id. if none has that region, return none
    def get_owner_id(self):
        if self.__owner is not None:
            return self.__owner.get_id()
        else:
            return None

    # return if this region is desert
    def is_desert(self):
        return self.__is_desert

    # set region with desert. player cannot buy desert
    def set_desert(self):
        self.__is_desert = True
        self.set_cannot_buy()

    # return price for upgrading region.
    def __get_upgrade_price(self):
        return int(self.__current_price * constant.UPGRADE_RATE)

    # return price for changing owner.
    def __get_change_owner_price(self):
        return int(self.__current_price * constant.CHANGE_OWNER_RATE)

    # return price for buying or upgrade region,
    # with _player_id, return proper type of purchase(first buy, upgrade, change owner)
    def get_sales_price(self, _player_id: int):
        # first purchase
        if self.__owner is None:
            return self.__current_price
        # change owner
        elif self.__owner.get_id() != _player_id:
            return self.__get_change_owner_price()
        # upgrade
        else:
            return self.__get_upgrade_price()

    # change owner to _player. but none can buy desert
    def __change_owner(self, _player: player.Player):
        # confirm that a region is desert or not
        if self.is_desert():
            return
        elif self.__owner is not _player:  # change owner part
            self.__owner = _player
            self.__Rect.change_owner(_player.get_color())

    def get_buy_type(self, _player_id: int):
        if self.__owner is None:
            return constant.REGION_FIRST_BUY
        elif self.__owner.get_id() != _player_id:
            return constant.REGION_CHANGE_OWNER
        else:
            return constant.REGION_UPGRADE

    # _player buy region. when success to buy, return True. other wise, return False
    def buy(self, _player: player.Player):
        # when region is desert, return False
        if self.is_desert():
            return False
            
        sales_price = self.get_sales_price(_player.get_id()) # get sales price
        updated_price = sales_price
        if self.__owner is None: # # when none owns the region
            is_success = _player.pay_money(sales_price)
        elif self.__owner.get_id() != _player.get_id():  # when owner and _player is different, pay money to owner
            is_success = _player.pay_money(sales_price, self.__owner)
        else:  # when owner == player,
            is_success = _player.pay_money(sales_price)
            updated_price += self.__current_price

        if is_success:  # when success to buy
            self.__change_owner(_player)  # change owner
            self.__current_price = updated_price  # update current sales price
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
