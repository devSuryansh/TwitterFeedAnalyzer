import streamlit as st
from auth.auth_manager import signup_user, login_user
from twitter.fetch import fetch_tweets
from db.mongo import save_search, get_user_searches
from analysis.sentiment import analyze_sentiment
from utils.helpers import sentiment_summary

st.set_page_config(page_title="Twitter Feed Analyzer", layout="centered")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login_ui():
    st.title("🔐 Login or Signup")
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = st.text_input("Username")
        passwd = st.text_input("Password", type="password")
        if st.button("Login"):
            success, msg = login_user(user, passwd)
            st.success(msg) if success else st.error(msg)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = user

    with tab2:
        user = st.text_input("New Username")
        passwd = st.text_input("New Password", type="password")
        if st.button("Signup"):
            success, msg = signup_user(user, passwd)
            st.success(msg) if success else st.error(msg)

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
                st.write("**Tweets:**")
                for i, t in enumerate(tweets):
                    st.write(f"{i+1}. {t} ({sentiments[i]})")
                save_search(username, keyword, tweets)
                st.write("### 📊 Sentiment Summary")
                st.bar_chart(sentiment_summary(tweets, analyze_sentiment))
            else:
                st.warning("No tweets found or API error.")

    elif menu == "View History":
        searches = get_user_searches(username)
        for search in searches:
            st.subheader(f"🔍 {search['keyword']} - {search['timestamp']}")
            tweets = search["tweets"]
            sentiments = sentiment_summary(tweets, analyze_sentiment)
            st.write("Sentiment Summary:")
            st.bar_chart(sentiments)

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

if not st.session_state.logged_in:
    login_ui()
else:
    main_ui()
