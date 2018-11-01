from pathlib import Path
from dotenv import load_dotenv

def load_settings(env):
    env_path = Path('settings') / '.env.{}'.format(env)
    load_dotenv(dotenv_path=env_path)