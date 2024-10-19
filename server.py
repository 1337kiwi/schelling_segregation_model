# Made by Kiwi! 

import mesa
from model import Schelling

def get_happy_agents(model):
    """
    Display a text count of how many happy agents there are.
    """
    return f"Agents that want to move: {model.happy}"

def get_satisfaction_pale_red(model):
    """
    Display the average satisfaction score for pale red.
    """
    return f"Average Satisfaction Score (Pale Red): {model.satisfactionPaleRed}"

def get_satisfaction_light_red(model):
    """
    Display the average satisfaction score for light red.
    """
    return f"Average Satisfaction Score (Light Red): {model.satisfactionLightRed}"

def get_satisfaction_dark_red(model):
    """
    Display the average satisfaction score for dark red.
    """
    return f"Average Satisfaction Score (Dark Red): {model.satisfactionDarkRed}"

def get_satisfaction_pale_blue(model):
    """
    Display the average satisfaction score for pale blue.
    """
    return f"Average Satisfaction Score (Pale Blue): {model.satisfactionPaleBlue}"

def get_satisfaction_light_blue(model):
    """
    Display the average satisfaction score for light blue.
    """
    return f"Average Satisfaction Score (Light Blue): {model.satisfactionLightBlue}"

def get_satisfaction_dark_blue(model):
    """
    Display the average satisfaction score for dark blue.
    """
    return f"Average Satisfaction Score (Dark Blue): {model.satisfactionDarkBlue}"

def get_avg_homophily_red(model):
    """
    Display the average homophily score for red.
    """
    return f"Average Homophily (Red): {model.avgHomophilyRed}"

def get_avg_homophily_blue(model):
    """
    Display the average homophily score for blue.
    """
    return f"Average Homophily (Blue): {model.avgHomophilyBlue}"

def get_avg_homophily_pale(model):
    """
    Display the average homophily score for pale.
    """
    return f"Average Homophily (Pale): {model.avgHomophilyPale}"

def get_avg_homophily_light(model):
    """
    Display the average homophily score for light.
    """
    return f"Average Homophily (Light): {model.avgHomophilyLight}"

def get_avg_homophily_dark(model):
    """
    Display the average homophily score for dark.
    """
    return f"Average Homophily (Dark): {model.avgHomophilyDark}"


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 1, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = "#FF0000"  # Dark Red
    elif agent.type == 1:
        portrayal["Color"] = "#FF7F7F"  # Light Red
    elif agent.type == 2:
        portrayal["Color"] = "#FFCCCC"  # Pale Red
    elif agent.type == 3:
        portrayal["Color"] = "#0000FF"  # Dark Blue
    elif agent.type == 4:
        portrayal["Color"] = "#7F7FFF"  # Light Blue
    elif agent.type == 5:
        portrayal["Color"] = "#CCCCFF"  # Pale Blue
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(
    portrayal_method=schelling_draw,
    grid_width=50,
    grid_height=50,
    canvas_width=800,
    canvas_height=800,
)

happy_chart = mesa.visualization.ChartModule([{"Label": "happy", "Color": "Black"}])
satisfaction_chart = mesa.visualization.ChartModule([
    {"Label": "satisfactionPaleRed", "Color": "#FFCCCC"},
    {"Label": "satisfactionLightRed", "Color": "#FF7F7F"},
    {"Label": "satisfactionDarkRed", "Color": "#FF0000"},
    {"Label": "satisfactionPaleBlue", "Color": "#CCCCFF"},
    {"Label": "satisfactionLightBlue", "Color": "#7F7FFF"},
    {"Label": "satisfactionDarkBlue", "Color": "#0000FF"}
])

color_homophily_chart = mesa.visualization.ChartModule([
    {"Label": "avgHomophilyRed", "Color": "#FF0000"},
    {"Label": "avgHomophilyBlue", "Color": "#0000FF"}
])

type_homophily_chart = mesa.visualization.ChartModule([
    {"Label": "avgHomophilyPale", "Color": "#00c5ff"},
    {"Label": "avgHomophilyLight", "Color": "#00f9ff"},
    {"Label": "avgHomophilyDark", "Color": "#0000FF"}
])

model_params = {
    "height": 50,
    "width": 50,
    "density": mesa.visualization.Slider(
        name="Agent density", value=0.8, min_value=0.1, max_value=1.0, step=0.1
    ),
    "statisfactionThreshold": mesa.visualization.Slider(
        name="Statisfaction Threshold", value=0.4, min_value=0.00, max_value=1.0, step=0.1
    ),
    "radius": mesa.visualization.Slider(
        name="Search Radius", value=1, min_value=1, max_value=5, step=1
    ),
    "society": mesa.visualization.Slider(
        name="Society", value=1, min_value=1, max_value=3, step=1
    ),
    "strategy": mesa.visualization.Slider(
        name="Strategy", value=1, min_value=1, max_value=3, step=1
    ),
}

server = mesa.visualization.ModularServer(
    model_cls=Schelling,
    visualization_elements = [
        canvas_element,
        get_happy_agents,
        happy_chart,
        get_satisfaction_pale_red,
        get_satisfaction_light_red,
        get_satisfaction_dark_red,
        get_satisfaction_pale_blue,
        get_satisfaction_light_blue,
        get_satisfaction_dark_blue,
        satisfaction_chart,
        get_avg_homophily_red,
        get_avg_homophily_blue,
        color_homophily_chart,
        get_avg_homophily_pale,
        get_avg_homophily_light,
        get_avg_homophily_dark,
        type_homophily_chart
        ],
    name="Schelling Segregation Model",
    model_params=model_params,
)