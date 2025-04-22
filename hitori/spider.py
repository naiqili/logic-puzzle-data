import requests
from bs4 import BeautifulSoup
import json
import time
from tqdm import tqdm

BASE_URL = "https://www.menneske.no/hitori/{n1}x{n2}/eng/solution.html?number={idx}"
results = {}

headers = {
    "User-Agent": "Mozilla/5.0"
}

cnt = 1
for nn in [5,6,8,9,12,15,17,20]:
    for idx in tqdm(range(1, 200)):
        url = BASE_URL.format(n1=nn,n2=nn,idx=idx)
        # print(f"Fetching {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("div", class_="hitori").find("table")

        encoded_q, encoded_a = "", ""
        for row in table.find_all("tr"):
            _n = 0
            for cell in row.find_all("td"):
                cell_class = cell.get("class", [])
                if "black" in cell_class:
                    encoded_a += "b" 
                    encoded_q += cell.text.strip()
                    _n += 1
                elif "white" in cell_class:
                    encoded_a += "w" 
                    encoded_q += cell.text.strip()
                    _n += 1

        if encoded_q == '':
            continue
        results[cnt] = {'question': encoded_q, 'answer': encoded_a, 'size': _n}
        cnt += 1
        # time.sleep(0.5)  # polite crawling

# 保存为 JSON 文件
with open("hitori.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done! Results saved to hitori_solutions.json")
