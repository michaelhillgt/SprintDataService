from flask import Flask, request, jsonify, Response
import dataHelper

def getTeams():
    
    try:
        # get list of distinct team names
        teams = dataHelper.getTeams()
         
        if teams == None or len(teams) == 0:
            # no teams found
            response_object = {
                'status': 'error',
                'message': 'no teams found'
            }
            return jsonify(response_object), 404
            
            
        else:
            response_object = {
                'status': 'success',
                'message': teams
            }
            return jsonify(response_object), 200
    
    except:
        response_object = {
            'status': 'error',
            'message': 'An error occurred in serviceHelper.getTeams()'
        }
        return jsonify(response_object), 500
    

def initialize(request_body):
    
    try:
        
        #team_user_ids = dataHelper.getTeamUserIds(request_body['team'])
        
        dataHelper.processWorklogs(request_body['team'])
        
        response_object = {
            'status': 'success',
            'message': 'Application successfully initialized'
        }
        return jsonify(response_object), 200
        
    
    except:
        response_object = {
            'status': 'error',
            'message': 'An error occurred in serviceHelper.initialize()'
        }
        return jsonify(response_object), 500
        
        
def getAward(request_body):
    
    try:
        
        #team_user_ids = dataHelper.getTeamUserIds(request_body['team'])
        #dataHelper.processWorklogs(team_user_ids)
        award_list = dataHelper.awardStar(request_body['team'])
        
        
        
        response_object = {
            'status': 'success',
            'message': award_list
        }
        return jsonify(response_object), 200
        
    
    except:
        response_object = {
            'status': 'error',
            'message': 'An error occurred in serviceHelper.getAward()'
        }
        return jsonify(response_object), 500
    
        
def getLeaderboard(request_body):
    leaderboard = dataHelper.getLeaderboard(request_body['team'])
    
    response_object = {
        'status': 'success',
        'message': leaderboard
    }
    print(response_object)
    print(jsonify(response_object))
    return jsonify(response_object), 200
    
    
def getStoryPoints(request_body):
    story_points = dataHelper.getStoryPoints(request_body['team'])
    
    response_object = {
        'status': 'success',
        'message': story_points
    }
    return jsonify(response_object), 200
    
def getTestTickets(request_body):
    test_tickets = dataHelper.getTestTickets(request_body['team'])
    
    
    
    response_object = {
        'status': 'success',
        'message': test_tickets
    }
    return jsonify(response_object), 200
    
def getCodeQuality(request_body):
    code_quality = dataHelper.getCodeQuality(request_body['team'])
    
    
    
    response_object = {
        'status': 'success',
        'message': code_quality
    }
    return jsonify(response_object), 200
    
def getAssists(request_body):
    assists = dataHelper.getAssists(request_body['team'])
    
    
    
    response_object = {
        'status': 'success',
        'message': assists
    }
    return jsonify(response_object), 200
    
def getKudos(request_body):
    kudos = dataHelper.getKudos(request_body['team'])
    
    response_object = {
        'status': 'success',
        'message': kudos
    }
    return jsonify(response_object), 200
        