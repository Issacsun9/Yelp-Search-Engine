def ner(sentence, nlp_food):
    doc = nlp_food(sentence)
    return doc.ents
