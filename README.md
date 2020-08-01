## Quikly scanning newest papers retrieved from [pubmed](https://pubmed.ncbi.nlm.nih.gov/)

### help
```
usage: search_paper_info.py [-h] -l LIST [-m MAXITERM] [-t OUTTYPE]

Rerieve published paper infomation from pubmed (https://pubmed.ncbi.nlm.nih.gov/) according to article title or keywords.

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  Input list include article title or keywords
  -m MAXITERM, --maxiterm MAXITERM
                        Max iterms when using esearch function, default is 20
  -t OUTTYPE, --outType OUTTYPE
                        Print out format, 0: list, 1: html
                        
```

### Example
```
python search_paper_info.py -l plist -m 5 -t 1 > out.html
python search_paper_info.py -l plist -m 5 -t 0 > out.list
```

### out files

(out.html)[https://github.com/wangpeng407/PaperSearch/edit/master/out.html]

 out.list
 ```
 Pubmed ID: 32703911

Title: Can Dietary Fatty Acids Affect the COVID-19 Infection Outcome in Vulnerable Populations?

Authors: Häggblom M M; Onishi J C; Shapses S A

Journal: mBio (mBio)

Date: 2020-07

Abstrct_EN: There is high mortality in coronavirus disease 2019 (COVID-19)-infected individuals with chronic inflammatory diseases, like obesity, diabetes, and hypertension. A cytokine storm in some patients after infection contributes to this mortality. In addition to lungs, the intestine is targeted during COVID-19 infection. The intestinal membrane serves as a barrier to prevent leakage of microorganisms and their products into the bloodstream; however, dietary fats can affect the gut microbiome and may increase intestinal permeability. In obese or diabetic individuals, there is an increase in the abundance of either Gram-negative bacteria in the gut or their product, endotoxin, in systemic circulation. We speculate that when the COVID-19 infection localizes in the intestine and when the permeability properties of the intestinal membrane are compromised, an inflammatory response is generated when proinflammatory endotoxin, produced by resident Gram-negative bacteria, leaks into the systemic circulation. This review discusses conditions contributing to inflammation that are triggered by microbially derived factors from the gut.

Abstrct_CN: 冠状病毒疾病2019（COVID-19）感染的慢性炎症性疾病（如肥胖症，糖尿病和高血压）的死亡率很高。感染后某些患者的细胞因子风暴可导致这种死亡。除肺外，在COVID-19感染期间还以肠道为目标。肠膜是防止微生物及其产物渗入血液的屏障。然而，膳食脂肪会影响肠道微生物组，并可能增加肠道通透性。在肥胖或糖尿病个体中，肠道中革兰氏阴性细菌或其产物内毒素在系统循环中的丰度增加。我们推测，当COVID-19感染位于肠道内，并且当肠膜的通透性受到损害时，当驻留的革兰氏阴性细菌产生的促炎性内毒素泄漏到体循环中时，就会产生炎症反应。这篇综述讨论了由肠道中微生物衍生的因素触发的促发炎症的疾病。

####################################################################################################
 ```
 
 
