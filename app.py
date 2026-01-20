from flask import Flask, render_template, jsonify, request

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.dbjungle
memos_col = db['memos']

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/memos", methods=["POST"])
def saving_memos():
    title_receive=request.form['memoTitle_give']
    contents_receive=request.form['memoContents_give']

    inventory ={
        'title' : title_receive,
        'contents' : contents_receive
    }

    try:
        result = memos_col.insert_one(inventory)
        print("INSERTED",result.inserted_id)
        print("COUNT:",memos_col.count_documents({}))
        return jsonify({'result':'success','msg':'저장 완료'})
    except Exception as e:
        print("ERROR", e)
        return jsonify({'result': 'fail', 'msg': str(e)})



@app.route("/memos", methods=["GET"])
def read_inventory():    
    memos = list(memos_col.find({}, {"title":1, "contents":1}))
    for m in memos:
        m["_id"] = str(m["_id"])
    return jsonify({'result':"success", 'inventory': memos})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)