import os

import pandas as pd

from typing import Optional

try:
    from .utils import RESULT_DIR, SOURCE_DIR, make_dir_if_needed
except ImportError:
    from utils import RESULT_DIR, SOURCE_DIR, make_dir_if_needed


# TODO: не всегда точка - это прерывание 
# должны сохраняться изначальные предложения с первоначальными
# конечными знаками препинания, чтобы была возможность собрать такой же текст


def main() -> None:
    """Managing function."""
    make_dir_if_needed(RESULT_DIR)
    # here name of source
    SOURCE_FILE_NAME = 'scenario.txt'
    SOURCE_PATH = os.path.join(SOURCE_DIR, SOURCE_FILE_NAME)
    RESULT_FILE_NAME = SOURCE_FILE_NAME.split('.')[0] + '_result.xlsx'
    RESULT_PATH = os.path.join(RESULT_DIR, RESULT_FILE_NAME)
    paragraphs = get_paragraphs(SOURCE_PATH)
    construction = get_text_construction(paragraphs)
    print(construction)
    text_df = pd.DataFrame(
        data=construction,
        columns=['Construction']
    )
    text_df['Num of words'] = text_df['Construction'].apply(calculate_words)
    print(text_df)
    text_df['Complexity'] = text_df['Num of words'].apply(check_complexity)

    print(text_df)
    # print(text_df)
    text_df.to_excel(RESULT_PATH)


def get_text_construction(paragraphs: list) -> list:
    """Returns text construction."""
    # print(paragraphs)
    construction = []
    for paragraph in paragraphs:
        sentense = ''
        word = ''
        for symbol in paragraph:
            # print(sentense)
            if symbol == ' ' and sentense == '':
                continue
            elif symbol in (' ', ',', '-', '(', ')', '—', '+', ':'):
                if word in ('и т.', 'д.', 'и'):
                    word += symbol
                    sentense += symbol
                elif sentense and sentense[-1] in ('.', '!', '?', ';'):
                    construction.append(sentense)
                    word = ''
                    sentense = ''
                else:
                    sentense += symbol
                    word = ''
            else:
                word += symbol
                sentense += symbol
        if sentense == '':
            construction.append('<break>')
        else:
            construction.append(sentense)
            construction.append('<break>')
    return construction


def check_complexity(num_of_words: int) -> str:
    if num_of_words == 0:
        return ''
    if num_of_words <= 10:
        return 'Ideal'
    if 10 < num_of_words <= 15:
        return 'Acceptable'
    if num_of_words <= 30:
        return 'Difficult for understanding'
    if num_of_words > 30:
        return 'Impossible to understand'


def calculate_words(sentence: str) -> Optional[int]:
    """Calculate words to pronounce in sentence."""
    if sentence == '<break>':
        return 0
    sentence = (
        sentence.replace('-', ' ').replace(',', '').replace('(', '')
        .replace(')', '').replace('"', '').replace(':', '')
        .replace('+', '').replace('—', '').replace('.', ' ')
    )
    sentence_list = sentence.split()
    sentence_list_cleaned = [word for word in sentence_list if word != '']
    print(sentence_list_cleaned)
    return len(sentence_list_cleaned)


def get_paragraphs(source_path: os.PathLike) -> list:
    paragraphs = []
    with open(source_path, 'r', encoding='UTF-8') as source_file:
        raw_paragraphs = source_file.readlines()
    for raw_paragraph in raw_paragraphs:
        paragraphs.append(raw_paragraph.strip())
    return paragraphs


if __name__ == '__main__':
    main()
