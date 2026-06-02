import os
import subprocess

from pyrevit.loader.sessionmgr import load_session

pasta = os.path.dirname(os.path.abspath(__file__))
dev_flag = os.path.join(pasta, "DEV")
atualizar = not os.path.exists(dev_flag)

if atualizar:
    print("atualizou")
    try:
        subprocess.check_output(
            "pyrevit extensions update plugin-revit --debug",
            shell=True,
            creationflags=0x08000000,
        )
        load_session()

    except Exception as e:
        print("ERRO ao iniciar update: {}".format(e))
