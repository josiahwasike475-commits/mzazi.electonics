# Mzazi Electronics — delivery outcomes

## 1. Brand shell and responsive navigation

- Use the Mzazi Electronics identity with white `#FFFFFFFFF`, orange `#F97316`, green `#0F172A`, and blue `#0F172A`.
- Provide a responsive header with logo, Home, Shop, Categories, Oraimo, Amaya, About Us, Contact Us, search, account, cart, and a mobile hamburger menu.
- Provide a footer with logo, business description, quick links, categories, Oraimo, Amaya, contact information, WhatsApp link, payment information, and `© 2026 Mzazi Electronics. All Rights Reserved.`
- Include a branded favicon set and `manus-routes.json` route manifest.

## 2. Storefront discovery and catalogue

- Create a homepage with the required hero message, Shop Now / Explore Oraimo / Chat With Us CTAs, Featured Products, Popular Categories, Best Sellers, New Arrivals, Oraimo Accessories, Amaya Products, Special Offers, Why Choose Mzazi Electronics, Customer Support, and newsletter subscription sections.
- Support the product families Phones and Accessories, Oraimo Accessories, Amaya Products, Computers and Accessories, Home Electronics, and Networking and Security.
- Each product card displays image, name, brand, KSh price, previous price/discount when configured, stock state, Add to Cart, Buy Now, and View Details.
- Support search, category filtering, brand filtering, price filtering, sorting by price/newest/popularity, and pagination behavior.
- Do not invent real prices, stock quantities, or customer reviews; product values are administrator-controlled and demo records are explicitly marked.

## 3. Product detail and cart

- Product details include product name, images, brand, model, price, description, technical specifications, stock, warranty, quantity, Add to Cart, Buy Now, Buy via WhatsApp, and related products.
- Cart supports add/remove, quantity changes, automatic subtotals/total, product imagery, Continue Shopping, and Proceed to Checkout.
- Persist the cart while navigating between pages.

## 4. Checkout and WhatsApp enquiry

- Collect full name, phone, optional email, delivery location, and additional instructions.
- Show line items, quantities, unit prices, subtotal, delivery fee, total, unique order number, and payment methods M-Pesa STK Push and WhatsApp order enquiry.
- Float a WhatsApp action on every page using `https://wa.me/254786163265` and prepare product/order enquiry messages with name, price, quantity, and order reference when available.

## 5. M-Pesa payment foundation

- Keep Daraja credentials server-side using `MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`, `MPESA_SHORTCODE`, `MPESA_PASSKEY`, `MPESA_CALLBACK_URL`, and `MPESA_ENVIRONMENT`.
- Implement access-token generation, STK password/timestamp, STK request, callback endpoint, amount/reference/receipt validation, status tracking, duplicate prevention, and Pending / Successful / Failed / Cancelled states.
- Mark an order paid only after a validated successful callback; do not claim live payment readiness until Safaricom credentials and callbacks are tested.

## 6. Accounts and customer orders

- Provide customer registration, login, logout, password reset, profile, order history, order tracking, and saved delivery information with protected personal information.

## 7. Admin, inventory, and reporting

- Provide a secure admin/dashboard view with total sales, total orders, pending/completed orders, customers, products, low-stock products, and successful M-Pesa payments.
- Allow product add/edit/delete, image upload, descriptions, prices, discounts, stock, categories, brands, and warranty fields.
- Allow order detail viewing, customer information, order status updates, delivery confirmation, cancellation, and invoice printing.
- Show payment customer/name/phone/order/amount/receipt/date/status.
- Track stock, reduce stock after confirmed orders, alert on low stock, adjust stock, and retain stock history.
- Support customer viewing/order/contact management and daily, weekly, monthly, annual, product performance, and payment reports with PDF/Excel export paths.

## 8. Security and operations

- Use Django authentication, hashed passwords, CSRF protection, input validation, permission checks, secure file uploads, environment-based secrets, duplicate-order/payment protections, and never store M-Pesa PINs.
- Keep deployment-ready settings for PostgreSQL and HTTPS; verify the project builds and the Preview server listens on port 3000.

## 9. On-page AI shopping assistant

- Provide a visible Mza AI assistant on customer-facing pages.
- Ground responses in the administrator-managed catalogue and business facts.
- Do not invent price, stock, reviews, delivery promises, warranties, specifications, or a physical address.
- Keep model credentials server-side and offer WhatsApp handoff for live confirmation.
