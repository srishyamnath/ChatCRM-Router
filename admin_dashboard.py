import streamlit as st
import json
import os

TENANT_FILE = os.path.join("..", "config", "tenants.json")

def load_tenants():
    if not os.path.exists(TENANT_FILE):
        return {"tenants": []}
    with open(TENANT_FILE, "r") as f:
        return json.load(f)

def save_tenants(data):
    with open(TENANT_FILE, "w") as f:
        json.dump(data, f, indent=2)

st.set_page_config(layout="wide", page_title="Admin Dashboard")

st.title("📘 Admin Dashboard")
st.caption("Manage your chatbot tenants and their CRM configurations.")

data = load_tenants()

# ---------------------------------------------
# Add New Tenant
st.subheader("🏢 Add New Tenant")
with st.form("add_tenant_form"):
    new_id = st.text_input("Tenant ID (e.g., lifecode_in)")
    new_name = st.text_input("Tenant Name")
    submitted = st.form_submit_button("Add Tenant")
    if submitted and new_id and new_name:
        if any(t["tenant_id"] == new_id for t in data["tenants"]):
            st.warning("Tenant ID already exists.")
        else:
            data["tenants"].append({
                "tenant_id": new_id,
                "name": new_name,
                "crm": "zoho",  # default
                "zoho": {},
                "hubspot": {},
                "branding": {
                    "welcome_message": "",
                    "logo_url": ""
                }
            })
            save_tenants(data)
            st.success("Tenant added successfully!")

# ---------------------------------------------
# Edit Tenant
tenant_ids = [t["tenant_id"] for t in data["tenants"]]
selected = st.selectbox("Select Tenant to Edit", tenant_ids)

if selected:
    tenant = next(t for t in data["tenants"] if t["tenant_id"] == selected)
    st.subheader(f"⚙️ Edit Tenant: `{selected}`")

    tenant["name"] = st.text_input("Name", value=tenant.get("name", ""))
    st.markdown("### Branding")
    tenant["branding"]["welcome_message"] = st.text_area("Welcome Message", value=tenant["branding"].get("welcome_message", ""))
    tenant["branding"]["logo_url"] = st.text_input("Logo URL", value=tenant["branding"].get("logo_url", ""))

    st.markdown("### CRM Configuration")
    tenant["crm"] = st.selectbox("CRM Choice", ["zoho", "hubspot"], index=["zoho", "hubspot"].index(tenant["crm"]))

    if tenant["crm"] == "zoho":
        tenant["zoho"]["client_id"] = st.text_input("Zoho Client ID", value=tenant["zoho"].get("client_id", ""))
        tenant["zoho"]["client_secret"] = st.text_input("Zoho Client Secret", value=tenant["zoho"].get("client_secret", ""), type="password")
        tenant["zoho"]["refresh_token"] = st.text_input("Zoho Refresh Token", value=tenant["zoho"].get("refresh_token", ""), type="password")
    else:
        tenant["hubspot"]["api_key"] = st.text_input("HubSpot API Key", value=tenant["hubspot"].get("api_key", ""), type="password")

    if st.button("💾 Save Changes"):
        save_tenants(data)
        st.success("Tenant updated!")

    if st.button("🗑️ Delete Tenant"):
        data["tenants"] = [t for t in data["tenants"] if t["tenant_id"] != selected]
        save_tenants(data)
        st.warning("Tenant deleted.")

# ---------------------------------------------
# Simulate Chat
st.markdown("---")
st.subheader("😀 Test Chatbot Routing")

sim_tenant = st.selectbox("Select a Tenant to Simulate a Chat", tenant_ids, key="sim_tenant")
sample_msg = st.text_area("Enter a sample user message:", "Hi, I'm interested in your services.")

if st.button("💬 Run Simulation"):
    tenant = next(t for t in data["tenants"] if t["tenant_id"] == sim_tenant)
    welcome = tenant["branding"].get("welcome_message", "")
    reply = f"""
    {welcome}
    Thank you! Your information has been received and a ticket has been created in our system.
    Our team will be in touch shortly.
    """
    st.success(reply.strip())
