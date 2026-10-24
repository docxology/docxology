/* Fully specified teaching models; no remote computation or external libraries. */
(() => {
    'use strict';
    function probability(value) {
        if (!Number.isFinite(value) || value < 0 || value > 1) throw new Error('Probabilities must be finite numbers between 0 and 1.');
        return value;
    }
    function binaryHistory(prior, yes, no, observations) {
        [prior, yes, no].forEach(probability);
        if (!Array.isArray(observations) || observations.length > 100 || observations.some(x => typeof x !== 'boolean')) throw new Error('Use at most 100 binary observations.');
        let h = Math.log(prior), n = Math.log1p(-prior);
        const rows = [{step: 0, observation: 'prior', posterior: prior}];
        observations.forEach((seen, index) => {
            h += Math.log(seen ? yes : 1 - yes);
            n += Math.log(seen ? no : 1 - no);
            const largest = Math.max(h, n);
            if (largest === -Infinity) throw new Error('This observation is impossible under both weighted hypotheses. State unchanged.');
            const ph = Math.exp(h - largest), pn = Math.exp(n - largest);
            rows.push({step: index + 1, observation: seen ? 'E' : 'not-E', posterior: ph / (ph + pn)});
        });
        return rows;
    }
    function integer(value, min, max, name) {
        if (!Number.isInteger(value) || value < min || value > max) throw new Error(`${name} must be an integer from ${min} to ${max}.`);
        return value;
    }
    function urnHistory(amber, blue, reinforcement, draws, seed) {
        integer(amber, 1, 20, 'Amber'); integer(blue, 1, 20, 'Blue');
        integer(reinforcement, 0, 5, 'Reinforcement'); integer(draws, 1, 200, 'Draws'); integer(seed, 0, 4294967295, 'Seed');
        // Mulberry32: fixed 32-bit integer operations, including the zero seed.
        let state = seed >>> 0;
        const random = () => {
            state = (state + 0x6D2B79F5) >>> 0;
            let t = Math.imul(state ^ (state >>> 15), 1 | state);
            t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        };
        const rows = [{step: 0, color: 'initial', amber, blue, fraction: amber / (amber + blue)}];
        for (let i = 1; i <= draws; i++) {
            const selected = random() < amber / (amber + blue);
            if (selected) amber += reinforcement; else blue += reinforcement;
            rows.push({step: i, color: selected ? 'amber' : 'blue', amber, blue, fraction: amber / (amber + blue)});
        }
        return rows;
    }
    if (typeof module !== 'undefined') module.exports = {binaryHistory, urnHistory};
    if (typeof document === 'undefined' || !document.getElementById('bayes')) return;

    const $ = id => document.getElementById(id);
    const NS = 'http://www.w3.org/2000/svg';
    let observations = [], bayesRows = [], urnRows = [], urnParameters = null;
    function plot(id, rows, field) {
        const svg = $(id); svg.replaceChildren();
        const path = document.createElementNS(NS, 'path');
        path.setAttribute('class', 'probability-line');
        const last = Math.max(1, rows.length - 1);
        path.setAttribute('d', rows.map((row, i) => `${i ? 'L' : 'M'}${48 + 720 * i / last},${232 - 200 * row[field]}`).join(' '));
        const axis = document.createElementNS(NS, 'path'); axis.setAttribute('d', 'M48,32V232H768'); axis.setAttribute('class', 'plot-axis'); svg.appendChild(axis);
        for (const [label, x, y] of [['1.0', 0, 38], ['0.0', 0, 238], ['0', 48, 268], [String(rows.length - 1), 730, 268]]) {
            const text = document.createElementNS(NS, 'text'); text.setAttribute('x', x); text.setAttribute('y', y); text.textContent = label; svg.appendChild(text);
        }
        svg.appendChild(path);
    }
    function table(id, rows, columns) {
        $(id).replaceChildren(...rows.map(row => {
            const tr = document.createElement('tr');
            for (const column of columns) { const td = document.createElement('td'); td.textContent = typeof row[column] === 'number' && !Number.isInteger(row[column]) ? row[column].toFixed(8) : String(row[column]); tr.appendChild(td); }
            return tr;
        }));
    }
    function download(rows, columns, parameters, filename) {
        const names = [...Object.keys(parameters), ...columns];
        const csv = names.join(',') + '\n' + rows.map(row => [...Object.values(parameters), ...columns.map(c => row[c])].join(',')).join('\n') + '\n';
        const url = URL.createObjectURL(new Blob([csv], {type: 'text/csv;charset=utf-8'}));
        const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }
    function bayesParameters() { return {prior: Number($('bayes-prior').value) / 100, likelihood_e_h: Number($('bayes-yes').value) / 100, likelihood_e_not_h: Number($('bayes-no').value) / 100}; }
    function updateBayes(next) {
        try {
            const p = bayesParameters();
            const rows = binaryHistory(p.prior, p.likelihood_e_h, p.likelihood_e_not_h, next);
            observations = next; bayesRows = rows;
            $('bayes-result').textContent = `P(H) = ${rows.at(-1).posterior.toFixed(8)} after ${observations.length} observation(s).`;
            table('bayes-history', rows, ['step', 'observation', 'posterior']); plot('bayes-chart', rows, 'posterior');
            $('bayes-positive').disabled = observations.length >= 100; $('bayes-negative').disabled = observations.length >= 100;
        } catch (error) { $('bayes-result').textContent = error.message; }
    }
    for (const id of ['bayes-prior', 'bayes-yes', 'bayes-no']) $(id).addEventListener('input', () => { $(id + '-value').value = $(id).value; updateBayes([]); });
    $('bayes-positive').addEventListener('click', () => updateBayes([...observations, true]));
    $('bayes-negative').addEventListener('click', () => updateBayes([...observations, false]));
    $('bayes-reset').addEventListener('click', () => updateBayes([]));
    $('bayes-export').addEventListener('click', () => download(bayesRows, ['step', 'observation', 'posterior'], bayesParameters(), 'bayesian-update.csv'));
    function runUrn() {
        try {
            const read = id => $(id).value.trim() === '' ? NaN : Number($(id).value);
            const p = {initial_amber: read('urn-amber'), initial_blue: read('urn-blue'), reinforcement: read('urn-reinforcement'), draws: read('urn-draws'), seed: read('urn-seed')};
            const rows = urnHistory(p.initial_amber, p.initial_blue, p.reinforcement, p.draws, p.seed);
            urnParameters = p; urnRows = rows;
            const last = rows.at(-1);
            $('urn-result').textContent = `Seed ${p.seed}: ${last.amber} amber, ${last.blue} blue after ${p.draws} draws. Amber fraction ${last.fraction.toFixed(8)}.`;
            table('urn-history', rows, ['step', 'color', 'amber', 'blue', 'fraction']); plot('urn-chart', rows, 'fraction'); $('urn-export').disabled = false;
        } catch (error) { $('urn-result').textContent = error.message; $('urn-export').disabled = true; }
    }
    for (const id of ['urn-amber', 'urn-blue', 'urn-reinforcement', 'urn-draws', 'urn-seed']) $(id).addEventListener('input', () => { $('urn-export').disabled = true; $('urn-result').textContent = 'Parameters changed. Run the urn to replace the previous results.'; });
    $('urn-run').addEventListener('click', runUrn);
    $('urn-export').addEventListener('click', () => { if (!$('urn-export').disabled) download(urnRows, ['step', 'color', 'amber', 'blue', 'fraction'], urnParameters, 'reinforced-urn.csv'); });
    updateBayes([]); runUrn();
})();
