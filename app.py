from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_olx(busca):
    query = "+".join(busca.split())
    url = f"https://www.olx.com.br/busca?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    itens = soup.select("li.sc-1fcmfeb-2") or soup.select("li.OLXad-card")
    resultados = []
    for item in itens[:10]:
        try:
            titulo = item.select_one("h2").text.strip()
            link = "https://www.olx.com.br" + item.select_one("a")["href"]
            preco = item.select_one("span.sc-ifAKCX").text.strip()
            resultados.append({
                "titulo": titulo,
                "link": link,
                "preco": preco
            })
        except:
            continue
    return resultados

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    busca = ""
    if request.method == "POST":
        busca = request.form.get("busca")
        if busca:
            resultados = buscar_olx(busca)
    return render_template("index.html", resultados=resultados, busca=busca)

if __name__ == "__main__":
    app.run(debug=True)
