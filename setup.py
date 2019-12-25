from cx_Freeze import setup, Executable

include = ["classe.py","constantes.py","images/laser.png","images/explosion.png","images/missile.png","images/monstre.png","images/vaisseau1.png","images/vaisseau2.png","musique/piste1.mp3"]

setup(
    name = "Space Adventures",
    version = "0.1",
    description = "",
    options = {"build_exe": {"packages":["pygame"],
                             "include_files": include}},
    executables = [Executable("SpaceAdventures.py")]
    )