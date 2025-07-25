from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret_key'

# 為替レート
exchange_rates = {
    'USD': 0.0072,   # 円 → ドル
    'EUR': 0.0066,   # 円 → ユーロ
    'KRW': 9.92      # 円 → 韓国ウォン
}
currency_emojis = {
    'USD': '💵',   # 円 → ドル
    'EUR': '💶',   # 円 → ユーロ
    'KRW': '👀'    # 円 → 韓国ウォン
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = float(request.form['yen'])  # 入力金額
        currency = request.form['currency']     # 通貨選択（USDなど）
        direction = request.form['direction']   # 方向（円→外貨 or 外貨→円）
        rate = exchange_rates[currency]
        
        emoji = currency_emojis.get(currency, '')

        if direction == 'to_foreign':
            result = round(amount * rate, 2)
            direction_str = f"{amount} 円 → {result} {currency} {emoji}"
        else:
            result = round(amount / rate, 2)
            direction_str = f"{amount} {currency} {emoji} → {result} 円"

        session['direction_str'] = direction_str
        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html', result=session['direction_str']) 

if __name__ == '__main__':
    app.run(debug=True, port=9999)
