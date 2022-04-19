import json
from urllib.request import Request, urlopen

#
# Get a page body text
#
def fetch_text(url, headers = {}):
  print(f"[fetch] {url}")
  req = Request(url)
  for key, value in headers.items():
    req.add_header(key, value)
  res = urlopen(req).read()
  print(f"[fetch] response")
  return res.decode()

#
# Get some JSON
#
def fetch_json(url, headers = {}):
  return json.loads(fetch_text(url, headers))
