import spacy

nlp = spacy.load('en')

doc = nlp(u'Mark and John are sincere employees at Google.')

noun_adj_pairs = []

for i,token in enumerate(doc):
    if token.pos_ not in ('NOUN','PROPN'):
        continue
    for j in range(i+1,len(doc)):
        if doc[j].pos_ == 'ADJ':
            noun_adj_pairs.append((token,doc[j]))
            break

noun_adj_pairs
