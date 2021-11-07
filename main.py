from bs4 import BeautifulSoup
import requests
import json

link = 'https://career.habr.com/api/frontend/vacancies?sort=relevance&type=all&with_salary=true&currency=RUR&page={' \
       'page} '


def search(div):
    chose = []
    vacan = []
    print("Выберите тип занятости (если несколько, через пробел):")
    print("1 - Частичная занятость; 2 - Полная занятость; 3 - Удаленная работа; ")
    emp = input().split()
    f = open('vacancies.txt', 'r')
    for i in f:
        if i != '\n':
            vacan.append(i.rstrip())
        try:
            xan = i.rstrip().split()
            if xan[0] == "Занятость:":
                for j in emp:
                    xanax = ' '.join(xan[1:6]).split(', ')
                    if j == '1' and xanax[1] == "Частичная занятость" and vacan not in chose:
                        chose.append(vacan)
                    if j == '2' and xanax[1] == "Полная занятость" and vacan not in chose:
                        chose.append(vacan)
                    if j == '3' and xanax[0] == "Возможна удаленная работа," and vacan not in chose:
                        chose.append(vacan)

        except IndexError:
            vacan = []
    print("Ответьте на вопросы о вашей заинтерисованности (1 - Да; 2 - Нет):")
    div = set(div)
    theme = list()
    for i in div:
        print('Вы заинтересованы в ', i, '?', sep='')
        if int(input()) == 1:
            theme.append(i)
    final = list()
    for i in chose:
        for j in theme:
            if j in i:
                final.append(i)
    if len(final) == 0:
        print("Ничего не нашлось:(")
        return 0
    print("Вам скорее всего подходит: ")
    for i in final:
        for j in i:
            print(j)
        print()


def ft(f):
    c = 1
    employm = ''
    sk = ''
    work = []
    emp = []
    div = []
    for k in range(4):
        content = requests.get(link.format(page=k + 1))
        for i in json.loads(content.content)["list"]:
            for z in range(len(i["skills"])):
                if z != len(i["skills"]) - 1:
                    sk += i["skills"][z]["title"] + ", "
                else:
                    sk += i["skills"][z]["title"]
            work.append(sk)
            if i["remoteWork"]:
                employm += "Возможна удаленная работа, "
            if i["employment"] == "full_time":
                employm += "Полная занятость"
            if i["employment"] == "part_time":
                employm += "Частичная занятость"
            emp.append(employm)
            t = "Вакансия №{num} (Ссылка: https://career.habr.com{href})\n{title}\nЗарплата: {salary}\nНавыки и " \
                "требования:\n{div}\n{" \
                "skills}\nЗанятость: {employ}\n\n"
            div.append(i["divisions"][0]["title"])
            f.write(t.format(num=c, href=i["href"], title=i["title"], employ=employm, salary=i["salary"]["formatted"],
                             div=i["divisions"][0]["title"], skills=sk))
            c += 1
            employm = ''
            sk = ''
    return work, emp, div


def main():
    f = open('vacancies.txt', 'w')
    work, emp, div = ft(f)
    f.close()
    search(div)


if __name__ == "__main__":
    main()
