import numpy as np
import pandas as pd
import tkinter
import tkinter.filedialog
from tkinter import ttk
import os


#ファイルパスを取得
def get_filepath():
    fTyp = [('', 'csv')]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    file_select.set(file_name)



if __name__ == '__main__':

    main_window = tkinter.Tk()
    main_window.attributes('-topmost', False)
    main_window.title('EMMA')
    main_window.geometry("600x200")

    main_frm=ttk.Frame(main_window)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

    #ファイル選択ラベル
    file_label = tkinter.Label(main_frm, text='ファイル選択')
    file_label.grid(column=0, row=0, pady=10)

    #ファイル選択のウィジェット変数
    file_select = tkinter.StringVar()
    file_entry = ttk.Entry(main_frm, textvariable=file_select, width=50)
    file_entry.grid(column=1, row=0, pady=10)

    #ファイル選択ボタン
    file_button = ttk.Button(main_frm, text='参照', command=get_filepath)
    file_button.grid(column=2, row=0, pady=10)

    #出力ファイルラベル
    result_label = ttk.Label(main_frm, text='ファイル名')
    result_label.grid(column=0, row=1, pady=10)

    #出力ファイル名入力欄
    result_name = ttk.Entry(width=50)
    result_name.grid(column=0, row=1)

    #チェックボックス
    bool_val = tkinter.BooleanVar()
    bool_val.set(False)
    check_box = ttk.Checkbutton(text='全データを1系列に変換する', variable=bool_val)
    check_box.grid(column=0, row=2, pady=10)

    #実行ボタン
    run_button = ttk.Button(main_frm, text='実行')
    run_button.grid(column=1, row=4, pady=10)
    main_window.mainloop()





