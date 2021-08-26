## Quikly scanning newest papers retrieved from [pubmed](https://pubmed.ncbi.nlm.nih.gov/)

### Help
```
python search_paper_info.py -h
usage: search_paper_info.py [-h] -l LIST [-m MAXITERM] [-t OUTTYPE]
                            [-d DATE_SORT]

Version 2.0: Rerieve published paper infomation from pubmed (https://pubmed.ncbi.nlm.nih.gov/) according to article title or keywords.

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  Input list include article title or keywords.
  -m MAXITERM, --maxiterm MAXITERM
                        Max iterms when using keyword, default is 20. You can only choose from 10,20,50,100,200
  -t OUTTYPE, --outType OUTTYPE
                        Print out format, 0: list, 1: html, default is 1.
  -d DATE_SORT, --date_sort DATE_SORT
                        Sort articles according to published date. 1: True, 0: False, default is 1.

```

### Example
```
python search_paper_info.py -l plist -m 10 -t 1 -d 1 > out.html
python search_paper_info.py -l plist -m 10 -t 0 -d 1 > out.list
```

### Example outfile

see [here](https://github.com/wangpeng407/berry_papers)

