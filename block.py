import json
import os
import hashlib

# Находим папку blockchain относительно нашей текущей папки
blockchain_dir = os.curdir + '/blockchain/'


# Считаем hexdigest файла переданного в filename
def get_hash(filename):
#    blockchain_dir = os.curdir + '/blockchain/'
# 'rb' - открываем в двоичном виде
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()



def check_integrity():
#    blockchain_dir = os.curdir + '/blockchain/'
# Получаем список файлов из папки blockchain
    files = os.listdir(blockchain_dir)
# переводим имена файлов в int и сортируем по порядку (от 1 по возрастанию)
    files = sorted([int(i) for i in files])

# По очереди для всех файлов, кроме первого (он генезис блок и не имеет Hash предыдущего блока)
    for file in files[1:]:
# Открываем файл
        f = open(blockchain_dir + str(file))
# загружаем из файла в json формате значение соответсвующее 'hash'
        h = json.load(f)['hash']
        prev_file = str(file - 1)
        actual_hash = get_hash(prev_file)

        if h == actual_hash:
            res = 'OK'
        else:
            res = 'Corrupted'
        print('block {} is: {}'.format(prev_file, res))

def write_block(name, amount, to_whom, prev_hash=''):
#    blockchain_dir = os.curdir + '/blockchain/'

    files = sorted(os.listdir(blockchain_dir))
    files = sorted([int(i) for i in files])

    last_file = files[-1]

    filename = str(last_file + 1)

    prev_hash = get_hash(str(last_file))

    #    print(filename)

    data = {'name': name,
            'amount': amount,
            'to_whom': to_whom,
            'hash': prev_hash}
    with open(blockchain_dir + filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    #    write_block(name='ivan', amount=2, to_whom='katja')
    check_integrity()


if __name__ == '__main__':
    main()
