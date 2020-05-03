# 1. Connection with the SQL Server
import pyodbc
import time

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


# 3. Creating a master list identifying all the quesions for each survey                                                
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

# 4. Getting answers 
# masterList = [[1,1,1],[1,2,1],[1,3,0],....]

#Matrix = []
#print(type(Matrix))
#a = 0

#while a < 3:
#    b = 0
#    SubMatrix = []
#    while b < 3:
#        SubMatrix.append(7)
#        b = b + 1
#    Matrix.append(SubMatrix)
#    a = a +1
#print(Matrix)

cursor = conn.cursor()
pointer = []
Matrix = []
for pointer in masterList:
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

#print(Matrix)
OMatrix = []
OSMatrix = []
count = 0
for question in Matrix:
    #print('\nQuestion\n')
    #print(question)
    #print(type(question))
    for elem in question:
        #print('\nElement from question:')
        #print(type(elem))
        #print(elem)
        for individual in elem:
            OSMatrix.append(individual)
        OMatrix.append(OSMatrix)
        OSMatrix = []

print(OMatrix)


    








    

   



