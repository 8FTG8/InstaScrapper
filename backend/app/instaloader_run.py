import instaloader
import requests
import pyshorteners
import time
from datetime import datetime, timedelta

# FUNÇÃO PARA BAIXAR E CLASSIFICAR OS POSTS
def download_and_classify_posts(username, data_inicial, data_final, max_posts = 100):
    loader = instaloader.Instaloader()

    proxies = {
        'http': '198.44.255.5:80',
        'https': '198.44.255.5:80',
    }
    loader.context._session.proxies.update(proxies)
    
    response = requests.get('https://www.instagram.com', proxies=proxies)

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
                    "Data": post.date.strftime("%d/%m/%Y"),
                    "Formato do Post": post.typename,
                    "URL Encurtada": shorten_url,
                    "Legenda": post.caption,
                })

                # Classifica o tipo do post
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
        print(f"Ocorreu um erro ao processar o post: {e}")

# FUNÇÃO PARA CLASSIFICAR LEADS POR ESTRELAS
def classify_profile_stars(posts):
    if not posts:
        return 1
    
    last_post_date = posts[0]["Data"]
    if datetime.now() - last_post_date > timedelta(days=90):
        return 1

    last_ten_posts = posts[:10]
    intervalos = [
        (last_ten_posts[i - 1]["Data"] - last_ten_posts[i]["Data"]).days
        for i in range(1, len(last_ten_posts))
    ]

    if any(intervalo > 10 for intervalo in intervalos):
        return 2
    else: 
        return 3
    
# FUNÇÃO PARA EXTRAIR O NOME DE USUÁRIO DE UM LINK
def extract_username(url_or_username):
    if "instagram.com/" in url_or_username:
        username = url_or_username.split("instagram.com/")[-1].rstrip("/")
        return username
    return url_or_username

# SOLICITA OS PARÂMETROS AO USUÁRIO
if __name__ == "__main__":
    input_data = input("\nInfome o link ou nome do perfil do Instagram: ")
    username = extract_username(input_data)

    data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
    data_final = input("Informe a data final (dd/mm/aaaa): ")

    # CHAMA AS FUNÇÕES
    posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial, data_final)
    estrela = classify_profile_stars(posts if posts else [])

    # EXIBE OS RESULTADOS
    if posts:
        print(f"\n---------- RESULTADOS ----------")
        print(f"Total de posts do período: {len(posts)}")
        print(f"Total de estáticos: {estatico}")
        print(f"Total de carroséis: {carrossel}")
        print(f"Total de reels: {reel}")
        print(f"Classificação do Lead por estrela: {estrela}")
        print(f"\n------------------------------\n")

        for idx, post in enumerate(posts, start = 1):
            print(f"Post {idx}:")
            for chave, valor in post.items():
                print(f"{chave}: {valor}")
            print("\n")
    else:
        print("Nenhuma postagem encontrada ou ocorreu um erro!")