import json
from importlib.resources import files
from pathlib import Path

from analizador.modelo.analizador import Analizador, ReglaPalabrasMasUsadas

if __name__ == "__main__":
    with open(str(files("tests").joinpath(Path("fixtures/testtext_2.txt"))), encoding='utf8') as file:
        texto = file.read()

    # regla = ReglaPalabrasMasUsadas()
    # with open("tests/fixtures/expectedwords_2.json", "w", encoding="utf8") as file:
    #     json.dump(regla._separar_palabras(texto), file)

    analizador = Analizador()
    print(json.dumps(analizador.procesar(texto)))
