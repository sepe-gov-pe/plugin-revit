# -*- coding: utf-8 -*-
import os
import webbrowser

from pyrevit import forms, script

usuario = os.environ.get("USERNAME")
manual_path = f"C:\\Users\\{usuario}\\DC\\ACCDocs\\SEPE\\BIBLIOTECA\\Project Files\\REVIT\\ARQUITETURA\\01_TEMPLATE\\MANUAL_SEPE_ARQUITETURA.pdf"


def main():
    """Abre o manual PDF automaticamente."""
    try:
        if os.path.exists(manual_path):
            webbrowser.open(manual_path)
            script.exit()

        forms.alert(
            f"Manual não encontrado!\n\n"
            f"Usuário atual: {usuario}\n"
            f"Caminho buscado:\n{manual_path}\n\n"
            "Verifique se o arquivo existe neste local.",
            title="Erro - Manual de modelagem",
        )
    except Exception as e:
        forms.alert(f"Erro ao abrir o manual:\n{str(e)}", title="Erro")


if __name__ == "__main__":
    main()
