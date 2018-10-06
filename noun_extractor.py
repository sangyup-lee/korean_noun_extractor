# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 21:11:51 2018

@author: Sang
"""


import hgtk
import re
from collections import Counter
import math
from konlpy.tag import Komoran
komoran = Komoran()

Except_komoran_pos = ['MAG', 'XR', 'VA', 'NP', 'VV','VA', 'NR']
Except_komoran_pos_num = ['MAG', 'XR', 'VA', 'NP', 'VV','VA', 'SN']
Pronouns = ['나', '너', '우리', '그', '그녀', '그대', '그이', '누구', '이분', '저분', '그분', '그들', '그녀들', '그대들', '우리들']

josa_list = set(['하며', '위한', '하지', '엔', '에서도', '이나마', '만', '토록', '로서는', '하고', '해', '조차', '다', '에', '이나', '님께', '로서야', '은', '에다가', '까지', '로', '이라도', '가', '라든가', '인즉슨', '으로', '로다', '에다', '만큼', '밖에', '에게', '에도', '해야', '에는', '든', '와의', '같', '든가', '로서도', '이면', '이라', '께', '을', '라는', '된', '말고', '의', '며', '히', '면', '이고', '이라고는', '님', '라면', '만치', '이랑', '에게서', '를', '이며', '으로부터', '에서처럼', '하는', '들', '는', '적인', '뿐', '라든지', '로서', '처럼', '있는', '라고는', '한', '로다가', '이다', '로부터', '마저', '되', '이란', '로서의', '이든', '같이', '에게로', '할', '치고야', '없는', '부터', '인즉', '이라고', '이든가', '나', '과', '고', '뿐만', '나마', '에서부터', '하면', '으로써', '께서', '엔들', '하게', '대로', '치고서', '이라든지', '하는한', '에서', '라고', '적', '씨', '이', '라서', '하', '한테서', '커녕', '보다', '라도', '이든지', '도', '인들', '되고', '으로서', '하다', '란', '마냥', '랑', '이라면', '와', '한테로', '치곤', '한테다가', '해서', '마다', '하고는', '치고', '라', '라곤', '한테', '으', '로써', '이라든가'])
Except_words = set(['위한', '하며', '있다', '흘러','이후', '이전', '낮게','흘려', '들을', '만한','지난','이끌어', '이미', '이밖', '이번', '이전','하면','힘든', '힘들다', '하면서','한다', '한다고', '한다면', '이제', '이젠','이하', '중이다', '중이던', '중인', '인한','전혀', '절대', '절반', '인해','이상','이어', '이어질','이날', '이내', '이달', '이동한', '이라며', '이라면서','이런', '이런일', '이렇게', '이루고', '이뤄질', '이르면', '이른바','어느', '어떤', '어떻게', '역시', '열리', '열린', '열심히', '열어', '어려운', '어려울', '어렵다', '어린','안팎', '알고', '알려져', '알려진','아니냐', '아니다', '아닌', '아닐', '아래', '아바나', '아주', '아직', '아찔','보이고', '보인다', '반드시','번째', '생긴','서로','새로운','스스로', '순간', '당시','따라', '따로','만큼', '만약', '명확히' '따르면', '따른', '때문','당일','되면','들어가', '들어간', '듯한',  '되지', '된다', '두고', '동안','대신','대한', '당장', '당초', '대거','높여', '놓고', '누구','그러한', '그렇지', '그분','강력하게', '거듭','걸쳐', '관한', '관련','계속','강력한', '강하게', '강한', '갖고', '갖춘', '같다','거쳐', '거쳐서', '겨우', '경우', '같다','갑자기','각각','가지', '가능한','강하게', '면서','이라며', '가운데','따라','것', '게다가', '결국', '결론적으로', '구체적으로', '그나저나', '그래서', '그러나', '그러니', '그러니까', '그러면', '그러므로', '그런', '그런데', '그럼에도', '그렇게', '그렇기는', '그렇지만', '그리고', '그리하여', '급기야', '끝으로', '다른', '다만', '대해서', '더구나', '더욱이', '덧붙혀', '도리어', '동시에', '따라서', '때문에', '또한', '마지막으로', '마침내', '말하면', '바로', '반대로', '반면에', '불구하고', '뿐만', '사실상', '아니라', '아울러', '어쩌면', '예컨데', '오히려', '왜냐하면', '이같이', '이처럼', '일례로', '점에서', '하물며', '하지만', '한편', '해도'])
#Proper_nouns = set(['김정은'])

def get_word_count(word, ojoels_count_dict):
    num = 0
    for ojoel in ojoels_count_dict.keys():
        if ojoel.find(word) == 0: # 어절의 처음이 해당 단어인 경우에 +1
            num += ojoels_count_dict[ojoel]
    return num

def check_if_not_Noun(word):
    
    Batchims = ['ㄳ','ㅆ', 'ㅀ', 'ㄾ', 'ㄶ','ㄵ', 'ㄺ', 'ㄼ','ㄿ']
    is_not_Noun = 0
    characters = hgtk.text.decompose(word)
    for batchim in Batchims:
        if batchim in characters:
            is_not_Noun = 1
            break
    if is_not_Noun == 0:
        for except_word in Except_words:
            if except_word in word:
                is_not_Noun = 1
                break
            
    return is_not_Noun

def check_if_josa(word, repetitives):
    repetitive_words = []
    word_len = len(word)
    for rep_word in repetitives:
        if rep_word[-1] in josa_list or rep_word[-2:] in josa_list or rep_word[word_len:] in josa_list:
            repetitive_words.append(rep_word)
    return repetitive_words

def get_repetitives(words_list): 
    # 다른 단어를 포함하는 단어들이 있는지, 그리고 그러한 단어는 같은 의미의 단어인지를 판단 
    # 중복이 되는 단어들을 찾아서 그 단어들을 리턴
    sorted_words_list = sorted(words_list, key=lambda x:len(x))

    repetitive_words = []
    total_repetitives = []
    for word in sorted_words_list:
        if word not in total_repetitives:
            repetitives=[]
            for word1 in sorted_words_list[sorted_words_list.index(word)+1:]:
                if word in word1:
                    repetitives.append(word1)
                    total_repetitives.append(word1)
            repetitive_words.extend(check_if_josa(word, repetitives))

    return set(repetitive_words)

def check_plural(words_list):
    words = words_list
    for word in words_list:
        if word[-1] == '들' or len(word)==1:
            words.remove(word)
            if len(word) - 1 > 1:
                words.append(word[:-1])
    return words

def check_if_noun(word, fre, ojoels_count_dict, threshold): #threshold는 num_josa_ojoels/total_num_ojoels
    is_word = 0
    num_proper_nouns = 0 #고유명사로 사용된 횟수 
    total_num_ojoels = fre # 해당 단어가 들어가는 어절이 몇개가 있는지를 저장
    num_josa_ojoels = 0 # 해당 단어가 들어간 어절 중에서 단어 뒤의 부분이 조사인 어절의 수
    
    for ojoel in ojoels_count_dict.keys():
        if ojoel.find(word) == 0:
            if len(ojoel) > len(word): #여기에서 고유 명사는 제거가 된다.
                suffix = ojoel[len(word):]
                if suffix in josa_list:
                    num_josa_ojoels += ojoels_count_dict[ojoel]
            elif len(ojoel) == len(word):
                if word[-1] not in josa_list and word[-2:] not in josa_list:
                    num_proper_nouns += ojoels_count_dict[ojoel]    # 끝 부분 음절이 조사가 아닌 경우는 일단 고유 명사로 간주           

    if num_josa_ojoels/total_num_ojoels > threshold:
        is_word = 1

    if num_proper_nouns/total_num_ojoels > 0.5:
        is_word = 1

    return is_word 

def extract(text, include_number = False, freq=0, threshold=0.4):
    """
    text: 분석하고자하는 텍스트 데이터
    include_number: 숫자를 포함한 단어를 포함할 것인지 여부
    freq: 최소 사용빈도
    threshold: 조사포함 어절 / 전체 어절
    """
    text1 = re.sub(r'[\(\)\'\"=~…]', ' ', text) # 특정 기호 없애기
    text1 = re.sub(r'\.','',text1) # 마침표 없애기
    cleaned_text = re.sub(r'[^∙\s\w\d]', '', text1) # 기호 없애기

    ojoels = [ojoel.strip() for ojoel in cleaned_text.split()] #어절 추출
    c = Counter(ojoels)
    ojoels_count_dict = dict(c)
    
    word_counts= {} # 단어라고 간주되는 것을 키로 저장하고, 그것의 출현 빈도를 value로 저장
    
    for word in Except_words: # 명사 단어를 포함하고 있지 않은 어절 제거
        while word in ojoels:
            ojoels.remove(word)
    
    for ojoel in set(ojoels):
        if len(ojoel) > 1: # 어절의 음절수가 하나인 경우는 제외
            for k in range(1, len(ojoel)+1):
                word = ojoel[0:k]
                if word not in josa_list: 
                    if word not in word_counts.keys():
                        word_counts[word] = get_word_count(word, ojoels_count_dict)    
                
    sorted_words = list(sorted(word_counts.items(), key=lambda x:x[1], reverse=True))
    # 많이 사용된 순으로 정렬
    
    Noun_words = []
    for word, fre in sorted_words:
        if fre >= freq:  # 사용된 빈도수에 따라서 1차 제거
            if check_if_noun(word, fre, ojoels_count_dict, threshold):
                Noun_words.append(word)
    
    for word in list(get_repetitives(Noun_words)): #강동호, 강동 두개의 단어에 대해서 '강동' 제외
        Noun_words.remove(word)
        
    singular_Noun_words=check_plural(Noun_words) # 복수 단어들은 제외
    
    Noun_words_2nd=[]
    for word in singular_Noun_words:
        if len(word) > 1:
            if not check_if_not_Noun(word): # ['ㄳ','ㅆ', 'ㅀ', 'ㄾ', 'ㄶ','ㄵ', 'ㄺ', 'ㄼ','ㄿ'] 받침 사용 단어는 제외
                Noun_words_2nd.append(word)
             
    final_Noun_words = []
    if include_number: #숫자를 포함하고자 하는 경우
        for word in Noun_words_2nd:
            kmr_pos = komoran.pos(word)
            if len(kmr_pos) > 1:
                    if kmr_pos[1][0] == '없' or kmr_pos[1][0] == '있':
                        final_Noun_words.append(kmr_pos[0][0])
                        continue
            if kmr_pos[0][1] not in Except_komoran_pos:
                final_Noun_words.append(word)
                
            
    else:
        for word in Noun_words_2nd:
            kmr_pos = komoran.pos(word)
            if len(kmr_pos) > 1:
                    if kmr_pos[1][0] == '없' or kmr_pos[1][0] == '있':
                        final_Noun_words.append(kmr_pos[0][0])
                        continue
            if kmr_pos[0][1] not in Except_komoran_pos_num:
                final_Noun_words.append(word)
    
    for word in Pronouns:
        if word in final_Noun_words:
            final_Noun_words.remove(word)

    return final_Noun_words
