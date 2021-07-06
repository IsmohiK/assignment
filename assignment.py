from flask import Flask, render_template, request,  jsonify, json
import numpy as np
import pandas as pd

######### Reading Data from CSV file ##########
df = pd.read_csv("books.csv",index_col ="id")
df.head()

app = Flask(__name__)

@app.route('/api/home')
def index():
    return render_template('index.html')
        
@app.route('/api/home/row',methods=['GET'])
def rowFilter():
    return render_template('row.html')

@app.route('/api/home/row',methods=['POST'])
def rowFilterDisplay():
    row_num = request.form['row_num']
    df2 = df.reset_index()
    df2 = df2.replace(np.nan,"null")
    df_req = df2.head(int(row_num))
    temp_list = []
    books = {}
    for i in df_req.index:
        temp_dict = {}
        for key in df_req.keys():
            temp_dict[key] = str(df_req[key][i])
        temp_list.append(temp_dict)
        
    books['Books'] = temp_list
    books_json_object = json.dumps(books, indent = 4)
    print(books_json_object)
    out_file = open("myfile.json", "w") 
    json.dump(books, out_file, indent = 4) 
    out_file.close() 
    ##return books_json_object
    return render_template('resultapi1.html', title="page", jsonfile=books_json_object)


@app.route('/api/home/column',methods=['GET'])
def colFilter():
    return render_template('column.html')

@app.route('/api/home/column',methods=['POST'])
def colFilterDisplay():
    column_name = request.form['column_name']   
    column_value = request.form['column_value'] 
    df2 = df.reset_index()
    df2 = df2.replace(np.nan,"null")
    print(column_name)
    if column_name not in df2.keys():
        return render_template('resultapi1.html', title="page", jsonfile="The column name you enetred is not present in the file. Please try again!!")
    flag = []
    for i in df2.index:
        if ',' in df2[column_name][i]:
            if column_value in df2[column_name][i].split(','):
                flag.append(i)
                
        elif column_value == df2[column_name][i]:
            flag.append(i)
            
    df_req = df2.iloc[flag]
    temp_list = []
    books = {}
    for i in df_req.index:
        temp_dict = {}
        for key in df_req.keys():
            temp_dict[key] = str(df_req[key][i])
        temp_list.append(temp_dict)
        
    books['Books'] = temp_list
    books_json_object = json.dumps(books, indent = 4)
    print(books_json_object)
    return render_template('resultapi1.html', title="page", jsonfile=books_json_object)

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5005)
