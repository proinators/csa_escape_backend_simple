from os import getenv
from pathlib import Path
from dotenv import load_dotenv

class Consts:
    ENV_FILE=".env"
    IS_DEBUG=None
    PORT=None
    GROQ_API_KEY=None

    def __init__(self) -> None:
        env_path = Path.cwd().joinpath(f"{self.ENV_FILE}")
        load_dotenv(dotenv_path=env_path)
        self.IS_DEBUG=getenv("IS_DEBUG")
        self.PORT=int(getenv("PORT"))
        self.GROQ_API_KEY=getenv("GROQ_API_KEY")