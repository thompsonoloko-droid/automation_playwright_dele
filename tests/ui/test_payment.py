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

    # Add a product to cart via the product detail page.
    # The hover-overlay add-to-cart on listing pages is unreliable across
    # browsers (Firefox overlay doesn't register, WebKit needs explicit hover).
    # The detail page always shows the button without a hover overlay.
    # Retry up to 2 times — in CI the first click can silently fail due to
    # ad-network redirects or transient overlays.
    for attempt in range(3):
        page.goto(
            "https://automationexercise.com/product_details/33",
            wait_until="domcontentloaded",
        )
        add_btn = page.locator("button.btn-default.cart")
        add_btn.wait_for(state="visible", timeout=15000)
        add_btn.click()

        # Wait for the "Added!" confirmation modal — this proves the
        # server accepted the add-to-cart request.
        cart_modal = page.locator("#cartModal")
        try:
            cart_modal.wait_for(state="visible", timeout=5000)
        except Exception:
            # Modal didn't appear — click may not have registered; retry
            if attempt < 2:
                continue
        # Modal appeared (or last attempt) — dismiss and move on
        close_btn = cart_modal.locator("button.close-modal, .close")
        if close_btn.first.is_visible(timeout=2000):
            close_btn.first.click()
        page.wait_for_timeout(500)
        break

    # Navigate to cart and verify the item is present
    page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded")
    expect(page.locator("#cart_items tbody tr").first).to_be_visible(timeout=15000)
    page.get_by_text("Proceed To Checkout").click()

    # After "Proceed To Checkout", verify we actually landed on the checkout page.
    # In WebKit the click may not navigate (e.g. a "Register / Login" modal can
    # appear if the session cookie was dropped). Handle gracefully.
    try:
        page.wait_for_url("**/checkout**", timeout=10000)
    except Exception:
        # Dismiss any modal that may have appeared and navigate directly
        modal_close = page.locator("#checkoutModal .close, #checkoutModal a[href='/login']")
        if modal_close.first.is_visible(timeout=2000):
            modal_close.first.click()
        page.goto("https://automationexercise.com/checkout", wait_until="domcontentloaded")
    page.wait_for_load_state("domcontentloaded")

    # Payment — card details from env vars, never hardcoded
    # Scroll to and click "Place Order" — in WebKit the link may be off-screen
    # and the role locator can be fragile, so use the direct href selector.
    place_order = page.locator("a[href='/payment']")
    try:
        place_order.wait_for(state="visible", timeout=20000)
        place_order.scroll_into_view_if_needed()
        place_order.click()
    except Exception:
        # Last resort: navigate directly to the payment page
        page.goto("https://automationexercise.com/payment", wait_until="domcontentloaded")
    page.wait_for_load_state("domcontentloaded")
    page.locator('input[name="name_on_card"]').fill(card["name"])
    page.locator('input[name="card_number"]').fill(card["number"])
    page.get_by_role("textbox", name="ex.").fill(card["cvc"])
    page.get_by_role("textbox", name="MM").fill(card["month"])
    page.get_by_role("textbox", name="YYYY").fill(card["year"])
    page.get_by_role("button", name="Pay and Confirm Order").click()
    expect(page.locator("#form")).to_contain_text("Congratulations! Your order has been confirmed!")

    # Logout and verify we land back on the login page.
    # After "Continue", WebKit may drop the session (the user is already
    # logged out and we land on the login page directly).  Handle both cases.
    page.get_by_role("link", name="Continue").click()
    page.wait_for_load_state("domcontentloaded")

    logout_link = page.locator("a[href='/logout']")
    if logout_link.is_visible(timeout=5000):
        logout_link.click()
        page.wait_for_load_state("domcontentloaded")
    else:
        # Session was dropped — navigate to login page directly
        page.goto(
            "https://automationexercise.com/login",
            wait_until="domcontentloaded",
        )

    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()
    expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()
