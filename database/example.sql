SELECT surname, firstname, email, cu.CountryCode, country FROM customer cu, country co
WHERE cu.CountryCode = co.CountryCode
AND cu.CountryCode = 'USA'
ORDER BY surname