from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_URL = "postgresql://postgres:Flavioleal91%21@db.yymysrghprccaxfehdts.supabase.co:5432/postgres"

def get_conn():
    return psycopg2.connect(DB_URL, sslmode="require")


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id SERIAL PRIMARY KEY,
        cliente TEXT,
        endereco TEXT,
        pego BOOLEAN DEFAULT FALSE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id SERIAL PRIMARY KEY,
        pedido_id INTEGER REFERENCES pedidos(id) ON DELETE CASCADE,
        ferramenta TEXT,
        quantidade INTEGER
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def home():
    return "API OK"


@app.route('/postar', methods=['POST'])
def postar():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "erro", "msg": "JSON vazio"}), 400

        cliente = data.get('cliente')
        endereco = data.get('endereco')
        pego = data.get('pego', False)
        ferramentas = data.get('ferramentas', [])

        conn = get_conn()
        cur = conn.cursor()

        # Inserir pedido
        cur.execute(
            "INSERT INTO pedidos (cliente, endereco, pego) VALUES (%s, %s, %s) RETURNING id",
            (cliente, endereco, pego)
        )

        pedido_id = cur.fetchone()[0]

        # Inserir itens
        for item in ferramentas:
            cur.execute(
                "INSERT INTO itens (pedido_id, ferramenta, quantidade) VALUES (%s, %s, %s)",
                (
                    pedido_id,
                    item.get('nome'),
                    item.get('quantidade')
                )
            )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status": "ok",
            "pedido_id": pedido_id
        })

    except Exception as e:
        return jsonify({
            "status": "erro",
            "msg": str(e)
        }), 500


if __name__ == '__main__':
    init_db()  # agora sim correto
    print("🚀 Servidor rodando em http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
