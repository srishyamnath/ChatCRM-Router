import json

def get_tenant_config(tenant_id: str) -> dict:
    with open("config/tenants.json", "r") as file:
        tenants = json.load(file)["tenants"]
    for tenant in tenants:
        if tenant["tenant_id"] == tenant_id:
            return tenant
    return {}
