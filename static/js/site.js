(() => {
  const catalogNode = document.getElementById('catalog-data');
  const products = catalogNode ? JSON.parse(catalogNode.textContent) : [];

  const byId = id => products.find(product => String(product.id) === String(id));
  const money = value => value ? `KSh ${Number(value).toLocaleString('en-KE', { maximumFractionDigits: 0 })}` : 'Price on request';
  const getCart = () => {
    try { return JSON.parse(localStorage.getItem('mzazi-cart-v1') || '[]'); }
    catch { return []; }
  };
  const setCart = cart => {
    localStorage.setItem('mzazi-cart-v1', JSON.stringify(cart));
    updateCartCount();
  };
  const updateCartCount = () => {
    const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
    document.querySelectorAll('[data-cart-count]').forEach(node => { node.textContent = count; });
  };
  const toast = message => {
    const node = document.createElement('div');
    node.className = 'site-toast';
    node.textContent = message;
    document.body.appendChild(node);
    requestAnimationFrame(() => node.classList.add('is-visible'));
    setTimeout(() => {
      node.classList.remove('is-visible');
      setTimeout(() => node.remove(), 250);
    }, 2600);
  };
  const addToCart = (id, quantity = 1) => {
    const cart = getCart();
    const item = cart.find(row => String(row.id) === String(id));
    if (item) item.quantity += quantity;
    else cart.push({ id: Number(id), quantity });
    setCart(cart);
    toast('Added to your cart');
  };
  const removeFromCart = id => setCart(getCart().filter(item => String(item.id) !== String(id)));
  const changeQuantity = (id, delta) => {
    const cart = getCart();
    const item = cart.find(row => String(row.id) === String(id));
    if (!item) return;
    item.quantity = Math.max(1, item.quantity + delta);
    setCart(cart);
    renderCartPage();
    renderCheckoutSummary();
  };
  const artClass = product => `product-art product-art--${product.category_slug}`;
  const artIcon = product => product.category.includes('Oraimo') ? '◉' : product.category.includes('Phone') ? '▱' : product.category.includes('Computer') ? '▰' : product.category.includes('Home') ? '⌂' : '◌';
  const productArt = product => `<div class="${artClass(product)}"><span class="product-art__tag">${product.brand}</span><span class="product-art__icon">${artIcon(product)}</span><span class="product-art__line">${product.category}</span></div>`;

  function updateSummary(total) {
    const text = total ? money(total) : 'Price on request';
    document.querySelectorAll('[data-cart-subtotal],[data-checkout-subtotal]').forEach(node => { node.textContent = total ? money(total) : 'Price on request'; });
    document.querySelectorAll('[data-cart-total],[data-checkout-total]').forEach(node => { node.textContent = text; });
  }

  function renderCartPage() {
    const list = document.querySelector('[data-cart-items]');
    if (!list) return;
    const cart = getCart().map(item => ({ ...item, product: byId(item.id) })).filter(item => item.product);
    if (!cart.length) {
      list.innerHTML = '<div class="empty-state"><span>⌁</span><h3>Your cart is waiting.</h3><p>Add a few essentials and they’ll show up here.</p><a class="button button--orange" href="/shop/">Start shopping ↗</a></div>';
      updateSummary(0);
      return;
    }
    list.innerHTML = cart.map(({ product, quantity }) => `<div class="cart-item"><div class="cart-item__visual">${productArt(product)}</div><div><div class="eyebrow">${product.brand} · ${product.category}</div><h3>${product.name}</h3><small>${product.price ? money(product.price) : 'Price confirmed on request'}</small><div class="cart-item__controls"><button type="button" data-cart-minus="${product.id}">−</button><span>${quantity}</span><button type="button" data-cart-plus="${product.id}">+</button><button class="cart-item__remove" type="button" data-cart-remove="${product.id}">Remove</button></div></div><div class="cart-item__price"><strong>${product.price ? money(product.price * quantity) : 'On request'}</strong></div></div>`).join('');
    updateSummary(cart.reduce((total, item) => total + (item.product.price || 0) * item.quantity, 0));
    bindCartControls();
  }

  function bindCartControls() {
    document.querySelectorAll('[data-cart-minus]').forEach(button => button.addEventListener('click', () => changeQuantity(button.dataset.cartMinus, -1)));
    document.querySelectorAll('[data-cart-plus]').forEach(button => button.addEventListener('click', () => changeQuantity(button.dataset.cartPlus, 1)));
    document.querySelectorAll('[data-cart-remove]').forEach(button => button.addEventListener('click', () => { removeFromCart(button.dataset.cartRemove); renderCartPage(); renderCheckoutSummary(); }));
  }

  function renderCheckoutSummary() {
    const list = document.querySelector('[data-checkout-items]');
    if (!list) return;
    const cart = getCart().map(item => ({ ...item, product: byId(item.id) })).filter(item => item.product);
    list.innerHTML = cart.length ? cart.map(({ product, quantity }) => `<div class="summary-row"><span>${quantity} × ${product.name}</span><strong>${product.price ? money(product.price * quantity) : 'On request'}</strong></div>`).join('') : '<p class="panel-note">Your cart is empty. <a href="/shop/">Browse the shop.</a></p>';
    updateSummary(cart.reduce((total, item) => total + (item.product.price || 0) * item.quantity, 0));
  }

  function openQuickView(id) {
    const product = byId(id);
    if (!product) return;
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `<div class="quick-modal" role="dialog" aria-modal="true"><button class="quick-modal__close" type="button" aria-label="Close">×</button><div class="quick-modal__visual">${productArt(product)}</div><div class="quick-modal__body"><span class="eyebrow">${product.brand} · ${product.category}</span><h2>${product.name}</h2><p>${product.description}</p><div class="product-detail__price"><strong>${money(product.price)}</strong></div><button class="button button--orange" data-modal-add="${product.id}">Add to cart ↗</button></div></div>`;
    document.body.appendChild(backdrop);
    const close = () => backdrop.remove();
    backdrop.addEventListener('click', event => { if (event.target === backdrop || event.target.closest('.quick-modal__close')) close(); });
    backdrop.querySelector('[data-modal-add]').addEventListener('click', () => { addToCart(id); close(); });
  }

  function bindProductActions() {
    document.querySelectorAll('[data-add-to-cart]').forEach(button => button.addEventListener('click', () => addToCart(button.dataset.addToCart, Number(document.querySelector('[data-product-quantity]')?.value || 1))));
    document.querySelectorAll('[data-quick-view]').forEach(button => button.addEventListener('click', () => openQuickView(button.dataset.quickView)));
  }

  function initFilters() {
    const grid = document.querySelector('[data-shop-grid]');
    if (!grid) return;
    const cards = [...grid.querySelectorAll('[data-product-card]')];
    const apply = () => {
      const query = document.querySelector('[data-shop-search]')?.value.toLowerCase().trim() || '';
      const categories = [...document.querySelectorAll('[data-category-filter]:checked')].map(input => input.value);
      const brands = [...document.querySelectorAll('[data-brand-filter]:checked')].map(input => input.value);
      const prices = [...document.querySelectorAll('[data-price-filter]:checked')].map(input => input.value);
      let visible = 0;
      cards.forEach(card => {
        const matches = (!query || card.dataset.name.includes(query) || card.dataset.brand.includes(query)) && (!categories.length || categories.includes(card.dataset.category)) && (!brands.length || brands.some(brand => card.dataset.brand.includes(brand))) && (!prices.length || prices.includes(Number(card.dataset.price) > 0 ? 'priced' : 'request'));
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      const count = document.querySelector('[data-results-count]');
      if (count) count.textContent = visible;
      const empty = document.querySelector('[data-empty-state]');
      if (empty) empty.hidden = visible !== 0;
    };
    document.querySelectorAll('[data-shop-search],[data-category-filter],[data-brand-filter],[data-price-filter]').forEach(input => input.addEventListener('input', apply));
    document.querySelector('[data-clear-filters]')?.addEventListener('click', () => {
      document.querySelectorAll('[data-shop-search]').forEach(input => { input.value = ''; });
      document.querySelectorAll('[data-category-filter],[data-brand-filter],[data-price-filter]').forEach(input => { input.checked = false; });
      apply();
    });
    document.querySelector('[data-sort-products]')?.addEventListener('change', event => {
      const sorted = [...cards].sort((a, b) => {
        if (event.target.value === 'price-low') return Number(a.dataset.price) - Number(b.dataset.price);
        if (event.target.value === 'price-high') return Number(b.dataset.price) - Number(a.dataset.price);
        if (event.target.value === 'popular') return Number(b.dataset.popularity) - Number(a.dataset.popularity);
        return 0;
      });
      sorted.forEach(card => grid.appendChild(card));
      apply();
    });
    const params = new URLSearchParams(window.location.search);
    if (params.get('q')) {
      const search = document.querySelector('[data-shop-search]');
      search.value = params.get('q');
    }
    apply();
  }

  function initCheckout() {
    const form = document.querySelector('[data-checkout-form]');
    if (!form) return;
    renderCheckoutSummary();
    document.querySelectorAll('.payment-choice').forEach(choice => choice.addEventListener('click', () => {
      document.querySelectorAll('.payment-choice').forEach(row => row.classList.remove('is-selected'));
      choice.classList.add('is-selected');
      choice.querySelector('input').checked = true;
    }));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const message = form.querySelector('[data-checkout-message]');
      const cart = getCart();
      if (!cart.length) { message.textContent = 'Your cart is empty. Add an item before checking out.'; return; }
      const data = new FormData(form);
      const payload = {
        customer: { name: data.get('name'), phone: data.get('phone'), email: data.get('email'), location: data.get('location'), instructions: data.get('instructions') },
        items: cart,
        payment_method: data.get('payment_method'),
        idempotency_key: `web-${Date.now()}-${Math.random().toString(16).slice(2)}`
      };
      const button = form.querySelector('button[type=submit]');
      button.disabled = true;
      button.textContent = 'Creating order…';
      try {
        const response = await fetch('/api/orders/', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '' }, body: JSON.stringify(payload) });
        const result = await response.json();
        if (!response.ok || !result.ok) throw new Error(result.message || 'We could not create the order.');
        setCart([]);
        window.location.href = result.status_url;
      } catch (error) {
        message.textContent = error.message;
        button.disabled = false;
        button.innerHTML = 'Place order <span>↗</span>';
      }
    });
  }

  function initNewsletter() {
    document.querySelectorAll('[data-newsletter-form]').forEach(form => form.addEventListener('submit', async event => {
      event.preventDefault();
      const message = form.querySelector('[data-newsletter-message]');
      const email = form.querySelector('input[name=email]').value;
      try {
        const response = await fetch('/newsletter/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': document.querySelector('meta[name=csrf-token]')?.content || '' }, body: new URLSearchParams({ email }) });
        const result = await response.json();
        message.textContent = result.message;
        form.reset();
      } catch { message.textContent = 'Thanks — we’ll keep you posted.'; }
    }));
  }

  function initAssistant() {
    const toggle = document.querySelector('[data-assistant-toggle]');
    const panel = document.querySelector('[data-assistant-panel]');
    const close = document.querySelector('[data-assistant-close]');
    const form = document.querySelector('[data-assistant-form]');
    const messages = document.querySelector('[data-assistant-messages]');
    const suggestions = document.querySelector('[data-assistant-suggestions]');
    if (!toggle || !panel || !form || !messages) return;
    const history = [];
    const addMessage = (text, role) => {
      const node = document.createElement('div');
      node.className = `assistant-message assistant-message--${role}`;
      node.textContent = text;
      messages.appendChild(node);
      messages.scrollTop = messages.scrollHeight;
      return node;
    };
    const setOpen = open => {
      panel.hidden = !open;
      toggle.hidden = open;
      toggle.setAttribute('aria-expanded', String(open));
      if (open) form.querySelector('input')?.focus();
    };
    toggle.addEventListener('click', () => setOpen(true));
    close?.addEventListener('click', () => setOpen(false));
    suggestions?.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
      form.querySelector('input').value = button.textContent;
      form.requestSubmit();
    }));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const input = form.querySelector('input');
      const message = input.value.trim();
      if (!message) return;
      addMessage(message, 'user');
      history.push({ role: 'user', content: message });
      input.value = '';
      input.disabled = true;
      const typing = addMessage('Mza AI is checking the catalogue…', 'bot assistant-message--typing');
      try {
        const response = await fetch('/api/assistant/', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('meta[name=csrf-token]')?.content || '' }, body: JSON.stringify({ message, history }) });
        const result = await response.json();
        typing.remove();
        const reply = result.reply || 'I could not answer that just now. Please chat with Josiah on WhatsApp.';
        addMessage(reply, 'bot');
        history.push({ role: 'assistant', content: reply });
      } catch {
        typing.remove();
        addMessage('I’m having trouble connecting. Please chat with Josiah on WhatsApp for a quick answer.', 'bot');
      } finally {
        input.disabled = false;
        input.focus();
      }
    });
  }
  function initLivePhoneClock() {
    const timeNode = document.querySelector('[data-live-time]');
    const dateNode = document.querySelector('[data-live-date]');
    if (!timeNode || !dateNode) return;
    const update = () => {
      const now = new Date();
      timeNode.textContent = new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(now);
      dateNode.textContent = new Intl.DateTimeFormat(undefined, { weekday: 'short', day: 'numeric', month: 'short' }).format(now);
    };
    update();
    window.setInterval(update, 1000);
  }

  document.querySelector('[data-menu-button]')?.addEventListener('click', () => document.querySelector('[data-nav]').classList.toggle('is-open'));
  document.querySelector('[data-global-search]')?.addEventListener('keydown', event => { if (event.key === 'Enter' && event.target.value.trim()) window.location.href = `/shop/?q=${encodeURIComponent(event.target.value.trim())}`; });
  document.querySelector('[data-quantity-minus]')?.addEventListener('click', () => { const input = document.querySelector('[data-product-quantity]'); input.value = Math.max(1, Number(input.value) - 1); });
  document.querySelector('[data-quantity-plus]')?.addEventListener('click', () => { const input = document.querySelector('[data-product-quantity]'); input.value = Number(input.value) + 1; });
  updateCartCount();
  bindProductActions();
  renderCartPage();
  initFilters();
  initCheckout();
  initNewsletter();
  initAssistant();
  initLivePhoneClock();
})();
