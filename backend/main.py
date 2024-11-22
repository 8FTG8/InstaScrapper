import instaloader
import pyshorteners
from datetime import datetime, timedelta

# FUNÇÃO PARA BAIXAR E CLASSIFICAR OS POSTS
def download_and_classify_posts(username, data_inicial, data_final):

    # INICIALIZA O INSTALOADER
    loader = instaloader.Instaloader()

    # CONTADORES DE REELS, POSTS ESTÁTICOS E TOTAL DE POSTS
    total = 0
    estaticos = 0
    reels = 0

    # CONVERTE AS DATAS PARA O FORMATO DATETIME
    data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
    data_final = datetime.strptime(data_final, "%d/%m/%Y") + timedelta(days=1)

    # LISTA PARA ARMAZENAR OS POSTS SELECIONADOS
    posts_selecionados = []

    try:
        # OBTÉM O PERFIL DO INSTAGRAM
        profile = instaloader.Profile.from_username(loader.context, username)

        # PERCORRE TODOS OS POSTS DO PERFIL
        for post in profile.get_posts():

            # VERIFICA SE O POST ESTÁ DENTRO DO INTERVALO DE DATAS
            if data_inicial <= post.date < data_final:

                # ENCURTA A URL DO POST
                link = pyshorteners.Shortener()
                shorten_url = link.tinyurl.short(post.url)

                # COLETA INFORMAÇÕES DO POST
                post_info = {
                    "Data": post.date,
                    "Legenda": post.caption,
                    "URL Encurtada": shorten_url,
                    "Formato do Post": post.typename
                }
                posts_selecionados.append(post_info)

                # CLASSIFICA O TIPO DO POST
                if post.is_video:
                    reels += 1
                else:
                    estaticos += 1
                
                # FAZ O DOWNLOAD DO POST
                # loader.download_post(post, target=username)
                
        # RETORNA OS POSTS COLETADOS
        return posts_selecionados, total, estaticos, reels
                
    except Exception as e:
        print("Ocorreu um erro: ", e)
        return None, 0, 0, 0

# FUNÇÃO PARA CLASSIFICAR CLIENTE POR ESTRELAS
def classify_profile_stars(posts):

    # SE NENHUM POST FOI ENCRONTRADO = 1 ESTRELA
    if not posts:
        estrela = 1
        return estrela

    # CALCULA A DATA DO ÚLTIMO POST
    last_post_date = posts[0]["Data"]

    # SE O ÚLTIMO POST FOI A MAIS DE 90 DIAS = 1 ESTRELA
    if datetime.now() - last_post_date > timedelta(days=90):
        estrela = 1
        return estrela
    
    # CONSIDERA OS ÚLTIMOS 10 POSTS
    last_ten_posts = posts[:10]

    # VERIFICA OS INTERVALOS PARA DETERMINAR A FREQUÊNCIA
    intervalos = []
    for i in range(1, len(last_ten_posts)):
        intervalo = last_ten_posts[i-1]["Data"] - last_ten_posts[i]["Data"]
        intervalos.append(intervalo.days)

        # SE OS INTERVALOS SÃO MAIORES QUE 10 DIAS EM QUALQUER CASO = 2 ESTRELAS
        if any(intervalo > 10 for intervalo in intervalos):
            estrela = 2
            return estrela

        # SE OS INTERVALOS SÃO ATÉ 10 DIAS = 3 ESTRELAS
        else: 
            estrela = 3
            return estrela

# SOLICITA OS PARÂMETROS AO USUÁRIO
if __name__ == "__main__":
    username = input("\nInfome o perfil do Instagram: ")
    data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
    data_final = input("Informe a data final (dd/mm/aaaa): ")

    # CHAMA As FUNÇÕES
    posts, total, estaticos, reels = download_and_classify_posts(username, data_inicial, data_final)
    estrela = classify_profile_stars(posts)

    # EXIBE OS RESULTADOS
    if posts:
        print(f"\n---------- RESULTADOS ----------")
        print(f"Total de posts do período: {len(posts)}")
        print(f"Total de estáticos: {estaticos}")
        print(f"Total de reels: {reels}")
        print(f"Classificação do Lead por estrela: {estrela}")
        print(f"\n")

        for idx, post in enumerate(posts, start = 1):
            print(f"Post {idx}:")
            for chave, valor in post.items():
                print(f"{chave}: {valor}")
            print("\n")
    else:
        print("Nenhuma postagem encontrada ou ocorreu um erro!")