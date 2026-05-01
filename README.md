# Wumpus World - Dynamic Logic Agent Web App

A web-based Knowledge-Based Agent that navigates a Wumpus World-style grid using **Propositional Logic** and **Resolution Refutation** to deduce safe cells.

## 📋 Features

### 1. **Dynamic Environment**
- Customizable grid size (3×3 to 10×10)
- Randomly placed Wumpus and Pits at each game start
- Agent starts at position [0,0] which is always safe
- Dynamic percepts based on agent location

### 2. **Logic-Based Inference Engine**
- **Propositional Logic Knowledge Base**: Maintains rules about pit/wumpus locations
- **Resolution Refutation**: Automated proof by contradiction algorithm
- Converts clauses to CNF and resolves them to find contradictions
- Tracks inference steps for visualization

### 3. **Percept System**
- **Breeze**: Generated when agent is adjacent to a pit
- **Stench**: Generated when agent is adjacent to the wumpus
- Agent learns from percepts and updates its knowledge base

### 4. **Web-Based Visualization**
- Interactive grid with color-coded cells:
  - 🟢 **Green**: Safe cells (proven safe by logic)
  - ⚪ **Gray**: Unvisited cells (unknown)
  - 🔴 **Red**: Confirmed hazards (pits/wumpus)
  - 🟡 **Yellow**: Current agent position
  - 🔵 **Blue**: Cells with percepts (breeze/stench)
- Real-time metrics dashboard
- Current percepts display
- Safe moves suggestions

### 5. **Real-Time Metrics**
- **Inference Steps**: Total resolution operations performed
- **Moves Made**: Number of cells the agent has visited
- **Safe Cells**: Number of proven safe cells discovered
- **KB Clauses**: Size of the knowledge base
- **Current Percepts**: What the agent senses at its location

## 🎯 Game Objective

The agent must **find the gold (💰)** while avoiding pits and the wumpus using **Propositional Logic** and **Resolution Refutation**.

### Elements:
- **🤖 Agent**: Starts at [0,0], must navigate using logic
- **💰 Gold**: Treasure to find (placed randomly, not at start)
- **🐲 Wumpus**: Monster that kills if encountered
- **🕳️ Pits**: Bottomless pits that kill if fallen into
- **Percepts**: Breeze (near pit), Stench (near wumpus), **Glitter (on gold)**

### Win Condition:
- Agent finds the gold and returns to start (future enhancement)
- Currently: Agent finds gold anywhere on the grid

### Lose Conditions:
- Agent moves to a cell with pit or wumpus (not implemented in UI yet)

### Knowledge Base Rules
When the agent perceives something:
```
If breeze at [1,1]: At least one adjacent cell has a pit
  Rule: pit_0_1 OR pit_1_0 OR pit_1_2 OR pit_2_1

If stench at [1,1]: At least one adjacent cell has wumpus
  Rule: wumpus_0_1 OR wumpus_1_0 OR wumpus_1_2 OR wumpus_2_1

If no percepts at [1,1]: All adjacent cells are safe
  Rule: NOT pit_0_1, NOT pit_1_0, etc.
```

### Resolution Refutation Algorithm
To prove a cell is safe (e.g., [2,2]):
1. Add negation of query to KB: "pit_2_2 exists" (negation of "NOT pit_2_2")
2. Try to resolve all clause pairs
3. If we derive an **empty clause** → contradiction found → cell IS safe
4. Count each resolution operation as an inference step

## 📁 Project Structure

```
Wumpus agent/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── wumpus_agent.py        # Agent logic & game mechanics
│   ├── knowledge_base.py      # KB & Resolution Refutation
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Web interface
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- A modern web browser

### Installation & Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```

   You should see:
   ```
   Starting Wumpus Agent Server on http://localhost:5000
    * Running on http://localhost:5000
   ```

4. **Open the web interface:**
   - Open your browser and navigate to: `file:///path/to/frontend/index.html`
   - Or set up a simple HTTP server in the frontend directory:
     ```bash
     # In a new terminal, from frontend directory
     python -m http.server 8000
     # Then open: http://localhost:8000
     ```

## 🎮 How to Play

1. **Initialize Game:**
   - Set desired grid dimensions (3-10)
   - Click "Initialize Game"
   - The agent starts at [0,0] (always safe)

2. **Move the Agent:**
   - **Manual Move**: Click on adjacent gray (unvisited) cells
   - **Auto Move**: Let the agent automatically move to the next safe cell using logic
   - Click "Show Safe Moves" to see all logically safe adjacent cells

3. **Monitor:**
   - Watch the **Inference Steps** counter increase as the logic engine works
   - Current **Percepts** show if there's a breeze or stench
   - **Safe Cells** counter shows proven safe locations
   - **KB Clauses** shows knowledge base size

4. **Reset:**
   - Click "Reset Game" to start over with new hazard placements

## 💡 Understanding the Algorithm

### Resolution Refutation (Proof by Contradiction)

The agent uses a classical logic technique:

```
To prove: "Cell [2,2] is definitely safe (no pit and no wumpus)"

Steps:
1. Assume opposite: "Cell [2,2] has a pit" (add to KB)
2. Try to derive a contradiction
3. Apply resolution rule repeatedly:
   Clause A: (pit_2_2 OR other_stuff)
   Clause B: (NOT pit_2_2 OR more_stuff)
   Resolvent: (other_stuff OR more_stuff)
4. If we derive: empty clause (contradiction!)
   → The assumption is false
   → Cell [2,2] IS safe
```

### Why This Works

- **Sound**: Only proves things that are logically true
- **Complete**: If something can be proven, this algorithm will find it
- **Automated**: Runs without human input (except navigation)

## 📊 Example Walkthrough

```
Initial State:
- Grid: 5×5
- Agent at [0,0]
- No percepts (proves adjacent cells are safe)

Move 1: Agent moves to [0,1]
- Percept: BREEZE
- KB Rule: pit_0_0 OR pit_0_2 OR pit_1_1
- Inference: [0,0] is already safe, [0,2] and [1,1] suspicious

Move 2: Agent moves to [0,2]
- Percept: None
- KB Rule: All adjacent cells are safe
- Inference: Pit must be at [1,1] (from breeze in [0,1])
- Using resolution: Can now prove [0,2] and many others are definitely safe

Continue: Agent explores safely using logic to identify hazard locations
```

## 🔧 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/init` | POST | Initialize new game |
| `/api/grid` | GET | Get current grid state |
| `/api/move` | POST | Move agent to adjacent cell |
| `/api/auto-move` | POST | Auto-move to next safe cell |
| `/api/check-safe` | POST | Check if cell is safe (runs resolution) |
| `/api/safe-moves` | GET | Get list of safe adjacent cells |
| `/api/metrics` | GET | Get current metrics |
| `/api/reset` | POST | Reset game |
| `/api/status` | GET | Get game status |

## 📝 Code Highlights

### Easy-to-Understand Python
The code uses simple, readable patterns:

```python
# Adding a rule to KB
kb.add_clause(['pit_1_1', 'pit_1_2', 'pit_2_1'])  # Simple list

# Proving safety
is_safe, steps = kb.prove('NOT pit_1_1')  # Returns (bool, int)

# Getting agent info
metrics = agent.get_metrics()  # Simple dictionary
```

### Simple Resolution Algorithm
```python
def prove(self, query):
    # Add negation of query
    clauses.add(Clause([negate(query)]))
    
    # Keep resolving until we find contradiction
    while clauses_to_resolve:
        for each pair of clauses:
            if they have complementary literals:
                resolvent = resolve(clause1, clause2)
                if empty_clause: return True  # Proof found!
                clauses_to_resolve.add(resolvent)
    
    return False  # Can't prove
```

## 🎓 Learning Outcomes

By working with this project, you'll understand:
- **Propositional Logic**: How to represent knowledge with logical statements
- **CNF (Conjunctive Normal Form)**: How to convert rules to a standard format
- **Resolution**: A fundamental inference rule in automated reasoning
- **Knowledge-Based Agents**: How agents use logic to make decisions
- **Wumpus World**: A classic AI problem for testing agent intelligence

## ⚙️ Configuration

### Grid Sizes
- Minimum: 3×3 (basic exploration)
- Maximum: 10×10 (complex logic puzzles)
- Recommended: 5×5 or 7×7 (good balance)

### Difficulty
- **Fewer pits**: Easier to explore
- **More pits**: Requires more logical deduction
- **Pits near start**: Forces early complex reasoning

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure the Flask backend is running
- Check that port 5000 is not in use

### Frontend doesn't load
- Use a proper HTTP server, not just file:// protocol
- Check browser console for CORS errors
- Ensure `requirements.txt` is installed

### Incorrect safe move suggestions
- This is likely the inference engine working correctly
- The agent is being conservative (only moves to provably safe cells)
- More exploration = more KB rules = more provable safe cells

## 🔐 Safety Guarantee

The agent only moves to cells it can **logically prove** are safe using resolution refutation. This is more conservative than heuristic approaches but guarantees no dangerous moves based on current knowledge.

## 📚 References

- **Propositional Logic**: Russell & Norvig, "Artificial Intelligence: A Modern Approach"
- **Resolution Refutation**: Automated Reasoning and Theorem Proving
- **Wumpus World**: Classic AI problem from AIMA textbook

## 📄 License

Open for educational use.

---

**Enjoy exploring the Wumpus World with logic!** 🎮🤖✨
