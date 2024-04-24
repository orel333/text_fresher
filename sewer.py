# sew rows from table to one text document

import os

import pandas as pd

from utils import RESULT_DIR, SOURCE_DIR


def main():
    """Manager."""
    source_file_name = 'scenario_edited.xlsx'
    result_file_name = 'scenario_edited.txt'
    source_path = os.path.join(SOURCE_DIR, source_file_name)
    result_path = os.path.join(RESULT_DIR, result_file_name)
    extract_text(source_path, result_path)


def extract_text(
        source_path: os.PathLike,
        result_path: os.PathLike
):
    """Extracts text from Excel file."""
    print(source_path)
    text_df = pd.read_excel(
        source_path,
        engine='openpyxl',
        sheet_name='edited',
        index_col=0
    )
    text_df.sort_index(inplace=True)
    print(text_df.columns)
    print(text_df.head(10))
    pro_text = text_df['Construction'].to_list()
    with open(result_path, 'w', encoding='UTF-8') as result_file:
        for item in pro_text:
            if item == '<break>':
                result_file.write('\n')
            else:
                item = item.strip()
                result_file.write(item)
                result_file.write(' ')


if __name__ == '__main__':
    main()
