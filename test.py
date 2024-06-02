# import wn
# en = wn.Wordnet('oewn:2023') 
# ss = en.synsets('1986')[0]
# print(ss.definition(),ss.examples())

# from collections import OrderedDict
# from sense2vec import Sense2Vec

# s2v = Sense2Vec().from_disk("s2v_old")

# def sense2vec_get_words(word,s2v):
#     output = []
#     word = word.lower()
#     word = word.replace(" ", "_")

#     sense = s2v.get_best_sense(word)
#     most_similar = s2v.most_similar(sense, n=3)

#     print ("most_similar ",most_similar)

#     for each_word in most_similar:
#         append_word = each_word[0].split("|")[0].replace("_", " ").lower()
#         if append_word.lower() != word:
#             output.append(append_word.title())

#     out = list(OrderedDict.fromkeys(output))
#     return out

# word = "Pinocchio"
# distractors = sense2vec_get_words(word,s2v)

# print ("Distractors for ",word, " : ",distractors)

# import nltk
# nltk.download('wordnet')
# from nltk.corpus import wordnet as wn

# # Distractors from Wordnet
# def get_distractors_wordnet(syn,word):
#     distractors=[]
#     word= word.lower()
#     orig_word = word
#     if len(word.split())>0:
#         word = word.replace(" ","_")
#     hypernym = syn.hypernyms()
#     if len(hypernym) == 0: 
#         return distractors
#     for item in hypernym[0].hyponyms():
#         name = item.lemmas()[0].name()
#         print ("name ",name, " word",orig_word)
#         if name == orig_word:
#             continue
#         name = name.replace("_"," ")
#         name = " ".join(w.capitalize() for w in name.split())
#         if name is not None and name not in distractors:
#             distractors.append(name)
#     return distractors
# original_word = "Pinocchio"
# synset_to_use = wn.synsets(original_word,'n')[0]
# distractors_calculated = get_distractors_wordnet(synset_to_use,original_word)


# import spacy
# import regex as re
# nlp = spacy.load("en_core_web_md")
# s2v = nlp.add_pipe("sense2vec")
# s2v.from_disk("s2v_old") 
# string1 = r"""
# Pinocchio ( pin-OH-kee-oh, Italian: ) is a fictional character
# and the protagonist of the children's novel The Adventures of Pinocchio (1883) by Italian writer Carlo Collodi of Florence, Tuscany. Pinocchio was carved by a woodcarver named Geppetto in a Tuscan village. He is created as a wooden puppet, but he dreams of becoming a real boy. He is known for his long nose, which grows when he lies.
# Pinocchio is a cultural icon and one of the most reimagined characters in children's literature. His story has been adapted into many other media, notably the 1940 Disney film Pinocchio. Collodi often used the Italian Tuscan dialect in his book. The name Pinocchio is possibly derived from the rare Tuscan form pinocchio (“pine nut”) or constructed from pino (“pine tree, pine wood”) and occhio ("eye").
# """
# doc = nlp(string1)

# print(doc)
# print(doc[97],doc[97].pos_)
# print(doc[0]._.s2v_most_similar(3))
# for index,i in enumerate(doc):
#    try:
#     print("INDEX:",index,'\n',i,i.pos_,'\n',i._.s2v_most_similar(3))
#    except ValueError as e:
#     print("INDEX:",index,e)
#      #If a token pos tag combination is not in the keyed vectors it raises              Error so we need to catch it
#     pass 

# import spacy

# # Load the spaCy model
# nlp = spacy.load("en_core_web_md")
# s2v = nlp.add_pipe("sense2vec")
# s2v.from_disk("s2v_old") 
# def extract_token_by_indices(sentence, start, end):
#     # Process the sentence with spaCy
#     doc = nlp(sentence)
    
#     # Extract the span using the start and end indices
#     span = doc.char_span(start, end)
    
#     if span is not None:
#         # Extract the token within the span
#         # tokens = [token for token in span]
#         # return tokens
#         return span
#     else:
#         return None

# # Example usage
# sentence = "Pinocchio ( pin-OH-kee-oh, Italian: ) is a fictional character and the protagonist of the children's novel The Adventures of Pinocchio (1883) by Italian writer Carlo Collodi of Florence, Tuscany. Pinocchio was carved by a woodcarver named Geppetto in a Tuscan village. He is created as a wooden puppet, but he dreams of becoming a real boy. He is known for his long nose, which grows when he lies. Pinocchio is a cultural icon and one of the most reimagined characters in children's literature. His story has been adapted into many other media, notably the 1940 Disney film Pinocchio. Collodi often used the Italian Tuscan dialect in his book. The name Pinocchio is possibly derived from the rare Tuscan form pinocchio (“pine nut”) or constructed from pino (“pine tree, pine wood”) and occhio ('eye')."
# # sentence = "A sentence about natural language processing."
# start = 136
# end = 140

# tokens = extract_token_by_indices(sentence, start, end)
# if tokens:
#     # print(f"Tokens at indices {start}-{end}: {[token.text for token in tokens]}")
#     # print(f"POS tags: {[token.pos_ for token in tokens]}")
#     # print(f"Dependencies: {[token.dep_ for token in tokens]}")
#     # print(f"Similarity: {[token._.s2v_most_similar(3) for token in tokens]}")
#     print(f"Similarity: {tokens._.s2v_most_similar(3)}")

# else:
#     print(f"No tokens found at indices {start}-{end}")


# from typing import OrderedDict
# import flask
# from flask import request, jsonify
# from transformers import (
#     AdamW,
#     T5ForConditionalGeneration,
#     T5Tokenizer
# )
# import json
# import spacy
# from sense2vec import Sense2Vec
# nlp = spacy.load("en_core_web_md")
# s2v = nlp.add_pipe("sense2vec")
# s2v.from_disk("s2v_old") 

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True
# trained_model_path = 'models/qag_t5_trained_model_v7'
# trained_tokenizer = 'models/qag_t5_tokenizer_v7'

# model = T5ForConditionalGeneration.from_pretrained(trained_model_path)
# tokenizer = T5Tokenizer.from_pretrained(trained_tokenizer)

# def sense2vec_get_words(word,s2v):
#     output = []
#     word = word.lower()
#     word = word.replace(" ", "_")

#     sense = s2v.get_best_sense(word)
#     most_similar = s2v.most_similar(sense, n=3)

#     print ("most_similar ",most_similar)

#     for each_word in most_similar:
#         append_word = each_word[0].split("|")[0].replace("_", " ").lower()
#         if append_word.lower() != word:
#             output.append(append_word.title())

#     out = list(OrderedDict.fromkeys(output))
#     return out

# def from_string(formatted_string):
#   parts = formatted_string.split("answer:")
#   try:
#     question = parts[0].replace("question:", "").strip()
#     answer = parts[1].replace("answer:", "").strip()
#   except:
#     answer = ""
#   return question, answer

# def get_question(mdl,tknizer,sentence,answers=["[MASK]"],num_of_q=1):
#     questions = []
#     for answer in answers:
#         text = "context: {} answer: {}".format(sentence,answer)
#         # print (text)
#         max_len = 512
#         encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

#         input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

#         outs = mdl.generate(input_ids=input_ids,
#                                     attention_mask=attention_mask,
#                                     early_stopping=True,
#                                     num_beams=5,
#                                     num_return_sequences=num_of_q,
#                                     no_repeat_ngram_size=2,
#                                     max_length=72)

#         decs = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
#         ques = []
#         for dec in decs:
#             # ques.append('question: {} answer: {}'.format(dec,answer))
#             Question, answer = from_string(dec)
            
#             ques.append({'question': Question , 'ans1': answer})
#         questions = questions + ques
#     return questions

# def get_question2(mdl,tknizer,sentence,answers=["[MASK]"],num_of_q=1):
#     questions = []
#     doc = nlp(sentence)
#     for answer in answers:
#         text = "context: {} answer: {}".format(sentence,answer)
#         # print (text)
#         max_len = 512
#         encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

#         input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

#         outs = mdl.generate(input_ids=input_ids,
#                                     attention_mask=attention_mask,
#                                     early_stopping=True,
#                                     num_beams=5,
#                                     num_return_sequences=num_of_q,
#                                     no_repeat_ngram_size=2,
#                                     max_length=72)

#         decs = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
#         ques = []
#         for dec in decs:
#             # ques.append('question: {} answer: {}'.format(dec,answer))
#             Question, answer = from_string(dec)
            
#             ques.append({'question': Question , 'ans1': answer})
#         questions = questions + ques
#     return questions

# context = """
# Pinocchio ( pin-OH-kee-oh, Italian: ) is a fictional character and the protagonist of the children's novel The Adventures of Pinocchio (1883) by Italian writer Carlo Collodi of Florence, Tuscany. Pinocchio was carved by a woodcarver named Geppetto in a Tuscan village. He is created as a wooden puppet, but he dreams of becoming a real boy. He is known for his long nose, which grows when he lies.
# Pinocchio is a cultural icon and one of the most reimagined characters in children's literature. His story has been adapted into many other media, notably the 1940 Disney film Pinocchio. Collodi often used the Italian Tuscan dialect in his book. The name Pinocchio is possibly derived from the rare Tuscan form pinocchio (“pine nut”) or constructed from pino (“pine tree, pine wood”) and occhio ("eye").
# """
# qs = get_question(model, tokenizer, context)
# print(qs)


# # In electronics and computer science, a reduced instruction set computer (RISC) is a computer architecture designed to simplify the individual instructions given to the computer to accomplish tasks. Compared to the instructions given to a complex instruction set computer (CISC), a RISC computer might require more instructions (more code) in order to accomplish a task because the individual instructions are written in simpler code. The goal is to offset the need to process more instructions by increasing the speed of each instruction, in particular by implementing an instruction pipeline, which may be simpler to achieve given simpler instructions.
# @app.route('/genqa', methods=['POST'])
# def generate_question():
#     data = request.get_json()
#     sentence = data.get('context')
#     answers = data.get('answers')
#     num_of_q = int(data.get('num_of_q')) 
#     questions = get_question(model, tokenizer,sentence, answers ,num_of_q)
#     return json.dumps(questions)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

# Distractors from Wordnet
def get_distractors_wordnet(syn,word):
    distractors=[]
    word= word.lower()
    orig_word = word
    if len(word.split())>0:
        word = word.replace(" ","_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0: 
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        #print ("name ",name, " word",orig_word)
        if name == orig_word:
            continue
        name = name.replace("_"," ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors
original_word = "8 bit"
synset_to_use = wn.synsets(original_word,'n')[0]
distractors_calculated = get_distractors_wordnet(synset_to_use,original_word)
print(distractors_calculated)