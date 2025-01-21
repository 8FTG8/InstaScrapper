import random
from datetime import datetime, timedelta
import instaloader
import pyshorteners
import time

# FUNÇÃO PARA SELECIONAR PROXY ALEATÓRIO
def get_random_proxy(proxies, used_proxies):
    avaliable_proxies = [proxy for proxy in proxies if proxy not in used_proxies]
    if not avaliable_proxies:
        raise ValueError("Nenhum proxy dispónível.")
    proxy = random.choice(avaliable_proxies)
    used_proxies.add(proxy)
    return proxy

# FUNÇÃO PARA VALIDAR DATAS
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        raise ValueError(f"Data inválida: {date_str}. Formato esperado: dd/mm/aaa.")

# FUNÇÃO PARA FAZER LOGIN NO INSTAGRAM
def login_instaloader(loader, proxies):
    used_proxies = set()
    for attempt in range(len(proxies)):
        try:
            proxy = get_random_proxy(proxies, used_proxies)
            loader.context.proxies = {"http": proxy, "https": proxy}
            loader.login('produtodrfisiologia', 'qwert00...')
            print(f"Login bem-sucedido usando proxy {proxy}.")
            return
        except Exception as e:
            print(f"Erro ao usar o proxy {proxy}: {e}")
    raise ConnectionError("Falha ao conectar com proxies")

# FUNÇÃO PARA BAIXAR E CLASSIFICAR OS POSTS
def download_and_classify_posts(username, data_inicial, data_final, max_posts = 100):
    loader = instaloader.Instaloader()
    proxies = [
        "http://us.ca.proxymesh.com:31280"
    ]

    login_instaloader(loader, proxies)
    data_inicial = validate_date(data_inicial)
    data_final = validate_date(data_final) + timedelta(days = 1)

    estatico, reel, carrossel, posts_selecionados = 0, 0, 0, []
    post_counter = 0
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
                time.sleep(random.uniform(1, 3))
                loader.download_post(post, target=username)

        return posts_selecionados, estatico, reel, carrossel
    
    except Exception as e:
        print(f"Erro ao processar o perfil '{username}': {e}")
        return [], 0, 0, 0

# FUNÇÃO PARA CLASSIFICAR LEADS POR ESTRELAS
def classify_profile_stars(posts):
    if not posts:
        return 1
    
    last_post_date = validate_date(posts[0]["Data"])
    if datetime.now() - last_post_date > timedelta(days=90):
        return 1f
    
    last_ten_posts = [validate_date(post["Data"]) for post in posts[:10]]
    intervalos = [
        (last_ten_posts[i - 1] - last_ten_posts[i]).days
        for i in range(1, len(last_ten_posts))
    ]
    return 2 if any(intervalo > 10 for intervalo in intervalos) else 3
    
# FUNÇÃO PARA EXTRAIR O NOME DE USUÁRIO DE UM LINK
def extract_username(url_or_username):
    if "instagram.com/" in url_or_username:
        username = url_or_username.split("instagram.com/")[-1].rstrip("/")
        return username
    return url_or_username

# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    while True:
        try:
            input_data = input("\nInforme o link ou nome do perfil do Instagram: ")
            username = extract_username(input_data)
            data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
            data_final = input("Informe a data final (dd/mm/aaaa): ")

            # CHAMA AS FUNÇÕES
            posts, estatico, reel, carrossel = download_and_classify_posts(username, data_inicial, data_final)
            estrela = classify_profile_stars(posts)

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
        except Exception as e:
            print(f"Erro: {e}")