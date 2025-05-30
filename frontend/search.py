# frontend/search.py
import streamlit as st
import requests

class SearchManager:
    """Render the internet search bar and display search results."""
    def __init__(self, api_key="e14302754ce68371ec396cbff2fd2f0db10cfc35"):
        self.api_key = api_key  # Optional future use

    def search(self, query):
        headers = { "X-API-KEY": self.api_key, "Content-Type": "application/json" }
        data = { "q": query }
        response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
        results = response.json().get("organic", [])[:3]
        return "\n\n".join([f"🔗 [{r['title']}]({r['link']})\n{r['snippet']}" for r in results])

def show_search_bar():
    st.markdown("---")
    st.subheader("🌐 Internetrecherche")
    query = st.text_input("Suchbegriff eingeben...")
    if query:
        manager = SearchManager()
        result = manager.search(query)
        st.info(result)