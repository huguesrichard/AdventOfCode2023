import math


max_balls = {"red": 12, "green": 13, "blue": 14}
d_c = {"red": 0, "green": 1, "blue": 2}

test = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

def read_draw(draw_text):
    """
    str -> Tuple(int, int, int)
    Reads a text with the number of blue, red and green
    and return a tuple with the corresponding values
    """
    t_draw = [0, 0, 0]
    for bs in draw_text.split(","):
        count, color = bs.strip().split(" ")
        t_draw[d_c[color]] = int(count)
    return tuple(t_draw)

def test_game(text):
    """ 
    str -> list(Tuple(int, Tuple(int,int,int)))
    Return the ID of the game is the config is possible 
    and 0 otherwise
    a Tuple with the (Red, Green, Blue) code
    """
    game_str, configs = text.split(":")
    gameID = int(game_str.removeprefix("Game "))
    l_configs = [read_draw(c) for c in configs.split(";")]
    if all((config_possible(x) for x in l_configs)):
        return gameID
    else:
        return 0

def power_game(text):
    """
    str -> Tuple(int,int,int)
    returns the minimum number of cubes of each color to make the 
    game work
    """
    game_str, configs = text.split(":")
    gameID = int(game_str.removeprefix("Game "))
    l_configs = [read_draw(c) for c in configs.split(";")]
    return [max(x) for x in zip(*l_configs)]

def config_possible(t_ball, max_vals = max_balls):
    """
    Tuple(int, int, int) -> Bool
    Returns True if the config is possible
    """
    for color in max_vals.keys():
        if t_ball[d_c[color]] > max_vals[color]:
            return False
    return True

for g in test:
    #print(g, ":", test_game(g))
    print(power_game(g))

fin = open("./input_day2.txt", "r")

#game_values = [test_game(l.strip()) for l in fin]
power_values = [math.prod(power_game(l.strip())) for l in fin]
fin.close()
#print(sum(game_values))
print(sum(power_values))
