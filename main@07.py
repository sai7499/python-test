from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
api = api.namespace("Student Marks", description=" Students Marks Management System")
mongo = PyMongo(app)
student = mongo.db.student_marks
faculty = mongo.db.faculty_name


# -----------------------------------------------------------------------------
# --> creating models for students and faculty below-------------


student_model = api.model("Student", {"_id": fields.Integer, "Name": fields.String, "Subject": fields.String, "Marks": fields.Integer})
faculty_model = api.model("Faculty", {"Name": fields.String, "Subject": fields.String})


#----------------------------------------------------------------------------------------
# --> creating empty list for each subject

mathematics_list = []
telugu_list = []
english_list = []
social_list = []
physics_list = []
chemistry_list = []

sub_list = ["Mathematics","Telugu","English","Social","Physics","Chemistry"]

students_list = []   # creating an empty students list
total_marks = {}     # empty dictionary to store total marks of each student
invidual_marks = {}  # empty dictionary to store invidual marks of each student

fac_dic = {}
for i in sub_list:
    query = faculty.find({'Subject': i})
    for j in query:
        fac_dic[i] = j['Name']


# --> maths 

query = student.find({'Subject': 'Mathematics'})
result = []

for i in query:
    dic = {'Name': i['Name'], 'Subject': i['Subject'], 'Marks': i['Marks']}
    result.append(dic)

for j in range(len(result)):
    mathematics_list.append(result[j]['Marks'])

# --> telugu
query = student.find({'Subject' : 'Telugu'})
result = []

for k in query:
    dic = {'Name':k['Name'],'Subject':k['Subject'],'Marks':k['Marks']}
    result.append(dic)

for l in range(len(result)):
    telugu_list.append(result[l]['Marks'])

# --> english

query = student.find({'Subject' : 'English'})
result = []

for m in query:
    dic = {'Name':m['Name'],'Subject':m['Subject'],'Marks':m['Marks']}
    result.append(dic)

for n in range(len(result)):
    english_list.append(result[n]['Marks'])

# --> social

query = student.find({'Subject' : 'Social'})
result = []

for o in query:
    dic = {'Name':o['Name'],'Subject':o['Subject'],'Marks':o['Marks']}
    result.append(dic)

for p in range(len(result)):
    social_list.append(result[p]['Marks'])

# --> physics

query = student.find({'Subject' : 'Physics'})
result = []

for q in query:
    dic = {'Name':q['Name'],'Subject':q['Subject'],'Marks':q['Marks']}
    result.append(dic)

for r in range(len(result)):
    physics_list.append(result[r]['Marks'])

# --> chemistry

query = student.find({'Subject' : 'Chemistry'})
result = []

for s in query:
    dic = {'Name':s['Name'],'Subject':s['Subject'],'Marks':s['Marks']}
    result.append(dic)

for t in range(len(result)):
    chemistry_list.append(result[t]['Marks'])


# ---Average methot to find the average---------


def Avg(subject):
    sum = 0
    count = 0
    for marks in range(0, len(subject)):
        if subject[marks] >= 40:
            sum = sum + subject[marks]
            count += 1
    return round((sum / count),2)  # here we are rounding the vlaue of avg by two digits



# -------------------------------------------------------------

# Appending the students name into an empty list named student_list

for i in range(1,101):
    s = student.find({'_Id' : i})
    for j in s:
        dic = {"Name":j['Name']}
        for name ,stud in dic.items():
            if stud not in students_list:
                students_list.append(stud)




# ----------------------------------------



#>>>>>>>>>> main methods start here------------


#____________Query1__________



@api.route('/query1')
class Greater(Resource):
     def get(self):

         """
         This query is used to find the faculty with highest student count who got more than 90% 
          
         """
         result = {}
        
         
         for j in sub_list:
             query = student.aggregate( [ {'$match': {'Subject':j, 'Marks': {'$gt':90} } },{'$count': "passed students"} ] )
             for i in query:
                 result[j] = i['passed students']


         for sub ,count in result.items():
             if count == max(result.values()):
              return {"The faculty with highest student count who got more than 90% is":fac_dic[sub] }






#__________________Query2_____________________________

@api.route('/query2')
class Highest(Resource):
    def get(self):
         
         """
         This query is used to find the faculty with highest pass percentage (> 40%)
          
         """
         result = {}
        
         
         for j in sub_list:
             query = student.aggregate( [ {'$match': {'Subject':j, 'Marks': {'$gt':40} } },{'$count': "passed students"} ] )
             for i in query:
                 result[j] = i['passed students']


         for sub ,count in result.items():
             if count == max(result.values()):
              return {"the faculty with highest pass percentage (> 40%)is ":fac_dic[sub] }






#______________________Query3_____________________________




@api.route('/query3')
class Least(Resource):
     def get(self):
         
         """
         This query is used to find the faculty with least pass percentage (<= 40%)
          
         """
         result = {}
        
         
         for j in sub_list:
             query = student.aggregate( [ {'$match': {'Subject':j, 'Marks': {'$lte':40} } },{'$count': "passed students"} ] )
             for i in query:
                 result[j] = i['passed students']


         for sub ,count in result.items():
             if count == max(result.values()):
              return {"The faculty with least pass percentage (<= 40%) is":fac_dic[sub] }





#________________________Query4________________________________________




@api.route('/query4')
class Max(Resource):

    def get(self):
        """
        This method is used to find the top student with max total 
        """
    
        total_marks= {}
        for i in students_list:
            query = student.aggregate([{ '$match' : { 'Name' : i } },{ "$group" : { '_id' : "$_Id", 'Total_Marks' : { '$sum' : "$Marks" } } }])
            for j in query:
                total_marks[i] = j['Total_Marks']
        for student_name ,marks in total_marks.items():
            if marks == max(total_marks.values()):
                return {"The top student with maximum total ": {'Name':student_name,'Marks':marks}}





#_____________________________Query5____________________________--

@api.route('/query5')
class Mathematics(Resource):
    def get(self):

        '''
        This Query is to used to find  the best student in Mathematics.

        '''
       
        query = student.find({'Subject': 'Mathematics', 'Marks': 100})
        for i in query:
            dic = {"Name": i['Name'], 'Subject':i['Subject'],'Marks': i['Marks']}
            #result.append(i)
        return {"The Best student in Mathematics is": dic}



#_______________________Query6____________________________________---


@api.route('/query6')
class Average(Resource):
     def get(self):

        '''
        This Query is to used to find  the average marks of students(except failures).

        '''
        return {"The Average Marks for each Subject are" :{"Mathematics"  : Avg(mathematics_list),"Telugu" : Avg(telugu_list),"English" : Avg(english_list),
                  "Social" : Avg(social_list),"Physics" : Avg(physics_list),"Chemistry" : Avg(chemistry_list)} }

                   

                     




@api.route('/query7')
class Min(Resource):
    def get(self):

        """
        This method is used to find the student with least total
        """
    
        total_marks= {}
        for i in students_list:
            query = student.aggregate([{ '$match' : { 'Name' : i } },{ "$group" : { '_id' : "$_Id", 'Total_Marks' : { '$sum' : "$Marks" } } }])
            for j in query:
                total_marks[i] = j['Total_Marks']
        for student_name ,marks in total_marks.items():
            if marks == min(total_marks.values()):
                return {"the student with least numbers of marks as total ": {'Name':student_name,'Marks':marks}}

    




    
        





if __name__ == "__main__":
    app.run(debug=True,port=5000)
