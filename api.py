from flask import Flask, request, jsonify, render_template
from datetime import datetime
from main import download_and_classify_posts, classify_profile_stars
import time

app = Flask(__name__, static_folder='static')

# Rota principal
@app.route('/')
def home():
    return render_template('index.html', time=int(time.time()))  # Passa o timestamp atual para evitar cache
    

# Rota para análise de posts
@app.route('/analyze_posts', methods=['POST'])
def analyze_posts():
    data = request.json
    username = data.get("username")
    data_inicial = data.get("start_date")
    data_final = data.get("end_date")

    if not username or not data_inicial or not data_final:
        return jsonify({"error": "Parâmetros ausentes ou inválidos"}), 400
    
    # Convertendo as datas para objetos datetime
    try:
        data_inicial_dt = datetime.strptime(data_inicial, '%d/%m/%Y')
        data_final_dt = datetime.strptime(data_final, '%d/%m/%Y')
    except ValueError:
        return jsonify({"error": "Formato de data inválido"}), 400

    data_inicial_str = data_inicial_dt.strftime('%d/%m/%Y')
    data_final_str = data_final_dt.strftime('%d/%m/%Y')

    if data_inicial_str > data_final_str:
        return jsonify({"error": "Data inicial não pode ser maior que a data final"}), 400

    try:
        # Função do back-end para download e classificação dos posts
        posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial_str, data_final_str)
        estrela = classify_profile_stars(posts)

        # Construção da resposta
        response = {
            "posts_count": len(posts),
            "estatico": estatico,
            "reel": reel,
            "carrossel": carrossel,
            "estrela": estrela,
            "posts": posts,  # Certifique-se de que posts tenha a estrutura correta
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500
    
if __name__ == "__main__":
    app.run(debug=True)