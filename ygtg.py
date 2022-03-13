import json
import sys

from warcio import archiveiterator


def warc_to_gmi(warc_path, out_path):
    with open(warc_path, 'rb') as stream:
        for record in archiveiterator.ArchiveIterator(stream):
            if record.rec_headers["WARC-Target-URI"].endswith("info"):
                continue
            print(json.loads(record.raw_stream.read())["rawEmail"])


def main(argv):
    warc_path = argv[1]
    out_path = argv[2]

    warc_to_gmi(warc_path, out_path)


if __name__ == "__main__":
    main(sys.argv)