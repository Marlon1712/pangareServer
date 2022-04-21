import os

import cv2
import numpy as np


# Classe para pré-processamento de imagem para que o dataset seja de 32x32 pixels
class SimplePreprocessor:
    def __init__(self, width, height, inter=cv2.INTER_AREA):
        self.width = width
        self.height = height
        self.inter = inter

    def preprocess(self, image):
        return cv2.resize(image, (self.width, self.height), interpolation=self.inter)


# Classe para importação do dataset com o pré-processamento já sendo realizado:
class Loader:
    def __init__(self, preprocessors=None):
        # Armazenamento da pré-processagem definida
        self.preprocessors = preprocessors

        # Se não existir pré-processagem:
        if self.preprocessors is None:
            self.preprocessors = []

    # Carregamento das imagens e separação dos dados e labels
    def load_model(self, imagePaths):
        data = []
        labels = []

        # Pré-processamento para criar o modelo
        # Separação das imagens em dados e labels:
        for (i, imagePath) in enumerate(imagePaths):
            # Como o caminho é organizado como /dataset/{label}/{image}.jpg:
            image = cv2.imread(imagePath)
            label = imagePath.split(os.path.sep)[-2]

            if self.preprocessors is not None:
                # Aplica o pré-processamento em todas as imagens puxadas
                for p in self.preprocessors:
                    image = p.preprocess(image)
            data.append(image)
            labels.append(label)

        return (np.array(data), np.array(labels))

    # Pré-processamento para aplicar o modelo:
    def load_predict(self, imagePaths):
        numeros = []
        displays = []
        # Separação em display e dados:
        for (i, imagePath) in enumerate(imagePaths):
            # Como o caminho é organizado como /dataset/{display}/{image}.jpg:
            image = cv2.imread(imagePath)
            display = imagePath.split(os.path.sep)[-2]

            if self.preprocessors is not None:
                # Aplica o pré-processamento em todas as imagens puxadas
                for p in self.preprocessors:
                    image = p.preprocess(image)
            numeros.append(image)
            displays.append(display)

        return (np.array(numeros), np.array(displays))
