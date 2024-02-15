import numpy as np
import pandas as pd
import itertools

def emma(data, minsup):
    episodes = []
    global compositte_episode
    
    for sequence in data:
        count_of_support = {}

        #step1-3
        [count_of_support.setdefault(sequence[i], []).append(i) for i in range(len(sequence))] #eventのsupportを数える
        occurr = {key:value for key, value in count_of_support.items() if len(value) >= minsup} #sup >= minsup のeventだけ保持
        compositte_episode = occurr.copy()
        key_list = list(occurr.keys())

        #Serial Extension
        for key_idx in range(len(key_list)):
            for key_idx_2 in range(len(key_list)):
                #sup >= minsup then continue, else break
                bool_list = list(map(lambda comp_value: comp_value in occurr[key_list[key_idx_2]], list(map(lambda value: value+1, occurr[key_list[key_idx]]))))
                sup = bool_list.count(True)

                if sup >= minsup:
                    extension_ep = {}
                    key = (key_list[key_idx], key_list[key_idx_2])
                    extension_ep.setdefault(key, []).append([value for value, bool_data in zip(occurr[key_list[key_idx]], bool_list) if bool_data == True])
                    extension_ep[key] = list(np.array(list(extension_ep.values())).flatten())
                    compositte_episode.update(extension_ep)
                    emma_join(extension_ep, occurr, key_list, minsup)
        episodes.append(compositte_episode)

    return episodes
            
            
def emma_join(episode, origin_dic, key_list, minsup):

    key_length = len(list(episode.keys())[0])
    
    #Serial Extensionされたepisode(長さ2以上)に対して、その後にfrequent eventが続くかどうかを探索
    for key_idx in range(len(key_list)):
        #bound_listの各要素(出現位置)+key_length-1でend_time(直後に続くイベントの出現位置)が出せることを利用
        bool_list = list(map(lambda comp_value: comp_value+key_length in list(map(lambda value: value, origin_dic[key_list[key_idx]])), list(np.array(list(episode.values())).flatten())))
        sup = bool_list.count(True)

        if sup >= minsup:
            key = tuple(list(list(episode.keys())[0])+[key_list[key_idx]])
            extension_ep = {}
            extension_ep.setdefault(key, []).append([value for value, bool_data in zip(list(np.array(list(episode.values())).flatten()), bool_list) if bool_data == True])
            extension_ep[key] = list(np.array(list(extension_ep.values())).flatten())
            compositte_episode.update(extension_ep) #Serial extensionしたepisodeを保存
            emma_join(extension_ep, origin_dic, key_list, minsup)


df = pd.read_csv('./test_sequence_multiple.csv',header=None)
data = df.to_numpy()
data = [list(itertools.chain.from_iterable(data))]

result = emma(data, 10)

for elem in result:
    keys_list = elem.keys()

    with open(f'test_result.txt', 'w', encoding='utf-8') as f:
        for key in keys_list:
            f.write(f'{key}:{elem[key]}\n')
