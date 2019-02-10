var express = require("express");
var app = express();

const admin =  require('firebase-admin');
var serviceAccount = require('/home/ubuntu/settings/firebase_account_key.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
var db = admin.firestore();


function getFirebaseData(snapshot){
    var retArray = [];
    snapshot.forEach((doc) => {
        console.log(doc.id, '=>', doc.data());
        retArray.push({id : doc.id, data: doc.data()});
    });
    return retArray;
}

function getCurrentStatus(jsonData){
    lastData = jsonData[jsonData.length-1].data;
    if(lastData.tlen_ans == 0)
        return {
            q_count : lastData.q_count,
            status : "考え中"
        };
    prevData = jsonData[jsonData.length-2].data;
    if(lastData.tlen_ans == prevData.tlen_ans)
        return {
            q_count : lastData.q_count + 1 ,
            status : "考え中"
        };
    return {
        q_count : lastData.q_count,
        status : "解答中"
    };
}

function getAnsHistory(jsonData){
    history = [];
    var startTime= Date.parse('2019/01/01 00:00:00');
    var nextQuestion = true;
    var q_count = 0
    var last_tlen_ans = 999; 
    console.log("jsondata : ", jsonData);
    jsonData.forEach((r) => {
        console.log("rdata : ", r);
        if(q_count < r.data.q_count)
            nextQuestion = true;
        if(last_tlen_ans == r.data.tlen_ans)
            nextQuestion = true;
        if (nextQuestion){
            while(q_count + 1 < r.data.q_count){
                q_count++;
                history.push({
                    q_count : q_count,
                    spent_sec : 0
                });
            }
            if(q_count > 0){
                var endTime = Date.parse(r.data.timestamp);
                var spent_sec = (endTime - startTime) / 1000;
                history.push({
                    q_count : q_count,
                    spent_sec : spent_sec
                });
            }
            startTime = Date.parse(r.data.timestamp);
            q_count++;
            nextQuestion = false;
        }
        last_tlen_ans = r.data.tlen_ans;
    });
    return history;
}

var server = app.listen(3000, function(){
    console.log("Node.js is listening to PORT:" + server.address().port);
});

app.use(express.static('public'));

app.get("/api/data/get/:collection", function(req, res, next){
    db.collection(req.params.collection).get()
    .then((snapshot) => {
        var jsonData = getFirebaseData(snapshot);
        console.log('jsonData got.');
        var status = getCurrentStatus(jsonData);
        console.log('status get : ', status);
        var history = getAnsHistory(jsonData);
        console.log('history get : ',history);
        datares = {
            status: status,
            history: history
        }
        res.json(datares);
    });
    // .catch(() => {
    //     console.log('Error getting documents', err);
    // });
});