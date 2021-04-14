from cassandra.cluster import Cluster

cassandra_ip_address = '0.0.0.0'
cassandra_port = 9042
cassandra_keyspace = 'trackstar'


cluster = Cluster([cassandra_ip_address],port=cassandra_port)
session = cluster.connect(cassandra_keyspace,wait_for_all_pools=True)
session.execute('USE '+cassandra_keyspace)


# rows = session.execute('SELECT * FROM team_members')
# for row in rows:
#     print(row.user_id,row.name,row.team)

def getTeams():
    rows = session.execute('SELECT DISTINCT team FROM team_members')
    result = []
    for row in rows:
        result.append(row.team)
    return result
    
def getTeamMembers(team_name):
    rows = session.execute('SELECT * FROM team_members where team=\''+team_name+'\' ')
    result = {}
    for row in rows:
        result[row.user_id] =row.name
        # result.append( { 'user_id': row.user_id,
        #                  'name': row.name
        #                 }
        #             )
    #print(result)
    return result
    
def getTeamUserIds(team_name):
    team_members = getTeamMembers(team_name)
    return list(team_members.keys())
    # id_list = []
    # for member in team_members:
    #     name_list.append(member['user_id'])
    # return name_list
        
    
def readTableHelper(table_name,team):
    rows = session.execute('SELECT * FROM ' + table_name + ' where team=\''+team+'\'')
    return rows

def getStarsForSprint(sprint_date,team):
    rows = session.execute('SELECT * FROM sprint_stars where sprint_date = \'' + sprint_date + '\' AND team = \''+team+'\'')
    stars = []
    for row in rows:
        stars.append( { 
                        'user_id':row.user_id,
                        'category':row.category
                      }  
                    )
    return stars

def getSprintStarTotals(team):
    data = readTableHelper('sprint_stars',team)
    sprint_stars_dict = {}
    for row in data:
        if row.user_id not in sprint_stars_dict.keys():
            sprint_stars_dict[row.user_id] = 1 
        else:    
            sprint_stars_dict[row.user_id] = sprint_stars_dict[row.user_id] + 1
    print(sprint_stars_dict)
    return sprint_stars_dict

def getStoryPoints(team):
    data = readTableHelper('story_points',team)
    story_points_dict = {}
    for row in data:
        if row.user_id not in story_points_dict.keys():
            story_points_dict[row.user_id] = 0
            
        story_points_dict[row.user_id] = story_points_dict[row.user_id] + int(row.story_points)
    return story_points_dict
        
    
def getTestTickets(team):
    data = readTableHelper('test_tickets',team)
    
    test_tickets_dict = {}
    for row in data:
        if row.user_id not in test_tickets_dict.keys():
            test_tickets_dict[row.user_id] = 0
            
        time_spent = row.time_spent 
        
        # remove 'h'
        time_spent = time_spent[:-1]
        
        test_tickets_dict[row.user_id] = test_tickets_dict[row.user_id] + int(time_spent)
    return test_tickets_dict
    
def getCodeQuality(team):
    data = readTableHelper('code_quality',team)
    
    code_quality_dict = {}
    for row in data:
        if row.user_id not in code_quality_dict.keys():
            code_quality_dict[row.user_id] = 0
            
        time_spent = row.time_spent 
        
        # remove 'h'
        time_spent = time_spent[:-1]
        
        code_quality_dict[row.user_id] = code_quality_dict[row.user_id] + int(time_spent)
    return code_quality_dict

def getAssists(team):
    data = readTableHelper('assists',team)
    
    assists_dict = {}
    for row in data:
        if row.user_id not in assists_dict.keys():
            assists_dict[row.user_id] = 0
            
        time_spent = row.time_spent 
        
        # remove 'h'
        time_spent = time_spent[:-1]
        
        assists_dict[row.user_id] = assists_dict[row.user_id] + int(time_spent)
    return assists_dict

def getKudos(team):
    
    data = readTableHelper('kudos',team)
    
    kudos_dict = {}
    for row in data:
        if row.recipient_id not in kudos_dict.keys():
            kudos_dict[row.recipient_id] = 1 
        else:    
            kudos_dict[row.recipient_id] = kudos_dict[row.recipient_id] + 1
    return kudos_dict




def insertStoryPoints(user_id,issue_id,story_points,team):
    
    return session.execute(
        """
        INSERT INTO story_points (user_id, issue_id, story_points,team)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id,issue_id,story_points,team)
    )
    
def insertTestTicket(user_id,worklog_id,time_spent,team):
    
    return session.execute(
        """
        INSERT INTO test_tickets (user_id, worklog_id, time_spent, team)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id,worklog_id,time_spent,team)
    )
    
def insertCodeQuality(user_id,worklog_id,time_spent,team):
    
    return session.execute(
        """
        INSERT INTO code_quality (user_id, worklog_id, time_spent, team)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id,worklog_id,time_spent,team)
    )

def insertAssist(user_id,worklog_id,time_spent,team):
    
    return session.execute(
        """
        INSERT INTO assists (user_id,worklog_id,time_spent,team)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id,worklog_id,time_spent,team)
    )
    
    
def insertKudos(user_id,worklog_id,recipient_id,team):
    
    return session.execute(
        """
        INSERT INTO kudos (user_id, worklog_id,recipient_id,team)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id,worklog_id,recipient_id,team)
    )
  
def insertSprintStar(sprint_date,user_id,category,team):
 
    return session.execute(
        """
        INSERT INTO sprint_stars (sprint_date,user_id,category,team)
        VALUES (%s, %s, %s, %s)
        """,
        (sprint_date,user_id,category,team)
    )




