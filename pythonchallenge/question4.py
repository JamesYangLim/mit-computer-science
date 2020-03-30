import requests 
import re

url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
n = "12345"
ok = True

while ok:
    r = requests.get(url + n) 
    ok = r.ok
    print(r.text)
    n = r.text.split()[5]
