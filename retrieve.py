import shutup; shutup.please()
import requests
import csv
import pandas as pd

api_key = "" # Get your own lol I had to do some interesting things to bypass the paywall, lets see if you can do it too. Plus you don't really need it anymore now that I DOWNLOADED THE WHOLE THING!

colleges = requests.get("http://universities.hipolabs.com/search?country=United+States").json()
collegelist = []
for i in colleges:
    collegelist.append(i['name'].split(',')[0])

print(collegelist)

info_ids_available = "acceptance_rate,act_cumulative_midpoint,act_cumulative_percentile25,act_cumulative_percentile75,admissions_website,aliases,application_website,average_aid_awarded_high_income,average_aid_awarded_lower_middle_income,average_aid_awarded_low_income,average_aid_awarded_middle_income,average_aid_awarded_upper_middle_income,average_financial_aid,avg_cost_of_attendance,avg_net_price,calendar_system,campus_image,city,class_size_range10_to19,class_size_range20_to29,class_size_range2_to9,class_size_range30_to39,class_size_range40_to49,class_size_range50_to99,class_size_range_over100,demographics_men,demographics_women,financial_aid_website,four_year_graduation_rate,fraternities_percent_participation,freshmen_live_on_campus,in_state_tuition,is_private,meal_plan_available,median_earnings_six_yrs_after_entry,median_earnings_ten_yrs_after_entry,men_varsity_sports,net_price_by_income_level0_to3000,net_price_by_income_level110001_plus,net_price_by_income_level30001_to48000,net_price_by_income_level48001_to75000,net_price_by_income_level75001_to110000,offers_study_abroad,on_campus_housing_available,out_of_state_tuition,percent_of_students_who_receive_financial_aid,percent_students_receiving_federal_grant_aid,percent_undergrads_awarded_aid,rankings_best_college_academics,rankings_best_college_athletics,rankings_best_college_campuses,rankings_best_college_food,rankings_best_college_locations,rankings_best_college_professors,rankings_best_colleges,rankings_best_colleges_for_art,rankings_best_colleges_for_biology,rankings_best_colleges_for_business,rankings_best_colleges_for_chemistry,rankings_best_colleges_for_communications,rankings_best_colleges_for_computer_science,rankings_best_colleges_for_design,rankings_best_colleges_for_economics,rankings_best_colleges_for_engineering,rankings_best_colleges_for_history,rankings_best_colleges_for_nursing,rankings_best_colleges_for_physics,rankings_best_greek_life_colleges,rankings_best_student_athletes,rankings_best_student_life,rankings_best_test_optional_colleges,rankings_best_value_colleges,rankings_colleges_that_accept_the_common_app,rankings_colleges_with_no_application_fee,rankings_hardest_to_get_in,rankings_hottest_guys,rankings_most_conservative_colleges,rankings_most_liberal_colleges,rankings_most_diverse_colleges,rankings_top_party_schools,region,sat_average,sat_composite_midpoint,sat_composite_percentile25,sat_composite_percentile75,sat_math_midpoint,sat_math_percentile25,sat_math_percentile75,sat_reading_midpoint,sat_reading_percentile25,sat_reading_percentile75,student_faculty_ratio,students_submitting_a_c_t,students_submitting_s_a_t,type_year,typical10_year_earnings,typical6_year_earnings,typical_books_and_supplies,typical_financial_aid,typical_misc_expenses,typical_room_and_board,undergrad_application_fee,undergraduate_size,women_only,women_varsity_sports".replace(',', '%2C')
info_ids_selector = info_ids_available

def get_college_info(college_name):
    url = f'https://api.collegeai.com/v1/api/autocomplete/colleges?api_key={api_key}'
    json_data = requests.get(url + '&query='+college_name).json()
    
    try:
        college_id = json_data['collegeList'][0]['unitId']
    except:
        return 1
    url = f'https://api.collegeai.com/v1/api/college/info?api_key={api_key}&college_unit_ids='+str(college_id)+'&info_ids='+info_ids_selector
    
    try:
        json_data = requests.get(url).json()['colleges'][0]
    except:
        return 1
    return json_data

y = get_college_info("harvard")

df = pd.DataFrame(columns=list(y.keys()))

total = len(collegelist)
iterator = 0

covered = []

for i in collegelist[:100]:
    iterator+=1
    print(f"Current College: {iterator}/{total}", end="\r")
    x = get_college_info(i)
    if x!=1 and x['collegeUnitId'] not in covered:
        for val in y.keys():
            if val in x.keys() and x[val] != "":
                x[val] = x[val]
            else:
                x[val] = "N/A"
                
        df = df.append(x, ignore_index=True)
        covered.append(x['collegeUnitId']) 
    else:
        total-=1
        iterator-=1

df.to_csv("college_info_2.csv")

print(f"Complete. {iterator}/{len(colleges)} covered.                                      ")