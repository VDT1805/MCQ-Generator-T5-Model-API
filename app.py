import flask
from flask import request, jsonify
from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer
)
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True
trained_model_path = 'models/qag_t5_trained_model_v7'
trained_tokenizer = 'models/qag_t5_tokenizer_v7'

model = T5ForConditionalGeneration.from_pretrained(trained_model_path)
tokenizer = T5Tokenizer.from_pretrained(trained_tokenizer)


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
    for answer in answers:
        text = "context: {} answer: {}".format(sentence,answer)
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
        for dec in decs:
            # ques.append('question: {} answer: {}'.format(dec,answer))
            Question, answer = from_string(dec)
            ques.append({'question': Question , 'ans1': answer})
        questions = questions + ques
    return questions

# context = """
# Pinocchio ( pin-OH-kee-oh, Italian: ) is a fictional character and the protagonist of the children's novel The Adventures of Pinocchio (1883) by Italian writer Carlo Collodi of Florence, Tuscany. Pinocchio was carved by a woodcarver named Geppetto in a Tuscan village. He is created as a wooden puppet, but he dreams of becoming a real boy. He is known for his long nose, which grows when he lies.
# Pinocchio is a cultural icon and one of the most reimagined characters in children's literature. His story has been adapted into many other media, notably the 1940 Disney film Pinocchio. Collodi often used the Italian Tuscan dialect in his book. The name Pinocchio is possibly derived from the rare Tuscan form pinocchio (“pine nut”) or constructed from pino (“pine tree, pine wood”) and occhio ("eye").
# """
# qs = get_question(model, tokenizer, context)
# print(qs)

@app.route('/genqa', methods=['POST'])
def generate_question():
    data = request.get_json()
    sentence = data.get('context')
    answers = data.get('answers')
    num_of_q = int(data.get('num_of_q')) 
    questions = get_question(model, tokenizer,sentence, answers ,num_of_q)
    return json.dumps(questions)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

