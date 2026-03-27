from flask import Flask, request, render_template, jsonify
import hashlib, hmac, time

app = Flask(__name__)

BOT_TOKEN = "8419151743:AAH4jk7zb1NvBOGevwKgpH4b6ppO2fCwltE"

def check_telegram_auth(data):
    auth_data = data.copy()
    received_hash = auth_data.pop('hash', None)

    if not received_hash:
        return False

    data_check_string = '\n'.join(
        [f"{k}={v}" for k, v in sorted(auth_data.items())]
    )

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return calculated_hash == received_hash


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/auth")
def auth():
    data = request.args.to_dict()

    if not check_telegram_auth(data):
        return "❌ Login inválido"

    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > 86400:
        return "⏰ Login expirado"

    return f"""
    <h1>✅ Logado com sucesso</h1>
    <p>ID: {data.get('id')}</p>
    <p>Nome: {data.get('first_name')}</p>
    <p>User: @{data.get('username')}</p>
    """
    

if __name__ == "__main__":
    app.run(debug=True)
