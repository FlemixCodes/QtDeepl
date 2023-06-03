from typing import Any
import textwrap

from install_playwright import install
from playwright._impl._api_types import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from errors import DeepLError, DeepLPageError


class DeepL:
    fr_langs = {
        "auto",
        "bg",
        "cs",
        "da",
        "de",
        "el",
        "en",
        "es",
        "et",
        "fi",
        "fr",
        "hu",
        "id",
        "it",
        "ja",
        "ko",
        "lt",
        "lv",
        "nl",
        "pl",
        "pt",
        "ro",
        "ru",
        "sk",
        "sl",
        "sv",
        "tr",
        "uk",
        "zh",
    }
    to_langs = fr_langs - {'auto'}

    def __init__(self, fr_lang: str, to_lang: str, timeout: int = 15000) -> None:
        if fr_lang not in self.fr_langs:
            raise DeepLError(f"{repr(fr_lang)} is not valid language. Valid language:\n" + repr(self.fr_langs))
        if to_lang not in self.to_langs:
            raise DeepLError(f"{repr(to_lang)} is not valid language. Valid language:\n" + repr(self.to_langs))
        
        self.fr_lang = fr_lang
        self.to_lang = to_lang
        self.translated_fr_lang: str | None = None
        self.translated_to_lang: str | None = None
        self.max_lenght = 3000
        self.timeout = timeout
        self.common_text = ""   

    def __generator_split(self, string: str) -> str | None:
        buffer = textwrap.wrap(string, width=self.max_lenght, break_long_words=False)
        for line in buffer:
            yield line

    def translate(self, string: str) -> str | None:
        return self.__translate(string)
    
    def install_browser(self) -> bool:
        with sync_playwright() as p:
            code = install(p.chromium)
            if code:
                return True
            else:
                return False
                
    def check_browser_install(self) -> bool:
        with sync_playwright() as p:
            try:
                self.__get_browser(p)
            except PlaywrightError as e:
                if "Executable doesn't exist at" in e.message:
                    return False
            else:
                return True

    def __translate(self, string: str) -> Any:
        with sync_playwright() as p:            
            browser = self.__get_browser(p)

            page = browser.new_page()
            page.set_default_timeout(self.timeout)

            excluded_resources = ["image", "media", "font", "other"]
            page.route(
                "**/*",
                lambda route: route.abort() if route.request.resource_type in excluded_resources else route.continue_(),
            )

            for line in self.__generator_split(string=string):
                url = "https://www.deepl.com/en/translator"
                try:
                    page.goto(f"{url}#{self.fr_lang}/{self.to_lang}/{line}")
                    page.get_by_role("main")
                except PlaywrightError as e:
                    msg = f"Maybe Time limit exceeded. ({self.timeout} ms)"
                    raise DeepLPageError(msg) from e

                try:
                    page.wait_for_function(
                        """
                        () => document.querySelector(
                        'd-textarea[data-testid=translator-target-input]')?.value?.length > 0
                    """,
                    )
                except PlaywrightError as e:
                    msg = f"Time limit exceeded. ({self.timeout} ms)"
                    raise DeepLPageError(msg) from e
                
                input_textbox = page.get_by_role("region", name="Source text").locator("d-textarea")
                output_textbox = page.get_by_role("region", name="Translation results").locator("d-textarea")

                self.translated_fr_lang = str(input_textbox.get_attribute("lang")).split("-")[0]
                self.translated_to_lang = str(output_textbox.get_attribute("lang")).split("-")[0]

                res = str((output_textbox.all_inner_texts())[0])
                res = res.replace("\n\n", "\n")

                self.common_text += f"{res}\n"

            browser.close()

            return self.common_text
        
    def __get_browser(self, p: Any) -> Any:
        return p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--single-process",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
            ],
        )