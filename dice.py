import tkinter as tk


class Dice(tk.PhotoImage):
    # dice image file path
    __images_path = {i: ("dice_images\\dice%d.gif" % i) for i in range(1, 7)}

    # initial image
    def __init__(self):
        super().__init__(file="dice_images\\dice0.gif")

    # update dice image
    def __update_image(self, image_path):
        self.config(file=image_path)

    # update dice num
    def update_dice_num(self, num:int):
        self.__update_image(Dice.__images_path[num])



