#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os
import gzip
import argparse

defaults = ["test/input", "ranklib.fv", "test/test.qrel"]

def msgExit(msg="", rc=0):
    print(msg)
    exit(rc)


def execute(input_folder=defaults[0], output_file=defaults[1], qrel_file=defaults[2]):
    out = dict()
    queryset = dict()
    teamset = set()
    for filename in os.listdir(input_folder):
        f = gzip.open(os.path.join(input_folder, filename), "rt")
        for line in f:
            words = line.split()
            teamset.add(words[5])
            out[words[2]] = out.get(words[2], dict())
            out[words[2]][words[0]] = out[words[2]].get(words[0], dict())
            out[words[2]][words[0]][words[5]] = [words[3], words[4], 1]
        f.close()
    f = open(qrel_file, "rt")
    for line in f:
        words = line.split()
        queryset[words[2]] = queryset.get(words[2], [])+[(words[0], words[3])]
    f.close()
    f = open(output_file, "w+")

    for doc in out:
        query_id = 1
        for query in queryset.get(doc, []):
            s = query[1] + " qid:" + str(query_id)+" "
            query_id += 1
            feature_id = 1
            for team in teamset:
                for score in out.get(doc, dict()).get(query[0], dict()).get(team, [0, 0, 0]):
                    s += str(feature_id)+":"+str(score)+" "
                    feature_id += 1
            f.write(s+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Creates a feature vector file (See https://sourceforge.net/p/lemur/wiki/RankLib%20File%20Format/) from run files ')
    parser.add_argument('-i', '--input_folder', default=defaults[0], type=str,
                        help='All files in the directory will be read. Default:'+str(defaults[0]))
    parser.add_argument('-o', '--output_file',
                        default=defaults[1], type=str,  help='Where to write to. Default:'+str(defaults[1]))
    parser.add_argument('-q', '--qrel_file', default=defaults[2], type=str,
                        help='The qrel file needed for the target relevance. Default:'+str(defaults[2]))

    try:  # If you want bash completion take a look at https://pypi.org/project/argcomplete/
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    args = parser.parse_args()
    execute(args.input_folder, args.output_file, args.qrel_file)
