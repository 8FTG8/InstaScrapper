from flask import Flask, request, jsonify, render_template
from datetime import datetime
from back.main import download_and_classify_posts, classify_profile_stars

app = Flask(__name__)

# Validação de datas
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_posts', methods=['POST'])
def analyze_posts():
    data = request.json
    username = data.get("username")
    data_inicial = validate_date(data.get("start_date"))
    data_final = validate_date(data.get("end_date"))

    if not username or not data_inicial or not data_final:
        return jsonify({"error": "Parâmetros ausentes ou inválidos"}), 400
    if data_inicial > data_final:
        return jsonify({"error": "Data inicial não pode ser maior que a data final"}), 400

    try:
        # Função do back-end para download e classificação dos posts
        posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial, data_final)
        estrela = classify_profile_stars(posts)

        # Construção da resposta
        response = {
            "posts_count": len(posts),
            "estatico": estatico,
            "reel": reel,
            "carrossel": carrossel,
            "estrela": estrela,
            "posts": posts,  # Certifique-se de que `posts` tenha a estrutura correta
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)