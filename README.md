# Japanese Python package

A set of tools for learning Japanese.

## Modules

### `jisho`

Two classes: `Jisho` for a collection of Japanese words with some lookup
methods, and `Entry` for an individual Japanese word.

### `verbs`

Defines a `Verb` class (subclass of `Entry`) with extra info for how a
verb behaves.
Also has functions for conjugating verbs.

### `numbers`

Has the function `int_to_kanji` which does what's on the label.

### `writing`

Converts between Hiragana and Romanji.

## Sources

When the `jisho.py` module is run, it creates a dictionary that loads
entries from the
[JMdict/EDICT Japanese Dictionary](http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project).
You will need to download the dictionary yourself.
Many thanks to everyone who contributed to that project and shared their
knowledge with the net.
