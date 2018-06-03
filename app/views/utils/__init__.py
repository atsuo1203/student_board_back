def parse_params(multi_dict):
    '''MultiDict形式のパラメータを辞書形式に変換する.

    通常のキー名は同一キー名としてマッピングされる。
    キー名が'[]'で終わるデータは、キー名から'[]'が削除され、
    複数存在するデータは配列に変換されマッピングされる。
    '''
    pargs = {}
    for key in multi_dict.keys():
        if key.endswith('[]'):
            pargs[key[:-2]] = multi_dict.getlist(key)
        else:
            pargs[key] = multi_dict.get(key)

    return pargs
