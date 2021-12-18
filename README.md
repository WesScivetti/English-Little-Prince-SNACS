# English-Little-Prince-SNACS
English Little Prince hand-annotated with prepositional supersenses ([SNACS](https://arxiv.org/abs/1704.02134), guidelines v2.5)

Each sentence is annotated with: syntactic parses (Universal Dependencies); multiword expressions involving prepositions/possessives; and supersense labels for prepositional/possessive expressions. The syntactic parses are automatic, produced by the Stanza parser (a few were hand-corrected).

The canonical data file is in the [CoNLL-U-Lex format](https://github.com/nert-nlp/streusle/blob/v4.4/CONLLULEX.md). 
JSON-converted data files are included for easy programmatic access.

Notes about the data:
- Sentence IDs are borrowed from the [AMR release](https://amr.isi.edu/download.html)
- The `# text = ...` field is derived from tokens and does not reflect original whitespace
- Chapters 1, 4, and 5 are currently missing (they were annotated as a pilot under an earlier version of the SNACS annotation scheme)
- Syntactic parses, POS tags, morphological features, and lemmas are from Stanza version 1.3.0
