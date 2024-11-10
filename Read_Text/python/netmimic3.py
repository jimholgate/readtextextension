#!/usr/bin/env python
# -*- coding: UTF-8-*-
"""Supports the Docker MyCroft AI Mimic TTS package. This
tool uses the same web address as MaryTTS by default, so you can't
run the two localhost servers together using the defaults."""


import os
import sys
import tempfile

try:
    import urllib
    import json

    BASICS_OK = True
except ImportError:
    BASICS_OK = False
import netcommon
import readtexttools


class Mimic3Class(object):
    """MyCroft AI Mimic TTS
====================

"A fast local neural text to speech engine for Mycroft"

Check the release status of the API for Mimic before using it. By default the
application shares the same address and port as MaryTTS so do not run them at
the same time using the same URL and port.

    mkdir -p "${HOME}/.local/share/mycroft/mimic3"
    chmod a+rwx "${HOME}/.local/share/mycroft/mimic3"
    docker run \
        -it \
        -p 59125:59125 \
        --restart=always \
        -v "${HOME}/.local/share/mycroft/mimic3:/home/mimic3/.local/share/mycroft/mimic3" \
        'mycroftai/mimic3'

To automatically start the daemon, set the Docker container restart policy to
"always", otherwise omit the option.

* [Local host](http://0.0.0.0:59125)
* [Mimic3 TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
* [GitHub](https://github.com/MycroftAI/mimic3)"""

    def __init__(self) -> None:
        """Initialize data."""
        _common = netcommon.LocalCommons()
        self.locker = _common.locker
        self.common = _common
        self.debug = _common.debug
        self.default_extension = _common.default_extension
        self.ok = False
        # This is the default. You can set up the server to use a different port.
        self.url = "http://0.0.0.0:59125"  # localhost port 59125
        self.help_icon = _common.help_icon
        self.help_heading = "Mimic 3"
        self.help_url = (
            "https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3"
        )
        self.local_dir = "mimic"
        self.max_chars = 360
        self.voice = ""
        self.voice_id = ""
        self.app_locker = readtexttools.get_my_lock("lock")

        self.accept_voice = [
            "",
            "all",
            "auto",
            "child_female1",
            "child_male1",
            "mimic3",
            "localhost",
            "docker",
            "local_server",
        ]
        self.checked_spacy = False
        self.default_lang = _common.default_lang
        self.default_voice = "en_UK/apope_low"
        self.default_extension = _common.default_extension
        self.full_names = []
        # Lists of genders are not authoritative. It might have
        # omitted or incorrect items. For omitted genders, the
        # routine falls back to including the name in both
        # <gender>_names lists. For a current list of voices,
        # see: https://mycroftai.github.io/mimic3-voices/#af_ZA
        self.male_names = []
        self.female_names = []
        self.male_list = [
            "bn/multi_low#03042",
            "bn/multi_low#00737",
            "bn/multi_low#01232",
            "bn/multi_low#02194",
            "bn/multi_low#3108",
            "bn/multi_low#3713",
            "bn/multi_low#1010",
            "bn/multi_low#00779",
            "bn/multi_low#9169",
            "bn/multi_low#4046",
            "bn/multi_low#5958",
            "bn/multi_low#01701",
            "bn/multi_low#0834",
            "bn/multi_low#3958",
            "de_DE/m-ailabs_low#karlsson",
            "de_DE/thorsten-emotion_low#amused",
            "de_DE/thorsten-emotion_low#angry",
            "de_DE/thorsten-emotion_low#disgusted",
            "de_DE/thorsten-emotion_low#drunk",
            "de_DE/thorsten-emotion_low#neutral",
            "de_DE/thorsten-emotion_low#sleepy",
            "de_DE/thorsten-emotion_low#surprised",
            "de_DE/thorsten-emotion_low#whisper",
            "de_DE/thorsten_low",
            "en_UK/apope_low",
            "en_US/cmu-arctic_low#awb",
            "en_US/cmu-arctic_low#rms",
            "en_US/cmu-arctic_low#ksp",
            "en_US/cmu-arctic_low#aew",
            "en_US/cmu-arctic_low#bdl",
            "en_US/cmu-arctic_low#jmk",
            "en_US/cmu-arctic_low#fem",
            "en_US/cmu-arctic_low#fem",
            "en_US/cmu-arctic_low#ahw",
            "en_US/cmu-arctic_low#aup",
            "en_US/cmu-arctic_low#gka",
            "en_US/hifi-tts_low#9017",
            "en_US/hifi-tts_low#6097",
            "en_US/m-ailabs_low#elliot_miller",
            "en_US/vctk_low#p259",
            "en_US/vctk_low#p247",
            "en_US/vctk_low#p263",
            "en_US/vctk_low#p274",
            "en_US/vctk_low#p286",
            "en_US/vctk_low#p270",
            "en_US/vctk_low#p281",
            "en_US/vctk_low#p271",
            "en_US/vctk_low#p284",
            "en_US/vctk_low#p287",
            "en_US/vctk_low#p360",
            "en_US/vctk_low#p374",
            "en_US/vctk_low#p376",
            "en_US/vctk_low#p304",
            "en_US/vctk_low#p347",
            "en_US/vctk_low#p311",
            "en_US/vctk_low#p334",
            "en_US/vctk_low#p316",
            "en_US/vctk_low#p363",
            "en_US/vctk_low#p275",
            "en_US/vctk_low#p258",
            "en_US/vctk_low#p232",
            "en_US/vctk_low#p292",
            "en_US/vctk_low#p272",
            "en_US/vctk_low#p278",
            "en_US/vctk_low#p298",
            "en_US/vctk_low#p279",
            "en_US/vctk_low#p285",
            "en_US/vctk_low#p326",
            "en_US/vctk_low#p254",
            "en_US/vctk_low#p252",
            "en_US/vctk_low#p345",
            "en_US/vctk_low#p243",
            "en_US/vctk_low#p227",
            "en_US/vctk_low#p251",
            "en_US/vctk_low#p246",
            "en_US/vctk_low#p226",
            "en_US/vctk_low#p260",
            "en_US/vctk_low#p245",
            "en_US/vctk_low#p241",
            "en_US/vctk_low#p237",
            "en_US/vctk_low#p256",
            "en_US/vctk_low#p302",
            "en_US/vctk_low#p364",
            "es_ES/carlfm_low",
            "es_ES/m-ailabs_low#tux",
            "es_ES/m-ailabs_low#victor_villarraza",
            "fi_FI/harri-tapani-ylilammi_low",
            "fr_FR/m-ailabs_low#ezwa",
            "fr_FR/m-ailabs_low#bernard",
            "fr_FR/m-ailabs_low#zeckou",
            "fr_FR/m-ailabs_low#gilles_g_le_blanc",
            "fr_FR/tom_low",
            "gu_IN/cmu-indic_low#cmu_indic_guj_ad",
            "ha_NE/openbible_low",
            "it_IT/mls_low#1595",
            "it_IT/mls_low#4998",
            "it_IT/mls_low#1989",
            "it_IT/mls_low#2033",
            "it_IT/mls_low#2019",
            "it_IT/mls_low#9772",
            "it_IT/mls_low#1725",
            "it_IT/mls_low#10446",
            "it_IT/mls_low#12428",
            "it_IT/mls_low#8181",
            "it_IT/mls_low#12804",
            "it_IT/mls_low#4705",
            "it_IT/mls_low#644",
            "it_IT/mls_low#1157",
            "it_IT/mls_low#6744",
            "it_IT/mls_low#7405",
            "it_IT/mls_low#5010",
            "it_IT/riccardo-fasol_low",
            "jv_ID/google-gmu_low#07875",
            "jv_ID/google-gmu_low#05522",
            "jv_ID/google-gmu_low#03424",
            "jv_ID/google-gmu_low#03314",
            "jv_ID/google-gmu_low#05219",
            "jv_ID/google-gmu_low#00027",
            "jv_ID/google-gmu_low#09724",
            "jv_ID/google-gmu_low#04588",
            "jv_ID/google-gmu_low#04285",
            "jv_ID/google-gmu_low#05970",
            "jv_ID/google-gmu_low#06080",
            "jv_ID/google-gmu_low#07765",
            "jv_ID/google-gmu_low#02326",
            "jv_ID/google-gmu_low#03727",
            "jv_ID/google-gmu_low#04175",
            "jv_ID/google-gmu_low#06383",
            "jv_ID/google-gmu_low#08178",
            "jv_ID/google-gmu_low#05667",
            "jv_ID/google-gmu_low#01519",
            "jv_ID/google-gmu_low#01932",
            "nl/bart-de-leeuw_low",
            "nl/flemishguy_low",
            "nl/pmk_low",
            "nl/rdh_low",
            "pl_PL/piotr_nater",
            "ru_RU/multi_low#minaev",
            "ru_RU/multi_low#nikolaev",
            "sw/lanfrica_low",
            "te_IN/cmu-indic_low#sk",
            "uk_UK/m-ailabs_low#obruchov",
            "uk_UK/m-ailabs_low#shepel",
            "uk_UK/m-ailabs_low#loboda",
            "uk_UK/m-ailabs_low#miskun",
            "uk_UK/m-ailabs_low#pysariev",
            "yo/openbible_low",
        ]
        self.female_list = [
            "af_ZA/google-nwu_low#7214",
            "af_ZA/google-nwu_low#8963",
            "af_ZA/google-nwu_low#7130",
            "af_ZA/google-nwu_low#8924",
            "af_ZA/google-nwu_low#8148",
            "af_ZA/google-nwu_low#1919",
            "af_ZA/google-nwu_low#2418",
            "af_ZA/google-nwu_low#6590",
            "af_ZA/google-nwu_low#0184",
            "bn/multi_low#rm",
            "bn/multi_low#4811",
            "de_DE/m-ailabs_low#ramona_deininger",
            "de_DE/m-ailabs_low#rebecca_braunert_plunkett",
            "de_DE/m-ailabs_low#eva_k",
            "de_DE/m-ailabs_low#angela_merkel",
            "el_GR/rapunzelina_low",
            "en_US/cmu-arctic_low#slt",
            "en_US/cmu-arctic_low#clb",
            "en_US/cmu-arctic_low#lnh",
            "en_US/cmu-arctic_low##rxr",
            "en_US/cmu-arctic_low#ljm",
            "en_US/cmu-arctic_low#slp",
            "en_US/cmu-arctic_low#axb",
            "en_US/cmu-arctic_low#eey",
            "en_US/hifi-tts_low#92",
            "en_US/ljspeech_low",
            "en_US/m-ailabs_low#judy_bieber",
            "en_US/m-ailabs_low#mary_ann",
            "en_US/vctk_low#p239",
            "en_US/vctk_low#p236",
            "en_US/vctk_low#p264",
            "en_US/vctk_low#p250",
            "en_US/vctk_low#p261",
            "en_US/vctk_low#p283",
            "en_US/vctk_low#p276",
            "en_US/vctk_low#p277",
            "en_US/vctk_low#p231",
            "en_US/vctk_low#p238",
            "en_US/vctk_low#p257",
            "en_US/vctk_low#p273",
            "en_US/vctk_low#p329",
            "en_US/vctk_low#p361",
            "en_US/vctk_low#p310",
            "en_US/vctk_low#p340",
            "en_US/vctk_low#p330",
            "en_US/vctk_low#p308",
            "en_US/vctk_low#p314",
            "en_US/vctk_low#p317",
            "en_US/vctk_low#p339",
            "en_US/vctk_low#p294",
            "en_US/vctk_low#p305",
            "en_US/vctk_low#p266",
            "en_US/vctk_low#p335",
            "en_US/vctk_low#p318",
            "en_US/vctk_low#p323",
            "en_US/vctk_low#p351",
            "en_US/vctk_low#p333",
            "en_US/vctk_low#p313",
            "en_US/vctk_low#p244",
            "en_US/vctk_low#p307",
            "en_US/vctk_low#p336",
            "en_US/vctk_low#p312",
            "en_US/vctk_low#p267",
            "en_US/vctk_low#p297",
            "en_US/vctk_low#p295",
            "en_US/vctk_low#p288",
            "en_US/vctk_low#p301",
            "en_US/vctk_low#p280",
            "en_US/vctk_low#p341",
            "en_US/vctk_low#p268",
            "en_US/vctk_low#p299",
            "en_US/vctk_low#p300",
            "en_US/vctk_low#s5",
            "en_US/vctk_low#p230",
            "en_US/vctk_low#p269",
            "en_US/vctk_low#p293",
            "en_US/vctk_low#p262",
            "en_US/vctk_low#p343",
            "en_US/vctk_low#p255",
            "en_US/vctk_low#p229",
            "en_US/vctk_low#p240",
            "en_US/vctk_low#p248",
            "en_US/vctk_low#p253",
            "en_US/vctk_low#p233",
            "en_US/vctk_low#p228",
            "en_US/vctk_low#p282",
            "en_US/vctk_low#p234",
            "en_US/vctk_low#p303",
            "en_US/vctk_low#p265",
            "en_US/vctk_low#p306",
            "en_US/vctk_low#p249",
            "en_US/vctk_low#p225",
            "en_US/vctk_low#p362",
            "es_ES/m-ailabs_low#karen_savage",
            "fa/haaniye_low",
            "fr_FR/m-ailabs_low#nadine_eckert_boulet",
            "fr_FR/siwis_low",
            "gu_IN/cmu-indic_low#cmu_indic_guj_dp",
            "gu_IN/cmu-indic_low#cmu_indic_guj_kt",
            "hu_HU/diana-majlinger_low",
            "it_IT/mls_low#4974",
            "it_IT/mls_low#6807",
            "it_IT/mls_low#659",
            "it_IT/mls_low#4649",
            "it_IT/mls_low#6348",
            "it_IT/mls_low#6001",
            "it_IT/mls_low#9185",
            "it_IT/mls_low#8842",
            "it_IT/mls_low#8828",
            "it_IT/mls_low#7440",
            "it_IT/mls_low#8207",
            "it_IT/mls_low#277",
            "it_IT/mls_low#5421",
            "it_IT/mls_low#7936",
            "it_IT/mls_low#844",
            "it_IT/mls_low#6299",
            "it_IT/mls_low#8384",
            "it_IT/mls_low#7444",
            "it_IT/mls_low#643",
            "it_IT/mls_low#4971",
            "it_IT/mls_low#4975",
            "it_IT/mls_low#8461",
            "jv_ID/google-gmu_low#06510",
            "jv_ID/google-gmu_low#03187",
            "jv_ID/google-gmu_low#07638",
            "jv_ID/google-gmu_low#06207",
            "jv_ID/google-gmu_low#08736",
            "jv_ID/google-gmu_low#04679",
            "jv_ID/google-gmu_low#01392",
            "jv_ID/google-gmu_low#05540",
            "jv_ID/google-gmu_low#00264",
            "jv_ID/google-gmu_low#09039",
            "jv_ID/google-gmu_low#08305",
            "jv_ID/google-gmu_low#04982",
            "jv_ID/google-gmu_low#08002",
            "jv_ID/google-gmu_low#02884",
            "jv_ID/google-gmu_low#06941",
            "jv_ID/google-gmu_low#00658",
            "jv_ID/google-gmu_low#04715",
            "jv_ID/google-gmu_low#07335",
            "jv_ID/google-gmu_low#02059",
            "ko_KO/kss_low",
            "ne_NP/ne-google_low#0546",
            "ne_NP/ne-google_low#3614",
            "ne_NP/ne-google_low#2099",
            "ne_NP/ne-google_low#3960",
            "ne_NP/ne-google_low#6834",
            "ne_NP/ne-google_low#7957",
            "ne_NP/ne-google_low#6329",
            "ne_NP/ne-google_low#9407",
            "ne_NP/ne-google_low#6587",
            "ne_NP/ne-google_low#0258",
            "ne_NP/ne-google_low#2139",
            "ne_NP/ne-google_low#5687",
            "ne_NP/ne-google_low#0283",
            "ne_NP/ne-google_low#3997",
            "ne_NP/ne-google_low#3154",
            "ne_NP/ne-google_low#0883",
            "ne_NP/ne-google_low#2027",
            "ne_NP/ne-google_low#0649",
            "nl/nathalie_low",
            "pl_PL/nina_brown",
            "ru_RU/multi_low#hajdurova",
            "te_IN/cmu-indic_low#ss",
            "te_IN/cmu-indic_low#kpn",
            "tn_ZA/google-nwu_low#1932",
            "tn_ZA/google-nwu_low#0045",
            "tn_ZA/google-nwu_low#3342",
            "tn_ZA/google-nwu_low#4850",
            "tn_ZA/google-nwu_low#6206",
            "tn_ZA/google-nwu_low#3629",
            "tn_ZA/google-nwu_low#9061",
            "tn_ZA/google-nwu_low#6116",
            "tn_ZA/google-nwu_low#7674",
            "tn_ZA/google-nwu_low#0378",
            "tn_ZA/google-nwu_low#5628",
            "tn_ZA/google-nwu_low#8333",
            "tn_ZA/google-nwu_low#8512",
            "tn_ZA/google-nwu_low#0441",
            "tn_ZA/google-nwu_low#6459",
            "tn_ZA/google-nwu_low#4506",
            "tn_ZA/google-nwu_low#7866",
            "tn_ZA/google-nwu_low#8532",
            "tn_ZA/google-nwu_low#2839",
            "tn_ZA/google-nwu_low#7896",
            "tn_ZA/google-nwu_low#1498",
            "tn_ZA/google-nwu_low#1483",
            "tn_ZA/google-nwu_low#8914",
            "tn_ZA/google-nwu_low#6234",
            "tn_ZA/google-nwu_low#9365",
            "uk_UK/m-ailabs_low#sumska",
            "vi_VN/vais1000_low",
        ]
        self.data = {}
        self.is_x86_64 = _common.is_x86_64
        self.pause_list = _common.pause_list
        self.add_pause = _common.add_pause
        self.voice_name = ""

    def spd_voice_to_mimic3_voice(
        self, _search="female1", _iso_lang="en-US", _alt_local_url=""
    ) -> str:
        """Assign a name like `en_UK/apope_low"` to a
        spd_voice like `male0`"""
        _search = _search.strip("'\" \n")
        if len(self.full_names) == 0:
            if not self.language_supported(_iso_lang, _alt_local_url, _search):
                self.voice_id = ""
                return self.voice_id
        _vox_number = int(
            "".join(["0", readtexttools.safechars(_search, "1234567890")])
        )
        _voice_count = 1
        if _search in self.full_names:
            self.voice_id = _search
        elif _search.lower().startswith("female"):
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.female_names
            )
            _voice_count = len(self.female_names) + 1
        elif _search.lower().startswith("male"):
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.male_names
            )
            _voice_count = len(self.male_names) + 1
        else:
            self.voice_id = netcommon.index_number_to_list_item(
                _vox_number, self.full_names
            )
            _voice_count = len(self.full_names) + 1
        _url = self.url
        voice_id = self.voice_id
        _help_url = self.help_url
        s_voice_count = str(_voice_count)
        _mimic_lang = voice_id.split("/")[0]
        print(
            f"""
Mimic 3
=======

* Mapped Voice: `{_search}`
* Available Locale: `{_mimic_lang}`
* Mimic3 Voice: `{voice_id}`
* Number of Voices: `{s_voice_count}`
* Mimic3 Server: `{_url}`

[Mimic3]({_help_url})
"""
        )
        return self.voice_id

    def language_supported(
        self, iso_lang="en-US", alt_local_url="", vox="auto"
    ) -> bool:
        """Is the language or voice supported?
        + `iso_lang` can be in the form `en-US` or a voice like
          `de_DE/thorsten_low`
        + `alt_local_url` If you are connecting to a local network's
           speech server using a different computer, you might need to use
           a different url."""
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if sys.version_info < (3, 8):
            self.ok = False
            return self.ok
        if len(self.voice_id) != 0:
            self.help_url = self.url
            self.help_icon = (
                "/usr/share/icons/HighContrast/scalable/actions/system-run.svg"
            )
            return True
        # format of json dictionary item: ''
        # "voice" or "language and region"
        _lang1 = (
            iso_lang.replace("-", "_")
            .replace("en_GB", "en_UK")
            .replace("uk_UA", "uk_UK")
        )
        # concise language
        _lang2 = iso_lang.lower().split("-")[0].split("_")[0]
        try:
            response = urllib.request.urlopen("".join([self.url, "/api/voices"]))
            data_response = response.read()
            self.data = json.loads(data_response)
        except urllib.error.URLError:
            _eurl = self.url
            if self.is_x86_64:
                print(
                    f"""
[Mimic 3](https://github.com/MycroftAI/mimic3)
can synthesize speech privately using <http://0.0.0.0:59125> or
a local URL that you specify.
"""
                )
            self.ok = False
            return False
        except AttributeError:
            self.ok = False
            return False
        if len(self.data) == 0:
            return False
        self.accept_voice.extend(netcommon.spd_voice_list(0, 200, ["female", "male"]))
        for _idiom in [_lang1, _lang2]:
            for _item in self.data:
                testbase = _item["location"]
                if testbase.startswith("http"):
                    # not installed
                    continue
                test_onnx = os.path.expanduser(f"{testbase}{os.sep}generator.onnx".replace("/home/mimic3/", "~/"))
                if os.path.isfile(test_onnx):
                    if os.path.getsize(os.path.realpath(test_onnx)) < 1000:
                        # The file is a placeholder, not a real onnx file. On
                        # <https://huggingface.co/mukowaty/mimic3-voices/>, you can get
                        # the generator.onnx file by clicking the download symbol to the
                        # right of "LFS". An onnx file has a size of several MegaBytes.
                        continue
                if bool(_item["speakers"]):
                    _voice_ids = _item["speakers"]
                    _speaker_prefix = "#"
                else:
                    _voice_ids = [""]
                    _speaker_prefix = ""
                for _speaker in _voice_ids:
                    if _item["language"].startswith(_idiom):
                        full_name = "".join(
                            [
                                _item["language"],
                                "/",
                                _item["name"],
                                _speaker_prefix,
                                _speaker,
                            ]
                        )
                        if full_name not in self.full_names:
                            self.accept_voice.append(full_name)
                            if vox == full_name:
                                self.male_names = [vox]
                                self.female_names = [vox]
                                self.ok = True
                                return self.ok
                            elif _item["language"].startswith(_lang1):
                                self.full_names.insert(0, full_name)
                                if full_name in self.male_list:
                                    self.male_names.insert(0, full_name)
                                elif full_name in self.female_list:
                                    self.female_names.insert(0, full_name)
                                else:
                                    self.male_names.insert(0, full_name)
                                    self.female_names.insert(0, full_name)
                                self.ok = True
                            elif _item["language"].startswith(_lang2):
                                self.full_names.insert(0, full_name)
                                if full_name in self.male_list:
                                    self.male_names.insert(0, full_name)
                                elif full_name in self.female_list:
                                    self.female_names.insert(0, full_name)
                                else:
                                    self.male_names.insert(0, full_name)
                                    self.female_names.insert(0, full_name)
                                self.ok = True
        if len(self.male_names) == 0:
            self.male_names = self.full_names
        if len(self.female_names) == 0:
            self.female_names = self.full_names
        return self.ok

    def try_url_lib(
        self,
        _voice="",
        _text="",
        _url="",
        _length_scale="",
        _ssml="",
        _ok_wait=4,
        _end_wait=10,
        _media_work="",
    ) -> bool:
        """Try getting a sound file using url_lib."""
        _done = False
        if not BASICS_OK:
            return False
        _common = netcommon.LocalCommons()
        _common.set_urllib_timeout(_ok_wait)
        my_url = "".join(
            [
                _url,
                "?voice=",
                urllib.parse.quote(_voice),
                "&lengthScale=",
                str(_length_scale),
                "&ssml=",
                urllib.parse.quote(_ssml),
                "&text=",
                urllib.parse.quote(_text),
            ]
        )
        if _common.debug:
            print(my_url)
        try:
            # GET
            response = urllib.request.urlopen(my_url, timeout=(_end_wait))
            with open(_media_work, "wb") as f:
                f.write(response.read())
            if os.path.isfile(_media_work):
                _done = os.path.getsize(os.path.realpath(_media_work)) != 0
        except (TimeoutError, urllib.error.HTTPError):
            _done = False
        return _done

    def read(
        self,
        _text="",
        _iso_lang="en-US",
        _visible="false",
        _audible="true",
        _out_path="",
        _icon="",
        _info="",
        _post_process=None,
        _writer="",
        _size="600x600",
        _speech_rate=160,
        ssml=False,
        _ok_wait=20,
        _end_wait=60,
    ) -> bool:
        """Read Mimic3 speech aloud"""
        if not self.ok:
            # You unlocked the lock, but the speech did not stop,
            # so exit before saying another item... (docker? flatpak?)
            return True
        _length_scale = 1
        if _speech_rate != 160:
            _length_scale = self.common.rate_to_rhasspy_length_scale(_speech_rate)[0]
        if not self.ok:
            return False
        if len(self.voice_id) == 0:
            self.voice_id = "nanotts:en-US"
            self.voice_name = ""
        _done = False
        _media_out = ""
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, "OUT")
        # Determine the temporary file name
        _media_work = os.path.join(tempfile.gettempdir(), "mimic3.wav")
        if os.path.isfile(_media_work):
            os.remove(_media_work)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock(self.locker)
                return True
            elif os.path.isfile(readtexttools.get_my_lock(self.locker)):
                readtexttools.unlock_my_lock(self.locker)
                return True
        _voice = self.voice_id
        self.checked_spacy = self.common.verify_spacy(_iso_lang.split("-")[0])
        if self.debug and 1:
            print(["`Mimic3Class` > ` `read`", "Request `_voice`: ", _voice])
            if bool(self.add_pause) and not ssml:
                for _symbol in self.pause_list:
                    if _symbol in _text:
                        _text = (
                            _text.translate(self.add_pause)
                            .replace(".\n;", ".")
                            .strip(";")
                        )
                        break
        if ssml:
            _ssml = "true"
        _url = "".join([self.url, "/api/tts"])
        _text = readtexttools.local_pronunciation(
            _iso_lang, _text, self.local_dir, "MIMIC3_USER_DIRECTORY", False
        )[0].strip()

        readtexttools.lock_my_lock(self.locker)
        _tries = 0
        _no = "0" * 10
        if ssml:
            _items = [_text]
        elif self.common.is_ai_developer_platform():
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        elif len(_text.splitlines()) == 1 or len(_text) < self.max_chars:
            _items = [_text]
        elif self.checked_spacy:
            _items = self.common.big_play_list(_text, _iso_lang.split("-")[0])
        else:
            _items = [_text]
        for _item in _items:
            if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                print("[>] Stop!")
                self.ok = False
                return True
            elif len(_item.strip().strip(""" ;:-,*+=_[]()'".!?\n""")) == 0:
                continue
            elif "." in _media_out and _tries != 0:
                _ext = os.path.splitext(_media_out)[1]
                _no = readtexttools.prefix_ohs(_tries, 10, "0")
                _media_out = _media_out.replace(f".{_ext}", f"_{_no}.{_ext}")
            _tries += 1
            _ssml = "false"
            if readtexttools.lax_bool(ssml):
                _ssml = "true"
            _done = self.try_url_lib(
                _voice,
                _item.strip(),
                _url,
                _length_scale,
                _ssml,
                _ok_wait,
                _end_wait,
                _media_work,
            )
            if not os.path.isfile(readtexttools.get_my_lock(self.locker)):
                print("[>] Stop")
                self.ok = False
                return True
            if _done:
                self.common.do_net_sound(
                    _info,
                    _media_work,
                    _icon,
                    _media_out,
                    _audible,
                    _visible,
                    _writer,
                    _size,
                    _post_process,
                    False,
                )
            else:
                break
        self.ok = _done
        if not _done:
            print(self.common.generic_problem)
        readtexttools.unlock_my_lock(self.locker)
        return _done
