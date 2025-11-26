# setup.py
import sys
from cx_Freeze import setup, Executable
from src.constants import APP_NAME

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
        ("assets", "assets"),
    ],
}

base = "gui" # Dont open a console window

executables = [
    Executable(
        main_script,
        base=base,
        target_name=APP_NAME,
        icon="assets/sprites/AppLogo.ico"  # if you have one
    )
]

setup(
    name=APP_NAME,
    version="1.0",
    description="A logic gate education tool",
    options={"build_exe": build_exe_options},
    executables=executables,
)
