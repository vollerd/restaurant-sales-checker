import datetime
import math

### get date from user ###
search_date = str(input("Please enter the date(YYYY-MM-DD): "))
search_date = datetime.datetime.strptime(search_date, "%Y-%m-%d")

### Read the sql file ito a string ###
with open("database.sql", "r", encoding="utf-8") as f:
    string = f.read()

### get list of shops and offer to user to select one ###
shops = string.split("INSERT INTO `shops`")[1].split("--")[0]
shop_list = shops.split("(")
count=0

for i in shop_list:
    count += 1
    if count>2:
        print(i.split("',")[0].replace("'","").replace(",",""))

### get shop from the user ###
print("---------")
search_shop = int(input("Please enter the shop: "))

year = search_date.year
month = search_date.month
day = search_date.day

#choice = int(input("1- Single   2-Aggregate : "))

choice = 1
if choice == 1:
  bd=0
  ### Get # of business days in the month ###
  bd_data = string.split("INSERT INTO `business_days`")[1].split("--")[0]
  ### if same year, month and shop, and bd=1 then increase count ###
  bd_list = bd_data.split("(")

  count = 0
  for i in bd_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[2][2:9]
          temp_bd = int(i.split(",")[4])
          if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:7]: # and temp_bd == 1:
              bd += 1


  ### Get monthly fixed costs for the shop then calculate daily ###
  fixed_costs = string.split("INSERT INTO `monthly_fixed_costs`")[1].split("--")[0]
  fc_list = fixed_costs.split("(")

  count = 0
  labor = 0
  rent = 0
  platform = 0
  others = 0

  for i in fc_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[2][2:9]
          if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:7]:
              labor += int(i.split(",")[3])
              rent += int(i.split(",")[4])
              platform += int(i.split(",")[5])
              others += int(i.split(",")[6])

  ### get daily report id ###
  dr_data = string.split("INSERT INTO `daily_reports`")[1].split("--")[0]
  dr_list = dr_data.split("(")

  dr_no = 0
  dr_no_lunch = 0

  count = 0
  for i in dr_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[5].replace("'","").strip()
          temp_dinner = int(i.split(",")[6])
          temp_id = int(i.split(",")[0])
          #print(f"{temp_shop} , {temp_date} , {temp_dinner} , {temp_id}")
          if int(temp_shop) == int(search_shop):
              if str(temp_date) == str(search_date)[:10]:
                  if temp_dinner == 2:
                      dr_no = temp_id
                  elif temp_dinner == 1:
                      dr_no_lunch = temp_id

  part_pay = 0
  pt_data = string.split("INSERT INTO `part_time_job_payments`")[1].split("--")[0]
  pt_list = pt_data.split("(")


  count = 0
  for i in pt_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_report = int(i.split(",")[2])
          if int(temp_shop) == int(search_shop) and temp_report == int(dr_no):
              part_pay += int(i.split(",")[3].replace("'",""))
          if int(temp_shop) == int(search_shop) and temp_report == int(dr_no_lunch):
              part_pay += int(i.split(",")[3].replace("'",""))

  #### Accounts payables and daily cash flows ###
  acc_pay = 0
  other_x = 0
  ap_data = string.split("INSERT INTO `accounts_payables`")[1].split("--")[0]
  ap_list = ap_data.split("(")

  count = 0
  for i in ap_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[5].replace("'","").strip()
          temp_survey = i.split(",")[6].replace("'","")
          if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:10]:
              if int(temp_survey) == 0 or int(temp_survey) == 1:
                  acc_pay += int(i.split(",")[7].replace("'",""))
              if int(temp_survey) > 1:
                  others += int(i.split(",")[7].replace("'",""))

  cash_pay = 0
  cp_data = string.split("INSERT INTO `cash_flows`")[1].split("--")[0]
  cp_list = cp_data.split("(")
   
  count = 0
  for i in cp_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[4].replace("'","").strip()
          temp_with = str(i.split(",")[5])
          temp_survey = i.split(",")[9]
          if int(temp_shop) == int(search_shop):
              if temp_date == str(search_date)[:10]:
                  if int(temp_with.replace("'","")) == 1:
                      if int(temp_survey) == 0 or int(temp_survey) == 1:
                          cash_pay += int(i.split(",")[10].replace("'",""))
                      if int(temp_survey) > 1:
                          other_x += int(i.split(",")[10].replace("'",""))
                          print(int(i.split(",")[10].replace("'","")))
                          print(others)


  print("\nDaily costs")
  print("-----------")
  total =(round(labor/bd))+part_pay+round(rent/bd)+round(platform/bd)+round(others/bd)+cash_pay+acc_pay
  print(f"TOTAL: {total} , labor: {(round(labor/bd))+part_pay}, foodstuff: {cash_pay+acc_pay}, rent: {round(rent/bd)}, platform: {round(platform/bd)}, others: {round(others/bd)+other_x}")



####### AGGREGATE #######
choice = 2

search_date = datetime.datetime.today().replace(day=1).replace(month=month)
if choice == 2:
    bd=0
    ### Get # of business days in the month ###
    bd_data = string.split("INSERT INTO `business_days`")[1].split("--")[0]
    ### if same year, month and shop, and bd=1 then increase count ###
    bd_list = bd_data.split("(")

    count = 0
    for i in bd_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[2][2:9]
          temp_bd = int(i.split(",")[4])
          if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:7]:# and temp_bd == 1:
              bd += 1


    ### Get monthly fixed costs for the shop then calculate daily ###
    fixed_costs = string.split("INSERT INTO `monthly_fixed_costs`")[1].split("--")[0]
    fc_list = fixed_costs.split("(")

    count = 0
    labor = 0
    rent = 0
    platform = 0
    others = 0

    for i in fc_list:
      count += 1
      if count > 2:
          temp_shop = i.split(",")[1]
          temp_date = i.split(",")[2][2:9]
          if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:7]:
              labor += int(i.split(",")[3])
              rent += int(i.split(",")[4])
              platform += int(i.split(",")[5])
              others += int(i.split(",")[6])

    agg_total = 0
    agg_labor = 0
    agg_rent = 0
    agg_platform = 0
    agg_others = 0
    agg_foods = 0

    for d in range(1,day+1):
      search_date = datetime.datetime.today().replace(day=1).replace(month=month).replace(day=d)
      ### get daily report id ###
      dr_data = string.split("INSERT INTO `daily_reports`")[1].split("--")[0]
      dr_list = dr_data.split("(")

      dr_no = 0
      dr_no_lunch = 0

      count = 0
      for i in dr_list:
          count += 1
          if count > 2:
              temp_shop = i.split(",")[1]
              temp_date = i.split(",")[5].replace("'","").strip()
              temp_dinner = int(i.split(",")[6])
              temp_id = int(i.split(",")[0])
              #print(f"{temp_shop} , {temp_date} , {temp_dinner} , {temp_id}")
              if int(temp_shop) == int(search_shop):
                  if str(temp_date) == str(search_date)[:10]:
                      if temp_dinner == 2:
                          dr_no = temp_id
                      elif temp_dinner == 1:
                          dr_no_lunch = temp_id

      part_pay = 0
      pt_data = string.split("INSERT INTO `part_time_job_payments`")[1].split("--")[0]
      pt_list = pt_data.split("(")


      count = 0
      for i in pt_list:
          count += 1
          if count > 2:
              temp_shop = i.split(",")[1]
              temp_report = int(i.split(",")[2])
              if int(temp_shop) == int(search_shop) and temp_report == int(dr_no):
                  part_pay += int(i.split(",")[3].replace("'",""))
              if int(temp_shop) == int(search_shop) and temp_report == int(dr_no_lunch):
                  part_pay += int(i.split(",")[3].replace("'",""))

      #### Accounts payables and daily cash flows ###
      acc_pay = 0
      others_x = 0
      ap_data = string.split("INSERT INTO `accounts_payables`")[1].split("--")[0]
      ap_list = ap_data.split("(")

      count = 0
      for i in ap_list:
          count += 1
          if count > 2:
              temp_shop = i.split(",")[1]
              temp_date = i.split(",")[5].replace("'","").strip()
              temp_survey = i.split(",")[6].replace("'","")
              if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:10]:
                  if int(temp_survey) == 0 or int(temp_survey) == 1:
                      acc_pay += int(i.split(",")[7].replace("'",""))
                  if int(temp_survey) > 1:
                      others_x += int(i.split(",")[7].replace("'",""))

      cash_pay = 0
      cp_data = string.split("INSERT INTO `cash_flows`")[1].split("--")[0]
      cp_list = cp_data.split("(")
       
      count = 0
      for i in cp_list:
          count += 1
          if count > 2:
              temp_shop = i.split(",")[1]
              temp_date = i.split(",")[4].replace("'","").strip()
              temp_with = str(i.split(",")[5])
              temp_survey = i.split(",")[9]
              if int(temp_shop) == int(search_shop):
                  if temp_date == str(search_date)[:10]:
                      if int(temp_with.replace("'","")) == 1:
                          if int(temp_survey) == 0 or int(temp_survey) == 1:
                              cash_pay += int(i.split(",")[10].replace("'",""))
                          if int(temp_survey) > 1:
                              others_x += int(i.split(",")[10].replace("'",""))

      #print(temp_date)
      #print(str(search_date)[:10]) 

      #print(dr_no)
      ### get part time daily cost ###

      #print("Monthly costs")
      #print("-------------")
      #print(f"labor: {labor}, rent: {rent}, platform: {platform}, others: {others}")
      bd_data = string.split("INSERT INTO `business_days`")[1].split("--")[0]
  ### if same year, month and shop, and bd=1 then increase count ###
      bd_list = bd_data.split("(")

      count = 0
      bus = 0
      for i in bd_list:
          count += 1
          if count > 2:
              temp_shop = i.split(",")[1]
              temp_date = i.split(",")[2][2:12]
              temp_bd = int(i.split(",")[4])
              if int(temp_shop) == int(search_shop) and temp_date == str(search_date)[:10] and temp_bd == 1:
                bus=1
      #if bus==1:
      print(f"date: {str(search_date)[:11]}. labor: {(round(labor/bd))+part_pay}, foodstuff: {cash_pay+acc_pay}, rent: {round(rent/bd)}, platform: {round(platform/bd)}, others: {round(others/bd)+others_x}")
      agg_rent += rent/bd
      agg_platform += platform/bd
      agg_others += (others/bd)+others_x
      agg_foods += (cash_pay+acc_pay)
      agg_labor += (labor/bd)+part_pay
      #if bus == 0:
      #  agg_labor += part_pay
      #  print(f"** date: {str(search_date)[:11]}. labor: {(round(labor/bd))+part_pay}, foodstuff: {cash_pay+acc_pay}, rent: {round(rent/bd)}, platform: {round(platform/bd)}, others: {round(others/bd)}")
    print(bd)
    agg_total=agg_labor+agg_foods+agg_rent+agg_platform+agg_others
    print("\nAccumulated costs")
    print("-----------")
    print(f"TOTAL: {round(agg_total)} , labor: {round(agg_labor)}, foodstuff: {round(agg_foods)}, rent: {round(agg_rent)}, platform: {round(agg_platform)}, others: {round(agg_others)}")