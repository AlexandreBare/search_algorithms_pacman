from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueueWithFunction
from pacman_module.util import manhattanDistance

initialNumFood = 0 #The initial number of food dots

def getNumFood(state):
    """
    Returns the number of food dots left to eat.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - The number of food dots left to eat.
    """
    
    foodMatrix = state.getFood()
    numFood = 0
    for row in foodMatrix:
        for element in row:
            if element == True:
                numFood += 1
    return numFood
    
def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state containing
    pacman's position and the current food grid representation.
    """
    
    return (state.getPacmanPosition(), state.getFood())
    
class PacmanAgent(Agent):
    
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:[]
        -------
        - A legal move as defined in `game.Directions`.
        """
        
        if not self.moves:
        	self.moves = self.astar(state)
            

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP
    
    def costFunction(n):
        """
        Returns the cost of the action leading to the given state. The cost is 
        equal to the current path length minus the number of food eaten
        
        Arguments:
        ----------
        - `n`: a tuple containing the current game sate and the
        saved path 
        
        Return:
        -------
        - the cost of the action leading to the current game state
        """
        
        state = n[0]
        path = n[1]
        return 1 + len(path) - (initialNumFood - getNumFood(state)) 
        
    def heuristic(n):
        """
        Returns the heuristic of the given state. This heuristic considers the goal to
        be the furthest food dot. It computes the highest manhattan distance from pacman
        to one of the food dot and from this food dot to the furthest food dot. The number
        of food dots left is retreived from the sum in order for the added cost to 
        catch a food dot to be 0
        
        Arguments:
        ----------
        - `n`: a tuple containing the current game sate and the
        saved path 
        
        Return:
        -------
        - the heuristic of the current game state
        """

        state = n[0]
        position = state.getPacmanPosition()
        dist = []
        foodPos = []
        maxDist = 0
        maxIndex = 0
        i = 0
        j = 0
        x = 0

        for row in state.getFood():
            for element in row:
                if element == True:
                    foodPos.append((i, j)) #save each food dot position
                    dist.append(manhattanDistance(foodPos[x], position)) 
                    #computes its manhattan distance to pacman
                    if dist[x] > maxDist:
                        maxDist = dist[x] 
                        furthestFoodIndex = x #saves the index of the furthest food dot
                    x += 1
                
                j += 1
                
            i += 1
            j = 0
        
        res = 0 #the estimated manhattan distance of the path left
        if len(dist) == 1: #if only one food dot left
            res = dist[0] 
        elif len(dist) > 1: #else if more than one left
            maxChasles = -1
            for a in range(len(dist)):
                if a != furthestFoodIndex:
                    chasles = dist[a] + manhattanDistance(foodPos[a], foodPos[furthestFoodIndex]) - dist[furthestFoodIndex] 
                    #the manhattan distance increase computed by adding one food dot on 
                    #the path to the furthest food dot from pacman's position 
                    #using Chasles' relation
                    if chasles > maxChasles:
                        maxChasles = chasles #saves the maximum distance increase
                        res = dist[a] + manhattanDistance(foodPos[a], foodPos[furthestFoodIndex])
                        #the manhattan distance of the path that has the maximum 
                        #distance increase
                            
                        
            if res < len(foodPos): 
                res = len(foodPos) #the estimated path left will always be at least as 
                                   #big as the number of food left
                
        return 1 + res - getNumFood(state) # +1 to prevent: heuristic = 0
            
    def priorityFunction(n):
        """
        Given a pacman game state, returns the priority function of 
        the state (sum of the heuristic and the cost function)
        
        Arguments:
        ----------
        - `n`: a tuple containing the current game sate and the
        saved path 
        
        Return:
        -------
        - the priority function of the current game state
        """
        
        return PacmanAgent.costFunction(n) + PacmanAgent.heuristic(n)
    
    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        
        global initialNumFood
        initialNumFood = getNumFood(state) 
        
        path = []
        closed = set()
        fringeKeys = set(key(state)) #set of keys for the states that are 
                                     #currently in the fringe
        fringe = PriorityQueueWithFunction(PacmanAgent.priorityFunction)
        fringe.push((state, path))
        
        while True:
            if fringe.isEmpty():
                return []  # failure
                
            _, (current, path) = fringe.pop() #pops the priority value and a tuple 
                                              #with the current state, the 
                                              #resulting path and the corresponding 
                                              #set of closed keys
            if current.isWin():
                return path
                
            current_key = key(current) #the position corresponding to the current state
            fringeKeys.discard(current_key) #the state key is removed from fringeKeys as
                                            #it is about to be processed
            
            if current_key not in closed:
                closed.add(current_key)
                for next_state, action in current.generatePacmanSuccessors():
                    next_key = key(next_state)
                    if next_key not in fringeKeys:
                       fringeKeys.add(next_key) #next_key added to the list of future processed keys
                       fringe.push((next_state, path + [action]))
                
        return path