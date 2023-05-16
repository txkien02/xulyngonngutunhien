import os,sys, math, re
from collections import Counter

def get_cosine_similarity(sentence1, sentence2):
    corpus = set(sentence1).union(sentence2)
    numerator = sum(sentence1.get(k, 0) * sentence2.get(k, 0) for k in corpus)
    magnitude_sentence1 = math.sqrt(sum(sentence1.get(k, 0)**2 for k in corpus))
    magnitude_sentence2 = math.sqrt(sum(sentence2.get(k, 0)**2 for k in corpus))
    return numerator / (magnitude_sentence1 * magnitude_sentence2)

def get_threshold(file_1, file_2, num_buckets=1000000):
    strings1, strings2  = [], []
    with open(file_1, 'r', encoding="utf8") as f:
        strings1 = f.readlines()
    strings1 = ''.join(strings1)
    
    with open(file_2, 'r', encoding="utf8") as f:
        strings2 = f.readlines()
    strings2 = ''.join(strings2)
    
    strings1 = strings1.lower().split()
    strings2 = strings2.lower().split()
    
    sentence1 = {}
    sentence2 = {}
    for word in set(strings1 + strings2):
        sentence1[word] = strings1.count(word)
        sentence2[word] = strings2.count(word)
    
    similarities = []
    for i in range(num_buckets):
        threshold = (i + 1) / num_buckets
        similarity = get_cosine_similarity(sentence1, sentence2)
        similarities.append(similarity)
        if similarity < threshold:
            break
    
    return threshold

def get_text_preprocessed(strings):
    strings = strings.lower()
    strings =  re.sub(r'[^\w\s]', '', strings).strip()
    return strings

classify_plagiarism = lambda x, th : 1 if x > th else 0
    
def check_for_plagiarism(file_1: str, file_2: str, th:int) -> str:
    strings1, strings2  = [], []
    with open(file_1, 'r', encoding="utf8") as f:
        strings1 = f.readlines()
    strings1 = ''.join(strings1)
    
    with open(file_2, 'r', encoding="utf8") as f:
        strings2 = f.readlines()
    strings2 = ''.join(strings2)
    strings1 = get_text_preprocessed(strings1).split()
    strings2 = get_text_preprocessed(strings2).split()
    sentence1 = Counter(strings1)
    sentence2 = Counter(strings2)
    similarity = (get_cosine_similarity(sentence1,sentence2))
    return classify_plagiarism(similarity,th), similarity


if __name__ == '__main__':
        if len(sys.argv) > 3:
            print("Invalid arguments")
        file1, file2 = sys.argv[1], sys.argv[-1]
        file1 = os.path.join(os.getcwd(),sys.argv[1])
        file2 = os.path.join(os.getcwd(),sys.argv[-1])
        th =  get_threshold(file1, file2)
        print("Threshold",th)
        result, similarity  = check_for_plagiarism(file1, file2, th)
        print(f"{result}")
        # data_folder = "data"
        # folders = [os.path.join(data_folder,x) for  x in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder,x))]
        # for folder in folders:
        #     file1 = os.path.join(folder, "1.txt")
        #     file2 = os.path.join(folder, "2.txt")
        #     result, distance  = is_plagiarism(file1, file2, threshold)
        #       print(f"{result}")
   
   