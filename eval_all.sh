cd stanford-corenlp
java -cp stanford-corenlp-3.2.0.jar:stanford-corenlp-3.2.0-models.jar:xom.jar:joda-time.jar:jollyday.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -filelist papers
cd ..
sh eval_co.sh
sh eval_pr.sh
sh eval_overlap.sh
cd eval
sh eval.sh