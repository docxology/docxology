/* Externalized from repositories.html inline script (CSP: script-src 'self'). Shared by repositories.html and repositories-forks.html. */
const rows = Array.from(document.querySelectorAll('#inventoryRows tr'));
        const input = document.getElementById('inventorySearch');
        const languageFilter = document.getElementById('inventoryLanguage');
        const count = document.getElementById('inventoryResultCount');
        let filter = 'all';
        function matchesFilter(row) {
            if (filter === 'docxology') return row.dataset.owner === 'docxology';
            if (filter === 'aii') return row.dataset.owner === 'ActiveInferenceInstitute';
            if (filter === 'curated') return row.dataset.curated === 'true';
            if (filter === 'uncataloged') return row.dataset.curated === 'false';
            if (filter === 'archived') return row.dataset.archived === 'true';
            if (filter === 'public' || filter === 'private') return row.dataset.visibility === filter;
            if (filter === 'recent') return row.dataset.recent === 'true';
            return true;
        }
        function applyFilters() {
            const q = input.value.trim().toLowerCase();
            const lang = languageFilter.value.toLowerCase();
            let visible = 0;
            rows.forEach(row => {
                const matchesLanguage = !lang || row.dataset.language === lang;
                const ok = matchesFilter(row) && matchesLanguage && (!q || row.dataset.search.includes(q));
                row.style.display = ok ? '' : 'none';
                if (ok) visible += 1;
            });
            count.textContent = `${visible} repositories shown`;
        }
        document.querySelectorAll('.filter-chip').forEach(button => {
            button.addEventListener('click', () => {
                document.querySelectorAll('.filter-chip').forEach(item => item.classList.remove('active'));
                button.classList.add('active');
                filter = button.dataset.filter;
                applyFilters();
            });
        });
        input.addEventListener('input', applyFilters);
        languageFilter.addEventListener('change', applyFilters);
        applyFilters();
