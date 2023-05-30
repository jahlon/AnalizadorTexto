import math
from abc import ABC, abstractmethod
from typing import Any


class ReglaAnalisis(ABC):

    def __init__(self, nombre: str):
        self.nombre: str = nombre

    @staticmethod
    def _separar_palabras(texto: str) -> list[str]:
        palabras = []
        if len(texto) > 0:
            texto_minuscula: str = texto.lower().replace("\n", " ")
            palabras_con_puntuacion = texto_minuscula.split(" ")
            for palabra in palabras_con_puntuacion:
                palabras.append(palabra.strip(".,?!¡¿"))

        return palabras

    @abstractmethod
    def analizar(self, texto: str) -> Any:
        ...


class ReglaPalabrasMasUsadas(ReglaAnalisis):

    def __init__(self):
        super().__init__(nombre="palabras_ordenadas")

    def analizar(self, texto: str) -> Any:
        palabras = self._separar_palabras(texto)
        conteo_palabras = {}
        for palabra in palabras:
            if palabra not in conteo_palabras:
                conteo_palabras[palabra] = 1
            else:
                conteo_palabras[palabra] += 1
        palabras_ordenadas = sorted(conteo_palabras.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in palabras_ordenadas[:10]]


class ReglaConteoPalabras(ReglaAnalisis):

    def __init__(self):
        super().__init__(nombre="conteo_palabras")

    def analizar(self, texto: str) -> Any:
        palabras = self._separar_palabras(texto)
        return len(palabras)


class ReglaTiempoLectura(ReglaAnalisis):

    TASA_LECTURA: int = 238

    def __init__(self):
        super().__init__(nombre="tiempo_lectura")

    def analizar(self, texto: str) -> Any:
        palabras = self._separar_palabras(texto)
        total_palabras = len(palabras)
        tiempo = total_palabras / ReglaTiempoLectura.TASA_LECTURA
        decimal, entero = math.modf(tiempo)
        minutos = int(entero)
        segundos = int(decimal * 60)
        return minutos, segundos


class Analizador:

    def __init__(self):
        self.reglas: list[ReglaAnalisis] = []
        self.reglas.append(ReglaPalabrasMasUsadas())
        self.reglas.append(ReglaConteoPalabras())
        self.reglas.append(ReglaTiempoLectura())

    def procesar(self, texto: str) -> dict[str, Any]:
        resultado = {}
        for regla in self.reglas:
            resultado[regla.nombre] = regla.analizar(texto)
        return resultado
