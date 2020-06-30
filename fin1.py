import cmath as math
import time

def creat_dictionary():
    dictionary = {}
    with open('dictionary.txt') as fread:
        for line in fread:
            word = line.strip()
            dictionary[word] = 0
    return dictionary

def fmm_segs(docs,dictionary):
    result=[]
    for doc in docs:
        newresult=fmm_seg(doc,dictionary)
        result.append(newresult)
    return result

def fmm_seg(sentence, dictionary):#result为字典结果
    max_len = 7
    start = 0
    result=[]
    while start < len(sentence):
        end = min(start + max_len, len(sentence))  # 边界
        while end > start:
            candidate = sentence[start: end]
            # print(candidate)
            if candidate in dictionary or end == start + 1:
                result.append(candidate)
                start = end
                break
            else:
                end -= 1
    return result

def build_inverted_index(dictionary,documents):
    inverted_index={}
    for word in dictionary :
        #print(word)
        tfword = {}
        i=0
        for doc in documents:
            tfword[i]=0
            for word2 in doc:
                if word2 == word :
                    tfword[i]+=1
                    #print(tfword)
            i+=1
       # print('real:')
        str=word
        inverted_index[str]=tfword
        #print(inverted_index)
        #tfword.clear()
    return inverted_index

def inverted_index_rank(index:dict):
    for word in index:
        newdic={}
        newdic=sorted(index[word].items(), key=lambda d: d[1], reverse=True)
        #print(newdic)
        index[word]=newdic
    #rankres = sorted(index.items(), key=lambda d: d[1], reverse=True)
    return

class collection :
    def __init__(self , strdocuments):
        self.documents = strdocuments
        self.n_docs = len(self.documents)
        self.dic = self.build_dic(self.documents)
        self.idf = self.compute_idf(self.documents)
        self.tf_vecs = self.build_tf_vecs(self.documents)
        #self.inverted_index=self.build_inverted_index(self.documents,dictionary: dict)

    def build_dic(self,documents):
        dic={}
        for document in documents:
            for word in document:
                if word in dic:
                    dic[word]+=1
                else:
                    dic[word]=0
        return dic


    def compute_idf(self, documents):
        idf={}
        df={}
        for doc in documents:
            for word in doc:
                if word in idf and word not in df :
                    idf[word]+=1
                    df[word]=1
                elif word not in idf and word not in df:
                    idf[word]=1
                    df[word]=1
            df.clear()
        #print(len(documents))
        for word in idf :
            #print(len(documents)/(idf[word]+1))
            idf[word]=math.log(len(documents)/(idf[word]+1))
        #print(idf)
        return idf

    def build_tf_vecs(self, documents):
        vecs = self.dic
        start = time.clock()
        for word in vecs:
            vecs[word]={}
            for j in range(len(self.documents)):
                vecs[word][j]=0
        i=0
        for doc in documents:
            self.build_tf_vec(doc,vecs,i)
            i+=1
        end = time.clock()
        print('Time in seconds:', end - start)
        return vecs

    def build_tf_vec(self, document,inverted_index:dict,i):

        for word in document :
            inverted_index[word][i]+=1
        return

class TFIDFModel:
    def __init__(self, collection):
        self.documents = collection.documents
        self.idf = collection.idf
        self.tf_vecs = collection.tf_vecs

    def ranking (self,score):
        """doc_scores = []
        for docid, doc in enumerate(self.tf_vecs):
            s_doc_scores = sorted(doc_scores, key=lambda item: -item[1])
        result=[]
        for docid, score in s_doc_scores:
            result.append((documents[docid], score))"""
        rankres = sorted(score.items(), key=lambda d: d[1], reverse=True)
        return rankres


    def doc_score(self, query):
        #score(q, d) = sum_{query中所有词} count(w, d) * idf(w)
        score={}
        #print(self.tf_vecs)
        print()
        #print(self.idf['北京'])
        i=0
        j=0
        for word in query:
            if word not in self.tf_vecs:
                prstr='%s关键词无效，不做考察'
                continue
            for docnum in self.tf_vecs[word] :
                str='%s%d'%('doc',i)
                if j==0:
                    score[str] = self.tf_vecs[word][i] * self.idf[word].real
                else :
                    score[str] += self.tf_vecs[word][i] * self.idf[word].real
                i+=1
            i=0
            j+=1
        return score

if __name__ == '__main__':
    doc_strings = []
    with open('corpus_1000.txt','r',encoding='utf-8') as fread:
        for line in fread:
            doc_strings.append(line.strip())
    dictionary=creat_dictionary()
    #print(dictionary)
    documents=fmm_segs(doc_strings,dictionary)
    collect=collection(documents)
    print(len(collect.dic))
   # inverted_index_rank(collect.tf_vecs)
    tfidf_model = TFIDFModel(collect)
    score = tfidf_model.doc_score(['北京', '旅游'])
    result = tfidf_model.ranking(score)
    presult = result[0:9]
    for word in presult:
        print(word)
        print()
