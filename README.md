# English-Little-Prince-SNACS

_The Little Prince_ in English hand-annotated with prepositional supersenses ([SNACS](https://arxiv.org/abs/1704.02134), guidelines v2.6)

_Le Petit Prince_ by Antoine de Saint-Exupéry was originally translated into English in 1943 by Katherine Woods. Our dataset uses this translation and follows the sentence segmentation of the [AMR project](https://github.com/flipz357/AMR-World/tree/main/data/reference_amrs).

Each sentence is annotated with: syntactic parses (Universal Dependencies); multiword expressions involving prepositions/possessives; and supersense labels for prepositional/possessive expressions. The syntactic parses are automatic, produced by the Stanza parser (a few were hand-corrected).

The canonical data file is in the [CoNLL-U-Lex format](https://github.com/nert-nlp/streusle/blob/v4.4/CONLLULEX.md). 
JSON-converted data files are included for easy programmatic access. The gov_obj annotations are generated via the govobj.py script in the [struesle](https://github.com/nert-nlp/streusle/blob/master/govobj.py) repo.

Notes about the data:
- en_lpp_full.conllulex and en_lpp_full_govobj.json are the most up to date files
- older versions of the data can be found in the legacy folder
- The `# text = ...` field is derived from tokens and does not reflect original whitespace
- Syntactic parses, POS tags, morphological features, and lemmas are from Stanza version 1.10.1


# Changelog

- **Version 1.0**: 
    - Updated parses with latest version of Stanza (1.10.1)
    - Added Chapters 1,4 and 5 with gold SNACS annotations
    - Updated all chapters to SNACS guidelines v2.6
    - Corrected some gold MWE spans from all chapters
    - Added latest conllulex file (en_lpp_full.conllulex)
    - Added latest json file with govobj annotations (en_lpp_full_govobj.json)
    - Moved older files into legacy folder

- **Version 0.9**:
    - Release all LPP chapters except 1,4 and 5
    - SNACS guidelines v2.5s
