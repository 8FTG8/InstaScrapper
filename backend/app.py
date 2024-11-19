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
                    "URL Encurtado": shorten_url,
                    "Formato do Post": post.typename
                }
                posts_selecionados.append(post_info)

                # CLASSIFICA O TIPO DO POST
                if post.is_video:
                    reels += 1
                else:
                    estaticos += 1

                # CLASSIFICA AS ESTRELAS DO PERFIL
                 

                # FAZ O DOWNLOAD DO POST
                loader.download_post(post, target=username)
                
        # RETORNA OS POSTS COLETADOS
        return posts_selecionados, total, estaticos, reels
                
    except Exception as e:
        print("Ocorreu um erro: ", e)
        return None, 0, 0, 0

# SOLICITA OS PARÂMETROS AO USUÁRIO
if __name__ == "__main__":
    username = input("\nInfome o perfil do Instagram: ")
    data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
    data_final = input("Informe a data final (dd/mm/aaaa): ")

    # CHAMA A FUNÇÃO
    posts, total, estaticos, reels = download_and_classify_posts(username, data_inicial, data_final)

    # EXIBE OS RESULTADOS
    if posts:
        print(f"\nTotal de posts do período: {len(posts)}")
        print(f"Posts estáticos: {estaticos}")
        print(f"Reels: {reels}\n")

        for idx, post in enumerate(posts, start = 1):
            print(f"Post {idx}:")
            for chave, valor in post.items():
                print(f"{chave}: {valor}")
            print("\n")
    else:
        print("Nenhuma postagem encontrada ou ocorreu um erro!")