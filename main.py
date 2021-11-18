import os,re,pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import fuction.get_data,fuction.pkl_input
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER


part_of_sentance = ["A","Na","Nc","Ncd","Nb","Nep","Neqa","Neqb","Nes","Nh","Nv","VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2","FW"]
part_of_sentance_for_reference = ["A","Na","Nc","Ncd","Nb","Nep","Neqa","Neqb","Nes","Nh","Nv","VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2"]

def remove_punctuation(line):
    rule = re.compile("[^a-zA-Z0-9\\u4e00-\\u9fa5]")
    line = rule.sub(' ',line)
    return line
def remove_number(line):
    rule = re.compile('[0-9]+')
    line = rule.sub(' ',line)
    return line
def remove_space(line):
    while "  " in line:
        rule = re.compile('  ')
        line = rule.sub(' ',line)
    return line

def ws_to_list(list,pkl_name,r_dic = {},force_dic = {}):
    new_list = []
    for i in list:
        i = i.replace('\n', '').replace('\r', '')
        new_list.append(i)
    os.environ["CUDA_VISIBLE_DEVICES"] = "0" 
    ws = WS("./data", disable_cuda=False)
    ner = NER("./data", disable_cuda=False)
    r_dic = construct_dictionary(r_dic)
    force_dic = construct_dictionary(force_dic)
    word_sentence_list = ws(
        new_list,
        sentence_segmentation = True, # To consider delimiters
        segment_delimiter_set = {",", "。", ":", "?", "!", ";","-","──","》","《","\\n",'民', '年', '月', '頁','日'," "},
        recommend_dictionary = r_dic,
        coerce_dictionary = force_dic,
    )
    del ws,ner
    with open(pkl_name, 'wb') as fp:
        pickle.dump(word_sentence_list, fp)
    print("WS done")
    return word_sentence_list

def pos_to_list(word_sentence_list,pkl_name):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    pos = POS("./data", disable_cuda=False)
    pos_sentence_list = pos(word_sentence_list)
    del pos
    with open(pkl_name, 'wb') as fp:
        pickle.dump(pos_sentence_list, fp)
    print("POS done")
    return pos_sentence_list

def ner_to_list(word_sentence_list,pos_sentence_list,pkl_name):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    ner = NER("./data", disable_cuda=False)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    del ner
    with open(pkl_name, 'wb') as fp:
        pickle.dump(entity_sentence_list, fp)
    print("NER done")
    return entity_sentence_list

def wash_ws_result(WS_list,POS_list,WS_pkl_name,POS_pkl_name,file_name,part_of_Sentence):
    ND_filter = ["1","2","3","4","5","6","7","8","9","0","年","月","日","週"]
    new_ws_list = []
    new_pos_list = []
    for i in range(0,len(WS_list)):
        new_WS = []
        new_POS = []
        for j in range(0,len(WS_list[i])):
            # print(POS_list[i][j]) 
            if POS_list[i][j] in part_of_Sentence:
                new_WS.append(WS_list[i][j])
                new_POS.append(POS_list[i][j])
            elif POS_list[i][j] == "Nd":
                temp = 0
                for z in WS_list[i][j]:
                    if z in ND_filter:
                        temp += 1
                        print(z)
                        print(temp)
                if temp == 0:
                    new_WS.append(WS_list[i][j])
                    new_POS.append(POS_list[i][j])
                    # print(WS_list[i][j])
        new_ws_list.append(new_WS)
        new_pos_list.append(new_POS)
    with open(WS_pkl_name, 'wb') as fp:
        pickle.dump(new_ws_list, fp)
    with open(POS_pkl_name, 'wb') as fp:
        pickle.dump(new_pos_list, fp)
    with open(file_name,"w") as file:
        for i , j in zip(new_ws_list,new_pos_list):
            for word,pos in zip(i,j):
                file.write(f"{word}({pos})  ")
            file.write("\n=================\n")
    print("washed done")

name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = fuction.get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = fuction.get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

new_keyword = []
for i in keyword:
    temp = i.split("、")
    for i in temp:
        new_keyword.append(i)
keyword_dic = {}
for i in new_keyword:
    keyword_dic[i] = 1

with open("./forward_data/corpus_wikidict_PAGETITLE.pkl", 'rb') as fp:
    WIKI_DIC = pickle.load(fp)
n_gram = ["臺灣學研究","嬰幼兒","WorldCat","文史工作室","臺灣佛教圖書館","縮微資料","全民健康保險","文史工作室","中國國民黨","農業改良場","中央健康保險","內政部建築研究所"]
n_gram_dic = {}
for i in n_gram:
    n_gram_dic[i] = 1

ngram_keyword_dic = {}
ngram_keyword_dic.update(keyword_dic)
ngram_keyword_dic.update(n_gram_dic)

print("start final")
CKIP_WIKI_Ngram_keyword_WS_name = ws_to_list(raw_name,"./PklData/final_CKIP_WIKI_Ngram_keyword_WS_name.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_name = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_name,"./PklData/final_POS_CKIP_WIKI_Ngram_keyword_name.pkl")
CKIP_WIKI_Ngram_keyword_NER_name = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_name,CKIP_WIKI_Ngram_keyword_POS_name,"./PklData/final_NER_CKIP_WIKI_Ngram_keyword_name.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_name,CKIP_WIKI_Ngram_keyword_POS_name,"./PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_name.pkl","./PklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_name.pkl","washed_name.txt",part_of_sentance)

print("final name done")

CKIP_WIKI_Ngram_keyword_WS_abstract = ws_to_list(raw_abstract,"./PklData/final_CKIP_WIKI_Ngram_keyword_WS_abstract.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_abstract = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_abstract,"./PklData/final_POS_CKIP_WIKI_Ngram_keyword_abstract.pkl")
CKIP_WIKI_Ngram_keyword_NER_abstract = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_abstract,CKIP_WIKI_Ngram_keyword_POS_abstract,"./PklData/final_NER_CKIP_WIKI_Ngram_keyword_abstract.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_abstract,CKIP_WIKI_Ngram_keyword_POS_abstract,"./PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_abstract.pkl","./PklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_abstract.pkl","washed_abstract.txt",part_of_sentance)

print("final abstract done")

CKIP_WIKI_Ngram_keyword_WS_reference = ws_to_list(raw_reference,"./PklData/final_CKIP_WIKI_Ngram_keyword_WS_reference.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_reference = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_reference,"./PklData/final_POS_CKIP_WIKI_Ngram_keyword_reference.pkl")
CKIP_WIKI_Ngram_keyword_NER_reference = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_reference,CKIP_WIKI_Ngram_keyword_POS_reference,"./PklData/final_NER_CKIP_WIKI_Ngram_keyword_reference.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_reference,CKIP_WIKI_Ngram_keyword_POS_reference,"./PklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_reference.pkl","./PklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_reference.pkl","washed_reference.txt",part_of_sentance_for_reference)

print("final reference done")