from urllib.request import Request, urlopen
import json

# Get a page body text
def fetch_text(url, headers = {}):
  req = Request(url)
  for key, value in headers.items():
    req.add_header(key, value)
  return urlopen(req).read().decode()

# Get some JSON
def fetch_json(url, headers = {}):
  return json.loads(fetch_text(url, headers))
