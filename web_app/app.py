from flask import Flask, render_template, send_file
#https://www.aliyun.com/jiaocheng/481233.html
# curl -X POST http://admin:admin@115.146.84.44:5984/db_test -d @result.json -H "Content-Type:application/json"
import chartkick
import random as Random
import couchdb
COUCHDB_SERVER = 'http://admin:admin@115.146.84.44:5984/'
COUCHDB_DATABASE = 'db_test'
DOC="scenario3"
couch=couchdb.Server(COUCHDB_SERVER)
db=couch[COUCHDB_DATABASE]
#print(db[document])

data=db[DOC]['features']

# data=[{u'late_slp_rank': 1, u'eco_index_rank': 1, u'Type': u'Feature', u'id': u'abc001', u'vic_loca_2': u'MELBOURNE'}, {u'late_slp_rank': 3, u'eco_index_rank': 10, u'Type': u'Feature', u'id': u'abc002', u'vic_loca_2': u'Calton'}, {u'late_slp_rank': 13, u'eco_index_rank': 9, u'Type': u'Feature', u'id': u'abc003', u'vic_loca_2': u'Parkville'}]
app = Flask(__name__)  
print(chartkick.js())
print(app.static_folder)
app.jinja_env.add_extension("chartkick.ext.charts")
col1=[]
col2=[]
col3=[]
col4=[]
bar_data={}
for x in data:
    if x['late_slp_rank'] is None or x['eco_index_rank'] is None:
        continue
    else:
        col1.append(x['vic_loca_2'])
        col2.append(x['late_slp_rank'])
        col3.append(x['eco_index_rank'])
        col4.append(x['late_slp_rank']-x['eco_index_rank'])

  #  if x['late_slp_rank'] != 'null' and x['eco_index_rank'] != 'null':
 #       print 
 #       col1=[x['vic_loca_2'] for x in data]
  #      col2=[x['late_slp_rank'] for x in data]
   #     col3=[x['eco_index_rank'] for x in data]
    #    col4=[x[0]-x[1] for x in zip(col2,col3bar_data={}
for x in range(len(col1)):
    bar_data[col1[x]]=col4[x]

######################
new_col1=col1[0:15]
new_col2=col2[0:15]
new_col3=col3[0:15]
new_col4=col4[0:15]
######################

print(bar_data)
chartdata = {u'Chrome': 0, u'Opera': -7, u'Firefox': 4}


@app.route('/')
def index():
    return render_template("test.html",bar_data=chartdata)


@app.route('/S1')
def S1():
    return render_template("s1_temp.html")


@app.route('/S2')
def S2():
    return render_template("s2_temp.html")


@app.route('/S3')
def S3():
    return render_template("s3_temp.html")

# @app.route('/Graphic')
# def graphic():
# 	return render_template("graph.html")

@app.route('/S1/map1')
def map1():
    return send_file("/doc/analysis/sentiment/html/crash_heatmap.html")


@app.route('/S1/map2')
def map2():
    return send_file("/doc/analysis/sentiment/html/liquor_heatmap.html")


@app.route('/S1/map3')
def map3():
    return send_file("/doc/analysis/sentiment/html/tweet_heatmap.html")


@app.route('/S2/map4')
def map4():
    return rsend_file("/doc/analysis/sentiment/html/choropleth.html")

@app.route('/S2/map5')
def map5():
    return send_file("/doc/analysis/sentiment/html/choropleth1.html")


@app.route('/S3/chart')
def graphic():
	return render_template("graph.html",rows=zip(new_col1,new_col2,new_col3,new_col4),bar_data=bar_data)




#print(m)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = 5000)
