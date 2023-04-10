import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs 
from deta import Deta
from sharekhanConnect import SharekhanConnect



#url to generate access token
url = 'https://api.sharekhan.com/skapi/auth/login.html?api_key=FH49SOfYA55nGsUpldXaOfxhtnMiDS2w&user_id=12345&version_id=1005'

deta = Deta('d0rwyaghixk_xdYc2J98omec5FU2bEyrePtiYZXPwHPF')
sharekhan_keys_db = deta.Base('sharekhan-keys')

api_key = sharekhan_keys_db.get('api_key')['value']
secret_key = sharekhan_keys_db.get('secret_key')['value']
user_id = sharekhan_keys_db.get('user_id')['value']
customer_id = sharekhan_keys_db.get('customer_id')['value']
version_id = "1005"

print(api_key)

def access_token(url):

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    request_token = query_params["request_token"][0]

    login = SharekhanConnect(api_key)
    encrypted_request_token=login.generate_session(request_token=request_token,secret_key=secret_key) #generate_session function is modified to return encrypted request token

    access_token=login.get_access_token(api_key,encrypted_request_token.decode(),userId=user_id,versionId=version_id)

    sharekhan_keys_db.put({"value":access_token['data']['token']},"access_token")



#-----------------------------------------UI Part-------------------------------------------------
st.title("Sway")

login_button = st.button('Login')

if login_button:
    response = requests.get(url)
    st.write(response.url)

url = st.text_area('Enter Redirected URL')
generate_button = st.button("Generate access token")

if generate_button:
    access_token(url)
    st.write("Done!")
