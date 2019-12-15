import re
import click
import requests
from pathlib import Path
from inspect import cleandoc
from lxml import html
from functools import wraps
import shelve

import click

from config import cookies


ok = click.style('✔︎', fg='green')
fail = click.style('✘', fg='red')
db = shelve.open('answers.db')


class Data(str):

    @property
    def int_lines(self):
        return [int(x) for x in self.splitlines()]

    @property
    def ints_lines(self):
        return [
            [int(x) for x in re.findall(r'-?\d+', line)]
            for line in self.splitlines()
        ]


def test(cases):
    def decorator(f):
        imported = __import__(f.__module__)
        if imported.__name__ != '__main__':
            return f
        path = Path(imported.__file__)
        day = int(re.search(r'\d+', path.name).group(0))
        part = f.__name__.replace('_', ' ')
        click.secho(f'day {day}, {part}')
        tests_ok = True
        for case, expected in cases.items():
            case = cleandoc(case)
            case_pretty = case.replace('\n', ', ')
            data = Data(case)
            result = f(data)
            if result == expected:
                click.secho(f'{ok} {case_pretty} == {result}')
            else:
                print(f'{fail} {case_pretty} == {result}, expected {expected}')
                tests_ok = False
        if tests_ok:
            data = load_input(day)
            result = f(data)
            click.secho(f'{result}\n')
            if result is not None:
                post_answer(result, day, part.split()[-1])
        else:
            click.secho('tests failed\n', fg='red')
        return f
    return decorator


def input_file(day):
    return Path(f'inputs/day{day:02d}.txt')


def download_input(day, year=2019):
    r = requests.get(f'http://adventofcode.com/{year}/day/{day}/input', cookies=cookies)
    r.raise_for_status()
    path = input_file(day)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(r.text)
    print(f'downloaded input for day {day}')


def load_input(day):
    path = input_file(day)
    if not path.exists():
        download_input(day)
    return Data(path.read_text())


def classify_answer_response(text):
    if "That's the right answer" in text:
        return True
    if "That's not the right answer" in text:
        return False
    if "You gave an answer too recently" in text:
        raise TimeoutError(text)
    if "You don't seem to be solving the right level" in text:
        return None


def post_answer(answer, day, part, year=2019):
    key = f'{year}.{day}.{part}.{answer}'
    text = db.get(key)
    if not text:
        url = f'https://adventofcode.com/{year}/day/{day}/answer'
        r = requests.post(
            url, data={'level': part, 'answer': answer}, cookies=cookies)
        r.raise_for_status()
        h = html.fromstring(r.content)
        text = h.xpath('//article')[0].text_content().rpartition(' [')[0]
        if classify_answer_response(text) in (True, False):
            db[key] = text

    kind = classify_answer_response(text)
    colors = {True: 'green', False: 'red', None: 'yellow'}
    click.secho(text, fg=colors[kind], bold=True)
    return text
