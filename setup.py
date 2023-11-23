from cx_Freeze import setup, Executable

setup(
    name="WebUntis-Viewer",
    version="1.1",
    description="See the Untis Timetable but better",
    executables=[Executable("Viewer.py")]
)
