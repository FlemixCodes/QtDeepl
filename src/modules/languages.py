class Language:
    __language_en = {
        "translating": "Translating...",
        "error": "Error",
        "error_auto": "You cannot set a translatable language in auto!",
        "error_input": "The input field is empty!",
        "error_valid_lang": "is not valid language. Valid language:",
        "error_limit_maybe": "Maybe Time limit exceeded.",
        "error_limit": "Time limit exceeded",
        "button_translate": "Translate",
        "install": "Install",
        "install_browser": "Installing browser executable. This may take some time",
        "install_browser_success": "Browser installed!",
        "button_switch_lang": "Switch lang",
    }

    __language_ru = {
        "translating": "Перевод...",
        "error": "Ошибка",
        "error_auto": "Вы не можете установить язык перевода в автоматическом режиме!",
        "error_input": "Поле ввода пустое!",
        "error_valid_lang": "это недопустимый язык. Допустимый язык:",
        "error_limit_maybe": "Возможно, лимит времени превышен.",
        "error_limit": "Лимит времени превышен.",
        "button_translate": "Перевести",
        "install": "Загрузка",
        "install_browser": "Установка исполняемого файла браузера. Это может занять некоторое время",
        "button_switch_lang": "Сменить язык",
    }

    def __init__(self) -> None:
        self.__languages = {
            'en': self.__language_en,
            'ru': self.__language_ru
        }
        self.__selected_language = None

    def set_language(self, language: str) -> None:
        if language in self.__languages.keys():
            self.__selected_language = language

    def get_string(self, translate_key: str) -> str | None:
        if translate_key in self.__languages[self.__selected_language]:
            return self.__languages[self.__selected_language][translate_key]
        else: 
            return 
        
    def get_select_language(self) -> str | None:
        if self.__selected_language is not None:
            return self.__selected_language
        else:
            return
        
    def get_languages(self) -> tuple:
        return tuple(self.__languages.keys())