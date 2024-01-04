salt_sql = """
SELECT salt FROM account WHERE username=:username
"""

account_sql = """
SELECT account_id FROM account WHERE username=:username
"""

login_sql = """
SELECT EXISTS(
    SELECT * FROM account WHERE username=:username AND password=:password
)
"""

profiles_sql = """
SELECT 
 pr.profile_id       AS 'profileId',
 pr.profile_name     AS 'profileName',
 a.account_id        AS 'accountId',
CASE 
WHEN pa.profile_id IS NOT NULL THEN 'patient'
WHEN sv.profile_id IS NOT NULL THEN 'supervisor'
ELSE 'unknown'
END                  AS 'type'
FROM profile pr
LEFT JOIN account a on pr.account_id = a.account_id
LEFT JOIN patient pa on pr.profile_id = pa.profile_id
LEFT JOIN supervisor sv on pr.profile_id = sv.profile_id
WHERE a.username = :username
"""


profiles_from_id_sql = """
SELECT 
 pr.profile_id       AS 'profileId',
 pr.profile_name     AS 'profileName',
 a.account_id        AS 'accountId',
CASE 
WHEN pa.profile_id IS NOT NULL THEN 'patient'
WHEN sv.profile_id IS NOT NULL THEN 'supervisor'
ELSE 'unknown'
END                  AS 'type'
FROM profile pr
LEFT JOIN account a on pr.account_id = a.account_id
LEFT JOIN patient pa on pr.profile_id = pa.profile_id
LEFT JOIN supervisor sv on pr.profile_id = sv.profile_id
WHERE a.account_id = :account_id
"""