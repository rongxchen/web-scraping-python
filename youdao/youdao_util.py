def __process_suggest_entry_explain(entry: str):
    explains = [string.strip().split(".") for string in entry.split(";")]
    res = {}
    for explain in explains:
        if len(explain) == 1:
            if "meaning" not in res:
                res["meaning"] = []
            res["meaning"].extend(explain)
        else:
            cat = explain[0] + "."
            if cat not in res:
                res[cat] = []
            res[cat].extend([t.strip() for t in "".join(explain[1:]).strip().split("；")])
    return res
    

def process_suggest(suggest_res: dict):
    if suggest_res["result"]["code"] != 200:
        return []
    entries = suggest_res["data"]["entries"]
    res = []
    for entry in entries:
        res.append({
            "suggested_text": entry["entry"],
            "explain": __process_suggest_entry_explain(entry["explain"]),
        })
    return res
    
    
def process_translate_one(translate_res: dict):
    translates = translate_res["ec"]["word"]["trs"]
    return {
        translate["pos"]: [t.strip() for t in str(translate["tran"]).split("；")]
    for translate in translates}
