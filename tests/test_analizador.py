import importlib.util
import inspect
import json
import sys

import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.fixture(scope="session", autouse=True)
def module_members(pytestconfig):
    file = pytestconfig.getoption("module_file")
    module_name = "analizador"
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
    return inspect.getmembers(module)


@pytest.fixture(scope="session")
def module_members_names(module_members):
    return [item[0] for item in module_members]


@pytest.fixture(scope="session")
def module_members_elements(module_members):
    return {item[0]: item[1] for item in module_members}


@pytest.fixture(scope="session")
def analizador_module():
    return importlib.import_module('analizador')


@pytest.fixture(scope="session")
def text_1():
    with open("fixtures/testtext_1.txt", "r", encoding='utf8') as file:
        content = file.read()
    return content


@pytest.fixture(scope="session")
def text_2():
    with open("fixtures/testtext_2.txt", "r", encoding='utf8') as file:
        content = file.read()
    return content


@pytest.fixture(scope="session")
def expected_words_1():
    with open("fixtures/expectedwords_1.json", "r", encoding='utf8') as file:
        words = json.load(file)

    return words


@pytest.fixture(scope="session")
def expected_words_2():
    with open("fixtures/expectedwords_2.json", "r", encoding='utf8') as file:
        words = json.load(file)

    return words


@pytest.fixture
def regla_palabras_ordenadas(analizador_module):
    return analizador_module.ReglaPalabrasMasUsadas()


@pytest.fixture
def regla_conteo_palabras(analizador_module):
    return analizador_module.ReglaConteoPalabras()


@pytest.fixture
def regla_tiempo_lectura(analizador_module):
    return analizador_module.ReglaTiempoLectura()


@pytest.fixture
def analizador(analizador_module):
    return analizador_module.Analizador()


# Test for the existence of elements within the module ---------------------------------------

def test_modulo_contiene_clase_ReglaAnalisis(module_members_elements):
    assert "ReglaAnalisis" in module_members_elements.keys()


def test_modulo_contiene_clase_ReglaPalabrasMasUsadas(module_members_elements):
    assert "ReglaPalabrasMasUsadas" in module_members_elements.keys()


def test_modulo_contiene_clase_ReglaConteoPalabras(module_members_elements):
    assert "ReglaConteoPalabras" in module_members_elements.keys()


def test_modulo_contiene_clase_ReglaTiempoLectura(module_members_elements):
    assert "ReglaTiempoLectura" in module_members_elements.keys()


def test_modulo_contiene_clase_Analizador(module_members_elements):
    assert "Analizador" in module_members_elements.keys()


@pytest.mark.parametrize("method_name, parameters", [
    ("__init__", ["self", "nombre"]),
    ("_separar_palabras", ["texto"]),
    ("analizar", ["texto"])
])
def test_clase_ReglaAnalisis_contiene_metodos(module_members_elements, method_name, parameters):
    class_name = "ReglaAnalisis"
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    class_elements = module_members_elements[class_name].__dict__
    method_parameters = list(inspect.signature(class_elements[method_name]).parameters)

    assert method_name in class_elements.keys() and \
           all(param in method_parameters for param in parameters)


@pytest.mark.parametrize("method_name, parameters", [
    ("__init__", ["self"]),
    ("analizar", ["self", "texto"])
])
def test_clase_ReglaPalabrasMasUsadas_contiene_metodos(module_members_elements, method_name, parameters):
    class_name = "ReglaPalabrasMasUsadas"
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    class_elements = module_members_elements[class_name].__dict__
    method_parameters = list(inspect.signature(class_elements[method_name]).parameters)

    assert method_name in class_elements.keys() and \
           all(param in method_parameters for param in parameters)


@pytest.mark.parametrize("method_name, parameters", [
    ("__init__", ["self"]),
    ("analizar", ["self", "texto"])
])
def test_clase_ReglaConteoPalabras_contiene_metodos(module_members_elements, method_name, parameters):
    class_name = "ReglaConteoPalabras"
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    class_elements = module_members_elements[class_name].__dict__
    method_parameters = list(inspect.signature(class_elements[method_name]).parameters)

    assert method_name in class_elements.keys() and \
           all(param in method_parameters for param in parameters)


@pytest.mark.parametrize("method_name, parameters", [
    ("__init__", ["self"]),
    ("analizar", ["self", "texto"])
])
def test_clase_ReglaTiempoLectura_contiene_metodos(module_members_elements, method_name, parameters):
    class_name = "ReglaTiempoLectura"
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    class_elements = module_members_elements[class_name].__dict__
    method_parameters = list(inspect.signature(class_elements[method_name]).parameters)

    assert method_name in class_elements.keys() and \
           all(param in method_parameters for param in parameters)


@pytest.mark.parametrize("method_name, parameters", [
    ("__init__", ["self"]),
    ("procesar", ["self", "texto"])
])
def test_clase_Analizador_contiene_metodos(module_members_elements, method_name, parameters):
    class_name = "Analizador"
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    class_elements = module_members_elements[class_name].__dict__
    method_parameters = list(inspect.signature(class_elements[method_name]).parameters)

    assert method_name in class_elements.keys() and \
           all(param in method_parameters for param in parameters)


def test_clase_ReglaAnalisis_es_abstracta(module_members_elements, analizador_module):
    super_class_name = "ABC"
    sub_class_name = "ReglaAnalisis"
    if super_class_name not in module_members_elements.keys() and \
            sub_class_name not in module_members_elements.keys():
        pytest.fail(f"{super_class_name} or {sub_class_name} not defined")

    assert issubclass(getattr(analizador_module, sub_class_name), getattr(analizador_module, super_class_name))


def test_clase_ReglaAnalisis_tiene_metodo_abstracto(module_members_elements):
    if "ReglaAnalisis" not in module_members_elements.keys():
        pytest.fail("ReglaAnalisis class not defined")

    assert "analizar" in module_members_elements["ReglaAnalisis"].__dict__['__abstractmethods__']


def test_clase_ReglaAnalisis_tiene_atributo_nombre(module_members_elements):
    class_name = "ReglaPalabrasMasUsadas"
    class_object = module_members_elements[class_name]()
    fields = dir(super(module_members_elements[class_name], class_object))

    assert "nombre" in fields


@pytest.mark.parametrize("super_class_name, sub_class_name", [
    ("ReglaAnalisis", "ReglaPalabrasMasUsadas"),
    ("ReglaAnalisis", "ReglaConteoPalabras"),
    ("ReglaAnalisis", "ReglaTiempoLectura")
])
def test_clases_reglas_heredan_de_ReglaAnalisis(module_members_elements, analizador_module, super_class_name,
                                                sub_class_name):
    if super_class_name not in module_members_elements.keys() and \
            sub_class_name not in module_members_elements.keys():
        pytest.fail(f"{super_class_name} or {sub_class_name} not defined")

    assert issubclass(getattr(analizador_module, sub_class_name), getattr(analizador_module, super_class_name))


def test_clase_ReglaTiempoLectura_contiene_constante(module_members_elements):
    class_name = "ReglaTiempoLectura"
    attribute_name = "TASA_LECTURA"

    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} not defined")

    fields = dir(module_members_elements[class_name]())
    assert attribute_name in fields


def test_clase_Analizador_contiene_atributo(module_members_elements):
    class_name = "Analizador"
    attribute_name = "reglas"

    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} not defined")

    fields = dir(module_members_elements[class_name]())
    assert attribute_name in fields


# Test for the functionality of the elements of the module ------------------------------------------


@pytest.mark.parametrize("text, expected", [
    (lazy_fixture("text_1"), {"de", "y", "se", "un", "en", "la", "a", "sus", "javier", "que"}),
    (lazy_fixture("text_2"), {"este", "usted", "hola", "es", "un", "ejemplo", "para", "que", "practique", "puede"}),
    ("", set()),
    ("a", {"a"})
])
def test_regla_palabras_mas_usadas_analiza_texto(regla_palabras_ordenadas, text, expected):
    result = regla_palabras_ordenadas.analizar(text)
    assert set(result) == expected


@pytest.mark.parametrize("text, expected", [
    (lazy_fixture("text_1"), 281),
    (lazy_fixture("text_2"), 21),
    ("a", 1),
    ("", 0)
])
def test_regla_conteo_palabras_analiza_texto(regla_conteo_palabras, text, expected):
    result = regla_conteo_palabras.analizar(text)
    assert result == expected


@pytest.mark.parametrize("text, expected", [
    (lazy_fixture("text_1"), (1, 10)),
    (lazy_fixture("text_2"), (0, 5)),
    ("a", (0, 0)),
    ("", (0, 0))
])
def test_regla_tiempo_lectura_analiza_texto(regla_tiempo_lectura, text, expected):
    result = regla_tiempo_lectura.analizar(text)
    assert result == expected


def test_analizador_tiene_tres_reglas_despues_de_inicializado(analizador):
    assert len(analizador.reglas) == 3


@pytest.mark.parametrize("text, expected_words", [
    (lazy_fixture("text_1"), lazy_fixture("expected_words_1")),
    (lazy_fixture("text_2"), lazy_fixture("expected_words_2")),
    ("", []),
    ("a", ["a"])
])
def test_regla_analisis_separa_palabras(regla_conteo_palabras, text, expected_words):
    result = regla_conteo_palabras._separar_palabras(text)
    assert result == expected_words


@pytest.mark.parametrize("rule, expected_name", [
    (lazy_fixture("regla_palabras_ordenadas"), "palabras_ordenadas"),
    (lazy_fixture("regla_conteo_palabras"), "conteo_palabras"),
    (lazy_fixture("regla_tiempo_lectura"), "tiempo_lectura"),
])
def test_nombre_regla_es_correcto(rule, expected_name):
    assert rule.nombre == expected_name


@pytest.mark.parametrize("text, expected", [
    (lazy_fixture("text_1"), {
        "palabras_ordenadas": ["de", "y", "se", "un", "en", "la", "a", "sus", "javier", "que"],
        "conteo_palabras": 281,
        "tiempo_lectura": (1, 10)
    }),
    (lazy_fixture("text_2"), {
        "palabras_ordenadas": ["este", "usted", "hola", "es", "un", "ejemplo", "para", "que", "practique", "puede"],
        "conteo_palabras": 21,
        "tiempo_lectura": (0, 5)
    }),
    ("", {"palabras_ordenadas": [], "conteo_palabras": 0, "tiempo_lectura": (0, 0)}),
    ("a", {"palabras_ordenadas": ["a"], "conteo_palabras": 1, "tiempo_lectura": (0, 0)}),
])
def test_analizador_analiza_texto(analizador, text, expected):
    result = analizador.procesar(text)
    assert set(result["palabras_ordenadas"]) == set(expected["palabras_ordenadas"]) \
        and result["conteo_palabras"] == expected["conteo_palabras"] \
        and result["tiempo_lectura"] == expected["tiempo_lectura"]
