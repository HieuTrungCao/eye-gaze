import nltk
from underthesea import sent_tokenize
from underthesea import word_tokenize
from nltk.corpus import stopwords

def pre_process():
    sw = stopwords.words('english')

    file_in = open('Data\data_in.txt', encoding='utf-8')
    data = file_in.read()
    file_in.close()

    tokens = word_tokenize(data)
    words = [w.lower() for w in tokens if w.isalpha() and w.lower() not in sw]

    fdist = nltk.FreqDist(words)
    features = fdist.keys()
    words = sorted(set(features))

    file_out = open('Data\data_out.txt', encoding="utf-8", mode='w')
    for word in words:
        if word not in nltk.corpus.words.words('en'):
            file_out.write(word + '\n')
    file_out.close()

def is_in_2d_list(two_d_list, val):
    return any(
        val in nested_list
        for nested_list in two_d_list
    )

def process():
    file_in = open('Data\data_out.txt', encoding='utf-8')
    data = file_in.read()
    file_in.close()
    out = []
    for word in data:
        for ch in word:
            if is_in_2d_list(out, ch) == False and ch != '\n' and ch.isascii():
                out.append([ch, int(1)])
            if any(ch in (match := nested_list) for nested_list in out):
                match[1] += 1
    print(out)
    for i in range(len(out) - 1):
        for j in range(0, len(out) - i - 1):
            if out[j][1] > out[j + 1][1]:
                out[j], out[j + 1] = out[j + 1], out[j]
    print(out)
    file_out = open('Data\out.txt', encoding="utf-8", mode='w')
    for nested_list in out:
        for w in nested_list:
            file_out.write(str(w) + ' ')
        file_out.write('\n')
    file_out.close()

def main():
    p = int(input())
    if p == 0:
        pre_process()
    elif p == 1:
        process()

if __name__ == "__main__":
    main()


