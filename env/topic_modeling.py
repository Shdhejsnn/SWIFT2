from gensim import corpora, models
from preprocessing import preprocess_text

def extract_topics(texts):
    tokenized_texts = [preprocess_text(text) for text in texts]
    dictionary = corpora.Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
    lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    topics = lda_model.print_topics()
    return [{'topic_id': i, 'words': topic[1]} for i, topic in enumerate(topics)]
