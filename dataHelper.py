import jiraHelper
import cassandraHelper
import datetime
import random

def convertIDsToNames(team, id_dict):
    print(id_dict)
    if len(id_dict.keys()) == 0:
        return id_dict
    team_members = getTeamMembers(team)
    print(team_members)
    name_dict = {}
    for key in id_dict.keys():
        name_dict[ team_members[key] ] = id_dict[key]
    return name_dict

def convertIDtoName(team, ID):
    team_members = getTeamMembers(team)
    return team_members[ID]
    
def getTeams():
    return cassandraHelper.getTeams()

def getTeamMembers(team_name):
    return cassandraHelper.getTeamMembers(team_name)

def getTeamUserIds(team_name):
    return cassandraHelper.getTeamUserIds(team_name)

def getStoryPoints(team):
    data = cassandraHelper.getStoryPoints(team)
    return convertIDsToNames(team, data)

def getTestTickets(team):
    data = cassandraHelper.getTestTickets(team)
    return convertIDsToNames(team, data)

def getCodeQuality(team):
    data = cassandraHelper.getCodeQuality(team)
    return convertIDsToNames(team, data)
    
def getAssists(team):
    data = cassandraHelper.getAssists(team)
    return convertIDsToNames(team, data)

def getKudos(team):
    data = cassandraHelper.getKudos(team)
    print(data)
    return convertIDsToNames(team, data)

def getLeaderboard(team):
    data = cassandraHelper.getSprintStarTotals(team)
    return convertIDsToNames(team, data)

    
def parseWorklogComment(comment):
    
    task_category,description = comment.split(':')
    task_category = task_category.lower().strip()
    task_category.replace(" ", "")
    
    env = None
    recipient_id = None
    if '/' in task_category:
        task_category,task_detail = task_category.split('/')
        
        if task_category == 'testing':
            env = task_detail.upper().strip()
        elif task_category == 'kudos':
            recipient_id = task_detail.lower().strip()
        
    return {
        'task':task_category,
        'description':description,
        'env':env,
        'recipient_id':recipient_id
    }

def processWorklogs(team_name):
    
    team_user_ids = getTeamUserIds(team_name)
    print(team_user_ids)
    
    worklogs = jiraHelper.getWorklogs()
    
    for log in worklogs:
        curr_worklog = worklogs[log]
        
        user_id = curr_worklog['author']['accountId']
        
        if (user_id in team_user_ids):    
            
            worklog_id = curr_worklog['id']
            time_spent = curr_worklog['timeSpent']
            
            display_name = curr_worklog['author']['displayName']
            print('found work log for ',display_name)
            print(curr_worklog['timeSpent'])
            print(curr_worklog['id'])
            print(curr_worklog['issueId'])
            
            comment = parseWorklogComment(
                curr_worklog['comment']['content'][0]['content'][0]['text']
                )
            print(comment)
            
            # timestamp = curr_worklog['updated']
            # print(type(timestamp))
            # print(timestamp)
            
            if comment['task'] == 'implementing' or comment['task'] == 'research':
                issue_id = curr_worklog['issueId']
                story_points = jiraHelper.getStoryPoints(issue_id)
                result = cassandraHelper.insertStoryPoints(user_id,issue_id,story_points,team_name)
                
            elif comment['task'] == 'testing' and comment['env'] == 'TEST':
                result = cassandraHelper.insertTestTicket(user_id,worklog_id,time_spent,team_name)
                
            elif comment['task'] == 'codequality':
                result = cassandraHelper.insertCodeQuality(user_id,worklog_id,time_spent,team_name)
                
            elif comment['task'] == 'assist':
                result = cassandraHelper.insertAssist(user_id,worklog_id,time_spent,team_name)
                
            elif comment['task'] == 'kudos':
                recipient_id = comment['recipient_id']
                result = cassandraHelper.insertKudos(user_id,worklog_id,recipient_id,team_name)
            else:
                print('\n\nUNRECOGNIZED TASK')
                print(comment)
                print('\n\n')
            #print(result)

def getWinnerList(data_dict):
    
    print(data_dict)
    #print(stop)
    
    max = 0
    winner_list = []
    for key in data_dict.keys():
        print('key ',key,' value: ',data_dict[key])
        if data_dict[key] > max:
            max = data_dict[key]
            winner_list = [{'user_id':key,
                            'category':None}]
        elif data_dict[key] == max:
            winner_list = winner_list + [{'user_id':key,
                                        'category':None}]
    print('winner:',winner_list)    
    return winner_list
    
def cleanupTaskString(task):
    
    if task == 'story_points':
        task = 'Story Points'
    elif task == 'test_tickets':
        task = 'Test Tickets'
    elif task == 'code_quality':
        task = 'Code Quality'
    elif task == 'assists':
        task = 'Assists'
    elif task == 'kudos':
        task = 'Kudos'
        
    return task
    
def awardStar(team_name):
    
    sprint_date = str(jiraHelper.getSprintStartDate())
    
    awards_for_current_sprint = cassandraHelper.getStarsForSprint(sprint_date,team_name)
    
    if len(awards_for_current_sprint) > 0:
        print(awards_for_current_sprint)
        # return the award list
        for user in awards_for_current_sprint:
            user['user_id'] = convertIDtoName(team_name, user['user_id'])
            user['category'] = cleanupTaskString(user['category'])
        return awards_for_current_sprint
        
        
    # else create an award
    
    tasks = ['story_points',
             'testing',
             'code_quality',
             'assists',
             'kudos']
             
    while len(tasks) > 0:
        
        award_category = random.choice(tasks)
        
        if award_category == 'story_points':
            data = cassandraHelper.getStoryPoints(team_name)
        elif award_category == 'testing':
            data = cassandraHelper.getTestTickets(team_name)
        elif award_category == 'code_quality':
            data = cassandraHelper.getCodeQuality(team_name)
        elif award_category == 'assists':
            data = cassandraHelper.getAssists(team_name)
        elif award_category == 'kudos':
            data = cassandraHelper.getKudos(team_name)
            
        if len(data.keys()) == 0:
            tasks.remove(award_category)
            print('No winners found for', award_category)
        else:
            awards_for_current_sprint = getWinnerList(data)
            print('awarding star for',award_category,'category to:', awards_for_current_sprint)
            for user in awards_for_current_sprint:
                user['category'] = award_category
                cassandraHelper.insertSprintStar(sprint_date,user['user_id'],award_category,team_name)
                user['user_id'] = convertIDtoName(team_name, user['user_id']) 
            return awards_for_current_sprint
            #print(stop)
            
    
    # handle no winner scenario
    print('No possible winner found for any category')
    return []
             
    

if __name__ == '__main__':
    team_name = 'Dev Team'
    #result = getTeamMembers(team_name)
    #print(awardStar(team_name))
    team = 'Dev Team'
    processWorklogs(team)
    kudos = getKudos(team)
    print(kudos)
#     #awardStar()
    
    