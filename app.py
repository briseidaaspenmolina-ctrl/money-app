# Budgeting & Investing App - MVP (beginner version)
# Run it with:  streamlit run app.py

import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Money App MVP", page_icon="💰")

# ---------------------------------------------------------
# 1. MEMORY: st.session_state keeps data while the app runs
# ---------------------------------------------------------
if "profile" not in st.session_state:
    st.session_state.profile = None          # intake answers go here

if "subscriptions" not in st.session_state:
    # Sample subscriptions (fake data for the MVP)
    st.session_state.subscriptions = [
        {"name": "Music app", "price": 10.99, "renews": date.today() + timedelta(days=3), "active": True},
        {"name": "Video streaming", "price": 15.49, "renews": date.today() + timedelta(days=12), "active": True},
        {"name": "Game pass", "price": 9.99, "renews": date.today() + timedelta(days=20), "active": True},
    ]

if "cash" not in st.session_state:
    st.session_state.cash = 1000.00           # practice money, not real
    st.session_state.holdings = {}            # stock name -> number of shares

# Fake stock prices for practice mode
PRICES = {"S&P 500 index fund": 50.00, "Tech company": 25.00, "Shoe company": 12.00}

# ---------------------------------------------------------
# 2. PAGE MENU in the sidebar
# ---------------------------------------------------------
page = st.sidebar.radio("Go to", ["Intake form", "Notifications", "Subscriptions", "Practice investing"])

# ---------------------------------------------------------
# 3. INTAKE FORM
# ---------------------------------------------------------
if page == "Intake form":
    st.title("Let's build your plan")

    age = st.radio("How old are you?", ["13-15", "16-17", "18-22", "23+"], horizontal=True)
    goal = st.radio("What's your main goal?",
                    ["Build a budget", "Start investing", "Save for something", "Learn the basics"])
    knowledge = st.radio("How much do you know about investing?",
                         ["Nothing yet", "A little", "A lot"], horizontal=True)
    monthly = st.number_input("Money you can set aside each month ($)", min_value=0, value=50, step=5)

    if st.button("Continue"):
        st.session_state.profile = {"age": age, "goal": goal, "knowledge": knowledge, "monthly": monthly}
        st.success("Saved! Here's your plan:")

        # Personalize: pick the first lesson based on their answers
        if knowledge == "Nothing yet":
            st.write("Start with: **Budgeting basics**")
        elif knowledge == "A little":
            st.write("Start with: **What is a stock?**")
        else:
            st.write("Start with: **Index funds and diversification**")

        # Under 18 = practice mode only
        if age in ["13-15", "16-17"]:
            st.info("You're in practice mode: you'll invest with fake money.")

# ---------------------------------------------------------
# 4. NOTIFICATION SETTINGS (so alerts aren't too much)
# ---------------------------------------------------------
elif page == "Notifications":
    st.title("Notification settings")
    st.write("Pick only what you want. You can change this anytime.")

    how_often = st.radio("How often?", ["Daily", "A few times a week", "Weekly", "Off"])
    st.write("What should we remind you about?")
    lessons = st.checkbox("Lesson and streak reminders", value=True)
    renewals = st.checkbox("Subscription renewal alerts", value=True)
    budget = st.checkbox("Budget alerts (when you're close to your limit)")
    days_before = st.slider("Warn me this many days before a subscription renews", 1, 7, 3)
    quiet = st.checkbox("Quiet hours (no alerts 9pm-8am)", value=True)

    if st.button("Save settings"):
        st.session_state.notif = {"how_often": how_often, "lessons": lessons, "renewals": renewals,
                                  "budget": budget, "days_before": days_before, "quiet": quiet}
        st.success("Settings saved.")

# ---------------------------------------------------------
# 5. SUBSCRIPTIONS: track, get reminders, mark canceled
# ---------------------------------------------------------
elif page == "Subscriptions":
    st.title("Your subscriptions")
    days_before = st.session_state.get("notif", {}).get("days_before", 3)

    total = 0
    for i, sub in enumerate(st.session_state.subscriptions):
        if not sub["active"]:
            continue
        total += sub["price"]
        days_left = (sub["renews"] - date.today()).days

        st.subheader(sub["name"])
        st.write(f"${sub['price']} per month - renews in {days_left} days")

        # Reminder if renewal is coming up soon
        if days_left <= days_before:
            st.warning("Renews soon! Cancel now if you don't use it.")

        if st.button(f"Mark {sub['name']} as canceled", key=f"cancel{i}"):
            sub["active"] = False
            st.rerun()

    st.metric("Total per month", f"${total:.2f}")
    st.caption("Tip: canceling one $10 subscription = $120 a year you could invest.")

# ---------------------------------------------------------
# 6. PRACTICE INVESTING: fast one-tap buy and sell (fake money)
# ---------------------------------------------------------
elif page == "Practice investing":
    st.title("Practice investing")
    st.caption("Fake money only. No real trades happen.")
    st.metric("Practice cash", f"${st.session_state.cash:.2f}")

    for name, price in PRICES.items():
        owned = st.session_state.holdings.get(name, 0)
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"**{name}** - ${price} | you own {owned}")

        if col2.button("Buy 1", key=f"buy{name}"):
            if st.session_state.cash >= price:
                st.session_state.cash -= price
                st.session_state.holdings[name] = owned + 1
                st.rerun()
            else:
                st.error("Not enough practice cash.")

        if col3.button("Sell 1", key=f"sell{name}"):
            if owned > 0:
                st.session_state.cash += price
                st.session_state.holdings[name] = owned - 1
                st.rerun()
            else:
                st.error("You don't own any yet.")
