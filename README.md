# Schelling Segregation Model

## Summary

The Schelling segregation model is a classic agent-based model, demonstrating how even a mild preference for similar neighbors can lead to a much higher degree of segregation than we would intuitively expect. The model consists of agents on a square grid, where each grid cell can contain at most one agent. Agents come in two colors: red and blue, and 3 shades, dark, light, and pale. They are happy if a certain number of their eight possible neighbors are of the same color, and unhappy otherwise. Unhappy agents will pick a random empty cell to move to each step, until they are happy. The model keeps running until there are no unhappy agents.

This program uses agent-based models and operationalizes agent behavior via norms. Norms are informal rules or behaviors that are considered acceptable or standard within a group or society. It also operationalizes Tolerance and experiment with societies with different levels of tolerance.

## Details


The multiagent environment is initialized with two primary types of agents, Red and Blue. Each agent type has the following three subtypes: Light, Pale, and Dark. In this simulation, each agent subtype follows a specific Tolerance (T), which defines their norms. Tolerance of agents can be categorized as low, medium, or high, and they determine how open an agent is to being surrounded by different types of agents.

- Light agents are most tolerant and can stay in diverse neighborhoods (i.e., agents with
different types). (High Tolerance)
- Pale agents are moderately tolerant and inclined to stay in balanced neighborhoods. (Medium Tolerance)
- Dark agents are the least tolerant and gravitate towards a homogenous neighborhood. (Low Tolerance)

NOTE: "Different types" refer to differences in the agent’s primary color types (i.e., Red and
Blue). “Different subtypes” refers to differences in the intensity of the color (i.e., Light, Pale, and
Dark). For example, for a Light Red agent, all Blue subtypes are considered a different type
(and all Red subtypes the same type), whereas all Light (regardless of color) are the same
subtype (and all Pale and Dark agents are a different subtype).

Neighborhoods are determined by Moore Neighborhood parsing methods, 

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

Directly run the file ``run.py`` in the terminal. e.g.

```
    $ python run.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

To view and run some example model analyses, launch the IPython Notebook and open ``analysis.ipynb``. Visualizing the analysis also requires [matplotlib](http://matplotlib.org/).

## How to Run without the GUI

To run the model with the grid displayed as an ASCII text, run `python run_ascii.py` in this directory.

## Files

* ``run.py``: Launches a model visualization server.
* ``model.py``: Contains the agent class, and the overall model class.
* ``server.py``: Defines classes for visualizing the model in the browser via Mesa's modular server, and instantiates a visualization server.

## Further Reading

Schelling's original paper describing the model:

[Schelling, Thomas C. Dynamic Models of Segregation. Journal of Mathematical Sociology. 1971, Vol. 1, pp 143-186.](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)

An interactive, browser-based explanation and implementation:

[Parable of the Polygons](http://ncase.me/polygons/), by Vi Hart and Nicky Case.

Norms:

[Robert Axelrod and William D. Hamilton, The Evolution of Cooperation](https://ee.stanford.edu/~hellman/Breakthrough/book/pdfs/axelrod.pdf)

[Robert Axelrod, An Evolutionary Approach to Norms](https://www.jstor.org/stable/1960858)