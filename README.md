Converts Yahoo Groups warc files (see https://datahorde.org/how-to-recover-your-yahoo-groups-from-the-internet-archive/ ) to Gemini-servable files.

```
$ python ygtg.py .../path/to/yahoogroup.warc output_dir
```

Dumps the emails in `yahoogroup.warc` to `output_dir`.

`output_dir/n/mail` contains the raw email and `output_dir/n/index.gmi` contains a Gemini version.
