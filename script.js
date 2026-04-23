// ============================
// N-Queens Visualizer
// Brute Force vs Backtracking
// ============================

// --- State ---
let N = 5;
let speed = 50;
let algorithm = 'backtracking';
let isRunning = false;
let shouldStop = false;
let steps = 0;
let backtracks = 0;
let queensPlaced = 0;
let startTime = 0;
let timerInterval = null;

// Results storage for comparison
const results = {
    backtracking: null,
    bruteforce: null
};

// --- DOM Elements ---
const boardEl = document.getElementById('chessboard');
const boardSizeSlider = document.getElementById('board-size');
const boardSizeValue = document.getElementById('board-size-value');
const speedSlider = document.getElementById('speed');
const speedValue = document.getElementById('speed-value');
const btnStart = document.getElementById('btn-start');
const btnReset = document.getElementById('btn-reset');
const statusBadge = document.getElementById('status-badge');
const boardTitle = document.getElementById('board-title');
const logContainer = document.getElementById('log-container');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    boardSizeSlider.addEventListener('input', (e) => {
        N = parseInt(e.target.value);
        boardSizeValue.textContent = N;
        boardTitle.textContent = `♛ Papan Catur ${N}×${N}`;
        if (!isRunning) createBoard();
    });

    speedSlider.addEventListener('input', (e) => {
        speed = parseInt(e.target.value);
        speedValue.textContent = speed;
    });

    createBoard();
    updateExplanation();
});

// --- Board Creation ---
function createBoard() {
    boardEl.innerHTML = '';
    boardEl.style.gridTemplateColumns = `repeat(${N}, 1fr)`;

    // Responsive cell size
    const maxBoardWidth = Math.min(500, window.innerWidth - 80);
    const cellSize = Math.floor(maxBoardWidth / N);

    for (let row = 0; row < N; row++) {
        for (let col = 0; col < N; col++) {
            const cell = document.createElement('div');
            cell.className = `cell ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
            cell.id = `cell-${row}-${col}`;
            cell.style.width = `${cellSize}px`;
            cell.style.height = `${cellSize}px`;
            cell.dataset.row = row;
            cell.dataset.col = col;
            boardEl.appendChild(cell);
        }
    }
}

// --- Algorithm Selection ---
function selectAlgorithm(algo) {
    if (isRunning) return;
    algorithm = algo;

    document.getElementById('btn-backtracking').classList.toggle('active', algo === 'backtracking');
    document.getElementById('btn-bruteforce').classList.toggle('active', algo === 'bruteforce');

    updateExplanation();
}

function updateExplanation() {
    const titleEl = document.getElementById('explanation-title');
    const contentEl = document.getElementById('explanation-content');

    if (algorithm === 'backtracking') {
        titleEl.textContent = '🧠 Algoritma Backtracking';
        contentEl.innerHTML = `
            <div class="explanation-text">
                <h3>Cara Kerja:</h3>
                <ol>
                    <li><strong>Tempatkan ratu</strong> di kolom pertama baris saat ini</li>
                    <li><strong>Cek</strong> apakah posisi aman (tidak konflik dengan ratu lain)</li>
                    <li>Jika <strong>aman</strong> → lanjut ke baris berikutnya</li>
                    <li>Jika <strong>tidak aman</strong> → coba kolom berikutnya</li>
                    <li>Jika <strong>semua kolom gagal</strong> → <span class="highlight-backtrack">BACKTRACK!</span> (mundur ke baris sebelumnya)</li>
                    <li>Ulangi sampai semua N ratu berhasil ditempatkan</li>
                </ol>
                <p style="margin-top: 14px; font-size: 0.85rem; color: var(--text-muted);">
                    <strong style="color: var(--accent-green);">Keunggulan:</strong> Pruning — langsung melewati cabang yang pasti gagal, sehingga jauh lebih cepat dari Brute Force.
                </p>
            </div>
            <div class="explanation-visual">
                <div class="complexity-box">
                    <h4>Kompleksitas</h4>
                    <div class="complexity-item">
                        <span class="complexity-label">Waktu (Worst)</span>
                        <span class="complexity-value">O(N!)</span>
                    </div>
                    <div class="complexity-item">
                        <span class="complexity-label">Ruang</span>
                        <span class="complexity-value">O(N)</span>
                    </div>
                    <div class="complexity-item">
                        <span class="complexity-label">Pruning</span>
                        <span class="complexity-value highlight-yes">Ya ✓</span>
                    </div>
                </div>
            </div>
        `;
    } else {
        titleEl.textContent = '💪 Algoritma Brute Force';
        contentEl.innerHTML = `
            <div class="explanation-text">
                <h3>Cara Kerja:</h3>
                <ol>
                    <li><strong>Generate semua permutasi</strong> penempatan N ratu (satu per baris)</li>
                    <li>Untuk setiap permutasi, <strong>tempatkan ratu</strong> di papan</li>
                    <li><strong>Cek apakah valid</strong> — tidak ada ratu saling menyerang</li>
                    <li>Jika valid → <strong>solusi ditemukan!</strong></li>
                    <li>Jika tidak → <strong>coba permutasi berikutnya</strong></li>
                    <li>Total permutasi yang dicek: <strong>N!</strong> kemungkinan</li>
                </ol>
                <p style="margin-top: 14px; font-size: 0.85rem; color: var(--text-muted);">
                    <strong style="color: var(--accent-amber);">Kelemahan:</strong> Tidak ada pruning — semua kemungkinan dicoba satu per satu, bahkan yang jelas-jelas gagal.
                </p>
            </div>
            <div class="explanation-visual">
                <div class="complexity-box">
                    <h4>Kompleksitas</h4>
                    <div class="complexity-item">
                        <span class="complexity-label">Waktu</span>
                        <span class="complexity-value">O(N! × N)</span>
                    </div>
                    <div class="complexity-item">
                        <span class="complexity-label">Ruang</span>
                        <span class="complexity-value">O(N)</span>
                    </div>
                    <div class="complexity-item">
                        <span class="complexity-label">Pruning</span>
                        <span class="complexity-value highlight-no">Tidak ✗</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// --- Utility Functions ---
function getDelay() {
    // Map speed 1-100 to delay 800ms - 5ms
    return Math.max(5, 800 - (speed - 1) * 8);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getCell(row, col) {
    return document.getElementById(`cell-${row}-${col}`);
}

function clearCellStates() {
    document.querySelectorAll('.cell').forEach(cell => {
        cell.className = cell.className.replace(/safe|conflict|trying|queen-placed|attack-zone/g, '').trim();
        cell.innerHTML = '';
    });
}

function resetCellHighlights() {
    document.querySelectorAll('.cell').forEach(cell => {
        cell.classList.remove('safe', 'conflict', 'trying', 'attack-zone');
    });
}

// --- Queen Placement Visual ---
function placeQueenVisual(row, col) {
    const cell = getCell(row, col);
    cell.classList.add('queen-placed');
    const queen = document.createElement('span');
    queen.className = 'queen-icon';
    queen.textContent = '♛';
    cell.innerHTML = '';
    cell.appendChild(queen);
}

function removeQueenVisual(row, col) {
    const cell = getCell(row, col);
    const queen = cell.querySelector('.queen-icon');
    if (queen) {
        queen.classList.add('removing');
        setTimeout(() => {
            cell.innerHTML = '';
            cell.classList.remove('queen-placed');
        }, 200);
    } else {
        cell.innerHTML = '';
        cell.classList.remove('queen-placed');
    }
}

function highlightAttackZones(queens) {
    // Reset previous attack zones
    document.querySelectorAll('.attack-zone').forEach(c => c.classList.remove('attack-zone'));

    for (const [qr, qc] of queens) {
        // Highlight row, col, diagonals
        for (let i = 0; i < N; i++) {
            if (i !== qc) getCell(qr, i)?.classList.add('attack-zone');
            if (i !== qr) getCell(i, qc)?.classList.add('attack-zone');
        }
        for (let d = 1; d < N; d++) {
            if (qr + d < N && qc + d < N) getCell(qr + d, qc + d)?.classList.add('attack-zone');
            if (qr + d < N && qc - d >= 0) getCell(qr + d, qc - d)?.classList.add('attack-zone');
            if (qr - d >= 0 && qc + d < N) getCell(qr - d, qc + d)?.classList.add('attack-zone');
            if (qr - d >= 0 && qc - d >= 0) getCell(qr - d, qc - d)?.classList.add('attack-zone');
        }
    }
}

// --- Logging ---
function addLog(message, type = '') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${steps}] ${message}`;
    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;

    // Keep max 500 entries
    while (logContainer.children.length > 500) {
        logContainer.removeChild(logContainer.firstChild);
    }
}

function clearLog() {
    logContainer.innerHTML = '';
}

// --- Stats Update ---
function updateStats() {
    document.getElementById('steps-count').textContent = steps.toLocaleString();
    document.getElementById('backtracks-count').textContent = backtracks.toLocaleString();
    document.getElementById('queens-count').textContent = queensPlaced;
}

function startTimer() {
    startTime = performance.now();
    timerInterval = setInterval(() => {
        const elapsed = performance.now() - startTime;
        document.getElementById('time-elapsed').textContent = formatTime(elapsed);
    }, 50);
}

function stopTimer() {
    if (timerInterval) clearInterval(timerInterval);
    const elapsed = performance.now() - startTime;
    document.getElementById('time-elapsed').textContent = formatTime(elapsed);
    return elapsed;
}

function formatTime(ms) {
    if (ms < 1000) return `${Math.round(ms)} ms`;
    return `${(ms / 1000).toFixed(2)} s`;
}

// --- Safety Check (is position safe for queen) ---
function isSafe(board, row, col) {
    // Check column
    for (let i = 0; i < row; i++) {
        if (board[i] === col) return false;
    }

    // Check upper-left diagonal
    for (let i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
        if (board[i] === j) return false;
    }

    // Check upper-right diagonal
    for (let i = row - 1, j = col + 1; i >= 0 && j < N; i--, j++) {
        if (board[i] === j) return false;
    }

    return true;
}

// --- Check if a complete arrangement is valid (for Brute Force) ---
function isValidArrangement(perm) {
    for (let i = 0; i < perm.length; i++) {
        for (let j = i + 1; j < perm.length; j++) {
            // Same column (impossible with permutation) or same diagonal
            if (Math.abs(perm[i] - perm[j]) === Math.abs(i - j)) {
                return false;
            }
        }
    }
    return true;
}

// ============================
// BACKTRACKING ALGORITHM
// ============================
async function solveBacktracking() {
    const board = new Array(N).fill(-1);
    const found = await backtrack(board, 0);

    if (!found && !shouldStop) {
        setStatus('Tidak ada solusi', 'failed');
        addLog(`Tidak ditemukan solusi untuk ${N}-Queens`, 'log-conflict');
    }

    return found;
}

async function backtrack(board, row) {
    if (shouldStop) return false;

    if (row === N) {
        // All queens placed! Solution found.
        setStatus('Solusi Ditemukan! ✓', 'solved');
        addLog(`🎉 SOLUSI DITEMUKAN! Penempatan: [${board.join(', ')}]`, 'log-solution');
        return true;
    }

    for (let col = 0; col < N; col++) {
        if (shouldStop) return false;

        steps++;
        updateStats();

        // Highlight trying
        const cell = getCell(row, col);
        cell.classList.add('trying');
        addLog(`Mencoba ratu di baris ${row + 1}, kolom ${col + 1}`, 'log-try');

        await sleep(getDelay());

        if (isSafe(board, row, col)) {
            // Place queen
            board[row] = col;
            queensPlaced++;
            updateStats();

            cell.classList.remove('trying');
            placeQueenVisual(row, col);

            // Show attack zones
            const queens = [];
            for (let i = 0; i <= row; i++) {
                if (board[i] !== -1) queens.push([i, board[i]]);
            }
            highlightAttackZones(queens);

            addLog(`✓ Ratu ditempatkan di baris ${row + 1}, kolom ${col + 1} (aman)`, 'log-place');

            await sleep(getDelay());

            // Recurse
            if (await backtrack(board, row + 1)) {
                return true;
            }

            // Backtrack
            if (shouldStop) return false;

            backtracks++;
            board[row] = -1;
            queensPlaced--;
            updateStats();

            removeQueenVisual(row, col);
            addLog(`↩ BACKTRACK dari baris ${row + 1}, kolom ${col + 1}`, 'log-backtrack');

            await sleep(getDelay() / 2);

            // Recalculate attack zones
            const remainingQueens = [];
            for (let i = 0; i < row; i++) {
                if (board[i] !== -1) remainingQueens.push([i, board[i]]);
            }
            if (remainingQueens.length > 0) {
                highlightAttackZones(remainingQueens);
            } else {
                document.querySelectorAll('.attack-zone').forEach(c => c.classList.remove('attack-zone'));
            }
        } else {
            // Conflict
            cell.classList.remove('trying');
            cell.classList.add('conflict');
            addLog(`✗ Konflik di baris ${row + 1}, kolom ${col + 1}`, 'log-conflict');

            await sleep(getDelay() / 2);
            cell.classList.remove('conflict');
        }
    }

    return false;
}

// ============================
// BRUTE FORCE ALGORITHM
// ============================
async function solveBruteForce() {
    const perm = [];
    for (let i = 0; i < N; i++) perm.push(i);

    addLog(`Brute Force: menggenerate semua ${factorial(N)} permutasi...`, 'log-info');

    const found = await tryPermutations(perm, 0);

    if (!found && !shouldStop) {
        setStatus('Tidak ada solusi', 'failed');
        addLog(`Tidak ditemukan solusi untuk ${N}-Queens`, 'log-conflict');
    }

    return found;
}

function factorial(n) {
    let result = 1;
    for (let i = 2; i <= n; i++) result *= i;
    return result;
}

async function tryPermutations(arr, start) {
    if (shouldStop) return false;

    if (start === arr.length) {
        steps++;
        updateStats();

        // Clear previous visualization
        clearCellStates();

        // Place all queens for this permutation
        addLog(`Mencoba permutasi: [${arr.join(', ')}]`, 'log-try');

        for (let row = 0; row < N; row++) {
            if (shouldStop) return false;
            const cell = getCell(row, arr[row]);
            cell.classList.add('trying');
            placeQueenVisual(row, arr[row]);
            queensPlaced = row + 1;
            updateStats();
            await sleep(getDelay() / N);
        }

        await sleep(getDelay());

        // Check if valid
        if (isValidArrangement(arr)) {
            // Mark all queens as safe
            for (let row = 0; row < N; row++) {
                getCell(row, arr[row]).classList.remove('trying');
                getCell(row, arr[row]).classList.add('queen-placed');
            }
            setStatus('Solusi Ditemukan! ✓', 'solved');
            addLog(`🎉 SOLUSI DITEMUKAN! Penempatan: [${arr.join(', ')}]`, 'log-solution');
            return true;
        } else {
            backtracks++;
            updateStats();

            // Find conflicting queens
            for (let i = 0; i < arr.length; i++) {
                for (let j = i + 1; j < arr.length; j++) {
                    if (Math.abs(arr[i] - arr[j]) === Math.abs(i - j)) {
                        getCell(i, arr[i]).classList.add('conflict');
                        getCell(j, arr[j]).classList.add('conflict');
                    }
                }
            }

            addLog(`✗ Permutasi [${arr.join(', ')}] gagal — ada konflik diagonal`, 'log-conflict');
            await sleep(getDelay() / 2);

            // Clear for next try
            clearCellStates();
            queensPlaced = 0;
            updateStats();
        }

        return false;
    }

    for (let i = start; i < arr.length; i++) {
        if (shouldStop) return false;

        // Swap
        [arr[start], arr[i]] = [arr[i], arr[start]];

        if (await tryPermutations(arr, start + 1)) {
            return true;
        }

        // Swap back
        [arr[start], arr[i]] = [arr[i], arr[start]];
    }

    return false;
}

// ============================
// CONTROL FUNCTIONS
// ============================
function setStatus(text, cls) {
    statusBadge.textContent = text;
    statusBadge.className = `status-badge ${cls || ''}`;
}

async function startVisualization() {
    if (isRunning) return;

    isRunning = true;
    shouldStop = false;
    steps = 0;
    backtracks = 0;
    queensPlaced = 0;

    btnStart.disabled = true;
    btnStart.innerHTML = '<span>⏳</span> Menjalankan...';
    boardSizeSlider.disabled = true;

    createBoard();
    clearLog();
    updateStats();
    setStatus('Menjalankan...', 'running');

    addLog(`Memulai ${algorithm === 'backtracking' ? 'Backtracking' : 'Brute Force'} untuk ${N}-Queens`, 'log-info');
    addLog(`Ukuran papan: ${N}×${N}, Jumlah ratu: ${N}`, 'log-info');

    startTimer();

    let found;
    if (algorithm === 'backtracking') {
        found = await solveBacktracking();
    } else {
        found = await solveBruteForce();
    }

    const elapsed = stopTimer();

    // Store results
    if (!shouldStop) {
        results[algorithm] = {
            steps,
            backtracks,
            time: elapsed,
            found
        };

        // Show comparison if both results exist
        if (results.backtracking && results.bruteforce) {
            showComparison();
        }
    }

    isRunning = false;
    btnStart.disabled = false;
    btnStart.innerHTML = '<span>▶</span> Mulai Visualisasi';
    boardSizeSlider.disabled = false;
}

function resetVisualization() {
    shouldStop = true;
    isRunning = false;

    if (timerInterval) clearInterval(timerInterval);

    steps = 0;
    backtracks = 0;
    queensPlaced = 0;

    createBoard();
    updateStats();
    document.getElementById('time-elapsed').textContent = '0 ms';
    setStatus('Siap', '');

    btnStart.disabled = false;
    btnStart.innerHTML = '<span>▶</span> Mulai Visualisasi';
    boardSizeSlider.disabled = false;

    clearLog();
    addLog('Visualisasi direset. Pilih algoritma dan klik "Mulai Visualisasi".', 'log-info');
}

// ============================
// COMPARISON
// ============================
function showComparison() {
    const section = document.getElementById('comparison-section');
    section.style.display = 'block';

    const bt = results.backtracking;
    const bf = results.bruteforce;

    document.getElementById('cmp-bt-steps').textContent = bt.steps.toLocaleString();
    document.getElementById('cmp-bf-steps').textContent = bf.steps.toLocaleString();
    document.getElementById('cmp-bt-backtracks').textContent = bt.backtracks.toLocaleString();
    document.getElementById('cmp-bf-backtracks').textContent = bf.backtracks.toLocaleString();
    document.getElementById('cmp-bt-time').textContent = formatTime(bt.time);
    document.getElementById('cmp-bf-time').textContent = formatTime(bf.time);

    // Winners
    document.getElementById('cmp-winner-steps').textContent =
        bt.steps < bf.steps ? '🧠 Backtracking' : bt.steps > bf.steps ? '💪 Brute Force' : 'Seri';
    document.getElementById('cmp-winner-steps').style.color =
        bt.steps <= bf.steps ? 'var(--accent-green)' : 'var(--accent-amber)';

    document.getElementById('cmp-winner-backtracks').textContent =
        bt.backtracks < bf.backtracks ? '🧠 Backtracking' : bt.backtracks > bf.backtracks ? '💪 Brute Force' : 'Seri';
    document.getElementById('cmp-winner-backtracks').style.color =
        bt.backtracks <= bf.backtracks ? 'var(--accent-green)' : 'var(--accent-amber)';

    document.getElementById('cmp-winner-time').textContent =
        bt.time < bf.time ? '🧠 Backtracking' : bt.time > bf.time ? '💪 Brute Force' : 'Seri';
    document.getElementById('cmp-winner-time').style.color =
        bt.time <= bf.time ? 'var(--accent-green)' : 'var(--accent-amber)';

    // Verdict
    const ratio = bf.steps > 0 ? (bf.steps / bt.steps).toFixed(1) : '∞';
    document.getElementById('comparison-verdict').innerHTML =
        `🏆 Backtracking menyelesaikan masalah dengan <strong>${ratio}x lebih sedikit langkah</strong> dibanding Brute Force! <br>` +
        `<span style="font-size: 0.85rem; opacity: 0.8;">Ini membuktikan efisiensi pruning dalam strategi Backtracking.</span>`;

    // Scroll to comparison
    section.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
