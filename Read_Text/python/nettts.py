import netcommon
import os
import re
import readtexttools
import sys
import time
import tempfile
try:
    import urllib
    BASICS_OK = True
except ImportError:
    BASICS_OK = False


class CoquiDemoLocalHost(object):
    '''# CoquiAI TTS

    The [TTS engine](https://github.com/coqui-ai/TTS/pkgs/container/tts-cpu)
    provides a local http service to convert text that you select to speech.
    
    The TTS server is powered by python. You can use `pip3`, `pipx`, `git`
    or a docker image to download it. For testing, I used Ubuntu 22.04 LTS
    and installed the TTS library using `pipx`.

    The server only serves one model at a time, but you can specify the
    language by selecting a model that includes the iso language code for
    the language in the model name.

    `tts-server --list_models`

    If you do not specify a model, then the server uses a female `en-US`
    model by default. Some voices require specific hardware capabilities and
    do not play on computers that are not compatible.

    Example server commands:

    * Default `tts-server` 
    * English `tts-server --model_name tts_models/en/vctk/vits`
    * French `tts-server --model_name tts_models/fr/css10/vits`
    * Spanish `tts-server --model_name tts_models/es/css10/vits`
    * Ukrainian `tts-server --model_name tts_models/uk/mai/vits`

    This script is a client of the `tts` webserver. The TTS github site
    includes a page to report problems and feature requests. It serves to
    identify limits, errors, pronunciation problems, and other issues.

    IMPORTANT: If some of the models are unusable, it is *not* this client's
    software issue -- report it to the author of the voice model, not the Read
    Text Extension's github bug tracker. Try the text using the locally hosted
    [web page](http://[::1]:5002/) and try to reproduce the problem using
    the same voice and settings.

    The TTS server supports custom models. Check the server documentation.

    `tts-server --tts_checkpoint /path/to/tts/model.pth `
    `--tts_config /path/to/tts/config.json `
    `--vocoder_checkpoint /path/to/vocoder/model.pth `
    `--vocoder_config /path/to/vocoder/config.json`

    ReadText Client 
    ---------------

    Some voice models require system files that are not explicitly stated
    in the documentation. If a model does not seem to work, run the
    `tts-server` program in a command window and note any error messages.

    This script is a python `TTS` client. You need a few additional system
    packages - `python3-bs4`, `python3-pip` and `espeak-ng`. On supported
    Ubuntu distributions you can use:

        `sudo apt-get install python3-bs4 python3-pip espeak-ng`
    
    Optionally, install `spacy` and the associated `spacy` text parsing
    packages for your language using `pipx`. Using the current long term
    support Ubuntu distribution, this allows the Read Text Extension to
    break long text into manageable chunks.'

        `pipx install spacy`

    To troubleshoot the client, you can see information and error messages
    if you run your office program using a terminal window.

        `/usr/bin/soffice`

    The client will not work unless the server is configured correctly and
    is running. You can check the server by navigating to the local server
    [demo page](http://[::1]:5002/).
    
    Docker
    ------

    If you want to try the demo without permanently installing coqui-ai tts,
    your Linux `var` directory must have at least 5 GB of available storage.

    `docker run --rm -it -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu`

    The official TTS server documentation lists equivalent docker commands
    for specific computer hardware configurations - like the GPU or CPU 
    architecture.

    Pipx
    ----

    * `pipx install tts`
    * `pipx install spacy`

    Your Linux `temp` and `home` directories must have at least 5 GB of
    available storage. Installing via `pip3` or `pipx` might not work on
    systems that use python support libraries that are too old or too new.

    Start server
    ------------

    Enter the following in a terminal.

    `tts-server [options]`

    You may need to wait a few moments for the server application to finish
    loading. Check it by opening the local [TTS Engine](http://[::1]:5002/)
    in your web browser.

    Troubleshooting
    ---------------

    To troubleshoot the server, you should run `tts-server` from
    a command line. If you can use [TTS engine](http://[::1]:5002/),
    then check this TTS client by running `/usr/bin/soffice` in a
    terminal window and checking for python errors. Be patient; the
    first time you run the server with a new model it can take a
    while for the TTS program to download the model data.

    + If the tts server stops responding, try quitting `soffice` and
      the tts-server. Use the `tts --list_models` to list available
      models. In some cases, the server can take a long time
      to respond if it needs to download an up-to-date `tts` model.
      This tts client does not automatically download models when
      you have not locally installed the model.
    * If the server is labelled as a demonstration, it might work
      differently than a finished product. For example, subscribing
      to a cloud service might allow you to use more voices and
      languages.
    * If you select a long text to say aloud, then the Coqui TTS web
      server can time out. Select a shorter text or use `pipx` to install
      the `spacy` text handling tool so that Read Text Extension can
      accurately split long text into manageable chunks.
    * Different models used in your `tts-server` command vary in the
      pronunciation, naturalness, intelligibilty, speed and reliability.
      If you can, try out a different model if one does not work well.
    * Conqui assumes that you have installed `espeak-ng`. Some models
      don't work without it.
    * Some models have specific memory, CPU and GPU requirements.
    * Some models will only work if you are running soffice as a
      native application, not as a snap or flatpak. This is because for
      some TTS models, this client uses the system `bs4` (Beautiful
      Soup) python library to check for languages or voices.
'''

    def __init__(self):  # -> None
        '''A docker image doesn't expose details of the directory structure
        to the tts host's API, so functions in the parent that rely on a
        specific file path do not work.'''
        _common = netcommon.LocalCommons()
        self.end = 0
        self.common = _common
        self.add_pause = _common.add_pause
        self.pause_list = _common.pause_list
        self.base_curl = _common.base_curl
        self.debug = _common.debug
        self.url = 'http://[::1]:5002/'  # locally hosted URL port 5002
        self.help_icon = _common.help_icon
        self.help_heading = "Coqui AI TTS demo server"
        self.first_option = ''
        self.help_url = 'https://github.com/coqui-ai/TTS/pkgs/container/tts-cpu'
        self.help_icon = '/usr/share/icons/HighContrast/scalable/actions/system-run.svg'
        self.mascot = '🐸'  # U+1F438  <https://www.compart.com/en/unicode/block/U+1F300>
        self.data_response = ''
        self.audio_format = 'wav'
        self.input_types = ['TEXT']
        self.accept_voice = [
            '', 'all', 'auto', 'coqui', 'localhost', 'docker', 'tts',
            'local_server'
        ]
        self.ok = False
        self.voice = ''
        self.soup = None
        self.checked_lang = ''
        self.styled_wav = ''
        self.base_models = [
            'tts_models/multilingual/multi-dataset/your_tts',
            'tts_models/bg/cv/vits', 'tts_models/cs/cv/vits',
            'tts_models/da/cv/vits', 'tts_models/et/cv/vits',
            'tts_models/ga/cv/vits', 'tts_models/en/ek1/tacotron2',
            'tts_models/en/ljspeech/tacotron2-DDC',
            'tts_models/en/ljspeech/tacotron2-DDC_ph',
            'tts_models/en/ljspeech/glow-tts',
            'tts_models/en/ljspeech/speedy-speech',
            'tts_models/en/ljspeech/tacotron2-DCA',
            'tts_models/en/ljspeech/vits', 'tts_models/en/ljspeech/vits--neon',
            'tts_models/en/ljspeech/fast_pitch',
            'tts_models/en/ljspeech/overflow',
            'tts_models/en/ljspeech/neural_hmm', 'tts_models/en/vctk/vits',
            'tts_models/en/vctk/fast_pitch', 'tts_models/en/sam/tacotron-DDC',
            'tts_models/en/blizzard2013/capacitron-t2-c50',
            'tts_models/en/blizzard2013/capacitron-t2-c150_v2',
            'tts_models/es/mai/tacotron2-DDC', 'tts_models/es/css10/vits',
            'tts_models/fr/mai/tacotron2-DDC', 'tts_models/fr/css10/vits',
            'tts_models/uk/mai/glow-tts', 'tts_models/uk/mai/vits',
            'tts_models/zh-CN/baker/tacotron2-DDC-GST',
            'tts_models/nl/mai/tacotron2-DDC', 'tts_models/nl/css10/vits',
            'tts_models/de/thorsten/tacotron2-DCA',
            'tts_models/de/thorsten/vits',
            'tts_models/de/thorsten/tacotron2-DDC',
            'tts_models/de/css10/vits-neon',
            'tts_models/ja/kokoro/tacotron2-DDC',
            'tts_models/tr/common-voice/glow-tts',
            'tts_models/it/mai_female/glow-tts',
            'tts_models/it/mai_female/vits', 'tts_models/it/mai_male/glow-tts',
            'tts_models/it/mai_male/vits', 'tts_models/ewe/openbible/vits',
            'tts_models/hau/openbible/vits', 'tts_models/lin/openbible/vits',
            'tts_models/tw_akuapem/openbible/vits',
            'tts_models/tw_asante/openbible/vits',
            'tts_models/yor/openbible/vits', 'tts_models/hu/css10/vits',
            'tts_models/el/cv/vits', 'tts_models/fi/css10/vits',
            'tts_models/hr/cv/vits', 'tts_models/lt/cv/vits',
            'tts_models/lv/cv/vits', 'tts_models/mt/cv/vits',
            'tts_models/pl/mai_female/vits', 'tts_models/pt/cv/vits',
            'tts_models/ro/cv/vits', 'tts_models/sk/cv/vits',
            'tts_models/sl/cv/vits', 'tts_models/sv/cv/vits',
            'tts_models/ca/custom/vits', 'tts_models/fa/custom/glow-tts'
        ]
        self.more_models = [
            'vocoder_models/universal/libri-tts/wavegrad',
            'vocoder_models/universal/libri-tts/fullband-melgan',
            'vocoder_models/en/ljspeech/multiband-melgan',
            'vocoder_models/en/ljspeech/hifigan_v2',
            'vocoder_models/en/ljspeech/univnet',
            'vocoder_models/en/blizzard2013/hifigan_v2',
            'vocoder_models/en/vctk/hifigan_v2',
            'vocoder_models/en/sam/hifigan_v2',
            'vocoder_models/nl/mai/parallel-wavegan',
            'vocoder_models/de/thorsten/wavegrad',
            'vocoder_models/de/thorsten/fullband-melgan',
            'vocoder_models/de/thorsten/hifigan_v1',
            'vocoder_models/ja/kokoro/hifigan_v1',
            'vocoder_models/uk/mai/multiband-melgan',
            'vocoder_models/tr/common-voice/hifigan'
        ]
        self.base_models = self.more_models + self.base_models
        self.coqui_fm = [
            'ED\n', 'p225', 'p227', 'p237', 'p240', 'p243', 'p244', 'p245',
            'p246', 'p247', 'p248', 'p249', 'p250', 'p257', 'p259', 'p260',
            'p261', 'p263', 'p268', 'p270', 'p271', 'p273', 'p274', 'p275',
            'p276', 'p277', 'p278', 'p280', 'p282', 'p283', 'p284', 'p288',
            'p293', 'p294', 'p295', 'p297', 'p300', 'p303', 'p304', 'p305',
            'p306', 'p308', 'p310', 'p311', 'p314', 'p316', 'p323', 'p239',
            'p333', 'p334', 'p335', 'p336', 'p339', 'p341', 'p343', 'p345',
            'p347', 'p360', 'p361', 'p362', 'p363', 'p364', 'p374',
            'female-en-5', 'female-pt-4', 'female-en5\n', 'olena'
        ]
        self.tts_equivalents = [
            ['p374', 'all'],
            ['male-pt-3', 'all'],
            ['p374', 'coqui'],
            ['male-pt-3', 'coqui'],
            ['p305', 'female_child1'],
            ['p374', 'male_child1'],
            ['ED\n', 'female1'],
            ['p336', 'female2'],
            ['p308', 'female3'],
            ['p230', 'male1'],
            ['p252', 'male2'],
            ['p313', 'male3'],
            ['female-en-5', 'female_child1'],
            ['male-pt-3\n', 'male_child1'],
            ['female-pt-3', 'female1'],
            ['female-en-5', 'female2'],
            ['female-en-5\n', 'female3'],
            ['male-pt-3\n', 'male1'],
            ['male-en-2', 'male2'],
            ['male-en-2', 'male3'],
        ]

    def _re_search_first_key(self, _key='title'):  # -> str
        '''Get the first text string that matches a key, or `''`if the key is
        not found '''
        html = self.data_response
        if not _key in html:
            return ''
        try:
            pattern = "<%(_key)s.*?>*?</%(_key)s.*?>" % locals()
            search_result = re.search(pattern, html, re.IGNORECASE)
            search_group = search_result.group()
            return re.sub("<.*?>", "", search_group)
        except (AttributeError, NameError):
            pass
        return ''

    def _check_tts_ids(self):
        '''Return `True` if the `tts` home page has interesting `id` contents,
        otherwise return `False`, so don't continue with `ds4`'''
        _continue = False
        if len(self.data_response) == 0:
            return _continue
        for fast_check in [
                'id="speaker_id"', 'id="language_id"', 'id="style_wav"'
        ]:
            if fast_check in self.data_response:
                _continue = True
                break
        return _continue

    def language_supported(self,
                           _iso_lang='en-US',
                           alt_local_url=''):  # -> bool
        '''Is the language or voice supported in the demonstration?
        + `iso_lang` can be in the form `en-US` or `en`.'''
        if alt_local_url.startswith("http"):
            self.url = alt_local_url
        if self.ok:
            return self.ok
        _lower_lang = _iso_lang.lower()
        _lang = _lower_lang.split('_')[0].split('-')[0]
        _found = False
        for _model in self.base_models:
            if '/' in _model:
                if _lang == _model.split('/')[1]:
                    _found = True
                    break
        if _found:
            try:
                from bs4 import BeautifulSoup
            except (ImportError, ModuleNotFoundError):
                try:
                    _local_pip = readtexttools.find_local_pip('bs4')
                    if len(_local_pip) != 0:
                        sys.path.append(_local_pip)
                        try:
                            from bs4 import BeautifulSoup
                        except:
                            pass
                except:
                    pass
            try:
                response = urllib.request.urlopen(self.url)
                self.data_response = response.read().decode('utf-8')
            except urllib.error.URLError:
                self.data_response = ''
            except TimeoutError:
                self.data_response = ''
            if len(self.data_response) == 0:
                self.ok = False
                return False
            help_heading = self._re_search_first_key('title')  # System display
            if len(help_heading) == 0:
                return False
            else:
                self.help_heading = help_heading
                self.first_option = urllib.parse.quote(
                    self._re_search_first_key('option'))  # url argument
            try:
                if not self._check_tts_ids():
                    self.checked_lang = ''
                    self.ok = True
                    return self.ok
                try:
                    self.soup = BeautifulSoup(self.data_response,
                                              features="lxml")
                except NameError:
                    print('''NameError: This speech synthesis model requires
[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to
parse values from a webpage. Install it using `pipx`, `pip3` or a distribution
system installer application like `apt`.''')
                    self.ok = False
                    return self.ok
                _language_ids = self.soup.find(attrs={'id': 'language_id'})
                _idioms = _language_ids.find_all('option')
                for _query in [_iso_lang, _lower_lang, _lang]:
                    for option in _idioms:
                        _idiom_value = option['value']
                        if _idiom_value.startswith(_query):
                            self.checked_lang = _idiom_value
                            self.ok = True
            except AttributeError:
                # 'NoneType' object has no attribute 'find_all'; so the page
                # is missing this section because the model does not feature
                # the options.
                self.checked_lang = ''
                self.ok = True
            except NameError:
                print('''NameError: This speech synthesis application requires
[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)''')
                self.ok = False
        return self.ok

    def get_bs4_style_wav(self, _content=''):  # -> string
        '''If the model supports it, use `style_wav` (dict or path to wav)
        to help generate speech.'''
        if not self.ok:
            return ''
        if not 'id="style_wav"' in self.data_response:
            return ''
        try:
            return urllib.parse.quote(_content)
        except:
            pass
        return ''

    def get_bs4_speaker(self, _vox='female1', _index=0):  # -> string
        '''Get the matching voice on thes CoquiAI server web page'''
        if not self._check_tts_ids():
            return ''
        if _vox == self.first_option:
            self.ok = True
            self.voice = _vox
            return self.voice
        _vox_number = int(''.join(
            ['0', readtexttools.safechars(_vox, '1234567890')]))
        _my_favs_count = 3  # male1, male2, male3
        _matches = []
        if _index == 0 and _vox_number > _my_favs_count:
            # You specify an out of range voice using `male4`, `female5` etc.
            # The voices chosen this way are not classified by gender.
            _index = _vox_number
        _matches = [_vox, 'p374', 'female-pt-3']
        for _item in self.tts_equivalents:
            if _vox.lower() == _item[1]:
                _matches.append(_item[0])
        print('\n' + self.help_heading)
        print('=' * (len(self.help_heading)))
        if not self.ok:
            return ''
        elif len(self.data_response) == 0:
            return ''
        try:
            speaker_ids = self.soup.find(attrs={'id': 'speaker_id'})
            speakers = speaker_ids.find_all('option')
        except AttributeError:
            return ''
        _default_voice = ''
        _index_voice = ''
        try:
            _default_voice = urllib.parse.quote(speakers[0]['value'])
        except (IndexError, ValueError):
            return ''
        try:
            len_speakers = len(speakers)
            if len_speakers != 0:
                _index = _index % len_speakers
                if 'female' in _vox:
                    # Use reverse index
                    _index = len_speakers - _index
                _index_voice = urllib.parse.quote(speakers[_index]['value'])
        except (IndexError, ValueError):
            _index_voice = _default_voice
        if len(_default_voice) == 0:
            return ''
        _print_values = ['']
        for option in speakers:
            _speaker_value = option['value']
            if _speaker_value == _index_voice:
                if _index > _my_favs_count:
                    self.voice = urllib.parse.quote(_index_voice)
                    self.mascot = u'\u263A '
                    print(''.join([
                        '\n* ', self.voice, ' ', self.mascot, ' (', _vox,
                        ')\n\n[', self.help_heading, '](', self.url, ')\n'
                    ]))
                    return self.voice
            self.accept_voice.append(_speaker_value)
            _print_values.append(_speaker_value.strip('\n'))
            if bool(_matches):
                for _match in _matches:
                    if _speaker_value == _match:
                        self.voice = urllib.parse.quote(_match)
                        if bool(self.debug):
                            printed_list = '\n* '.join(_print_values) + '\n'
                            print(
                                printed_list.replace(
                                    _match, self.voice + ' ' + self.mascot +
                                    ' (' + _vox + ')'))
                        else:
                            print(''.join([
                                '\n* ', self.voice, ' ', self.mascot, ' (',
                                _vox, ')\n\n[', self.help_heading, '](',
                                self.url, ')\n'
                            ]))
                        return self.voice
        if len(_index_voice) == 0:
            self.voice = _default_voice
        else:
            self.voice = _index_voice
        return self.voice

    def read(self,
             _text="",
             _iso_lang='en-US',
             _visible="false",
             _audible="true",
             _out_path="",
             _icon="",
             _info="",
             _post_process=None,
             _writer='',
             _size='600x600',
             _speech_rate=160,
             _vox='female1',
             _ok_wait=4,
             _end_wait=30,
             _style_wav=''):  # -> bool
        '''Read text using the Coqui-demo local server.'''
        if not self.ok:
            return False
        _media_out = ''
        _done = False
        # Determine the output file name
        _media_out = readtexttools.get_work_file_path(_out_path, _icon, 'OUT')
        # Determine the temporary file name
        _end = '-demo.wav'
        if netcommon.have_gpu('nvidia'):
            # NVIDIA GPU support
            _end = '-cuda.wav'
        _media_work = os.path.join(tempfile.gettempdir(),
                                   self.help_heading.replace(' ', '-') + _end)
        if len(_out_path) == 0 and bool(_post_process):
            if readtexttools.handle_sound_playing(_media_work):
                readtexttools.unlock_my_lock('tts')
                return True
            elif os.path.isfile(readtexttools.get_my_lock('tts')):
                readtexttools.unlock_my_lock('tts')
                return True
        if bool(self.add_pause):
            for _symbol in self.pause_list:
                if _symbol in _text:
                    _text = _text.translate(self.add_pause).replace('.;', '.')
                    break

        _view_json = self.debug and 1
        response = readtexttools.local_pronunciation(_iso_lang, _text, 'coqui',
                                                     'COQUI_USER_DIRECTORY',
                                                     _view_json)
        _text = response[0]
        if _view_json:
            print(response[1])
        _url1 = self.url
        _url = '%(_url1)s/api/tts' % locals()
        _speaker_id = self.get_bs4_speaker(_vox)
        retval = False
        if BASICS_OK:
            _text = _text.strip('\n;')
            _language_id = self.checked_lang
            _style_wav = self.get_bs4_style_wav(_style_wav)
            _logo = ' ' + self.mascot + ' '
            # Coqui TTS is not currently available as a built in
            # in system package, so the behaviour and requirements
            # doe not change consistently across platforms.
            play_list = self.common.big_play_list(_text,
                                                  _iso_lang.split('-')[0])
            last_item = ''
            _tries = 0
            readtexttools.lock_my_lock('tts')
            _no = 10 * '0'
            for _item in play_list:
                if not os.path.isfile(readtexttools.get_my_lock('tts')):
                    print('[>] Stop!')
                    return True
                _item = _item.strip(' \n;')
                _ilen = len(_item)
                if _ilen == 0:
                    continue
                elif _ilen < 3:
                    # Using the default Coqui Web page, enter just "No"
                    # into the text entry field and click "Speak". Wait
                    # and wait until the web server times out. Good luck!
                    # Let's add some punctuation so it reads a short word
                    # aloud.
                    _item = _item + '!'
                elif _ilen > len(last_item):
                    # Could make unusual noises. Your mileage may vary.
                    #
                    # Let's make sure that the previous utterance is done.
                    time.sleep(2)
                last_item = _item
                _no = readtexttools.prefix_ohs(_tries, 10, '0')
                if '.' in _media_out and _tries != 0:
                    _ext = os.path.splittext(_media_out)[1]
                    _media_out = _media_out.replace(
                        '.%(_ext)s' % locals(), '_%(_no)s.%(_ext)s' % locals())
                _tries += 1
                if os.path.isfile(_media_work):
                    os.remove(_media_work)
                q_text = urllib.parse.quote(_item)
                my_url = '''%(_url)s?text=%(q_text)s&speaker_id=%(_speaker_id)s&style_wav=%(_style_wav)s&language_id=%(_language_id)s''' % locals(
                )
                # _method = "GET"
                if self.debug:
                    if len(play_list) != 1:
                        print('\n'.join(['', _no, _item, 10 * '-']))
                if len(_item) > 200:
                    _end_wait = int(_end_wait * len(_item) / 500)
                    _logo = ' ⌛ '  # U+231B <https://www.compart.com/en/unicode/U+231B>
                if not retval:
                    if "TTS engine" in self.data_response:
                        readtexttools.pop_message(
                            ''.join([self.help_heading, _logo, self.voice]),
                            self.url, 0, self.help_icon, 0)
                self.common.set_urllib_timeout(_end_wait)
                try:
                    # The API uses GET and a `text` argument for text
                    req = urllib.request.Request(my_url)
                    resp = urllib.request.urlopen(req)
                    response_content = resp.read()
                    with open(_media_work, 'wb') as f:
                        f.write(response_content)
                    if os.path.isfile(_media_work):
                        _done = os.path.getsize(_media_work) != 0
                except urllib.error.HTTPError:
                    _logo = u' \u26a0\ufe0f '
                    print('%(_logo)s Tried using `%(_iso_lang)s` with Coqui TTS but failed with an HTTP Error.' % locals())
                    readtexttools.unlock_my_lock('tts')
                    done = False
                except TimeoutError:
                    readtexttools.unlock_my_lock('tts')
                    done = False
                if not _done:
                    return False
                if not os.path.isfile(readtexttools.get_my_lock('tts')):
                    print('[>] Stop')
                    return True
                retval = self.common.do_net_sound(_info, _media_work, _icon,
                                                  _media_out, _audible,
                                                  _visible, _writer, _size,
                                                  _post_process, False)
            readtexttools.unlock_my_lock('tts')
            return retval
