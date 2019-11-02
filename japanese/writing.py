"""Convert between the syllabic writing systems"""
import string


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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
