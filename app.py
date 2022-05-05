from flask import Flask, redirect, render_template, request
import csv
import requests

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get('rates')

def get():
    code = []
    ask = []
    currency = []
    for n in rates:
        code.append(n['code'])
        ask.append(n['ask'])
        currency.append(n['currency'])
    return sorted(code)

def save():
    fields = ["currency", "code", "ask", "bid"]
    with open("Data.csv", 'w') as output_file:
        write = csv.DictWriter(output_file, delimiter=';', fieldnames=fields)
        write.writeheader()
        write.writerows(rates)

save()

@app.route('/', methods=["GET", "POST"])
def form():
    code = get()
    if request.method == "POST":
        data = request.form
        currency = data.get('code')
        amount = data.get('amount')
        for data in rates:
            if data.get('code') == currency:
                ask = data.get('ask')

                break
        results = '%0.2f' % (float(amount) * float(ask))
        return render_template("results.html", results = results, ask=ask, currency=currency)                                
    return render_template("index.html", code = code)
                                  
if __name__ == "__main__":               
    app.run(debug=True)