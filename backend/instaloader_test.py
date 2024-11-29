import instaloader
import pyshorteners
from datetime import datetime, timedelta

# FUNÇÃO PARA BAIXAR E CLASSIFICAR OS POSTS
def download_and_classify_posts(username, data_inicial, data_final):
    loader = instaloader.Instaloader()
    estatico, reel, carrossel, posts_selecionados = 0, 0, 0, []

    try: # CONVERTE AS DATAS PARA O FORMATO DATETIME
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y") + timedelta(days=1)
    except ValueError as e:
        print("Erro no formato das datas:", e)
        return None, 0, 0
    
    link = pyshorteners.Shortener()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        for post in profile.get_posts():
            if data_inicial <= post.date < data_final:

                shorten_url = link.tinyurl.short(post.url)
                
                posts_selecionados.append({
                    "Data": post.date,
                    "Legenda": post.caption,
                    "URL Encurtada": shorten_url,
                    "Formato do Post": post.typename,
                })

                # CLASSIFICA O TIPO DO POST
                if post.typename == "GraphImage":
                    estatico += 1
                    #post.typename = "Post Estático"
                    
                elif post.typename == "GraphSidecar":
                    carrossel += 1
                    #post.typename = "Carrossel"

                elif post.is_video:
                    reel += 1
                    #post.typename = "Reel/Vídeo"
                
                loader.download_post(post, target=username)

        return posts_selecionados, estatico, reel, carrossel
    
    except Exception as e:
        print("Ocorreu um erro: ", e)
        return None, 0, 0, 0

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

# SOLICITA OS PARÂMETROS AO USUÁRIO
if __name__ == "__main__":
    username = input("\nInfome o perfil do Instagram: ")
    data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
    data_final = input("Informe a data final (dd/mm/aaaa): ")

    # CHAMA As FUNÇÕES
    posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial, data_final)
    estrela = classify_profile_stars(posts if posts else [])

    # EXIBE OS RESULTADOS
    if posts:
        print(f"\n---------- RESULTADOS ----------")
        print(f"Total de posts do período: {len(posts)}")
        print(f"Total de estáticos: {estatico}")
        print(f"Total de reels: {reel}")
        print(f"Classificação do Lead por estrela: {estrela}")
        print(f"\n")

        for idx, post in enumerate(posts, start = 1):
            print(f"Post {idx}:")
            for chave, valor in post.items():
                print(f"{chave}: {valor}")
            print("\n")
    else:
        print("Nenhuma postagem encontrada ou ocorreu um erro!")