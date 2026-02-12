class Settings:
    def __init__(self, path="config//config.yaml"):
        import yaml
        with open(path) as f:
            self.data = yaml.safe_load(f)

settings = Settings()


if __name__ == "__main__":
    print(settings.data['llm']['reasoning'])