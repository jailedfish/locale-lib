import os
from typing import Optional


class Message:
    name: str
    locales: dict[str, str]
    _default_locale: str
    def __init__(self, name:str, locales: dict[str, str], default_locale: Optional[str]):
        self.locales = locales
        self.name = name
        self._default_locale = default_locale if default_locale is not None else ''
    
    def localed(self, locale_id: str):
        try:
            if self._default_locale:
                return self.locales.get(locale_id, self._default_locale.format(message=self.name, locale_id=locale_id))
            return self.locales['locale_id']
        except KeyError:
            raise KeyError(f'could not find {locale_id} version of {self.name}')

    def add(self, code: str, locale: str) -> None:
        self.locales[code] = locale
        


class LocaleManager:
    _messages: list[Message] = []
    _use_if_not_found: str
    locales: list[str] = []
    
    def __init__(self, locale_folder: str, fill_not_found: str | None = None):
        if fill_not_found is None:
            fill_not_found = ''
        if not os.path.exists(locale_folder):
            raise FileNotFoundError(f'locale folder {locale_folder} not found')
        self.locales_folder = locale_folder
        self._use_if_not_found = fill_not_found
    
    def setup(self):
        if self.locales_folder:
            for filename in os.listdir(self.locales_folder):
                if not filename.startswith('locale_') and not filename.endswith('.lc'):
                    continue
                self.locales.append(filename[filename.rfind('_') + 1: filename.rfind('.')])

                with open(os.path.join(self.locales_folder, filename), 'r', encoding='utf-8') as file:
                    lines = file.read().split('\n')
                    code = filename[filename.rfind('_') + 1: filename.rfind('.')]
                    for entry in lines:
                        if entry == '':
                            continue

                        key, val = entry.split(': ')
                        val = val.replace(':/ ', ': ').replace('\\n', '\n')
                        
                        for i, msg in enumerate(self._messages):
                            if msg.name == key:
                                self._messages[i].add(code, val)
                                break
                        else:
                            self._messages.append(Message(key, {code: val}, self._use_if_not_found))
                
            return self

    def get(self, name: str) -> Message:
        for message in self._messages:
            if message.name == name:
                return message

        return Message(name, {}, self._use_if_not_found)
    
    def message_names(self) -> list[str]:
        return [msg.name for msg in self._messages]
    