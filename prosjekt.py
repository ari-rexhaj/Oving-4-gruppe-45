from statistics import mean

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