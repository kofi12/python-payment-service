from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from models import models
from sqlmodel import SQLModel, Session, create_engine
from dotenv import find_dotenv, load_dotenv
import stripe
import os

load_dotenv(find_dotenv())
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = "2023-10-16"
DATABASE_URL = os.getenv('DATABASE_URL', '')

engine = create_engine(DATABASE_URL)

router = APIRouter(prefix = "/api")

@router.post("/create-checkout-session")
async def create_checkout(request: Request):
    try:
        data = await request.json()
        price : stripe.Price = stripe.Price.create(
            currency = "cad",
            unit_amount = data['price'] * 100,
            product_data = {
                'name': 'fancy product'
            },
            stripe_account = "acct_1OuV7JCZDWrvI6w3"
        )
        session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price' : price.id,
                    'quantity' : 1, 
                },
            ],
            mode = 'payment',
            success_url = 'http://localhost:8000',
            cancel_url = 'http://localhost:8000',
            stripe_account = "acct_1OuV7JCZDWrvI6w3"
        )
        return {"session_url": session.url}
    except Exception as e:
        print("Exception caught")
        print(e)
        return 'Error creating checkout session'
        
@router.post("/onboard-seller")
def init_connected_account():
    try:
        print("in the try block")
        stripe_account : stripe.Account = create_account()
        if isinstance(stripe_account, str):
            print(stripe_account)
            return stripe_account
        print(stripe_account.id)
        accountLink : stripe.AccountLink = generate_accountLink(stripe_account)
        if isinstance(accountLink, str):
            print(accountLink)
            return accountLink
        print(accountLink.url)
        return RedirectResponse(accountLink.url)
    except Exception as e:
        return 'Error onboarding seller'
        
# stripe account creation helper function
def create_account() -> stripe.Account:
    try:
        stripe_account: stripe.Account = stripe.Account.create(
            type = 'custom',
            country = 'CA',
            capabilities = {"card_payments": {"requested": True}, "transfers": {"requested": True}}
            )
        # Add the stripe connected account to the database
        account = models.Seller(seller_id=stripe_account.id)
        session = Session(engine)
        session.add(account)
        session.commit()
        session.close()
        return stripe_account
    except Exception as e:
        print(e)
        raise e
    
# stripe accountlink creation helper function
def generate_accountLink(stripe_account: stripe.Account) -> stripe.AccountLink:
    try:
        account_link = stripe.AccountLink.create(
            type = 'account_onboarding',
            account = stripe_account.id,
            refresh_url= 'http://localhost:8000/api/refresh',
            return_url = 'http://localhost:3000/catalogue',
        )

        return account_link
    except Exception as e:
        print(e)
        raise e
