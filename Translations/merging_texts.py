#!/usr/bin/python3
#
# Files:
# - dialogue.txt
# - Translated_Dialogue.txt
# - Output.txt
#
# Copyright (C) RootTool
# Copyright (C) Kinderfeld
#
# This file is part of ACLS Remake.
#
# ACLS Remake is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# ACLS Remake is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with ACLS Remake. If
# not, see <https://www.gnu.org/licenses/>.

import os
from typing import Set, List


def combine_files_line_by_line(file1_path: str, file2_path: str, output_path: str = 'output.txt') -> None:
    """
    Комбинирует текст из двух файлов, создавая один выходной с чередующимися
    старыми/новыми строками.

    Аргументы:
        file1_path (str): Путь до первого файла.
        file2_path (str): Путь до второго файла.
        output_path (str): Путь до выходного файла. По умолчанию - 'output.txt'.

    Возвращает:
        None: Ничего.
    """

    existing_originals: Set[str] = set()

    with open(file1_path, 'r', encoding='utf-8') as f1, \
            open(file2_path, 'r', encoding='utf-8') as f2, \
            open(output_path, 'w', encoding='utf-8') as out:

        lines1: List[str] = [line.strip().replace('"', "'") for line in f1.readlines()]
        lines2: List[str] = [line.strip().replace('"', "'") for line in f2.readlines()]

        max_lines: int = max(len(lines1), len(lines2))

        for i in range(max_lines):
            line1: str = lines1[i] if i < len(lines1) else ''

            if not line1 or line1 in existing_originals:
                continue

            existing_originals.add(line1)
            line2: str = lines2[i] if i < len(lines2) else ''

            out.write(f'    old "{line1}"\n    new "{line2}"\n\n')

    print(f"[combine_files_line_by_line()]: Результат сохранён в файл: {output_path}")


def prepend_text(filename: str, text_to_add: str) -> None:
    """
    Редактирует указанный файл, добавляя определенный текст в начало файла.

    Аргументы:
        filename (str): Путь до файла для редактирования.
        text_to_add (str): Текст для добавления.

    Возвращает:
        None: Ничего.
    """

    with open(filename, 'r+', encoding='utf-8') as file:
        content: str = file.read()
        file.seek(0, 0)
        file.write(text_to_add + '\n' + content)

    print("[prepend_text()]: Готово!")


def remove_empty_lines(filename: str) -> None:
    """
    Редактирует указанный файл, удаляя в нем пустые строки.

    Аргументы:
        filename (str): Путь до файла для редактирования.

    Возвращает:
        None: Ничего.
    """

    with open(filename, 'r', encoding='utf-8') as file:
        lines: List[str] = file.readlines()

    non_empty_lines: List[str] = [line for line in lines if line.strip()]

    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(non_empty_lines)

    print('[remove_empty_lines()]: Готово!')


def split_file(input_file: str, lines_per_file: int = 10, output_dir: str = "split_files") -> None:
    """
    Разделяет указанный файл на n-ное количество файлов в указанной директории,
    базируясь на максимальной количестве строк в одном файле.

    Аргументы:
        input_file (str): Входной файл для разбиения.
        lines_per_file (int): Максимально допустимое количество строк в одном файле. По умолчанию - 10.
        output_dir (str): Выходная директория, содержащая все файлы, созданные во время разбиения.

    Возвращает:
        None: Ничего.
    """

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as file:
        lines: List[str] = file.readlines()

    total_files: int = (len(lines) + lines_per_file - 1) // lines_per_file

    for i in range(total_files):
        start_idx: int = i * lines_per_file
        end_idx: int = start_idx + lines_per_file
        chunk: List[str] = lines[start_idx:end_idx]

        output_file: str = os.path.join(output_dir, f"part_{i + 1}.txt")

        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(chunk)

    print(f"[split_file()]: Файл разбит на {total_files} частей по {lines_per_file} строк в папке '{output_dir}'.")


if __name__ == '__main__':
    original_dialogue_path: str = 'dialogue.txt'
    translated_dialogue_path: str = 'Translated_Dialogue.txt'
    file_out: str = 'Output.txt'
    combine_files_line_by_line(original_dialogue_path, translated_dialogue_path, file_out)
    prepend_text(file_out, 'translate russian strings:')

    # remove_empty_lines('Translated_Dialogue.txt')
    # split_file('dialogue.txt', 150)
