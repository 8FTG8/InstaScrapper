import instaloader
from datetime import datetime

def download_and_classify_posts(username, data_inicial, data_final):

    # INICIALIZA O INSTALOADER
    loader = instaloader.Instaloader()

    # CONTADORES DE REELS E POSTS ESTÁTICOS
    estaticos = 0
    reels = 0

    # CONVERTE AS DATAS PARA O FORMATO DATETIME
    data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
    data_final = datetime.strptime(data_final, "%d/%m/%Y")

    # LISTA PARA ARMAZENAR OS POSTS SELECIONADOS
    pots_selecionados = []

    try:
        # OBTÉM O PERFIL DO INSTAGRAM
        profile = instaloader.Profile.from_username(loader.context, username)

        # PERCORRE TODOS OS POSTS DO PERFIL
        for post in profile.get_posts():
            # VERIFICA SE O POST ESTÁ DENTRO DO INTERVALO DE DATAS
            if data_inicial <= post.date <= data_final:
                # COLETA INFORMAÇÕES DO POST
                post_info = {
                    "Data: ", post.date,
                    "Legenda: ", post.caption,
                    "URL da imagem: ", post.url,
                    "Formato do post: ", post.typename
                }
                pots_selecionados.append(post_info)

                # CLASSIFICA O TIPO DO POST
                if post.is_video:
                    reels += 1
                else:
                    estaticos += 1
                
                # FAZ O DOWNLOAD DO POST
                loader.download_post(post, target=username)

                # EXIBE O TOTAL DE POSTS ENCONTRADOS
                print(f"Total de reels: {reels}")
                print(f"Total de posts estáticos: {estaticos}")

                # RETORNA OS POSTS COLETADOS
                return pots_selecionados
                
    except Exception as e:
        print("Ocorreu um erro: ", e)
        return None
    
# PARÂMETROS DE ENTRADA
username = "leomessi"
data_inicial = "05/11/2024"
data_final = "15/11/2024"

posts = download_and_classify_posts(username, data_inicial, data_final)

if posts:
    for idx, post in enumerate(posts, start = 1):
        print(f"Total de posts {idx}: ")
        for chave, valor in post.items():
            print(f"{chave}:{valor}")