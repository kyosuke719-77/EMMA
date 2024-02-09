import numpy as np
import pandas as pd
import tkinter
import tkinter.filedialog
from tkinter import ttk
import os
import re


#ファイルパスを取得
def get_filepath():
    fTyp = [('', 'csv')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    file_select.set(file_name)


#バリデーション関数
def isOk(value):
    
    if re.match(re.compile('[0-9]+'), value):
        return True

    return False


def execute_emma():
    file_path = file_select.get()
    file_name = result_name.get()
    minsup = minsup_value.get()
    check = bool_val.get()

    df = pd.read_csv(file_path)
    data_size = df.to_numpy().shape

    #入力データが1次元配列であるとき
    if data_size[0] == 0:
        data_size = list(data_size)
        data_size[0] = 1
    print(tuple(data_size))

    #全データを1系列として



def emma(data, data_size, minsup):
    episodes = []
    global compositte_episode
    
    for sequence in data:
        count_of_support = {}

        #step1-3
        [count_of_support.setdefault(sequence[i], []).append(i) for i in range(data_size[1])] #eventのsupportを数える
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


if __name__ == '__main__':

    main_window = tkinter.Tk()
    main_window.attributes('-topmost', False)
    main_window.title('EMMA')
    main_window.geometry("490x180")

    main_frm=ttk.Frame(main_window)
    # main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)
    tcl_isOK = main_window.register(isOk)

    #ファイル選択ラベル
    file_label = tkinter.Label(text='ファイル選択')
    file_label.place(x=13, y=25)

    #ファイル選択のウィジェット変数
    file_select = tkinter.StringVar()
    file_entry = ttk.Entry(textvariable=file_select, width=50)
    file_entry.place(x=80, y=25)

    #ファイル選択ボタン
    file_button = ttk.Button(text='参照', command=get_filepath)
    file_button.place(x=390, y=23)

    #出力ファイルラベル
    result_label = ttk.Label(text='ファイル名')
    result_label.place(x=19, y=55)

    #出力ファイル名入力欄
    result_name = ttk.Entry(width=50)
    result_name.place(x=80, y=55)

    #minsup入力欄
    minsup_labe = ttk.Label(text='minsup')
    minsup_labe.place(x=22, y=85)
    minsup_value = ttk.Entry(validate='key', validatecommand=(tcl_isOK, '%S'), textvariable=tkinter.StringVar())
    minsup_value.place(x=80, y=85)

    #チェックボックス
    bool_val = tkinter.BooleanVar()
    bool_val.set(False)
    check_box = ttk.Checkbutton(text='全データを1系列に変換する', variable=bool_val)
    check_box.place(x=20, y=115)

    #実行ボタン
    run_button = ttk.Button(text='実行', command=execute_emma)
    run_button.place(x=200, y=145)

    main_window.mainloop()





