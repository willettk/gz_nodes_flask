from flask import Flask, jsonify, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from gz_classes import *
from gz_mongo import *

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('gz_nodes_local.cfg', silent=True)
#app.config.from_envvar('APPLICATION_SETTINGS', silent=True)

db=SQLAlchemy(app)
db.Model.metadata.reflect(db.get_engine(app,'gz2'))
BC2=get_tables(db,'gz2')
db.Model.metadata.reflect(db.get_engine(app,'gz3'),extend_existing=True)
BC3=get_tables(db,'gz3')
db_dict={'gz2':GZ2(db,app,BC2),
               'gz3':GZ3(db,app,BC3),
               'gz4_s':GZ4_sloan(),
               'gz4_u':GZ4_ukidss(),
               'gz4_f':GZ4_ferengi(),
               'gz4_c':GZ4_candels()}

@app.route('/')
def index():
    return render_template('index.html')

# random route is depreciated in the js code
# .run in each class now takes 'random' as and argument
#@app.route('/_get_random')
#def get_random(table='gz2'):
#    table = request.args.get('table', 'gz2', type=str)
#    gal_name,gal_id,ra_gal,dec_gal,url=db_dict[table].get_rand_obj()
#    return jsonify(result={"gal_name":gal_name})

@app.route('/_get_path')
def get_path():
    table = request.args.get('table', 'gz2', type=str)
    argv = request.args.get('argv', '180 0', type=str)
    return jsonify(result=db_dict[table].run(argv))

if __name__=="__main__":
    app.debug = True
    app.run()
