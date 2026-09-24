/* ============================================================
   SOMETHING BANK — logica frontend (vanilla JS)
   Salvataggio locale: player_id salvato nel browser (localStorage),
   dati persistiti lato server in SQLite.
   ============================================================ */

const PID_KEY = "sb_pid";
const NAME_KEY = "sb_name";

const getPid = () => localStorage.getItem(PID_KEY);
const getName = () => localStorage.getItem(NAME_KEY) || "";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---------- Formattazione ---------- */
function euro(n, dec = 0) {
  const neg = n < 0;
  const abs = Math.abs(n);
  const s = abs.toLocaleString("it-IT", {
    minimumFractionDigits: dec,
    maximumFractionDigits: dec,
  });
  return (neg ? "-" : "") + "€" + s;
}
function euroSigned(n) {
  return (n >= 0 ? "+" : "-") + "€" + Math.abs(n).toLocaleString("it-IT", { maximumFractionDigits: 2 });
}

/* ---------- API ---------- */
async function api(path, body) {
  const opts = { method: body ? "POST" : "GET", headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

/* ---------- Toast / eventi ---------- */
function showToast(msg, isError = false) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.toggle("error", isError);
  t.classList.remove("hidden");
  requestAnimationFrame(() => t.classList.add("show"));
  clearTimeout(t._h);
  t._h = setTimeout(() => {
    t.classList.remove("show");
    setTimeout(() => t.classList.add("hidden"), 300);
  }, 2600);
}

function showEvent({ title, text, amount }) {
  const e = document.getElementById("event-toast");
  if (!e) return;
  let html = "";
  if (title) html += `<div class="e-title">${title}</div>`;
  if (text) html += `<div class="e-text">${text}</div>`;
  if (amount !== undefined && amount !== null) {
    const cls = amount >= 0 ? "pos" : "neg";
    html += `<div class="e-amt ${cls}">${euroSigned(amount)}</div>`;
  }
  e.innerHTML = html;
  e.classList.remove("hidden");
  requestAnimationFrame(() => e.classList.add("show"));
  clearTimeout(e._h);
  e._h = setTimeout(() => {
    e.classList.remove("show");
    setTimeout(() => e.classList.add("hidden"), 350);
  }, 4200);
}

async function announceEvents(events) {
  if (!events || !events.length) return;
  for (const ev of events) {
    if (ev.type === "market") {
      showEvent({ title: ev.company, text: ev.text, amount: null });
      const e = document.getElementById("event-toast");
      if (e) {
        const cls = ev.pct >= 0 ? "pos" : "neg";
        e.innerHTML += `<div class="e-amt ${cls}">${ev.pct >= 0 ? "+" : ""}${ev.pct}%</div>`;
      }
    } else {
      showEvent({ title: null, text: ev.text, amount: ev.amount });
    }
    await sleep(900);
  }
}

function announceAchievements(list) {
  if (!list || !list.length) return;
  list.forEach((a, i) => {
    setTimeout(() => showEvent({ title: "🏆 Achievement", text: a.name }), 400 + i * 1400);
  });
}

/* ---------- Guardia di sessione ---------- */
async function requireSession() {
  const pid = getPid();
  if (!pid) {
    window.location.href = "/";
    return null;
  }
  const { ok, data } = await api("/api/state?pid=" + encodeURIComponent(pid));
  if (!ok) {
    localStorage.removeItem(PID_KEY);
    localStorage.removeItem(NAME_KEY);
    window.location.href = "/";
    return null;
  }
  return data;
}

/* ============================================================
   PAGINA: INDEX (nome + intro)
   ============================================================ */
async function initIndex() {
  // Se già registrato, salta direttamente alla banca.
  if (getPid()) {
    const { ok } = await api("/api/state?pid=" + encodeURIComponent(getPid()));
    if (ok) {
      window.location.href = "/bank";
      return;
    }
    localStorage.removeItem(PID_KEY);
  }

  const form = document.getElementById("name-form");
  const input = document.getElementById("name-input");
  const errEl = document.getElementById("name-error");
  input.focus();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = input.value.trim();
    if (!name) {
      errEl.textContent = "Serve un nome. Anche uno inventato.";
      return;
    }
    errEl.textContent = "";
    const { ok, data } = await api("/api/register", { name });
    if (!ok) {
      errEl.textContent = data.error || "Qualcosa è andato storto.";
      return;
    }
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

  const lines = [
    `Ciao, ${name}.`,
    "Abbiamo aperto un conto a tuo nome.",
    "Abbiamo anche depositato €100.000.",
    "Non fare domande.",
  ];

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

  document.getElementById("start-button").addEventListener("click", () => {
    window.location.href = "/bank";
  });
}

/* ============================================================
   PAGINA: BANK
   ============================================================ */
function renderBank(state) {
  document.getElementById("account-name").textContent = state.name;
  const nw = document.getElementById("networth");
  nw.textContent = euro(state.net_worth, 2);
  nw.classList.remove("pop");
  void nw.offsetWidth;
  nw.classList.add("pop");

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
    const cls = h.amount >= 0 ? "pos" : "neg";
    li.innerHTML = `<span>${h.description}</span><span class="amt ${cls}">${euroSigned(h.amount)}</span>`;
    list.appendChild(li);
  });
}

async function initBank() {
  const state = await requireSession();
  if (!state) return;
  renderBank(state);

  document.getElementById("reset-btn").addEventListener("click", () => {
    if (confirm("Ricominciare da capo? Il progresso verrà dimenticato su questo browser.")) {
      localStorage.removeItem(PID_KEY);
      localStorage.removeItem(NAME_KEY);
      window.location.href = "/";
    }
  });

  setInterval(async () => {
    const { ok, data } = await api("/api/tick", { pid: getPid() });
    if (ok) {
      renderBank(data.state);
      await announceEvents(data.events);
      announceAchievements(data.new_achievements);
    }
  }, 7000);
}

/* ============================================================
   PAGINA: SHOP
   ============================================================ */
let SHOP_STATE = null;
let CATALOG = null;
let ACTIVE_CAT = null;

function updateShopBalance() {
  document.getElementById("shop-balance").textContent = euro(SHOP_STATE.cash);
}

function renderCatNav() {
  const nav = document.getElementById("cat-nav");
  nav.innerHTML = "";
  CATALOG.categories.forEach((cat) => {
    const chip = document.createElement("button");
    chip.className = "cat-chip" + (cat === ACTIVE_CAT ? " active" : "");
    chip.textContent = cat;
    chip.dataset.testid = "cat-" + cat;
    chip.addEventListener("click", () => {
      ACTIVE_CAT = cat;
      renderCatNav();
      renderProducts();
    });
    nav.appendChild(chip);
  });
}

function renderProducts() {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";
  CATALOG.products
    .filter((p) => p.category === ACTIVE_CAT)
    .forEach((p) => {
      const card = document.createElement("div");
      card.className = "product fade-in";
      card.innerHTML = `
        <div class="p-name">${p.name}</div>
        <div class="p-price">${euro(p.price)}</div>
        <div class="p-desc">${p.description}</div>
        <button class="buy-btn" data-testid="buy-${p.id}">COMPRA</button>`;
      card.querySelector(".buy-btn").addEventListener("click", () => buyProduct(p, card));
      grid.appendChild(card);
    });
}

async function buyProduct(p, card) {
  const { ok, data } = await api("/api/buy", { pid: getPid(), product_id: p.id });
  if (!ok) {
    showToast(data.error || "Errore.", true);
    return;
  }
  SHOP_STATE = data.state;
  updateShopBalance();
  card.classList.remove("pop");
  void card.offsetWidth;
  card.classList.add("pop");

  if (data.went_into_debt) {
    showToast("Hai finito i soldi.", true);
    setTimeout(() => showToast("Hai scoperto il debito.", true), 1600);
  } else {
    showToast(data.phrase);
  }
  announceAchievements(data.new_achievements);
}

async function initShop() {
  SHOP_STATE = await requireSession();
  if (!SHOP_STATE) return;
  document.getElementById("shop-title").textContent = `Cosa vuoi comprare, ${SHOP_STATE.name}?`;
  updateShopBalance();

  const { data } = await api("/api/catalog");
  CATALOG = data;
  ACTIVE_CAT = CATALOG.categories[0];
  renderCatNav();
  renderProducts();
}

/* ============================================================
   PAGINA: INVESTMENTS
   ============================================================ */
let INV_STATE = null;

function updateInvBalance() {
  document.getElementById("inv-balance").textContent = euro(INV_STATE.cash);
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
      actions = `<span class="owned-tag" data-testid="owned-${c.id}">TUA</span>`;
    } else {
      const canBuyCompany = INV_STATE.cash >= c.market_cap;
      actions = `
        <input type="number" min="1" value="1" class="qty-input" data-testid="qty-${c.id}" />
        <button class="mini-btn buy-stock" data-testid="buy-stock-${c.id}">Compra</button>
        <button class="mini-btn sell-stock" data-testid="sell-stock-${c.id}">Vendi</button>
        ${canBuyCompany
          ? `<button class="mini-btn buy-company" data-testid="buy-company-${c.id}">ACQUISTA AZIENDA (${euro(c.market_cap)})</button>`
          : ""}`;
    }

    div.innerHTML = `
      <div class="company-top">
        <div>
          <div class="company-name">${c.name}</div>
          <div class="company-meta">Possiedi ${c.shares} azioni · valore ${euro(c.value)} · cap. ${euro(c.market_cap)}</div>
        </div>
        <div class="company-price">${euro(c.price, 0)}<span class="chg ${chgCls}">${chgTxt}</span></div>
      </div>
      <div class="company-actions">${actions}</div>`;

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
  if (!ok) {
    showToast(data.error || "Errore.", true);
    return;
  }
  INV_STATE = data.state;
  updateInvBalance();
  renderMarket();
  showToast(kind === "buy_stock" ? "Azioni acquistate." : "Azioni vendute.");
  announceAchievements(data.new_achievements);
}

async function buyCompany(c) {
  if (!confirm(`Comprare l'intera ${c.name} per ${euro(c.market_cap)}?`)) return;
  const { ok, data } = await api("/api/buy_company", { pid: getPid(), company_id: c.id });
  if (!ok) {
    showToast(data.error || "Non puoi permettertelo.", true);
    return;
  }
  INV_STATE = data.state;
  updateInvBalance();
  renderMarket();
  const nm = data.company_name;
  showEvent({ title: `Congratulazioni, ${INV_STATE.name}.`, text: `Ora possiedi ${nm}. Non sappiamo cosa tu debba farci.` });
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
  nw.classList.remove("pop");
  void nw.offsetWidth;
  nw.classList.add("pop");

  // Oggetti raggruppati
  const wrap = document.getElementById("items-wrap");
  wrap.innerHTML = "";
  if (!state.inventory.length) {
    wrap.innerHTML = `<p class="empty">Ancora niente. La sobrietà è una scelta.</p>`;
  } else {
    const counts = {};
    state.inventory.forEach((it) => {
      counts[it.name] = (counts[it.name] || 0) + 1;
    });
    Object.entries(counts).forEach(([name, n]) => {
      const chip = document.createElement("span");
      chip.className = "item-chip";
      chip.innerHTML = `${name}<b>×${n}</b>`;
      wrap.appendChild(chip);
    });
  }

  // Achievement
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
    if (ok) {
      renderPortfolio(data.state);
      await announceEvents(data.events);
      announceAchievements(data.new_achievements);
    }
  }, 8000);
}

/* ============================================================
   Router
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;
  if (page === "index") initIndex();
  else if (page === "bank") initBank();
  else if (page === "shop") initShop();
  else if (page === "investments") initInvestments();
  else if (page === "portfolio") initPortfolio();
});