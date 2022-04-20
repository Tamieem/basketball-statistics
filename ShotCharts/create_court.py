import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc


def create_court(ax=None, color='black', lw=2, out_lines=False):
    if ax is None:
        ax = plt.gca()

    # basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color, fill=False)

    # Paint
    outer_paint = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_paint = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # free throw
    free_throw_top = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    free_throw_bottom = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    # restricted area
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color, )

    # three point line
    corner_three1 = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three2 = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # center court
    center_outer = Arc((0, 422.5), 120, 120, theta2=0, theta1=180, linewidth=lw, color=color)
    center_inner = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    court = [hoop, backboard, outer_paint, inner_paint, free_throw_bottom, free_throw_top, restricted,
             corner_three1, corner_three2, three_arc, center_outer, center_inner]
    if out_lines:
        out_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court.append(out_lines)
    for item in court:
        ax.add_patch(item)

    return ax
