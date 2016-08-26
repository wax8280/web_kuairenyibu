def try_int(string_, default):
    try:
        i_ = int(string_)
    except:
        i_ = default
    finally:
        return i_

def try_get_from_dict(dict_,key_,default):
    try:
        v_=dict_[key_]
    except:
        v_=default
    finally:
        return v_