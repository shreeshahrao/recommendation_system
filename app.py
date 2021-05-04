
from flask import Flask,request,jsonify,render_template , redirect
import pandas as pd
from model import display_ingredients , recipenames
from recipe_recommendation_model import recommendation
import model as md
import jinja2
import csv
from csv import writer
env = jinja2.Environment()
env.globals.update(zip = zip)

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
d=dict()
search=dict()

@app.route('/')
def home_page():
    return render_template('Login_v3/index.html')

@app.route('/home',methods = ['POST'])
def present_user():
    try:
        user_info = pd.read_excel('user_info.xlsx')
    except:
        return render_template('register/index.html')
    values  = [x for x in request.form.values()]
    usr,psd = values[0],values[1]
    dishes = md.history(usr = usr)
    dishes_name = [x.TranslatedRecipeName for x in dishes]
    dishes_url = [x.URL for x in dishes]
    l = display_ingredients()

    if (str(user_info[ (user_info['user']== usr) ].password.loc[0])==str(psd)):
        return render_template('Nutrient/index.html',name = 'hello '+ usr,dishes = dishes_name,urls= dishes_url, l=l,d=d)
    else:
        return render_template('register/index.html')

@app.route('/user_page',methods= ['POST'])
def new_user():
    try:
        user_info = pd.read_excel('user_info.xlsx')
    except:
        user_info = pd.DataFrame(data=None,columns=['mail','user','password','d1','d2','d3','d4','d5'])

    values = [x for x in request.form.values()]
    name = values[0]
    values  = values[:3]
    values.extend([0]*5)
    values = pd.DataFrame([values],columns=['mail','user','password','d1','d2','d3','d4','d5'])
    user_info=user_info.append(values)
    #user_info = pd.DataFrame.append(values)
    #user_info[name] = values[1:3]
    l = display_ingredients()

    user_info.to_excel('user_info.xlsx')
    return render_template('Nutrient/index.html',name = 'hello '+name,dishes = ["Gobi Manchuri","Jeera Rice"],l=l,d=d)


@app.route('/ingredients', methods=["POST"])

def ingredients():

    if request.method == "POST":
        l2 = []
        l1 = request.form.getlist("field[]")
        s = ' '.join(l1)
        l2.append(s)
        l3,link = recommendation(l2)
        d = dict(zip(l3,link))
        print(d)
        rec = "You can prepare these recipes"
        rname="Recipe Name"
        rlink="Recipe Link"
        l = display_ingredients()


    return render_template("Nutrient/index.html", l3=l3, rec=rec, l=l,link=link,d=d,rname=rname,rlink=rlink)

@app.route('/getrecipe', methods=["POST"])

def getrecipe():
    recipe_ = pd.read_csv('recipe_dataset.csv')
    ind=0
    if request.method =="POST":
        recipename=request.form['recipenam']
        recipename1=''.join(recipename)
        recipelist = recipe_['TranslatedRecipeName'].tolist()
        ind=recipelist.index(recipename1)
        print(ind)
        print(recipe_.iloc[ind])
        recipedata=recipe_.iloc[ind]
        RecipeName=recipedata[2]
        RecipeIngredients=recipedata[3]
        RecipePreptime=recipedata[4]
        RecipeCooktime=recipedata[5]
        RecipeTotaltime=recipedata[6]
        Recipeservings=recipedata[7]
        RecipeCusine=recipedata[8]
        RecipeCourse=recipedata[9]
        RecipeDiet=recipedata[10]
        RecipeInstruction=recipedata[11]
        RecipeUrl=recipedata[12]
        rn='Recipe Name'
        ri='Recipe Ingredients'
        rp='Recipe Preparation'
        rt='Recipe Totaltime'
        rs='Recipe Servings'
        rc='Recipe Course'
        rcusine='Recipe Cusine'
        rcook='Recipe Cook Time'
        rd='Recipe Diet'
        rins='Recipe Instructions'
        rurl='Recipe URL'
        link='Link to Recipe'
        list1=['Recipe Name','Recipe Ingredients','Recipe Preparation','Recipe Totaltime','Recipe Servings','Recipe Course','Recipe Cusine','Recipe Cook Time','Recipe Diet','Recipe Instructions','Recipe URL']
        list2=[recipedata[2],recipedata[3],recipedata[4],recipedata[5],recipedata[6],recipedata[7],recipedata[8],recipedata[9],recipedata[10],recipedata[11],recipedata[12]]
        search=dict(zip(list1,list2))
        list1.clear()
        list2.clear()
        recipelist1 = recipenames()



    return render_template('Nutrient/blog.html',recipename1=recipename1,recipedata=recipedata,rn=rn,RecipeName=RecipeName,ri=ri,RecipeIngredients=RecipeIngredients,rp=rp,RecipePreptime=RecipePreptime,rt=rt,RecipeTotaltime=RecipeTotaltime,rs=rs,Recipeservings=Recipeservings,rc=rc,RecipeCourse=RecipeCourse,rd=rd,RecipeDiet=RecipeDiet,rins=rins,RecipeInstruction=RecipeInstruction,rurl=rurl,RecipeUrl=RecipeUrl,rcusine=rcusine,RecipeCusine=RecipeCusine,rcook=rcook,RecipeCooktime=RecipeCooktime,link=link,recipelist=recipelist1,search=search)

@app.route('/contact')
def contact():
    return render_template('Nutrient/contact.html')

@app.route('/submit_form',methods=["POST"])
def submit_form():

    if request.method=="POST":
        name=request.form['Name']
        email=request.form['email']
        textarea=request.form['textarea']
        l=[]
        l.append(name)
        l.append(email)
        l.append(textarea)
        with open('contact_form.csv','a',newline='') as csvfile:
            writer_object=writer(csvfile)
            writer_object.writerow(l)
            csvfile.close()
        l.clear()
        recived='We Recived Your Message'
        return render_template('Nutrient/contact.html',recived=recived)

@app.route('/about')
def about():
    return render_template('Nutrient/about.html')

@app.route('/blog')
def blog():
    recipelist1=recipenames()
    return render_template('Nutrient/blog.html',recipelist=recipelist1,search=search)
@app.route('/detail')
def detail():
    return render_template('Nutrient/detail.html')

@app.route('/home')
def home():
    l = display_ingredients()
    return render_template('Nutrient/index.html',l=l,d=d)

@app.route('/menu')
def menu():
    return render_template('Nutrient/menu.html')

@app.route('/services')
def services():
    return render_template('Nutrient/services.html')

@app.route('/team')
def team():
    return render_template('Nutrient/team.html')
@app.route('/logout')
def logout():
    return render_template('Login_v3/index.html')

if __name__== '__main__':
    app.run(debug=True)