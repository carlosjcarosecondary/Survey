# Importing libraries
import pyodbc
import csv

# 1. Connection with the SQL Server
try:
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ABRAXAS-WINDOWS;'
                      'Database=Survey_Sample_A18;'
                      'Trusted_Connection=yes;')
except pyodbc.Error as err:
    print('Error 101 - There was an issue with the connection')

# 2. Getting all Survey IDs
surveyIDs = []
try:
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT SurveyId FROM Survey ORDER BY SurveyId') 
        for row in cursor:
            element = [elem for elem in row]
            surveyIDs.append(element[0])
    except:
        print('Error 201 - The query could not be processed')
except:
    print('Error 102 - The query could not be executed due to a connection error')

# 3. Creating a survey list identifying all the quesions for each survey                                                
surveyList = []     
try:
    cursor = conn.cursor()                                     
    for i in surveyIDs:
        try:
            cursor.execute('SELECT * FROM(SELECT SurveyId, QuestionId, ' + str(i) +
                           'as InSurvey FROM SurveyStructure WHERE SurveyId = ' + str(i) +
                           'UNION SELECT ' + str(i) +
                           '''as SurveyId, Q.QuestionId, 0 as InSurvey FROM Question as Q
                           WHERE NOT EXISTS (SELECT * FROM SurveyStructure as S WHERE S.SurveyId = ''' + str(i) +
                           'AND S.QuestionId = Q.QuestionId)) as t ORDER BY QuestionId;')
            for row in cursor:
                surveyList.append(list(row))
        except:
            print('Error 201 - The query could not be processed')
except:
    print('Error 102 - The query could not be executed due to a connection error')


# 4. Getting the answers from each survey
pointer = []
Matrix = []
try:
    cursor = conn.cursor()
    for pointer in surveyList:
        if pointer[2] != 0:
            TempRow = []
            currentSurvey = pointer[0]
            currentQuestion = pointer[1]
            try:
                cursor.execute('''SELECT U.UserId, U.[User_Name], COALESCE (
                                (SELECT A.Answer_Value FROM Answer as A 
                                WHERE A.SurveyId = ''' + str(currentSurvey) + 
                                'AND A.QuestionId = ' + str(currentQuestion) + 
                                'AND A.UserId = U.UserId), -1) as Q1 FROM [User] as U')
            except:
                print('Error 201 - The query could not be processed')
            for row in cursor:
                TempRow.append(row)
            Matrix.append(TempRow)
except:
    print('Error 102 - The query could not be executed due to a connection error')

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
fields = ['User ID', 'User Name', 'Survey 1 - Q1', 'Survey 1 - Q2', 'Survey 2 -Q2', 'Survey 2 - Q3', 'Survey 3 - Q'] 
filename = "survey_report.csv"
    
# writing to csv file
try: 
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        # writing the fields  
        csvwriter.writerow(fields)  
        # writing the data rows  
        csvwriter.writerows(OFMatrix) 
except:
    print('Error 301 - The CSV file could not be created, please check the settings')