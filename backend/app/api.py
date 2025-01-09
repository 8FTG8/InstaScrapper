import time
import instaloader
import pyshorteners
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# FUNÇÃO PARA BAIXAR E CLASSIFICAR OS POSTS
def download_and_classify_posts(username, data_inicial, data_final, max_posts=100):
    loader = instaloader.Instaloader()

    estatico, reel, carrossel, posts_selecionados = 0, 0, 0, []
    post_counter = 0

    try:
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y") + timedelta(days=1)
    except ValueError as e:
        return {"error": "Erro no formato das datas"}, 0, 0, 0

    link = pyshorteners.Shortener()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        for post in profile.get_posts():
            
            if post_counter >= max_posts:
                break

            if data_inicial <= post.date < data_final:

                shorten_url = link.tinyurl.short(post.url)

                posts_selecionados.append({
                    "Data": post.date.isoformat(),
                    "Formato do Post": post.typename,
                    "URL Encurtada": shorten_url,
                    "Legenda": post.caption,
                })

                if post.typename == "GraphImage":
                    estatico += 1
                    
                elif post.typename == "GraphSidecar":
                    carrossel += 1

                elif post.is_video:
                    reel += 1
                
                post_counter += 1
                time.sleep(1)

                #loader.download_post(post, target=username)

        return posts_selecionados, estatico, reel, carrossel
    
    except Exception as e:
        return{"error": f"Erro ao processar o perfil: {str(e)}"}, 0, 0, 0

# FUNÇÃO PARA CLASSIFICAR LEADS POR ESTRELAS
def classify_profile_stars(posts):
    if not posts:
        return 1
    
    last_post_date = datetime.fromisoformat(posts[0]["Data"])
    if datetime.now() - last_post_date > timedelta(days = 90):
        return 1
    
    last_ten_posts = posts[:10]
    intervalos = [
        (datetime.fromisoformat(last_ten_posts[i - 1]["Data"]) - datetime.fromisoformat(last_ten_posts[i]["Data"])).days
        for i in range(1, len(last_ten_posts))
    ]
    
    if any(intervalo > 10 for intervalo in intervalos):
        return 2
    else:
        return 3
    
@app.route('/analyze', methods = ['POST'])
def analyze():
    data = request.json
    username = data.get("username")
    data_inicial = data.get("data_inicial")
    data_final = data.get("data_final")

    posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial, data_final)

    if isinstance(posts, dict) and "error" in posts:
        return jsonify(posts), 400
    
    estrela = classify_profile_stars(posts)

    return jsonify({
        "posts": posts,
        "estatico": estatico,
        "reel": reel,
        "carrossel": carrossel,
        "estrela": estrela
    })

if __name__ == '__main__':
    app.run(debug = False)