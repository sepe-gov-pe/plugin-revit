import subprocess

try:
    result = subprocess.check_output(
        "pyrevit extensions update SEPE-Revit --debug",
        shell=True,
        creationflags=0x08000000,
    )

    result = str(result).lower()

except Exception as e:
    print("ERRO ao iniciar update: {}".format(e))
