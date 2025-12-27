// History Btn
function toggleHistory(show) {
    if (show) {
        historyModal.classList.remove('hidden');
        setTimeout(() => historyPanel.classList.remove('translate-x-full'), 10);
    } else {
        historyPanel.classList.add('translate-x-full');
        setTimeout(() => historyModal.classList.add('hidden'), 300);
    }
}

function addToHistory(file, data) {
    const historyItem = {
        id: Date.now(),
        fileName: file.name,
        fileSize: (file.size / 1024).toFixed(1) + ' KB',
        date: new Date().toLocaleString('en-GB'),
        summary: {
            total: data.insights.total_reviews,
            risk: data.insights.risk_level,
            positive: Math.round((data.insights.sentiment_distribution.positive || 0) * 100)
        },
        fullData: data
    };

    const history = JSON.parse(localStorage.getItem('insyte_history') || '[]');
    history.unshift(historyItem);
    localStorage.setItem('insyte_history', JSON.stringify(history));
}

function renderHistoryList() {
    const container = document.getElementById('historyList');
    const history = JSON.parse(localStorage.getItem('insyte_history') || '[]');

    container.innerHTML = '';

    if (history.length === 0) {
        container.innerHTML = `<div class="text-center py-10 opacity-50 text-slate-500"><p>No history found</p></div>`;
        return;
    }

    history.forEach(item => {
        let riskColor = item.summary.risk === 'high' ? 'text-red-400 bg-red-400/10' :
            (item.summary.risk === 'medium' ? 'text-yellow-400 bg-yellow-400/10' : 'text-green-400 bg-green-400/10');

        const div = document.createElement('div');
        div.className = "bg-slate-800 hover: border-slate-700 p-4 rounded-xl cursor-pointer transition duration-300 ease-out hover:scale-[1.04] group";
        div.onclick = () => restoreAnalysis(item.id);

        div.innerHTML = `
            <div class="flex justify-between items-start mb-3">
                <div class="min-w-0">
                    <h4 class="text-white font-medium truncate text-sm">${item.fileName}</h4>
                    <p class="text-xs text-slate-500">${item.date}</p>
                </div>
                <span class="text-xs font-bold px-2 py-1 rounded capitalize ${riskColor}">${item.summary.risk} Risk</span>
            </div>
            <div class="flex justify-between text-xs text-slate-400 border-t border-slate-700/50 pt-2 mt-2">
                <span>${item.summary.total} Reviews</span>
                <span class="text-green-400">${item.summary.positive}% Positive</span>
            </div>
        `;
        container.appendChild(div);
    });
}

function restoreAnalysis(id) {
    const history = JSON.parse(localStorage.getItem('insyte_history') || '[]');
    const item = history.find(x => x.id === id);
    if (item) {
        lastResponse = item.fullData;
        renderInsights(item.fullData);
        document.getElementById('emptyState').parentElement.classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');
        toggleHistory(false);
    }
}

function clearHistory() {
    if (confirm("Delete all history?")) {
        localStorage.removeItem('insyte_history');
        renderHistoryList();
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        toggleHistory(false);
    }
});