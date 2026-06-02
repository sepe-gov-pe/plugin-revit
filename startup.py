import os
import subprocess

atualizar = not os.path.exists("nao_atualizar.flag")

if atualizar:
    print("Atualizar")
    try:
        subprocess.check_output(
            "pyrevit extensions update plugin-revit --debug",
            shell=True,
            creationflags=0x08000000,
        )

    except Exception as e:
        print("ERRO ao iniciar update: {}".format(e))

else:
    print("Não atualizar")
