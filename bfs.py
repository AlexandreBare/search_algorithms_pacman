from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueueWithFunction
from pacman_module.util import manhattanDistance

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
        	self.moves = self.bfs(state)
            

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP
    
    def costFunction(n):
        """
        Returns the cost of the action leading to the given state. The cost is equal to 
        the current path length plus one.
        
        Arguments:
        ----------
        - `n`: a tuple containing the current game sate and the
        saved path 
        
        Return:
        -------
        - the cost of the action leading to the current game state
        """
        
        path = n[1]
        return 1 + len(path)
        
    def heuristic(n):
        """
        Returns the heuristic of the given state. Heuristic = 0 for all n						
        
        Arguments:
        ----------
        - `n`: a tuple containing the current game sate and the
        saved path 
        
        Return:
        -------
        - the heuristic of the current game state
        """
        return 0
        
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

        return (PacmanAgent.costFunction(n) + PacmanAgent.heuristic(n))
        
    def bfs(self, state):
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