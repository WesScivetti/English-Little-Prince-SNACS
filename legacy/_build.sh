cat legacy/enriched/*.conllulex > prince_en_without_1_4_5.conllulex
conllulex2json -c prince_en prince_en_without_1_4_5.conllulex prince_en_without_1_4_5.json
conllulex-govobj --no-edeps prince_en_without_1_4_5.json prince_en_without_1_4_5.govobj.json
