# Login and place an order on the website
# Consent overlay is blocked at the network level by conftest.py — no manual dismiss needed.
# All credentials loaded from environment variables (.env) — never hardcoded.

import os

import pytest
from playwright.sync_api import Page, expect


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

    # Login
    page.get_by_role("link", name=" Signup / Login").click()
    page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(
        user["email"]
    )
    page.get_by_role("textbox", name="Password").fill(user["password"])
    page.get_by_role("button", name="Login").click()

    # Browse Men → Jeans and add a product to cart
    # Navigate directly to the category page — sidebar accordion clicks are
    # unreliable across browsers (the anchor #Men doesn't expand the panel).
    page.goto("https://automationexercise.com/category_products/6", wait_until="domcontentloaded")
    add_btn = page.locator(".productinfo .add-to-cart").first
    add_btn.wait_for(state="visible", timeout=15000)
    add_btn.scroll_into_view_if_needed()
    add_btn.click()

    # View cart and proceed to checkout
    # After adding to cart, a modal with "View Cart" may appear.
    # In Firefox the modal link can stay hidden, so fall back to direct navigation.
    modal_link = page.locator("a[href='/view_cart']:has-text('View Cart')")
    try:
        modal_link.wait_for(state="visible", timeout=10000)
        modal_link.click()
    except Exception:
        page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded")
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#cart_items tbody tr").first).to_be_visible(timeout=15000)
    page.get_by_text("Proceed To Checkout").click()

    # Payment — card details from env vars, never hardcoded
    # Wait for 'Place Order' link to be visible before clicking
    page.get_by_role("link", name="Place Order").wait_for(state="visible", timeout=15000)
    page.get_by_role("link", name="Place Order").click()
    page.locator('input[name="name_on_card"]').fill(card["name"])
    page.locator('input[name="card_number"]').fill(card["number"])
    page.get_by_role("textbox", name="ex.").fill(card["cvc"])
    page.get_by_role("textbox", name="MM").fill(card["month"])
    page.get_by_role("textbox", name="YYYY").fill(card["year"])
    page.get_by_role("button", name="Pay and Confirm Order").click()
    expect(page.locator("#form")).to_contain_text("Congratulations! Your order has been confirmed!")

    # Logout and verify we land back on the login page
    page.get_by_role("link", name="Continue").click()
    page.get_by_role("link", name=" Logout").click()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()
    expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()
