import json

from ftfy import fix_text

with open("data/json/month_utterances.json", "r") as infile:
    month_utterances = json.load(infile)


def clean_strng(strng):
    replacers = "()[]<>,.!-&#:;@?+*=\"/0"
    strng = strng.lower()
    strng = strng.replace("=laughs", "")
    strng = strng.replace("xxx", "")
    strng = strng.replace("_", " ")
    for replacer in replacers:
        strng = strng.replace(replacer, "")
    strng = strng.split()
    strng = [fix_text(e) for e in strng]
    strng = [e for e in strng if not e.isnumeric()]
    strng = " ".join(strng)
    return strng


month_cleaned = {}
for k,v in month_utterances.items():
    utterances = []
    for u in v:
        u = clean_strng(u)
        if len(u) > 1:
            utterances.append(u)
    month_cleaned[k] = utterances

with open("data/json/clean.json", "w") as outfile:
    json.dump(month_cleaned, outfile)
