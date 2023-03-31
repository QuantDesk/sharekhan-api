import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs 

url = 'https://api.sharekhan.com/skapi/auth/login.html?api_key=FH49SOfYA55nGsUpldXaOfxhtnMiDS2w&user_id=SWAYFS444'


st.title("Request Token Generator")

login_button = st.button('Login')

if login_button:
    response = requests.get(url)
    st.write(response.url)

redirected = st.text_area('Enter Redirected URL')
extract_button = st.button("Extract Request Token")

if extract_button:
    parsed_url = urlparse(redirected)
    query_params = parse_qs(parsed_url.query)
    request_token = query_params["request_token"][0]

    st.write(request_token)
