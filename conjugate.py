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
                    self.type = vt[:-5]
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

    def formal_prefix(self):
        if verb.type == 'suru':
            return str(self)[:-2] + 'し'
        elif verb.type == 'kuru':
            return str(self)[:-2] + 'き'
        elif verb.type == 'ichidan':
            return str(self)[:-1]
        else:
            return verb.conjugate('い')

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


def negative_informal(verb):
    """
    >>> negative_informal(Verb('ある', ['godan verb'], []))
    'ない'
    >>> negative_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べない'
    >>> negative_informal(Verb('わかる', ['godan verb'], []))
    'わからない'
    >>> negative_informal(Verb('よぶ', ['godan verb'], []))
    'よばない'
    >>> negative_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買わない'
    >>> negative_informal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行かない'
    >>> negative_informal(Verb('いる', ['ichidan verb'], []))
    'いない'
    """
    written = str(verb)
    if verb.type == 'suru':
        return written[:-2] + 'しない'
    elif verb.type == 'kuru':
        return written[:-2] + 'こない'
    elif verb.reading[-2:] == 'ある':
        return written[:-2] + 'ない'
    elif verb.type == 'godan' and written[-1] == 'う':
        return written[:-1] + 'わない'
    elif verb.type == 'ichidan':
        return written[:-1] + 'ない'
    else:
        return verb.conjugate('あ') + 'ない'


def negative_formal(verb):
    """
    >>> negative_formal(Verb('ある', ['godan verb'], []))
    'ありません'
    >>> negative_formal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べません'
    >>> negative_formal(Verb('わかる', ['godan verb'], []))
    'わかりません'
    >>> negative_formal(Verb('よぶ', ['godan verb'], []))
    'よびません'
    >>> negative_formal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買いません'
    """
    return verb.formal_prefix() + 'ません'


def past_informal(verb):
    """
    >>> past_informal(Verb('ある', ['godan verb'], []))
    'あった'
    >>> past_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べた'
    >>> past_informal(Verb('わかる', ['godan verb'], []))
    'わかった'
    >>> past_informal(Verb('よぶ', ['godan verb'], []))
    'よんだ'
    >>> past_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買った'
    >>> past_informal(Verb('きく', ['godan verb'], []))
    'きいた'
    >>> past_informal(Verb('およぐ', ['godan verb'], []))
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
    >>> past_negative_informal(Verb('ある', ['godan verb'], []))
    'なかった'
    >>> past_negative_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べなかった'
    >>> past_negative_informal(Verb('わかる', ['godan verb'], []))
    'わからなかった'
    >>> past_negative_informal(Verb('よぶ', ['godan verb'], []))
    'よばなかった'
    >>> past_negative_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買わなかった'
    >>> past_negative_informal(Verb('くる', ['kuru verb'], []))
    'こなかった'
    >>> past_negative_informal(Verb('きく', ['godan verb'], []))
    'きかなかった'
    >>> past_negative_informal(Verb('およぐ', ['godan verb'], []))
    'およがなかった'
    >>> past_negative_informal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行かなかった'
    """
    negative = negative_informal(verb)
    return negative[:-1] + 'かった'


def volitional_informal(verb):
    """
    >>> volitional_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べよう'
    >>> volitional_informal(Verb('はなす', ['godan verb'], [], kanji='話す'))
    '話そう'
    >>> volitional_informal(Verb('しんじる', ['ichidan verb'], [], kanji='信じる'))
    '信じよう'
    >>> volitional_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買おう'
    >>> volitional_informal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行こう'
    """
    written = str(verb)
    if verb.type == 'suru':
        return written[:-2] + 'しよう'
    elif verb.type == 'kuru':
        return written[:-2] + 'こよう'
    elif verb.type == 'ichidan':
        return written[:-1] + 'よう'
    else:
        return verb.conjugate('お') + 'う'


def volitional_formal(verb):
    """
    >>> volitional_formal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べましょう'
    >>> volitional_formal(Verb('はなす', ['godan verb'], [], kanji='話す'))
    '話しましょう'
    >>> volitional_formal(Verb('しんじる', ['ichidan verb'], [], kanji='信じる'))
    '信じましょう'
    >>> volitional_formal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買いましょう'
    >>> volitional_formal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行きましょう'
    """
    return verb.formal_prefix() + 'ましょう'


def potential_informal(verb):
    """
    >>> potential_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べられる'
    >>> potential_informal(Verb('はなす', ['godan verb'], [], kanji='話す'))
    '話せる'
    >>> potential_informal(Verb('しんじる', ['ichidan verb'], [], kanji='信じる'))
    '信じられる'
    >>> potential_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買える'
    >>> potential_informal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行ける'
    >>> potential_informal(Verb('とる', ['ichidan verb'], [], kanji='取る'))
    '取れる'
    """
    written = str(verb)
    if verb.type == 'suru':
        return written[:-2] + 'できる'
    elif verb.type == 'kuru':
        return written[:-2] + 'こられる'
    elif verb.type == 'ichidan':
        return written[:-1] + 'られる'
    else:
        return verb.conjugate('え') + 'る'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
