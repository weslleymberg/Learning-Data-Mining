from collections import namedtuple, defaultdict
from itertools import islice

Doc = namedtuple('Doc', ['class_', 'tokens'])

def load_file(file_name):
    with open(file_name) as f:
        for line in f:
            _, class_, tweet = line.split(',', 2)
            yield Doc(int(class_), tweet.split())

def get_vocabulary(training_set):
    training_set = list(training_set)
    V = list()
    feature_set = defaultdict(list)
    for doc in training_set:
        V.extend(doc.tokens)
    return list(set(V))

def get_document_features(V, tokens):
    doc_feature = list()
    for word in V:
        if word in tokens:
            doc_feature.append(1)
        else:
            doc_feature.append(0)
    return doc_feature

def generate_feature_set(V, docs):
    feature_set = defaultdict(list)
    for doc in docs:
        feature_set[doc.class_].append(get_document_features(V, doc.tokens))
    return feature_set

def train(V, feature_set):
    N = sum(len(i) for i in feature_set.values())
    Wc = {} #P(wi|C)
    Pc = {} #P(C)
    for class_, features in feature_set.iteritems():
        Nk = float(len(features))
        Pc[class_] = Nk/N
        for i in xrange(len(V)):
            document_count = 0
            for feature in features:
                if feature[i] is 1:
                    document_count += 1
            Wc[class_, V[i]] = document_count/Nk
    return Wc, Pc

def classify(Wc, Pc, V, doc):
    result = []
    doc_features = get_document_features(V, doc)
    for class_, likelihood in Pc.iteritems():
        product = 1
        for i in xrange(len(doc_features)):
            product *= (Wc[class_, V[i]]+(1-doc_features[i])*(1-Wc[class_, V[i]]))
        result.append((class_, Pc[class_]*product))
    return max(result, key=lambda x: x[1])[0]




if __name__ == '__main__':
    #CONFIG
    FILE_NAME = "normalized_sentiment_analisys_10k_dataset.csv"
    TRAINING_SET_LENGHT = int(0.90*10000)
    #======

    print 'Bufering file...'
    buf = load_file(FILE_NAME)
    training_set = list(islice(buf, None, TRAINING_SET_LENGHT))

    print 'Extracting vocabulary...'
    V = get_vocabulary(training_set)
    print 'Generating document features...'
    feature_set = generate_feature_set(V, training_set)
    print 'Training...'
    Wc, Pc = train(V, feature_set)

    del training_set, feature_set

    print 'Classifying documents...'
    TP, FP, TN, FN = 0.0, 0.0, 0.0,0.0 #True Positive, False Positive, True Negative, False Negative
    for doc in buf:
        result = classify(Wc, Pc, V, doc.tokens)
        if result is 1 and doc.class_ is 1:
            TP += 1
        elif result is 0 and doc.class_ is 1:
            FN += 1
        elif result is 1 and doc.class_ is 0:
            FP += 1
        elif result is 0 and doc.class_ is 0:
            TN += 1

    print 'The precision is: ', TP/(TP+FP)
    print 'The recall is: ', TP/(TP+FN)
