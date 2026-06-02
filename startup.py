import os
import subprocess

pasta = os.path.dirname(os.path.abspath(__file__))
modo_dev = os.path.join(pasta, "MODO_DEV")
atualizar = not os.path.exists(modo_dev)

if atualizar:
    try:
        subprocess.check_output(
            "pyrevit extensions update plugin-revit --debug",
            shell=True,
            creationflags=0x08000000,
        )

    except Exception as e:
        print("ERRO ao iniciar update: {}".format(e))
