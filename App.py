from flask import Flask, request, jsonify
import yaml

app = Flask(__name__)

# Carrega o decoder YAML
with open("decoderx.yaml", "r") as f:
    decoder_config = yaml.safe_load(f)

# Função simples de decodificação
def decode_amal(raw_code):
    # Exemplo fictício simplificado (você depois substitui pela sua lógica)
    # raw_code = "AMAL:1-5-9-11-14"
    try:
        if not raw_code.startswith("AMAL:"):
            return {"error": "Formato inválido"}

        nums = raw_code.replace("AMAL:", "").split("-")
        nums = [int(n) for n in nums]

        return {
            "decoded_sequence": nums,
            "decoder_used": decoder_config.get("decoder", "X")
        }
    except:
        return {"error": "Falha ao processar código AMAL"}

# Rota principal
@app.route("/decode", methods=["POST"])
def decode():
    data = request.get_json()
    raw = data.get("amal", "")
    result = decode_amal(raw)
    return jsonify(result)

# Necessário para o Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
