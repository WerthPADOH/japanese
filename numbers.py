import datetime


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
    >>> int_to_kanji(-569)
    'マイナス五百六十九'
    >>> int_to_kanji(-0)
    'ゼロ'
    """
    out = ''
    if i < 0:
        out = 'マイナス'
        i = -i
    if i in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000}:
        return out + number_kanji[i]
    remainder = i
    threshholds = [10**12, 10**8, 10**4, 1000, 100, 10]
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


def translate_time(dt):
    """
    >>> t = datetime.date.fromisoformat('2019-11-06')
    >>> translate_time(t)
    '2019年11月6日'
    >>> s = datetime.datetime.fromisoformat('1788-12-31T05:32:44')
    >>> translate_time(s)
    '1788年12月31日5時32分44秒'
    """
    out = f'{dt.year}年{dt.month}月{dt.day}日'
    try:
        out += f'{dt.hour}時{dt.minute}分{dt.second}秒'
    except AttributeError:
        pass
    return out


if __name__ == '__main__':
    import doctest
    doctest.testmod()
