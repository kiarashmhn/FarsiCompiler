# -*- coding: utf-8 -*-
from googletrans import Translator
import sys

args_list = sys.argv
if '-en2fa' in args_list:
    mode = 2
elif '-fa2en' in args_list:
    mode = 1
else:
    raise ('mode is not defined')
if '-src' in args_list:
    src = args_list[args_list.index('-src') + 1]
else:
    src = 'src.txt'
if '-dst' in args_list:
    dst = args_list[args_list.index('-dst') + 1]
else:
    dst = 'dst.txt'

translator = Translator()


def fa2EngAlphabets():
    result = {}
    with open('_alphabetsFa.txt') as f:
        for line in f:
            line = line.strip()
            tmp = line.split(' ')
            result[tmp[0]] = tmp[1]
    return result


def fa2EngKeyword():
    result = {}
    with open('_keywords.txt') as f:
        for line in f:
            line = line.strip()
            tmp = line.split(' ')
            result[tmp[0]] = tmp[1]
    return result


def eng2FaAlphabets():
    result = {}
    with open('_alphabetsEng.txt') as f:
        for line in f:
            line = line.strip()
            tmp = line.split(' ')
            result[tmp[0]] = tmp[1]
    return result


def eng2FaKeyword():
    result = {}
    with open('_keywords.txt') as f:
        for line in f:
            line = line.strip()
            tmp = line.split(' ')
            result[tmp[1]] = tmp[0]
    return result


def remove(text):
    newText = []
    for line in text:
        newline = line[0:len(line) - 1]
        newText.append(newline)
    return newText


def translated(mode, src, dst):
    dict_word = fa2EngKeyword() if mode == 1 else eng2FaKeyword()
    dict_alphabet = fa2EngAlphabets() if mode == 1 else eng2FaAlphabets()
    with open(src) as f:
        oldText = f.readlines()
        text = remove(oldText)
        translate = []
        for line in text:
            words = line.split(' ')
            tLine = []
            i = 0
            while i < len(words):
                word = words[i]
                if word == '':
                    tLine.append(' ')
                    i += 1
                elif word[0] == "'":
                    sentence = word[1:] + ' '
                    i += 1
                    word = words[i]
                    while word[-1] != "'":
                        sentence += word + ' '
                        i += 1
                        if i == len(words):
                            word = "'"
                        else:
                            word = words[i]
                    sentence += word[:-1]
                    i += 1
                    sentence = sentence[0:-4]
                    if mode == 1:
                        tLine.append('"' + translator.translate(sentence, src='fa').text + '"')
                    else:
                        tLine.append('"' + translator.translate(sentence, dest='fa').text + '"')

                elif word[0] == '"':
                    sentence = word[1:] + ' '
                    i += 1
                    word = words[i]
                    while word[-1] != '"':
                        sentence += word + ' '
                        i += 1
                        if i == len(words):
                            word = '"'
                        else:
                            word = words[i]
                    sentence += word[:-1]
                    i += 1
                    sentence = sentence[0:-4]
                    if mode == 1:
                        tLine.append('"' + translator.translate(sentence, src='fa').text + '"')
                    else:
                        tLine.append('"' + translator.translate(sentence, dest='fa').text + '"')


                elif word in dict_word:
                    tLine.append(dict_word[word])
                    i += 1
                elif word in dict_alphabet:
                    tLine.append(word)
                    i += 1
                else:
                    if mode == 1:
                        tLine.append(translator.translate(word, src='fa').text)
                    else:
                        tLine.append(translator.translate(word, dest='fa').text)
                    i += 1
            translate.append(tLine)

    with open(dst, 'w') as f:
        for line in translate:
            for word in line:
                if word == ' ':
                    f.write(word)
                else:
                    f.write(word + ' ')
            f.write('\n')


translated(mode, src, dst)
