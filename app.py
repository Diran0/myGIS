import requests
import sqlite3
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from geopy.distance import geodesic as GD


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('1.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/raion/')
def raion():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM raion').fetchall()
    count = conn.execute('SELECT count(distinct raion_url) num FROM raion').fetchall()
    conn.close()
    return render_template('raion.html', posts=posts, count=count)

@app.route('/rayoni/<nam>/')
def micro(nam):
    s1= '%'
    s2=nam
    s3='_'
    conn = get_db_connection()
    cort = str(s1)+str(s2)+str(s3)
    corts = (str(cort), '0')
    posts = conn.execute("SELECT * FROM micro, raion WHERE micro.micro_raion=raion.raion_url and (micro_raion like ? OR micro_raion=?)", corts).fetchall()
    count = conn.execute("SELECT count(distinct micro_url) num FROM micro WHERE micro_raion like ? OR micro_raion=?", corts).fetchall()
    conn.close()
    return render_template('micro.html', posts=posts, count=count)

@app.route('/micro/<nam>/')
def ulics(nam):
    s1='%'
    s2=nam
    s3='%'
    conn = get_db_connection()
    cort = str(s1)+str(s2)+str(s3)
    corts = (str(cort), '0')
    posts = conn.execute("SELECT * FROM ul_micro, ulic, micro WHERE ulic.ulic_url = ul_micro.ulic_url and micro.micro_url = ul_micro.ulic_micro and (ul_micro.ulic_micro like ? OR ul_micro.ulic_micro=?)", corts).fetchall()
    count = conn.execute("SELECT count(distinct ulic.ulic_url) num FROM ul_micro, ulic WHERE ulic.ulic_url = ul_micro.ulic_url and (ul_micro.ulic_micro like ? OR ul_micro.ulic_micro=?)", corts).fetchall()
    conn.close()
    return render_template('ulic.html', posts=posts, count=count)

@app.route('/ulicy/<nam>/')
def ulic(nam):
    s1='%'
    s2=nam
    s3='%'
    conn = get_db_connection()
    cort = str(s1)+str(s2)+str(s3)
    corts = (str(cort), '0')
    posts = conn.execute("SELECT distinct dom.dom_ulic, dom.dom_name, dom.dom_url, dom.dom_coor1, dom.dom_coor2,ulic.ulic_url,ulic.ulic_namef,ulic.ulic_names,ulic.ulic_longs,ulic.ulic_name FROM ulic, dom WHERE dom.dom_ulic=ulic.ulic_url  and (ulic.ulic_url like ? OR ulic.ulic_url=?)", corts).fetchall()
    count = conn.execute("SELECT count(distinct dom.dom_url) num,  max(ulic.ulic_namef) ulic_namef, max(ulic.ulic_names) ulic_names, max(ulic.ulic_longs) ulic_longs FROM ul_micro, ulic, micro, dom WHERE ulic.ulic_url = ul_micro.ulic_url and micro.micro_url = ul_micro.ulic_micro and dom.dom_ulic=ulic.ulic_url and (ulic.ulic_url like ? OR ul_micro.ulic_micro=?)", corts).fetchall()
    cross = conn.execute("SELECT distinct cross.cross_url1, cross.cross_url2, ulic.ulic_url, ulic.ulic_namef, ulic.ulic_names FROM ulic, cross WHERE cross.cross_url2=ulic.ulic_url and (cross.cross_url1 like ? OR cross.cross_url1=?)", corts).fetchall()
    mics = conn.execute("SELECT * FROM ul_micro, ulic, micro, raion WHERE ulic.ulic_url = ul_micro.ulic_url and micro.micro_raion=raion.raion_url and micro.micro_url = ul_micro.ulic_micro and (ul_micro.ulic_url like ? OR ul_micro.ulic_micro=?)", corts).fetchall()
    conn.close()
    return render_template('ulic_info.html', posts=posts, count=count, cross=cross, mics=mics)

@app.route('/ulicy/<nam1>/<nam2>/', methods=('GET', 'POST'))
def doms(nam1, nam2):
    s1='%'
    s2=nam1
    s3='%'
    s4=nam2
    s5='%'
    conn = get_db_connection()
    cort = str(s1)+str(s2)+str(s3)+str(s4)+str(s5)
    corts = (str(cort), str(cort))
    posts = conn.execute("SELECT * FROM dom, ulic WHERE dom.dom_ulic=ulic.ulic_url and (dom_url like ? OR dom_url=?)", corts).fetchall()
    posts1 = conn.execute("SELECT * FROM dom, ulic WHERE dom.dom_ulic=ulic.ulic_url ").fetchall()
    conn.close()
    rezult=[]
    shir1=float(posts[0]['dom_coor1'])
    dol1=float(posts[0]['dom_coor2'])
    flag1 = 0
    flag2 = 0
    if request.method == 'POST':
        long_max = request.form['long_max']
        long_min = request.form['long_min']
        if long_min:
            flag1 = 1
        if long_max:
            flag2 = 1
        for tem in posts1:
            if tem['dom_coor1'] and tem['dom_coor2']:
                coor1=float(tem['dom_coor1'])
                coor2=float(tem['dom_coor2'])
                if (flag1 == 1 or flag2 == 1) and ((flag1 == 1 and GD((coor1,coor2),(shir1, dol1)).m>float(long_min)) or flag1 == 0) and ((flag2 == 1 and GD((coor1,coor2),(shir1, dol1)).m<float(long_max)) or flag2 == 0):
                    qwer = str(GD((coor1,coor2),(shir1, dol1)).m)[0:7]
                    cortes = (tem['dom_name'], tem['dom_url'], tem['ulic_name'], tem['ulic_url'], qwer)
                    rezult.append(cortes)
    return render_template('dom_info.html', posts=posts, rezult=rezult)

@app.route('/search/', methods=('GET', 'POST'))
def search():

    if request.method == 'POST':
        namef = request.form['namef'] 
        nnamef = request.form['nnamef'] 
        names = request.form['names'] 
        nnames = request.form['nnames']
        nomer = request.form['nomer'] 
        nnomer =request.form['nnomer']
        corp = request.form['corp'] 
        ncorp =request.form['ncorp']
        lit = request.form['lit'] 
        nlit =request.form['nlit']
        mic = request.form['mic'] 
        nmic =request.form['nmic']
        rai = request.form['rai'] 
        nrai =request.form['nrai']


        if not namef:
            namef = '%'
        if not nnamef:
            nnamef = '*'
        if not names:
            names = '%'
        if not nnames:
            nnames = '*'
        if not nomer:
            nomer = '%'
        if not nnomer:
            nnomer = '*'
        if not corp:
            corp = '%'
        if not ncorp:
            ncorp = '*'
        if not lit:
            lit = '%'
        if not nlit:
            nlit = '*'
        if not mic:
            mic = '%'
        if not nmic:
            nmic = '*'
        if not rai:
            rai = '%'
        if not nrai:
            nrai = '*'

        namef = '%' + namef + '%'
        nnamef = '%' + nnamef + '%'
        names = '%' + names + '%'
        nnames = '%' + nnames + '%'
        nomer = '%' + nomer + '%'
        nnomer = '%' + nnomer + '%'
        corp = '%' + corp+ '%'
        ncorp = '%' + ncorp + '%'
        lit = '%' + lit + '%'
        nlit = '%' + nlit + '%'
        mic = '%' + mic + '%'
        nmic = '%' + nmic + '%'
        rai = '%' + rai + '%'
        nrai = '%' + nrai + '%'

        conn = get_db_connection()
        if corp == '%%%' or lit == '%%%':
            if corp != '%%%':
                rezult = conn.execute("SELECT distinct dom.dom_name, dom.name3_nomer nomer, dom.name3_corp corp, dom.name3_lit lit,dom.dom_url, ulic.ulic_url,ulic.ulic_namef,ulic.ulic_names,ulic.ulic_name, micro.micro_name, micro.micro_url, raion.raion_name, raion.raion_url FROM ulic, dom, ul_micro, micro,raion WHERE dom.dom_ulic=ulic.ulic_url  and ulic.ulic_url=ul_micro.ulic_url and ul_micro.ulic_micro=micro.micro_url and micro.micro_raion=raion.raion_url and ulic.ulic_namef like ? and ulic.ulic_namef not like ? and ulic.ulic_names like ? and ulic.ulic_names not like ? and dom.name3_nomer like ? and dom.name3_nomer not like ?  and dom.name3_corp like ? and dom.name3_corp not like ? and micro.micro_name like ? and micro.micro_name not like ? and raion.raion_name like ? and raion.raion_name not like ?", (namef, nnamef, names, nnames, nomer, nnomer, corp, ncorp, mic, nmic, rai, nrai)).fetchall()
            elif lit != '%%%':
                rezult = conn.execute("SELECT distinct dom.dom_name, dom.name3_nomer nomer, dom.name3_corp corp, dom.name3_lit lit,dom.dom_url, ulic.ulic_url,ulic.ulic_namef,ulic.ulic_names,ulic.ulic_name, micro.micro_name, micro.micro_url, raion.raion_name, raion.raion_url FROM ulic, dom, ul_micro, micro,raion WHERE dom.dom_ulic=ulic.ulic_url  and ulic.ulic_url=ul_micro.ulic_url and ul_micro.ulic_micro=micro.micro_url and micro.micro_raion=raion.raion_url and ulic.ulic_namef like ? and ulic.ulic_namef not like ? and ulic.ulic_names like ? and ulic.ulic_names not like ? and dom.name3_nomer like ? and dom.name3_nomer not like ?  and dom.name3_lit like ? and dom.name3_lit not like ? and micro.micro_name like ? and micro.micro_name not like ? and raion.raion_name like ? and raion.raion_name not like ?", (namef, nnamef, names, nnames, nomer, nnomer, lit, nlit, mic, nmic, rai, nrai)).fetchall()
            else:
                rezult = conn.execute("SELECT distinct dom.dom_name, dom.name3_nomer nomer, dom.name3_corp corp, dom.name3_lit lit,dom.dom_url, ulic.ulic_url,ulic.ulic_namef,ulic.ulic_names,ulic.ulic_name, micro.micro_name, micro.micro_url, raion.raion_name, raion.raion_url FROM ulic, dom, ul_micro, micro,raion WHERE dom.dom_ulic=ulic.ulic_url  and ulic.ulic_url=ul_micro.ulic_url and ul_micro.ulic_micro=micro.micro_url and micro.micro_raion=raion.raion_url and ulic.ulic_namef like ? and ulic.ulic_namef not like ? and ulic.ulic_names like ? and ulic.ulic_names not like ? and dom.name3_nomer like ? and dom.name3_nomer not like ?  and micro.micro_name like ? and micro.micro_name not like ? and raion.raion_name like ? and raion.raion_name not like ? order by micro.micro_name", (namef, nnamef, names, nnames, nomer, nnomer, mic, nmic, rai, nrai)).fetchall()                
        else:
            rezult = conn.execute("SELECT distinct dom.dom_name, dom.name3_nomer nomer, dom.name3_corp corp, dom.name3_lit lit,dom.dom_url, ulic.ulic_url,ulic.ulic_namef,ulic.ulic_names,ulic.ulic_name, micro.micro_name, micro.micro_url, raion.raion_name, raion.raion_url FROM ulic, dom, ul_micro, micro,raion WHERE dom.dom_ulic=ulic.ulic_url  and ulic.ulic_url=ul_micro.ulic_url and ul_micro.ulic_micro=micro.micro_url and micro.micro_raion=raion.raion_url and ulic.ulic_namef like ? and ulic.ulic_namef not like ? and ulic.ulic_names like ? and ulic.ulic_names not like ? and dom.name3_nomer like ? and dom.name3_nomer not like ?  and dom.name3_corp like ? and dom.name3_corp not like ? and dom.name3_lit like ? and dom.name3_lit not like ? and micro.micro_name like ? and micro.micro_name not like ? and raion.raion_name like ? and raion.raion_name not like ?", (namef, nnamef, names, nnames, nomer, nnomer, corp, ncorp, lit, nlit, mic, nmic, rai, nrai)).fetchall()
        
        conn.close()
        return render_template('search.html', rezult=rezult)


    return render_template('search.html', rezult='0')
app.run()