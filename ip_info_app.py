import streamlit as st
import requests
import socket
import pandas as pd

# ----------- IP Information -------------
def get_ip_info(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            return {
                "IP Address": data['query'],
                "Country": data['country'],
                "Region": data['regionName'],
                "City": data['city'],
                "ZIP Code": data['zip'],
                "ISP": data['isp'],
                "Latitude": data['lat'],
                "Longitude": data['lon'],
                "Timezone": data['timezone']
            }
        else:
            return {"Error": "Could not fetch IP details."}
    except requests.RequestException as e:
        return {"Error": str(e)}

def resolve_url_to_ip(url):
    try:
        return socket.gethostbyname(url)
    except socket.gaierror:
        return None

# ----------- Streamlit UI -------------
st.title("IP Address or URL Finder")

# IP/URL section
with st.form("ip_form"):
    input_value = st.text_input("Enter an IP address or URL", placeholder="e.g., 8.8.8.8 or google.com")
    submitted_ip = st.form_submit_button("Fetch Info")

if submitted_ip:
    if input_value:
        # Check if it's a URL or IP
        if not input_value.replace(".", "").isdigit():  # URL
            ip = resolve_url_to_ip(input_value)
            if ip:
                st.write(f"Resolved IP address for **{input_value}** is: `{ip}`")
            else:
                st.error("Invalid URL. Could not resolve to IP.")
                st.stop()
        else:
            ip = input_value

        result = get_ip_info(ip)
        if "Error" in result:
            st.error(result["Error"])
        else:
            st.success("Information fetched successfully!")
            for key, value in result.items():
                if key not in ["Latitude", "Longitude"]:
                    st.write(f"**{key}**: {value}")

            # Plot map using latitude and longitude
            st.markdown("### 📍 Location on Map")
            location_df = pd.DataFrame({
                'lat': [result['Latitude']],
                'lon': [result['Longitude']]
            })
            st.map(location_df)

    else:
        st.warning("Please enter an IP address or URL.")
