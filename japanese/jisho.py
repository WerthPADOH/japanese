"""Use the JMdict/EDICT Japanese dictionary

Downloaded from:
    http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project

Papers relating to project:
    http://www.edrdg.org/~jwb/papers.html
"""
import collections
import os
import re
from dataclasses import dataclass
from xml.etree import ElementTree


_code_values = dict()
_dict_file = os.path.join(os.path.dirname(__file__), 'JMdict_e.xml')


def decode_chars(text):
    codes = set(re.findall(r'&#\d+;', text))
    new_codes = codes - set(_code_values.keys())
    for nc in new_codes:
        _code_values[nc] = chr(int(nc[2:-1]))
    for cd in codes:
        text = text.replace(cd, _code_values[cd])
    return text


@dataclass
class Prevalence:
    news: int = None
    ichimango: int = None
    loanword: int = None
    special: int = None
    top_n: int = None

    @classmethod
    def from_nodes(cls, nodes):
        out = cls()
        if not nodes:
            return out
        node_values = (n.text for n in nodes)
        for nv in node_values:
            if nv.startswith('news'):
                out.news = int(nv[4:])
            elif nv.startswith('ichi'):
                out.ichimango = int(nv[4:])
            elif nv.startswith('gai'):
                out.ichimango = int(nv[3:])
            elif nv.startswith('spec'):
                out.special = int(nv[4:])
            elif nv.startswith('nf'):
                out.top_n = 500 * int(nv[2:])
        return out


@dataclass
class Entry:
    reading: str
    parts_of_speech: tuple
    meanings: tuple
    kanji: str = ''
    kanji_alternates: tuple = tuple()
    prevalence: Prevalence = Prevalence()

    @classmethod
    def from_node(cls, node):
        read_node = node.find('r_ele')
        reading = decode_chars(read_node.find('reb').text)
        sense_node = node.find('sense')
        parts_of_speech = tuple(
            decode_chars(n.text).lower().replace('`', '\'')
            for n in sense_node.findall('pos')
            )
        gloss_nodes = sense_node.findall('gloss')
        lang_attr = '{http://www.w3.org/XML/1998/namespace}lang'
        meanings = tuple(
            decode_chars(n.text) for n in gloss_nodes
            if n.attrib[lang_attr].startswith('en')
            )
        entry = cls(
            reading=reading,
            parts_of_speech=parts_of_speech,
            meanings=meanings
            )
        kanji_nodes = node.findall('k_ele')
        if kanji_nodes:
            entry.kanji = decode_chars(kanji_nodes[0].find('keb').text)
            entry.kanji_alternates = tuple(
                decode_chars(n.find('keb').text) for n in kanji_nodes[1:]
                )
            prev_nodes = kanji_nodes[0].findall('ke_pri')
            entry.prevalence = Prevalence.from_nodes(prev_nodes)
        else:
            prev_nodes = read_node.findall('reb/re_pri')
            entry.prevalence = Prevalence.from_nodes(prev_nodes)
        return entry

    def __hash__(self):
        return hash(self.reading + ''.join(m for m in self.meanings))

    def __str__(self):
        if self.kanji:
            return self.kanji
        return self.reading

    def is_part_of_speech(self, pos: str):
        """Determine if a word is a specified part of speech"""
        keyword = pos.lower()
        for p in self.parts_of_speech:
            if keyword in p:
                return True
        return False


class Jisho(collections.abc.MutableSet):
    def __init__(self, entries):
        self._entries = set()
        self._by_kanji = collections.defaultdict(set)
        self._by_reading = collections.defaultdict(set)
        self._by_part_of_speech = collections.defaultdict(set)
        self.parts_of_speech = set()
        for e in entries:
            self.add(e)

    def __contains__(self, x):
        return x in self._entries

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)

    def add(self, x):
        self._entries.add(x)
        self._by_reading[x.reading].add(x)
        for pos in x.parts_of_speech:
            self._by_part_of_speech[pos].add(x)
            self.parts_of_speech.add(pos)
        if x.kanji:
            self._by_kanji[x.kanji].add(x)

    def discard(self, x):
        self._by_reading[x.reading].discard(x)
        for pos in x.parts_of_speech:
            self._by_part_of_speech[pos].discard(x)
        if x.kanji:
            self._by_kanji[x.kanji].discard(x)

    def lookup_part_of_speech(self, phrase: str):
        phrase = phrase.lower()
        matches = set()
        for pos, entries in self._by_part_of_speech.items():
            if phrase in pos:
                matches.update(entries)
        return matches

    def lookup_reading(self, reading: str):
        reading = reading.lower()
        return self._by_reading.get(reading, set())

    def lookup_kanji(self, kanji: str):
        kanji = kanji.lower()
        return self._by_kanji.get(kanji, set())


def create_dictionary():
    tree = ElementTree.parse(_dict_file)
    return Jisho(Entry.from_node(node) for node in tree.getroot())

if __name__ == '__main__':
    dictionary = create_dictionary()
