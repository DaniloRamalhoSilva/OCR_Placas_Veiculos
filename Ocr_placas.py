
import os
import cv2
import pytesseract
import shutil
from PIL import Image

# Configura o caminho do tesseract.exe (ajuste se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Classe para representar uma placa
class Placa:
    def __init__(self, titulo, imagem_original, x, y, w, h):
        self.titulo = titulo
        self.imagem_original = imagem_original
        self.imagem_cortada = ""
        self.imagem_tratada = ""
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.texto_ocr = ""

# Recorta a imagem de acordo com localização x,y
def RecortarImagem(placa):
    imagem = cv2.imread(placa.imagem_original)
    if imagem is None:
        print(f"[ERRO] Imagem não encontrada: {placa.imagem_original}")
        return
    roi = imagem[placa.y:placa.y + placa.h, placa.x:placa.x + placa.w]
    caminho_saida = os.path.join("PlacasCortadas", placa.titulo)
    cv2.imwrite(caminho_saida, roi)
    placa.imagem_cortada = caminho_saida

# Pré-processamento da imagem para melhor extração do texto
def PreProcessamentoImagem(placa):
    imagem = cv2.imread(placa.imagem_cortada)
    if imagem is None:
        print(f"[ERRO] Imagem cortada não encontrada: {placa.imagem_cortada}")
        return

    # Redimensiona a imagem para aumentar a definição
    escala = 3
    imagem = cv2.resize(imagem, (0, 0), fx=escala, fy=escala, interpolation=cv2.INTER_CUBIC)

    # Conversão para tons de cinza
    gray_image = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Threshold (sem inversão)
    _, thresh_image = cv2.threshold(gray_image, 155, 260, cv2.THRESH_BINARY)

    # Suavização e reforço de contornos
    blurred_image = cv2.GaussianBlur(thresh_image, (3, 3), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed_image = cv2.dilate(blurred_image, kernel, iterations=1)

    caminho_saida = os.path.join("PlacasTratadas", placa.titulo)
    cv2.imwrite(caminho_saida, imagem)
    placa.imagem_tratada = caminho_saida

# Monta uma lista da classe Placa a partir da pasta com imagens e do CSV
def MontarListaDePlacas(pasta_imagens, caminho_csv):
    placas = []
    with open(caminho_csv, 'r', encoding='utf-8') as arquivo:
        next(arquivo)  # Pula o cabeçalho
        for linha in arquivo:
            partes = linha.strip().split('\t')
            if len(partes) == 5:
                nome, x, y, w, h = partes
                caminho_imagem = os.path.join(pasta_imagens, f"{nome}.png")
                if os.path.exists(caminho_imagem):
                    placas.append(Placa(f"{nome}.png", caminho_imagem, x, y, w, h))
    return placas

# Faz o OCR
def FazerOCR(placa):
    imagem = Image.open(placa.imagem_tratada)
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    texto = pytesseract.image_to_string(imagem, config=custom_config)
    placa.texto_ocr = texto.strip()

if __name__ == "__main__":
    # Cria/limpa as pastas de saída
    for pasta in ["PlacasCortadas", "PlacasTratadas"]:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
        os.makedirs(pasta)

    # Caminhos
    pasta_imagens = r'C:\Users\Raul\Desktop\Danilo\CP3-OCR-Placas\Placas'
    caminho_csv = r'C:\Users\Raul\Desktop\Danilo\CP3-OCR-Placas\Placas\labelLocalizacao.csv'

    # Executa pipeline
    placas = MontarListaDePlacas(pasta_imagens, caminho_csv)

    for placa in placas:
        RecortarImagem(placa)
        PreProcessamentoImagem(placa)
        FazerOCR(placa)
        print(f"[{placa.titulo}] Texto OCR: {placa.texto_ocr}")