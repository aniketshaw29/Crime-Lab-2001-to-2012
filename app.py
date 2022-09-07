# using flask
import base64
from io import BytesIO
import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt

app = Flask(__name__)

#required dataset
df=pd.read_csv("data.csv") #load the dataset   #df is the data frame here(data set)
df['TOTAL']=df.iloc[:,-12:].sum(axis=1)  #new col for total crimes
d=df[:-38] #to drop total crime rows      #d is the updated data set 
#d dataset is only used for max calculations


#slicing of list ---->  list[ Initial : End : IndexJump ]

#required in the coding part for ("/INDIA_CRIME_CHART")
list_of_all_states_and_uts = d['STATE/UT'].unique().tolist()  
list_of_all_states_and_uts.remove('TOTAL (STATES)') 
list_of_all_states_and_uts.remove('TOTAL (UTs)') 
list_of_all_states_and_uts.remove('TOTAL (ALL-INDIA)') 

#required in the coding part for ("/All_UT")  
list_all_uts = list_of_all_states_and_uts[28:36]     #particular ut

#required in the coding part for ("/All_States")  
list_of_all_states = list_of_all_states_and_uts[0:28]    #particular state

#required in the coding part for each plotting
font1 = {'family':'serif','color':'orange','size':20}
font2 = {'family':'serif','color':'red','size':15}

######################################################################################
#important required templates

def crime_template(sCrimeName):
    temp1 = d[d['CRIME HEAD'].str.contains(sCrimeName)] 
    temp2 = temp1.drop(temp1.index[[-1,-2,-10]]) 
    tl=temp2['TOTAL'].tolist()
    temp2.plot(kind='bar',x='STATE/UT',y='TOTAL',color='red',figsize=(15,6))
    plt.xticks(rotation='vertical')
    plt.grid(b=True, color='purple',alpha=0.5)
    plt.title(sCrimeName, fontdict = font1)
    plt.xlabel("LIST OF STATES/UT", fontdict = font2)
    plt.ylabel("RATE OF CRIMES", fontdict = font2)
    for i in range(35):                         #to show the value on the bar
        plt.text(x=i-0.4, y = tl[i]+2, s = tl[i], size = 10)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def state_ut_template(sName):
    temp1 = d[d['STATE/UT'].str.contains(sName)]
    tl=temp1['TOTAL'].tolist() 
    temp1.plot(kind='bar',x='CRIME HEAD',y='TOTAL',color='red',figsize=(8,6))
    plt.xticks(rotation='vertical')
    plt.grid(b=True, color='purple',alpha=0.5)
    plt.title(sName, fontdict = font1)
    plt.xlabel("LIST OF CRIMES", fontdict = font2)
    plt.ylabel("RATE OF CRIMES", fontdict = font2)
    for i in range(12):
        plt.text(x=i-0.3, y = tl[i]+2, s = tl[i], size = 10)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def crime_by_year_template(sYear):
    y=d[d['STATE/UT'].str.contains('ALL-INDIA')]
    sc=y.loc[:,['CRIME HEAD',sYear]]
    tl=sc[sYear].tolist()
    sc.plot(kind='bar',x='CRIME HEAD',y=sYear,color='red',figsize=(8,4))
    plt.xticks(rotation="vertical")
    plt.grid(b=True, color='grey',alpha=0.5)
    plt.title(sYear, fontdict = font1)
    plt.xlabel("TYPE OF CRIMES", fontdict = font2)
    plt.ylabel("RATE OF CRIME", fontdict = font2)
    for i in range(12):
        plt.text(x=i-0.3, y = tl[i]+10, s = tl[i], size = 10)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def total_templates(list,nLen,sXLabel,sTitle,nFig,nTextx,nTexty,NSize): 
    total_list=[]
    for i in list:
        temp1 = d[d['STATE/UT'].str.contains(i)] 
        temp2=temp1.sum(axis=0)
        temp2=temp2['TOTAL']
        total_list.append(temp2)
    data = {'STATE/UT':list, 'TOTAL':total_list}
    ts=pd.DataFrame(data)
    ts = ts.sort_values(by ='TOTAL' ,ascending=False)
    tl=ts['TOTAL'].tolist() 
    ts.plot(kind='bar',x='STATE/UT',y='TOTAL',color='red',figsize=(float(nFig),6))
    plt.xticks(rotation='vertical')
    plt.grid(b=True, color='purple',alpha=0.5)
    plt.title(sTitle, fontdict = font1)
    for i in range(int(nLen)):
        plt.text(x=i-float(nTextx), y = tl[i]+int(nTexty), s = tl[i], size = NSize)
    plt.xlabel("LIST OF "+sXLabel, fontdict = font2)
    plt.ylabel("RATE OF CRIMES", fontdict = font2)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

#####################################################################################
#home page route

@app.route("/")
def home():
    return render_template('home.html')

#####################################################################################################
# first drop down list menu

@app.route("/crime_infanticide")
def crime_infanticide():
    data = crime_template('INFANTICIDE')
    return render_template('showData.html', data=data)

@app.route("/crime_murder_of_children")
def crime_murder_of_children():
    data = crime_template('MURDER OF CHILDREN')
    return render_template('showData.html', data=data)

@app.route("/crime_rape_of_children")
def crime_rape_of_children():
    data = crime_template('RAPE OF CHILDREN')
    return render_template('showData.html', data=data)
    
@app.route("/crime_kidnapping_and_abduction_of_children")
def crime_kidnapping_and_abduction_of_children():
    data = crime_template('KIDNAPPING and ABDUCTION OF CHILDREN')
    return render_template('showData.html', data=data)

@app.route("/crime_foeticide")
def crime_foeticide():
    data = crime_template('FOETICIDE')
    return render_template('showData.html', data=data)

@app.route("/crime_abetment_of_suicide")
def crime_abetment_of_suicide():
    data = crime_template('ABETMENT OF SUICIDE')
    return render_template('showData.html', data=data)

@app.route("/crime_exposure_and_abandonment")
def crime_exposure_and_abandonment(): 
    data = crime_template('EXPOSURE AND ABANDONMENT')
    return render_template('showData.html', data=data)

@app.route("/crime_procuration_of_minor_girls")
def crime_procuration_of_minor_girls():
    data = crime_template('PROCURATION OF MINOR GILRS')
    return render_template('showData.html', data=data)

@app.route("/crime_buying_of_girls_for_prostitution")
def crime_buying_of_girls_for_prostitution():
    data = crime_template('BUYING OF GIRLS FOR PROSTITUTION')
    return render_template('showData.html', data=data)

@app.route("/crime_selling_of_girls_for_prostitution")
def crime_selling_of_girls_for_prostitution(): 
    data = crime_template('SELLING OF GIRLS FOR PROSTITUTION')
    return render_template('showData.html', data=data)

@app.route("/crime_prohibition_of_child_marriage_act")
def crime_prohibition_of_child_marriage_act(): 
    data = crime_template('PROHIBITION OF CHILD MARRIAGE ACT')
    return render_template('showData.html', data=data)

@app.route("/crime_other_crimes_against_children")
def crime_other_crimes_against_children():
    data = crime_template('OTHER CRIMES AGAINST CHILDREN')
    return render_template('showData.html', data=data)

@app.route("/Total_Crime")                            
def total_crime():
    temp1 = d[d['STATE/UT']=='TOTAL (ALL-INDIA)']
    temp1 = temp1.sort_values(by ='TOTAL' ,ascending=False)
    tl=temp1['TOTAL'].tolist()
    temp1.plot(kind='bar',x='CRIME HEAD',y='TOTAL',color='red',figsize=(8,6))
    plt.xticks(rotation='vertical')
    plt.grid(b=True, color='purple',alpha=0.5)
    plt.title("TOTAL CRIMES", fontdict = font1)
    for i in range(12):
        plt.text(x=i-0.2, y = tl[i]+1000, s = tl[i], size = 8)
    plt.xlabel("LIST OF CRIMES", fontdict = font2)
    plt.ylabel("RATE OF CRIMES", fontdict = font2)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('showData.html', data=data)
    
@app.route("/INDIA_CRIME_CHART")       
def INDIA_CRIME_CHART():
    data = total_templates(list_of_all_states_and_uts,35,'TOTAL STATES & UTs','Indian Crime Chart',16.6,0.5,1000,8)
    return render_template('showData.html', data=data)
    
####################################################################################################
# second drop down list menu

@app.route("/ANDHRA_PRADESH")
def ANDHRA_PRADESH():
    data = state_ut_template('ANDHRA PRADESH')
    return render_template('showData.html', data=data)
    
@app.route("/ARUNACHAL_PRADESH")
def ARUNACHAL_PRADESH():
    data = state_ut_template('ARUNACHAL PRADESH')
    return render_template('showData.html', data=data)
    
@app.route("/ASSAM")
def ASSAM():
    data = state_ut_template('ASSAM')
    return render_template('showData.html', data=data)
    
@app.route("/BIHAR")
def BIHAR():
    data = state_ut_template('BIHAR')
    return render_template('showData.html', data=data)
    
@app.route("/CHHATTISGARH")
def CHHATTISGARH(): 
    data = state_ut_template('CHHATTISGARH')
    return render_template('showData.html', data=data)

@app.route("/GOA")
def GOA():
    data = state_ut_template('GOA')
    return render_template('showData.html', data=data)

@app.route("/GUJARAT")
def GUJARAT():
    data = state_ut_template('GUJARAT')
    return render_template('showData.html', data=data)

@app.route("/HARYANA")
def HARYANA():
    data = state_ut_template('HARYANA')
    return render_template('showData.html', data=data)

@app.route("/HIMACHAL_PRADESH")
def HIMACHAL_PRADESH(): 
    data = state_ut_template('HIMACHAL PRADESH')
    return render_template('showData.html', data=data)
    
@app.route("/JAMMU_and_KASHMIR")
def JAMMU_and_KASHMIR(): 
    data = state_ut_template('JAMMU & KASHMIR')
    return render_template('showData.html', data=data)

@app.route("/JHARKHAND")
def JHARKHAND():
    data = state_ut_template('JHARKHAND')
    return render_template('showData.html', data=data)

@app.route("/KARNATAKA")
def KARNATAKA():
    data = state_ut_template('KARNATAKA')
    return render_template('showData.html', data=data)

@app.route("/KERALA")
def KERALA(): 
    data = state_ut_template('KERALA')
    return render_template('showData.html', data=data)

@app.route("/MADHYA_PRADESH")
def MADHYA_PRADESH():
    data = state_ut_template('MADHYA PRADESH')
    return render_template('showData.html', data=data)

@app.route("/MAHARASHTRA")
def MAHARASHTRA(): 
    data = state_ut_template('MAHARASHTRA')
    return render_template('showData.html', data=data)
    
@app.route("/MANIPUR")
def MANIPUR():
    data = state_ut_template('MANIPUR')
    return render_template('showData.html', data=data)
    
@app.route("/MEGHALAYA")
def MEGHALAYA():
    data = state_ut_template('MEGHALAYA')
    return render_template('showData.html', data=data)
    
@app.route("/MIZORAM")
def MIZORAM():
    data = state_ut_template('MIZORAM')
    return render_template('showData.html', data=data)
    
@app.route("/NAGALAND")
def NAGALAND():
    data = state_ut_template('NAGALAND')
    return render_template('showData.html', data=data)
    
@app.route("/ODISHA")
def ODISHA():
    data = state_ut_template('ODISHA')
    return render_template('showData.html', data=data)
    
@app.route("/PUNJAB")
def PUNJAB():
    data = state_ut_template('PUNJAB')
    return render_template('showData.html', data=data)
    
@app.route("/RAJASTHAN")
def RAJASTHAN(): 
    data = state_ut_template('RAJASTHAN')
    return render_template('showData.html', data=data)
    
@app.route("/SIKKIM")
def SIKKIM(): 
    data = state_ut_template('SIKKIM')
    return render_template('showData.html', data=data)
    
@app.route("/TAMIL_NADU")
def TAMIL_NADU():
    data = state_ut_template('TAMIL NADU')
    return render_template('showData.html', data=data)
    
@app.route("/TRIPURA")
def TRIPURA():
    data = state_ut_template('TRIPURA')
    return render_template('showData.html', data=data)
    
@app.route("/UTTAR_PRADESH")
def UTTAR_PRADESH():
    data = state_ut_template('UTTAR PRADESH')
    return render_template('showData.html', data=data)
    
@app.route("/UTTARAKHAND")
def UTTARAKHAND():
    data = state_ut_template('UTTARAKHAND')
    return render_template('showData.html', data=data)
    
@app.route("/WEST_BENGAL")
def WEST_BENGAL():
    data = state_ut_template('WEST BENGAL')
    return render_template('showData.html', data=data)
    
@app.route("/A_and_N_ISLANDS")
def A_and_N_ISLANDS():
    data = state_ut_template('A & N ISLANDS')
    return render_template('showData.html', data=data)

@app.route("/CHANDIGARH")
def CHANDIGARH(): 
    data = state_ut_template('CHANDIGARH')
    return render_template('showData.html', data=data)

@app.route("/D_and_N_HAVELI")
def D_and_N_HAVELI():
    data = state_ut_template('D & N HAVELI')
    return render_template('showData.html', data=data)

@app.route("/DAMAN_and_DIU")
def DAMAN_and_DIU():
    data = state_ut_template('DAMAN & DIU')
    return render_template('showData.html', data=data)

@app.route("/DELHI")
def DELHI():
    data = state_ut_template('DELHI')
    return render_template('showData.html', data=data)

@app.route("/LAKSHADWEEP")
def LAKSHADWEEP():
    data = state_ut_template('LAKSHADWEEP')
    return render_template('showData.html', data=data)

@app.route("/PUDUCHERRY")
def PUDUCHERRY():
    data = state_ut_template('PUDUCHERRY')
    return render_template('showData.html', data=data)

@app.route("/All_States")       
def All_States():
    data =  total_templates(list_of_all_states,28,'STATES','All States',16.5,0.4,1000,9)
    return render_template('showData.html', data=data)
    
@app.route("/All_UT")         
def All_UT():
    data =  total_templates(list_all_uts,7,'UNION TERRITORY','All UTs',8,0.2,100,10)
    return render_template('showData.html', data=data)

#####################################################################################################
#third dropdown menu list

@app.route("/crime_2001")
def crime_2001():
    data = crime_by_year_template('2001')
    return render_template('showData.html', data=data)

@app.route("/crime_2002")
def crime_2002():
    data = crime_by_year_template('2002')
    return render_template('showData.html', data=data)

@app.route("/crime_2003")
def crime_2003():
    data = crime_by_year_template('2003')
    return render_template('showData.html', data=data)

@app.route("/crime_2004")
def crime_2004():
    data = crime_by_year_template('2004')
    return render_template('showData.html', data=data)

@app.route("/crime_2005")
def crime_2005():
    data = crime_by_year_template('2005')
    return render_template('showData.html', data=data)

@app.route("/crime_2006")
def crime_2006():
    data = crime_by_year_template('2006')
    return render_template('showData.html', data=data)

@app.route("/crime_2007")
def crime_2007():
    data = crime_by_year_template('2007')
    return render_template('showData.html', data=data)

@app.route("/crime_2008")
def crime_2008():
    data = crime_by_year_template('2008')
    return render_template('showData.html', data=data)

@app.route("/crime_2009")
def crime_2009():
    data = crime_by_year_template('2009')
    return render_template('showData.html', data=data)

@app.route("/crime_2010")
def crime_2010():
    data = crime_by_year_template('2010')
    return render_template('showData.html', data=data)

@app.route("/crime_2011")
def crime_2011():
    data = crime_by_year_template('2011')
    return render_template('showData.html', data=data)

@app.route("/crime_2012")
def crime_2012():
    data = crime_by_year_template('2012')
    return render_template('showData.html', data=data)

####################################################################################################

if __name__ == "__main__": 
    app.run(debug=True) 