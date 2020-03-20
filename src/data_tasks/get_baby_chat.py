import json
from os import listdir
from os.path import isdir, isfile, join

in_path = "data/raw"
corpora_dirs = [d for d in listdir(in_path) if isdir(join(in_path, d))]


def cha_reader(cha):
    with open(cha, "r") as infile:
        strng = infile.read().split("\n")
    month = [e for e in strng if e.startswith("@ID") and "CHI" in e][
        0].split("\t")[1].split("|")[3]
    chi_utterances = [e for e in strng if e.startswith("*CHI:")]
    chi_utterances = [e.split("\t")[1] for e in chi_utterances]

    month = month.split(".")[0]
    year, month = month.split(";")
    m_y = int(year) * 12
    total_month = m_y + int(month)
    return total_month, chi_utterances


month_utterances = {}
for subcorpus in corpora_dirs:
    speaker_dirs = [
        d
        for d in listdir(join(in_path, subcorpus))
        if isdir(join(in_path, subcorpus, d))
    ]
    if len(speaker_dirs) > 0:
        for d in speaker_dirs:
            try:
                chas = [
                    join(in_path, subcorpus, d, f)
                    for f in listdir(join(in_path, subcorpus, d))
                    if isfile(join(in_path, subcorpus, d, f))
                ]
                chas = [f for f in chas if f.endswith(".cha")]
            except Exception as e:
                print(e)
                continue
    else:
        chas = [
            join(in_path, subcorpus, f)
            for f in listdir(join(in_path, subcorpus))
            if isfile(join(in_path, subcorpus, f))
        ]
        chas = [f for f in chas if f.endswith(".cha")]
    for cha in chas:
        try:
            mm, ut = cha_reader(cha)
            if mm not in month_utterances.keys():
                month_utterances[mm] = ut
            else:
                month_utterances[mm].extend(ut)
        except Exception as e:
            print(e)
            continue

with open("data/json/month_utterances.json", "w") as outfile:
    json.dump(month_utterances, outfile)
