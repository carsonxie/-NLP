import random
import re
import jieba
import pandas as pd

simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>  蓝色的 | 好看的 | 小小的
"""

adj_grammar = """
Adj* => null | Adj Adj*
Adj => 蓝色的 | 好看的 | 小小的
"""

#my first grammar
customer = """
customer = 自己　动作　需求
自己　= 我 | 俺 | 我们
动作 = 需要|　想
需求　=  下单　|　点菜　|打包　"""


#my second grammar
waitress = """
waitress =　寒暄 报数 询问 业务相关 结尾 
报数　=　我是　数字　号，
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 | 欢迎光临海面捞,
询问 = 请问你要 | 您需要
业务相关 = 具体业务
具体业务 = 鸳鸯锅 | 酒单 | 今日推荐 
结尾 = 吗？
"""


def adj():  
    return random.choice('蓝色的 | 好看的 | 小小的'.split('|')).split()[0]


def adj_star():
    return random.choice([lambda : '', lambda : adj() + adj_star()])()



def create_grammar(grammar_str, split= '=>', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip(): continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar
 


def generate(gram, target):
    choice = random.choice
    if target not in gram:
        return target
    expaned = [generate(gram, t) for t in choice(gram[target])]
    return ''.join([e if e != '/n' else '\n' for e in expaned if e != 'null'])


def generate_n(n_sentence):
    for i in range(n_sentence):
        print(generate(gram = create_grammar(waitress, split = '='), target = 'waitress'))


#part 2 
#load file and clean the file
def load_and_clean(file_name):
    data = pd.read_csv(file_name, sep='\t')
    print(data.head())










def main():
    

    #print(create_grammar(adj_grammar))
    #ex_grammar = create_grammar(waitress, split = '=')
    #print(ex_grammar)
    
    #generate_n(10)

    file_name = '/home/carson/Desktop/开课吧－nlp/AI-and-NLP-course/train.txt'
    load_and_clean(file_name)


main()