# 1. Connection with the SQL Server
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ABRAXAS-WINDOWS;'
                      'Database=Survey_Sample_A18;'
                      'Trusted_Connection=yes;')

# Reference
#cursor = conn.cursor()
#cursor.execute('SELECT U.UserId, U.[User_Name], COALESCE ((SELECT A.Answer_Value FROM Answer as A WHERE A.SurveyId = 1 AND A.QuestionId = 1 AND A.UserId = U.UserId), -1) as Q1 FROM [User] as U')
#for row in cursor:
#    print(row)

# 2. Getting all Survey IDs
cursor = conn.cursor()
cursor.execute('SELECT SurveyId FROM Survey ORDER BY SurveyId')
surveyIDs = []
for row in cursor:
    element = [elem for elem in row]
    surveyIDs.append(element[0])

#3. Creating a master list identifying all the quesions for each survey                                                
masterList = []                                                                                                       
cursor = conn.cursor()                                     
for i in surveyIDs:
    cursor.execute('SELECT * FROM(SELECT SurveyId, QuestionId, ' + str(i) +
                   'as InSurvey FROM SurveyStructure WHERE SurveyId = ' + str(i) +
                   'UNION SELECT ' + str(i) +
                   '''as SurveyId, Q.QuestionId, 0 as InSurvey FROM Question as Q
                   WHERE NOT EXISTS (SELECT * FROM SurveyStructure as S WHERE S.SurveyId = ''' + str(i) +
                   'AND S.QuestionId = Q.QuestionId)) as t ORDER BY QuestionId;')
    for row in cursor:
        masterList.append(list(row))



