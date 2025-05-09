import streamlit as st
import requests
import socket
import pandas as pd
import whois

# ---------- Functions ----------
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
                "Latitude 📍": data['lat'],
                "Longitude 📍": data['lon'],
                "Timezone": data['timezone']
            }
        else:
            return {"Error ❌": "Could not fetch IP details."}
    except requests.RequestException as e:
        return {"Error ❌": str(e)}

def resolve_url_to_ip(url):
    try:
        return socket.gethostbyname(url)
    except socket.gaierror:
        return None
def format_date(value):
    if isinstance(value, list):
        return str(value[0]) if value else "N/A"
    return str(value) if value else "N/A"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "Domain Name": w.domain_name,
            "Registrar": w.registrar,
            "Created Date": format_date(w.creation_date),
            "Expiry Date": format_date(w.expiration_date),
            "Organization": w.org,
            "Name Servers": ", ".join(w.name_servers) if w.name_servers else "N/A"
        }
    except Exception as e:
        return {"WHOIS Error ❌": f"Could not fetch WHOIS info. {e}"}

# ---------- Streamlit UI ----------
st.set_page_config(page_title="IP/URL Info", page_icon="🌐")
st.title("IP Address & URL Finder")
st.markdown("Enter an IP or domain name to get detailed info including **location**, **ISP**, and **WHOIS** data.")

with st.form("ip_form"):
    input_value = st.text_input("🔎 Enter IP address or URL", placeholder="e.g., 8.8.8.8 or google.com")
    submitted = st.form_submit_button("Fetch Info")

if submitted:
    if input_value:
        with st.spinner("Fetching details..."):
            # Detect and resolve
            is_url = not input_value.replace(".", "").isdigit()
            if is_url:
                ip = resolve_url_to_ip(input_value)
                if ip:
                    st.success(f"✅ Resolved IP for **{input_value}** is: `{ip}`")
                else:
                    st.error("❌ Could not resolve URL to IP.")
                    st.stop()
            else:
                ip = input_value

            # IP Info
            st.markdown("### 🌍 IP Address Details")
            ip_result = get_ip_info(ip)
            if "Error ❌" in ip_result:
                st.error(ip_result["Error ❌"])
            else:
                for k, v in ip_result.items():
                    st.write(f"**{k}**: {v}")

                # Map plot
                st.markdown("### 🗺️ Location on Map")
                location_df = pd.DataFrame({
                    'lat': [ip_result['Latitude 📍']],
                    'lon': [ip_result['Longitude 📍']]
                })
                st.map(location_df)

            # WHOIS Info (only for URL)
            if is_url:
                st.markdown("### 🧾 WHOIS Information")
                whois_result = get_whois_info(input_value)
                for k, v in whois_result.items():
                    st.write(f"**{k}**: {v}")
    else:
        st.warning("⚠️ Please enter a valid IP or URL.")
