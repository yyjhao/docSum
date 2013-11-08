# ./ROUGE-1.5.5.pl -d -U -s -e data -n 4 -z SPL paper.spl.lst
./ROUGE-1.5.5.pl -d -s -e data -n 4 -z SPL papers_coref.lst | tee coref.result
./ROUGE-1.5.5.pl -d -s -e data -n 4 -z SPL papers_pageRank.lst | tee pageRank.result
./ROUGE-1.5.5.pl -d -s -e data -n 4 -z SPL papers_overlap.lst | tee overlap.result
