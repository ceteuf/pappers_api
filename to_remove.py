# %%
import requests
from bs4 import BeautifulSoup
# %%

agent = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0'}

page = requests.get("https://www.amazon.co.uk/s?k=109840059077&rh=p_n_condition-type%3A12319067031&dc", headers=agent)

soup = BeautifulSoup(page.content, 'html.parser')

htmlName = soup.find_all('span', 'a', {"class":"a-offscreen"}, limit=1)
# %%
print(htmlName)

print(soup)