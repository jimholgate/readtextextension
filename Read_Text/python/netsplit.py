#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Split strings into lists specifying the maximum string length and using
localized punctuation for use with web based text to speech platforms.

Use
---

import netsplit
_netsplitlocal = netsplit.LocalHandler()
_items = _netsplitlocal.create_play_list(_text, _iso_lang.split("-")[0])"""


import io
import os
import re
import string
import unicodedata


class LocalHandler(object):
    """Use data specific to Read Text Extension"""

    def __init__(self):  # -> None

        self.last_lang = None
        self.patterns = None

    def _split_sentence(self, _text=""):  # -> list
        """
        Fallback method to split _text into a list of sentences.

        Returns:
            list: A list of sentence or phrase strings.
        """
        if _text:
            _text = re.sub(r"([.?!`—;:．！？—–。︁︒…])\s+", r"\1\n", _text)
            return _text.splitlines()
        return []

    def create_play_list(self, _text="", _lang_str="en", _verbose=True):  # -> list
        """
        Splits a long string of sentences or paragraphs into a list
        using local punctuation and line endings.

        Example:
            - `create_play_list("Bye! Sleep Well!", "en", False)`

        Args:
            _text (str): The text to split.
            _lang_str (str): A short ISO language code, e.g., 'en'.
            _verbose (bool): Print the exception if it occurs.

        Returns:
            list
        """
        # <https://raw.githubusercontent.com/nvaccess/nvda/refs/heads/master/source/locale/en/symbols.dic>
        #
        # This project includes files that are a part of the NonVisual
        # Desktop Access (NVDA) project. Copyright (c) 2011-2024 NVDA
        # Contributors. Licensed under the GNU General
        # Public License (GPL). For full licensing terms, see:
        # https://github.com/nvaccess/nvda#readme

        if not _text.strip():
            return []
        _text = _text.strip()
        if not _lang_str:
            _lang_str = "es"
        split_list = None
        try:
            _lang = _lang_str.split("-")[0].split("_")[0].lower()
            if _lang != self.last_lang:
                self.patterns = None
                self.last_lang = _lang

            if not self.patterns:
                # Specify a fallback location for systems that do not have a
                # directory with speech-dispatcher locale resources.
                local_dic = ""
                l10n_dir = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "po", "_l10n"
                )
                if os.path.join(l10n_dir, "en", "symbols.dic"):
                    local_dic = os.path.join(l10n_dir, "en", "symbols.dic")

                for dic_file in (
                    "/usr/share/speech-dispatcher/locale/{0}/symbols.dic".format(_lang),
                    "/usr/share/speech-dispatcher/locale/en/symbols.dic",
                    local_dic,
                ):
                    if os.path.isfile(dic_file):
                        self.patterns = extract_sentence_patterns(dic_file)
                        _sentence_splitter = SentenceSplitter(self.patterns)
                        split_list = split_text_for_tts(
                            _text, dic_file, 250, 85, 4, False
                        )
                        if split_list:
                            return split_list
                if not split_list:
                    return split_text_for_tts(_text, "", 250, 85, 4, False)

            _sentence_splitter = SentenceSplitter(self.patterns)
            return _sentence_splitter.regsplit(_text)
        except Exception as e:
            if _verbose:
                print(
                    "Exception in `create_play_list`: {0}".format(e),
                    "\nFalling back to a simple `split_sentence` method.",
                )
            return self._split_sentence(_text)


class SentenceSplitter(object):
    """
    Splits text into sentences using compiled regex patterns from Speech Dispatcher.
    """

    def __init__(self, patterns):
        """
        Initialize the SentenceSplitter.

        Args:
            patterns (list): List of regex patterns for sentence/phrase endings.
        """
        self.patterns = patterns
        if patterns:
            self.delimiter_regex = re.compile(
                "|".join("({})".format(p) for p in patterns)
            )
        else:
            self.delimiter_regex = None

    def regsplit(self, text):
        """
        Split text into sentences using the compiled regex patterns.

        Args:
            text (str): Input text.

        Returns:
            list: List of sentence strings.
        """
        text = re.sub(r"(?<![.!?])\n+", ". ", text)
        if not self.delimiter_regex:

            def fallback_sentences(_text=""):
                if _text:
                    _text = re.sub(r"([.?!`—;:．！？—–。︁︒…])\s+", r"\1\n", _text)
                    return _text.splitlines()
                return []

            return fallback_sentences(text)

        sentences = []
        start = 0
        for match in self.delimiter_regex.finditer(text):
            end = match.end()
            sentence = text[start:end].strip()
            if sentence:
                sentences.append(sentence)
            start = end
        if start < len(text):
            tail = text[start:].strip()
            if tail:
                sentences.append(tail)
        return sentences


def is_punctuation(ch=""):  # -> bool:
    """Return `True` if the character at the end of the string uses
    punctuation in one of the Unicode punctuation categories.

        Args:
            ch (str): The string to evaluate.

        Returns:
            `True` if the evaluation finds punctuation at the end
            of the string.

    """
    if not ch:
        return False
    ch = str(ch)
    try:
        return unicodedata.category(ch[-1]).startswith("P")
    except (NameError, TypeError):
        if is_ascii_punct(ch[-1]):
            return True
        if ch[-1] in "«»‘’‚‛“”„.?!`—;:．！？—–":
            return True
    return False


def is_ascii_punct(ch=""):  # -> bool
    """Return `True` if the character at the end of the string uses
    ASCII compatible punctuation.

        Args:
            ch (str): The string to evaluate.

        Returns:
            `True` if the evaluation finds ASCII punctuation at the
            end of the string.
    """
    if not ch:
        return False
    ch = str(ch)
    return ch[-1] in string.punctuation


def normalize_edge_punct(s=""):  # -> str:
    """
    Normalize leading and trailing punctuation on a string.

    This function removes any sequence of punctuation characters at both
    ends of the input, then re-inserts at most one ASCII punctuation mark
    at the start (the first encountered) and one at the end (the last
    encountered). If no ending punctuation remains, a period is appended.

    Args:
        s (str): The string to normalize.

    Returns:
        str: The input trimmed of excess edge punctuation, with at most one
             ASCII punctuation character preserved at each end.
    """
    if not s:
        return str(s)
    s = str(s).strip()

    end_punct = ""
    while is_punctuation(s[-1]):
        if is_ascii_punct(s[-1]):
            end_punct = s[-1]
        s = s[:-1]

    start_punct = ""
    while is_punctuation(s[0]):
        if is_ascii_punct(s[0]):
            start_punct = s[0]
        s = s[1:]

    if not end_punct:
        end_punct = "."

    return start_punct + s.strip() + end_punct


def contains_cjk(text):  # -> bool
    """
    Detect if the text contains any CJK (Chinese, Japanese, Korean) characters.

    Args:
        text (str): Input text.

    Returns:
        bool: True if CJK characters are found, False otherwise.
    """
    return re.search("[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", str(text)) is not None


def is_valid_short_fragment(text="", limit=3):  # -> bool
    """
    A valid fragment is one of the following:
      - A number followed by a period (e.g., "1.")
      - A single letter followed by a period (e.g., "A.")
      - A capitalized abbreviation of a few letters followed by a period.
        (e.g., "Dr.", "Mrs.", "St.", "Ave.", "Apt.")

    Args:
        text (str): The text to evaluate.
        limit(int): Maximum letters before a period in capitalized Roman text.

    Returns:
        bool: True if the text is a valid short fragment, False otherwise.

    """
    s = str(text).strip()

    # Fast fail: must end with a period
    if not s.endswith("."):
        return False

    # Number + period
    if s[:-1].isdigit():
        return True

    # Single letter + period
    if len(s) == 2 and s[0].isalpha():
        return True

    # Capitalized abbreviations up to the value of `limit` letters + period
    if (
        3 <= len(s) <= limit + 1
        and s[:-1].isalpha()
        and s[0].isupper()
        and s[1:].islower()
    ):
        return True

    return False


def _analyse_sentence_patterns(patterns, filestream=None, keys=None):
    """
    Parse the 'complexSymbols' section of a Speech Dispatcher symbols.dic file.

    Args:
        patterns (list): List to append regex patterns to.
        filestream (iterable or None): Open file or list of lines. If None, uses a built-in fallback.
        keys (list or None): Keys to match in the second column (e.g., ["sentence ending", "phrase ending"]).

    Returns:
        list or None: Returns patterns list if using fallback, otherwise None.
    """
    in_block = False
    if not keys:
        keys = ["sentence ending", "phrase ending"]

    if not filestream:
        filestream = [
            r"complexSymbols:",
            r"# identifier\tregexp",
            r"# Sentence endings.",
            r". sentence ending\t(?<=[^\s.])\.(?=[\"'”’)\s]|$)",
            r"! sentence ending\t(?<=[^\s!])\!(?=[\"'”’)\s]|$)",
            r"? sentence ending\t(?<=[^\s?])\?(?=[\"'”’)\s]|$)",
            r"# Phrase endings.",
            r"; phrase ending\t(?<=[^\s;]);(?=\s|$)",
            r": phrase ending\t(?<=[^\s:]):(?=\s|$)",
            r"symbols:",
            r"",
        ]

    for line in filestream:
        line = line.rstrip("\n")
        if line.strip() == "complexSymbols:":
            in_block = True
            continue
        if line.strip() == "symbols:":
            in_block = False
            return patterns
        if in_block:
            if not line.strip():
                return patterns
            if line.lstrip().startswith("#"):
                continue
            parts = re.split(r"\t+", line.strip())
            if len(parts) != 2:
                continue
            if len(parts) == 2 and any(check == parts[1] for check in keys):
                patterns.append(parts[-1])
    return None


def extract_sentence_patterns(file_path="", keys=None):
    """
    Extract regex patterns for sentence and phrase endings from a symbols.dic file.

    Args:
        file_path (str): Path to the symbols.dic file.
        keys (list or None): Keys to match (default: ["sentence ending", "phrase ending"]).

    Returns:
        list: List of regex pattern strings.
    """
    if keys is None:
        keys = ["sentence ending", "phrase ending"]

    patterns = []
    if not os.path.exists(file_path):
        _analyse_sentence_patterns(patterns, None, keys)
        return patterns

    with io.open(file_path, mode="r", encoding="utf-8") as f:
        _analyse_sentence_patterns(patterns, f, keys)
    return patterns


def enforce_length_per_sentence(
    sentences,
    default_max_chars=250,
    cjk_max_chars=85,
    max_bytes=250,
    phrase_delims=None,
    debug=False,
):
    """
    Ensure that no sentence exceeds its maximum character limit and that each
    sentence stays within the specified byte limit when UTF-8 encoded.

    The function first enforces a maximum character count per sentence, using
    different limits for CJK (Chinese, Japanese, Korean) scripts and Roman
    characters. It then ensures that each sentence also fits within the
    specified byte limit. Sentences that exceed these limits are split at
    phrase delimiters, spaces, or, as a last resort, at the hard character limit.

    Args:
        sentences (list of str): A list of sentences to process.
        default_max_chars (int, optional): Safe number of Roman characters
            allowed per sentence. Defaults to 250.
        cjk_max_chars (int, optional): Estimated safe number of CJK (Asian)
            characters allowed per sentence. Defaults to 85.
        max_bytes (int, optional): Hard limit of bytes per sentence when
            UTF-8 encoded. Defaults to 250.
        phrase_delims (set of str, optional): Additional delimiters to break on
            when splitting sentences. Defaults to {",", "(", "…"}.
        debug (bool, optional): If True, prints the function's activity in
            real time. Defaults to False.

    Returns:
        list of str: A list of sentences or sentence fragments that meet the
        character and byte constraints.
    """
    if phrase_delims is None:
        phrase_delims = {",", "(", "…"}  # U+2026 is Unicode ellipsis

    def within_byte_limit(s):
        """Check if string fits within max_bytes when UTF-8 encoded."""
        return len(s.encode("utf-8")) <= max_bytes

    result = []
    for sentence in sentences:
        # Pick char limit based on script
        max_chars = cjk_max_chars if contains_cjk(sentence) else default_max_chars

        # First enforce character limit
        while len(sentence) > max_chars:
            split_point = -1
            split_reason = "fallback"

            for delim in phrase_delims:
                idx = sentence.rfind(delim, 0, max_chars)
                if idx > split_point:
                    split_point = idx + len(delim)
                    split_reason = "phrase delimiter '{}'".format(delim)

            if split_point == -1:
                idx = sentence.rfind(" ", 0, max_chars)
                if idx != -1:
                    split_point = idx
                    split_reason = "space fallback"

            if split_point == -1:
                split_point = max_chars
                split_reason = "hard length cut"

            if debug:
                print(
                    "[DEBUG] Splitting at {0} due to {1}".format(
                        split_point, split_reason
                    )
                )

            result.append(sentence[:split_point].strip())
            sentence = sentence[split_point:].lstrip()

        # Then enforce byte limit
        while not within_byte_limit(sentence):
            # Find largest substring that fits
            for i in range(len(sentence), 0, -1):
                if within_byte_limit(sentence[:i]):
                    if debug:
                        print("[DEBUG] Byte-limit split at {0} bytes".format(i))
                    result.append(sentence[:i].strip())
                    sentence = sentence[i:].lstrip()
                    break

        if sentence:
            result.append(sentence)

    return result


def merge_short_chunks(chunks, min_len=3, debug=False):
    """Merge chunks shorter than min_len unless they are valid short fragments."""
    merged = []
    buffer = ""
    for chunk in chunks:
        stripped = chunk.strip()
        if len(stripped) < min_len and not is_valid_short_fragment(stripped, 3):
            if debug:
                print("[DEBUG] Merging short chunk '{}' into next".format(stripped))
            if buffer:
                buffer += " " + stripped
            else:
                buffer = stripped
        else:
            if buffer:
                merged.append((buffer + " " + stripped).strip())
                buffer = ""
            else:
                merged.append(chunk)
            if debug and len(stripped) < min_len:
                print(
                    "[DEBUG] Keeping short chunk '{}' as valid fragment".format(
                        stripped
                    )
                )
    if buffer:
        merged.append(buffer)
    return merged


def split_text_for_tts(
    text,
    symbols_file_path="",
    default_max_chars=250,
    cjk_max_chars=85,
    min_chunk_len=4,
    debug=False,
):
    """
    Full pipeline: load patterns, split into sentences, enforce per-sentence length limits.

    Args:
        text (str): Input text to split.
        symbols_file_path (str): Path to Speech Dispatcher symbols.dic file.
        default_max_chars (int): Max chars for non-CJK sentences.
        cjk_max_chars (int): Max chars for CJK sentences.

    Returns:
        list: List of TTS-friendly text chunks.
    """
    patterns = extract_sentence_patterns(symbols_file_path)
    splitter = SentenceSplitter(patterns)
    sentences = splitter.regsplit(text)
    chunks = enforce_length_per_sentence(
        sentences, default_max_chars, cjk_max_chars, debug=debug
    )
    chunks = merge_short_chunks(chunks, min_chunk_len, debug=debug)
    return chunks
