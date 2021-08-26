#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os,re
import logging
import requests
import argparse
import json
from math import *
from termcolor import colored
import urllib
from urllib import request, parse
from bs4 import BeautifulSoup
from retrying import retry
# from googletrans import Translator
from google_trans_new import google_translator
# from translate import Translator

logging.basicConfig(level=logging.ERROR, format='%(asctime)s: %(levelname)s: %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description=
                                    "Version 2.0: Rerieve published paper information from "
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

@retry(stop_max_attempt_number=50,stop_max_delay=5000)
#def translate2(cont):
#    translator = google_translator()
#    translate_text = translator.translate(cont, lang_src='en', lang_tgt='zh-cn')
#    return translate_text
def translate2(data):
	url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
	formData = {
         'i': data, 'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict',
         'client': 'fanyideskweb', 'salt': '1538959984992', 'sign': 'e2fd5830da31a783b6c1f83b522a7d7c',
         'doctype': 'json', 'keyfrom': 'fanyi.web', 'action': 'FY_BY_CLICKBUTTION', 'typoResult': 'false',
     }
	from_data_parse = urllib.parse.urlencode(formData).encode('utf-8')
	response =request.urlopen(url,data=from_data_parse)
	response_str=response.read().decode('utf-8')
	response_dict=json.loads(response_str)
	full_text = [response_dict['translateResult'][0][i]['tgt'] for i in range(0, len(response_dict['translateResult'][0]))]
	return " ".join(full_text)

# def translate(cont):
#     '''translate english into Chinese using google_translator'''
#     translator = Translator(service_urls=['translate.google.cn'])
#     trans_cont = translator.translate(cont, src='en', dest='zh-cn').text
#     return trans_cont

# def translate2(cont):
#     translator= Translator(to_lang="zh")
#     return translator.translate(cont)



def all_paper_infomation(idlists):
    results = {}
    temp_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    for each_id in idlists:
        try:
            results[each_id] = get_each_paper_content(each_id)
        except:
            logging.error('No information about {}, try {}{}'.format(each_id, temp_url, each_id))
    return results

@retry(stop_max_attempt_number=50,stop_max_delay=5000)
def get_each_paper_content(pmid):
    IDresult = {}
    temp_url = 'https://pubmed.ncbi.nlm.nih.gov/' + str(pmid)
    try:
        r = requests.Session().get(temp_url)
        r2 = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
    except Exception as e:
        logging.error('Retrieving {} | {}\n\n'.format(temp_url, e))
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
    t_temp = title.replace('\'', '')
    IDresult['en_title'] = title
    try:
        cn_title = translate2(t_temp)
        IDresult['cn_title'] = cn_title
    except:
        IDresult['cn_title'] = '暂时不能翻译'
    try:
        journal = r2.find('meta', attrs={"name": "citation_journal_title"})['content']
    except:
        journal = 'No journal'
        #IF = get_IF(journal)
    IDresult['journal'] = journal

    try:
        link_url = r2.find('link', attrs={"rel": "canonical"})['href']
    except:
        link_url = 'No link url'
    IDresult['link_url'] = link_url
    try:
        enc_pool = r2.find('div', attrs={"id": "enc-abstract"}).find_all('p')
        enc_abstract1 = "\n".join([str(i.text).replace("\n", "").lstrip()for i in enc_pool])
        enc_abstract = ' '.join(enc_abstract1.split())
        # enc_abstract = str(r2.find('div', attrs={"id": "enc-abstract"}).find('p').text).replace("\n", "").lstrip()
    except:
        enc_abstract = 'No abstract'
    IDresult['enc_abstract'] = enc_abstract
    enc_abstract_temp = enc_abstract.replace('\'', '')
    try:
        cn_abstract = translate2(enc_abstract_temp)
        IDresult['cn_abstract'] = cn_abstract
    except:
        IDresult['cn_abstract'] = "暂时不能翻译"
    return IDresult

@retry(stop_max_attempt_number=50,stop_max_delay=5000)
def get_pmids(terms, maxi, date_sort):
    base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    pmids = []
    global tol_page_num
    for term in terms:
        interm = parse.quote(term.replace(' ', '+')).replace('%2B', '+')
        ds = '&sort=pubdate' if date_sort else ''
        full_url = base_url + '?term=' + interm + ds + '&size=' + str(maxi)
        try:
            r = requests.Session().get(full_url)
            tmp_r = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
            try:
                tol_paper_num = int(re.sub(r',', '', tmp_r.find('span', class_=['value']).text))
                tol_page_num = ceil(tol_paper_num/int(maxi))
            except:
                tol_page_num = 1
        except Exception as e:
            logging.error('e1 when searching {} \n{} | {}\n\n'.format(term, full_url, e))
        try:
            all_url = [full_url + '&page=' + str(i) for i in range(1, tol_page_num+1)]
            for temp_url in all_url:
                rr = requests.Session().get(temp_url)
                r2 = BeautifulSoup(rr.content, "html.parser", from_encoding="utf-8")
                temp_pmid = r2.find('meta', attrs={"name": "uid"})
                temp2_pmid = r2.find_all('a', class_='docsum-title') # keywords for many papers
                if temp_pmid is None and len(temp2_pmid) == 0:
                    logging.warning('No results for {}.\n'.format(term))
                if temp_pmid is not None:
                    pmids.append(temp_pmid['content'])
                else:
                    for i in temp2_pmid:
                        pmids.append(i['data-article-id'])
        except Exception as e:
            logging.error('e2 when searching {} \n{} | {}\n\n'.format(term, temp_url, e))
    return pmids

@retry(stop_max_attempt_number=50,stop_max_delay=5000)
def get_IF(Journal):
    surl = 'https://www.greensci.net/search?kw='
    jurl = surl + parse.quote(Journal.replace(' ', '+')).replace('%2B', '+')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/84.0.4147.105 Safari/537.36'}
    r = requests.Session().get(jurl, headers=headers)
    r4 = BeautifulSoup(r.content, "html.parser", from_encoding="utf-8")
    res = {}
    for t in r4.find_all('ul', class_=['mail-table']):
        cont = t.text.lstrip().rstrip().split('\n\n')
        del (cont[1])
        cont[1] = re.sub(r'^\s+', '\nName\n ', cont[1]).rstrip()
        temp = [re.sub(r'^\s', '', re.sub(r'\s+', ' ', tmp)) for tmp in cont if not re.search(r'\s+$', tmp)]
        res = dict([(i.split(" ")[0], " ".join(i.split(" ")[1:]).lower()) for i in temp])
        if Journal.lower() in res.values():
            return res
    if not res:
        return ' ||| Not finding IF'

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
    sorted_dict = dict(sorted(infs.items(), key=lambda x:x[0], reverse=True))
    for pmid,temp_dict in sorted_dict.items():
        if format_type is None:
            cfprint('Pubmed ID: ' + str(pmid), type=1)
            cfprint('EN_title: ' + temp_dict['en_title'])
            cfprint('CN_title: ' + temp_dict['cn_title'])
            cfprint('doi: ' + temp_dict['doi'])
            cfprint('link_url: ' + temp_dict['link_url'])
            cfprint('journal: ' + temp_dict['journal'])
            cfprint('date: ' + temp_dict['date'])
            cfprint('enc_abstract: ' + temp_dict['enc_abstract'])
            cfprint('cn_abstract: '+ temp_dict['cn_abstract'])
            cfprint('#'*100, type=2)
        else:
            html_cont += '\n<h2>Pubmed_ID: ' + str(pmid) + '</h2>\n'
            html_cont += '\n<h3>' + str(temp_dict['en_title']) + '</h3>\n'
            html_cont += '\n<h3>' + str(temp_dict['cn_title']) + '</h3>\n'
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
        logging.error('Input list not exists or is empty, please check.\n')
        exit()
    iterms = read_list(args.list)
    if args.maxiterm not in [10,20,50,100,200]:
        logging.error('\n-m/--maxiterm must be choose from [10,20,50,100,200]\n')
        exit()
    ids_pool = get_pmids(terms = iterms, maxi=args.maxiterm, date_sort=args.date_sort)
    res = all_paper_infomation(ids_pool)
    #logging.info("\n".join(iterms))
    outtype = 1 if args.outType else None
    print_info(res, format_type=outtype)


if __name__ == '__main__':
    main()
