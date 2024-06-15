from app.api.config.crowdstrike_config import Config, Settings


class StorageRepo:

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        print('Create Storage Repo')

    def get_name(self) -> str:
        # config = Config()
        # return config.get_config().app_name
        return self.settings.storage_connect
