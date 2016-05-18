import constant
import map


class Player:
    __no = 0  # static variable. it is equal to the total number of players.

    def __init__(self, username="", initial_money=constant.INITIAL_MONEY):
        Player.__no += 1
        if username != "":
            self.__username = username  # should not change username after initialization.
        else:
            self.__username = "Player%d" % Player.__no
        self.__money = initial_money # Initialize money
        self.marker = Marker()
        self.__id = Player.__no  # This variable must have unique value.

    def move(self, distance: int, map_info: map.Map):
        # give money when
        self.__money += constant.ROTATION_MONEY * self.marker.move(distance)
        # TODO: checking current position is already bought region or not.
        # If it is already bought, then pay toll.
        owner = map_info.check_owner(self.get_current_pos())
        if owner is not None and owner != self.__id:
            self.pay_toll()
        # Ask people to buy or not.
        want_to_buy = True
        if want_to_buy:
            if self.buy(map_info.get_region(self.get_current_pos())):
                print("Success.")
            else:
                print("Fail.")

    def get_current_money(self):
        return self.__money

    def add_money(self, money: int):
        self.__money += money

    def pay_toll(self):
        # TODO: Implement this.
        pass

    def get_current_pos(self):
        return self.marker.get_current_pos()

    def get_username(self):
        return self.__username

    def get_id(self):
        return self.__id

    def buy(self, region : map.Region):
        price = region.get_price(owner=self.__id)
        if self.__money > price:
            self.__money -= price
            region.set_owner(self.__id)
            return True
        else:
            return False


# This class for display Player's marker.
class Marker:
    def __init__(self):
        self.__current_pos = 0

    def move(self, distance=0):
        rotate_times = (self.__current_pos + distance) // constant.TOTAL_REGION
        self.__current_pos = (self.__current_pos + distance) % constant.TOTAL_REGION
        # TODO: Display Marker on screen.
        return rotate_times

    def get_current_pos(self):
        return self.__current_pos
