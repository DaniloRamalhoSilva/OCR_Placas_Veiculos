# 🧾 OCR de Placas de Veículos com Python, OpenCV e Tesseract

## 📌 Descrição
Este projeto tem como objetivo extrair automaticamente o texto de placas de veículos a partir de imagens utilizando **Tesseract OCR** integrado com **OpenCV** para pré-processamento de imagens.

---

## ⚙️ Tecnologias utilizadas

- Python 3.x
- OpenCV (`opencv-python`)
- Tesseract OCR (`pytesseract`)
- Pillow (`PIL`)
- NumPy
- Ambiente virtual com `requirements.txt`

---

## 📂 Estrutura do Projeto

```
OCR_Placas_Veiculos/
├── Placas/                       # Pasta com as imagens de entrada (.png)
│   └── labelLocalizacao.csv      # CSV com as coordenadas de corte (nome, x, y, w, h)
├── PlacasCortadas/               # Gerada automaticamente
├── PlacasTratadas/               # Gerada automaticamente
├── Ocr_placas.py                 # Código principal
├── requirements.txt              # Dependências do projeto
└── README.md
```

---

## 🔧 Instalação e Configuração

### 1. Clone o repositório:
```bash
git clone https://github.com/DaniloRamalhoSilva/OCR_Placas_Veiculos
cd OCR_Placas_Veiculos
```

### 2. Crie um ambiente virtual:
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual:
- **Windows**
```bash
venv\Scripts\activate
```
- **Linux/Mac**
```bash
source venv/bin/activate
```

### 4. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 5. Configure o Tesseract OCR:
Instale o [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) e ajuste o caminho no seu script:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🚀 Execução

Com as imagens e o arquivo `labelLocalizacao.csv` na pasta `Placas/`, execute:

```bash
python Ocr_placas.py
```

Isso irá:
- Recortar as regiões das placas com base no CSV
- Realizar o pré-processamento com OpenCV
- Aplicar OCR com Tesseract
- Exibir os textos extraídos no terminal
- Salvar imagens cortadas e processadas nas pastas respectivas

---

## 🔍 Etapas de Processamento

1. **Leitura do CSV** com localização das placas
2. **Recorte da placa** na imagem original com redimensionamento proporcional
3. **Pré-processamento com OpenCV**:
   - Conversão para tons de cinza
   - Thresholding binário
   - Blur + Dilatação
4. **Reconhecimento de texto (OCR)** com Tesseract, modo PSM 7
5. **Saída com log no terminal** e imagens geradas

---

## 📈 Resultados e Considerações Finais

Durante os testes com 5 imagens distintas, os seguintes resultados foram obtidos:

```
CORRETO: RI02A19 - Texto OCR: R1ODA1D4 
CORRETO: GAE0244 - Texto OCR: GAE0244 
CORRETO: PZL9906 - Texto OCR: PZL9905 
CORRETO: PLL6F50 - Texto OCR: 
CORRETO: CDV2172 - Texto OCR: 172 
CORRETO: OUK9627 - Texto OCR:
```

### 📝 Observações:
- A **conversão simples para tons de cinza** apresentou resultados superiores à combinação completa de técnicas (thresholding, blur e dilatação).
- Como as imagens variam muito em qualidade, nitidez e iluminação, **cada uma exigiria um tratamento específico** para um desempenho ideal de OCR.
- Com um pipeline genérico e técnicas simples, os resultados foram limitados, mas servem como base sólida para estudos sobre pré-processamento e OCR com Python.

---
