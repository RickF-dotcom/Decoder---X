from flask import Flask, request, jsonify
import yaml
import os

app = Flask(__name__)

# ===== Carrega configuração do decodificador =====

DECODER_CONFIG = {}

def load_decoder_config():
    global DECODER_CONFIG
    cfg_path = os.path.join(os.path.dirname(__file__), "decoderx.yaml")
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            DECODER_CONFIG = yaml.safe_load(f) or {}
    except Exception as e:
        # Se der erro, deixa uma config padrão e loga o problema
        print(f"[Decoder-X] Erro ao carregar decoderx.yaml: {e}")
        DECODER_CONFIG = {}

load_decoder_config()

def get_total_numbers():
    """
    Quantidade de dezenas que a máscara representa.
    Pega do YAML; se não tiver, assume 25 (Lotofácil).
    """
    try:
        return int(DECODER_CONFIG.get("config", {}).get("total_numbers", 25))
    except Exception:
        return 25

# ===== Lógica de decodificação =====

def decode_binary_mask(mask: str):
    """
    Recebe string binária (ex: '01001100101010')
    e devolve lista de dezenas ['01','04',...].
    """
    # limpa espaços e quebras
    mask = (mask or "").strip().replace(" ", "").replace("\n", "")

    if not mask:
        raise ValueError("máscara vazia")

    # valida se só tem 0 e 1
    if any(c not in "01" for c in mask):
        raise ValueError("a máscara deve conter apenas 0 e 1")

    total = get_total_numbers()

    # ajusta tamanho: se for menor, faz zero-pad à esquerda; se for maior, pega os últimos bits
    if len(mask) < total:
        mask = mask.zfill(total)
    elif len(mask) > total:
        mask = mask[-total:]

    # posição 1 -> '01', posição 2 -> '02', etc.
    dezenas = []
    for idx, bit in enumerate(mask, start=1):
        if bit == "1":
            dezenas.append(f"{idx:02d}")

    return dezenas

# ===== Rotas HTTP =====

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Decoder-X ativo"})


@app.route("/decode", methods=["POST"])
def decode():
    try:
        # corpo vem como texto/YAML (ex: input: "0100...")
        payload_raw = request.data.decode("utf-8")
        data = yaml.safe_load(payload_raw) or {}

        if not isinstance(data, dict):
            raise ValueError("payload deve ser um objeto YAML/JSON com campo 'input'")

        mask = data.get("input")
        if mask is None:
            raise ValueError("campo 'input' é obrigatório")

        dezenas = decode_binary_mask(str(mask))

        return jsonify({
            "input": str(mask),
            "decoded": dezenas,
            "decoded_str": " ".join(dezenas),
            "status": "ok"
        })

    except Exception as e:
        # erro controlado -> 400
        return jsonify({"status": "erro", "detalhe": str(e)}), 400


if __name__ == "__main__":
    # Render usa essa linha quando roda localmente também
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
