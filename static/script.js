/* ============================================================
   SOMETHING BANK — frontend (vanilla JS) con i18n IT/EN + grafici
   Salvataggio locale: player_id nel browser, dati in SQLite lato server.
   ============================================================ */

const PID_KEY = "sb_pid";
const NAME_KEY = "sb_name";
const LANG_KEY = "sb_lang";

const getPid = () => localStorage.getItem(PID_KEY);
const getLang = () => (localStorage.getItem(LANG_KEY) === "en" ? "en" : "it");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ============================================================
   Traduzioni
   ============================================================ */
const I18N = {
  it: {
    welcome_title: "Benvenuto.", ask_name: "Come ti chiami?", name_ph: "Il tuo nome",
    continue: "CONTINUA →", all_yours: "Sono tutti tuoi.", start: "INIZIA",
    name_error: "Serve un nome. Anche uno inventato.",
    restart: "Ricomincia", back: "← Indietro",
    wealth: "Patrimonio", net_worth: "Patrimonio netto",
    cash: "Contanti", investments: "Investimenti", stocks: "Azioni",
    property: "Proprietà", objects: "Oggetti", companies: "Aziende",
    houses: "Case", debts: "Debiti", history: "Cronologia",
    spend: "SPENDI", invest: "INVESTI", portfolio: "PORTAFOGLIO",
    shop_title: "Cosa vuoi comprare, {name}?", buy: "COMPRA",
    invest_title: "Investi", invest_sub: "I prezzi si muovono da soli. Buona fortuna.",
    buy_stock: "Compra", sell_stock: "Vendi", buy_company: "ACQUISTA AZIENDA ({value})",
    owned_tag: "TUA", holdings: "Possiedi {shares} azioni · valore {value} · cap. {cap}",
    prev_close: "Chiusura prec.", price_label: "Prezzo", day_change: "Var. giorno",
    pf_title: "Il tuo patrimonio", your_items: "I tuoi oggetti", achievements: "Achievement",
    empty_items: "Ancora niente. La sobrietà è una scelta.",
    out_of_money: "Hai finito i soldi.", discovered_debt: "Hai scoperto il debito.",
    shares_bought: "Azioni acquistate.", shares_sold: "Azioni vendute.",
    cant_afford: "Non puoi permettertelo.", generic_error: "Errore.",
    confirm_restart: "Ricominciare da capo? Il progresso verrà dimenticato su questo browser.",
    confirm_buy_company: "Comprare l'intera {name} per {value}?",
    congrats_title: "Congratulazioni, {name}.",
    congrats_text: "Ora possiedi {company}. Non sappiamo cosa tu debba farci.",
    ach_label: "🏆 Achievement", secret: "Achievement segreto.",
    intro1: "Ciao, {name}.", intro2: "Abbiamo aperto un conto a tuo nome.",
    intro3: "Abbiamo anche depositato €100.000.", intro4: "Non fare domande.",
    r_1g: "1 G", r_5g: "5 G", r_1m: "1 M", r_1a: "1 A", r_5a: "5 A", r_max: "Massimo",
    locale: "it-IT",
  },
  en: {
    welcome_title: "Welcome.", ask_name: "What's your name?", name_ph: "Your name",
    continue: "CONTINUE →", all_yours: "All yours.", start: "START",
    name_error: "A name is required. Even a made-up one.",
    restart: "Restart", back: "← Back",
    wealth: "Net worth", net_worth: "Net worth",
    cash: "Cash", investments: "Investments", stocks: "Stocks",
    property: "Property", objects: "Objects", companies: "Companies",
    houses: "Houses", debts: "Debts", history: "History",
    spend: "SPEND", invest: "INVEST", portfolio: "PORTFOLIO",
    shop_title: "What do you want to buy, {name}?", buy: "BUY",
    invest_title: "Invest", invest_sub: "Prices move on their own. Good luck.",
    buy_stock: "Buy", sell_stock: "Sell", buy_company: "BUY COMPANY ({value})",
    owned_tag: "OWNED", holdings: "You own {shares} shares · value {value} · cap {cap}",
    prev_close: "Prev. close", price_label: "Price", day_change: "Day change",
    pf_title: "Your net worth", your_items: "Your items", achievements: "Achievements",
    empty_items: "Nothing yet. Restraint is a choice.",
    out_of_money: "You're out of money.", discovered_debt: "You've discovered debt.",
    shares_bought: "Shares bought.", shares_sold: "Shares sold.",
    cant_afford: "You can't afford it.", generic_error: "Error.",
    confirm_restart: "Start over? Your progress will be forgotten on this browser.",
    confirm_buy_company: "Buy the entire {name} for {value}?",
    congrats_title: "Congratulations, {name}.",
    congrats_text: "You now own {company}. We don't know what you're supposed to do with it.",
    ach_label: "🏆 Achievement", secret: "Secret achievement.",
    intro1: "Hi, {name}.", intro2: "We've opened an account in your name.",
    intro3: "We also deposited €100,000.", intro4: "Don't ask questions.",
    r_1g: "1D", r_5g: "5D", r_1m: "1M", r_1a: "1Y", r_5a: "5Y", r_max: "Max",
    locale: "en-US",
  },
};

function t(key, vars) {
  const lang = getLang();
  let s = (I18N[lang] && I18N[lang][key]) || I18N.it[key] || key;
  if (vars) for (const k in vars) s = s.replaceAll("{" + k + "}", vars[k]);
  return s;
}

function applyI18n() {
  const lang = getLang();
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.getAttribute("data-i18n"));
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
  });
  const toggle = document.getElementById("lang-toggle");
  if (toggle) toggle.textContent = lang === "it" ? "EN" : "IT";
}

function initLangToggle() {
  const toggle = document.getElementById("lang-toggle");
  if (!toggle) return;
  toggle.addEventListener("click", () => {
    localStorage.setItem(LANG_KEY, getLang() === "it" ? "en" : "it");
    location.reload();
  });
}

/* ============================================================
   Formattazione
   ============================================================ */
function euro(n, dec = 0) {
  const neg = n < 0;
  const s = Math.abs(n).toLocaleString(t("locale"), { minimumFractionDigits: dec, maximumFractionDigits: dec });
  return (neg ? "-" : "") + "€" + s;
}
function euroSigned(n) {
  return (n >= 0 ? "+" : "-") + "€" + Math.abs(n).toLocaleString(t("locale"), { maximumFractionDigits: 2 });
}
function axisNum(n) {
  const dec = Math.abs(n) >= 100 ? 0 : Math.abs(n) >= 10 ? 1 : 2;
  return n.toLocaleString(t("locale"), { minimumFractionDigits: dec, maximumFractionDigits: dec });
}

/* ============================================================
   API
   ============================================================ */
async function api(path, body) {
  const opts = { method: body ? "POST" : "GET", headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify({ ...body, lang: getLang() });
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

/* ============================================================
   Toast / eventi
   ============================================================ */
function showToast(msg, isError = false) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.classList.toggle("error", isError);
  el.classList.remove("hidden");
  requestAnimationFrame(() => el.classList.add("show"));
  clearTimeout(el._h);
  el._h = setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.classList.add("hidden"), 300);
  }, 2600);
}

function showEvent({ title, text, amount }) {
  const el = document.getElementById("event-toast");
  if (!el) return;
  let html = "";
  if (title) html += `<div class="e-title">${title}</div>`;
  if (text) html += `<div class="e-text">${text}</div>`;
  if (amount !== undefined && amount !== null) {
    html += `<div class="e-amt ${amount >= 0 ? "pos" : "neg"}">${euroSigned(amount)}</div>`;
  }
  el.innerHTML = html;
  el.classList.remove("hidden");
  requestAnimationFrame(() => el.classList.add("show"));
  clearTimeout(el._h);
  el._h = setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.classList.add("hidden"), 350);
  }, 4200);
}

async function announceEvents(events) {
  if (!events || !events.length) return;
  for (const ev of events) {
    if (ev.type === "market") {
      showEvent({ title: ev.company, text: ev.text, amount: null });
      const el = document.getElementById("event-toast");
      if (el) el.innerHTML += `<div class="e-amt ${ev.pct >= 0 ? "pos" : "neg"}">${ev.pct >= 0 ? "+" : ""}${ev.pct}%</div>`;
    } else {
      showEvent({ title: null, text: ev.text, amount: ev.amount });
    }
    await sleep(900);
  }
}

function announceAchievements(list) {
  if (!list || !list.length) return;
  list.forEach((a, i) => setTimeout(() => showEvent({ title: t("ach_label"), text: a.name }), 400 + i * 1400));
}

/* ============================================================
   Guardia di sessione
   ============================================================ */
async function requireSession() {
  const pid = getPid();
  if (!pid) { window.location.href = "/"; return null; }
  const res = await fetch(`/api/state?pid=${encodeURIComponent(pid)}&lang=${getLang()}`);
  if (!res.ok) {
    localStorage.removeItem(PID_KEY);
    localStorage.removeItem(NAME_KEY);
    window.location.href = "/";
    return null;
  }
  return res.json();
}

/* ============================================================
   PAGINA: INDEX
   ============================================================ */
async function initIndex() {
  if (getPid()) {
    const res = await fetch(`/api/state?pid=${encodeURIComponent(getPid())}&lang=${getLang()}`);
    if (res.ok) { window.location.href = "/bank"; return; }
    localStorage.removeItem(PID_KEY);
  }
  const form = document.getElementById("name-form");
  const input = document.getElementById("name-input");
  const errEl = document.getElementById("name-error");
  input.focus();
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = input.value.trim();
    if (!name) { errEl.textContent = t("name_error"); return; }
    errEl.textContent = "";
    const { ok, data } = await api("/api/register", { name });
    if (!ok) { errEl.textContent = data.error || t("generic_error"); return; }
    localStorage.setItem(PID_KEY, data.id);
    localStorage.setItem(NAME_KEY, data.name);
    runIntro(data.name);
  });
}

async function runIntro(name) {
  document.getElementById("welcome").classList.add("hidden");
  const intro = document.getElementById("intro");
  intro.classList.remove("hidden");
  const textEl = document.getElementById("intro-text");
  const finalEl = document.getElementById("intro-final");
  const lines = [t("intro1", { name }), t("intro2"), t("intro3"), t("intro4")];
  for (const line of lines) {
    textEl.textContent = line;
    textEl.classList.remove("type-fade");
    void textEl.offsetWidth;
    textEl.classList.add("type-fade");
    await sleep(1600);
  }
  textEl.textContent = "";
  finalEl.classList.remove("hidden");
  finalEl.classList.add("fade-in");
  document.getElementById("start-button").addEventListener("click", () => (window.location.href = "/bank"));
}

/* ============================================================
   PAGINA: BANK
   ============================================================ */
function renderBank(state) {
  document.getElementById("account-name").textContent = state.name;
  const nw = document.getElementById("networth");
  nw.textContent = euro(state.net_worth, 2);
  nw.classList.remove("pop"); void nw.offsetWidth; nw.classList.add("pop");
  const b = state.breakdown;
  document.getElementById("s-cash").textContent = euro(b.cash);
  document.getElementById("s-stocks").textContent = euro(b.stocks);
  document.getElementById("s-property").textContent = euro(b.property);
  document.getElementById("s-objects").textContent = euro(b.objects);
  document.getElementById("s-companies").textContent = euro(b.companies);
  document.getElementById("s-debt").textContent = euro(b.debt);
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  state.history.forEach((h) => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${h.description}</span><span class="amt ${h.amount >= 0 ? "pos" : "neg"}">${euroSigned(h.amount)}</span>`;
    list.appendChild(li);
  });
}

async function initBank() {
  const state = await requireSession();
  if (!state) return;
  renderBank(state);
  document.getElementById("reset-btn").addEventListener("click", () => {
    if (confirm(t("confirm_restart"))) {
      localStorage.removeItem(PID_KEY);
      localStorage.removeItem(NAME_KEY);
      window.location.href = "/";
    }
  });
  setInterval(async () => {
    const { ok, data } = await api("/api/tick", { pid: getPid() });
    if (ok) { renderBank(data.state); await announceEvents(data.events); announceAchievements(data.new_achievements); }
  }, 7000);
}

/* ============================================================
   PAGINA: SHOP
   ============================================================ */
let SHOP_STATE = null, CATALOG = null, ACTIVE_CAT = null;

function updateShopBalance() {
  document.getElementById("shop-balance").textContent = euro(SHOP_STATE.cash);
}
function catLabel(c) { return getLang() === "en" ? c.label_en : c.label_it; }
function prodName(p) { return getLang() === "en" ? p.name_en : p.name; }
function prodDesc(p) { return getLang() === "en" ? p.description_en : p.description; }

function renderCatNav() {
  const nav = document.getElementById("cat-nav");
  nav.innerHTML = "";
  CATALOG.categories.forEach((c) => {
    const chip = document.createElement("button");
    chip.className = "cat-chip" + (c.key === ACTIVE_CAT ? " active" : "");
    chip.textContent = catLabel(c);
    chip.dataset.testid = "cat-" + c.key;
    chip.addEventListener("click", () => { ACTIVE_CAT = c.key; renderCatNav(); renderProducts(); });
    nav.appendChild(chip);
  });
}

function renderProducts() {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";
  CATALOG.products.filter((p) => p.category === ACTIVE_CAT).forEach((p) => {
    const card = document.createElement("div");
    card.className = "product fade-in";
    card.innerHTML = `
      <div class="p-name">${prodName(p)}</div>
      <div class="p-price">${euro(p.price)}</div>
      <div class="p-desc">${prodDesc(p)}</div>
      <button class="buy-btn" data-testid="buy-${p.id}">${t("buy")}</button>`;
    card.querySelector(".buy-btn").addEventListener("click", () => buyProduct(p, card));
    grid.appendChild(card);
  });
}

async function buyProduct(p, card) {
  const { ok, data } = await api("/api/buy", { pid: getPid(), product_id: p.id });
  if (!ok) { showToast(data.error || t("generic_error"), true); return; }
  SHOP_STATE = data.state;
  updateShopBalance();
  card.classList.remove("pop"); void card.offsetWidth; card.classList.add("pop");
  if (data.went_into_debt) {
    showToast(t("out_of_money"), true);
    setTimeout(() => showToast(t("discovered_debt"), true), 1600);
  } else {
    showToast(data.phrase);
  }
  announceAchievements(data.new_achievements);
}

async function initShop() {
  SHOP_STATE = await requireSession();
  if (!SHOP_STATE) return;
  document.getElementById("shop-title").textContent = t("shop_title", { name: SHOP_STATE.name });
  updateShopBalance();
  const { data } = await api("/api/catalog");
  CATALOG = data;
  ACTIVE_CAT = CATALOG.categories[0].key;
  renderCatNav();
  renderProducts();
}

/* ============================================================
   PAGINA: INVESTMENTS + GRAFICI
   ============================================================ */
let INV_STATE = null;
const RANGE_SEL = {};
const RANGES = [
  { key: "1g", sec: 86400 }, { key: "5g", sec: 432000 }, { key: "1m", sec: 2592000 },
  { key: "1a", sec: 31536000 }, { key: "5a", sec: 157680000 }, { key: "max", sec: Infinity },
];

function updateInvBalance() {
  document.getElementById("inv-balance").textContent = euro(INV_STATE.cash);
}

function buildChartSvg(company, rangeSec) {
  const W = 640, H = 220, padL = 54, padR = 48, padT = 14, padB = 26;
  const now = Date.now() / 1000;
  let pts = company.history || [];
  if (rangeSec !== Infinity) {
    const filtered = pts.filter((p) => p.t >= now - rangeSec);
    if (filtered.length >= 2) pts = filtered;
  }
  const ref = company.ref;
  if (!pts.length) pts = [{ t: now, p: company.price }];
  const prices = pts.map((p) => p.p);
  let min = Math.min(ref, ...prices), max = Math.max(ref, ...prices);
  if (min === max) { min -= min * 0.01 + 0.5; max += max * 0.01 + 0.5; }
  const range = max - min; min -= range * 0.12; max += range * 0.12;
  const t0 = pts[0].t, t1 = pts[pts.length - 1].t;
  const span = t1 - t0 || 1;
  const xFor = (tt) => padL + (W - padL - padR) * ((tt - t0) / span);
  const yFor = (pp) => padT + (max - pp) / (max - min) * (H - padT - padB);
  const bottom = H - padB;

  const last = prices[prices.length - 1];
  const up = last >= ref;
  const color = up ? "#3ddc84" : "#ff6b6b";

  let grid = "";
  for (let i = 0; i <= 4; i++) {
    const y = padT + (i / 4) * (H - padT - padB);
    const val = max - (i / 4) * (max - min);
    grid += `<line class="grid-line" x1="${padL}" y1="${y.toFixed(1)}" x2="${W - padR}" y2="${y.toFixed(1)}"/>`;
    grid += `<text class="axis-label" x="${padL - 8}" y="${(y + 4).toFixed(1)}" text-anchor="end">${axisNum(val)}</text>`;
  }

  const refY = yFor(ref);
  const refPill = `<g><rect class="ref-pill" x="${W - padR - 2}" y="${(refY - 11).toFixed(1)}" width="46" height="22" rx="6"/>` +
    `<text class="axis-label" x="${W - padR + 21}" y="${(refY + 4).toFixed(1)}" text-anchor="middle" style="fill:#c9ccff">${axisNum(ref)}</text></g>`;
  const refLine = `<line class="ref-line" x1="${padL}" y1="${refY.toFixed(1)}" x2="${W - padR}" y2="${refY.toFixed(1)}"/>`;

  const linePts = pts.map((p) => `${xFor(p.t).toFixed(1)},${yFor(p.p).toFixed(1)}`).join(" ");
  const areaD = `M ${xFor(pts[0].t).toFixed(1)},${bottom} ` +
    pts.map((p) => `L ${xFor(p.t).toFixed(1)},${yFor(p.p).toFixed(1)}`).join(" ") +
    ` L ${xFor(t1).toFixed(1)},${bottom} Z`;
  const area = `<path class="price-area" d="${areaD}" fill="${color}"/>`;
  const line = `<polyline class="price-line" points="${linePts}" stroke="${color}"/>`;

  const fmtTime = (tt) => new Date(tt * 1000).toLocaleTimeString(t("locale"), { hour: "2-digit", minute: "2-digit" });
  const tMid = t0 + span / 2;
  const xlabels =
    `<text class="axis-label" x="${padL}" y="${H - 6}" text-anchor="start">${fmtTime(t0)}</text>` +
    `<text class="axis-label" x="${((padL + (W - padR)) / 2).toFixed(1)}" y="${H - 6}" text-anchor="middle">${fmtTime(tMid)}</text>` +
    `<text class="axis-label" x="${W - padR}" y="${H - 6}" text-anchor="end">${fmtTime(t1)}</text>`;

  return `<svg class="chart-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
    ${grid}${area}${refLine}${line}${refPill}${xlabels}</svg>`;
}

function buildChartCard(company) {
  const sel = RANGE_SEL[company.id] || "1g";
  const ranges = RANGES.map((r) =>
    `<button class="range-btn ${r.key === sel ? "active" : ""}" data-range="${r.key}" data-cid="${company.id}">${t("r_" + r.key)}</button>`
  ).join("");
  const rSec = (RANGES.find((r) => r.key === sel) || RANGES[0]).sec;
  const svg = buildChartSvg(company, rSec);
  const dc = company.day_change;
  const stats = `<div class="chart-stats">
    <div class="cs"><span>${t("prev_close")}</span><b>${euro(company.ref, 2)}</b></div>
    <div class="cs"><span>${t("price_label")}</span><b>${euro(company.price, 2)}</b></div>
    <div class="cs"><span>${t("day_change")}</span><b class="${dc >= 0 ? "pos" : "neg"}">${dc >= 0 ? "+" : ""}${dc.toFixed(2)}%</b></div>
  </div>`;
  return `<div class="chart-card"><div class="chart-ranges">${ranges}</div>${svg}${stats}</div>`;
}

function renderMarket() {
  const wrap = document.getElementById("market-list");
  wrap.innerHTML = "";
  INV_STATE.market.forEach((c) => {
    const chgCls = c.change >= 0 ? "pos" : "neg";
    const chgTxt = (c.change >= 0 ? "+" : "") + c.change.toFixed(1) + "%";
    const div = document.createElement("div");
    div.className = "company" + (c.owned ? " owned" : "");
    div.dataset.testid = "company-" + c.id;

    let actions = "";
    if (c.owned) {
      actions = `<span class="owned-tag" data-testid="owned-${c.id}">${t("owned_tag")}</span>`;
    } else {
      const canBuyCompany = INV_STATE.cash >= c.market_cap;
      actions = `
        <input type="number" min="1" value="1" class="qty-input" data-testid="qty-${c.id}" />
        <button class="mini-btn buy-stock" data-testid="buy-stock-${c.id}">${t("buy_stock")}</button>
        <button class="mini-btn sell-stock" data-testid="sell-stock-${c.id}">${t("sell_stock")}</button>
        ${canBuyCompany ? `<button class="mini-btn buy-company" data-testid="buy-company-${c.id}">${t("buy_company", { value: euro(c.market_cap) })}</button>` : ""}`;
    }

    div.innerHTML = `
      <div class="company-top">
        <div>
          <div class="company-name">${c.name}</div>
          <div class="company-meta">${t("holdings", { shares: c.shares, value: euro(c.value), cap: euro(c.market_cap) })}</div>
        </div>
        <div class="company-price">${euro(c.price, 0)}<span class="chg ${chgCls}">${chgTxt}</span></div>
      </div>
      ${buildChartCard(c)}
      <div class="company-actions">${actions}</div>`;

    div.querySelectorAll(".range-btn").forEach((btn) => {
      btn.addEventListener("click", () => { RANGE_SEL[btn.dataset.cid] = btn.dataset.range; renderMarket(); });
    });
    if (!c.owned) {
      const qtyEl = div.querySelector(".qty-input");
      div.querySelector(".buy-stock").addEventListener("click", () => tradeStock("buy_stock", c, qtyEl));
      div.querySelector(".sell-stock").addEventListener("click", () => tradeStock("sell_stock", c, qtyEl));
      const bc = div.querySelector(".buy-company");
      if (bc) bc.addEventListener("click", () => buyCompany(c));
    }
    wrap.appendChild(div);
  });
}

async function tradeStock(kind, c, qtyEl) {
  const shares = Math.max(1, parseInt(qtyEl.value, 10) || 1);
  const { ok, data } = await api("/api/" + kind, { pid: getPid(), company_id: c.id, shares });
  if (!ok) { showToast(data.error || t("generic_error"), true); return; }
  INV_STATE = data.state;
  updateInvBalance();
  renderMarket();
  showToast(kind === "buy_stock" ? t("shares_bought") : t("shares_sold"));
  announceAchievements(data.new_achievements);
}

async function buyCompany(c) {
  if (!confirm(t("confirm_buy_company", { name: c.name, value: euro(c.market_cap) }))) return;
  const { ok, data } = await api("/api/buy_company", { pid: getPid(), company_id: c.id });
  if (!ok) { showToast(data.error || t("cant_afford"), true); return; }
  INV_STATE = data.state;
  updateInvBalance();
  renderMarket();
  showEvent({ title: t("congrats_title", { name: INV_STATE.name }), text: t("congrats_text", { company: data.company_name }) });
  announceAchievements(data.new_achievements);
}

async function initInvestments() {
  INV_STATE = await requireSession();
  if (!INV_STATE) return;
  updateInvBalance();
  renderMarket();
  setInterval(async () => {
    const { ok, data } = await api("/api/tick", { pid: getPid() });
    if (ok) {
      INV_STATE = data.state;
      updateInvBalance();
      renderMarket();
      await announceEvents(data.events);
      announceAchievements(data.new_achievements);
    }
  }, 6000);
}

/* ============================================================
   PAGINA: PORTFOLIO
   ============================================================ */
function renderPortfolio(state) {
  const b = state.breakdown;
  document.getElementById("w-cash").textContent = euro(b.cash, 2);
  document.getElementById("w-stocks").textContent = euro(b.stocks, 2);
  document.getElementById("w-companies").textContent = euro(b.companies, 2);
  document.getElementById("w-property").textContent = euro(b.property, 2);
  document.getElementById("w-objects").textContent = euro(b.objects, 2);
  document.getElementById("w-debt").textContent = euro(b.debt, 2);
  const nw = document.getElementById("pf-networth");
  nw.textContent = euro(state.net_worth, 2);
  nw.classList.remove("pop"); void nw.offsetWidth; nw.classList.add("pop");

  const wrap = document.getElementById("items-wrap");
  wrap.innerHTML = "";
  if (!state.inventory.length) {
    wrap.innerHTML = `<p class="empty">${t("empty_items")}</p>`;
  } else {
    const counts = {};
    state.inventory.forEach((it) => { counts[it.name] = (counts[it.name] || 0) + 1; });
    Object.entries(counts).forEach(([name, n]) => {
      const chip = document.createElement("span");
      chip.className = "item-chip";
      chip.innerHTML = `${name}<b>×${n}</b>`;
      wrap.appendChild(chip);
    });
  }

  const grid = document.getElementById("ach-grid");
  grid.innerHTML = "";
  state.achievements.forEach((a) => {
    const div = document.createElement("div");
    div.className = "ach" + (a.unlocked ? " unlocked" : "");
    div.dataset.testid = "ach-" + a.code;
    div.innerHTML = `<div class="a-name">${a.name}</div><div class="a-desc">${a.desc}</div>`;
    grid.appendChild(div);
  });
}

async function initPortfolio() {
  const state = await requireSession();
  if (!state) return;
  renderPortfolio(state);
  setInterval(async () => {
    const { ok, data } = await api("/api/tick", { pid: getPid() });
    if (ok) { renderPortfolio(data.state); await announceEvents(data.events); announceAchievements(data.new_achievements); }
  }, 8000);
}

/* ============================================================
   Router
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  applyI18n();
  initLangToggle();
  const page = document.body.dataset.page;
  if (page === "index") initIndex();
  else if (page === "bank") initBank();
  else if (page === "shop") initShop();
  else if (page === "investments") initInvestments();
  else if (page === "portfolio") initPortfolio();
});