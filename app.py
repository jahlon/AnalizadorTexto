import json

from analizador.analizador import Analizador

if __name__ == "__main__":
    texto = "Hola, este es un ejemplo para que usted practique. Usted puede tomar este texto y" \
            " usarlo como su caso de prueba."
    analizador = Analizador()
    print(json.dumps(analizador.procesar(texto)))
