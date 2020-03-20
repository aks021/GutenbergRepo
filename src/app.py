from flask import Flask,redirect, request
from utils import *
import json
# Globals
app = Flask(__name__)
app.secret_key = 'super secret key'
app.debug = True

@app.route('/')
def invalidRootUrl():
    return redirect("/1", code=302)

@app.route('/<variable>', methods=['GET'])
def rootUrl(variable):
    args = request.args
    filterDict = {}
    filterDict = dict(args)
    for key in filterDict.keys():
        filterDict[key] = filterDict[key][0].split(',')
    page = int(variable) - 1
    json_data = fetchDataFromDataBase(filterDict, page)
    if(json_data == []):
        return redirect("/1", code=302)
    return json.dumps({'data': json_data})
