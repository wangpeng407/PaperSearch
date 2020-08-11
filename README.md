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

### out files

[out.html](https://github.com/wangpeng407/PaperSearch/blob/master/out.html)

out.list

```
 Pubmed ID: 32019791

title: Influence of Plant Fraction, Soil, and Plant Species on Microbiota: a Multikingdom Comparison [植物组成，土壤和植物物种对微生物群落的影响：多王国比较]

doi: 10.1128/mBio.02785-19

link_url: https://pubmed.ncbi.nlm.nih.gov/32019791/

journal: mBio

date: 02/04/2020

enc_abstract: Plant roots influence the soil microbiota via physical interaction, secretion, and plant immunity. However, it is unclear whether the root fraction or soil is more important in determining the structure of the prokaryotic or eukaryotic community and whether this varies between plant species. Furthermore, the leaf (phyllosphere) and root microbiotas have a large overlap; however, it is unclear whether this results from colonization of the phyllosphere by the root microbiota. Soil, rhizosphere, rhizoplane, and root endosphere prokaryote-, eukaryote-, and fungus-specific microbiotas of four plant species were analyzed with high-throughput sequencing. The strengths of factors controlling microbiota structure were determined using permutational multivariate analysis of variance (PERMANOVA) statistics. The origin of the phyllosphere microbiota was investigated using a soil swap experiment. Global microbial kingdom analysis conducted simultaneously on multiple plants shows that cereals, legumes, and Brassicaceae establish similar prokaryotic and similar eukaryotic communities inside and on the root surface. While the bacterial microbiota is recruited from the surrounding soil, its profile is influenced by the root itself more so than by soil or plant species. However, in contrast, the fungal microbiota is most strongly influenced by soil. This was observed in two different soils and for all plant species examined. Microbiota structure is established within 2 weeks of plant growth in soil and remains stable thereafter. A reciprocal soil swap experiment shows that the phyllosphere is colonized from the soil in which the plant is grown.IMPORTANCE Global microbial kingdom analysis conducted simultaneously on multiple plants shows that cereals, legumes, and Brassicaceae establish similar prokaryotic and similar eukaryotic communities inside and on the root surface. While the bacterial microbiota is recruited from the surrounding soil, its profile is influenced by the root fraction more so than by soil or plant species. However, in contrast, the fungal microbiota is most strongly influenced by soil. This was observed in two different soils and for all plant species examined, indicating conserved adaptation of microbial communities to plants. Microbiota structure is established within 2 weeks of plant growth in soil and remains stable thereafter. We observed a remarkable similarity in the structure of a plant's phyllosphere and root microbiotas and show by reciprocal soil swap experiments that both fractions are colonized from the soil in which the plant is grown. Thus, the phyllosphere is continuously colonized by the soil microbiota.

cn_abstract: 植物根系通过物理相互作用，分泌和植物免疫力影响土壤微生物。但是，尚不清楚根部分或土壤在确定原核或真核群落的结构以及植物物种之间是否有所不同方面是否更为重要。此外，叶（叶层）和根微生物区系有很大的重叠。然而，目前尚不清楚这是否是根系菌群对叶球定植的结果。使用高通量测序分析了四种植物的土壤，根际，根际平面和根内球原核生物，真核生物和真菌特有的微生物群。使用排列多元方差分析（PERMANOVA）统计数据确定控制微生物群结构的因素的强度。使用土壤交换实验研究了叶圈微生物群的起源。同时在多种植物上进行的全球微生物王国分析表明，谷物，豆类和十字花科在根表面内和根表面建立了相似的原核和相似的真核生物群落。虽然细菌微生物群是从周围的土壤中募集的，但其根系受根本身的影响要大于土壤或植物物种的影响。但是，相反，真菌微生物群受土壤的影响最大。在两种不同的土壤以及所检查的所有植物物种中均观察到了这一点。微生物群的结构在植物在土壤中生长的2周内建立，并在此后保持稳定。相互的土壤交换实验表明，叶环是从种植植物的土壤中定植的。重要事项对多种植物同时进行的全球微生物界分析表明，谷物，豆类和十字花科在其内部和外部建立了相似的原核和相似的真核生物群落。根表面。虽然细菌微生物群是从周围的土壤中募集的，但其分布状况受根部分的影响要大于土壤或植物物种的影响。但是，相反，真菌微生物群受土壤的影响最大。在两种不同的土壤中以及所有被检查的植物物种中都观察到了这一点，表明微生物群落对植物的保守适应性。微生物群的结构在植物在土壤中生长的2周内建立，并在此后保持稳定。我们观察到了植物的叶球结构和根微生物区系的显着相似性，并通过相互的土壤交换实验表明，这两个部分都是从植物生长的土壤中定植的。因此，叶环被土壤微生物群不断地定殖。

####################################################################################################
 ```
 
 
