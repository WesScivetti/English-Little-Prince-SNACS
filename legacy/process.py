"""
Combine annotations from the origin c1, c4, c5 pilot annotations and the later annotations for all
other chapters and produce conllulex for all of them
"""
from collections import defaultdict
from glob import glob
from pprint import pprint
import conllu

import conllulex.conllulex_to_json as clxj
import conllulex.main as clx


def read_conllulex(conllulex_path):
    """
    Parse a 19-column .conllulex file.
    Args:
        conllulex_path: a filepath to a conllulex file
    Returns: A list of `conllu.TokenList` for each sentence.
    `TokenList` is an iterable, and every token is a dictionary keyed by the name
    of its column, lowercased.
    """
    fields = tuple(
        list(conllu.parser.DEFAULT_FIELDS)
        + [
            "smwe",  # 10
            "lexcat",  # 11
            "lexlemma",  # 12
            "ss",  # 13
            "ss2",  # 14
            "wmwe",  # 15
            "wcat",  # 16
            "wlemma",  # 17
            "lextag",  # 18
        ]
    )

    with open(conllulex_path, "r", encoding="utf-8") as f:
        return conllu.parse(f.read(), fields=fields)


def parse_tsv(path):
    with open(path, "r") as f:
        lines = f.read().split("\n")[1:]
    output = []
    for line in lines:
        pieces = line.split("\t")
        if line[0] and line[0][0] == "#":
            output.append({"type": "meta", "line": line})
        elif pieces[0] and pieces[1]:
            output.append(
                {"type": "token", "line": line, "id": pieces[0], "form": pieces[1], "ss": pieces[3], "ss2": pieces[4]}
            )
        else:
            output.append({"type": "blank"})
    return output


def find_sentences(parsed):
    sentences = []
    current = []
    parsed.append({"type": "blank"})

    for item in parsed:
        type = item["type"]
        if type == "blank":
            if len(current) > 0:
                sentences.append(current)
                current = []
        elif type == "token":
            current.append(item)
        else:
            current.append(item)
    return sentences


def find_mwes(sentences):
    indices = []
    for sentence in sentences:
        runs = {}
        for i, token in enumerate(sentence):
            if token["type"] == "token":
                ss = token["ss"].strip()
                if len(ss) > 0 and ss != "_" and sentence[i + 1]["ss"].strip() == "_":
                    run = [i]
                    j = i + 1
                    while sentence[j]["ss"] == "_":
                        run.append(j)
                        j += 1
                    runs[i] = run
        indices.append(runs)
    return indices


def fmt(**kwargs):
    ss = kwargs.get("ss", "_") or "_"
    ss2 = kwargs.get("ss2", "_") or "_"
    if ss != "_" and ss[0] != "`":
        ss = "p." + ss
    if ss2 != "_" and ss2[0] != "`":
        ss2 = "p." + ss2
    return (
        "\t".join(
            [
                kwargs.get("id"),
                kwargs.get("form"),
                kwargs.get("lemma", "_") or "_",
                kwargs.get("upos", "_") or "_",
                kwargs.get("xpos", "_") or "_",
                kwargs.get("feats", "_") or "_",
                kwargs.get("head", "_") or "_",
                kwargs.get("deprel", "_") or "_",
                kwargs.get("deps", "_") or "_",
                kwargs.get("misc", "_") or "_",
                kwargs.get("smwe", "_") or "_",
                kwargs.get("lexcat", "_") or "_",
                kwargs.get("lexlemma", "_") or "_",
                ss,
                ss2,
                kwargs.get("wmwe", "_") or "_",
                kwargs.get("wcat", "_") or "_",
                kwargs.get("wlemma", "_") or "_",
                kwargs.get("lextag", "_") or "_",
            ]
        )
        + "\n"
    )


def format_tsv(path):
    sentences = find_sentences(parse_tsv(path))
    mwe_indices = find_mwes(sentences)
    s = ""
    for sentence, mwes in zip(sentences, mwe_indices):
        i = 0
        mwe_counter = 1
        while i < len(sentence):
            token = sentence[i]
            if token["type"] == "meta":
                s += token["line"] + "\n"
                i += 1
            elif i not in mwes:
                s += fmt(id=token["id"], form=token["form"], smwe="_", lexlemma="_", ss=token["ss"], ss2=token["ss2"])
                i += 1
            else:
                run = mwes[i]
                for mwe_position, j in enumerate(run):
                    token = sentence[j]
                    s += fmt(
                        id=token["id"],
                        form=token["form"],
                        smwe=f"{mwe_counter}:{mwe_position + 1}",
                        lexlemma="_" if mwe_position == 0 else "_",
                        ss=token["ss"] if mwe_position == 0 else "_",
                        ss2=token["ss2"] if mwe_position == 0 else "_",
                    )
                mwe_counter += 1
                i += len(run)
        s += "\n"

    return s


def write_blanked_tsvs():
    paths = glob("raw_tsv/*.tsv")
    for path in paths:
        formatted = format_tsv(path)
        with open(("blanked" + path[7:-4] + ".conllulex"), "w") as f:
            f.write(formatted)


def write_blanked_145():
    paths = glob("raw_145/*.conllulex")
    combined = ""
    for path in paths:
        sents = read_conllulex(path)
        outpath = f"blanked{path[7:]}".replace("annotation-chpt", "").replace(".conllulex", "_ADJ.conllulex")
        with open(outpath, "w") as f:
            for sent in sents:
                del sent.metadata["text"]
                for token in sent:
                    token["upos"] = "_"
                    token["xpos"] = "_"
                    token["head"] = "_"
                    token["deprel"] = "_"
                    token["feats"] = "_"
                    token["misc"] = "_"
                    token["deps"] = "_"
                    token["lexlemma"] = "_"
                ss = sent.serialize()
                f.write(ss)
                combined += ss


def combine_blanked():
    write_blanked_145()
    write_blanked_tsvs()
    with open("prince_en.conllulex", "w") as f1:
        for i in range(1, 28):
            if i in [1, 4, 5]:
                continue
            with open(f"blanked/lpp_{i}_ADJ.conllulex", "r") as f2:
                f1.write(f2.read())


def enrich():
    for i in range(1, 28):
        if i in [1, 4, 5]:
            continue
        out_path = f"enriched/lpp_{i}_ADJ.conllulex"
        clx.enrich.callback(f"blanked/lpp_{i}_ADJ.conllulex", out_path, "prince_en", None)

        # get error report
        include_morph_deps = True
        include_misc = True
        validate_upos_lextag = True
        validate_type = True
        store_conllulex_string = "none"
        override_mwe_render = False
        sentences, errors = clxj._load_sentences(
            "prince_en",
            out_path,
            include_morph_deps,
            include_misc,
            store_conllulex_string,
            lambda x: x,
        )
        clxj._validate_sentences(
            "prince_en", sentences, errors, validate_upos_lextag, validate_type, override_mwe_render
        )

        edict = defaultdict(list)
        for error in errors:
            edict[error["sentence_id"]].append(error)

        sentences = read_conllulex(out_path)
        s_out = ""
        for sentence in sentences:
            for j, error in enumerate(edict[sentence.metadata["sent_id"]]):
                if error["token"]:
                    try:
                        s = f"Tokens {error['token']['toknums']}: "
                    except KeyError as e:
                        s = f"Token {error['token']['#']}: "
                else:
                    s = ""
                s += error["explanation"]
                sentence.metadata[f"{j}_ERROR"] = s
            s_out += sentence.serialize()
        with open(out_path, "w") as f:
            f.write(s_out)


def main():
    combine_blanked()
    enrich()


if __name__ == "__main__":
    main()
