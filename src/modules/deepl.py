import asyncio
from typing import Any
import textwrap

from install_playwright import install
from playwright._impl._api_types import Error as PlaywrightError
from playwright.async_api import async_playwright
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

    async def __async_generator_split(self, string: str) -> str | None:
        buffer = textwrap.wrap(string, width=self.max_lenght, break_long_words=False)
        for line in buffer:
            yield line

    async def translate(self, string: str) -> str | None:
        return await self.__translate(string)
    
    async def install_browser(self) -> bool:
        async with async_playwright() as p:
            code = await asyncio.get_event_loop().run_in_executor(None, install, p.chromium)
            if code:
                return True
            else:
                return False
                
    async def check_browser_install(self) -> bool:
        async with async_playwright() as p:
            try:
                await self.__get_browser(p)
            except PlaywrightError as e:
                if "Executable doesn't exist at" in e.message:
                    return False
            else:
                return True

    async def __translate(self, string: str) -> Any:
        async with async_playwright() as p:            
            browser = await self.__get_browser(p)

            page = await browser.new_page()
            page.set_default_timeout(self.timeout)

            excluded_resources = ["image", "media", "font", "other"]
            await page.route(
                "**/*",
                lambda route: route.abort() if route.request.resource_type in excluded_resources else route.continue_(),
            )

            async for line in self.__async_generator_split(string=string):
                url = "https://www.deepl.com/en/translator"
                try:
                    await page.goto(f"{url}#{self.fr_lang}/{self.to_lang}/{line}")
                    page.get_by_role("main")
                except PlaywrightError as e:
                    msg = f"Maybe Time limit exceeded. ({self.timeout} ms)"
                    raise DeepLPageError(msg) from e

                try:
                    await page.wait_for_function(
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

                self.translated_fr_lang = str(await input_textbox.get_attribute("lang")).split("-")[0]
                self.translated_to_lang = str(await output_textbox.get_attribute("lang")).split("-")[0]

                res = str((await output_textbox.all_inner_texts())[0])
                res = res.replace("\n\n", "\n")

                self.common_text += f"{res}\n"

            await browser.close()

            return self.common_text
        
    async def __get_browser(self, p: Any) -> Any:
        return await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--single-process",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
            ],
        )