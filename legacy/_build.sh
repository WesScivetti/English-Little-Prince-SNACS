cat legacy/enriched/*_{2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27}_*.conllulex > prince_en_without_1_4_5.conllulex
conllulex2json -c prince_en prince_en_without_1_4_5.conllulex prince_en_without_1_4_5.json
conllulex-govobj --no-edeps prince_en_without_1_4_5.json prince_en_without_1_4_5.govobj.json
