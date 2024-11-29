from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
import pyshorteners
import time

# CONFIGURAÇÃO DO WEBDRIVER
def init_driver():
    service = Service(ChromeDriverManager().install()) 
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Inicializa o driver com o serviço e as opções configuradas
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# FUNÇÃO PARA BAIXAR E CLASSIFICAR POSTS
def download_and_classify_posts(driver, profile, data_inicial, data_final):
    estatico, reel, carrossel, posts_selecionados = 0, 0, 0, []
    shortener = pyshorteners.Shortener()

    # CONVERTE AS DATAS PARA FORMATO DATETIME
    try:
        data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
        data_final = datetime.strptime(data_final, "%d/%m/%Y") + timedelta(days=1)
    except ValueError as e:
        print("Erro no formato das datas:", e)
        return None, 0, 0, 0
    
    # ACESSA O PERFIL
    driver.get(f"https://www.instagram.com/{profile}/")
    time.sleep(5) # Aguarda o perfil carregar

    # ENCONTRA OS POSTS E OS CLASSIFICA
    posts_elements = driver.find_elements(By.XPATH, '//article//a')
    for posts_element in posts_elements:
        try:
            post_url = posts_element.get_attribute("href")
            posts_element.click()
            time.sleep(3)

            # Coleta dados do post
            date_element = driver.find_element(By.XPATH, "//time")
            post_date = datetime.strptime(date_element.get_attribute("datetime")[:10], "%Y-%m-%d")

            if data_inicial <= post_date < data_final:
                caption = driver.find_element(By.XPATH, '//div[@role="dialog"]//span').text
                post_type = "Reel" if "reel" in post_url else "Carrossel" if len(driver.find_elements(By.XPATH, '//div[@role="dialog"]//img')) > 1 else "Estático"

                 # Atualiza contadores
                if post_type == "Estático":
                    estatico += 1
                elif post_type == "Carrossel":
                    carrossel += 1
                elif post_type == "Reel":
                    reel += 1

                # Encurta o URL
                shorten_url = shortener.tinyurl.short(post_url)

                # Adiciona o post à lista
                posts_selecionados.append({
                    "Data": post_date,
                    "Legenda": caption,
                    "URL Encurtada": shorten_url,
                    "Formato do Post": post_type,
                })

            # Fecha o post
            driver.find_element(By.XPATH, '//div[@role="dialog"]/div/button').click()
            time.sleep(2)
        
        except Exception as e:
            print(f"Erro ao processar post: {e}")
            continue

    return posts_selecionados, estatico, carrossel, reel

# SOLICITA OS PARÂMETROS AO USUÁRIO
if __name__ == "__main__":
    profile = input("\nInforme o perfil público a ser analisado: ")
    data_inicial = input("Informe a data inicial (dd/mm/aaaa): ")
    data_final = input("Informe a data final (dd/mm/aaaa): ")

     # INICIALIZA O DRIVER E EXECUTA O SCRIPT
    driver = init_driver()
    try:
        posts, estatico, reel, carrossel = download_and_classify_posts(driver, profile, data_inicial, data_final)

        # EXIBE OS RESULTADOS
        if posts:
            print("\n---------- RESULTADOS ----------")
            print(f"Total de posts do período: {len(posts)}")
            print(f"Total de estáticos: {estatico}")
            print(f"Total de carrosséis: {carrossel}")
            print(f"Total de reels: {reel}\n")

            for idx, post in enumerate(posts, start=1):
                print(f"Post {idx}:")
                for chave, valor in post.items():
                    print(f"{chave}: {valor}")
                print("\n")
        else:
            print("Nenhuma postagem encontrada ou ocorreu um erro!")
    finally:
        driver.quit()