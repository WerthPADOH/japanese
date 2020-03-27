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

    def negative_informal(self):
        """
        >>> Verb('ある', ['godan verb'], []).negative_informal()
        'ない'
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').negative_informal()
        '食べない'
        >>> Verb('わかる', ['godan verb'], [], kanji='分かる').negative_informal()
        '分からない'
        >>> Verb('よぶ', ['godan verb'], [], kanji='呼ぶ').negative_informal()
        '呼ばない'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').negative_informal()
        '買わない'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').negative_informal()
        '行かない'
        >>> Verb('いる', ['ichidan verb'], []).negative_informal()
        'いない'
        """
        written = str(self)
        if self.type == 'suru':
            return written[:-2] + 'しない'
        elif self.type == 'kuru':
            if written[-2:] == '来る':
                return written[:-2] + '来ない'
            else:
                return written[:-2] + 'こない'
        elif self.reading[-2:] == 'ある':
            return written[:-2] + 'ない'
        elif self.type == 'godan' and written[-1] == 'う':
            return written[:-1] + 'わない'
        elif self.type == 'ichidan':
            return written[:-1] + 'ない'
        elif self.type == 'godan':
            return self.conjugate('あ') + 'ない'
        else:
            raise ConjugationError(self)

    def negative_formal(self):
        """
        >>> Verb('ある', ['godan verb'], []).negative_formal()
        'ありません'
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').negative_formal()
        '食べません'
        >>> Verb('わかる', ['godan verb'], [], kanji='分かる').negative_formal()
        '分かりません'
        >>> Verb('よぶ', ['godan verb'], [], kanji='呼ぶ').negative_formal()
        '呼びません'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').negative_formal()
        '買いません'
        """
        return self.stem() + 'ません'

    def past_informal(self):
        """
        >>> Verb('ある', ['godan verb'], []).past_informal()
        'あった'
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').past_informal()
        '食べた'
        >>> Verb('わかる', ['godan verb'], [], kanji='分かる').past_informal()
        '分かった'
        >>> Verb('よぶ', ['godan verb'], [], kanji='呼ぶ').past_informal()
        '呼んだ'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').past_informal()
        '買った'
        >>> Verb('きく', ['godan verb'], [], kanji='聞く').past_informal()
        '聞いた'
        >>> Verb('およぐ', ['godan verb'], [], kanji='泳ぐ').past_informal()
        '泳いだ'
        """
        tf = self.te_form()
        if tf[-1] == 'て':
            return tf[:-1] + 'た'
        elif tf[-1] == 'で':
            return tf[:-1] + 'だ'

    def past_negative_informal(self):
        """
        >>> Verb('ある', ['godan verb'], []).past_negative_informal()
        'なかった'
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').past_negative_informal()
        '食べなかった'
        >>> Verb('わかる', ['godan verb'], [], kanji='分かる').past_negative_informal()
        '分からなかった'
        >>> Verb('よぶ', ['godan verb'], [], kanji='呼ぶ').past_negative_informal()
        '呼ばなかった'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').past_negative_informal()
        '買わなかった'
        >>> Verb('くる', ['kuru verb'], []).past_negative_informal()
        'こなかった'
        >>> Verb('くる', ['kuru verb'], [], kanji='来る').past_negative_informal()
        '来なかった'
        >>> Verb('きく', ['godan verb'], [], kanji='聞く').past_negative_informal()
        '聞かなかった'
        >>> Verb('およぐ', ['godan verb'], [], kanji='泳ぐ').past_negative_informal()
        '泳がなかった'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').past_negative_informal()
        '行かなかった'
        """
        negative = self.negative_informal()
        return negative[:-1] + 'かった'

    def volitional_informal(self):
        """
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').volitional_informal()
        '食べよう'
        >>> Verb('はなす', ['godan verb'], [], kanji='話す').volitional_informal()
        '話そう'
        >>> Verb('しんじる', ['ichidan verb'], [], kanji='信じる').volitional_informal()
        '信じよう'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').volitional_informal()
        '買おう'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').volitional_informal()
        '行こう'
        """
        written = str(self)
        if self.type == 'suru':
            return written[:-2] + 'しよう'
        elif self.type == 'kuru':
            if written[-2:] == '来る':
                return written[:-2] + '来よう'
            else:
                return written[:-2] + 'こよう'
        elif self.type == 'ichidan':
            return written[:-1] + 'よう'
        elif self.type == 'godan':
            return self.conjugate('お') + 'う'
        else:
            raise ConjugationError(self)

    def volitional_formal(self):
        """
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').volitional_formal()
        '食べましょう'
        >>> Verb('はなす', ['godan verb'], [], kanji='話す').volitional_formal()
        '話しましょう'
        >>> Verb('しんじる', ['ichidan verb'], [], kanji='信じる').volitional_formal()
        '信じましょう'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').volitional_formal()
        '買いましょう'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').volitional_formal()
        '行きましょう'
        """
        return self.stem() + 'ましょう'

    def potential_informal(self):
        """
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').potential_informal()
        '食べられる'
        >>> Verb('はなす', ['godan verb'], [], kanji='話す').potential_informal()
        '話せる'
        >>> Verb('しんじる', ['ichidan verb'], [], kanji='信じる').potential_informal()
        '信じられる'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').potential_informal()
        '買える'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').potential_informal()
        '行ける'
        >>> Verb('とる', ['godan verb'], [], kanji='取る').potential_informal()
        '取れる'
        >>> Verb('そんする', ['suru verb'], [], kanji='存する').potential_informal()
        '存出来る'
        >>> Verb('そんする', ['suru verb'], []).potential_informal()
        'そんできる'
        """
        written = str(self)
        has_kanji = any(unicodedata.name(char)[:3] == 'CJK' for char in written)
        if self.type == 'suru':
            if has_kanji:
                return written[:-2] + '出来る'
            else:
                return written[:-2] + 'できる'
        elif self.type == 'kuru':
            if written[-2:] == '来る':
                return written[:-2] + '来られる'
            else:
                return written[:-2] + 'こられる'
        elif self.type == 'ichidan':
            return written[:-1] + 'られる'
        elif self.type == 'godan':
            return self.conjugate('え') + 'る'
        else:
            raise ConjugationError(self)

    def progressive_informal(self):
        """
        >>> Verb('たべる', ['ichidan verb'], [], kanji='食べる').progressive_informal()
        '食べている'
        >>> Verb('はなす', ['godan verb'], [], kanji='話す').progressive_informal()
        '話している'
        >>> Verb('しんじる', ['ichidan verb'], [], kanji='信じる').progressive_informal()
        '信じている'
        >>> Verb('かう', ['godan verb'], [], kanji='買う').progressive_informal()
        '買っている'
        >>> Verb('いく', ['godan verb'], [], kanji='行く').progressive_informal()
        '行っている'
        >>> Verb('とる', ['godan verb'], [], kanji='取る').progressive_informal()
        '取っている'
        >>> Verb('しぬ', ['godan verb'], [], kanji='死ぬ').progressive_informal()
        '死んでいる'
        """
        return self.te_form() + 'いる'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
