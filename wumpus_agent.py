import random
from knowledge_base import KnowledgeBase

class WumpusAgent:
    """Dynamic Wumpus World Agent with Logic-Based Navigation"""
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.kb = KnowledgeBase()
        
        # Initialize grid state
        self.grid = [[{'type': 'empty', 'visited': False, 'safe': False, 'breeze': False, 'stench': False, 'glitter': False} 
                      for _ in range(cols)] for _ in range(rows)]
        
        # Place hazards randomly
        self.pit_positions = set()
        self.wumpus_position = None
        self.gold_position = None
        self.place_hazards()
        
        # Agent position
        self.agent_pos = (0, 0)
        self.visited_cells = set()
        self.visited_cells.add(self.agent_pos)
        
        # Game state
        self.has_gold = False
        self.game_won = False
        
        # Metrics
        self.total_inferences = 0
        self.moves_made = 0
        
        # Initialize KB with starting position being safe
        self.mark_safe(0, 0)
    
    def place_hazards(self):
        """Randomly place wumpus, pits, and gold (not at start position 0,0)"""
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        safe_cells = [(0, 0)]  # Start position is always safe
        available_cells = [cell for cell in all_cells if cell not in safe_cells]
        
        # Place wumpus
        self.wumpus_position = random.choice(available_cells)
        available_cells.remove(self.wumpus_position)
        
        # Place gold (not too close to start)
        far_cells = [(r, c) for r, c in available_cells if abs(r) + abs(c) >= 2]
        if far_cells:
            self.gold_position = random.choice(far_cells)
            available_cells.remove(self.gold_position)
        else:
            self.gold_position = random.choice(available_cells)
            available_cells.remove(self.gold_position)
        
        # Place 3-5 pits
        num_pits = random.randint(3, min(5, len(available_cells)))
        self.pit_positions = set(random.sample(available_cells, num_pits))
        
        # Update grid with hazard info (for backend knowledge)
        for r, c in self.pit_positions:
            self.grid[r][c]['type'] = 'pit'
        self.grid[self.wumpus_position[0]][self.wumpus_position[1]]['type'] = 'wumpus'
        self.grid[self.gold_position[0]][self.gold_position[1]]['type'] = 'gold'
    
    def get_adjacent_cells(self, r, c):
        """Get all adjacent cells (up, down, left, right)"""
        adjacent = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adjacent.append((nr, nc))
        return adjacent
    
    def perceive(self, r, c):
        """Get percepts at current position"""
        percepts = []
        
        # Check for breeze (adjacent to pit)
        has_breeze = any((nr, nc) in self.pit_positions for nr, nc in self.get_adjacent_cells(r, c))
        if has_breeze:
            percepts.append('breeze')
            self.grid[r][c]['breeze'] = True
        
        # Check for stench (adjacent to wumpus)
        has_stench = any((nr, nc) == self.wumpus_position for nr, nc in self.get_adjacent_cells(r, c))
        if has_stench:
            percepts.append('stench')
            self.grid[r][c]['stench'] = True
        
        # Check for glitter (on gold)
        if (r, c) == self.gold_position:
            percepts.append('glitter')
            self.grid[r][c]['glitter'] = True
        
        return percepts
    
    def add_percept_rules(self, r, c, percepts):
        """Add rules to KB based on percepts"""
        # If no percepts, all adjacent cells are safe
        if not percepts:
            for nr, nc in self.get_adjacent_cells(r, c):
                self.kb.add_clause([f"NOT pit_{nr}_{nc}", f"NOT wumpus_{nr}_{nc}"])
        else:
            # If breeze, at least one adjacent cell has a pit
            if 'breeze' in percepts:
                adjacent = self.get_adjacent_cells(r, c)
                pit_literals = [f"pit_{nr}_{nc}" for nr, nc in adjacent]
                self.kb.add_clause(pit_literals)
            
            # If stench, at least one adjacent cell has wumpus
            if 'stench' in percepts:
                adjacent = self.get_adjacent_cells(r, c)
                wumpus_literals = [f"wumpus_{nr}_{nc}" for nr, nc in adjacent]
                self.kb.add_clause(wumpus_literals)
    
    def is_safe(self, r, c):
        """
        Check if a cell is safe using Resolution Refutation
        Returns (is_safe, inference_steps)
        """
        # Query: Can we prove the cell is safe (no pit and no wumpus)?
        query = f"NOT pit_{r}_{c}"
        is_pit_free, steps1 = self.kb.prove(query)
        
        query = f"NOT wumpus_{r}_{c}"
        is_wumpus_free, steps2 = self.kb.prove(query)
        
        total_steps = steps1 + steps2
        self.total_inferences += total_steps
        
        # Cell is safe if we can prove both pit-free AND wumpus-free
        is_definitely_safe = is_pit_free and is_wumpus_free
        
        return is_definitely_safe, total_steps
    
    def mark_safe(self, r, c):
        """Mark a cell as definitely safe"""
        self.grid[r][c]['safe'] = True
        self.grid[r][c]['visited'] = True
    
    def get_safe_moves(self):
        """Get list of safe adjacent unvisited cells"""
        r, c = self.agent_pos
        adjacent = self.get_adjacent_cells(r, c)
        safe_moves = []
        
        for nr, nc in adjacent:
            if (nr, nc) not in self.visited_cells:
                is_safe, _ = self.is_safe(nr, nc)
                if is_safe:
                    safe_moves.append((nr, nc))
        
        return safe_moves
    
    def move(self, new_r, new_c):
        """Move agent to new position and perceive"""
        if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
            self.agent_pos = (new_r, new_c)
            self.visited_cells.add(self.agent_pos)
            self.moves_made += 1
            
            # Check for gold
            if self.agent_pos == self.gold_position and not self.has_gold:
                self.has_gold = True
                self.game_won = True
            
            # Perceive at new location
            percepts = self.perceive(new_r, new_c)
            self.add_percept_rules(new_r, new_c, percepts)
            self.mark_safe(new_r, new_c)
            
            return percepts
        return []
    
    def auto_move(self):
        """Automatically move to next safe cell if available"""
        safe_moves = self.get_safe_moves()
        
        if safe_moves:
            next_pos = safe_moves[0]  # Move to first safe cell
            percepts = self.move(next_pos[0], next_pos[1])
            return True, next_pos, percepts
        else:
            return False, None, []
    
    def get_grid_state(self):
        """Return current grid state for visualization"""
        grid_state = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                cell_info = {
                    'row': r,
                    'col': c,
                    'visited': (r, c) in self.visited_cells,
                    'safe': self.grid[r][c]['safe'],
                    'breeze': self.grid[r][c]['breeze'],
                    'stench': self.grid[r][c]['stench'],
                    'glitter': self.grid[r][c]['glitter'],
                    'is_agent': self.agent_pos == (r, c),
                    'has_gold': self.has_gold and self.agent_pos == (r, c)
                }
                row.append(cell_info)
            grid_state.append(row)
        return grid_state
    
    def get_metrics(self):
        """Return metrics for dashboard"""
        r, c = self.agent_pos
        percepts = []
        if self.grid[r][c]['breeze']:
            percepts.append('breeze')
        if self.grid[r][c]['stench']:
            percepts.append('stench')
        if self.grid[r][c]['glitter']:
            percepts.append('glitter')
        
        return {
            'agent_position': self.agent_pos,
            'moves_made': self.moves_made,
            'total_inferences': self.total_inferences,
            'current_percepts': percepts,
            'visited_cells': len(self.visited_cells),
            'num_safe_cells': sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c]['safe']),
            'num_clauses_in_kb': len(self.kb.clauses),
            'has_gold': self.has_gold,
            'game_won': self.game_won
        }
    
    def reset(self, rows, cols):
        """Reset the game with new dimensions"""
        self.__init__(rows, cols)
