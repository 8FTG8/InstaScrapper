import pytest
from datetime import datetime, timedelta
from main import download_and_classify_posts

# Lista de perfis para teste
test_profiles = [
    "instagram.com/fernandeslaboratorio",
    "instagram.com/laboratorio.santa.marta",
    "instagram.com/epigene.dna",
    "instagram.com/labvidamaceio",
    "instagram.com/laboratoriosantema",
    "instagram.com/exatusgene",
    "instagram.com/bioanalisesreserva",
    "instagram.com/labmonlaboratorio",
    "instagram.com/cepac.laboratorio",
    "instagram.com/lab_labcenterr",
    "instagram.com/biocenteranalises",
    "instagram.com/qualilabms",
    "instagram.com/laboratorioessencial",
    "instagram.com/mcservicece",
    "instagram.com/laboratorioescobar",
    "instagram.com/labsantaritadiagnosticos",
    "instagram.com/laboratoriovisao",
    "instagram.com/laboratorioanalisescp",
    "instagram.com/laboratoriodenadai",
    "instagram.com/laboratorioamaro",
]

# Datas de teste
data_inicial = (datetime.now() - timedelta(days = 30)).strftime("%d/%m/%Y")
data_final = datetime.now().strftime("%d/%m/%Y")

@pytest.mark.parametrize("profile", test_profiles)
def test_profiles_analysis(profile):
    try:
        posts, estatico, reel, carrossel = download_and_classify_posts(
            username = profile,
            data_inicial = data_inicial,
            data_final = data_final,
            max_posts = 100
        )
        if isinstance(posts, dict) and 'error' in posts:
            pytest.fail(f"Erro ao testar o perfil {profile}: {posts['error']}")
        
        assert isinstance(posts, list), "Posts devem ser uma lista"
        assert estatico >= 0, "Contador de estáticos não pode ser negativo"
        assert reel >= 0, "Contador de reels não pode ser negativo"
        assert carrossel >= 0, "Contador de carrosséis não pode ser negativo"

    except Exception as e:
        pytest.fail(f"Erro ao testar o perfil {profile}: {e}")