import pytesseract
from cv2 import cv2 as cv
from matplotlib import pyplot as plt

# image_path = "./src/img/printGrfTeste.png"
image_path = "./src/img/Print/print.jpg"

pytesseract.pytesseract.tesseract_cmd = "./tesseract/tesseract.exe"
custom_oem_psm_config = r"--oem 3 --psm 6"


def predicao(imagem, x, y, w, h):
    # img = cv.imread(imagem, cv.COLOR_BGR2RGB)
    im = cv.imread(imagem)
    im = im[y : y + h, x : x + w]
    im = cv.resize(im, (560, 144), interpolation=cv.INTER_NEAREST)
    img = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    _, th = cv.threshold(gray, 200, 255, cv.THRESH_BINARY_INV)  #
    # img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv.findContours(th, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    # mask = np.zeros(im.shape[:2], dtype="uint8")
    cv.drawContours(th, contours, -1, (0, 0, 255), 10)

    result = pytesseract.image_to_string(th, config=custom_oem_psm_config)
    print(result)
    plt.imshow(th, cmap="gray")  # cmap="gray"
    plt.show()


# predicao(image_path, 240, 120, 65, 25) # Data
# predicao(image_path, 325, 120, 130, 25)  # Hora
# predicao(image_path, 235, 246, 135, 30)  # Recipientes Processados

predicao(image_path, 485, 85, 110, 24)  # Recipientes Processados
