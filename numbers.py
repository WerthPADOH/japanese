number_kanji = {
    0: 'ゼロ',
    1: '一',
    2: '二',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '七',
    8: '八',
    9: '九',
    10: '十',
    100: '百',
    1000: '千',
    10**4: '万',
    10**8: '億',
    10**12: '兆'
    }


def int_to_kanji(i: int):
    """
    >>> int_to_kanji(1)
    '一'
    >>> int_to_kanji(36)
    '三十六'
    >>> int_to_kanji(999)
    '九百九十九'
    >>> int_to_kanji(8002)
    '八千二'
    >>> int_to_kanji(1234567890)
    '十二億三千四百五十六万七千八百九十'
    >>> int_to_kanji(10**8)
    '一億'
    """
    if i in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000}:
        return number_kanji[i]
    remainder = i
    threshholds = [10**12, 10**8, 10**4, 1000, 100, 10]
    out = ''
    for n in threshholds:
        factor, remainder = divmod(remainder, n)
        if factor:
            if factor == 1 and n in {10, 100, 1000}:
                out += number_kanji[n]
            else:
                out += int_to_kanji(factor) + number_kanji[n]
        if not remainder:
            break
    if remainder:
        out += number_kanji[remainder]
    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod()
