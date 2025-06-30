# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
import os
import zipfile
import pandas as pd
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    # Ruta del archivo zip
    zip_path = os.path.join("files", "input.zip")
    # Carpeta destino para la extracción (se espera que se cree "files/input")
    input_folder = os.path.join("files", "input")
    
    # Crear la carpeta "files/input" si no existe
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    
    # Descomprimir el archivo zip en la carpeta "files/input"
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(input_folder)
    
    # Verificar si la estructura extraída tiene la carpeta "train" en el nivel esperado.
    # Si no se encuentra, es posible que el zip contenga una carpeta raíz extra.
    expected_train_path = os.path.join(input_folder, "train")
    if not os.path.isdir(expected_train_path):
        # Listar las carpetas dentro de input_folder
        subdirs = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
        # Si hay solo una carpeta, asumimos que es la raíz real de los datos
        if len(subdirs) == 1:
            input_folder = os.path.join(input_folder, subdirs[0])
        else:
            raise FileNotFoundError("No se encontró la carpeta 'train' en la estructura extraída.")
    
    # Crear la carpeta de salida "files/output"
    output_folder = os.path.join("files", "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Procesar cada conjunto de datos: train y test
    for dataset in ["train", "test"]:
        dataset_path = os.path.join(input_folder, dataset)
        csv_filename = os.path.join(output_folder, f"{dataset}_dataset.csv")
        registros = []  # Lista para almacenar los registros
        
        # Se asume que cada dataset tiene las subcarpetas: negative, positive y neutral
        for sentiment in ["negative", "positive", "neutral"]:
            sentiment_path = os.path.join(dataset_path, sentiment)
            if not os.path.isdir(sentiment_path):
                raise FileNotFoundError(f"No se encontró la carpeta esperada: {sentiment_path}")
            # Listar y ordenar los archivos .txt
            for filename in sorted(os.listdir(sentiment_path)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(sentiment_path, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        phrase = file.read().strip()
                    registros.append([phrase, sentiment])
        
        # Crear un DataFrame y guardar en CSV con columnas "phrase" y "target"
        df = pd.DataFrame(registros, columns=["phrase", "target"])
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"Archivo guardado: {csv_filename}")

def main():
    # Llamar a la función para procesar y generar los archivos CSV
    pregunta_01()

if __name__ == "__main__":
    main()