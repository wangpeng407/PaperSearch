#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import argparse
from Bio import Entrez
from googletrans import Translator
from termcolor import colored


def parse_args():
    parser = argparse.ArgumentParser(description="Rerieve published paper infomation from "
                                                 "pubmed (https://pubmed.ncbi.nlm.nih.gov/) "
                                                 "according to article title or keywords.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--list", type=str, required=True,
                        help="input list include article title or keywords")
    parser.add_argument('-m', '--maxiterm', type=int, required=False, default=20,
                        help="Max iterms when using esearch function, default is 20")
    args = parser.parse_args()
    return args


def read_list(infile):
    with open(infile, 'r') as f:
        cont = [i.rstrip() for i in f if not i.startswith('#')]
    return cont

def multi_try(func):
    '''
    try to run a function 10 times
    '''
    def wrapper(*args, **kargs):
        times = 0
        N = 10
        while times <= N:
            try:
                #if function running correctly, return it, or throw  exception and try again
                f = func(*args, **kargs)
                # print('test running {} {}'.format(func.__name__, times))
                return f
            except Exception:
                times += 1
                sys.stderr.write('Error occurs when running {}: {}\n'.format(func.__name__, times))
        # if tried times exceed the setting N, then exit.
        if times > N:
            sys.exit('Please try another {} times, when running {}\n'.format(N, func.__name__))
    return wrapper

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

def translate(cont):
    '''translate english into Chinese using google_translator'''
    translator = Translator(service_urls=['translate.google.cn'])
    return translator.translate(cont, dest='zh-cn').text

@multi_try
def get_idlist(Pnames, maxiterm=20):
    '''getting pubmed id according to keywords or article title, then store in a list'''
    Entrez.email = "m18747115215@163.com"
    pubmedIDs = []
    for n in Pnames:
        ids = Entrez.read(Entrez.esearch(db="pubmed", retmax=maxiterm, term=n))['IdList']
        if ids:
            pubmedIDs.extend(ids)
        else:
            sys.stderr.write('Error: Not searching pubmed id of {}.\n'.format(n))
    return pubmedIDs


@multi_try
def retrieve_article_info(idlist):
    '''
    efech article infomation from pubmed IDs, and process the complex data structure
    '''
    # try:
    xml_handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="xml")
    record = Entrez.read(xml_handle)['PubmedArticle']
    # except Exception:
    #     sys.exit('Error occurs when efeching idList.\n')
    # cfprint(record, type=1)
    result_pool = {}
    for each_rcd in record:
        rcd2 = each_rcd['MedlineCitation']
        #pubmed ID
        try:
            pmid = rcd2['PMID']
        except:
            pmid = 'No pmid found.'
        if pmid not in result_pool:
            result_pool[pmid] = {}
        #keywords
        try:
            keywords = "; ".join([str(rcd2['KeywordList'][0][i]) for i in range(0, len(rcd2['KeywordList'][0]))]) if 'KeywordList' in rcd2 else 'NONE'
        except:
            keywords = 'No keywords'
        result_pool[pmid]['Keywords'] = keywords

        if 'Article' in rcd2:
            article_info = rcd2['Article']
        else:
            sys.stderr.write('Error occurs when finding article {}, and escape it.\n'.format(pmid))
            continue
        # published date
        try:
            article_date = '-'.join([article_info['Journal']['JournalIssue']['PubDate']['Year'],
                                    article_info['Journal']['JournalIssue']['PubDate']['Month']])
        except:
            article_date = 'No article date'
        result_pool[pmid]['Date'] = article_date
        # article title
        try:
            article_title = article_info['ArticleTitle']
        except:
            article_title = 'No article title'
        result_pool[pmid]['Title'] = article_title
        # authors and affiliations
        try:
            authorlist = article_info['AuthorList'] if 'AuthorList' in article_info else 'NONE'

            au_info = dict([(authorlist[i]['LastName'] + " " + authorlist[i]['ForeName'],
                            authorlist[i]['AffiliationInfo'][0]['Affiliation']) for i in range(0, len(authorlist))])
        except:
            au_info = {'NONE':'No affiliation'}
        result_pool[pmid]['Authors'] = au_info
        #Journal name
        try:
            journal_name = article_info['Journal']['Title'] + ' (' + \
                           article_info['Journal']['ISOAbbreviation'] + ')' \
                if 'Journal' in article_info else 'NONE'
        except:
            journal_name = 'No journal name'
        result_pool[pmid]['Journal'] = journal_name
        # exctract abstract text and translating
        try:
            abstract_text = " ".join([article_info['Abstract']['AbstractText'][i] \
                                    for i in range(0, len(article_info['Abstract']['AbstractText']))]) \
            if 'Abstract' in article_info else 'NONE'
        except:
            abstract_text = 'No abstract'
        result_pool[pmid]['Abstract_EN'] = abstract_text
        ch_abstract = translate(abstract_text)
        result_pool[pmid]['Abstract_CN'] = ch_abstract

    return result_pool

# #pmid | Keywords, Date, Title, Authors, Journal, Abstract_EN, Abstract_CN

def print_info(infs):
    if not isinstance(infs, dict):
        sys.stderr.write('Data structure may be wrong.')
    for pmid,temp_dict in infs.items():
        cfprint('Pubmed ID: ' + str(pmid), type=1)
        cfprint('Title: ' + temp_dict['Title'])
        cfprint('Journal: ' + temp_dict['Journal'])
        cfprint('Date: ' + temp_dict['Date'])
        cfprint('Abstrct_EN: ' + temp_dict['Abstract_EN'])
        cfprint('Abstrct_CN: '+ temp_dict['Abstract_CN'])
        cfprint('#'*100, type=2)

def main():
    args = parse_args()
    if not os.path.isfile(args.list):
        sys.exit('Input list not exists or is empty, please check.\n')
    plist = read_list(args.list)
    idLists = get_idlist(plist, args.maxiterm)
    cfprint('#All pubmed ids: {}'.format(", ".join(idLists)), type=2)
    papers_info = retrieve_article_info(idLists)
    print_info(papers_info)

if __name__ == '__main__':
    main()
