# setup.py
import sys
from cx_Freeze import setup, Executable

main_script = "src/main.py"

build_exe_options = {
    "includes": [
        "PySide6",
        "src.control.LogicComponentController",
        "src.control.LevelFileController",
        "src.control.LevelController",
        "src.view.MainScene",
        "src.view.LevelScene",
        "src.view.LevelSelectionScene",
        "src.view.SandboxModeScene",
        "src.infrastructure.eventBus",
        "src.constants",
    ],
    "excludes": [],
    # 👇 This copies the whole "levels" folder into the build
    "include_files": [
        ("levels", "levels"),
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # no console window

executables = [
    Executable(
        main_script,
        base=base,
        target_name="LogicGatesGame.exe",
        # icon="assets/icons/app.ico",  # if you have one
    )
]

setup(
    name="LogicGatesGame",
    version="1.0",
    description="Logic Gates Game (PySide6)",
    options={"build_exe": build_exe_options},
    executables=executables,
)
