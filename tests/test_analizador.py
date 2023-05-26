import importlib.util
import inspect
import sys

import pytest


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


@pytest.mark.parametrize("class_name", [
    "ReglaAnalisis",
    "ReglaPalabrasMasUsadas",
    "ReglaConteoPalabras",
    "ReglaTiempoLectura",
    "Analizador"
])
def test_modulo_contiene_clase(module_members_elements, class_name):
    assert class_name in module_members_elements.keys()


@pytest.mark.parametrize("class_name, method_name", [
    ("ReglaAnalisis", "__init__"),
    ("ReglaAnalisis", "_separar_palabras"),
    ("ReglaAnalisis", "__init__"),
    ("ReglaPalabrasMasUsadas", "__init__"),
    ("ReglaPalabrasMasUsadas", "analizar"),
    ("ReglaConteoPalabras", "__init__"),
    ("ReglaConteoPalabras", "analizar"),
    ("ReglaTiempoLectura", "__init__"),
    ("ReglaTiempoLectura", "analizar"),
    ("Analizador", "__init__"),
    ("Analizador", "procesar"),
])
def test_clase_contiene_metodo(module_members_elements, class_name, method_name):
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} class not defined")

    assert method_name in module_members_elements[class_name].__dict__.keys()


@pytest.mark.parametrize("super_class_name, sub_class_name", [
    ("ABC", "ReglaAnalisis"),
    ("ReglaAnalisis", "ReglaPalabrasMasUsadas"),
    ("ReglaAnalisis", "ReglaConteoPalabras"),
    ("ReglaAnalisis", "ReglaTiempoLectura")
])
def test_clase_hereda(module_members_elements, analizador_module, super_class_name, sub_class_name):
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


@pytest.mark.parametrize("class_name, attribute_name", [
    ("Analizador", "reglas"),
    ("ReglaTiempoLectura", "TASA_LECTURA")
])
def test_clase_contiene_atributo(module_members_elements, class_name, attribute_name):
    if class_name not in module_members_elements.keys():
        pytest.fail(f"{class_name} not defined")

    fields = dir(module_members_elements[class_name]())
    assert attribute_name in fields
