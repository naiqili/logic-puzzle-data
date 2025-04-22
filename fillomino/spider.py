import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm

BASE_URL_Q5 = "https://menneske.no/fillomino/eng/showpuzzle.html?number={idx}"
BASE_URL_A5 = "https://menneske.no/fillomino/eng/solution.html?number={idx}"
BASE_URL_Q7 = "https://menneske.no/fillomino/7x7/eng/showpuzzle.html?number={idx}"
BASE_URL_A7 = "https://menneske.no/fillomino/7x7/eng/solution.html?number={idx}"
results = {}

headers = {
    "User-Agent": "Mozilla/5.0"
}

cnt = 1
for (BASE_URL_Q, BASE_URL_A) in [(BASE_URL_Q5, BASE_URL_A5), (BASE_URL_Q7, BASE_URL_A7)]:
    for idx in tqdm(range(1, 200)):
        url = BASE_URL_Q.format(idx=idx)
        # print(f"Fetching {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("div", class_="grid").find("table")

        encoded_q= ""
        for row in table.find_all("tr"):
            _n = 0
            for cell in row.find_all("td"):
                c = cell.text.strip()
                if len(c) != 1:
                    c = '0'
                encoded_q += c
                _n += 1
                
        #=============
        url = BASE_URL_A.format(idx=idx)
        # print(f"Fetching {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("div", class_="grid").find("table")

        encoded_a= ""
        for row in table.find_all("tr"):
            _n = 0
            for cell in row.find_all("td"):
                c = cell.text.strip()
                if len(c) != 1:
                    c = '0'
                encoded_a += c
                _n += 1

        if encoded_q == '':
            continue
        results[cnt] = {'question': encoded_q, 'answer': encoded_a, 'size': _n}
        cnt += 1
        # time.sleep(0.5)  # polite crawling

# 保存为 JSON 文件
with open("fillomino.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done! Results saved to fillomino.json")
