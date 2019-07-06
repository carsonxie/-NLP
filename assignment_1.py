import random
import re
import jieba
import pandas as pd
from collections import Counter

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

#use re
def token(string):
    return re.findall('\w+', string)


#load file and clean the file, return all text
def load_and_clean(file_name):
    
    #must add parameter header
    data = pd.read_csv(file_name, sep='\t',header=None)
    articles = data[0].tolist()
    #print(len(articles)) #len = 12889
    clean_text = []

    for line in articles:
        #split by special symbol
        split_by_str = line.strip().split('++$++')
        
        #remove token line '?' in a string
        remove_symbol = token(split_by_str[2])
        clean_text.append(remove_symbol)
    
    #concatenate all str in a 2-d-list into one long str
    one_d_str =[]
    for i in range(12889):
        one_d_str.append(clean_text[i][0])
    join_text = ''.join(one_d_str)
    
    join_text_file = open("join_text.txt", "w")
    join_text_file.write(join_text)
    join_text_file.close()
    return join_text
        
def cut(string):
    
    join_text = string
    with_jieba_cut = Counter(jieba.cut(join_text))
    
    #print(with_jieba_cut.most_common()[:10])
    return with_jieba_cut.most_common()[:20]



     
#1-gram model
def prob_1(word):

    token_list = []
    for i, line in enumerate((open('join_text.txt'))):
        if i % 100 == 0: print(i)
        
        if i > 10000: break    
    token_list += cut(line)
    #print(token_list)



    return Counter(word) / len(token_list)



def main():
    

    #print(create_grammar(adj_grammar))
    #ex_grammar = create_grammar(waitress, split = '=')
    #print(ex_grammar)
    
    generate_n(10)

    file_name = '/home/carson/Desktop/开课吧－nlp/AI-and-NLP-course/train.txt'
    join_text = load_and_clean(file_name)
    jieba_cut_summary = cut(join_text)
    print(jieba_cut_summary)
    #print(prob_1('你'))


if __name__ == "__main__":
    main()