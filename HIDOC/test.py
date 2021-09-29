from gensim.models import Word2Vec

def tokenize(doc):
    new_list = str(doc).split()
    return new_list

model=Word2Vec.load('hidoc.model')
print(model.most_similar(positive=tokenize('생리 예정일')))

