# Login and place an order on the website
# Consent overlay is blocked at the network level by conftest.py — no manual dismiss needed.
# All credentials loaded from environment variables (.env) — never hardcoded.

import os

import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.payment_page import PaymentPage
from pages.product_page import ProductPage


def _valid_user() -> dict:
    """Return valid user credentials from environment variables.

    Skips the test gracefully when required env vars are missing.
    """
    user = {
        "name": os.environ.get("TEST_USER_NAME", ""),
        "email": os.environ.get("TEST_USER_EMAIL", ""),
        "password": os.environ.get("TEST_USER_PASSWORD", ""),
    }
    missing = [k for k, v in user.items() if not v]
    if missing:
        pytest.skip(
            f"Missing env vars: {', '.join(f'TEST_USER_{k.upper()}' for k in missing)}. "
            "Copy .env.example → .env and fill in test values."
        )
    return user


def _card_details() -> dict:
    """Load card details from environment variables.

    Skips the test gracefully when required env vars are missing.
    """
    card = {
        "name": os.environ.get("CARD_NAME", ""),
        "number": os.environ.get("CARD_NUMBER", ""),
        "cvc": os.environ.get("CARD_CVC", ""),
        "month": os.environ.get("CARD_EXPIRY_MONTH", ""),
        "year": os.environ.get("CARD_EXPIRY_YEAR", ""),
    }
    missing = [k for k, v in card.items() if not v]
    if missing:
        pytest.skip(
            f"Missing card env vars: {', '.join(f'CARD_{k.upper()}' for k in missing)}. "
            "Copy .env.example → .env and fill in test values."
        )
    return card


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.checkout
def test_order_flow(page: Page) -> None:
    """End-to-end: login → browse → add to cart → checkout → payment → logout."""
    user = _valid_user()
    card = _card_details()

    # --- Login ---
    home_page = HomePage(page)
    home_page.navigate_to_login()

    login_page = LoginPage(page)
    login_page.login(user["email"], user["password"])

    # --- Add product to cart via detail page (reliable across all browsers) ---
    product_page = ProductPage(page)
    product_page.add_product_via_detail_page(product_id=33)

    # --- Verify cart and proceed to checkout ---
    cart_page = CartPage(page)
    cart_page.navigate_to_cart()
    cart_page.verify_has_items()
    cart_page.proceed_to_checkout()

    # --- Checkout → Place Order ---
    checkout_page = CheckoutPage(page)
    checkout_page.ensure_on_checkout()
    checkout_page.place_order()

    # --- Payment ---
    payment_page = PaymentPage(page)
    payment_page.fill_card_details(card)
    payment_page.pay_and_confirm()

    # --- Logout and verify ---
    payment_page.continue_after_payment()
    payment_page.logout()
    payment_page.verify_on_login_page()
