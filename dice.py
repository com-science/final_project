import tkinter as tk


class Dice(tk.PhotoImage):
    __images_path = {i: ("dice_images\\dice%d.gif" % i) for i in range(1, 7)}

    def __init__(self):
        super().__init__(file="dice_images\\dice0.gif")

    def __update_image(self, image_path):
        self.config(file=image_path)

    def update_dice_num(self, num:int):
        self.__update_image(Dice.__images_path[num])

#    def __eq__(self, other):



def main():
    root_view = tk.Tk()
    canvas = tk.Canvas(root_view)
    dice1, dice2 = Dice(), Dice()
    dice1.update_dice_num(2); dice2.update_dice_num(4)
    canvas.create_image(50, 50, image=dice1)
    canvas.create_image(120, 50, image=dice2)
    canvas.pack()
    import time
    import random
    for i in range(20):
        dice1.update_dice_num(random.randint(1, 6))
        dice2.update_dice_num(random.randint(1, 6))
        canvas.update()
        time.sleep(0.1)
    root_view.mainloop()

if __name__== "__main__":
    main()