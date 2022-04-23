import numpy as np
import pandas as pd
import yake
from nltk.tokenize import sent_tokenize


def remove_stopwords(sen, stop_words):
    # USE: function to remove stopwords
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new


def summarize(df, len_summary, show_summary=False):
    # USE: Summarize the sentences in the reviews for a bussiness
    # INPUT:
    # df: each row of which is a review for this bussiness, df
    # len_summary: number of sentences in summary for output, int
    # show_summary: print summary or not, boolean
    # OUTPUT: sorted sentences in all reviews, list of tuples

    # split the the text in the articles into sentences
    sentences = []
    for s in df['text']:
        sentences.append(sent_tokenize(s))
    sentences = [y for x in sentences for y in x]
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    # remove stopwords from the sentences
    stop_words = stopwords.words('english')
    clean_sentences = [remove_stopwords(r.split(), stop_words) for r in clean_sentences]

    # Extract word vectors
    word_embeddings = {}
    f = open('glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    # Extract sentence vectors
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # Similarities among the sentences
    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = \
                cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[0, 0]
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Generate summary
    if show_summary == True:
        for i in range(len_summary):
            print(ranked_sentences[i][1])

    return ranked_sentences[0: len_summary]


def get_keywords(text, numOfKeywords=5, max_ngram_size=3, deduplication_threshold=0.7, windowsSize=5,
                 show_keywords=False):
    # USE: get the keywords in a paragraph, str
    if type(text) is list:
        text = str(text).replace("', '", ' ').replace("['", '').replace("']", "")
    custom_kw_extractor = yake.KeywordExtractor(lan='en', n=max_ngram_size, dedupLim=deduplication_threshold,
                                                dedupFunc='seqm', top=numOfKeywords, features=None)
    keywords_all = custom_kw_extractor.extract_keywords(text)
    print(keywords_all)
    keywords = [item[0] for item in keywords_all]
    if show_keywords == True:
        for keyword in keywords:
            print(keyword)
    return keywords


# %%

# If work on str input
testText = "food bad restaurant feel like old chinese restaurant got confused saw spaghetti meatball menu since chinese restaurant decided try well nice"
#print(get_keywords(testText))

# If work on list of str input
testText = ['food', 'bad', 'restaurant', 'feel', 'like', 'old', 'chinese', 'restaurant', 'got', 'confused', 'saw',
            'spaghetti', 'meatball', 'menu', 'since', 'chinese', 'restaurant', 'decided', 'try', 'well', 'nice']
#get_keywords(testText)


