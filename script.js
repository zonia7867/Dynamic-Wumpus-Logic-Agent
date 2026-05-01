// API Configuration
// Use environment variable if available, otherwise default based on hostname
const API_URL = (() => {
    // Check if we have a deployed backend URL
    if (typeof window !== 'undefined') {
        // For local development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:5000/api';
        }
        // For production - set via environment variable or check sessionStorage
        const deployedBackend = sessionStorage.getItem('BACKEND_URL');
        if (deployedBackend) {
            return deployedBackend + '/api';
        }
    }
    // Fallback
    return 'http://localhost:5000/api';
})();

// Game state
let gameState = {
    initialized: false,
    rows: 0,
    cols: 0,
    grid: [],
    metrics: {},
    winModalShown: false
};

// Initialize game
async function initGame() {
    const rows = parseInt(document.getElementById('gridRows').value);
    const cols = parseInt(document.getElementById('gridCols').value);

    if (rows < 3 || rows > 10 || cols < 3 || cols > 10) {
        updateStatus('Error: Grid size must be between 3x3 and 10x10', 'error');
        return;
    }

    try {
        updateStatus('Initializing game...', 'info');
        
        const response = await fetch(`${API_URL}/init`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rows, cols })
        });

        const data = await response.json();
        
        if (!response.ok) {
            updateStatus('Error: ' + data.error, 'error');
            return;
        }

        gameState.initialized = true;
        gameState.rows = rows;
        gameState.cols = cols;
        gameState.grid = data.grid;
        gameState.metrics = data.metrics;
        gameState.winModalShown = false;

        renderGrid();
        updateMetrics();
        updateStatus(`Game initialized! ${rows}x${cols} grid ready.`, 'success');
        
    } catch (error) {
        updateStatus('Error: ' + error.message, 'error');
        console.error('Init error:', error);
    }
}

// Reset game
async function resetGame() {
    const rows = parseInt(document.getElementById('gridRows').value);
    const cols = parseInt(document.getElementById('gridCols').value);

    try {
        updateStatus('Resetting game...', 'info');
        
        const response = await fetch(`${API_URL}/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rows, cols })
        });

        const data = await response.json();
        
        gameState.grid = data.grid;
        gameState.metrics = data.metrics;

        renderGrid();
        updateMetrics();
        updateStatus('Game reset!', 'success');
        
    } catch (error) {
        updateStatus('Error: ' + error.message, 'error');
        console.error('Reset error:', error);
    }
}

// Move to a cell
async function moveToCell(row, col) {
    if (!gameState.initialized) {
        updateStatus('Error: Game not initialized', 'error');
        return;
    }

    // Check if cell is unvisited
    const cell = gameState.grid[row][col];
    if (cell.visited) {
        updateStatus('Error: Cell already visited', 'error');
        return;
    }

    try {
        updateStatus('Moving to cell...', 'info');
        
        const response = await fetch(`${API_URL}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ row, col })
        });

        const data = await response.json();
        
        if (!response.ok) {
            updateStatus('Error: ' + data.error, 'error');
            return;
        }

        gameState.grid = data.grid;
        gameState.metrics = data.metrics;

        renderGrid();
        updateMetrics();
        
        const perceptText = data.percepts.length > 0 ? data.percepts.join(', ') : 'None (Safe)';
        updateStatus(`Moved to [${row}, ${col}]. Percepts: ${perceptText}`, 'success');
        
    } catch (error) {
        updateStatus('Error: ' + error.message, 'error');
        console.error('Move error:', error);
    }
}

// Auto move to next safe cell
async function autoMove() {
    if (!gameState.initialized) {
        updateStatus('Error: Game not initialized', 'error');
        return;
    }

    updateStatus('Auto-exploring...', 'info');
    
    let moves = 0;
    const maxMoves = 50; // Prevent infinite loops
    
    while (moves < maxMoves) {
        const response = await fetch(`${API_URL}/auto-move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        gameState.grid = data.grid;
        gameState.metrics = data.metrics;

        renderGrid();
        updateMetrics();

        if (data.moved) {
            const perceptText = data.percepts.length > 0 ? data.percepts.join(', ') : 'None (Safe)';
            updateStatus(`Auto-move ${moves + 1}: [${data.new_position[0]}, ${data.new_position[1]}] - ${perceptText}`, 'info');
            
            // Check if game is won
            if (gameState.metrics.game_won) {
                updateStatus('🎉 GOLD FOUND! Game won!', 'success');
                break;
            }
            
            moves++;
            // Small delay for visualization
            await new Promise(resolve => setTimeout(resolve, 500));
        } else {
            updateStatus('No more safe moves available. Exploration complete.', 'warning');
            break;
        }
    }
    
    if (moves >= maxMoves) {
        updateStatus('Auto-exploration stopped (max moves reached)', 'warning');
    }
}

// Show safe moves
async function showSafeMoves() {
    if (!gameState.initialized) {
        updateStatus('Error: Game not initialized', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/safe-moves`, {
            method: 'GET'
        });

        const data = await response.json();

        const safeMovesList = document.getElementById('safeMovesList');
        
        if (data.count === 0) {
            safeMovesList.innerHTML = '<p class="info-text">No safe moves available</p>';
        } else {
            let html = '';
            data.safe_moves.forEach(move => {
                html += `<div class="safe-move-item">[${move[0]}, ${move[1]}]</div>`;
            });
            safeMovesList.innerHTML = html;
        }

        updateStatus(`Found ${data.count} safe adjacent cells`, 'info');
        
    } catch (error) {
        updateStatus('Error: ' + error.message, 'error');
        console.error('Safe moves error:', error);
    }
}

// Render the game grid
function renderGrid() {
    const gameGridDiv = document.getElementById('gameGrid');
    gameGridDiv.innerHTML = '';

    const gridStyle = `grid-template-columns: repeat(${gameState.cols}, 50px);`;
    gameGridDiv.style.cssText = gridStyle;

    for (let r = 0; r < gameState.rows; r++) {
        for (let c = 0; c < gameState.cols; c++) {
            const cell = gameState.grid[r][c];
            const cellDiv = document.createElement('div');
            cellDiv.className = 'grid-cell';

            let cellClass = '';
            let cellContent = '';

            if (cell.is_agent) {
                cellClass = 'cell-agent';
                cellContent = '🤖';
                if (cell.has_gold) {
                    cellContent = '🤖💰';  // Agent with gold
                }
            } else if (!cell.visited) {
                cellClass = 'cell-unvisited';
                cellContent = '?';
            } else if (cell.safe) {
                if (cell.glitter) {
                    cellClass = 'cell-gold';
                    cellContent = '💰';  // Gold found
                } else if (cell.breeze || cell.stench) {
                    cellClass = 'cell-breeze-stench';
                    cellContent = cell.breeze && cell.stench ? '💨🔥' : (cell.breeze ? '💨' : '🔥');
                } else {
                    cellClass = 'cell-safe';
                    cellContent = '✓';
                }
            }

            if (cellClass) {
                cellClass.split(' ').forEach(cls => {
                    if (cls.trim()) {
                        cellDiv.classList.add(cls);
                    }
                });
            }
            cellDiv.textContent = cellContent;
            cellDiv.title = `[${r}, ${c}]`;

            // Add click handler for unvisited cells
            if (!cell.visited && !cell.is_agent) {
                cellDiv.addEventListener('click', () => moveToCell(r, c));
                cellDiv.style.cursor = 'pointer';
            }

            gameGridDiv.appendChild(cellDiv);
        }
    }
}

// Update metrics display
function updateMetrics() {
    const metrics = gameState.metrics;

    document.getElementById('agentPos').textContent = `[${metrics.agent_position[0]}, ${metrics.agent_position[1]}]`;
    document.getElementById('moveCount').textContent = metrics.moves_made;
    document.getElementById('inferenceCount').textContent = metrics.total_inferences;
    document.getElementById('safeCellCount').textContent = metrics.num_safe_cells;
    document.getElementById('visitedCount').textContent = metrics.visited_cells;
    document.getElementById('clauseCount').textContent = metrics.num_clauses_in_kb;
    document.getElementById('gameStatus').textContent = metrics.game_won ? 'WON! 🎉' : (metrics.has_gold ? 'Has Gold' : 'Exploring');

    // Update percepts
    const perceptsList = document.getElementById('perceptsList');
    if (metrics.current_percepts && metrics.current_percepts.length > 0) {
        let html = '';
        metrics.current_percepts.forEach(percept => {
            const icon = percept === 'breeze' ? '💨' : (percept === 'stench' ? '🔥' : '✨');
            html += `<span class="percept-item">${icon} ${percept.toUpperCase()}</span>`;
        });
        perceptsList.innerHTML = html;
    } else {
        perceptsList.innerHTML = '<span class="percept-none">None (Safe)</span>';
    }
    
    // Check for game win condition
    if (metrics.game_won && !gameState.winModalShown) {
        gameState.winModalShown = true;
        showGameOverModal(true);
    }
}

// Update status message
function updateStatus(message, type = 'info') {
    const statusBar = document.getElementById('statusMessage');
    statusBar.textContent = message;
    
    // Add color styling based on type
    statusBar.style.color = '';
    if (type === 'error') {
        statusBar.style.color = '#dc2626';
    } else if (type === 'success') {
        statusBar.style.color = '#16a34a';
    } else if (type === 'warning') {
        statusBar.style.color = '#ea580c';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btnInit').addEventListener('click', initGame);
    document.getElementById('btnReset').addEventListener('click', resetGame);
    document.getElementById('btnAutoMove').addEventListener('click', autoMove);
    document.getElementById('btnGetSafeMoves').addEventListener('click', showSafeMoves);

    updateStatus('Ready to start. Set grid dimensions and click "Initialize Game".', 'info');
});

// Modal functions
function showGameOverModal(isWin) {
    const modal = document.getElementById('gameOverModal');
    const titleEl = document.getElementById('modalTitle');
    const messageEl = document.getElementById('modalMessage');
    
    if (isWin) {
        titleEl.textContent = '🎉 You Win!';
        titleEl.className = 'modal-title win';
        messageEl.textContent = 'Congratulations! You found the gold and used logic to avoid all hazards!';
    } else {
        titleEl.textContent = '💀 Game Over';
        titleEl.className = 'modal-title lose';
        messageEl.textContent = 'You hit a pit or the wumpus! Use better logic next time.';
    }
    
    // Update stats
    document.getElementById('finalMoves').textContent = gameState.metrics.moves_made;
    document.getElementById('finalInferences').textContent = gameState.metrics.total_inferences;
    document.getElementById('finalSafeCells').textContent = gameState.metrics.num_safe_cells;
    
    modal.classList.add('show');
}

function closeModal() {
    const modal = document.getElementById('gameOverModal');
    modal.classList.remove('show');
}

function newGame() {
    closeModal();
    initGame();
}

// Config Modal functions
function showConfigModal() {
    const modal = document.getElementById('configModal');
    const input = document.getElementById('configBackendUrl');
    
    // Load saved URL if any
    const saved = sessionStorage.getItem('BACKEND_URL');
    if (saved) {
        input.value = saved;
    }
    
    modal.classList.add('show');
}

function closeConfigModal() {
    const modal = document.getElementById('configModal');
    modal.classList.remove('show');
}

function saveBackendConfig() {
    const url = document.getElementById('configBackendUrl').value.trim();
    
    if (url) {
        sessionStorage.setItem('BACKEND_URL', url);
        updateStatus('✅ Backend URL saved! Reload page to use new URL.', 'success');
    } else {
        sessionStorage.removeItem('BACKEND_URL');
        updateStatus('✅ Using default backend (localhost:5000)', 'success');
    }
    
    closeConfigModal();
}
