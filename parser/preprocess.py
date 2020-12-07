# coding=utf-8
# written by Kangwook Lee (kw.brian.lee@samsung.com)


import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nl2bash'))

import json
import random

from nlp_tools import tokenizer
from encoder_decoder import data_utils
from bashlint import data_tools

KEYWORD_LIST = ['_DATETIME', '_TIMESPAN', 'Timespan', '_DIRECTORY', '_FILE', 'Directory', 'File', 'Path', '_NUMBER',
                'Number', '_PERMISSION', 'Permission', '_REGEX', 'Regex', '_SIZE', 'Size', 'Program', 'Quantity']


def main():
    with open(os.path.join(os.getcwd(), 'data/nl2bash-data.json')) as fr:
        d_nl2bash = json.load(fr)
    with open(os.path.join(os.getcwd(), 'data/ainix_data.json')) as fr:
        d_ainix = json.load(fr)
    tuple_nl2bash = [(d_nl2bash[key]['invocation'], d_nl2bash[key]['cmd']) for key in d_nl2bash]
    tuple_ainix = [(d_ainix[key]['invocation'], d_ainix[key]['cmd']) for key in d_ainix]
    tuple_all = list(set(tuple_nl2bash + tuple_ainix))

    d = {}
    for idx, t in enumerate(tuple_all):
        temp = {}
        temp['invocation'] = t[0]
        temp['cmd'] = [t[1]]
        d[str(idx+1)] = temp

    def normalizer(text):
        for keyword in KEYWORD_LIST:
            if keyword in text:
                return 'ARG'
        return text

    input_template_predictor = []
    input_argument_predictor = []
    for t in tuple_all:
        nl = t[0][0].lower() + t[0][1:]
        norm_nl = ' '.join(tokenizer.basic_tokenizer(nl, to_lower_case=False, lemmatization=False, remove_stop_words=True, correct_spell=False)[0])
        norm_nl_arg_replace = ' '.join([normalizer(item) for item in data_utils.nl_to_tokens(nl, tokenizer=tokenizer.ner_tokenizer)])

        cm = t[1]
        norm_cm = [normalizer(item.split('<FLAG_SUFFIX>')[0])
                   for item in data_utils.cm_to_tokens(cm, data_tools.bash_tokenizer, arg_type_only=True)]
        norm_cm_ref = [normalizer(item.split('<FLAG_SUFFIX>')[0])
                       for item in data_utils.cm_to_tokens(cm, data_tools.bash_tokenizer, arg_type_only=False)]
        args = []
        for c, r in zip(norm_cm, norm_cm_ref):
            if c != r:
                args.append(r)
        norm_cm = ' '.join(norm_cm)
        
        if len(args) > 0:
            source = norm_nl + ' SEP ' + norm_cm
            target = ' SEP '.join(args)
            input_argument_predictor.append((source, target))
        input_template_predictor.append((norm_nl_arg_replace, norm_cm))

    random.seed(18015651)
    random.shuffle(input_template_predictor)
    random.shuffle(input_argument_predictor)

    os.makedirs(os.path.join(os.getcwd(), 'corpus/template_predictor'), exist_ok=True)
    with open(os.path.join(os.getcwd(), 'corpus/template_predictor/train.nl'), 'w') as fwn, \
         open(os.path.join(os.getcwd(), 'corpus/template_predictor/train.cm'), 'w') as fwc:
        for example in input_template_predictor:
            fwn.write(example[0] + '\n')
            fwc.write(example[1] + '\n')
    with open(os.path.join(os.getcwd(), 'corpus/template_predictor/valid.nl'), 'w') as fwn, \
         open(os.path.join(os.getcwd(), 'corpus/template_predictor/valid.cm'), 'w') as fwc:
        for example in input_template_predictor[10247:]:
            fwn.write(example[0] + '\n')
            fwc.write(example[1] + '\n')
    with open(os.path.join(os.getcwd(), 'corpus/template_predictor/test.nl'), 'w') as fwn, \
         open(os.path.join(os.getcwd(), 'corpus/template_predictor/test.cm'), 'w') as fwc:
        for example in input_template_predictor[10247:]:
            fwn.write(example[0] + '\n')
            fwc.write(example[1] + '\n')

    os.makedirs(os.path.join(os.getcwd(), 'corpus/argument_predictor'), exist_ok=True)
    with open(os.path.join(os.getcwd(), 'corpus/argument_predictor/train.ctx'), 'w') as fwc, \
         open(os.path.join(os.getcwd(), 'corpus/argument_predictor/train.arg'), 'w') as fwa:
        for example in input_argument_predictor:
            fwc.write(example[0] + '\n')
            fwa.write(example[1] + '\n')
    with open(os.path.join(os.getcwd(), 'corpus/argument_predictor/valid.ctx'), 'w') as fwc, \
         open(os.path.join(os.getcwd(), 'corpus/argument_predictor/valid.arg'), 'w') as fwa:
        for example in input_argument_predictor[9830:]:
            fwc.write(example[0] + '\n')
            fwa.write(example[1] + '\n')
    with open(os.path.join(os.getcwd(), 'corpus/argument_predictor/test.ctx'), 'w') as fwc, \
         open(os.path.join(os.getcwd(), 'corpus/argument_predictor/test.arg'), 'w') as fwa:
        for example in input_argument_predictor[9830:]:
            fwc.write(example[0] + '\n')
            fwa.write(example[1] + '\n')


if __name__ == '__main__':
    main()

