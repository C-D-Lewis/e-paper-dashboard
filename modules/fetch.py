import urllib.request, json

# Get a page body
def fetch_text(url):
  with urllib.request.urlopen(url) as req:
    return req.read().decode()

# Get some JSON
def fetch_json(url):
  return json.loads(fetch_text(url))
