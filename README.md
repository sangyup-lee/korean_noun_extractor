# korean_noun_extractor

한글 명사 추출기입니다. 

파이썬 konlpy에서 제공되는 기본 형태소 분석기를 사용하는 경우, 미등록 단어의 문제가 발생합니다. 
이러한 미등록 단어의 많은 경우가 명사 단어들입니다. 

noun_extractor는 이러한 문제를 해결하기 위해 고안된 모듈입니다. 

noun_extractor의 extract()는 다음과 같은 명사의 특징을 사용하여 명사를 추출합니다. 
- 명사의 사용 특성 (예, 조사와 같이 사용된다. 단독으로 사용된다.)
- 사용 빈도 (주요한 명사는 여러번 사용된다.)
- Komoran 형태소 분석기 보완 사용

지속적으로 업데이트가 되고 있습니다. 
