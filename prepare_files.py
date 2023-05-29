import os


if __name__ == "__main__":
    files_names = os.listdir("./analizador/entregas")
    for name in files_names:
        index = name.find("_")
        tmp_name = f"{name[:index].strip()}.py"
        new_name = tmp_name.lower().replace(" ", "_")
        os.renames(f"./analizador/entregas/{name}", f"./analizador/entregas/{new_name}")
