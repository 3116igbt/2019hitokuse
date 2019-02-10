import sys

def get_diagonal_vertex(vertices):
    xpoints = [a["x"] for a in vertices]
    ypoints = [a["y"] for a in vertices]
    return ({"x": min(xpoints), "y": min(ypoints)}, {"x": max(xpoints), "y": max(ypoints)})

# GCPの戻り値の必要な部分だけjsonに変換
def convert_to_objects_json(detected_texts):
    ret = []
    for text in detected_texts:
        buf = {}
        buf['desc'] = text.description
        vert = [{"x" : v.x, "y" :v.y} for v in text.bounding_poly.vertices]
        buf["vertices"] = vert
        ret.append(buf)
    print("json_ret : {}".format(ret))
    return ret

def get_text_info(texts_json):
    ret = []
    first_time = True
    for text_json in texts_json:
        # 最初は全体なので省く
        if first_time:
            first_time = False
            continue
        # 左上と右下を検出
        ul_1, br_1 = get_diagonal_vertex(text_json["vertices"])
        print("ul_1 {}".format(ul_1))
        print("br_1 {}".format(br_1))
        tlen = len(text_json['desc'])
        buf = {
            'ul' : ul_1,
            'br' : br_1,
            'text_len' : tlen
        }
        ret.append(buf)
    print("info_ret : {}".format(ret))
    return ret

def detect_progress(texts_info, img_width):
    ST_THK = 'think'
    ST_ANS = 'answer'
    q_count = 0
    status = ST_ANS

    status_thd = img_width / 2
    prev_r = 0
    tlen = {
        ST_THK : 0,
        ST_ANS : 0
    }
    # ステータスを作成
    for text_info in texts_info:
        # 改行判定
        if prev_r < text_info['ul']['y']:
            st_change = False
            # 左(記述中)か右（最終回答）か判断
            if status_thd <= text_info['ul']['x']:
                if status != ST_ANS:
                    st_change = True
                status = ST_ANS
            else:
                if status != ST_THK:
                    st_change = True
                    q_count = q_count + 1
                status = ST_THK
            prev_r = text_info['br']['y']
            if st_change:
                tlen[status] = 0
                print("status change : {0}, question_count : {1}".format(status, q_count))
        tlen[status] = tlen[status] + text_info['text_len']
        print("current status : {0} , len : {1}".format(status, tlen[status]))
    
    ret = {
        u'q_count' : q_count,
        u'tlen_thk' : tlen[ST_THK],
        u'tlen_ans' : tlen[ST_ANS]
    } 
    return ret

def get_detected_record(detected_texts,  img_width):
    detected_texts_json = convert_to_objects_json(detected_texts)
    texts_info_json = get_text_info(detected_texts_json)
    detected_record = detect_progress(texts_info_json, img_width)
    return detected_record