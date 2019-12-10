import datetime
from collections import defaultdict
from flask import Flask,jsonify,json
from flask_restplus import Api, Resource, fields
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/employ"
api = api.namespace("Employees", description=" Employee Management System")
mongo = PyMongo(app)
employ = mongo.db.employ




@api.route('/query1')
class List(Resource):
    def get(self):
        """
        This is a query to list the dept names
        """
        #dept_list = defaultdict(int)
        result = []
        dept_list = []
        query = employ.find({},{'dept':1})
        for i in query:
            dic = i['dept']
            result.append(dic)
        for j in range(len(result)):
            if result[j][0]['dept'] not in dept_list:
                dept_list.append(result[j][0]['dept'])
        # dept_list[result[j][0]['dept']] +=1
        
        return {"Departments list are " : dept_list}






@api.route('/query2')
class Salary(Resource):

    def get(self): 
        """
        This is a query to display the present top 10 highest paid  employees 
        """

        result = []
        sal_list =[]
        emp_details = []
        query = employ.find({},{'salaries':1,'first_name':1, 'last_name':1})
        for i in query:
            dic = { 'Id' : i ['_id'],'salaries': i ['salaries']}
            result.append(dic)

        for j in result:
            if j['salaries'][-1]['from_date'] <= datetime.datetime.now() <= j['salaries'][-1]['to_date']:
                sal_list.append(j['salaries'][-1]['salary'])
        sal_list.sort(reverse= True)
        sal_list_top_10 = sal_list[0 : 10]

        for  sal in sal_list_top_10:
            query1 = employ.find({'salaries.salary' : sal})

            for details in query1:
                dic ={ 'Id' : details['_id'],'First Name' : details['first_name'], 'Last Name' : details['last_name'],'Department': details['dept'][-1]['dept'],'Salary' : details['salaries'][-1]['salary']}
                emp_details.append(dic)

        return jsonify(emp_details)


@api.route('/query3')
class Engineer(Resource):
    def get(self):
        """
        This is a query to display the current senior engineers

        """
        result = []
        sr_eng = []
        query = employ.find( {}, { 'titles':1,'first_name':1, 'last_name':1,'dept':1 } )
        for i in query:
            dic = { 'Id' : i ['_id'],'titles': i ['titles'],'first_name' : i ['first_name'], 'last_name' : i ['last_name'],'dept' : i['dept']}
            result.append(dic)

        for j in result:
            if j['titles'][-1]['from_date'] <= datetime.datetime.now() <= j['titles'][-1]['to_date']:
                if j['titles'][-1]['title'] == "Senior Engineer":
                    dic ={ 'Id' : j['Id'],'First Name' : j['first_name'], 'Last Name' : j['last_name'],'Department': j['dept'][-1]['dept']}
                    sr_eng.append(dic)
        #print(len(sr_eng))
        return {"List of all senior engineer are ": sr_eng}


@api.route('/query4')
class Dept(Resource):
    def get(self):
        """
        This is a query to display the total no of employees by dept
        """
    
        dept_list = defaultdict(int)
        result = []
        query = employ.find({},{'dept.':1})
        for i in query:
            dic = i['dept']
            result.append(dic)
        for j in range(len(result)):
            dept_list[result[j][0]['dept']] +=1
        return {"The count of employees by department are ": dept_list}



@api.route('/query5')
class Title(Resource):
    def get(self):
        """
        This is a query to display the total no of employees by  their job title
        """
    
        titles_list = defaultdict(int)
        result = []
        query = employ.find({},{'titles':1})
        for i in query:
            dic = i['titles']
            result.append(dic)
            
        for j in range(len(result)):
            titles_list[result[j][0]['title']] +=1
        
        return jsonify({"The count of employees by job title are ":titles_list})


@api.route('/query6')
class Latest(Resource):
    def get(self):
        """
        This is a query to display the latest recruited  employees
        """
        result =[]
        # lates_emp = []
        query = employ.aggregate( [ { '$sort' : { 'hire_date' : -1 }  }  ] , allowDiskUse = True )

        for i in query:
            if i['hire_date'] <= datetime.datetime.now():
                dic = { 'ID' : i['_id'],'Hire date' : i['hire_date'] , 'First Name' : i['first_name'],'Last Name' : i['last_name'],'title': i['titles'][-1]['title'] ,'salary': i['salaries'][-1]['salary'], 'Department' : i['dept'][-1]['dept']}
                result.append(dic)
        latest_emp = result[0]
        return jsonify({"Latest Recruited Employees are " : latest_emp })






if __name__ == '__main__':
    app.run(debug = True)