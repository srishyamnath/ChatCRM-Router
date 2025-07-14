from .zoho_crm import create_lead_zoho
# from .hubspot_crm import create_lead_hubspot  # Uncomment if you use HubSpot

def send_to_crm(lead_data, tenant_config):
    crm_type = tenant_config.get("crm")

    if crm_type == "zoho":
        return create_lead_zoho(lead_data, tenant_config["zoho"])

    elif crm_type == "hubspot":
        # return create_lead_hubspot(lead_data, tenant_config["hubspot"])
        return {"status": "HubSpot CRM routing not implemented yet."}

    return {"status": "Unknown CRM selected"}
