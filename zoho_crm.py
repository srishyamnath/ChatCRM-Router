import requests

def refresh_zoho_token(config):
    payload = {
        "refresh_token": config["refresh_token"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "grant_type": "refresh_token"
    }
    response = requests.post("https://accounts.zoho.in/oauth/v2/token", params=payload)
    data = response.json()
    return data.get("access_token")

def create_lead_zoho(lead_data, config):
    access_token = refresh_zoho_token(config)
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "data": [{
            "Last_Name": lead_data["name"] or "Unknown",
            "Email": lead_data["email"],
            "Description": lead_data["message"]
        }]
    }
    response = requests.post(
        "https://www.zohoapis.in/crm/v2/Leads",
        headers=headers,
        json=data
    )
    return response.json()
