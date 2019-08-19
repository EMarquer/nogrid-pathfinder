APP_TITLE = "Test app"

DRAW_SCALE = 100
COOR_TEXT = "x: {}\ny: {}"
GRID_PRECISIONS = tuple(i / 10 for i in range(1, 11, 1))

def get_color(r_ratio: float, g_ratio: float, b_ratio: float, rate: float=1):
    # apply rate
    def apply_rate(color_ratio: float) -> float:
        return (1 * (1 - rate)) + (color_ratio * rate)

    # convert [0; 1] to hexa
    r = min(round(apply_rate(r_ratio) * 256), 255)
    g = min(round(apply_rate(g_ratio) * 256), 255)
    b = min(round(apply_rate(b_ratio) * 256), 255)

    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

ORIGIN_COLOR = "darkgreen"
TARGET_COLOR = "darkblue"
ASTAR_COLOR = "violet"
NOGRID_COLOR = "green"
GRID_COLOR = "lightgray"
OBSTACLE_COLOR_GETTER = lambda rate: get_color(.9, .5, .5, rate=rate)
OBSTACLE_BORDER_COLOR = "red"

NODE_RADIUS = 5
NODE_WIDTH = 3

LABEL_FRAME_KWARGS = {"side": "top", "fill": "x", "expand": "yes"}
COOR_INNER_FRAME_KWARGS = {"side": "left", "fill": "x", "expand": "yes", "ipadx": 5, "ipady": 5, "padx": 5, "pady": 5}


get_color(0, 0, 1)
get_color(.1, .2, .1)