import flask
from flask import request, jsonify
from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5Tokenizer
)
import requests
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True
API_URL = "https://api-inference.huggingface.co/models/vuductoan2002hp/T5QAG"
headers = {"Authorization": "Bearer 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"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# output = query({
# 	"inputs": "The answer to the universe is",
# })


def from_string(formatted_string):
  parts = formatted_string.split("answer:")
  try:
    question = parts[0].replace("question:", "").strip()
    answer = parts[1].replace("answer:", "").strip()
  except:
    answer = ""
  return question, answer

def get_question(sentence,answers=["[MASK]"],num_of_q=1):
    questions = []
    res = []
    for answer in answers:
        text = "context: {} answer: {}".format(sentence,answer)
        # print (text)
        payload = {"inputs": text, "wait_for_model": True, "parameters":{"max_length": 512}}
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()[0]
        Question, answer = output['generated_text'].split('answer:')
        res.append({'question': Question , 'ans1': answer})
        # decs = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]
        # ques = []
        # for dec in decs:
        #     # ques.append('question: {} answer: {}'.format(dec,answer))
        #     Question, answer = from_string(dec)
        #     ques.append({'question': Question , 'ans1': answer})
        # questions = questions + ques
    return res

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
    questions = get_question(sentence, answers ,num_of_q)
    return json.dumps(questions)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

