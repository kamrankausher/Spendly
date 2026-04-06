document.addEventListener('DOMContentLoaded', () => {

    // ═══════════ Theme Engine ═══════════
    const saved = localStorage.getItem('spendly_theme');
    if (saved === 'dark') document.body.setAttribute('data-theme', 'dark');
    updateThemeIcon();

    document.querySelectorAll('#themeBtn').forEach(btn => {
        btn.addEventListener('click', () => {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            document.body.setAttribute('data-theme', isDark ? '' : 'dark');
            localStorage.setItem('spendly_theme', isDark ? 'light' : 'dark');
            updateThemeIcon();
        });
    });
    function updateThemeIcon() {
        const isDark = document.body.getAttribute('data-theme') === 'dark';
        document.querySelectorAll('#themeBtn').forEach(b => b.textContent = isDark ? '☀️' : '🌙');
    }

    // ═══════════ Mobile Sidebar Toggle ═══════════
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const mobileToggle = document.getElementById('mobileToggle');

    function openSidebar() {
        if (sidebar) sidebar.classList.add('open');
        if (overlay) overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    function closeSidebar() {
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('show');
        document.body.style.overflow = '';
    }
    if (mobileToggle) mobileToggle.addEventListener('click', () => {
        sidebar && sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    });
    if (overlay) overlay.addEventListener('click', closeSidebar);
    // Close sidebar when a nav link is clicked (mobile)
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', closeSidebar);
    });

    // ═══════════ Smooth Toasts ═══════════
    document.querySelectorAll('.toast').forEach(t => {
        setTimeout(() => { t.classList.add('fade-out'); setTimeout(() => t.remove(), 400); }, 3500);
    });

    // ═══════════ Date Autofill ═══════════
    document.querySelectorAll('input[type="date"]').forEach(el => {
        if (!el.value) el.valueAsDate = new Date();
    });

    // ═══════════ Custom Confirm + AJAX Delete ═══════════
    // Create confirm modal once
    const confirmHTML = `
    <div id="confirmModal" class="modal-overlay">
        <div class="card modal-box confirm-modal">
            <div class="confirm-icon">⚠️</div>
            <h3 id="confirmTitle">Confirm Delete</h3>
            <p id="confirmMsg">Are you sure you want to delete this item? This cannot be undone.</p>
            <div class="confirm-actions">
                <button class="btn btn-outline" onclick="closeConfirm()">Cancel</button>
                <button class="btn btn-danger" id="confirmYes">Delete</button>
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', confirmHTML);

    let pendingDeleteUrl = null;
    let pendingDeleteRow = null;

    window.confirmDelete = function(url, rowEl, itemName) {
        pendingDeleteUrl = url;
        pendingDeleteRow = rowEl;
        document.getElementById('confirmMsg').textContent = `Are you sure you want to delete this ${itemName || 'item'}? This cannot be undone.`;
        document.getElementById('confirmModal').classList.add('show');
    };

    window.closeConfirm = function() {
        document.getElementById('confirmModal').classList.remove('show');
        pendingDeleteUrl = null;
        pendingDeleteRow = null;
    };

    document.getElementById('confirmYes').addEventListener('click', () => {
        closeConfirm();
        if (pendingDeleteUrl) {
            if (pendingDeleteRow) {
                pendingDeleteRow.classList.add('deleting');
            }
            // Navigate to the delete URL (server handles it and redirects)
            setTimeout(() => { window.location.href = pendingDeleteUrl; }, 350);
        }
    });

    // Intercept all delete links and use confirm modal instead
    document.querySelectorAll('a[data-delete]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const row = link.closest('tr') || link.closest('.goal-card') || link.closest('.card');
            confirmDelete(link.href, row, link.dataset.delete);
        });
    });

    // ═══════════ Chart Helpers ═══════════
    const CHART_COLORS = [
        '#7c3aed','#a78bfa','#c084fc','#d4a017','#059669','#dc2626',
        '#d97706','#6366f1','#ec4899','#14b8a6','#f43f5e','#8b5cf6'
    ];
    function getCSS(prop) { return getComputedStyle(document.body).getPropertyValue(prop).trim(); }
    const chartDefaults = {
        responsive: true, maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: getCSS('--text-muted'), padding: 14, font: { family: 'Inter', size: 12 }, usePointStyle: true, pointStyle: 'circle' }
            }
        }
    };

    // ═══════════ Dashboard Charts ═══════════
    const catEl = document.getElementById('cat-data');
    if (catEl) {
        const data = JSON.parse(catEl.textContent);
        const labels = Object.keys(data), values = Object.values(data);
        const barCtx = document.getElementById('spendChart');
        if (barCtx) {
            new Chart(barCtx, {
                type: 'bar',
                data: { labels, datasets: [{ data: values, backgroundColor: CHART_COLORS.slice(0, labels.length), borderRadius: 10, borderSkipped: false }] },
                options: {
                    ...chartDefaults,
                    plugins: { ...chartDefaults.plugins, legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(128,128,128,.06)', drawBorder: false }, ticks: { color: getCSS('--text-muted'), font: { size: 11 } }, border: { display: false } },
                        x: { grid: { display: false }, ticks: { color: getCSS('--text-muted'), font: { size: 11 } }, border: { display: false } }
                    }
                }
            });
        }
        const donutCtx = document.getElementById('budgetDonut');
        if (donutCtx) {
            const spent = values.reduce((a, b) => a + b, 0);
            const budgetEl = document.querySelector('.stat-value.gold');
            const budget = parseFloat((budgetEl ? budgetEl.textContent : '0').replace(/[^0-9.]/g, '')) || 0;
            new Chart(donutCtx, {
                type: 'doughnut',
                data: { labels: ['Spent', 'Remaining'], datasets: [{ data: [spent, Math.max(0, budget - spent)], backgroundColor: ['#dc2626', '#059669'], borderWidth: 0, spacing: 4, borderRadius: 8 }] },
                options: { ...chartDefaults, cutout: '68%', plugins: { ...chartDefaults.plugins, legend: { position: 'bottom', ...chartDefaults.plugins.legend } } }
            });
        }
    }

    // ═══════════ Reports Charts ═══════════
    const repCatEl = document.getElementById('report-cat-data');
    if (repCatEl) {
        const data = JSON.parse(repCatEl.textContent);
        const barCtx = document.getElementById('reportBarChart');
        if (barCtx) {
            new Chart(barCtx, {
                type: 'bar',
                data: { labels: data.map(d => d.category), datasets: [{ data: data.map(d => d.total), backgroundColor: CHART_COLORS, borderRadius: 10, borderSkipped: false }] },
                options: { ...chartDefaults, indexAxis: 'y', plugins: { ...chartDefaults.plugins, legend: { display: false } },
                    scales: { x: { grid: { color: 'rgba(128,128,128,.06)' }, ticks: { color: getCSS('--text-muted') }, border: { display: false } }, y: { grid: { display: false }, ticks: { color: getCSS('--text-muted') }, border: { display: false } } } }
            });
        }
    }
    const repBudgetEl = document.getElementById('report-budget-data');
    if (repBudgetEl) {
        const d = JSON.parse(repBudgetEl.textContent);
        const ctx = document.getElementById('reportPieChart');
        if (ctx) new Chart(ctx, { type: 'doughnut', data: { labels: ['Spent', 'Remaining'], datasets: [{ data: [d.spent, Math.max(0, d.budget - d.spent)], backgroundColor: ['#d97706', '#059669'], borderWidth: 0, spacing: 4, borderRadius: 8 }] }, options: { ...chartDefaults, cutout: '62%', plugins: { ...chartDefaults.plugins, legend: { position: 'bottom', ...chartDefaults.plugins.legend } } } });
    }
    const trendEl = document.getElementById('report-trend-data');
    if (trendEl) {
        const data = JSON.parse(trendEl.textContent);
        const ctx = document.getElementById('trendChart');
        if (ctx && data.length > 0) {
            const gr = ctx.getContext('2d').createLinearGradient(0, 0, 0, 250);
            gr.addColorStop(0, 'rgba(124,58,237,0.25)'); gr.addColorStop(1, 'rgba(124,58,237,0.01)');
            new Chart(ctx, { type: 'line', data: { labels: data.map(d => d.month), datasets: [{ label: 'Spending', data: data.map(d => d.total), borderColor: '#7c3aed', backgroundColor: gr, fill: true, tension: .4, borderWidth: 2.5, pointBackgroundColor: '#7c3aed', pointRadius: 5, pointHoverRadius: 8 }] },
                options: { ...chartDefaults, plugins: { ...chartDefaults.plugins, legend: { display: false } }, scales: { y: { grid: { color: 'rgba(128,128,128,.06)' }, ticks: { color: getCSS('--text-muted') }, border: { display: false } }, x: { grid: { display: false }, ticks: { color: getCSS('--text-muted') }, border: { display: false } } } } });
        }
    }

    // ═══════════ Tracking Chart ═══════════
    const trackEl = document.getElementById('tracking-cat-data');
    if (trackEl) {
        const data = JSON.parse(trackEl.textContent);
        const ctx = document.getElementById('trackingChart');
        if (ctx) new Chart(ctx, { type: 'doughnut', data: { labels: Object.keys(data), datasets: [{ data: Object.values(data), backgroundColor: CHART_COLORS, borderWidth: 0, spacing: 3, borderRadius: 6 }] }, options: { ...chartDefaults, cutout: '55%', plugins: { ...chartDefaults.plugins, legend: { position: 'right', ...chartDefaults.plugins.legend } } } });
    }

    // ═══════════ Analytics Charts ═══════════
    const analCatEl = document.getElementById('analytics-cat-trend');
    if (analCatEl) {
        const data = JSON.parse(analCatEl.textContent);
        const ctx = document.getElementById('catTrendChart');
        if (ctx && data.length > 0) {
            new Chart(ctx, { type: 'bar', data: { labels: data.map(d => d.category), datasets: [{ label: 'Total Spent', data: data.map(d => d.total), backgroundColor: CHART_COLORS, borderRadius: 10, borderSkipped: false }] },
                options: { ...chartDefaults, plugins: { ...chartDefaults.plugins, legend: { display: false } }, scales: { y: { grid: { color: 'rgba(128,128,128,.06)' }, border: { display: false }, ticks: { color: getCSS('--text-muted') } }, x: { grid: { display: false }, border: { display: false }, ticks: { color: getCSS('--text-muted') } } } } });
        }
    }
    const analMonthEl = document.getElementById('analytics-monthly');
    if (analMonthEl) {
        const data = JSON.parse(analMonthEl.textContent);
        const ctx = document.getElementById('monthlyTrendChart');
        if (ctx && data.length > 0) {
            const gr = ctx.getContext('2d').createLinearGradient(0, 0, 0, 250);
            gr.addColorStop(0, 'rgba(5,150,105,0.2)'); gr.addColorStop(1, 'rgba(5,150,105,0.01)');
            new Chart(ctx, { type: 'line', data: { labels: data.map(d => d.month), datasets: [{ label: 'Monthly Spending', data: data.map(d => d.total), borderColor: '#059669', backgroundColor: gr, fill: true, tension: .4, borderWidth: 2.5, pointBackgroundColor: '#059669', pointRadius: 5, pointHoverRadius: 8 }] },
                options: { ...chartDefaults, plugins: { ...chartDefaults.plugins, legend: { display: false } }, scales: { y: { grid: { color: 'rgba(128,128,128,.06)' }, border: { display: false }, ticks: { color: getCSS('--text-muted') } }, x: { grid: { display: false }, border: { display: false }, ticks: { color: getCSS('--text-muted') } } } } });
        }
    }

    // ═══════════ Receipt Scanner (Tesseract.js) ═══════════
    const scanInput = document.getElementById('scanFileInput');
    if (scanInput) {
        const scanZone = document.getElementById('scanZone');
        const previewImg = document.getElementById('scanPreview');
        const resultDiv = document.getElementById('scanResult');
        const loadingDiv = document.getElementById('scanLoading');

        // Drag & drop
        if (scanZone) {
            scanZone.addEventListener('dragover', e => { e.preventDefault(); scanZone.classList.add('dragover'); });
            scanZone.addEventListener('dragleave', () => scanZone.classList.remove('dragover'));
            scanZone.addEventListener('drop', e => { e.preventDefault(); scanZone.classList.remove('dragover'); if (e.dataTransfer.files[0]) processImage(e.dataTransfer.files[0]); });
        }

        scanInput.addEventListener('change', () => { if (scanInput.files[0]) processImage(scanInput.files[0]); });

        function processImage(file) {
            const reader = new FileReader();
            reader.onload = async (e) => {
                previewImg.src = e.target.result;
                previewImg.style.display = 'block';
                loadingDiv.style.display = 'flex';
                resultDiv.style.display = 'none';

                try {
                    const { createWorker } = Tesseract;
                    const worker = await createWorker('eng');
                    const { data: { text } } = await worker.recognize(e.target.result);
                    await worker.terminate();
                    parseReceipt(text);
                } catch (err) {
                    loadingDiv.style.display = 'none';
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = `<p class="text-danger">OCR failed. Please enter details manually.</p>`;
                }
            };
            reader.readAsDataURL(file);
        }

        function parseReceipt(text) {
            loadingDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            // Parse amounts (look for currency symbols or numbers after "total")
            const amountMatch = text.match(/(?:total|amount|grand|net|sum)[:\s]*[₹$€£]?\s*([\d,]+\.?\d*)/i)
                || text.match(/[₹$€£]\s*([\d,]+\.?\d*)/i)
                || text.match(/([\d,]+\.\d{2})/);
            const amount = amountMatch ? amountMatch[1].replace(/,/g, '') : '';

            // Parse date
            const dateMatch = text.match(/(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/);
            let dateStr = '';
            if (dateMatch) {
                const y = dateMatch[3].length === 2 ? '20' + dateMatch[3] : dateMatch[3];
                dateStr = `${y}-${dateMatch[2].padStart(2, '0')}-${dateMatch[1].padStart(2, '0')}`;
            }

            // Fill form fields
            const amtField = document.getElementById('scanAmount');
            const dateField = document.getElementById('scanDate');
            const descField = document.getElementById('scanDesc');
            const rawField = document.getElementById('scanRawText');

            if (amtField) amtField.value = amount;
            if (dateField) dateField.value = dateStr || new Date().toISOString().split('T')[0];
            if (descField) descField.value = text.split('\n').filter(l => l.trim()).slice(0, 2).join(' — ').substring(0, 80);
            if (rawField) rawField.value = text;

            resultDiv.innerHTML = `<div class="flex items-center gap-1 mb-1" style="color:var(--success);font-weight:600">✅ Scan Complete</div>
                <p class="text-muted" style="font-size:.82rem">Extracted data has been pre-filled below. Review and adjust before saving.</p>`;
        }
    }

    // ═══════════ Multi-Language ═══════════
    const TRANSLATIONS = {
        English: {},
        Hindi: { 'Dashboard':'डैशबोर्ड','Tracking':'ट्रैकिंग','Reports':'रिपोर्ट्स','Alerts':'अलर्ट','Goals':'लक्ष्य','Profile':'प्रोफ़ाइल','Sign Out':'लॉग आउट','Monthly Budget':'मासिक बजट','Total Spent':'कुल खर्च','Remaining':'शेष','Budget Used':'बजट उपयोग','Scanner':'स्कैनर','Analytics':'विश्लेषण' },
        Spanish: { 'Dashboard':'Panel','Tracking':'Seguimiento','Reports':'Informes','Alerts':'Alertas','Goals':'Metas','Profile':'Perfil','Sign Out':'Salir','Monthly Budget':'Presupuesto','Total Spent':'Gastado','Remaining':'Restante','Budget Used':'Presupuesto usado','Scanner':'Escáner','Analytics':'Analíticas' },
        French: { 'Dashboard':'Tableau','Tracking':'Suivi','Reports':'Rapports','Alerts':'Alertes','Goals':'Objectifs','Profile':'Profil','Sign Out':'Déconnexion','Monthly Budget':'Budget','Total Spent':'Dépensé','Remaining':'Restant','Budget Used':'Budget utilisé','Scanner':'Scanner','Analytics':'Analytiques' }
    };
    const langMeta = document.querySelector('meta[name="user-lang"]');
    if (langMeta) {
        const lang = langMeta.content;
        if (lang && lang !== 'English' && TRANSLATIONS[lang]) applyTranslations(TRANSLATIONS[lang]);
    }
    function applyTranslations(dict) {
        document.querySelectorAll('.sidebar-nav a, .stat-label, .topbar-title, .sidebar-footer a').forEach(el => {
            const clean = el.textContent.replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '').trim();
            if (dict[clean]) {
                const span = el.querySelector('.nav-icon');
                if (span) { el.childNodes.forEach(n => { if (n.nodeType === 3 && n.textContent.trim()) n.textContent = ' ' + dict[clean]; }); }
                else { const m = el.textContent.match(/^([\u{1F300}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]\s*)/u); el.textContent = (m ? m[1] : '') + dict[clean]; }
            }
        });
    }

    // ═══════════ PDF Print ═══════════
    window.printReport = function() { window.print(); };

    // ═══════════ Real-time refresh ═══════════
    if (document.getElementById('cat-data') && window.location.pathname === '/dashboard') {
        setInterval(() => {
            fetch('/api/summary').then(r => r.json()).then(d => {
                const vals = document.querySelectorAll('.stat-value');
                if (vals.length >= 3) {
                    const sym = vals[0].textContent.replace(/[0-9,.]/g, '');
                    vals[1].textContent = sym + d.spent.toLocaleString('en-IN', { maximumFractionDigits: 0 });
                    vals[2].textContent = sym + d.remaining.toLocaleString('en-IN', { maximumFractionDigits: 0 });
                }
            }).catch(() => {});
        }, 30000);
    }

    // ═══════════ PWA Install Prompt ═══════════
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        const installBtn = document.getElementById('installPwa');
        if (installBtn) {
            installBtn.style.display = 'inline-flex';
            installBtn.addEventListener('click', () => {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(() => { deferredPrompt = null; installBtn.style.display = 'none'; });
            });
        }
    });
});
