clash_check_sql = """
WITH selected_active_ingredients AS (
    SELECT mag.medicine_name, mag.active_ingredient
    FROM medicine_active_ingredients mag
    WHERE mag.medicine_name IN ({medicine_list_str})
)
SELECT DISTINCT
    sai1.medicine_name AS medicine_1,
    sai2.medicine_name AS medicine_2,
    ct.clash_level
FROM clashing_ingredients ct
INNER JOIN selected_active_ingredients sai1 ON ct.ingredient_1 = sai1.active_ingredient
INNER JOIN selected_active_ingredients sai2 ON ct.ingredient_2 = sai2.active_ingredient
"""

get_medicines_sql = """
SELECT PUM.medicine_name as medicine_name, 
PUM.frequency as frequency,
DT.start_date as start_date
FROM patient_uses_medicine as PUM 
INNER JOIN dosage_time as DT 
ON (PUM.patient_id=DT.patient_id AND PUM.medicine_name=DT.medicine_name)  
WHERE PUM.patient_id={profile_id}
"""