rd /S /Q dist\main
pyinstaller -w --clean --win-private-assemblies --version-file=version.txt --icon=imagenes\logo.ico main.py