import os

import pandas as pd

try:
    from .utils import RESULT_DIR, SOURCE_DIR, make_dir_if_needed
except ImportError:
    from utils import RESULT_DIR, SOURCE_DIR, make_dir_if_needed


def main() -> None:
    """Managing function."""
    make_dir_if_needed(RESULT_DIR)
    # here name of source
    SOURCE_FILE_NAME = 'scenario.txt'
    SOURCE_PATH = os.path.join(SOURCE_DIR, SOURCE_FILE_NAME)
    RESULT_FILE_NAME = SOURCE_FILE_NAME.split('.')[0] + '_result.xlsx'
    RESULT_PATH = os.path.join(RESULT_DIR, RESULT_FILE_NAME)
    sentences = get_sentences(SOURCE_PATH)
    print(sentences)
    text_df = pd.DataFrame(
        data=sentences,
        columns=['Sentences']
    )
    print(text_df)
    text_df['Num of words'] = text_df['Sentences'].apply(calculate_words)
    print(text_df)
    text_df['Complexity'] = text_df['Num of words'].apply(check_complexity)
    print(text_df)
    text_df.to_excel(RESULT_PATH)


def check_complexity(num_of_words: int) -> str:
    if num_of_words <= 10:
        return 'Ideal'
    if 10 < num_of_words <= 15:
        return 'Acceptable'
    if num_of_words <= 30:
        return 'Difficult for understanding'
    if num_of_words > 30:
        return 'Impossible to understand'


def calculate_words(sentence: str) -> int:
    """Calculate words to pronounce in sentence."""
    sentence = (
        sentence.replace('-', ' ').replace('.', '')
        .replace(',', '').replace(';', '').replace('(', '')
        .replace(')', '').replace('?', '').replace('!', '')
        .replace('"', '').replace(':', '').replace('+', '')
        .replace('—', '')
    )
    sentence_list = sentence.split()
    sentence_list_cleaned = [word for word in sentence_list if word != '']
    print(sentence_list_cleaned)
    return len(sentence_list_cleaned)


def get_sentences(source_path: os.PathLike) -> list:
    sentences = []
    with open(source_path, 'r', encoding='UTF-8') as source_file:
        paragraphs = source_file.readlines()
    print(paragraphs)
    for paragraph in paragraphs:
        paragraph = (
            paragraph.replace('!', '.').replace('?', '.').replace(';', '.')
        )
        paragraph_list = paragraph.split('.')
        for raw_sentence in paragraph_list:
            sentence = raw_sentence.strip()
            if sentence != '':
                sentence += '.'
                sentences.append(sentence)
    return sentences


if __name__ == '__main__':
    main()
