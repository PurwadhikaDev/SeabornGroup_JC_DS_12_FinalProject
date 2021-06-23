import joblib
import pickle
import pandas as pd
import numpy as np

from flask import Flask, render_template, request, session
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

# # Opsi 1 : Opsi Klasik - Opsi Statis
# - Dataset
# df.to_html("dataset.html")

# - Visualisasi
# plt.savefig

# - Prediction
# Model Import 

app = Flask(__name__)

@app.route('/')
def home():
    #return 'Selamat Datang'
    return render_template('home.html')

@app.route('/visualize1')
def vis1():
    return render_template('viz1.html')

@app.route('/visualize2')
def vis2():
    return render_template('viz2.html')

@app.route('/visualize3')
def vis3():
    return render_template('viz3.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/dataset')
def dataset():
    sqlengine = create_engine('mysql+pymysql://root:Albert123@127.0.0.1/philadelphia', pool_recycle=3605)
    engine = sqlengine.raw_connection()
    cursor = engine.cursor()
    cursor.execute("SELECT * FROM property")
    data = cursor.fetchall()
    return render_template('dataset.html', data=data)

@app.route('/predict1')
def pred1():
    return render_template('pred1.html')

@app.route('/predict2')
def pred2():
    return render_template('pred2.html')

@app.route('/hasil1', methods=['POST'])
def result1():
    global recommend
    if request.method == 'POST':
        input = request.form
        basements = input["basements"]
        if basements == '0':
            print_basements = "None"
        elif basements == 'A':
            print_basements = "Full Finished"
        elif basements == 'B':
            print_basements = "Full Semi-Finished"
        elif basements == 'C':
            print_basements = "Full Unfinished"
        elif basements == 'D':
            print_basements = "Full Unknown Finished"
        elif basements == 'E':
            print_basements = "Partial Finished"
        elif basements == 'F':
            print_basements = "Partial Semi-Finished"
        elif basements == 'G':
            print_basements = "Partial Unfinished"
        elif basements == 'H':
            print_basements = "Partial Unknown Finished"
        elif basements == 'I':
            print_basements = "Unknown Size - Finished"
        elif basements == 'J':
            print_basements = "Unknown Size - Semi-Finished"

        central_air = input["central_air"]
        if central_air == 'Y':
            print_central_air = "Using (Yes)"
        elif central_air == 'N':
            print_central_air = "Not Using (No)"

        exterior_condition = input["exterior_condition"]
        if exterior_condition == "2":
            print_exterior_condition = "New / Rehabbed – Noticeably New Construction"
        elif exterior_condition == "3":
            print_exterior_condition = "Above Average"
        elif exterior_condition == "4":
            print_exterior_condition = "Average – Would Be Typical"
        elif exterior_condition == "5":
            print_exterior_condition = "Below Average"
        elif exterior_condition == "6":
            print_exterior_condition = "Vacant – No occupancy"
        elif exterior_condition == "7":
            print_exterior_condition = "Sealed / Structurally Compromised"

        fireplaces = input["fireplaces"]

        garage_type = input["garage_type"]
        if garage_type == "0":
            print_garage_type = "None"
        elif garage_type == "A":
            print_garage_type = "Basement / Built-In"
        elif garage_type == "B":
            print_garage_type= "Attached Garage"
        elif garage_type == "C":
            print_garage_type = "Detached Garage"
        elif garage_type == "F":
            print_garage_type = "Converted"
        
        interior_condition = input["interior_condition"]
        if interior_condition == "2":
            print_interior_condition = "New / Rehabbed – Noticeably New Construction"
        elif interior_condition == "3":
            print_interior_condition = "Above Average"
        elif interior_condition == "4":
            print_interior_condition = "Average – Would Be Typical"
        elif interior_condition == "5":
            print_interior_condition = "Below Average"
        elif interior_condition == "6":
            print_interior_condition = "Vacant – No occupancy"
        elif interior_condition == "7":
            print_interior_condition = "Sealed / Structurally Compromised"

        number_of_rooms = input["number_of_rooms"]

        number_stories = input["number_stories"]

        parcel_shape = input["parcel_shape"]
        if parcel_shape == "A":
            print_parcel_shape = "Irregular"
        elif parcel_shape == "B":
            print_parcel_shape = "Grossly Irregular"
        elif parcel_shape == "C":
            print_parcel_shape = "Triangular"
        elif parcel_shape == "D":
            print_parcel_shape = "Right of Way"
        elif parcel_shape == "E":
            print_parcel_shape = "Rectangular"

        street_designation = input["street_designation"]
        if street_designation == "ALY":
            print_street_designation = "Alley"
        elif street_designation == "AVE":
            print_street_designation = "Avenue"
        elif street_designation == "BLV":
            print_street_designation = "Boulevard"
        elif street_designation == "CIR":
            print_street_designation = "Circle"
        elif street_designation == "CT ":
            print_street_designation = "Court"
        elif street_designation == "DR ":
            print_street_designation = "Drive"
        elif street_designation == "HTS":
            print_street_designation = "Heights"
        elif street_designation == "LN ":
            print_street_designation = "Lane"
        elif street_designation == "MEW":
            print_street_designation = "Mews"
        elif street_designation == "PK ":
            print_street_designation = "Park"
        elif street_designation == "PKY":
            print_street_designation = "Parkway"
        elif street_designation == "PL ":
            print_street_designation = "Place"
        elif street_designation == "PLZ":
            print_street_designation = "Plaza"
        elif street_designation == "RD ":
            print_street_designation = "Road"
        elif street_designation == "ROW":
            print_street_designation = "Roadway"
        elif street_designation == "SQ ":
            print_street_designation = "Square"
        elif street_designation == "ST ":
            print_street_designation = "Street"
        elif street_designation == "TER":
            print_street_designation = "Terrace"
        elif street_designation == "WAY":
            print_street_designation = "Way"

        topography = input["topography"]
        if topography == "1":
            print_topography = "Above Street Level"
        elif topography == "2":
            print_topography = "Below Street Level"
        elif topography == "3":
            print_topography = "Flood Plain or Flood Hazard Zone"
        elif topography == "4":
            print_topography = "Rocky"
        elif topography == "5":
            print_topography = "Not Identified"
        elif topography == "6":
            print_topography = "Level"

        total_area = input["total_area"]

        total_livable_area = input["total_livable_area"]

        type_heater = input["type_heater"]
        if type_heater == "0":
            print_type_heater = "None"
        elif type_heater == "A":
            print_type_heater = "Hot Air (Ducts)"
        elif type_heater == "B":
            print_type_heater = "Hot Water (Radiators or Baseboards)"
        elif type_heater == "C":
            print_type_heater = "Electric Baseboard"
        elif type_heater == "D":
            print_type_heater = "Heat Pump (Outside Unit)"
        elif type_heater == "E":
            print_type_heater = "Other (Portable Heater)"
        elif type_heater == "F":
            print_type_heater = "Radiant"
        elif type_heater == "G":
            print_type_heater = "Undetermined"

        view_type = input["view_type"]
        if view_type == "0":
            print_view_type = "None"
        elif view_type == "A":
            print_view_type = "Cityscape / Skyline"
        elif view_type == "B":
            print_view_type = "Flowing Water"
        elif view_type == "C":
            print_view_type = "Park / Green Area"
        elif view_type == "D":
            print_view_type = "Commercial"
        elif view_type == "E":
            print_view_type = "Industrial"
        elif view_type == "H":
            print_view_type = "Edifice / Landmark"
        elif view_type == "I":
            print_view_type = "Typical / Other"

        building_description = input["building_description"]
        if building_description == "FRAME":
            print_building_description = "Frame"
        elif building_description == "MASONRY":
            print_building_description = "Masonry"
        elif building_description == "MASONRY+OTHER":
            print_building_description = "Masonry + Other"
        elif building_description == "STONE":
            print_building_description = "Stone"

        section = input["section"]
        if section == "Central City":
            print_section = "Central City"
        elif section == "North":
            print_section = "North"
        elif section == "North East":
            print_section = "North East"
        elif section == "North West":
            print_section = "North West"
        elif section == "South":
            print_section = "South"
        elif section == "South West":
            print_section = "South West"
        elif section == "West":
            print_section = "West"

        abc = [[basements, central_air, exterior_condition, fireplaces, garage_type, interior_condition, number_of_rooms, number_stories, parcel_shape, street_designation, topography, total_area, total_livable_area, type_heater, view_type, building_description, section]]
        does = pd.DataFrame(data=abc, columns=['basements', 'central_air', 'exterior_condition', 'fireplaces', 'garage_type', 'interior_condition', 'number_of_rooms', 'number_stories', 'parcel_shape', 'street_designation', 'topography', 'total_area', 'total_livable_area', 'type_heater', 'view_type', 'building_description', 'section'])
        prediction = round(Model_Regressor.predict(does)[0],2)

        rec = [[basements, central_air, exterior_condition, fireplaces, garage_type, interior_condition, prediction, number_of_rooms, number_stories, parcel_shape, street_designation, topography, total_area, total_livable_area, type_heater, view_type, building_description, section]]
        recommend = pd.DataFrame(data=rec, columns=['basements', 'central_air', 'exterior_condition', 'fireplaces', 'garage_type', 'interior_condition', 'market_value', 'number_of_rooms', 'number_stories', 'parcel_shape', 'street_designation', 'topography', 'total_area', 'total_livable_area', 'type_heater', 'view_type', 'building_description', 'section'])
    return render_template('result1.html', data = input, pred = prediction, result_basements = print_basements, result_central_air = print_central_air, result_exterior_condition = print_exterior_condition, result_garage_type = print_garage_type, result_interior_condition = print_interior_condition, result_parcel_shape = print_parcel_shape, result_street_designation = print_street_designation, result_topography = print_topography, result_type_heater = print_type_heater, result_view_type = print_view_type, result_building_description = print_building_description, result_section = print_section)

@app.route('/hasilrecommendation', methods=['POST'])
def recommendation():
    if request.method == 'POST':
        df = pd.read_csv('PHL_Building_Dataset_Recommendation_Mini.csv')
        df = df[:25000]
        
        df2 = pd.read_csv('PHL_Building_Dataset_Recommendation_Big.csv')
        df2 = df2.reset_index()

        df2['basements'] = df2['basements'].replace({'0': 'None', 'A' : 'Full Finished', 'B' : 'Full Semi-Finished', 
                                                'C' : 'Full Unfinished', 'D' : 'Full', 'E' : 'Partial Finished',
                                                'F' : 'Partial Semi-Finished', 'G' : 'Partial Unfinished',
                                                'H' : 'Partial - Unknown Finish', 'I' : 'Unknown Size - Finished',
                                                'J' : 'Unknown Size - Unfinished'})

        df2['central_air'] = df2['central_air'].replace({'Y' : 'Yes', 'N' : 'No'})

        df2['exterior_condition'] = df2['exterior_condition'].replace({0 : 'Not Applicable', 2 : 'Newer Construction / Rehabbed', 
                                                                3 : 'Above Average',
                                                                4 : 'Average', 5 : 'Below Average', 6 : 'Vacant',
                                                                7 : 'Sealed / Structurally Compromised'})

        df2['garage_type'] = df2['garage_type'].replace({'0' : 'None', 'A' : 'Basement / Built-In','B' : 'Attached Garage',
                                                    'C' : 'Detached Garage', 'F' : 'Converted',
                                                    'S' : 'Self Park', 'T' : 'Attendant'})

        df2['interior_condition'] = df2['interior_condition'].replace({0 : 'Not Applicable', 2 : 'Newer Construction / Rehabbed',
                                                                3 : 'Above Average', 4 : 'Average',
                                                                5 : 'Below Average', 6 : 'Vacant', 
                                                                7 : 'Sealed / Structurally Compromised'})

        df2['parcel_shape'] = df2['parcel_shape'].replace({'A' : 'Irregular', 'B' : 'Grossly Irregular',
                                                    'C' : 'Triangular', 'D' : 'Right of way', 'E' : 'Rectangular'})

        df2['street_designation'] = df2['street_designation'].replace({'ALY' : 'Alley' ,'AVE' : 'Avenue', 'BLV' : 'Boulevard', 'CIR' : 'Circle',
                                                                'CT ' : 'Court', 'DR ' : 'Drive', 'HTS' : 'Heights', 'LN ' : 'Lane',
                                                                'MEW' : 'Mews', 'PK ' : 'Park', 'PKY' : 'Parkway',
                                                                'PL ' : 'Place', 'PLZ' : 'Plaza', 'RD ' : 'Road',
                                                                'ROW' : 'Roadway', 'SQ ' : 'Square', 'ST ' : 'Street', 
                                                                'TER' : 'Terrace'})

        df2['topography'] = df2['topography'].replace({1 : 'Above Street Level', 2 : 'Below Street Level', 
                                                3 : 'Flood Plain', 4 : 'Rocky', 5 : 'Not identified', 
                                                6 : 'Level'})

        df2['type_heater'] = df2['type_heater'].replace({'A':'Hot Air (Ducts)', 'B' :'Hot Water (Radiator or Baseboards)', 
                                                    'C' :'Electric Baseboard', 'D' :'Heat Pump', 'E' :'Other', 
                                                    'G' :'Radiant', 'H' : 'Undetermined', '0' : 'None'})

        df2['view_type'] = df2['view_type'].replace({'I' : 'Typical', 'A' :'Cityscape', 'B' :'Flowing Water', 
                                                'C' : 'Park/Green Area', 'D' :'Commercial', 'E' :'Industrial', 
                                                'H' :'Edifice/Landmark', '0' : 'None'})

        df2['zoning'] = df2['zoning'].replace({1: 'RSA-5', 2:'RSA-4', 3:'RSA-3', 4 :'RSA-2', 5 : 'RSA-1', 
                                        6 :'RSD-3', 7 : 'RSD-2', 8 : 'RSD-1' })
        
        df = df.append(recommend, ignore_index=True)

        features = ["exterior_condition", "interior_condition", "market_value", "number_stories", "total_area", "total_livable_area", "building_description", "section"]

        for i in df.columns:
            df[i] = df[i].astype('str')

        def combo(x):
            return x["exterior_condition"] + " " + x["interior_condition"] + " " + x["market_value"] + " " + x["number_stories"] + " " + x["section"] + " " + x["building_description"] + " " + x["total_area"] + " " + x["total_livable_area"]

        df['combo_features'] = df.apply(combo, axis=1)

        CV = CountVectorizer()

        property_matrix = CV.fit_transform(df['combo_features'])

        cos_score = cosine_similarity(property_matrix)

        similar_property = list(enumerate(cos_score[-1]))

        sorted_property = sorted(similar_property, key=lambda x:x[1], reverse=True)[1:] # [1:] -> propertynya sendiri ga masuk

        a1 = []
        count = 1
        for i in sorted_property:
            for j in range(1, 26):
                a1.append((df2.columns[j].replace("_"," ").title() , df2.iloc[i[0]][j]))
            count += 1
            if count == 6:
                break

        b0 = []
        for i in recommend.columns:
            for j in recommend[i]:
                b0.append(j)

        basements_01 = b0[0]
        if basements_01 == '0':
            result_basements_01 = "None"
        elif basements_01 == 'A':
            result_basements_01 = "Full Finished"
        elif basements_01 == 'B':
            result_basements_01 = "Full Semi-Finished"
        elif basements_01 == 'C':
            result_basements_01 = "Full Unfinished"
        elif basements_01 == 'D':
            result_basements_01 = "Full Unknown Finished"
        elif basements_01 == 'E':
            result_basements_01 = "Partial Finished"
        elif basements_01 == 'F':
            result_basements_01 = "Partial Semi-Finished"
        elif basements_01 == 'G':
            result_basements_01 = "Partial Unfinished"
        elif basements_01 == 'H':
            result_basements_01 = "Partial Unknown Finished"
        elif basements_01 == 'I':
            result_basements_01 = "Unknown Size - Finished"
        elif basements_01 == 'J':
            result_basements_01 = "Unknown Size - Semi-Finished"

        central_air_01 = b0[1]
        if central_air_01 == 'Y':
            result_central_air_01 = "Using (Yes)"
        elif central_air_01 == 'N':
            result_central_air_01 = "Not Using (No)"

        exterior_condition_01 = b0[2]
        if exterior_condition_01 == "2":
            result_exterior_condition_01 = "New / Rehabbed – Noticeably New Construction"
        elif exterior_condition_01 == "3":
            result_exterior_condition_01 = "Above Average"
        elif exterior_condition_01 == "4":
            result_exterior_condition_01 = "Average – Would Be Typical"
        elif exterior_condition_01 == "5":
            result_exterior_condition_01 = "Below Average"
        elif exterior_condition_01 == "6":
            result_exterior_condition_01 = "Vacant – No occupancy"
        elif exterior_condition_01 == "7":
            result_exterior_condition_01 = "Sealed / Structurally Compromised"

        result_fireplaces_01 = b0[3]

        garage_type_01 = b0[4]
        if garage_type_01 == "0":
            result_garage_type_01 = "None"
        elif garage_type_01 == "A":
            result_garage_type_01 = "Basement / Built-In"
        elif garage_type_01 == "B":
            result_garage_type_01 = "Attached Garage"
        elif garage_type_01 == "C":
            result_garage_type_01 = "Detached Garage"
        elif garage_type_01 == "F":
            result_garage_type_01 = "Converted"

        interior_condition_01 = b0[5]
        if interior_condition_01 == "2":
            result_interior_condition_01 = "New / Rehabbed – Noticeably New Construction"
        elif interior_condition_01 == "3":
            result_interior_condition_01 = "Above Average"
        elif interior_condition_01 == "4":
            result_interior_condition_01 = "Average – Would Be Typical"
        elif interior_condition_01 == "5":
            result_interior_condition_01 = "Below Average"
        elif interior_condition_01 == "6":
            result_interior_condition_01 = "Vacant – No occupancy"
        elif interior_condition_01 == "7":
            result_interior_condition_01 = "Sealed / Structurally Compromised"
        
        result_market_value_01 = b0[6]

        result_number_of_rooms_01 = b0[7]

        result_number_stories_01 = b0[8]

        parcel_shape_01 = b0[9]
        if parcel_shape_01 == "A":
            result_parcel_shape_01 = "Irregular"
        elif parcel_shape_01 == "B":
            result_parcel_shape_01 = "Grossly Irregular"
        elif parcel_shape_01 == "C":
            result_parcel_shape_01 = "Triangular"
        elif parcel_shape_01 == "D":
            result_parcel_shape_01 = "Right of Way"
        elif parcel_shape_01 == "E":
            result_parcel_shape_01 = "Rectangular"

        street_designation_01 = b0[10]
        if street_designation_01 == "ALY":
            result_street_designation_01 = "Alley"
        elif street_designation_01 == "AVE":
            result_street_designation_01 = "Avenue"
        elif street_designation_01 == "BLV":
            result_street_designation_01 = "Boulevard"
        elif street_designation_01 == "CIR":
            result_street_designation_01 = "Circle"
        elif street_designation_01 == "CT ":
            result_street_designation_01 = "Court"
        elif street_designation_01 == "DR ":
            result_street_designation_01 = "Drive"
        elif street_designation_01 == "HTS":
            result_street_designation_01 = "Heights"
        elif street_designation_01 == "LN ":
            result_street_designation_01 = "Lane"
        elif street_designation_01 == "MEW":
            result_street_designation_01 = "Mews"
        elif street_designation_01 == "PK ":
            result_street_designation_01 = "Park"
        elif street_designation_01 == "PKY":
            result_street_designation_01 = "Parkway"
        elif street_designation_01 == "PL ":
            result_street_designation_01 = "Place"
        elif street_designation_01 == "PLZ":
            result_street_designation_01 = "Plaza"
        elif street_designation_01 == "RD ":
            result_street_designation_01 = "Road"
        elif street_designation_01 == "ROW":
            result_street_designation_01 = "Roadway"
        elif street_designation_01 == "SQ ":
            result_street_designation_01 = "Square"
        elif street_designation_01 == "ST ":
            result_street_designation_01 = "Street"
        elif street_designation_01 == "TER":
            result_street_designation_01 = "Terrace"
        elif street_designation_01 == "WAY":
            result_street_designation_01 = "Way"

        topography_01 = b0[11]
        if topography_01 == "1":
            result_topography_01 = "Above Street Level"
        elif topography_01 == "2":
            result_topography_01 = "Below Street Level"
        elif topography_01 == "3":
            result_topography_01 = "Flood Plain or Flood Hazard Zone"
        elif topography_01 == "4":
            result_topography_01 = "Rocky"
        elif topography_01 == "5":
            result_topography_01 = "Not Identified"
        elif topography_01 == "6":
            result_topography_01 = "Level"

        result_total_area_01 = b0[12]

        result_total_livable_area_01 = b0[13]

        type_heater_01 = b0[14]
        if type_heater_01 == "0":
            result_type_heater_01 = "None"
        elif type_heater_01 == "A":
            result_type_heater_01 = "Hot Air (Ducts)"
        elif type_heater_01 == "B":
            result_type_heater_01 = "Hot Water (Radiators or Baseboards)"
        elif type_heater_01 == "C":
            result_type_heater_01 = "Electric Baseboard"
        elif type_heater_01 == "D":
            result_type_heater_01 = "Heat Pump (Outside Unit)"
        elif type_heater_01 == "E":
            result_type_heater_01 = "Other (Portable Heater)"
        elif type_heater_01 == "F":
            result_type_heater_01 = "Radiant"
        elif type_heater_01 == "G":
            result_type_heater_01 = "Undetermined"

        view_type_01 = b0[15]
        if view_type_01 == "0":
            result_view_type_01 = "None"
        elif view_type_01 == "A":
            result_view_type_01 = "Cityscape / Skyline"
        elif view_type_01 == "B":
            result_view_type_01 = "Flowing Water"
        elif view_type_01 == "C":
            result_view_type_01 = "Park / Green Area"
        elif view_type_01 == "D":
            result_view_type_01 = "Commercial"
        elif view_type_01 == "E":
            result_view_type_01 = "Industrial"
        elif view_type_01 == "H":
            result_view_type_01 = "Edifice / Landmark"
        elif view_type_01 == "I":
            result_view_type_01 = "Typical / Other"
    
        building_description_01 = b0[16]
        if building_description_01 == "FRAME":
            result_building_description_01 = "Frame"
        elif building_description_01 == "MASONRY":
            result_building_description_01 = "Masonry"
        elif building_description_01 == "MASONRY+OTHER":
            result_building_description_01 = "Masonry + Other"
        elif building_description_01 == "STONE":
            result_building_description_01 = "Stone"

        section_01 = b0[17]
        if section_01 == "Central City":
            result_section_01 = "Central City"
        elif section_01 == "North":
            result_section_01 = "North"
        elif section_01 == "North East":
            result_section_01 = "North East"
        elif section_01 == "North West":
            result_section_01 = "North West"
        elif section_01 == "South":
            result_section_01 = "South"
        elif section_01 == "South West":
            result_section_01 = "South West"
        elif section_01 == "West":
            result_section_01 = "West"
        
        first = a1[0:25]
        second = a1[25:50]
        third = a1[50:75]
        fourth = a1[75:100]
        fifth = a1[100:125]

        input1a = first[0][0]
        input2a = first[1][0]
        input3a = first[2][0]
        input4a = first[3][0]
        input5a = first[4][0]
        input6a = first[5][0]
        input7a = first[6][0]
        input8a = first[7][0]
        input9a = first[8][0]
        input10a = first[9][0]
        input11a = first[10][0]
        input12a = first[11][0]
        input13a = first[12][0]
        input14a = first[13][0]
        input15a = first[14][0]
        input16a = first[15][0]
        input17a = first[16][0]
        input18a = first[17][0]
        input19a = first[18][0]
        input20a = first[19][0]
        input21a = first[20][0]
        input22a = first[21][0]
        input23a = first[22][0]
        input24a = first[23][0]
        input25a = first[24][0]

        recommenderA1 = first[0][1]
        recommenderA2 = first[1][1]
        recommenderA3 = first[2][1]
        recommenderA4 = first[3][1]
        recommenderA5 = first[4][1]
        recommenderA6 = first[5][1]
        recommenderA7 = first[6][1]
        recommenderA8 = first[7][1]
        recommenderA9 = first[8][1]
        recommenderA10 = first[9][1]
        recommenderA11 = first[10][1]
        recommenderA12 = first[11][1]
        recommenderA13 = first[12][1]
        recommenderA14 = first[13][1]
        recommenderA15 = first[14][1]
        recommenderA16 = first[15][1]
        recommenderA17 = first[16][1]
        recommenderA18 = first[17][1]
        recommenderA19 = first[18][1]
        recommenderA20 = first[19][1]
        recommenderA21 = first[20][1]
        recommenderA22 = first[21][1]
        recommenderA23 = first[22][1]
        recommenderA24 = first[23][1]
        recommenderA25 = first[24][1]

        recommenderB1 = second[0][1]
        recommenderB2 = second[1][1]
        recommenderB3 = second[2][1]
        recommenderB4 = second[3][1]
        recommenderB5 = second[4][1]
        recommenderB6 = second[5][1]
        recommenderB7 = second[6][1]
        recommenderB8 = second[7][1]
        recommenderB9 = second[8][1]
        recommenderB10 = second[9][1]
        recommenderB11 = second[10][1]
        recommenderB12 = second[11][1]
        recommenderB13 = second[12][1]
        recommenderB14 = second[13][1]
        recommenderB15 = second[14][1]
        recommenderB16 = second[15][1]
        recommenderB17 = second[16][1]
        recommenderB18 = second[17][1]
        recommenderB19 = second[18][1]
        recommenderB20 = second[19][1]
        recommenderB21 = second[20][1]
        recommenderB22 = second[21][1]
        recommenderB23 = second[22][1]
        recommenderB24 = second[23][1]
        recommenderB25 = second[24][1]

        recommenderC1 = third[0][1]
        recommenderC2 = third[1][1]
        recommenderC3 = third[2][1]
        recommenderC4 = third[3][1]
        recommenderC5 = third[4][1]
        recommenderC6 = third[5][1]
        recommenderC7 = third[6][1]
        recommenderC8 = third[7][1]
        recommenderC9 = third[8][1]
        recommenderC10 = third[9][1]
        recommenderC11 = third[10][1]
        recommenderC12 = third[11][1]
        recommenderC13 = third[12][1]
        recommenderC14 = third[13][1]
        recommenderC15 = third[14][1]
        recommenderC16 = third[15][1]
        recommenderC17 = third[16][1]
        recommenderC18 = third[17][1]
        recommenderC19 = third[18][1]
        recommenderC20 = third[19][1]
        recommenderC21 = third[20][1]
        recommenderC22 = third[21][1]
        recommenderC23 = third[22][1]
        recommenderC24 = third[23][1]
        recommenderC25 = third[24][1]

        recommenderD1 = fourth[0][1]
        recommenderD2 = fourth[1][1]
        recommenderD3 = fourth[2][1]
        recommenderD4 = fourth[3][1]
        recommenderD5 = fourth[4][1]
        recommenderD6 = fourth[5][1]
        recommenderD7 = fourth[6][1]
        recommenderD8 = fourth[7][1]
        recommenderD9 = fourth[8][1]
        recommenderD10 = fourth[9][1]
        recommenderD11 = fourth[10][1]
        recommenderD12 = fourth[11][1]
        recommenderD13 = fourth[12][1]
        recommenderD14 = fourth[13][1]
        recommenderD15 = fourth[14][1]
        recommenderD16 = fourth[15][1]
        recommenderD17 = fourth[16][1]
        recommenderD18 = fourth[17][1]
        recommenderD19 = fourth[18][1]
        recommenderD20 = fourth[19][1]
        recommenderD21 = fourth[20][1]
        recommenderD22 = fourth[21][1]
        recommenderD23 = fourth[22][1]
        recommenderD24 = fourth[23][1]
        recommenderD25 = fourth[24][1]

        recommenderE1 = fifth[0][1]
        recommenderE2 = fifth[1][1]
        recommenderE3 = fifth[2][1]
        recommenderE4 = fifth[3][1]
        recommenderE5 = fifth[4][1]
        recommenderE6 = fifth[5][1]
        recommenderE7 = fifth[6][1]
        recommenderE8 = fifth[7][1]
        recommenderE9 = fifth[8][1]
        recommenderE10 = fifth[9][1]
        recommenderE11 = fifth[10][1]
        recommenderE12 = fifth[11][1]
        recommenderE13 = fifth[12][1]
        recommenderE14 = fifth[13][1]
        recommenderE15 = fifth[14][1]
        recommenderE16 = fifth[15][1]
        recommenderE17 = fifth[16][1]
        recommenderE18 = fifth[17][1]
        recommenderE19 = fifth[18][1]
        recommenderE20 = fifth[19][1]
        recommenderE21 = fifth[20][1]
        recommenderE22 = fifth[21][1]
        recommenderE23 = fifth[22][1]
        recommenderE24 = fifth[23][1]
        recommenderE25 = fifth[24][1]
    return render_template('recommendation.html', result_basements_01 = result_basements_01, result_central_air_01 = result_central_air_01, result_exterior_condition_01 = result_exterior_condition_01, result_fireplaces_01 = result_fireplaces_01, result_garage_type_01 = result_garage_type_01, result_interior_condition_01 = result_interior_condition_01, result_market_value_01 = result_market_value_01, result_number_of_rooms_01 = result_number_of_rooms_01, result_number_stories_01 = result_number_stories_01, result_parcel_shape_01 = result_parcel_shape_01, result_street_designation_01 = result_street_designation_01, result_topography_01 = result_topography_01, result_total_area_01 = result_total_area_01, result_total_livable_area_01 = result_total_livable_area_01, result_type_heater_01 = result_type_heater_01, result_view_type_01 = result_view_type_01, result_building_description_01 = result_building_description_01, result_section_01 = result_section_01 ,input1a = input1a, input2a = input2a, input3a = input3a, input4a = input4a, input5a = input5a, input6a = input6a, input7a = input7a, input8a = input8a, input9a = input9a, input10a = input10a, input11a = input11a, input12a = input12a, input13a = input13a, input14a = input14a, input15a = input15a, input16a = input16a, input17a = input17a, input18a = input18a, input19a = input19a, input20a = input20a, input21a = input21a, input22a = input22a, input23a = input23a, input24a = input24a, input25a = input25a, recommenderA1 = recommenderA1, recommenderA2 = recommenderA2, recommenderA3 = recommenderA3, recommenderA4 = recommenderA4, recommenderA5 = recommenderA5, recommenderA6 = recommenderA6, recommenderA7 = recommenderA7, recommenderA8 = recommenderA8, recommenderA9 = recommenderA9, recommenderA10 = recommenderA10, recommenderA11 = recommenderA11, recommenderA12 = recommenderA12, recommenderA13 = recommenderA13, recommenderA14 = recommenderA14, recommenderA15 = recommenderA15, recommenderA16 = recommenderA16, recommenderA17 = recommenderA17, recommenderA18 = recommenderA18, recommenderA19 = recommenderA19, recommenderA20 = recommenderA20, recommenderA21 = recommenderA21, recommenderA22 = recommenderA22, recommenderA23 = recommenderA23, recommenderA24 = recommenderA24, recommenderA25 = recommenderA25, recommenderB1 = recommenderB1, recommenderB2 = recommenderB2, recommenderB3 = recommenderB3, recommenderB4 = recommenderB4, recommenderB5 = recommenderB5, recommenderB6 = recommenderB6, recommenderB7 = recommenderB7, recommenderB8 = recommenderB8, recommenderB9 = recommenderB9, recommenderB10 = recommenderB10, recommenderB11 = recommenderB11, recommenderB12 = recommenderB12, recommenderB13 = recommenderB13, recommenderB14 = recommenderB14, recommenderB15 = recommenderB15, recommenderB16 = recommenderB16, recommenderB17 = recommenderB17, recommenderB18 = recommenderB18, recommenderB19 = recommenderB19, recommenderB20 = recommenderB20, recommenderB21 = recommenderB21, recommenderB22 = recommenderB22, recommenderB23 = recommenderB23, recommenderB24 = recommenderB24, recommenderB25 = recommenderB25, recommenderC1 = recommenderC1, recommenderC2 = recommenderC2, recommenderC3 = recommenderC3, recommenderC4 = recommenderC4, recommenderC5 = recommenderC5, recommenderC6 = recommenderC6, recommenderC7 = recommenderC7, recommenderC8 = recommenderC8, recommenderC9 = recommenderC9, recommenderC10 = recommenderC10, recommenderC11 = recommenderC11, recommenderC12 = recommenderC12, recommenderC13 = recommenderC13, recommenderC14 = recommenderC14, recommenderC15 = recommenderC15, recommenderC16 = recommenderC16, recommenderC17 = recommenderC17, recommenderC18 = recommenderC18, recommenderC19 = recommenderC19, recommenderC20 = recommenderC20, recommenderC21 = recommenderC21, recommenderC22 = recommenderC22, recommenderC23 = recommenderC23, recommenderC24 = recommenderC24, recommenderC25 = recommenderC25, recommenderD1 = recommenderD1, recommenderD2 = recommenderD2, recommenderD3 = recommenderD3, recommenderD4 = recommenderD4, recommenderD5 = recommenderD5, recommenderD6 = recommenderD6, recommenderD7 = recommenderD7, recommenderD8 = recommenderD8, recommenderD9 = recommenderD9, recommenderD10 = recommenderD10, recommenderD11 = recommenderD11, recommenderD12 = recommenderD12, recommenderD13 = recommenderD13, recommenderD14 = recommenderD14, recommenderD15 = recommenderD15, recommenderD16 = recommenderD16, recommenderD17 = recommenderD17, recommenderD18 = recommenderD18, recommenderD19 = recommenderD19, recommenderD20 = recommenderD20, recommenderD21 = recommenderD21, recommenderD22 = recommenderD22, recommenderD23 = recommenderD23, recommenderD24 = recommenderD24, recommenderD25 = recommenderD25, recommenderE1 = recommenderE1, recommenderE2 = recommenderE2, recommenderE3 = recommenderE3, recommenderE4 = recommenderE4, recommenderE5 = recommenderE5, recommenderE6 = recommenderE6, recommenderE7 = recommenderE7, recommenderE8 = recommenderE8, recommenderE9 = recommenderE9, recommenderE10 = recommenderE10, recommenderE11 = recommenderE11, recommenderE12 = recommenderE12, recommenderE13 = recommenderE13, recommenderE14 = recommenderE14, recommenderE15 = recommenderE15, recommenderE16 = recommenderE16, recommenderE17 = recommenderE17, recommenderE18 = recommenderE18, recommenderE19 = recommenderE19, recommenderE20 = recommenderE20, recommenderE21 = recommenderE21, recommenderE22 = recommenderE22, recommenderE23 = recommenderE23, recommenderE24 = recommenderE24, recommenderE25 = recommenderE25)

@app.route('/hasil2', methods=['POST'])
def result2():
    if request.method == 'POST':
        input = request.form
        basements = input["basements"]
        if basements == '0':
            print_basements = "None"
        elif basements == 'A':
            print_basements = "Full Finished"
        elif basements == 'B':
            print_basements = "Full Semi-Finished"
        elif basements == 'C':
            print_basements = "Full Unfinished"
        elif basements == 'D':
            print_basements = "Full Unknown Finished"
        elif basements == 'E':
            print_basements = "Partial Finished"
        elif basements == 'F':
            print_basements = "Partial Semi-Finished"
        elif basements == 'G':
            print_basements = "Partial Unfinished"
        elif basements == 'H':
            print_basements = "Partial Unknown Finished"
        elif basements == 'I':
            print_basements = "Unknown Size - Finished"
        elif basements == 'J':
            print_basements = "Unknown Size - Semi-Finished"

        central_air = input["central_air"]
        if central_air == 'Y':
            print_central_air = "Using (Yes)"
        elif central_air == 'N':
            print_central_air = "Not Using (No)"

        exterior_condition = input["exterior_condition"]
        if exterior_condition == "2":
            print_exterior_condition = "New / Rehabbed – Noticeably New Construction"
        elif exterior_condition == "3":
            print_exterior_condition = "Above Average"
        elif exterior_condition == "4":
            print_exterior_condition = "Average – Would Be Typical"
        elif exterior_condition == "5":
            print_exterior_condition = "Below Average"
        elif exterior_condition == "6":
            print_exterior_condition = "Vacant – No occupancy"
        elif exterior_condition == "7":
            print_exterior_condition = "Sealed / Structurally Compromised"

        fireplaces = input["fireplaces"]

        garage_type = input["garage_type"]
        if garage_type == "0":
            print_garage_type = "None"
        elif garage_type == "A":
            print_garage_type = "Basement / Built-In"
        elif garage_type == "B":
            print_garage_type= "Attached Garage"
        elif garage_type == "C":
            print_garage_type = "Detached Garage"
        elif garage_type == "F":
            print_garage_type = "Converted"

        interior_condition = input["interior_condition"]
        if interior_condition == "2":
            print_interior_condition = "New / Rehabbed – Noticeably New Construction"
        elif interior_condition == "3":
            print_interior_condition = "Above Average"
        elif interior_condition == "4":
            print_interior_condition = "Average – Would Be Typical"
        elif interior_condition == "5":
            print_interior_condition = "Below Average"
        elif interior_condition == "6":
            print_interior_condition = "Vacant – No occupancy"
        elif interior_condition == "7":
            print_interior_condition = "Sealed / Structurally Compromised"

        number_of_rooms = input["number_of_rooms"]

        market_value = input["market_value"]

        parcel_shape = input["parcel_shape"]
        if parcel_shape == "A":
            print_parcel_shape = "Irregular"
        elif parcel_shape == "B":
            print_parcel_shape = "Grossly Irregular"
        elif parcel_shape == "C":
            print_parcel_shape = "Triangular"
        elif parcel_shape == "D":
            print_parcel_shape = "Right of Way"
        elif parcel_shape == "E":
            print_parcel_shape = "Rectangular"

        topography = input["topography"]
        if topography == "1":
            print_topography = "Above Street Level"
        elif topography == "2":
            print_topography = "Below Street Level"
        elif topography == "3":
            print_topography = "Flood Plain or Flood Hazard Zone"
        elif topography == "4":
            print_topography = "Rocky"
        elif topography == "5":
            print_topography = "Not Identified"
        elif topography == "6":
            print_topography = "Level"

        total_area = input["total_area"]

        total_livable_area = input["total_livable_area"]

        type_heater = input["type_heater"]
        if type_heater == "0":
            print_type_heater = "None"
        elif type_heater == "A":
            print_type_heater = "Hot Air (Ducts)"
        elif type_heater == "B":
            print_type_heater = "Hot Water (Radiators or Baseboards)"
        elif type_heater == "C":
            print_type_heater = "Electric Baseboard"
        elif type_heater == "D":
            print_type_heater = "Heat Pump (Outside Unit)"
        elif type_heater == "E":
            print_type_heater = "Other (Portable Heater)"
        elif type_heater == "F":
            print_type_heater = "Radiant"
        elif type_heater == "G":
            print_type_heater = "Undetermined"

        view_type = input["view_type"]
        if view_type == "A":
            print_view_type = "Cityscape / Skyline"
        elif view_type == "B":
            print_view_type = "Flowing Water"
        elif view_type == "C":
            print_view_type = "Park / Green Area"
        elif view_type == "D":
            print_view_type = "Commercial"
        elif view_type == "E":
            print_view_type = "Industrial"
        elif view_type == "H":
            print_view_type = "Edifice / Landmark"
        elif view_type == "I":
            print_view_type = "Typical / Other"

        building_description = input["building_description"]
        if building_description == "FRAME":
            print_building_description = "Frame"
        elif building_description == "MASONRY":
            print_building_description = "Masonry"
        elif building_description == "MASONRY+OTHER":
            print_building_description = "Masonry + Other"
        elif building_description == "STONE":
            print_building_description = "Stone"

        abc2 = [[basements, central_air, exterior_condition, fireplaces, garage_type, interior_condition, market_value, number_of_rooms, parcel_shape, topography, total_area, total_livable_area, type_heater, view_type, building_description]]
        does2 = pd.DataFrame(data=abc2, columns=['basements', 'central_air', 'exterior_condition', 'fireplaces', 'garage_type', 'interior_condition', 'market_value', 'number_of_rooms', 'parcel_shape', 'topography', 'total_area', 'total_livable_area', 'type_heater', 'view_type', 'building_description'])
        prediction2 = Model_Classifier.predict(does2)[0]
    return render_template('result2.html', data = input, pred = prediction2, result_basements = print_basements, result_central_air = print_central_air, result_exterior_condition = print_exterior_condition, result_garage_type = print_garage_type, result_interior_condition = print_interior_condition, result_parcel_shape = print_parcel_shape, result_topography = print_topography, result_type_heater = print_type_heater, result_view_type = print_view_type, result_building_description = print_building_description)

if __name__ == "__main__":
    Model_Regressor = joblib.load("Model_PHL_Building_Regressor_DT")
    Model_Classifier = joblib.load("Model_PHL_Building_Classification_RF")
    app.run(debug=True)