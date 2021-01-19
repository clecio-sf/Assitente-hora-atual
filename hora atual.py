import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
import requests
from bs4 import BeautifulSoup
import re

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"

# expressão regex para validar o formato de hora recebido no web scraping
formato_hora = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')


def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    global configuracao

    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

    with open(CAMINHO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)

        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]
        arquivo_configuracao.close()


# função para verificar se o formato do que foi recebido
# está igual ao definido no regex
def verificar_formato_hora(horas):
    return bool(formato_hora.match(horas))


def busca_horario(objeto):
    # concatena no local recebido o '+', para ficar no padrão usado pelo google
    # ex: vitoria da conquista ficará vioria+da+conquista
    local = '+'.join(objeto)

    # url do google utilizada para o web scraping, concatenando ao final
    # da url o local informado pelo usuario para a pesquisa
    url = 'https://www.google.com/search?q=hora+' + local

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    # após receber o resultado da url, é retirado das classes html somente
    # as informações importantes, neste caso a hora e local
    hora, local = soup.find('div', class_='BNeawe').text, soup.find(
        'span', class_='rQMQod').text

    return hora, local


def escutar_comando():
    global reconhecedor

    comando = None

    with sr.Microphone() as fonte_audio:
        # ajuste para gravação em abientes com barulho
        reconhecedor.adjust_for_ambient_noise(fonte_audio)

        print("Fale alguma coisa...")
        fala = reconhecedor.listen(fonte_audio)

        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
            print('Eu falei', comando)
        except sr.UnknownValueError:
            print('Não entendi o que você disse, por favor repita')
            pass

    return comando


def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada

    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)

    return tokens_filtrados


def tokenizar_comando(comando):
    global nome_assistente

    acao = None
    objeto = None

    tokens = word_tokenize(comando.lower(), IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)
        if len(tokens) >= 2:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                if(len(tokens) >= 3):
                    # caso seja informado um local para pesquisa do horario
                    # ele será recebido na posição 2 em diante
                    objeto = tokens[2:]
                else:
                    # não sendo informado nenhum local para pesquisa do horario
                    # é feito a pesquisa do horario no Brasil
                    objeto = "Brasil"

    return acao, objeto


def validar_comando(acao, objeto):
    global acoes
    valido = False

    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                valido = True
                break

    return valido


def executar_comando(acao, objeto):
    print("Buscando horário...")


if __name__ == '__main__':
    iniciar()

    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    executar_comando(acao, objeto)
                    hora, local = busca_horario(objeto)
                    # caso o google retorne um formato igual ao defindo no regex
                    # será validado na função verificar_formato_hora
                    # e impresso para o usuario
                    if(verificar_formato_hora(hora)):
                        print(f'Agora são {hora} em {local}')
                    else:
                        # caso o retorno do google nao esteja no formato
                        # definido no regex, não será validado na função
                        print('Local não encontrado, por favor tente novamente')
                else:
                    print('Comando Inválido')
        except KeyboardInterrupt:
            print("Tchau!")

            continuar = False
