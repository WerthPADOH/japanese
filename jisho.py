"""Use the JMdict/EDICT Japanese dictionary

Downloaded from:
    http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project

Papers relating to project:
    http://www.edrdg.org/~jwb/papers.html
"""
import re
from dataclasses import dataclass
from xml.etree import ElementTree


_code_values = dict()


def decode_chars(text):
    
    codes = set(re.findall(r'&#\d+;', text))
    new_codes = codes - set(_code_values.keys())
    for nc in new_codes:
        _code_values[nc] = chr(int(nc[2:-1]))
    for cd in codes:
        text = text.replace(cd, _code_values[cd])
    return text


@dataclass
class Entry:
    reading: str
    parts_of_speech: tuple
    meanings: tuple
    kanji: str = ''
    kanji_alternates: tuple = tuple()
    prev_level: int = None
    prev_class: str = ''
    freq_rank: int = None

    @classmethod
    def from_node(cls, node):
        read_node = node.find('r_ele')
        reading = decode_chars(read_node.find('reb').text)
        sense_node = node.find('sense')
        parts_of_speech = tuple(
            decode_chars(n.text) for n in sense_node.findall('pos')
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
            prev_node = kanji_nodes[0].find('ke_pri')
            if prev_node is not None:
                entry.prev_level = int(prev_node.text[-1])
                entry.prev_class = prev_node.text[:-1]
        return entry


tree = ElementTree.parse('JMdict_e.xml')
jisho = [Entry.from_node(node) for node in tree.getroot()]


def _print_entry(node):
    text = ElementTree.tostring(node).decode()
    print(decode_chars(text))
