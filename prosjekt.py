from statistics import mean
import matplotlib.pyplot as mpl
from datetime import datetime
from collections import defaultdict

temperaturer = [-5, 2, 6, 13, 9, 22, 28, 19, 24, 12, 5, 1, -3, -8, 2, 8, 15, 18, 21, 26, 21, 31, 15, 4, 1, -2]
dogn_nedbor = [2, 5, 0, 0, 0, 3, 6, 4, 0, 0, 5, 0, 12, 12, 12, 12, 7, 19]

temperaturer_tidspunkter = []
for index in range(len(temperaturer)):
    temperaturer_tidspunkter.append(index)

def check(ListFloat,Int):           # enter list and value, checks if values in list are greater or equal to Int value and returns list of those values
    check_list = []
    for i in range(0,len(ListFloat)):
        if Int <= ListFloat[i]:
            check_list.append(ListFloat[i])
    return check_list

def reverse_check(ListFloat,Int):           # enter list and value, checks if values in list are greater or equal to Int value and returns list of those values
    check_list = []
    for i in range(0,len(ListFloat)):
        if Int > ListFloat[i]:
            check_list.append(ListFloat[i])
    return check_list

def delta_finder(List):             # returns a list of deltas
    delta_list = []
    for i in range(0,len(List)-1):
        delta = List[i+1] - List[i]
        delta_list.append(delta)
    return delta_list


def delta_output(delta_list):                   #outputs delta
    for i in range(0,len(delta_list)):
        delta = delta_list[i]

        if delta < 0:
            print(f"index {i} er synkende ({delta_list[i]})")
        elif delta == 0:
            print(f"index {i} er uforandret ({delta_list[i]})")
        else: 
            print(f"index {i} er stigende ({delta_list[i]})")


def nullzero_combo_finder(List):    # finds how many conescutive zeros there are in a given list and returns int of them
    null_combo = 0
    temp_null_combo = 0
    
    for value in List:
        
        if value == 0:
            temp_null_combo += 1
            
            if null_combo < temp_null_combo:
                null_combo = temp_null_combo
        else:
            temp_null_combo = 0

    return null_combo


def datasett(x, y):                 # finds trend between 2 lists
    a_top = 0
    a_bot = 0

    for i in range(0,len(x)):
        a_top += (x[i]-mean(x))*(y[i]-mean(y))
        a_bot += (x[i]-mean(x))**2

    a = a_top/a_bot
    b = mean(y)-a*mean(x)

    return (a,b)


def plantevekst(List):              # takes a list, removes 5 from each index, if any index is negative, turn it to zero, returns updated list
    plant_temp = 0
    plant_temp_sum = 0

    for value in List:
        plant_temp = value - 5

        if plant_temp < 0:
            plant_temp = 0 

        plant_temp_sum += plant_temp
        
    return plant_temp_sum


sommer_dager = check(temperaturer,20)              # checks what temperatures are what
høysommer_dager = check(temperaturer,25)
trope_dager = check(temperaturer,30)

delta_output(delta_finder(temperaturer))
print("- - -")

print(f"{nullzero_combo_finder(dogn_nedbor)} dager uten nedbør")
print("- - -")

trend_a = datasett(temperaturer_tidspunkter, temperaturer)[0]       #trenden i datasettet
if trend_a < 0:
    print("trenden er synkende")
elif trend_a > 0:
    print("trenden er stigende")
else:
    print("trenden er uforandret........... B)")
print("- - -")

print(f"Den totale planteveksten er: {plantevekst(temperaturer)}")        #total plantgrowth

# format: Navn ; Stasjon ; Tid(norsk normaltid) ; Snødybde ; Nedbør (døgn) ; Middeltemperatur (døgn) ; Gjennomsnittlig skydekke (døgn) ; Høyeste middelvind (døgn)

location = __file__.replace("prosjekt.py","")

file_data = open(f"{location}snoedybder_vaer_fem_stasjoner_dogn.csv_")
list_data = file_data.readlines()
list_data.pop(0)
list_data.pop(len(list_data)-1)

Processed_data = []

def lagre_som_hashmap(list_data):
    for data in list_data:
        i = 0
        temp_dict = {"Sted":"","Stasjon":"","Dato":"","Snødybde":0.0,"Nedbør":0.0,"Middel temperatur":0.0,"Gjennomsnittlig skydekke":0.0,"Høyeste middelvind":0.0}

        for value in data.split(";"):

            if value == "-" or value == "-\n":
                value = "?"
                continue

            if i > 2:
                value = value.replace(",",".")

            match i:
                case 0:
                    temp_dict["Sted"] = value
                case 1:
                    temp_dict["Stasjon"] = value
                case 2:
                    temp_dict["Dato"] = value
                case 3:
                    temp_dict["Snødybde"] = float(value)
                case 4:
                    temp_dict["Nedbør"] = float(value)
                case 5:
                    temp_dict["Middel temperatur"] = float(value)
                case 6:
                    temp_dict["Gjennomsnittlig skydekke"] = float(value)
                case 7:
                    temp_dict["Høyeste middelvind"] = float(value)
            i += 1

        Processed_data.append(temp_dict)
    return Processed_data 

stasjon_name_list = ['SN12960','SN13420','SN10380','SN40420','SN69100']

def fordel_data_per_stasjon(dict_list:list[dict]):

    SN12960_list = []
    SN13420_list = []
    SN10380_list = []
    SN40420_list = []
    SN69100_list = []

    for data in dict_list:
        match data["Stasjon"]:

            case "SN12960":
                SN12960_list.append(data)
            case "SN13420":
                SN13420_list.append(data)
            case "SN10380":
                SN10380_list.append(data)
            case "SN40420":
                SN40420_list.append(data)
            case "SN69100":
                SN69100_list.append(data)

    return ((SN12960_list,SN13420_list,SN10380_list,SN40420_list,SN69100_list))

def er_i_skisesong(Dato):
    if int(Dato[3:5]) >= 10 or int(Dato[3:5]) <= 6:
        return True
    else:
        return False

def finn_skifører(dict_list:list[dict]):

    temp_list = []
    finished_list = []

    for data in dict_list:

        if er_i_skisesong(data["Dato"]):
            temp_list.append(data["Snødybde"])
        else:
            if len(temp_list) != 0:
                finished_list.append(temp_list)
            temp_list = []

    if len(temp_list) != 0:
        finished_list.append(temp_list)

    return finished_list

dict_list = lagre_som_hashmap(list_data)
stasjon_data_list = fordel_data_per_stasjon(dict_list)

skifører_list = []
for stasjon in stasjon_data_list:
    stasjon_skiføre = finn_skifører(stasjon)

    temp_list = []

    for value in stasjon_skiføre:
        done = check(value,20)
        if len(done) != 0:
            temp_list.append(done)

    skifører_list.append(temp_list)

def data_for_year(dict_list:list[dict],wanted_data,filter_val):

    temp_dict = {}

    for data in dict_list:
        if er_i_skisesong(data["Dato"]):
            if data["Dato"][6:10] in temp_dict.keys():
                if data[wanted_data] > filter_val:
                    temp_dict[data["Dato"][6:10]] += 1
            else: 
                temp_dict.update({data["Dato"][6:10]:1})

    return (temp_dict)

color_list = ['red','blue','yellow','green','purple']
for i in range(0,len(stasjon_data_list)):
    xy_list = data_for_year(stasjon_data_list[i],"Snødybde",20)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(xy_list[aar])

    mpl.scatter(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')

    #print("trend for stasjon",i,datasett(aar_list,lengde_list))

all_aar_list = aar_list

mpl.title("snow depth for all stasjon")
mpl.legend()
mpl.show()

def data_filterer(input_dict,data_wanted,min_data):
    preproccesed = {}
    for data in input_dict:
        if data[data_wanted] == '?':
            continue

        year = int(data['Dato'][6:10])

        if year not in preproccesed:
            preproccesed[year] = [data[data_wanted]]
        else:
            preproccesed[year].append(data[data_wanted])

    proccesed = {}

    for year in preproccesed:
        if len(preproccesed[year]) > (min_data-1):
            proccesed[year] = preproccesed[year]

    return proccesed
        
for i in range(0,len(stasjon_data_list)):

    xy_list = data_filterer(stasjon_data_list[i],"Middel temperatur",300)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(plantevekst(xy_list[aar]))

    mpl.plot(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("plantevekst for hver stasjon")
mpl.legend()
mpl.show()

for i in range(0,len(stasjon_data_list)):

    xy_list = data_filterer(stasjon_data_list[i],"Nedbør",300)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(nullzero_combo_finder(xy_list[aar]))

    print(lengde_list[0])
    mpl.plot(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("lengste tørke per år for hver stasjon")
mpl.legend()
mpl.show()

#drep meg
for i in range(0,len(stasjon_data_list)):

    xy_list = data_filterer(stasjon_data_list[i],"Gjennomsnittlig skydekke",300)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(sum(reverse_check(xy_list[aar],3)))

    mpl.plot(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("antall penværsdager per år for all stasjon")
mpl.legend()
mpl.show()

for i in range(0,len(stasjon_data_list)):

    xy_list = data_filterer(stasjon_data_list[i],"Høyeste middelvind",300)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(max(xy_list[aar]))

    mpl.plot(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("høyeste middelvind per år for all stasjon")
mpl.legend()
mpl.show()

for i in range(0,len(stasjon_data_list)):

    xy_list = data_filterer(stasjon_data_list[i],"Høyeste middelvind",300)

    aar_list = []
    lengde_list = []

    for aar in xy_list.keys():

        aar_list.append(int(aar))
        lengde_list.append(sorted(xy_list[aar])[round(len(xy_list)/2)])

    mpl.plot(aar_list,lengde_list,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("median middelvind per år for all stasjon")
mpl.legend()
mpl.show()

def monthly_average(temp_dict):
    month_temp = defaultdict(list)

    for data in temp_dict:
        dato = data["Dato"]
        temp = data["Middel temperatur"]

        if temp == '?':
            continue

        date_obj = datetime.strptime(dato,'%d.%m.%Y')
        month_year = date_obj.strftime('%B %Y')

        month_temp[month_year].append(temp)

    month_averages = {month:sum(temps) / len(temps) for month, temps in month_temp.items()}
    return month_averages


for i in range(0,len(stasjon_data_list)):
    monthly_average_temp = monthly_average(stasjon_data_list[i])
    sorted_months = sorted(monthly_average_temp.keys(),key=lambda d: datetime.strptime(d,'%B %Y'))
    sorted_avg_temp = [monthly_average_temp[month] for month in sorted_months]

    mpl.plot(sorted_months,sorted_avg_temp,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("avg temp per month per år for all stasjon")
mpl.xticks(rotation=90)
mpl.legend()
mpl.show()

for i in range(0,len(stasjon_data_list)):
    monthly_average_temp = monthly_average(stasjon_data_list[i])
    sorted_months = sorted(monthly_average_temp.keys(),key=lambda d: datetime.strptime(d,'%B %Y'))
    sorted_avg_temp = [monthly_average_temp[month] for month in sorted_months]

    temp_delta = delta_finder(sorted_avg_temp)

    mpl.plot(sorted_months[1:],temp_delta,color=color_list[i],label=f'stasjon {stasjon_name_list[i]}')
mpl.title("delta temp per month år for all stasjon")
mpl.xticks(rotation=90)
mpl.legend()
mpl.show()