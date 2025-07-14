import requests

data = {
    "grant_type": "authorization_code",
    "client_id": "1000.CSHGEBS3UWDNBS8TSVI76M8NWXPFKC",
    "client_secret": "3aa63f075e19d9a39a312dd18b15e393b15826ad92",
    "redirect_uri": "https://www.zoho.in",
    "code": "1000.a6b564f755acac01aac24ecc0f69ba4d.fcdcdc8c47bc440e719f774453ff0069"
}

res = requests.post("https://accounts.zoho.in/oauth/v2/token", data=data)

# 👇 Debug output
print(res.status_code)
print(res.text)

