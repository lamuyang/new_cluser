from collections import Counter
from numpy import RankWarning
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import math
from sklearn.preprocessing import normalize
import fuction.pkl_input,fuction.get_data

name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = fuction.get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = fuction.get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

def get_all_list(old_list):
    new_list = []
    for i in old_list:
        for j in i:
            new_list.append(j)
    return new_list
def collect_all_blank_word(raw_list):
    new_list = []
    for i in raw_list:
        new_list.append(" ".join(i))
    return new_list
def tf_idf(new_min_df=1,new_token_pattern="\\b\\w+\\b",new_stop_words = [],corpus=[]):
    vectoerizer = CountVectorizer(min_df=new_min_df, token_pattern=new_token_pattern,stop_words=new_stop_words)
    tfidf_transformer = TfidfTransformer()
    tfidf = tfidf_transformer.fit_transform(vectoerizer.fit_transform(corpus))
    word = vectoerizer.get_feature_names()
    weight = tfidf.toarray()
    return word, weight
def print_result(word,weight):
    new_list = []
    for i in range(len(weight)):
        print(f"{i}項")
        tem_list = {}
        for j in range(len(word)):
            if weight[i][j] != 0.0 :
                print(word[j],weight[i][j])
                tem_list[word[j]]=weight[i][j]
        new_list.append(tem_list)
    return new_list
def write_tfidf_result(raw_list,blank_list,old_list,tf_idf_list,filename):
    with open(filename,"w") as fileobj:
        for i in range(0,len(old_list)):
            fileobj.write(f"{raw_list[i]}\n") 
            fileobj.write(blank_list[i])
            fileobj.write("\n")
            for j in old_list[i]:
                z = j.lower()  
                try:
                    temp = f"{j} {tf_idf_list[i][z]}"
                except KeyError:
                    temp = f"{j} Null"
                print(temp,end=" ")
                fileobj.write(f"{temp} ")
            temp = sorted(tf_idf_list[i].items(), key=lambda d: d[1], reverse=True) 
            fileobj.write(f"\n{temp}\n")
            fileobj.write("==================\n")
name = fuction.pkl_input.open_pkl("PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_name.pkl")
all_title = get_all_list(name)
name_stopwords = ["探討","分析","內","日","期"]
all_blank_title = collect_all_blank_word(name)
title_word,title_weight = tf_idf(new_stop_words=name_stopwords,corpus=all_blank_title)
title_tfidf_list = print_result(title_word,title_weight)

write_tfidf_result(raw_name,all_blank_title,name,title_tfidf_list,"tfidf_name.txt")

# abstract = fuction.pkl_input.open_pkl("PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_abstract.pkl")
# all_abstract = get_all_list(abstract)
# all_blank_abstract = collect_all_blank_word(abstract)
# abstract_stopwords = ["研究","本","為","各","有","其","者","法","高"]
# abstract_word,abstract_weight = tf_idf(new_stop_words=abstract_stopwords,corpus=all_blank_abstract)
# abstract_tfidf_list = print_result(abstract_word,abstract_weight)

# write_tfidf_result(raw_abstract,all_blank_abstract,abstract,abstract_tfidf_list,"tfidf_abstract.txt")

# reference = fuction.pkl_input.open_pkl("PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_reference.pkl")
# all_reference = get_all_list(reference)
# all_blank_reference = collect_all_blank_word(reference)
# reference_stopwords = ["研究","民","頁","”","出版","期","日","為","例","學","版","社","“"]
# reference_word,reference_weight = tf_idf(new_stop_words=reference_stopwords,corpus=all_blank_reference)
# reference_tfidf_list = print_result(reference_word,reference_weight)

# write_tfidf_result(raw_reference,all_blank_reference,reference,reference_tfidf_list,"tfidf_reference.txt")