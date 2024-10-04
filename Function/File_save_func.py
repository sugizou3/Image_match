import os


def write_list_2d(sheet, l_2d, start_row, start_col):
    for y, row in enumerate(l_2d):
        for x, cell in enumerate(row):
            sheet.cell(row=start_row + y,
                       column=start_col + x,
                       value=l_2d[y][x])

def create_folder_if_not_exists(folder_path):
    # フォルダが存在しない場合は作成する
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"フォルダ '{folder_path}' を作成しました。")
    else:
        print(f"フォルダ '{folder_path}' は既に存在します。")
        

def check_and_write_file(file_path):
    # ファイルが存在するかどうかをチェック
    if os.path.exists(file_path):
        # ファイルが存在する場合、書き替えるかどうかを確認
        overwrite = input(f"ファイル '{file_path}' は既に存在します。上書きしますか？ (y/n): ")
        if overwrite.lower() != 'y':
            print("ファイルの上書きを中止しました。")
            return
    # # ファイルに書き込む
    # with open(file_path, 'w', encoding='utf-8') as f:
    #     f.write(content)
    # print(f"ファイル '{file_path}' に書き込みました。")