## %% import packages:
import webbrowser
import time
from wcwidth import wcswidth
import datetime
import json
import html
import importlib
import importlib.util
from collections import Counter
import pandas as pd
import re   # for regular expressions
#import nltk  # for text manipulation
import string
import os
import sys
import pickle
import click
import pyautogui
# Since it doesnt work I try to import from miniforge
pd.options.mode.chained_assignment = None
click.clear()

# If commands are not detected use : source ~/.bash_profile

## %% Click options


@click.command()
# @click.option('--filename', type=str, help='CSV file stored in data_twitter',
#  required=True, prompt='What is the file you want to apply the ranom forest to?')
@click.argument("infile", type=str, required=True)
#@click.argument('wvmodel', type=str, required=False, default='trained_wash_minn.model')
@click.option('--new', help='If you are classiying new data', is_flag=True, required=False, default=False, show_default=True)
@click.option('--os', help='your operating system[windows|mac]. default=windows', type=str, required=False, default='windows', show_default=True)
# @click.argument("protfile", type=click.File("w", encoding="txt"), default="-")
# @click.argument("nonprotfile", type=click.File("w", encoding="txt"), default="-")
## %% Click definition :
##
#infile = 'cat_esp_twitter500'
#new = False
def cli(infile, new,os):
    df = pd.read_csv(f'./{infile}.csv', low_memory=False)
    click.secho(f'The  file {infile} is being processed',
                fg='yellow', bg='red', bold=True)
    if os == 'mac':
        key = 'command'
    elif os == 'windows':
        key = 'ctrl'
    if new:
        click.secho('YOU ARE ABOUT TO RE-START CLASSIFICATION OF AN OLD FILE')
        old_file = click - \
            prompt(
                'Whats the name of the old file?[name without .csv]', bg='white', fg='blue')
        existing = pd.read_csv(
            f'./classified/{old_file}.csv')
        last = click.secho('What is the last row you classified?',
                           type=int, bg='white', fg='blue')
        # last = existing['index'].iloc[-1]
        click.secho(f'Starting classification where you left it, in row {last}',
                    fg='yellow', bg='red', bold=True)
        df = existing.loc[last:].reset_index()
        infile = click.secho(
            'Name to store the new file [name without .csv]', bg='white', fg='blue')

    print('---------------------------------')
    print('---------------------------------')
    click.secho('The shape of the  data is '
                + str(df.shape), fg='blue', bg='white')
    init_len = len(df)
    df['url'] = df['text'].apply(lambda x: re.findall(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", x))
    df = df.reset_index()
    df['lang'] = ""
    df['text1'] = ""
    df['text2'] = ""
    df['image'] = ""
    df['video'] = ""

    check = click.prompt(
                f'Do you want to store the file ./classified/{infile}_coded.csv  [y|n]', default='n')
    if check == 'n':
        exit()
    how_many = click.prompt(
        'How many tweets do you want to classify? Default=all', default=len(df))
    for i in range(0, how_many):
        print(_text(df, i))
        #print(protesters_top['text'][i])
        x = click.prompt(
            'Do you want to open the url? [y|n] ', default='y')
        if x in ['y'] and df['url'][i] != []:
            webbrowser.open(df.url[i][0], new=2)
            time.sleep(10)
            pyautogui.hotkey(key, 'w')
            time.sleep(1)
            pyautogui.hotkey(key, 'tab')
            time.sleep(1)
        click.secho('--Language--| 0=Other | 1=Cat | 2=Esp | 3=Both |',
                    fg='blue', bg='white')
        y1 = click.prompt(
            'Whats the tweets language?[0,1,2,3]')
        #pyautogui.hotkey('command','alt','f')
        df['lang'][i] = y1
        print('-'*80)
        print('-'*80)
        click.secho(
            '--Image content-- | 0=None | 1=Peaceful | 2=Violent | 3=Unrelated', fg='blue', bg='white')
        y2 = click.prompt(
            'Hows the image content?[0,1,2,3]', type=int)
        df['image'][i] = y2
        print('-'*80)
        print('-'*80)
        click.secho(
            '--Video content-- | 0=None | 1=Peaceful | 2=Violent | 3=Unrelated', fg='blue', bg='white')
        y3 = click.prompt(
            'Hows the video content?[0,1,2,3]', type=int)
        df['video'][i] = y3
        print('-'*80)
        print('-'*80)
        click.secho(
            '--TEXT CONTENT 1-- | 0=Unrelated | 1=Peaceful | 2=Violent | 3=Neutral', fg='red', bg='white')
        y4 = click.prompt(
            'Hows the text1 content?[0,1,2,3]', type=int)
        df['text1'][i] = y4
        print('-'*80)
        print('-'*80)
        click.secho('0=Unrelated')
        click.secho(
            ' 1=For democracy \n 2=For independence \n 3=For catalan government', fg='green')
        click.secho(
            ' 4=Against spanish gov \n 5= Against police \n 6=Against spanish institutions', fg='red')
        click.secho(
            ' 7=Against referendum/voting \n 8= Against independence \n 9=Against catalan gov', fg='red')
        click.secho(
            ' 10=For spanish gov \n 11= For police \n 12=For spanish institutions', fg='blue')
        click.secho('13=Sadness')
        y5 = click.prompt(
            'Hows the text2 content?[0,1,2,3,...,13]', type=int)
        df['text2'][i] = y5
        df.to_csv(
            f'./classified/{infile}_coded.csv', index=False)

        print('-'*80)
        print('-'*80)


#
#
#
## %% Other functions:


def _border(text, width=75):
    text_no_colors = click.unstyle(text)
    margin = (width - wcswidth(text_no_colors) - 4) * ' '
    return f'┃ {text}{margin} ┃'


def _textwrap(s, width=75):
    # it would be nice to use textwrap module here but we need to factor in
    # the actual terminal display of unicode characters when splitting
    if '\n' in s:
        parts = s.split('\n', 1)
        return _textwrap(parts[0], width) + [''] + _textwrap(parts[1], width)

    words = re.split(r'(\s+)', s)
    lines = []
    line = ''
    while len(words) > 0:

        # get the next word
        word = words.pop(0)

        # the word needs to be split
        if wcswidth(word) > width:

            # figure out where to break
            for pos in range(0, len(word)):
                if wcswidth(word[0:pos]) >= width - 4:
                    break

            lines.append(word[0:pos])
            words.insert(0, word[pos:])

        # the word caused the line to wrap
        elif wcswidth(line) + wcswidth(word) > width:
            lines.append(line)
            line = word

        # this is the first word on the line
        elif line == '':
            line = word

        # just adding another word to the line
        else:
            line += word

    if line != '':
        lines.append(line)

    return lines


def _text(tweet, i, width=75):

    # the top line
    body = ['┏' + '━' * (width - 2) + '┓']

    # add author
    body.append(
        _border(
            click.style(
                '@'
                + ' - ',                fg='yellow'
            ),
            width
        )
    )

    # blank line
    body.append(_border('', width))

    # add the text of the tweet
    tweet_text = html.unescape(tweet['text'][i])
    body.extend(
        map(
            lambda s: _border(s, width),
            _textwrap(
                tweet_text,
                width=width - 4
            )
        )
    )

    # blank line
    body.append(_border('', width))

    # the date
    #Luis: I got some datasets without dates so I put an exception here:
    try:
        created = str(maya.parse(tweet['created_at'][i], strict=False))
    except:
        created = ''
    #m = tweet['public_metrics'][i]
    metrics = (
        f'♡'
        f'♺'
        f'↶'
        f'«'
    )

    padding = (width - 4 - wcswidth(created + metrics)) * ' '

    body.append(
        _border(
            click.style(
                created
                + padding
                + metrics,
                fg='green'
            ),
            width
        )
    )

    # the bottom line
    body.append('┗' + '━' * (width - 2) + '┛')
    return '\n'.join(body)


#
#
#
#
#
#
