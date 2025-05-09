import streamlit as st
import requests

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
            return {"Error": "Could not fetch details. IP may be invalid."}
    except requests.RequestException as e:
        return {"Error": str(e)}

st.title("IP Address Information")

ip = st.text_input("Enter an IP address", placeholder="e.g., 8.8.8.8")

if st.button("Fetch IP Info"):
    if ip:
        result = get_ip_info(ip)
        if "Error" in result:
            st.error(result["Error"])
        else:
            st.success("IP information fetched successfully!")
            for key, value in result.items():
                st.write(f"**{key}**: {value}")
    else:
        st.warning("Please enter a valid IP address.")
