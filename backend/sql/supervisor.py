get_patients_sql = """
SELECT 
 sa.patient_id       AS 'profileId',
 pp.profile_name     AS 'profileName'
FROM profile pr
LEFT JOIN supervisor_patient sa on sa.supervisor_id = pr.profile_id
LEFT JOIN profile pp on pp.profile_id = sa.patient_id
WHERE sa.supervisor_id = :supervisor_id
"""