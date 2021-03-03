from proc_plant.create_plant import Plant, draw_plants
from proc_plant.general_utils import connect_to_debugger


def test():

    connect_to_debugger()

    p = Plant("my_cool_plant")
    p.draw_plant()
    draw_plants(n=2)