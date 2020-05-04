# Importing libraries
import pyodbc
import time

# 1. Connection with the SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ABRAXAS-WINDOWS;'
                      'Database=Survey_Sample_A18;'
                      'Trusted_Connection=yes;')

# 2. Getting all Survey IDs
cursor = conn.cursor()
cursor.execute('SELECT SurveyId FROM Survey ORDER BY SurveyId')
surveyIDs = []
for row in cursor:
    element = [elem for elem in row]
    surveyIDs.append(element[0])

# 3. Creating a survey list identifying all the quesions for each survey                                                
surveyList = []                                                                                                       
cursor = conn.cursor()                                     
for i in surveyIDs:
    cursor.execute('SELECT * FROM(SELECT SurveyId, QuestionId, ' + str(i) +
                   'as InSurvey FROM SurveyStructure WHERE SurveyId = ' + str(i) +
                   'UNION SELECT ' + str(i) +
                   '''as SurveyId, Q.QuestionId, 0 as InSurvey FROM Question as Q
                   WHERE NOT EXISTS (SELECT * FROM SurveyStructure as S WHERE S.SurveyId = ''' + str(i) +
                   'AND S.QuestionId = Q.QuestionId)) as t ORDER BY QuestionId;')
    for row in cursor:
        surveyList.append(list(row))

# 4. Getting answers 
cursor = conn.cursor()
pointer = []
Matrix = []
for pointer in surveyList:
    if pointer[2] != 0:
        TempRow = []
        currentSurvey = pointer[0]
        currentQuestion = pointer[1]
        cursor.execute('''SELECT TOP 3 U.UserId, U.[User_Name], COALESCE (
                        (SELECT A.Answer_Value FROM Answer as A 
                        WHERE A.SurveyId = ''' + str(currentSurvey) + 
                        'AND A.QuestionId = ' + str(currentQuestion) + 
                        'AND A.UserId = U.UserId), -1) as Q1 FROM [User] as U')
        for row in cursor:
            TempRow.append(row)
        Matrix.append(TempRow)

#5 Organzing the answers into a MasterList
OMatrix = []
OSMatrix = []
for question in Matrix:
    for elem in question:
        for individual in elem:
            OSMatrix.append(individual)
        OMatrix.append(OSMatrix)
        OSMatrix = []

#6 Formating the Master List
numUsers = int(len(OMatrix) / 5)
OFMatrix = []
OFMatrix = OMatrix[0:numUsers]
value = 1
while value < 5:
    x = 0
    for x in range(numUsers):
        OFMatrix[x].append(OMatrix[x + numUsers * value][2])
    value = value + 1

#7 Converting to CSV
print(OFMatrix)

