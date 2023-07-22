#!/usr/bin/env python3
# -*- coding: UTF-8-*-
'''
This text explains how to use a web service and media player to read a text
file. It outlines the terms and conditions associated with using the on-line
service, as well as the potential privacy and security risks. It introduces
text-to-speech tools, Mimic3, Larynx, Rhvoice, MaryTTS and TTS, and how to
use them. It mentions the need to check if the network is available and to
set permissions when using these tools. Lastly, it provides advice on how to
update local libraries and packages when using these tools.

-----

This python tool reads a text file using an web service and a media player.
Online services require a network connection and installation of an online
connection library.

Check the terms and conditions that apply to the on-line service provider.
There may be acceptable use policies, limits or costs.

* Variants like speech rate, pitch, voice and gender might
  not apply to all services or to all languages.
* Online services could be terminated without warning.
* Your content might not be private or secure.
* Your organization or local laws might restrict use of online
  data services. For example, they might restrict services
  provided outside of your country's jurisdiction.
* An online provider could block your access because your use
  is excessive or otherwise violates their terms of service.
* If you run the application in a prsotected container like a flatpak
  or snap, some functions might not work because the application
  does not have permission to execute them.
* On some systems, you might need to install additional software
  libraries like `bs4`, `spacy`, `docker.io` `python3-requests`
  and `ffmpeg` to ensure that libraries are available to download
  and process files.

Docker
------

You can install some text to speech local host tools using docker.io.

If Read Text Extension documentation does not specifically state that it
supports a docker image, check if the docker image has a `maryTTS`
compatibility mode. The compatibility mode allows the speech synthesis
image to use the maryTTS address and port and the maryTTS Application
Program Interface (API) to list installed voices and to produce spoken
audio files over a local web service.
 
See also:
[Docker docs](https://docs.docker.com/desktop/install/linux-install/)
  
Mimic 3
-------

"A fast local neural text to speech engine for Mycroft"

Mycroft Mimic3 is a fast text to speech tool that includes very high quality
voice assets. As of May 2023, it is still in the development stage. The
author of Rhasspy Larynx is a major contributor to the project, so anyone
familiar with Larynx will find it easy to add voice models and manage the
service using the Mimic 3 locally hosted web page.

Mimic 3 covers a lot of languages. The locally hosted web page has a Feedback
 button that encourages users to comment on how the pronunciation could be
 improved. 

If your computer architecture supports Mimic 3, you can use Mimic TTS with
speech-dispatcher or as a localhost web server with this application. When
installed from an apt archive, or a from compiled code, you can start the
local web server at startup using a command to initiate `mimic3-server`.

If you use a docker image, you can get the computer to start the mimic 
localhost web server on startup by setting the Docker container restart policy
to "always". 

[Mimic TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)

### It doesn't work?

The first step is to check if the network is available. The
network service might offer an account status report page or
a help document to assist you.

The tool relies on external libraries or packages, and python
might not have access to the current required packages.

Some ways of installing your office application restrict the
application's ability to run third party extensions. You or
your system administrator might need to set permissions for
this extension to run or for the extension to access a
network resource.

Some of the network tools require specific versions of python
or a specific system platform like `amd64`, `arm64` or `v7`.
This script might not work with those tools because it can't use
the required libraries on an unsupported version of python.

If you use python pip to install local libraries, you might have to
manually update them from time to time. Packages that are managed
by update utilities like `apt-get`, `yum` and `dnf` are upgraded
by the distribution.

Larynx
------

You can configure Read Text Extension to use Larynx. Larynx
works with most Linux distributions, even if provides your
office application using a container distribution platform
like `flatpak` or `snap`.

Using Larynx does not require an on-line connection. The
`larynx-server` application provides speech on a `localhost`
web service similarly to how [`cups`](https://www.cups.org/)
provides printing services using a `localhost` server on many
Posix computers like MacOS and desktop Linux distributions.

> Offline end-to-end text to speech system using gruut and
> onnx (architecture). There are 50 voices available across
> 9 languages.

-- [Rhasspy Larynx
Website](https://github.com/rhasspy/larynx)

<https://hub.docker.com/r/rhasspy/larynx>

### It doesn't work?

+ Is the larynx server running? Consider setting up `larynx-server`
  to automatically start up when you log in.
+ Is the language of the selected text supported and installed?

If you are using a Docker network service, it might take a little
more time to than usual to start up when the package updates
it's files. If you are using a system docker application with a
personal account, then you might need to manually download updated
speech resources if the docker application stops working with
locally installed languages. A system administrator can change your
account's ability to access a docker service or for the docker
package to access locally installed resources.

Rhvoice
-------

[Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest) is
a docker image container that can read English, Esperanto, Georgian,
Kyrgyz, Macedonian, Portuguese, Russian, Tatar and Ukrainian.

MaryTTS
-------

[MaryTTS](http://mary.dfki.de/) (Modular Architecture for Research in Synthesis)
is an open-source, multilingual Text-to-Speech Synthesis platform written in Java.
It can turn text into speech in many different languages. It runs on a `localhost`
web resource on your computer using a Docker container. Using MaryTTS does not
require an on-line connection.

You can make it sound like you by recording your voice and using MaryTTS [Import
Tools](https://github.com/marytts/marytts-wiki/blob/master/VoiceImportToolsTutorial.md)
to create a personalized voice.

The Rhsspy MaryTTS docker image is an easy-to install web application that
includes voices in several languages by default, including,

* English
* French
* German
* Italian
* Swedish
* Russian
* Telugu
* Turkish

See also:

[Adding-voices](https://rhasspy.readthedocs.io/en/v2.4.20/text-to-speech/#adding-voices)

[Docker image](https://hub.docker.com/r/synesthesiam/marytts)

[Rhasspy community](https://community.rhasspy.org/)

TTS
---

TTS is a text to speech authoring tool that includes support for converting
text to speech. The Read Text Extension accesses TTS as a client of a locally
hosted Coqui AI TTS web service. To interpret the capabilities of each tts
model, the Read Text Extension web client requires the `bs4` (beautiful soup)
pythonlibrary. To correctly parse the text the Read Text python client
requires the `spacy` python library.

TTS is a development platform. You, like other users and online community
contributors can create voice models. The speed, reliability and accuracy
of TTS's artificial intelligence generated speech can vary by model, language
and your computer's hardware. The Read Text Extension's local host web client
might not be able to access all the features of all TTS language models on all
computers

[Coqui.ai News](https://tts.readthedocs.io/en/latest/index.html)
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import getopt
import math
import os
import sys
import netgtts
try:
    import requests
    REQUESTS_OK = True
except (AttributeError, ImportError):
    REQUESTS_OK = False
try:
    import netmimic3
except (AttributeError, ImportError):
    pass
try:
    import netlarynx
except (AttributeError, ImportError):
    pass
try:
    import netmary
except (AttributeError, ImportError):
    pass
try:
    import netopentts
except (AttributeError, ImportError):
    pass
try:
    import netrhvoice
except (AttributeError, ImportError):
    pass
try:
    import nettts
except (AttributeError, ImportError):
    pass
try:
    import readtexttools
except (AttributeError, ImportError):
    pass


def usage():  # -> None
    '''
    Command line help
    '''
    print('''
Network Speech Synthesis
========================

Reads a text file using an on-line voice and a media player like ffmpeg or
avconv.

Usage
-----

    network_read_text_file.py --language=ca-ES --visible=False "input.txt"
    network_read_text_file.py --language=ca-ES --rate=70% "input.txt"

Relies on optional external libraries and an on-line connection. With long
strings, or using a slow network, the latency might be longer than two
seconds, or retrieving the online resource might fail.

Local Server
------------

The extension can use a local server that is compatible with the application
programming interface (API) of a locally hosted speech server daemon.

It is normal for a local server to take a moment to start speaking the first
time that you use it.

* [Larynx](https://github.com/rhasspy/larynx)
* [MaryTTS](http://mary.dfki.de/)
* [Mimic TTS](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3)
* [Open TTS](https://github.com/synesthesiam/opentts#open-text-to-speech-server)
* [Rhvoice-rest](https://hub.docker.com/r/aculeasis/rhvoice-rest)
* [CoquiAI demo](https://github.com/coqui-ai/TTS/pkgs/container/tts-cpu)
''')


def network_problem(voice='default'):  # -> str
    '''Return suggestions to make an on-line voice work.'''
    if len(voice) == 0:
        voice = 'requested'
    return '''Is the network connected?
=========================

+ The `%(voice)s` on-line voice is currently unavailable.
+ It might help to restart your device, refresh the network
  or check your on-line account status.
+ If you are using a `localhost` server, it might help to
  enter the local speech server command in a terminal and
  read what it prints out. (i. e.: `larynx-server`)
  ''' % locals()


def speech_wpm(_percent='100%'):  # -> int
    '''
    _percent - rate expressed as a percentage.
    Use '100%' for default rate of 160 words per minute (wpm).
    Returns rate between 20 and 640.
    '''
    _calc_product = 0
    _result = 0
    _minimum = 20
    _maximum = 640
    _normal = 160
    _p_cent = ''

    try:
        if '%' in _percent:
            _p_cent = _percent.replace('%', '')
            _calc_product = (float(_p_cent)
                             if '.' in _p_cent else int(_p_cent) / 100)
            _result = math.ceil(_calc_product * _normal)
        else:
            _calc_product = (float(_percent)
                             if '.' in _percent else int(_percent))
            _result = math.ceil(_calc_product)
    except TypeError:
        return _normal
    if _result == 0:
        return _normal
    elif _result <= _minimum:
        return _minimum
    elif _result >= _maximum:
        return _maximum
    return _result


def network_ok(_iso_lang='en-US', _local_url=''):  # -> bool
    '''Do at least one of the classes support an on-line speech library?'''
    _continue = False
    if not _continue:
        try:
            _mimic3 = netmimic3.Mimic3Class()
            _continue = _mimic3.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _larynx = netlarynx.LarynxClass()
            _continue = _larynx.language_supported(_iso_lang, _local_url, 'AUTO')
        except NameError:
            pass
    if not _continue:
        try:
            _rhvoice_rest = netrhvoice.RhvoiceLocalHost()
            _continue = _rhvoice_rest.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _opentts = netopentts.OpenTTSClass()
            if _opentts.language_supported(_iso_lang, _local_url):
                _continue = True
        except NameError:
            pass
    if not _continue:
        try:
            _mary_tts = netmary.MaryTtsClass()
            _continue = _mary_tts.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    if not _continue:
        try:
            _gtts_class = netgtts.GoogleTranslateClass()
            if _gtts_class.check_version(_gtts_class.tested_version):
                _continue = True
        except NameError:
            pass
    if not _continue:
        try:
            _coqui_demo = nettts.CoquiDemoLocalHost()
            _continue = _coqui_demo.language_supported(_iso_lang, _local_url)
        except NameError:
            pass
    return _continue


def is_ssml(_text=''):
    '''Return `True` if text includes standard ssml tags and the string
    is valid XML,'''
    _ssml = '</speak>' in _text and '<speak' in _text
    if _ssml:
        # Check if `_text` is valid XML
        if readtexttools.strip_xml(_text) == _text:
            _ssml = False
    return _ssml


def network_main(_text_file_in='',
                 _iso_lang='ca-ES',
                 _visible='false',
                 _audible='true',
                 _media_out='',
                 _writer='',
                 _title='',
                 _icon='',
                 _size='600x600',
                 _speech_rate=160,
                 _vox='',
                 _local_url='',
                 _denoiser_strength=0.005,
                 _noise_scale=0.667):  # -> boolean
    '''Read a text file aloud using a network resource.'''
    _imported_meta = readtexttools.ImportedMetaData()
    _text = _imported_meta.meta_from_file(_text_file_in)
    if len(_text.strip()) == 0:
        return False
    _info = readtexttools.check_artist(_writer)
    clip_title = readtexttools.check_title(_title, 'espeak')
    # If the library does not require a postprocess, use `0`,
    # otherwise use the item corresponding to the next action.
    _post_processes = [
        None, 'process_mp3_media', 'process_playlist',
        'process_riff_media', 'process_vorbis_media', 'process_wav_media',
        'process_audio_media'
    ]
    _vox = _vox.strip('\'" \t\n').lower()
    # Prioritize speech engines that use json to communicate data
    # because text tables can use ambiguous labels (i. e.: `NA`)
    # Prioritize engines where everything can be achieved using `urllib`
    # because some immutable office packages do not include `requests`
    # support.
    try:
        _mimic3 = netmimic3.Mimic3Class()
        if _mimic3.language_supported(_iso_lang, _local_url, _vox):
            _mimic3.spd_voice_to_mimic3_voice(_vox, _iso_lang, _local_url)
            _ssml = is_ssml(_text)
            _mimic3.read(_text, _iso_lang, _visible, _audible, _media_out,
                        _icon, clip_title, _post_processes[5], _info, _size,
                        _ssml, 20, 60)
            return True
    except NameError:
        pass
    try:
        _larynx = netlarynx.LarynxClass()        
        if _larynx.language_supported(
                _iso_lang,
                _local_url,
                _vox,
                ) and _vox in _larynx.accept_voice:

            _quality = -1  # Auto; Manual is 0 (lowest) to 2 (highest)
            _ssml = is_ssml(_text)
            _larynx.read(_text, _iso_lang, _visible, _audible, _media_out,
                        _icon, clip_title, _post_processes[5], _info, _size,
                        _speech_rate, _quality, _ssml, _denoiser_strength,
                        _noise_scale, 20, 60)
            return True
    except NameError:
        pass
    try:
        _rhvoice_rest = netrhvoice.RhvoiceLocalHost()
        if _rhvoice_rest.language_supported(_iso_lang, _local_url):
            _rhvoice_rest.read(_text, _iso_lang, _visible, _audible,
                            _media_out, _icon, clip_title,
                            _post_processes[5], _info, _size, _speech_rate,
                            _vox, 4, 30)
            return True
    except NameError:
        pass
    try:
        _opentts = netopentts.OpenTTSClass()
        if _opentts.language_supported(_iso_lang, _local_url):
            _ssml = is_ssml(_text)
            _opentts._spd_voice_to_opentts_voice(_vox, _iso_lang)
            _opentts.read(_text, _iso_lang, _visible, _audible, _media_out,
                        _icon, clip_title, _post_processes[5], _info,
                        _size, _ssml, .03, 20, 60)
            return True
    except NameError:
        pass
    try:
        _marytts = netmary.MaryTtsClass()
        if _marytts.language_supported(_iso_lang, _local_url):
            _ssml = is_ssml(_text)
            if REQUESTS_OK:
                if int(requests.__version__[0] == 1):
                    if _ssml:
                        _text = readtexttools.strip_xml(_text)
                        _ssml = False
            else:
                if _ssml:
                    _text = readtexttools.strip_xml(_text)
                    _ssml = False
            _marytts.read(_text, _iso_lang, _visible, _audible, _media_out,
                        _icon, clip_title, _post_processes[5], _info, _size,
                        _speech_rate, _ssml, _vox, 4, 15)
            return True
    except NameError:
        pass
    try:
        _coqui_demo = nettts.CoquiDemoLocalHost()
        if _coqui_demo.language_supported(_iso_lang, _local_url):
            _coqui_demo.read(_text, _iso_lang, _visible, _audible, _media_out,
                            _icon, clip_title, _post_processes[5], _info,
                            _size, _speech_rate, _vox, 20, 60)
            return True
    except (NameError, TypeError):
        pass
    try:
        _gtts_class = netgtts.GoogleTranslateClass() 
        if _gtts_class.check_version(
                _gtts_class.tested_version) and _vox in _gtts_class.accept_voice:
            _gtts_class.read(_text, _iso_lang, _visible, _audible, _media_out,
                            _icon, clip_title, _post_processes[1], _info,
                            _size, _speech_rate)        
            return True
    except NameError:
        pass
    # Just display a translation link.
    _gtts_class.read(_text, _iso_lang, _visible, _audible, _media_out,
                     _icon, clip_title, _post_processes[0], _info,
                     _size, _speech_rate)
    
    print(
        'No working network server was found, or the requested voice is unavailable.\n'
    )
    usage()
    return False


def main():  # -> NoReturn
    '''Use network speech synthesis for supported languages while on-line'''
    if not sys.version_info >= (3, 6) or not os.name in ['posix', 'nt']:
        print('Your system does not support the network python tool.')
        usage()
        sys.exit(0)
    _speech_rate = 160
    _iso_lang = 'ca-ES'
    try:
        _iso_lang = readtexttools.default_lang().replace('_', '-')
    except (AttributeError, ImportError):
        pass
    _media_out = ''
    _visible = ''
    _audible = ''
    _text = ''
    _percent_rate = '100%'
    _speech_rate = speech_wpm(_percent_rate)
    _denoiser_strength = 0.005
    _noise_scale = 0.667
    _icon = ''
    _title = ''
    _writer = ''
    _size = '600x600'
    _speaker = 'AUTO'
    _local_url = ''
    _text_file_in = sys.argv[-1]

    if os.path.isfile(_text_file_in):
        if sys.argv[-1] == sys.argv[0]:
            usage()
            sys.exit(0)
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hovalritndsxuec', [
                'help', 'output=', 'visible=', 'audible=', 'language=',
                'rate=', 'image=', 'title=', 'artist=', 'dimensions=',
                'speaker=', 'voice=', 'url=', 'denoiser_strength=',
                'noise_scale='
            ])
        except getopt.GetoptError:
            print('option -a not recognized')
            usage()
            sys.exit(2)
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(0)
            elif o in ('-o', '--output'):
                _media_out = a
            elif o in ('-v', '--visible'):
                _visible = a
            elif o in ('-a', '--audible'):
                _audible = a
            elif o in ('-l', '--language'):
                _iso_lang = a
            elif o in ('-r', '--rate'):
                _percent_rate = a
                if len(_percent_rate) != 0:
                    _speech_rate = speech_wpm(_percent_rate)
            elif o in ('-i', '--image'):
                _icon = a
            elif o in ('-t', '--title'):
                _title = a
            elif o in ('-n', '--artist'):
                _writer = a
            elif o in ('-d', '--dimensions'):
                _size = a
            elif o in ('-s', '--speaker'):
                # depreciated
                _speaker = a
            elif o in ('-x', '--voice'):
                _speaker = a
            elif o in ('-u', '--url'):
                _local_url = a
            elif o in ('-e', '--denoiser_strength'):
                try:
                    _denoiser_strength = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_denoiser_strength):
                    _denoiser_strength = 0.005
            elif o in ('-c', '--noise_scale'):
                try:
                    _noise_scale = float(o)
                except (AttributeError, TypeError, ValueError):
                    pass
                if not bool(_noise_scale):
                    _noise_scale = 0.667
            else:
                assert False, 'unhandled option'
        network_main(_text_file_in, _iso_lang, _visible, _audible, _media_out,
                     _writer, _title, _icon, _size, _speech_rate, _speaker,
                     _local_url, _denoiser_strength, _noise_scale)
    sys.exit(0)


if __name__ == '__main__':
    main()
