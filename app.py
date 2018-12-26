import os

from flask import Flask, request, jsonify, send_from_directory
from googletrans import Translator
import sys

from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='/Users/kiarash/Desktop/FaCompiler')

UPLOAD_FOLDER = '/Users/kiarash/Desktop/FaCompiler'
ALLOWED_EXTENSIONS = set(['txt', 'py'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 1 : Fa to En
# 2 : En to Fa


translator = Translator()


@app.route('/<int:mode>', methods=['POST'])
def translate(mode):
    if 'file' not in request.files:
        out = {'status': 'No file part!'}
        return jsonify(out), 400
    file = request.files['file']

    if file.filename == '':
        out = {'status': 'No selected file!'}
        return jsonify(out), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        src = filename
        dst = 'dst.txt'
        translated(mode, src, dst)
        out = {'file': '/dst.txt'}
        return jsonify(out), 200
    else:
        out = {'status': 'File type not allowed!'}
        return jsonify(out), 400


@app.route('/<filename>', methods=['GET'])
def get_result(filename):
    return send_from_directory(app.static_folder,
                               filename), 200


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
