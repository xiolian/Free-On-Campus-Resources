-- 1. Tutoring Queries
SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
WHERE subject LIKE 'CSE%';

SELECT tutoring_id, subject, building, location, weekday, start_time, end_time
FROM tutoring
GROUP BY subject, building, location, weekday, start_time, end_time;