from flask import Flask, request, jsonify, Response
import waitress

import serviceHelper

app = Flask(__name__)

@app.route('/sprintDataService/initialize',methods=['POST'])

def initialize():
    request_body = request.json
    return serviceHelper.initialize(request_body)

@app.route('/sprintDataService/teams',methods=['GET'])
def getTeams():
    return serviceHelper.getTeams()
    
@app.route('/sprintDataService/award',methods=['POST'])
def getAward():
    request_body = request.json
    return serviceHelper.getAward(request_body)
    
@app.route('/sprintDataService/leaderboard',methods=['POST'])
def getLeaderboard():
    request_body = request.json
    return serviceHelper.getLeaderboard(request_body)

@app.route('/sprintDataService/storyPoints',methods=['POST'])
def getStoryPoints():
    request_body = request.json
    return serviceHelper.getStoryPoints(request_body)
    
@app.route('/sprintDataService/testTickets',methods=['POST'])
def getTestTickets():
    request_body = request.json
    return serviceHelper.getTestTickets(request_body)
    
@app.route('/sprintDataService/codeQuality',methods=['POST'])
def getCodeQuality():
    request_body = request.json
    return serviceHelper.getCodeQuality(request_body)
    
@app.route('/sprintDataService/assists',methods=['POST'])
def getAssists():
    request_body = request.json
    return serviceHelper.getAssists(request_body)
    
@app.route('/sprintDataService/kudos',methods=['POST'])
def getKudos():
    request_body = request.json
    return serviceHelper.getKudos(request_body)

if __name__ == '__main__':
    waitress.serve(app, host="0.0.0.0", port=8080)