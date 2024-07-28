import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse

def search_shopify_shops(query):
    """Suche Shopify-Shops, die das gegebene Keyword enthalten."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': st.secrets["google_api"]["api_key"],
        'cx': st.secrets["google_api"]["cse_id"],
        'q': f"intitle:{query} site:myshopify.com"
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result['items'] if 'items' in result else []

def make_clickable(link):
    """Macht Links in der Ergebnistabelle anklickbar und zeigt die Domain als Hyperlinktext."""
    parsed_url = urlparse(link)
    domain = parsed_url.netloc
    return f'<a href="{link}" target="_blank">{domain}</a>'

def main():
    st.title('Shopify Shop Finder')
    st.write('Geben Sie ein Keyword ein, um Shopify-Shops zu finden, die dieses Keyword enthalten.')

    keyword = st.text_input('Keyword eingeben:', '')

    if st.button('Suchen') and keyword:
        shops = search_shopify_shops(keyword)
        
        if shops:
            data = [{'Shop Name': shop['title'], 'URL': shop['link']} for shop in shops]
            df = pd.DataFrame(data)
            df['URL'] = df['URL'].apply(make_clickable)
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.write("Keine Ergebnisse gefunden.")
        
        if st.button('Neue Suche'):
            st.experimental_rerun()

if __name__ == "__main__":
    main()
