-- 1. Tutoring Queries
SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
WHERE subject LIKE 'CSE%';

SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
GROUP BY subject, building, location, weekday, start_time, end_time;

-- 2. Joins of Tables
-- Find all resources available on mondays for all tables
select h.health_id, h.service, h.location, h.weekday,
       t.tutoring_id, t.subject, t.building, t.location, t.weekday,
       asupp.support_id, asupp.aca_supp_service, asupp.service_name, asupp.building, asupp.location, asupp.weekday
from health_services h, tutoring t, academic_support asupp
where h.weekday like 'Monday%' and t.weekday like 'Monday%' and asupp.weekday like 'Monday%';