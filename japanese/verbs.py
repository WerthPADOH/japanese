import unicodedata
import jisho


class ConjugationError(Exception):
    def __init__(self, verb):
        message = f'Unable to conjugate {verb.type} form of {verb}'
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

    def stem(self):
        if self.type == 'suru':
            return str(self)[:-2] + 'し'
        elif self.type == 'kuru':
            return str(self)[:-2] + 'き'
        elif self.type == 'ichidan':
            return str(self)[:-1]
        elif self.type == 'godan':
            return self.conjugate('い')
        else:
            raise ConjugationError(self)

    def te_form(self):
        written = str(self)
        if self.type == 'suru':
            return 'して'
        elif self.type == 'kuru':
            if written[-2:] == '来る':
                return written[:-2] + '来て'
            else:
                return written[:-2] + 'きて'
        elif self.kanji.endswith('行く'):
            return written[:-2] + '行って'
        elif self.reading == 'いく':
            return 'いって'
        elif self.type == 'ichidan':
            return written[:-1] + 'て'
        elif self.type == 'godan':
            if written[-1] == 'す':
                return written[:-1] + 'して'
            elif written[-1] == 'く':
                return written[:-1] + 'いて'
            elif written[-1] == 'ぐ':
                return written[:-1] + 'いで'
            elif written[-1] in {'む', 'ぶ', 'ぬ'}:
                return written[:-1] + 'んで'
            elif written[-1] in {'る', 'う', 'つ'}:
                return written[:-1] + 'って'
        else:
            raise ConjugationError(self)

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


def negative_informal(verb):
    """
    >>> negative_informal(Verb('ある', ['godan verb'], []))
    'ない'
    >>> negative_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べない'
    >>> negative_informal(Verb('わかる', ['godan verb'], [], kanji='分かる'))
    '分からない'
    >>> negative_informal(Verb('よぶ', ['godan verb'], [], kanji='呼ぶ'))
    '呼ばない'
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
        if written[-2:] == '来る':
            return written[:-2] + '来ない'
        else:
            return written[:-2] + 'こない'
    elif verb.reading[-2:] == 'ある':
        return written[:-2] + 'ない'
    elif verb.type == 'godan' and written[-1] == 'う':
        return written[:-1] + 'わない'
    elif verb.type == 'ichidan':
        return written[:-1] + 'ない'
    elif verb.type == 'godan':
        return verb.conjugate('あ') + 'ない'
    else:
        raise ConjugationError(verb)


def negative_formal(verb):
    """
    >>> negative_formal(Verb('ある', ['godan verb'], []))
    'ありません'
    >>> negative_formal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べません'
    >>> negative_formal(Verb('わかる', ['godan verb'], [], kanji='分かる'))
    '分かりません'
    >>> negative_formal(Verb('よぶ', ['godan verb'], [], kanji='呼ぶ'))
    '呼びません'
    >>> negative_formal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買いません'
    """
    return verb.stem() + 'ません'


def past_informal(verb):
    """
    >>> past_informal(Verb('ある', ['godan verb'], []))
    'あった'
    >>> past_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べた'
    >>> past_informal(Verb('わかる', ['godan verb'], [], kanji='分かる'))
    '分かった'
    >>> past_informal(Verb('よぶ', ['godan verb'], [], kanji='呼ぶ'))
    '呼んだ'
    >>> past_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買った'
    >>> past_informal(Verb('きく', ['godan verb'], [], kanji='聞く'))
    '聞いた'
    >>> past_informal(Verb('およぐ', ['godan verb'], [], kanji='泳ぐ'))
    '泳いだ'
    """
    tf = verb.te_form()
    if tf[-1] == 'て':
        return tf[:-1] + 'た'
    elif tf[-1] == 'で':
        return tf[:-1] + 'だ'


def past_negative_informal(verb):
    """
    >>> past_negative_informal(Verb('ある', ['godan verb'], []))
    'なかった'
    >>> past_negative_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べなかった'
    >>> past_negative_informal(Verb('わかる', ['godan verb'], [], kanji='分かる'))
    '分からなかった'
    >>> past_negative_informal(Verb('よぶ', ['godan verb'], [], kanji='呼ぶ'))
    '呼ばなかった'
    >>> past_negative_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買わなかった'
    >>> past_negative_informal(Verb('くる', ['kuru verb'], []))
    'こなかった'
    >>> past_negative_informal(Verb('くる', ['kuru verb'], [], kanji='来る'))
    '来なかった'
    >>> past_negative_informal(Verb('きく', ['godan verb'], [], kanji='聞く'))
    '聞かなかった'
    >>> past_negative_informal(Verb('およぐ', ['godan verb'], [], kanji='泳ぐ'))
    '泳がなかった'
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
        if written[-2:] == '来る':
            return written[:-2] + '来よう'
        else:
            return written[:-2] + 'こよう'
    elif verb.type == 'ichidan':
        return written[:-1] + 'よう'
    elif verb.type == 'godan':
        return verb.conjugate('お') + 'う'
    else:
        raise ConjugationError(verb)


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
    return verb.stem() + 'ましょう'


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
    >>> potential_informal(Verb('とる', ['godan verb'], [], kanji='取る'))
    '取れる'
    >>> potential_informal(Verb('そんする', ['suru verb'], [], kanji='存する'))
    '存出来る'
    >>> potential_informal(Verb('そんする', ['suru verb'], []))
    'そんできる'
    """
    written = str(verb)
    has_kanji = any(unicodedata.name(char)[:3] == 'CJK' for char in written)
    if verb.type == 'suru':
        if has_kanji:
            return written[:-2] + '出来る'
        else:
            return written[:-2] + 'できる'
    elif verb.type == 'kuru':
        if written[-2:] == '来る':
            return written[:-2] + '来られる'
        else:
            return written[:-2] + 'こられる'
    elif verb.type == 'ichidan':
        return written[:-1] + 'られる'
    elif verb.type == 'godan':
        return verb.conjugate('え') + 'る'
    else:
        raise ConjugationError(verb)


def continuing_informal(verb):
    """
    >>> continuing_informal(Verb('たべる', ['ichidan verb'], [], kanji='食べる'))
    '食べている'
    >>> continuing_informal(Verb('はなす', ['godan verb'], [], kanji='話す'))
    '話している'
    >>> continuing_informal(Verb('しんじる', ['ichidan verb'], [], kanji='信じる'))
    '信じている'
    >>> continuing_informal(Verb('かう', ['godan verb'], [], kanji='買う'))
    '買っている'
    >>> continuing_informal(Verb('いく', ['godan verb'], [], kanji='行く'))
    '行っている'
    >>> continuing_informal(Verb('とる', ['godan verb'], [], kanji='取る'))
    '取っている'
    >>> continuing_informal(Verb('しぬ', ['godan verb'], [], kanji='死ぬ'))
    '死んでいる'
    """
    return verb.te_form() + 'いる'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
