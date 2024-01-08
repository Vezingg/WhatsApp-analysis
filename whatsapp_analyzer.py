#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import io
import sys
from collections import Counter
import emoji

from chatline import Chatline
from font_color import Color

parser = argparse.ArgumentParser(
    description='Read and analyze WhatsApp chat',
    usage="python whatsapp_analyzer.py FILE [-h] [-d] [-s] [-c]"
)

stop_words_options = ["arabic", "bulgarian", "catalan", "czech", "danish", "dutch", "english", "finnish", "french", "german", "hebrew", "hindi", "hungarian", "indonesian", "italian", "malaysian", "norwegian", "polish", "portuguese", "romanian", "russian", "slovak", "spanish", "swedish", "turkish", "ukrainian", "vietnamese"]

parser.add_argument('file',
                    metavar='FILE',
                    help='Chat file path')

parser.add_argument(
    '-d',
    '--debug',
    required=False,
    help="Debug mode. Shows details for every parsed line.", action="store_true")

parser.add_argument(
    '-s',
    '--stopword',
    required=False,
    choices=stop_words_options,
    metavar='',
    help="Stop Words: A stop word is a commonly used word (such as 'the', 'a', 'an', 'in').\
        In order to get insightful most common word mentioned in the chat, we need to skip these type of word.\
        The Allowed values are: " + ", ".join(stop_words_options))

parser.add_argument(
    '-c',
    '--customstopword',
    required=False,
    metavar='',
    help="Custom Stop Words. File path to stop word. File must a raw text. One word for every line"
)

args = parser.parse_args()

try:
    with io.open(args.file, "r", encoding="utf-8") as file:
        lines = file.readlines()

except IOError as e:
    print("File \"" + args.file + "\" not found. Please recheck your file location")
    sys.exit()

stop_words = []
if args.stopword:
    try:
        with io.open("stop-words/" + args.stopword + ".txt", "r", encoding="utf-8") as file:
            stop_words = [x.strip() for x in file.readlines()]
    except IOError as e:
        print("Stop Words file not found in \"" + args.file + "\" not found.")
        sys.exit()

if args.customstopword:
    try:
        with io.open(args.customstopword, "r", encoding="utf-8") as file:
            stop_words = [x.strip() for x in file.readlines()]
    except IOError as e:
        print("Stop Words file not found in \"" + args.file + "\" not found.")
        sys.exit()

chat_counter = {
    'chat_count': 0,
    'deleted_chat_count': 0,
    'event_count': 0,
    'senders': [],
    'timestamps': [],
    'words': [],
    'domains': [],
    'emojis': [],
    'fav_emoji': [],
    'fav_word': []
}

previous_line = None
for line in lines:
    chatline = Chatline(line=line, previous_line=previous_line, debug=args.debug)
    previous_line = chatline

    if chatline.line_type == 'Chat':
        chat_counter['chat_count'] += 1

    if chatline.line_type == 'Event':
        chat_counter['event_count'] += 1

    if chatline.is_deleted_chat:
        chat_counter['deleted_chat_count'] += 1

    if chatline.sender is not None:
        chat_counter['senders'].append(chatline.sender)
        for i in chatline.emojis:
            chat_counter['fav_emoji'].append((chatline.sender, i))

        for i in chatline.words:
            chat_counter['fav_word'].append((chatline.sender, i))

    if chatline.timestamp:
        chat_counter['timestamps'].append(chatline.timestamp)

    if len(chatline.words) > 0:
        chat_counter['words'].extend(chatline.words)

    if len(chatline.emojis) > 0:
        chat_counter['emojis'].extend(chatline.emojis)

    if len(chatline.domains) > 0:
        chat_counter['domains'].extend(chatline.domains)

def reduce_and_sort(data):
    return sorted(
        dict(
            zip(
                Counter(data).keys(),
                Counter(data).values()
            )
        ).items(),
        key=lambda x: x[1],
        reverse=True
    )

def reduce_and_filter_words(list_of_words):
    val = [w.lower() for w in list_of_words if (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)]
    return val

def filter_single_word(w):
    return (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)

def reduce_fav_item(data):
    exist = []
    arr = []
    for i in data:
        if i[1] > 0 and not i[0][0] in exist:
            exist.append(i[0][0])
            arr.append(i)
    return arr

chat_counter['senders'] = reduce_and_sort(chat_counter['senders'])
chat_counter['words'] = reduce_and_sort(reduce_and_filter_words(chat_counter['words']))
chat_counter['domains'] = reduce_and_sort(chat_counter['domains'])
chat_counter['emojis'] = reduce_and_sort(chat_counter['emojis'])
chat_counter['timestamps'] = reduce_and_sort([(x.strftime('%A'), x.strftime('%H')) for x in chat_counter['timestamps']])
chat_counter['fav_emoji'] = reduce_fav_item(reduce_and_sort(chat_counter['fav_emoji']))
chat_counter['fav_word'] = reduce_fav_item(reduce_and_sort([x for x in chat_counter['fav_word'] if filter_single_word(x[1])]))

def printBar(value, total, label='', prefix='', decimals=1, length=100, fill='█', printEnd="\r"):
    filledLength = int(value / (total / length))
    bar = fill * filledLength + '' * (length - filledLength)
    print("\r{} |{} {}".format(label, bar, Color.bold(str(value))), end=printEnd)
    print()

def printBarChart(data, fill="█"):
    if len(data) <= 0:
        print("Empty data")
        return

    total = max([x[1] for x in data])
    max_label_length = len(sorted(data, key=lambda tup: len(tup[0]), reverse=True)[0][0])
    for i in data:
        label = i[0] + " " * (max_label_length - len(i[0]))
        printBar(i[1], total, length=50, fill=fill, label=label)

def printCalendar(data):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours =
