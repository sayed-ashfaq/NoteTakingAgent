from langchain.chat_models import init_chat_model
from config.settings import settings
from dotenv import load_dotenv



_models = {}

def get_llm(role: str):
    load_dotenv()
    if role not in _models:
        cfg = settings.data["llm"][role]
        _models[role] = init_chat_model(
            model=cfg["model_name"],
            model_provider=cfg["provider"],
            temperature=cfg["temperature"], 

        )
    return _models[role]


if __name__ == "__main__":
    print(get_llm("simple").invoke("Hey there, testing!!"))