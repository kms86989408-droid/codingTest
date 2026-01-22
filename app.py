from flask import Flask, render_template, jsonify, request

from bson.objectid import ObjectId
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
    memoLikes_receive=int(request.form['memoLikes_give'])

    inventory ={
        'title' : title_receive,
        'contents' : contents_receive,
        'likes' : memoLikes_receive
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
    memos = list(memos_col.find({}).sort("likes", -1))
    for m in memos:
        m["_id"] = str(m["_id"])
        m["likes"]=m.get("likes",0)
    return jsonify({'result':"success", 'inventory': memos})

@app.route("/memos", methods=["PUT"])
def edit_memos():
    editId_receive=request.form['editId_give']
    editTitle_receive=request.form['editTitle_give']
    editContents_receive=request.form['editContents_give']
    
    try:
        result = memos_col.update_one(
        {"_id": ObjectId(editId_receive)},
        {"$set":{"title":editTitle_receive, "contents":editContents_receive}}
    )
        if result.matched_count == 0:
            return jsonify({'result':'fail', 'msg':'메모를 찾지 못햇습니다.'})
        return jsonify({'result':'success', 'msg':'수정 완료'})
    except Exception as e:
        return jsonify({'result': 'fail', 'msg': str(e)})
    
@app.route("/memos/delete", methods=["POST"])
def delete_memos():
    delete_receive=request.form['deleteId_give']
    
    try:
        result = memos_col.delete_one(
            {"_id": ObjectId(delete_receive)}
        )
        return jsonify({'result':'success','msg':'삭제 완료'})
    except Exception as e:
        print("ERROR", e)
        return jsonify({'result': 'fail', 'msg': str(e)})
    
@app.route("/memos/like", methods=["POST"])
def add_likes():
    likeId_receive=request.form['likeId_give']

    try:
        result = memos_col.update_one(
            {"_id": ObjectId(likeId_receive)},
            {'$inc':{"likes":1}}
        )
        memo = memos_col.find_one({"_id":ObjectId(likeId_receive)})
        return jsonify({'result':'success', 'likes': memo.get('likes', 0)})
    except Exception as e:
        print("ERROR", e)
        return jsonify({'result':'fail', 'msg':str(e)})

        

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)