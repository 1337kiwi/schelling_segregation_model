# Made by Kiwi! 

import mesa
import random

class SchellingAgent(mesa.Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, unique_id, model, agent_type, satisfaction_threshold, strategy):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type 
           satisfaction_threshold: The threshold we will define for the agent
           strategy: strategy to use
        """
        super().__init__(unique_id, model)
        self.type = agent_type

        # Metrics
        self.satisfaction_threshold = satisfaction_threshold
        self.satisfactionScore = 0
        self.satisfied = False 

        # Color and tolerance
        self.color = 0 # default to red
        self.tolerance = 0

        # Strategy for agent relocation
        self.strategy = strategy

        if self.type in [3, 4, 5]:
            self.color = 1 # blue if 3, 4, 5, red is default

        # Determine the tolerance threshold based on agent type
        if self.type == 0:  # Dark Red
            self.model.totalDarkRed += 1
            self.tolerance = 0.25
        elif self.type == 1:  # Light Red
            self.model.totalLightRed += 1
            self.tolerance = 0.7
        elif self.type == 2:  # Pale Red
            self.model.totalPaleRed += 1
            self.tolerance = 0.50
        elif self.type == 3:  # Dark Blue
            self.model.totalDarkBlue += 1
            self.tolerance = 0.25
        elif self.type == 4:  # Light Blue
            self.model.totalLightBlue += 1
            self.tolerance = 0.7
        elif self.type == 5:  # Pale Blue
            self.model.totalPaleBlue += 1
            self.tolerance = 0.50

    def step(self):
        shouldMove = False

        # Get neighbors
        neighbors = self.model.grid.iter_neighbors(
            self.pos, moore=True, radius=self.model.radius
        )

        # Send initial satisfaction
        self.satisfactionScore = calculate_satisfaction(neighbors, self.type)
        if self.type == 0:  # Dark Red
            self.model.satisfactionDarkRed += self.satisfactionScore
        elif self.type == 1:  # Light Red
            self.model.satisfactionLightRed += self.satisfactionScore
        elif self.type == 2:  # Pale Red
            self.model.satisfactionPaleRed += self.satisfactionScore
        elif self.type == 3:  # Dark Blue
            self.model.satisfactionDarkBlue += self.satisfactionScore
        elif self.type == 4:  # Light Blue
            self.model.satisfactionLightBlue += self.satisfactionScore
        elif self.type == 5:  # Pale Blue
            self.model.satisfactionPaleBlue += self.satisfactionScore

        # Send color count
        diversity = calculate_diversity(self, self.color, None)
        if self.color == 0: # red
            self.model.diversityRed += diversity
        else: # blue
            self.model.diversityBlue += diversity

        # Send type count
        typeDiversity = calculate_diversity(self, None, self.type)
        if self.type == 0 or self.type == 3:  # Dark agents
            self.model.diversityDark += typeDiversity
        elif self.type == 1 or self.type == 4:  # Light agents
            self.model.diversityLight += typeDiversity
        elif self.type == 2 or self.type == 5:  # Pale agents
            self.model.diversityPale += typeDiversity

        diversity = calculate_diversity(self, self.color, None)

        # If unhappy, decide to move:
        if diversity > self.tolerance:
            shouldMove = True
            self.model.happy += 1

        # Find the satisfaction score, total subtypes / total agents

        oldPos = self.pos
        # Begin Agent Relocation Strategy
        if shouldMove:
            newSatisfactionScore = -1
            if self.strategy == 1:
                self.model.grid.move_to_empty(self)
                neighbors = self.model.grid.iter_neighbors(
                            self.pos, moore=True, radius=self.model.radius
                            )
                self.satisfactionScore = calculate_satisfaction(neighbors, self.type)
            elif self.strategy == 2:
                # The agent will move to any available location on the matrix.
                self.model.grid.move_to_empty(self)
                neighbors = self.model.grid.iter_neighbors(
                            self.pos, moore=True, radius=self.model.radius
                            )
                newSatisfactionScore = calculate_satisfaction(neighbors, self.type)
                if newSatisfactionScore < self.satisfactionScore: # Check if satisfaction is higher
                    self.model.grid.move_to_empty(self)
                    neighbors = self.model.grid.iter_neighbors(
                                self.pos, moore=True, radius=self.model.radius
                                )
                    newSatisfactionScore = calculate_satisfaction(neighbors, self.type)
                    # If the 2nd step is still lower than the current, we go back
                    if newSatisfactionScore < self.satisfactionScore:
                        self.model.grid.move_agent(self, oldPos)
                    else:
                        self.satisfactionScore = newSatisfactionScore
                    # Shouldn't need to reset the neighbor iterator cuz it will reset on next step
                else:
                    self.satisfactionScore = newSatisfactionScore
            else:
                    successful = False
                    # Loop through neighbors
                    for i in range(5):
                        if successful == True:
                            break
                        # Get the neighborhood in a radius of 5
                        radiusNeighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=i)
                        # Get a list of empty cells in that neighborhood
                        # emptyCells = self.model.grid.select_cells(radiusNeighborhood, None, None, only_empty=True)
                        # Iterate through and test if the empty cells will give a higher satisfaction score
                        for cell in radiusNeighborhood:
                            if (self.model.grid.is_cell_empty(cell) is True): # If cell is full
                                self.model.grid.move_agent(self, cell)
                                neighbors = self.model.grid.iter_neighbors(
                                            self.pos, moore=True, radius=self.model.radius
                                            )
                                newSatisfactionScore = calculate_satisfaction(neighbors, self.type)
                                if newSatisfactionScore > self.satisfactionScore: # We found a successful location
                                    successful = True
                                    self.satisfactionScore = newSatisfactionScore
                                    break
    
                    if successful == False: 
                        self.model.grid.move_to_empty(self)
                        neighbors = self.model.grid.iter_neighbors(
                                        self.pos, moore=True, radius=self.model.radius
                                    )
                        newSatisfactionScore = calculate_satisfaction(neighbors, self.type)
                        # If the 2nd step is still lower than the current, we go back
                        if newSatisfactionScore < self.satisfactionScore:
                            self.model.grid.move_agent(self, oldPos)
                        else: 
                            self.satisfactionScore = newSatisfactionScore
                        
def calculate_satisfaction(neighbors, type):
    numSimilarSubtypes = 0
    numNeighbors = 0
    for neighbor in neighbors:
            if type == neighbor.type or type == neighbor.type + 3 or type + 3 == neighbor.type: # We can do this because 0 and 3 are dark, 1 and 4 are light, and 2 and 5 are pale
                numSimilarSubtypes += 1
            numNeighbors += 1
    if numNeighbors == 0:
        return 0
    return numSimilarSubtypes / numNeighbors

def calculate_diversity(agent, color=None, type=None):
    numNeighbors = 0
    numSimilar = 0
    neighbors = agent.model.grid.iter_neighbors(
            agent.pos, moore=True, radius=agent.model.radius
        )
    for neighbor in neighbors:
        # If red, similar if any reds exist. If blue, similar if any blues exist.
        if color is not None and color == neighbor.color:
            numSimilar += 1
        if type is not None and (type == neighbor.type or type == neighbor.type + 3 or type + 3 == neighbor.type):
            numSimilar += 1
        numNeighbors += 1

            # Number of different types of agents / total number of agents
    if numNeighbors == 0:
        return 0
    else: 
        return (numNeighbors - numSimilar) / numNeighbors

class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(
        self,
        height=20,
        width=20,
        statisfactionThreshold=0.4,
        radius=1,
        density=0.8,
        society=1,
        strategy=3,
        seed=None,
    ):
        """
        Create a new Schelling model.

        Args:
            width, height: Size of the space.
            density: Initial Chance for a cell to populated
            minority_pc: Chances for an agent to be in minority class
            homophily: Minimum number of agents of same class needed to be happy
            radius: Search radius for checking similarity
            seed: Seed for Reproducibility
            society:    1: Tolerant Society: 50% Light, 25% Pale, and 25% Dark, 
                        2: Neutral Society: 50% Pale, 25% Light, and 25% Dark
                        3: Intolerant Society: 50% Dark, 25% Light, and 25% Pal
            strategy:   1. Move Randomly
                        2. Move to a Random Cell with Higher Satisfaction
                        3. Move to the Nearest Cell with Higher Satisfaction
        """

        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.statisfactionThreshold = statisfactionThreshold
        self.radius = radius
        self.society = society
        self.strategy = strategy

        self.iterations = 0
        self.totalNumMoves = 0
        self.totalPaleRed = 0
        self.totalLightRed = 0 
        self.totalDarkRed = 0
        self.totalPaleBlue = 0
        self.totalLightBlue = 0 
        self.totalDarkBlue = 0

        # Homophily Metrics

        self.diversityRed = 0
        self.diversityBlue = 0
        self.diversityPale = 0
        self.diversityLight = 0
        self.diversityDark = 0

        self.avgHomophilyRed = 0
        self.avgHomophilyBlue = 0
        self.avgHomophilyPale = 0
        self.avgHomophilyLight = 0
        self.avgHomophilyDark = 0

        # End Homophily Metrics

        # Satisfaction Metrics

        self.satisfactionPaleRed = 0
        self.satisfactionLightRed = 0 
        self.satisfactionDarkRed = 0
        self.satisfactionPaleBlue = 0
        self.satisfactionLightBlue = 0 
        self.satisfactionDarkBlue = 0

        # End Satisfaction Metrics

        self.satisfactionScore = 0

        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = mesa.DataCollector(
            model_reporters = {
                                "happy": "happy", # Model-level count of happy agents
                                "satisfactionPaleRed": "satisfactionPaleRed",
                                "satisfactionLightRed": "satisfactionLightRed",
                                "satisfactionDarkRed": "satisfactionDarkRed",
                                "satisfactionPaleBlue": "satisfactionPaleBlue",
                                "satisfactionLightBlue": "satisfactionLightBlue",
                                "satisfactionDarkBlue": "satisfactionDarkBlue",
                                "avgHomophilyRed": "avgHomophilyRed",  # Reporting average homophily for red
                                "avgHomophilyBlue": "avgHomophilyBlue",  # Reporting average homophily for blue
                                "avgHomophilyPale": "avgHomophilyPale",  # Reporting average homophily for pale
                                "avgHomophilyLight": "avgHomophilyLight",  # Reporting average homophily for light
                                "avgHomophilyDark": "avgHomophilyDark"   # Reporting average homophily for dark
                            },  
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agentType = generate_agent_type(self.society)

                agent = SchellingAgent(self.next_id(), self, agentType, self.statisfactionThreshold, strategy)

                self.grid.place_agent(agent, pos)
                self.schedule.add(agent)

        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model.
        """
        numAgents = self.schedule.get_agent_count()
        self.satisfactionPaleRed = 0
        self.satisfactionLightRed = 0 
        self.satisfactionDarkRed = 0
        self.satisfactionPaleBlue = 0
        self.satisfactionLightBlue = 0 
        self.satisfactionDarkBlue = 0
        self.diversityRed = 0
        self.diversityBlue = 0 
        self.diversityPale = 0 
        self.diversityLight = 0 
        self.diversityDark = 0 

        self.happy = 0  # Reset counter of happy agents
        self.iterations += 1

        self.schedule.step()

        self.satisfactionPaleRed = self.satisfactionPaleRed / self.totalPaleRed if self.totalPaleRed > 0 else 0
        self.satisfactionLightRed = self.satisfactionLightRed / self.totalLightRed if self.totalLightRed > 0 else 0
        self.satisfactionDarkRed = self.satisfactionDarkRed / self.totalDarkRed if self.totalDarkRed > 0 else 0
        self.satisfactionPaleBlue = self.satisfactionPaleBlue / self.totalPaleBlue if self.totalPaleBlue > 0 else 0
        self.satisfactionLightBlue = self.satisfactionLightBlue / self.totalLightBlue if self.totalLightBlue > 0 else 0
        self.satisfactionDarkBlue = self.satisfactionDarkBlue / self.totalDarkBlue if self.totalDarkBlue > 0 else 0

        self.avgHomophilyRed = self.diversityRed / (self.totalLightRed + self.totalPaleRed + self.totalDarkRed)
        self.avgHomophilyBlue = self.diversityBlue / (self.totalLightBlue + self.totalPaleBlue + self.totalDarkBlue) 
        self.avgHomophilyPale = self.diversityPale / (self.totalPaleBlue + self.totalPaleRed) # Adjust if needed
        self.avgHomophilyLight = self.diversityLight / (self.totalLightRed + self.totalLightBlue)  # Adjust if needed
        self.avgHomophilyDark = self.diversityDark / (self.totalDarkRed + self.totalDarkBlue)  # Adjust if needed

        self.datacollector.collect(self)

        self.totalNumMoves += self.happy

        #if self.happy == self.schedule.get_agent_count():
        if self.happy == 0 or self.iterations == 999:
            self.running = False

def generate_agent_type(society):
    '''
    Generate the agent type based on the type of society
    '''
    curr = random.random()
    
    if society == 1:  # Tolerant Society
        if curr < 0.50:
            return random.choice([1,4])  # Light agents
        elif curr < 0.75:
            return random.choice([2,5])  # Pale (neutral) agents
        else:
            return random.choice([0,3])  # Dark Agents
        
    elif society == 2:  # Neutral Society
        if curr < 0.50:
            return random.choice([2,5])  # Pale (neutral) agents
        elif curr < 0.75:
            return random.choice([1,4])  # Light agents
        else:
            return random.choice([0,3])  # Dark Agents

    elif society == 3:  # Intolerant Society
        if curr < 0.50:
            return random.choice([0,3])  # Dark Agents
        elif curr < 0.75:
            return random.choice([1,4])  # Light agents
        else:
            return random.choice([2,5])  # Pale (neutral) agents