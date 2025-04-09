# /app.py
import streamlit as st
from auth.auth_manager import signup_user, login_user
from twitter.fetch import fetch_tweets
from db.mongo import save_search, get_user_searches
from analysis.sentiment import analyze_sentiment
from utils.helpers import sentiment_summary
from icon.icon import icon_base64

st.set_page_config(page_title="Twitter Feed Analyzer", page_icon=icon_base64, layout="centered")

# Session init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login_ui():
    st.title("🔐 Login or Signup")
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username", key="login_user")
        passwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(user, passwd)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.success(msg)
                st.rerun()  # force reload into main UI
            else:
                st.error(msg)

    with tab2:
        user = st.text_input("New Username", key="signup_user")
        passwd = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Signup"):
            success, msg = signup_user(user, passwd)
            if success:
                st.success(msg)
            else:
                st.error(msg)

def main_ui():
    st.title("🐦 Twitter Feed Analyzer")
    menu = st.sidebar.selectbox("Menu", ["Search Tweets", "View History", "Logout"])
    username = st.session_state.username

    if menu == "Search Tweets":
        keyword = st.text_input("Enter keyword")
        if st.button("Search"):
            tweets = fetch_tweets(keyword)
            if tweets:
                sentiments = [analyze_sentiment(t) for t in tweets]
                st.subheader("📝 Tweets with Sentiment")
                for i, (t, s) in enumerate(zip(tweets, sentiments), start=1):
                    st.write(f"{i}. {t} ({s})")
                save_search(username, keyword, tweets)
                st.subheader("📊 Sentiment Summary")
                st.bar_chart(sentiment_summary(tweets, analyze_sentiment))
            else:
                st.warning("No tweets found or API error.")

    elif menu == "View History":
        searches = get_user_searches(username)
        if not searches:
            st.info("No search history found.")
        for search in searches:
            st.subheader(f"🔍 {search['keyword']} - {search['timestamp']}")
            tweets = search["tweets"]
            sentiments = sentiment_summary(tweets, analyze_sentiment)
            st.write("Sentiment Summary:")
            st.bar_chart(sentiments)

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("You have been logged out.")
        st.rerun()

if not st.session_state.logged_in:
    login_ui()
else:
    main_ui()
