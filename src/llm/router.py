from langchain.chat_models import init_chat_model
from config.settings import settings

_models = {}

def get_llm(role: str):
    if role not in _models:
        cfg = settings.data["llm"][role]
        _models[role] = init_chat_model(
            model=cfg["model_name"],
            model_provider=cfg["provider"],
            temperature=cfg["temperature"]
        )
    return _models[role]
