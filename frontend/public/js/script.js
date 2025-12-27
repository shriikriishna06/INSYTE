const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const emptyState = document.getElementById('emptyState');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const reviewsList = document.getElementById('reviewsList');
const filterLabel = document.getElementById('filterLabel');
const supportedReviewsSection = document.getElementById('supportedReviewsSection');
const historyModal = document.getElementById('historyModal');
const historyPanel = document.getElementById('historyPanel');
const viewHistoryBtn = document.getElementById('viewHistoryBtn');

viewHistoryBtn.addEventListener('click', () => {
    renderHistoryList();
    toggleHistory(true);
});

let lastResponse = null;

//File Upload(drag n drop & select)
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-brand-500', 'bg-slate-800/50');
});
dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-brand-500', 'bg-slate-800/50');
});
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-brand-500', 'bg-slate-800/50');
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        dropZone.querySelector('p.text-slate-300').textContent = e.dataTransfer.files[0].name;
    }
});

//Update drop zone
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        dropZone.querySelector('p.text-slate-300').textContent = fileInput.files[0].name;
    }
});

//Analyze Btn
analyzeBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];

    //Validation
    if (!file) {
        dropZone.classList.add('border-red-500');
        setTimeout(() => dropZone.classList.remove('border-red-500'), 2000);
        return alert("Please upload a CSV file.");
    }

    
    const originalContent = analyzeBtn.innerHTML;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `<div class="loader mr-2"></div> Analyzing...`;
    analyzeBtn.classList.add('opacity-75', 'cursor-not-allowed');

    try {
        //Read File
        const text = await file.text();
        const lines = text.split("\n").map(l => l.trim()).filter(Boolean);

        let reviews = lines;
        //Header Detection
        if (lines[0].toLowerCase().includes("review")) {
            reviews = lines.slice(1);
        }

        //API Call
        const res = await fetch("http://127.0.0.1:8000/api/batch-analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ reviews })
        });

        if (!res.ok) {
            const err = await res.text();
            throw new Error(err || "Analysis failed");
        }

        lastResponse = await res.json();
        addToHistory(file, lastResponse);

        //Render Data
        renderInsights(lastResponse);

        //Update UI State (Success)
        emptyState.parentElement.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (e) {
        console.error(e);
        alert("Service temporarily unavailable.");
    } finally {
        // Reset Button
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalContent;
        analyzeBtn.classList.remove('opacity-75', 'cursor-not-allowed');
    }
});

//RENDERING LOGIC

function renderInsights(data) {
    const i = data.insights;
    
    //Total Reviews
    const totalEl = resultsSection.querySelector('.grid > div:nth-child(1) p.text-3xl');
    if (totalEl) totalEl.textContent = i.total_reviews.toLocaleString();

    //Risk Level
    const riskContainer = resultsSection.querySelector('.grid > div:nth-child(2)');
    const riskEl = riskContainer.querySelector('p.text-2xl');

    if (riskEl) {
        //Set text
        riskEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-lg"></i> ${i.risk_level.toUpperCase()}`;
        riskContainer.className = `glass-panel p-5 rounded-2xl border-b-4 ${getRiskColorClass(i.risk_level)}`;
        riskEl.className = `text-2xl font-bold flex items-center gap-2 ${getTextColorClass(i.risk_level)}`;
    }

    //Avg Confidence
    const confEl = resultsSection.querySelector('.grid > div:nth-child(3) p.text-3xl');
    if (confEl) confEl.textContent = i.average_confidence;

    //Mixed Reviews
    const mixedEl = resultsSection.querySelector('.grid > div:nth-child(4) p.text-3xl');
    if (mixedEl) mixedEl.textContent = i.mixed_feedback_ratio;

    //Sentiment Distribution
    renderSentimentChart(i.sentiment_distribution);

    //Pros & Cons
    renderList('pro', i.pros);
    renderList('con', i.cons);
}

function renderSentimentChart(dist) {
    const updateCard = (index, value) => {
        const percentage = Math.round(value * 100) + '%';
        const card = resultsSection.querySelectorAll('.grid')[1].children[index];
        if (card) {
            card.querySelector('.text-4xl').textContent = percentage;
            card.querySelector('.bg-slate-800 > div').style.width = percentage;
        }
    };
    updateCard(0, dist.positive || 0); 
    updateCard(1, dist.neutral || 0);  
    updateCard(2, dist.negative || 0); 
}

function renderList(type, items) {
    const containerIndex = type === 'pro' ? 0 : 1;
    const container = resultsSection.querySelectorAll('.grid')[2].children[containerIndex];
    const listContainer = container.querySelector('.space-y-3');

    listContainer.innerHTML = ""; 

    items.forEach(factor => {
        const div = document.createElement('div');

        div.className = "insight-item cursor-pointer p-3 rounded-xl bg-slate-900/40 border border-slate-800 transition-all duration-200 group";
        
        const hoverColor = type === 'pro' ? 'group-hover:text-green-400' : 'group-hover:text-red-400';
        const barColor = type === 'pro' ? 'bg-green-500' : 'bg-red-500';
        const randomWidth = Math.floor(Math.random() * (90 - 40) + 40) + '%';

        div.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="text-slate-200 font-medium ${hoverColor} transition-colors capitalize">${factor}</span>
                <i class="fa-solid fa-chevron-right text-slate-600 text-xs"></i>
            </div>
            <div class="w-full bg-slate-800 h-1 mt-3 rounded-full overflow-hidden">
                <div class="${barColor} h-1 rounded-full" style="width: ${randomWidth}"></div>
            </div>
        `;

        div.onclick = () => showEvidence(factor, type);
        listContainer.appendChild(div);
    });
}
//Review Validation Section
function showEvidence(factor, type) {
    
    filterLabel.innerText = factor;
    filterLabel.className = type === 'pro'
        ? 'text-green-400 font-bold capitalize'
        : 'text-red-400 font-bold capitalize';

    reviewsList.innerHTML = '';
    const ids = lastResponse.insights.factor_review_map[factor] || [];

    if (ids.length === 0) {
        reviewsList.innerHTML = `<div class="p-4 text-slate-500 italic">No specific reviews found.</div>`;
    } else {
        ids.forEach(id => {
            const r = lastResponse.results.find(x => x.review_id === id);
            if (r) {
                const div = document.createElement('div');
                div.className = "bg-slate-800 p-4 rounded-xl border border-slate-700/50 hover:border-slate-600 transition-colors";

                const sentimentColor = r.sentiment === 'positive' ? 'text-green-400' : (r.sentiment === 'negative' ? 'text-red-400' : 'text-slate-400');

                div.innerHTML = `
                    <div class="flex items-start gap-3">
                        <i class="fa-solid fa-quote-left text-slate-600 text-xs mt-1"></i>
                        <div class="flex-1">
                            <p class="text-slate-300 text-sm leading-relaxed font-light">${r.summary || "Review content unavailable"}</p>
                            <div class="mt-2 flex gap-2 text-xs">
                                <span class="${sentimentColor} font-medium capitalize">${r.sentiment}</span>
                                <span class="text-slate-600">•</span>
                                <span class="text-slate-500">Conf: ${r.confidence}</span>
                            </div>
                        </div>
                    </div>
                `;
                reviewsList.appendChild(div);
            }
        });
    }
    supportedReviewsSection.classList.remove('hidden');
    supportedReviewsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

//UTILS

function getRiskColorClass(level) {
    if (level === 'high') return 'border-b-red-500';
    if (level === 'medium') return 'border-b-yellow-500';
    return 'border-b-green-500'; // low
}

function getTextColorClass(level) {
    if (level === 'high') return 'text-red-500';
    if (level === 'medium') return 'text-yellow-500';
    return 'text-green-500';
}





