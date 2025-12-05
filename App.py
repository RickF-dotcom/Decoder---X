from flask import Flask, request, jsonify
import yaml

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Decoder-X ativo"}

@app.route("/decode", methods=["POST"])
def decode():
    try:
        # recebe o payload em texto
        payload = request.data.decode("utf-8")

        # tenta interpretar como YAML
        data = yaml.safe_load(payload)

        # demonstra retorno (AQUI você coloca sua lógica real)
        return jsonify({
            "recebido": data,
            "status": "processado com sucesso"
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
