import os

class Message:
    name: str
    locales: dict[str, str]
    def __init__(self, name:str, locales: dict[str, str]):
        self.locales = locales
        self.name = name
    
    def localed(self, locale_id: str):
        return self.locales[locale_id]

    def add(self, code: str, locale: str) -> None:
        self.locales[code] = locale
        


class LocaleManager:
    messages: list[Message] = []
    
    def __init__(self, locale_folder: str):
        if not os.path.exists(locale_folder):
            raise FileNotFoundError(f'locale folder {locale_folder} not found')
        self.locales_folder = locale_folder
    
    def setup(self):
        if self.locales_folder:
            for filename in os.listdir(self.locales_folder):
                if not filename.startswith('locale_') and not filename.endswith('.lc'):
                    continue
                    
                with open(os.path.join(self.locales_folder, filename), 'r', encoding='utf-8') as file:
                    lines = file.read().split('\n')
                    code = filename[filename.rfind('_') + 1: filename.rfind('.')]
                    for entry in lines:
                        if entry == '':
                            continue

                        key, val = entry.split(': ')
                        val = val.replace(':/ ', ': ').replace('\\n', '\n')
                        for i, msg in enumerate(self.messages):
                            if msg.name == key:
                                self.messages[i].add(code, val)
                                break
                        else:
                            self.messages.append(Message(key, {code: val}))
                        

            return self

    def get(self, name: str) -> Message:
        for message in self.messages:
            if message.name == name:
                return message
        raise KeyError
