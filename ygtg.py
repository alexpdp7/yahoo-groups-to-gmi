import email.header
import email.parser
import html
import json
import pathlib
import shutil
import sys
import textwrap

from warcio import archiveiterator


def warc_to_gmi(warc_path, out_path: pathlib.Path):
    shutil.rmtree(out_path, ignore_errors=True)

    index = {}

    with open(warc_path, 'rb') as stream:
        for record in archiveiterator.ArchiveIterator(stream):
            if record.rec_headers["WARC-Target-URI"].endswith("info"):
                continue
            num = record.rec_headers["WARC-Target-URI"].split("/")[-2]
            raw_email = json.loads(record.raw_stream.read())["rawEmail"]
            maildir = out_path / num
            maildir.mkdir(parents=True, exist_ok=True)

            with open(maildir / "mail", "w") as f:
                f.write(raw_email)

            parsed_mail = email.parser.Parser().parsestr(raw_email)
            
            if parsed_mail.get("Subject"):
                subject = ""
                decoded_headers = email.header.decode_header(parsed_mail.get("Subject"))
                for decoded_header in decoded_headers:
                    s, enc = decoded_header
                    subject += s.decode(enc) if enc else str(s)
            else:
                subject = "Unknown"

            date = parsed_mail.get("Date")
            from_ = html.unescape(parsed_mail.get("From"))
            body = parsed_mail.get_payload(decode=True).decode("iso-8859-1")
            body = html.unescape(body)

            with open(maildir / "index.gmi", "w") as f:
                f.write(textwrap.dedent(f"""
                    Date: {date}
                    From: {from_}
                    Subject: {subject}

                    ```
                """))
                f.write(body.strip())
                f.write("\n```\n")

            index[int(num)] = f"=> {num}/ {date} - {from_} - {subject}"

    with open(out_path / "index.gmi", "w") as f:
        for i in range(1, max(index.keys()) + 1):
            if i in index:
                f.write(index[i] + "\n")


def main(argv):
    warc_path = pathlib.Path(argv[1])
    out_path = pathlib.Path(argv[2])

    warc_to_gmi(warc_path, out_path)


if __name__ == "__main__":
    main(sys.argv)