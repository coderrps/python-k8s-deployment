from flask import Flask, request, jsonify, render_template_string
import urllib.request
import json

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>

<head>

    <title>Stock Profit Calculator</title>

    <style>

        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 50px;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: #1e293b;
            padding: 30px;
            border-radius: 15px;
        }

        h1 {
            color: #38bdf8;
        }

        select,
        input {
            padding: 12px;
            margin: 8px;
            border-radius: 6px;
            border: none;
            font-size: 16px;
            width: 235px;
        }

        button {
            padding: 12px 25px;
            margin-top: 15px;
            background: #22c55e;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #16a34a;
        }

        .result {
            margin-top: 25px;
            padding: 20px;
            background: #0f172a;
            border-radius: 10px;
        }

        .profit {
            color: #22c55e;
            font-size: 24px;
            font-weight: bold;
        }

        .loss {
            color: #ef4444;
            font-size: 24px;
            font-weight: bold;
        }

    </style>

</head>


<body>

<div class="container">

    <h1>📈 Stock Profit Calculator</h1>

    <p>
        Check stock price and calculate your profit/loss.
    </p>


    <select id="symbol">

        <option value="">
            Select a stock
        </option>

        <option value="RELIANCE.NS">
            Reliance Industries
        </option>

        <option value="TCS.NS">
            TCS
        </option>

        <option value="INFY.NS">
            Infosys
        </option>

        <option value="HDFCBANK.NS">
            HDFC Bank
        </option>

        <option value="ICICIBANK.NS">
            ICICI Bank
        </option>

        <option value="SBIN.NS">
            State Bank of India
        </option>

        <option value="ITC.NS">
            ITC
        </option>

        <option value="LT.NS">
            Larsen & Toubro
        </option>

    </select>


    <br>


    <input
        id="quantity"
        type="number"
        placeholder="Quantity"
    >


    <br>


    <input
        id="buyPrice"
        type="number"
        placeholder="Buy Price"
    >


    <br>


    <button onclick="calculate()">
        Calculate
    </button>


    <div id="result"></div>

</div>


<script>

async function calculate() {

    const symbol =
        document.getElementById("symbol").value;

    const quantity =
        Number(
            document.getElementById("quantity").value
        );

    const buyPrice =
        Number(
            document.getElementById("buyPrice").value
        );

    const result =
        document.getElementById("result");


    if (!symbol || quantity <= 0 || buyPrice <= 0) {

        result.innerHTML =
            "<p>Please enter valid values.</p>";

        return;
    }


    try {

        const response = await fetch(
            "/api/stock?symbol=" + symbol
        );


        const data =
            await response.json();


        if (data.error) {

            result.innerHTML =
                "<p>" + data.error + "</p>";

            return;
        }


        const marketPrice =
            data.price;


        const investment =
            quantity * buyPrice;


        const currentValue =
            quantity * marketPrice;


        const profit =
            currentValue - investment;


        const percentage =
            (profit / investment) * 100;


        const profitClass =
            profit >= 0
            ? "profit"
            : "loss";


        result.innerHTML = `

            <div class="result">

                <p>
                    Stock:
                    <b>${data.name}</b>
                </p>

                <p>
                    Current Price:
                    <b>₹${marketPrice.toFixed(2)}</b>
                </p>

                <p>
                    Investment:
                    <b>₹${investment.toFixed(2)}</b>
                </p>

                <p>
                    Current Value:
                    <b>₹${currentValue.toFixed(2)}</b>
                </p>

                <p class="${profitClass}">
                    Profit/Loss:
                    ₹${profit.toFixed(2)}
                </p>

                <p>
                    Return:
                    <b>${percentage.toFixed(2)}%</b>
                </p>

            </div>

        `;

    }

    catch (error) {

        result.innerHTML =
            "<p>Unable to get stock price.</p>";

    }

}

</script>


</body>

</html>
"""


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/api/stock")
def stock():

    symbol = request.args.get("symbol")


    if not symbol:

        return jsonify({
            "error": "Stock symbol is required."
        }), 400


    try:

        url = (
            "https://query1.finance.yahoo.com/v8/finance/"
            "chart/"
            + symbol.upper()
            + "?range=1d&interval=1m"
        )


        request_object = urllib.request.Request(

            url,

            headers={
                "User-Agent": "Mozilla/5.0"
            }

        )


        with urllib.request.urlopen(
            request_object,
            timeout=10
        ) as response:

            data = json.loads(
                response.read().decode()
            )


        result = data["chart"]["result"][0]


        price = result["meta"]["regularMarketPrice"]


        return jsonify({

            "symbol": symbol.upper(),

            "name": symbol.upper(),

            "price": price

        })


    except Exception:

        return jsonify({

            "error":
                "Could not fetch stock price. "
                "Check the stock symbol."

        }), 500


@app.route("/health")
def health():

    return jsonify({

        "status": "healthy"

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )