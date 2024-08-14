from typing import OrderedDict
import flask
from flask import request, jsonify
from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer
)
import json
import spacy
from sense2vec import Sense2Vec
nlp = spacy.load("en_core_web_md")
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk("s2v_old") 
s2v1 = Sense2Vec().from_disk("s2v_old")


app = flask.Flask(__name__)
app.config["DEBUG"] = True
trained_model_path = 'models/qag_t5_trained_model_v7'
trained_tokenizer = 'models/qag_t5_tokenizer_v7'

model = T5ForConditionalGeneration.from_pretrained(trained_model_path)
tokenizer = T5Tokenizer.from_pretrained(trained_tokenizer)

def sense2vec_get_words(word,s2v):
    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=5)

    # print ("most_similar ",most_similar)

    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())

    out = list(OrderedDict.fromkeys(output))
    return out

def extract_token_by_indices(doc, start, end):
    
    # Extract the span using the start and end indices
    span = doc.char_span(start, end)
    
    if span is not None:
        # # Extract the token within the span
        # tokens = [token for token in span]
        # return tokens
        return span
    else:
        return None

def from_string(formatted_string):
  parts = formatted_string.split("answer:")
  try:
    question = parts[0].replace("question:", "").strip()
    answer = parts[1].replace("answer:", "").strip()
  except:
    answer = ""
  return question, answer

def get_question(mdl,tknizer,sentence,answers=["[MASK]"],num_of_q=1):
    questions = []
    # Process the sentence with spaCy
    doc = nlp(sentence)
    for answer in answers:
        text = "context: {} answer: {}".format(sentence,answer[0])
        # print (text)
        max_len = 512
        encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

        input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

        outs = mdl.generate(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    early_stopping=True,
                                    num_beams=5,
                                    num_return_sequences=num_of_q,
                                    no_repeat_ngram_size=2,
                                    max_length=72)

        decs = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
        ques = []
        for index,dec in enumerate(decs):
            Question, ans = from_string(dec)
            # print("Answer: ", answer,"\n",dec)
            ques.append([Question , ans, answer[1], answer[2]])
            # ques.append({'question': Question , 'ans1': answer, 'ans2': distractions[0], 'ans3': distractions[1], 'ans4': distractions[2], 'ans5': distractions[3], "ans6": distractions[4]})
        questions = questions + ques
        #one answer only
    print(questions)
    res = []
    for index,q in enumerate(questions):
        if answers[0][0] == "[MASK]":
            start = sentence.find(q[1])
            end = start + len(q[1])
        else:
            start = int(q[2])
            end = int(q[3])
        print("Start: ", start, "End: ", end)
        tokens = extract_token_by_indices(doc, start, end)
        distractions = ["","","","",""]
        try:
            distractions = tokens._.s2v_most_similar(5)
            if distractions == None:
                distractions = ["","","","",""]
            distractions = [distract[0][0] for distract in distractions]
        except Exception as e:
            print(e)
            # distractions = sense2vec_get_words(q[1],s2v1)
            # if distractions == None:
            distractions = ["","","","",""]
        distractions += [''] * (5 - len(distractions))
        res.append({'question': q[0] , 'ans1': q[1], 'ans2': distractions[0], 'ans3': distractions[1], 'ans4': distractions[2], 'ans5': distractions[3], "ans6": distractions[4]})
    # questions = res
    return res

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
#             distractors = sense2vec_get_words(answer,s2v)

#             ques.append({'question': Question , 'ans1': answer, 'ans2': distractors[0]})
#         questions = questions + ques
#     return questions

# context = """
# Pinocchio ( pin-OH-kee-oh, Italian: ) is a fictional character and the protagonist of the children's novel The Adventures of Pinocchio (1883) by Italian writer Carlo Collodi of Florence, Tuscany. Pinocchio was carved by a woodcarver named Geppetto in a Tuscan village. He is created as a wooden puppet, but he dreams of becoming a real boy. He is known for his long nose, which grows when he lies.
# Pinocchio is a cultural icon and one of the most reimagined characters in children's literature. His story has been adapted into many other media, notably the 1940 Disney film Pinocchio. Collodi often used the Italian Tuscan dialect in his book. The name Pinocchio is possibly derived from the rare Tuscan form pinocchio (“pine nut”) or constructed from pino (“pine tree, pine wood”) and occhio ("eye").
# """
# qs = get_question(model, tokenizer, context)
# print(qs)


# In electronics and computer science, a reduced instruction set computer (RISC) is a computer architecture designed to simplify the individual instructions given to the computer to accomplish tasks. Compared to the instructions given to a complex instruction set computer (CISC), a RISC computer might require more instructions (more code) in order to accomplish a task because the individual instructions are written in simpler code. The goal is to offset the need to process more instructions by increasing the speed of each instruction, in particular by implementing an instruction pipeline, which may be simpler to achieve given simpler instructions.
@app.route('/genqa', methods=['POST'])
def generate_question():
    data = request.get_json()
    sentence = data.get('context')
    answers = data.get('answers')
    num_of_q = int(data.get('num_of_q'))
    print(answers)
    questions = get_question(model, tokenizer,sentence, answers ,num_of_q)
    print(questions)
    return json.dumps(questions)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

