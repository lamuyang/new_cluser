from pymongo import MongoClient

def get_mongodb_row(collection_name):
    client = MongoClient('localhost', 27017)
    db = client["110_reference"]
    collection = db[collection_name]

    cursor = collection.find({}, {"record_num":1,"chi_paper_name":1,"chi_teacher_name":1,"degree":1,"college":1,"department":1,"language":1,"graduation_year":1,"chi_keyword":1,"abstract":1,"content":1,"reference":1,"_id":1})
    
    record_num_list = [] #記錄編號
    chi_paper_name_list = [] #論文名稱(中文)
    chi_teacher_name_list = [] #指導教授(中文)
    degree_list = [] #學位類別
    college_list = [] #學院名稱
    department_list = [] #系所名稱
    language_list = [] #語文別
    graduation_year_list = [] #畢業學年度
    chi_keyword_list = [] #中文關鍵詞
    abstract_list = [] #摘要
    content_list = [] #論文目次
    reference_list = [] #參考資源
    allfields_list = [] #全部


    for row in cursor:
        record_num_list.append(row["record_num"])
        chi_paper_name_list.append(row['chi_paper_name'])
        chi_teacher_name_list.append(row["chi_teacher_name"])
        degree_list.append(row['degree'])
        college_list.append(row['college'])
        department_list.append(row['department'])
        language_list.append(row["language"])
        graduation_year_list.append(row['graduation_year'])
        chi_keyword_list.append(row['chi_keyword'])
        abstract_list.append(row['abstract'])
        content_list.append(row['content'])
        reference_list.append(row['reference'])
        allfields_list.append((row['chi_paper_name'],row['chi_keyword'],row['abstract'],row['content'],row['reference']))
  
    return allfields_list
    
def pre_data(name,keyword,abstract,content,reference,allfields_list):
    allfields_list= get_mongodb_row("LINS")

    name = []
    keyword = []
    abstract = []
    content = []
    reference = []
    for i in range(0,len(allfields_list)):
        name.append(allfields_list[i][0])
        keyword.append(allfields_list[i][1])
        abstract.append(allfields_list[i][2])
        content.append(allfields_list[i][3])
        reference.append(allfields_list[i][4])
    return name,keyword,abstract,content,reference









# reference_list = [' '.join([i.strip() for i in z.strip().split('\t')]) for z in reference_list]







#以下為變數
# Record_Num = [] #記錄編號
# chi_paper_name = [] #論文名稱(中文)
# eng_paper_name = [] #論文名稱(外文)
# chi_teacher_name = [] #指導教授(中文)
# eng_teacher_name = [] #指導教授(外文)
# degree = [] #學位類別
# college = [] #學院名稱
# department = [] #系所名稱
# language = [] #語文別
# graduation_year = [] #畢業學年度
# chi_keyword = [] #中文關鍵詞
# eng_keyword = [] #外文關鍵詞
# abstract = [] #摘要
# eng_abstract = [] #摘要(外文)
# content = [] #論文目次
# reference = [] #參考資源














