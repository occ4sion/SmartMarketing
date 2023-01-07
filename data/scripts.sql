-- Худшие клиенты
SELECT 
    id, 
    conversion * cost + conversion * activity AS benefit 
FROM user
ORDER BY benefit ASC 
LIMIT 10;

-- Бесполезные активы
SELECT 
    id, 
    conversion * cost / (current_date - contract_date) AS benefit 
FROM user
ORDER BY benefit ASC 
LIMIT 10;

-- Самые длинные кампании
SELECT 
    id, 
    rounds
FROM campaign
ORDER BY campaign DESC 
LIMIT 10;