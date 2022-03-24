import turtle
from random import *
from turtle import *
from StoryGame import StoryGame
from freegames import path

car = path('car.gif')
tiles = list(range(32)) * 2
state = {'mark': None}
hide = [True] * 64
num_of_pairs_found = 0


def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    idx = int((x + 200) // 50 + ((y + 200) // 50) * 8)
    return idx


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    global num_of_pairs_found
    """Update mark and hidden tiles based on tap."""
    spot = index(x, y)
    # print("Tapped on index:", spot)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
        # print("55")
    else:
        print("Found Pair")
        num_of_pairs_found += 1
        print("num of found pairs =", num_of_pairs_found)
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None
        if num_of_pairs_found % 3 == 0:
            print("Generate Question")
        if num_of_pairs_found == 32:
            print("Finished the game!")
            turtle.bye()


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 100)


shuffle(tiles)
# print(tiles)
# lst8 = tiles[0:8]
# lst7 = tiles[8:16]
# lst6 = tiles[16:24]
# lst5 = tiles[24:32]
# lst4 = tiles[32:40]
# lst3 = tiles[40:48]
# lst2 = tiles[48:56]
# lst1 = tiles[56:64]
# print(lst1)
# print(lst2)
# print(lst3)
# print(lst4)
# print(lst5)
# print(lst6)
# print(lst7)
# print(lst8)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
sg = StoryGame()
sg.start_game()
draw()
done()
