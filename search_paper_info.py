#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import requests
import argparse
from termcolor import colored
from urllib import parse
from bs4 import BeautifulSoup
from retrying import retry
from googletrans import Translator


def parse_args():
    parser = argparse.ArgumentParser(description=
                                    "Version 2.0: Rerieve published paper infomation from " 
                                    "pubmed (https://pubmed.ncbi.nlm.nih.gov/) "
                                    "according to article title or keywords.\n",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--list", type=str, required=True,
                        help="Input list include article title or keywords.\n")

    parser.add_argument('-m', '--maxiterm', type=int, required=False, default=20,
                        help="Max iterms when using keyword, default is 20. You can only choose from 10,20,50,100,200\n")

    parser.add_argument('-t', '--outType', type=int,required=False, default=1,
                        help='Print out format, 0: list, 1: html, default is 1.\n')

    parser.add_argument('-d', '--date_sort', type=int, required=False, default=1,
                        help='Sort articles according to published date. 1: True, 0: False, default is 1.')

    args = parser.parse_args()
    return args

def read_list(infile):
    with open(infile, 'r') as f:
        cont = [i.rstrip() for i in f if not i.startswith('#') and i.rstrip() != '']
    return cont

def translate(cont):
    '''translate english into Chinese using google_translator'''
    translator = Translator(service_urls=['translate.google.cn'])
    return translator.translate(cont, dest='zh-cn').text

def all_paper_infomation(idlists):
    results = {}
    for each_id in idlists:
        results[each_id] = get_each_paper_content(each_id)
    return results

@retry(stop_max_attempt_number=5,stop_max_delay=50)
def get_each_paper_content(pmid):
    IDresult = {}
    temp_url = 'https://pubmed.ncbi.nlm.nih.gov/' + str(pmid)
    try:
        r = requests.Session().get(temp_url)
        r2 = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
    except Exception as e:
        sys.stderr.write('Error occurs when retrieving {} | {}\n\n'.format(temp_url, e))
    # try:
    #     pmid = r2.find('meta', attrs={"name": "uid"})['content']
    # except:
    #     pmid = 'No pmid'
    try:
        date = r2.find('meta', attrs={"name": "citation_date"})['content']
    except:
        date = 'No date'
    IDresult['date'] = date
    try:
        doi = r2.find('meta', attrs={"name": "citation_doi"})['content']
    except:
        doi = 'No doi'
    IDresult['doi'] = doi
    try:
        title = r2.find('meta', attrs={"name": "citation_title"})['content']
    except:
        title = 'No title'
    cn_title = translate(title)
    IDresult['title'] = title + ' [' + cn_title + "]"
    try:
        journal = r2.find('meta', attrs={"name": "citation_publisher"})['content']
    except:
        journal = 'No journal'
    IDresult['journal'] = journal
    try:
        link_url = r2.find('link', attrs={"rel": "canonical"})['href']
    except:
        link_url = 'No link url'
    IDresult['link_url'] = link_url
    try:
        enc_abstract = str(r2.find('div', attrs={"id": "enc-abstract"}).find('p').text).replace("\n", "").lstrip()
    except:
        enc_abstract = 'No abstract'
    IDresult['enc_abstract'] = enc_abstract
    cn_abstract = translate(enc_abstract)
    IDresult['cn_abstract'] = cn_abstract
    return IDresult

@retry(stop_max_attempt_number=5,stop_max_delay=20)
def get_pmids(terms, maxi, date_sort):
    base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    pmids = []
    for term in terms:
        interm = parse.quote(term.replace(' ', '+')).replace('%2B', '+')
        ds = '&sort=pubdate' if date_sort else ''
        full_url = base_url + '?term=' + interm + ds + '&size=' + str(maxi)
        try:
            r = requests.Session().get(full_url)
            r2 = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
            temp_pmid = r2.find('meta', attrs={"name": "uid"})
            temp2_pmid = r2.find_all('a', class_='docsum-title') # keywords for many papers
            if temp_pmid is None and len(temp2_pmid) == 0:
                sys.stderr.write('WARNING: no results for {}.\n'.format(colored(term, 'red')))
            if temp_pmid is not None:
                pmids.append(temp_pmid['content'])
            else:
                for i in temp2_pmid:
                    pmids.append(i['data-article-id'])
        except Exception as e:
            sys.stderr.write('Error occurs when searching {} \n{} | {}\n\n'.format(colored(term, 'cyan'), full_url, e))
    return pmids

def cfprint(text, type = None):
    '''
    print text with color, 1: red; 2: yellow; 3: blue; 4: cyan, else normal print
    '''
    if type == 1:
        print(colored(text, 'red', attrs=['bold']), end='\n\n')
    elif type == 2:
        print(colored(text, 'yellow', attrs=['bold']), end='\n\n')
    elif type == 3:
        print(colored(text, 'blue', attrs=['bold']), end='\n\n')
    elif type == 4:
        print(colored(text, 'cyan', attrs=['bold']), end='\n\n')
    else:
        print(text, end='\n\n')

def print_info(infs, format_type=None):
    '''format_type is none (txt) or html'''
    if not isinstance(infs, dict):
        sys.stderr.write('Data structure may be wrong.')
    html_cont = '<!DOCTYPE html> <html lang = \"en\">\n <body>\n'
    sorted_dict = dict(sorted(infs.items(), key=lambda x:x[0], reverse=False))
    for pmid,temp_dict in sorted_dict.items():
        if format_type is None:
            cfprint('Pubmed ID: ' + str(pmid), type=1)
            cfprint('title: ' + temp_dict['title'])
            cfprint('doi: ' + temp_dict['doi'])
            cfprint('link_url: ' + temp_dict['link_url'])
            cfprint('journal: ' + temp_dict['journal'])
            cfprint('date: ' + temp_dict['date'])
            cfprint('enc_abstract: ' + temp_dict['enc_abstract'])
            cfprint('cn_abstract: '+ temp_dict['cn_abstract'])
            cfprint('#'*100, type=2)
        else:
            html_cont += '\n<h2>' + str(pmid) + ": " + str(temp_dict['title']) + '</h2>\n'
            html_cont += '\n<p style=\"margin:20px\"> <font face="arial"> <b>DOI: ' + \
                         str(temp_dict['doi']) + '</b> </font> </P>\n'
            html_cont += '\n<p style=\"margin:20px\"> <font face="arial" <b>URL: ' + \
                         str(temp_dict['link_url']) + '</b> </font> </P>\n'
            html_cont += '\n<p style=\"margin:20px\"> <font face="arial" color=\"blue\"> <b>Journal: ' + \
                         str(temp_dict['journal']) + '</b> </font> </P>\n'
            html_cont += '\n<p style=\"margin:20px\"> <font face="arial" color=\"blue\"> <b> Date: ' + \
                         str(temp_dict['date']) + '</b> </font> </p>\n'
            html_cont += '\n<p style=\"line-height:1.8;margin:20px\"> Abstract: ' + \
                         str(temp_dict['enc_abstract']) + '</p>\n'
            abs_ch = temp_dict['cn_abstract']
            html_cont += '\n<p style=\"line-height:1.8;margin:20px\"> 摘要: ' + \
                         str(abs_ch).replace(' ', '') + '</p>\n'
    html_cont += '\n' + '</body>\n</html>\n'
    if format_type is not None:
        print(html_cont)

def main():
    args = parse_args()
    if not os.path.isfile(args.list):
        sys.exit('\nError: input list not exists or is empty, please check.\n')
    iterms = read_list(args.list)
    if args.maxiterm not in [10,20,50,100,200]:
        sys.exit('\nError: -m/--maxiterm must be choose from [10,20,50,100,200]\n')
    ids_pool = get_pmids(terms = iterms, maxi=args.maxiterm, date_sort=args.date_sort)
    res = all_paper_infomation(ids_pool)
    print("\n".join(iterms), end="\n\n")
    outtype = 1 if args.outType else None
    print_info(res, format_type=outtype)

if __name__ == '__main__':
    main()

