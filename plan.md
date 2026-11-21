# Mzazi Electronics — implementation plan

## Scope

Build a polished, responsive Kenyan electronics storefront and management-ready Django application for Mzazi Electronics, owned by Josiah Wasike. The first delivered slice prioritizes the customer-facing shopping experience and the data foundations required for products, orders, accounts, inventory, and payment wiring. Prices, stock, reviews, shop address, and M-Pesa credentials remain administrator/configuration controlled rather than invented.

## Implementation approach

- **Backend:** Django project with SQLite for local development, Django ORM models for products, brands, categories, orders, order lines, and payment attempts, and Django admin registration for management. PostgreSQL can be selected through `DATABASE_URL` in deployment.
- **Frontend:** Django templates with a small, dependency-light JavaScript layer for catalogue filtering, cart persistence, quick-view modal, checkout state, and dashboard interactions. CSS is custom and responsive, using the supplied white/orange/green/blue palette.
- **Payments:** Daraja STK Push service module with server-side environment variables, timestamp/password generation, callback endpoint, amount/account validation, idempotency checks, and explicit unconfigured/failed states. No order is marked paid from an STK request alone.
- **Data and safety:** Demo catalogue records are clearly marked as sample data with zero assumed stock/prices; production credentials and M-Pesa secrets are never placed in client code. CSRF, Django authentication, input validation, protected admin routes, and upload constraints are part of the structure.
- **Routes:** Home, shop, category landing pages, product detail, cart, checkout, order status, account, about, contact, and dashboard pages, plus JSON endpoints for catalogue/cart/order/payment handoff.

## Design direction

### Style options

- **Probability 0.06 — Nairobi Signal:** energetic, editorial commerce with bold color blocks and ticker-like category navigation.
- **Probability 0.05 — Quiet Utility:** restrained white space, monochrome product photography, and minimal green/orange accents.
- **Probability 0.04 — Modern Market Grid:** modular, high-contrast retail panels inspired by Kenyan storefront signage.

**Chosen direction: Nairobi Signal.** It fits the business brief, feels local and confident, and gives electronics a clear, shoppable visual rhythm without overcrowding.

- **Design movement:** contemporary African retail editorial with Swiss-influenced grids, confident labels, and tactile card surfaces.
- **Core principles:** fast scanning, clear trust signals, warm human support, and intentional color hierarchy.
- **Color philosophy:** white creates clean product space; blue anchors credibility; orange creates action and momentum; green is reserved for WhatsApp, availability, and verified success.
- **Layout paradigm:** asymmetric split hero, horizontal category rail, and dense-but-breathable product shelves rather than a generic centered marketing stack.
- **Signature elements:** orange “signal” bars, a rounded electric-blue status pill, and green WhatsApp support dock.
- **Interaction philosophy:** every important interaction answers one question immediately: what is it, what does it cost, can I get it, and how do I ask Josiah?
- **Animation:** 160–240ms transitions, lift-on-hover cards, soft reveal for modal/detail panels, and no looping decorative motion that competes with product decisions.
- **Typography:** Plus Jakarta Sans for UI/body, Space Grotesk for display headings and brand lockups; uppercase micro-labels use tight tracking.
- **Brand essence:** practical, trustworthy electronics for everyday Kenyan life; personality: bright, capable, welcoming.
- **Brand voice:** direct and useful. Example lines: “Power your everyday.” and “Need a real answer? Chat with Josiah.”
- **Wordmark/logo:** an `mza` monogram in a rounded signal badge paired with “Electronics”; the mark uses a small cart-wave accent rather than a generic shopping bag.
- **Signature brand color:** Mzazi Orange `#FF7900`.

## Project structure

```text
mzazishop/
├── manage.py
├── requirements.txt
├── .env.example
├── mzazi_config/          # Django settings, URLs, WSGI
├── core/                  # shared pages, settings, JSON helpers
├── catalog/               # product, brand, category, API and admin models
├── orders/                # checkout, order models, cart helpers, payment states
├── accounts/              # account/profile views and auth integration
├── dashboard/             # protected management overview and reports
├── templates/             # reusable layouts and page templates
├── static/css/            # responsive brand system
├── static/js/             # catalogue/cart/dashboard interactions
├── static/images/         # logo, favicon and lightweight visual assets
├── plan.md
├── TODO.md
└── public/manus-routes.json
```

## Serving and delivery

Run `python manage.py runserver 0.0.0.0:3000` in Preview. Keep browser URLs relative and serve `public/manus-routes.json` from Django/static routing. Use a future production WSGI server behind HTTPS; configure `ALLOWED_HOSTS`, secure cookies, PostgreSQL, storage, and Daraja secrets through environment variables before production launch.
