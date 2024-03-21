"""A useful library for handling multiple languages. Run to check JSON
translation code. Run with `--help` to see more options."""

import json
import os
import argparse


class Translator:
    """Translate from key English phrases"""

    def __init__(self) -> None:
        self.debug = False
        l10n_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "po", "_l10n"
        )
        self.json_path = os.path.join(l10n_dir, "messages.json")
        self.new_json_path = os.path.expanduser(f"~{os.path.sep}new_messages.json")
        self.messages = {
            "fr": {
                "$[LANGUAGE_ENGLISH]": "French",
                "About": "À propos",
                "Download a compatible voice model": "Télécharger un modèle vocal compatible",
                "Next": "Suivant",
                "No voice model found": "Aucun modèle vocal trouvé",
                "Python error": "Erreur python",
                "Read Text": "Read Text",
                "Stop": "Arrêter",
                "The Piper_TTS client cannot find a compatible voice model for your language.": "Le client Piper_TTS ne trouve pas de modèle vocal compatible.",
                "`gtts` failed to connect.": "`gtts` n'a pas réussi à se connecter.",
                "`qrcode` missing. `pip3 install qrcode[pil]`": "`qrcode` manquant. `pip3 install qrcode[pil]`",
            }
            # Create a separate json template to safely review, print or update
            # JSON code. Use `python l10n.py --save_json_template` in your home
            # directory.
        }

    def load_messages(self, iso_lang: str = "en-US") -> bool:
        """Load messages from a JSON file for the given language"""
        try:
            with open(
                self.json_path,
                "r",
                encoding="utf-8",
            ) as f:
                data = json.load(f)
                sorted_data = {
                    k: dict(sorted(v.items())) for k, v in sorted(data.items())
                }
                self.messages = sorted_data
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            if self.debug:
                print(f"Error loading messages for {iso_lang}")
            return False
        return True

    def json_template(self, _save_template: bool = False) -> bool:
        """Create a template for a new language item for the `messages.json` file"""
        json_string = json.dumps(self.messages, indent=4, ensure_ascii=False)
        print(json_string)
        if _save_template:
            try:
                with open(self.new_json_path, "w", encoding="utf-8") as f:
                    json.dump(self.messages, f, ensure_ascii=False, indent=4)
            except:
                return False
        return True

    def get_translation(self, iso_lang: str = "en", key: str = "") -> str:
        """
        Returns the translation for the given key and language if available,
        otherwise returns the key itself.

        Parameters:
        iso_lang (str): The ISO language code.
        key (str): The key for the message to translate.

        Returns:
        str: The translated message or the key if the translation is not available.
        """
        _code = iso_lang.replace("_", "-")
        _family = _code.split("-")[0]
        # Check if the language and message are available
        for _lang in [_code, _family]:
            if _lang not in self.messages:
                if not self.load_messages(_lang):
                    return key
            if _lang in self.messages and key in self.messages[_lang]:
                return self.messages[_lang][key]
        return key  # Default to the key itself


def main() -> None:
    """Use the Translator class data to print specific text translations, or return the
    key if the translation is not in the dictionary."""
    parser = argparse.ArgumentParser(description="Translate key English phrases.")
    parser.add_argument(
        "--key", type=str, default="", help="The key for the message to translate."
    )
    parser.add_argument(
        "--language", type=str, default="en", help="The ISO language code."
    )
    parser.add_argument(
        "--save_json_template",
        type=bool,
        default=False,
        help="If `True` then save a JSON template in the home directory.",
    )
    args = parser.parse_args()

    _translator = Translator()
    message = _translator.get_translation(args.language, args.key)
    if len(message) == 0:
        _translator.json_template(args.save_json_template)
    else:
        print(message)


if __name__ == "__main__":
    main()
