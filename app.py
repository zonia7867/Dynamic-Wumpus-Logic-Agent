from flask import Flask, jsonify, request
from flask_cors import CORS
from wumpus_agent import WumpusAgent

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for frontend

# Global agent instance
agent = None

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({'status': 'Wumpus Agent Server is running!', 'port': 5000})

@app.route('/api/init', methods=['POST'])
def init_game():
    """Initialize a new game with given dimensions"""
    global agent
    
    data = request.json
    rows = data.get('rows', 5)
    cols = data.get('cols', 5)
    
    # Validate dimensions
    if rows < 3 or cols < 3 or rows > 10 or cols > 10:
        return jsonify({'error': 'Grid dimensions must be between 3x3 and 10x10'}), 400
    
    agent = WumpusAgent(rows, cols)
    
    return jsonify({
        'status': 'success',
        'message': f'Game initialized with {rows}x{cols} grid',
        'grid': agent.get_grid_state(),
        'metrics': agent.get_metrics()
    })

@app.route('/api/grid', methods=['GET'])
def get_grid():
    """Get current grid state"""
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    return jsonify({
        'grid': agent.get_grid_state(),
        'metrics': agent.get_metrics()
    })

@app.route('/api/move', methods=['POST'])
def manual_move():
    """Move agent to a specific cell"""
    global agent
    
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    data = request.json
    new_r = data.get('row')
    new_c = data.get('col')
    
    # Check if it's adjacent to current position
    curr_r, curr_c = agent.agent_pos
    if abs(new_r - curr_r) + abs(new_c - curr_c) != 1:
        return jsonify({'error': 'Can only move to adjacent cells'}), 400
    
    # Check if already visited
    if (new_r, new_c) in agent.visited_cells:
        return jsonify({'error': 'Cell already visited'}), 400
    
    percepts = agent.move(new_r, new_c)
    
    return jsonify({
        'status': 'success',
        'percepts': percepts,
        'grid': agent.get_grid_state(),
        'metrics': agent.get_metrics()
    })

@app.route('/api/auto-move', methods=['POST'])
def auto_move():
    """Automatically move agent to next safe cell"""
    global agent
    
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    success, next_pos, percepts = agent.auto_move()
    
    if success:
        return jsonify({
            'status': 'success',
            'moved': True,
            'new_position': next_pos,
            'percepts': percepts,
            'grid': agent.get_grid_state(),
            'metrics': agent.get_metrics()
        })
    else:
        return jsonify({
            'status': 'success',
            'moved': False,
            'message': 'No safe moves available',
            'grid': agent.get_grid_state(),
            'metrics': agent.get_metrics()
        })

@app.route('/api/check-safe', methods=['POST'])
def check_safe():
    """Check if a cell is safe using resolution refutation"""
    global agent
    
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    data = request.json
    r = data.get('row')
    c = data.get('col')
    
    is_safe, inference_steps = agent.is_safe(r, c)
    
    return jsonify({
        'row': r,
        'col': c,
        'is_safe': is_safe,
        'inference_steps': inference_steps
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get current game metrics"""
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    return jsonify(agent.get_metrics())

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get overall game status"""
    if agent is None:
        return jsonify({'initialized': False})
    
    return jsonify({
        'initialized': True,
        'grid_size': (agent.rows, agent.cols),
        'metrics': agent.get_metrics()
    })

@app.route('/api/safe-moves', methods=['GET'])
def get_safe_moves():
    """Get list of safe adjacent cells"""
    if agent is None:
        return jsonify({'error': 'Game not initialized'}), 400
    
    safe_moves = agent.get_safe_moves()
    
    return jsonify({
        'safe_moves': safe_moves,
        'count': len(safe_moves)
    })

@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game"""
    global agent
    
    data = request.json
    rows = data.get('rows', 5)
    cols = data.get('cols', 5)
    
    agent = WumpusAgent(rows, cols)
    
    return jsonify({
        'status': 'success',
        'message': 'Game reset',
        'grid': agent.get_grid_state(),
        'metrics': agent.get_metrics()
    })

if __name__ == '__main__':
    print("Starting Wumpus Agent Server on http://localhost:5000")
    app.run(debug=True, port=5000)
