import string

from . import jisho


class ConjugationError(Exception):
    def __init__(self, form, verb):
        message = 'Unable to conjugate {} form of {}'.format(form, verb)
        super().__init__(message)


class Verb(jisho.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordered by most to least commonly used
        verb_types = (
            'godan verb', 'ichidan verb', 'kuru verb', 'suru verb', 'su verb',
            'nidan verb', 'yodan verb'
            )
        self.type = None
        for pos in self.parts_of_speech:
            for vt in verb_types:
                if vt in pos:
                    self.type = vt
                    break
            if self.type is not None:
                break

    @classmethod
    def from_entry(cls, entry):
        values = vars(entry)
        return cls(**values)

    def conjugate(self, vowel):
        ending = self.reading[-1]
        replacement = self._u_conjugated[(ending, vowel)]
        return str(self)[:-1] + replacement

    _u_conjugated = {
        ('う', 'あ'): 'あ',
        ('う', 'え'): 'え',
        ('う', 'い'): 'い',
        ('う', 'お'): 'お',
        ('う', 'う'): 'う',
        ('く', 'あ'): 'か',
        ('く', 'え'): 'け',
        ('く', 'い'): 'き',
        ('く', 'お'): 'こ',
        ('く', 'う'): 'く',
        ('ぐ', 'あ'): 'が',
        ('ぐ', 'え'): 'げ',
        ('ぐ', 'い'): 'ぎ',
        ('ぐ', 'お'): 'ご',
        ('ぐ', 'う'): 'ぐ',
        ('す', 'あ'): 'さ',
        ('す', 'え'): 'せ',
        ('す', 'い'): 'し',
        ('す', 'お'): 'そ',
        ('す', 'う'): 'す',
        ('ず', 'あ'): 'ざ',
        ('ず', 'え'): 'ぜ',
        ('ず', 'い'): 'じ',
        ('ず', 'お'): 'ぞ',
        ('ず', 'う'): 'ず',
        ('つ', 'あ'): 'た',
        ('つ', 'え'): 'て',
        ('つ', 'い'): 'ち',
        ('つ', 'お'): 'と',
        ('つ', 'う'): 'つ',
        ('づ', 'あ'): 'だ',
        ('づ', 'え'): 'で',
        ('づ', 'い'): 'ぢ',
        ('づ', 'お'): 'ど',
        ('づ', 'う'): 'づ',
        ('ぬ', 'あ'): 'な',
        ('ぬ', 'え'): 'ね',
        ('ぬ', 'い'): 'に',
        ('ぬ', 'お'): 'の',
        ('ぬ', 'う'): 'ぬ',
        ('ふ', 'あ'): 'は',
        ('ふ', 'え'): 'へ',
        ('ふ', 'い'): 'ひ',
        ('ふ', 'お'): 'ほ',
        ('ふ', 'う'): 'ふ',
        ('ぶ', 'あ'): 'ば',
        ('ぶ', 'え'): 'べ',
        ('ぶ', 'い'): 'び',
        ('ぶ', 'お'): 'ぼ',
        ('ぶ', 'う'): 'ぶ',
        ('ぷ', 'あ'): 'ぱ',
        ('ぷ', 'え'): 'ぺ',
        ('ぷ', 'い'): 'ぴ',
        ('ぷ', 'お'): 'ぽ',
        ('ぷ', 'う'): 'ぷ',
        ('む', 'あ'): 'ま',
        ('む', 'え'): 'め',
        ('む', 'い'): 'み',
        ('む', 'お'): 'も',
        ('む', 'う'): 'む',
        ('る', 'あ'): 'ら',
        ('る', 'え'): 'れ',
        ('る', 'い'): 'り',
        ('る', 'お'): 'ろ',
        ('る', 'う'): 'る'
        }


_rmj_to_hrgn = {
    'a': 'あ',  'e': 'え',  'i': 'い',  'o': 'お',  'u': 'う',
    'ka': 'か', 'ke': 'け', 'ki': 'き', 'ko': 'こ', 'ku': 'く',
    'ga': 'が', 'ge': 'げ', 'gi': 'ぎ', 'go': 'ご', 'gu': 'ぐ',
    'sa': 'さ', 'se': 'せ', 'shi': 'し', 'so': 'そ', 'su': 'す',
    'za': 'ざ', 'ze': 'ぜ', 'ji': 'じ', 'zo': 'ぞ', 'zu': 'ず',
    'ta': 'た', 'te': 'て', 'chi': 'ち', 'to': 'と', 'tsu': 'つ',
    'da': 'だ', 'de': 'で', 'zhi': 'ぢ', 'do': 'ど', 'dzu': 'づ',
    'na': 'な', 'ne': 'ね', 'ni': 'に', 'no': 'の', 'nu': 'ぬ',
    'ha': 'は', 'he': 'へ', 'hi': 'ひ', 'ho': 'ほ', 'fu': 'ふ',
    'ba': 'ば', 'be': 'べ', 'bi': 'び', 'bo': 'ぼ', 'bu': 'ぶ',
    'pa': 'ぱ', 'pe': 'ぺ', 'pi': 'ぴ', 'po': 'ぽ', 'pu': 'ぷ',
    'ma': 'ま', 'me': 'め', 'mi': 'み', 'mo': 'も', 'mu': 'む',
    'ra': 'ら', 're': 'れ', 'ri': 'り', 'ro': 'ろ', 'ru': 'る',
    'wa': 'わ', 'we': 'ゑ', 'wi': 'ゐ', 'wo': 'を',
    'ya': 'や', 'yo': 'よ', 'yu': 'ゆ',
    'sha': 'しゃ', 'sho': 'しょ', 'shu': 'しゅ',
    'ja': 'じゃ', 'jo': 'じょ', 'ju': 'じゅ',
    'cha': 'ちゃ', 'cho': 'ちょ', 'chu': 'ちゅ',
    'zha': 'ぢゃ', 'zho': 'ぢょ', 'zhu': 'ぢゅ',
    'kya': 'きゃ', 'kyo': 'きょ', 'kyu': 'きゅ',
    'gya': 'ぎゃ', 'gyo': 'ぎょ', 'gyu': 'ぎゅ',
    'nya': 'にゃ', 'nyo': 'にょ', 'nyu': 'にゅ',
    'hya': 'ひゃ', 'hyo': 'ひょ', 'hyu': 'ひゅ',
    'bya': 'びゃ', 'byo': 'びょ', 'byu': 'びゅ',
    'pya': 'ぴゃ', 'pyo': 'ぴょ', 'pyu': 'ぴゅ',
    'rya': 'りゃ', 'ryo': 'りょ', 'ryu': 'りゅ',
    'mya': 'みゃ', 'myo': 'みょ', 'myu': 'みゅ',
    'n': 'ん', 'vu': 'ゔ'
    }

_hrgn_to_rmj = {h: r for r, h in _rmj_to_hrgn.items()}


def romanji_to_hiragana(text):
    """
    >>> romanji_to_hiragana('minna, shigoto ha kyuji ni hajimeru no tottemo ii')
    'みんな, しごと は きゅじ に はじめる の とっても いい'
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}
    on = ''
    hiragana = []
    for char in text:
        is_letter = char in string.ascii_letters
        if is_letter:
            on += char
        if char in vowels or (on and not is_letter):
            if len(on) > 1 and on[0] == on[1]:
                if on[0] != 'n':
                    hiragana.append('っ')
                else:
                    hiragana.append('ん')
                on = on[1:]
            hiragana.append(_rmj_to_hrgn[on])
            on = ''
        if not is_letter:
            hiragana.append(char)
    return ''.join(hiragana)


def hiragana_to_romanji(text):
    """
    >>> hiragana_to_romanji('みんな, しごと は きゅじ に はじめる の とっても いい')
    'minna, shigoto ha kyuji ni hajimeru no tottemo ii'
    """
    out = []
    previous = ''
    is_carried = False
    for char in text:
        if char in {'ゃ', 'ょ', 'ゅ'}:
            del out[-1]
            char = previous + char
        if char == 'っ':
            is_carried = True
        else:
            rj = _hrgn_to_rmj.get(char, char)
            if is_carried:
                rj = rj[0] + rj
                is_carried = False
            out.append(rj)
        previous = char
    return ''.join(out)


def verb_type(verb):
    """
    >>> verb_type('かう')
    'う'
    >>> verb_type('たべる')
    'る'
    >>> verb_type('わかる')
    'う'
    >>> verb_type('する')
    >>> verb_type('くる')
    """
    exceptional_u = {
        'かえる': '帰る',
        'しゃべる': 'しゃべる',
        'しる': '知る',
        'はいる': '入る',
        'きる': '切る',
        'へる': '減る',
        'あせる': '焦る',
        'かぎる': '限る',
        'ける': '蹴る',
        'すべる': '滑る',
        'にぎる': '握る',
        'ねる': '練る',
        'まいる': '参る',
        'まじる': '交じる',
        'あざける': '嘲る',
        'くつがえる': '覆る',
        'さえぎる': '遮る',
        'ののしる': '罵る',
        'ひねる': '捻る',
        'ひるがえる': '翻る',
        'めいる': '滅入る',
        'よみがえる': '蘇る'
        }
    if verb in {'する', 'くる'}:
        return None
    elif verb[-1] != 'る' or verb in exceptional_u:
        return 'う'
    elif hiragana_to_romanji(verb[-2])[-1] in {'a', 'o', 'u'}:
        return 'う'
    else:
        return 'る'


def negative_informal(verb):
    """
    >>> negative_informal(Verb('ある', ['godan verb'], []))
    'ない'
    >>> negative_informal(Verb('たべる', ['ichidan verb'], []))
    'たべない'
    >>> negative_informal(Verb('わかる', ['godan verb'], []))
    'わからない'
    >>> negative_informal(Verb('よぶ', ['godan verb'], []))
    'よばない'
    >>> negative_informal(Verb('かう', ['godan verb'], []))
    'かわない'
    >>> negative_informal(Verb('いく', ['godan verb'], []))
    'いかない'
    >>> negative_informal(Verb('いる', ['ichidan verb'], []))
    'いない'
    """
    written = str(verb)
    if verb.type == 'suru verb':
        return written[:-2] + 'しない'
    elif verb.type == 'kuru verb':
        return written[:-2] + 'こない'
    elif verb.reading[-2:] == 'ある':
        return written[:-2] + 'ない'
    elif verb.type == 'godan verb' and written[-1] == 'う':
        return written[:-1] + 'わない'
    elif verb.type == 'ichidan verb':
        return written[:-1] + 'ない'
    else:
        return verb.conjugate('あ') + 'ない'


def _formal_prefix(verb):
    if verb == 'する':
        return 'し'
    elif verb == 'くる':
        return 'き'
    elif verb_type(verb) == 'る':
        return verb[:-1]
    else:
        i_ending = _u_conjugated[(verb[-1], 'い')]
        return verb[:-1] + i_ending


def negative_formal(verb):
    """
    >>> negative_formal('ある')
    'ありません'
    >>> negative_formal('たべる')
    'たべません'
    >>> negative_formal('わかる')
    'わかりません'
    >>> negative_formal('よぶ')
    'よびません'
    >>> negative_formal('かう')
    'かいません'
    """
    return _formal_prefix(verb) + 'ません'


def past_informal(verb):
    """
    >>> past_informal('ある')
    'あった'
    >>> past_informal('たべる')
    'たべた'
    >>> past_informal('わかる')
    'わかった'
    >>> past_informal('よぶ')
    'よんだ'
    >>> past_informal('かう')
    'かった'
    >>> past_informal('きく')
    'きいた'
    >>> past_informal('およぐ')
    'およいだ'
    """
    if verb == 'する':
        return 'した'
    elif verb == 'くる':
        return 'きた'
    elif verb == 'いく':
        return 'いった'
    elif verb_type(verb) == 'る':
        return verb[:-1] + 'た'
    elif verb[-1] == 'す':
        return verb[:-1] + 'した'
    elif verb[-1] == 'く':
        return verb[:-1] + 'いた'
    elif verb[-1] == 'ぐ':
        return verb[:-1] + 'いだ'
    elif verb[-1] in {'む', 'ぶ', 'ぬ'}:
        return verb[:-1] + 'んだ'
    elif verb[-1] in {'る', 'う', 'つ'}:
        return verb[:-1] + 'った'


def past_negative_informal(verb):
    """
    >>> past_negative_informal('ある')
    'なかった'
    >>> past_negative_informal('たべる')
    'たべなかった'
    >>> past_negative_informal('わかる')
    'わからなかった'
    >>> past_negative_informal('よぶ')
    'よばなかった'
    >>> past_negative_informal('かう')
    'かわなかった'
    >>> past_negative_informal('くる')
    'こなかった'
    >>> past_negative_informal('きく')
    'きかなかった'
    >>> past_negative_informal('およぐ')
    'およがなかった'
    >>> past_negative_informal('いく')
    'いかなかった'
    """
    negative = negative_informal(verb)
    return negative[:-1] + 'かった'


def volitional_informal(verb):
    """
    >>> volitional_informal('たべる')
    'たべよう'
    >>> volitional_informal('はなす')
    'はなそう'
    >>> volitional_informal('しんじる')
    'しんじよう'
    >>> volitional_informal('かう')
    'かおう'
    >>> volitional_informal('いく')
    'いこう'
    """
    if verb == 'する':
        return 'しよう'
    elif verb == 'くる':
        return 'こよう'
    elif verb_type(verb) == 'る':
        return verb[:-1] + 'よう'
    else:
        o_ending = _u_conjugated[(verb[-1], 'お')]
        return verb[:-1] + o_ending + 'う'


def volitional_formal(verb):
    """
    >>> volitional_formal('たべる')
    'たべましょう'
    >>> volitional_formal('はなす')
    'はなしましょう'
    >>> volitional_formal('しんじる')
    'しんじましょう'
    >>> volitional_formal('かう')
    'かいましょう'
    >>> volitional_formal('いく')
    'いきましょう'
    """
    return _formal_prefix(verb) + 'ましょう'


def potential_informal(verb):
    """
    >>> potential_informal('たべる')
    'たべられる'
    >>> potential_informal('はなす')
    'はなせる'
    >>> potential_informal('しんじる')
    'しんじられる'
    >>> potential_informal('かう')
    'かえる'
    >>> potential_informal('いく')
    'いける'
    >>> potential_informal('とる')
    'とれる'
    """
    if verb == 'する':
        return 'できる'
    elif verb == 'くる':
        return 'こられる'
    elif verb_type(verb) == 'る':
        return verb[:-1] + 'られる'
    else:
        e_ending = _u_conjugated[(verb[-1], 'え')]
        return verb[:-1] + e_ending + 'る'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
