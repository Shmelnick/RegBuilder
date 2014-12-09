# coding: utf8
__author__ = 'antre'
from os import listdir
from os.path import isfile, join
import argparse
import readline


def parse_args():
    """
    Парсинг аргументов командной строки
    """
    c_l_parser = argparse.ArgumentParser(description='Преобразование урлов к регуляркам')
    c_l_parser.add_argument('-c', dest='dom', type=str, required=True, help='Исследуемый домен')
    return c_l_parser.parse_args()


def main():
    args = parse_args()
    mydom = args.dom
    outfile = open("res_reg", 'a')
    outfile_with_skipped = open("skipped", 'a')

    li = list()

    only_files = [f for f in listdir('auto_extract') if isfile(join('auto_extract', f))]
    for f in only_files:
        opened = open(join('auto_extract', f), 'rb')
        for line in opened:
            line = line.strip()[1:-1]
            if mydom in line:
                li.append((line.replace(".", "\."), f))

    for e in li:
        print e

    list_of_additions = list()
    list_of_additions.append(".*")

    for e in li:
        stop_it = False
        while not stop_it:
            print ">>", e
            readline.set_startup_hook(lambda: readline.insert_text(e[0]))
            s = raw_input()
            s = s.strip().split(" ")
            if len(s) == 1:
                # Со всем согласны
                outfile.write(s[0] + "\t" + e[1] + "\n")
                print "OK", s[0]
                stop_it = True
            elif s[1] == 'x':
                print "Не добавляем, сохранили в исключения"
                outfile_with_skipped.write(s[0] + "\t" + e[1] + "\n")
                stop_it = True
            elif s[1] == 's':
                print "Скипнули"
                stop_it = True
            elif s[1] == 'a':
                try:
                    list_of_additions.append(s[2])
                    print "Добавлено", len(list_of_additions) - 1, s[2]
                except IndexError:
                    print "Нужно выражение"
            elif s[1] == "l":
                print "Выводим список добавочных выражений"
                for i, el in enumerate(list_of_additions):
                    print i, el
            else:
                try:
                    code = int(s[1])
                    if code <= 0:
                        code += len(s[0])
                    else:
                        sss = s[0].split("/")
                        am_of_slashes = int(s[1][0])
                        le = len("/".join(sss[0:am_of_slashes])) + 1
                        code = le
                        try:
                            code += int(s[1][1:])
                        except ValueError:
                            pass

                    try:
                        # Индекс выражения из добавочных
                        code_of_addition = int(s[2])
                        new_s = s[0][:code] + list_of_additions[code_of_addition] + s[0][code:]
                    except ValueError:
                        # Там не индекс, а полноценное выражение
                        new_s = s[0][:code] + s[2] + s[0][code:]
                    e = (new_s, e[1])
                except (ValueError, IndexError):
                    print "Неправильный формат"


if __name__ == '__main__':
    main()