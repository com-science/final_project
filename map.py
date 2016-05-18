import constant


class Region:
    def __init__(self, name, initial_price):
        self.__name = name
        self.__owner_id = None
        self.__initial_price = initial_price
        self.__buy_times = 0
        self.__current_price = initial_price

    def get_price(self, owner=None):
        return self.__current_price

    def get_owner_id(self):
        return self.__owner_id

    def set_owner(self, owner_id):
        if self.__owner_id != owner_id:
            self.__owner_id = owner_id
        else:
            self.upgrade()

    def upgrade(self):
        self.__current_price


class Map:
    def __init__(self):
        self.__regions = [Region("AAA"), Region("AAB")]
        self.__players = {}

    def check_owner(self, region_id):
        # TODO: implement checking the region is already bought or not.
        pass

    def get_owner_by_region_id(self, region_id):
        owner_id = self.get_region(region_id).get_owner_id()
        return self.__players.get(owner_id, None)

    def get_region(self, region_id):
        return self.__regions[region_id]

map_info = Map()
print(map_info.get_owner_by_region_id(1))