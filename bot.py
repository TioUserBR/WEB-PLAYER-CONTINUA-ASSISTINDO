from flask import Flask, request, jsonify
import hashlib
import hmac
import time

app = Flask(__name__)

BOT_TOKEN = "8419151743:AAH4jk7zb1NvBOGevwKgpH4b6ppO2fCwltE"  # token do BotFather

# 🔐 Função pra validar dados do Telegram
def check_telegram_auth(data):
    auth_data = data.copy()
    received_hash = auth_data.pop('hash')

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

# 🚀 Rota de login
@app.route("/auth")
def telegram_auth():
    data = request.args.to_dict()

    # valida assinatura
    if not check_telegram_auth(data):
        return jsonify({"status": "erro", "msg": "hash inválido"}), 403

    # valida tempo (anti replay attack)
    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > 86400:
        return jsonify({"status": "erro", "msg": "login expirado"}), 403

    # dados do usuário
    user = {
        "id": data.get("id"),
        "first_name": data.get("first_name"),
        "username": data.get("username"),
        "photo_url": data.get("photo_url")
    }

    # 👉 aqui você salva no banco se quiser

    return jsonify({
        "status": "ok",
        "user": user
    })

if __name__ == "__main__":
    app.run(debug=True)
