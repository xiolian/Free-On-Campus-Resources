SELECT
    s.studentID,
    s.studentName,
    COUNT(DISTINCT a.advisor_id) AS advisor_count,
    COUNT(DISTINCT t.tutoring_id) AS tutoring_count,
    COUNT(DISTINCT sup.supply_id) AS supplies_count,
    COUNT(DISTINCT h.health_id) AS health_count,
    COUNT(DISTINCT asupp.support_id) AS academic_support_count,
    COUNT(DISTINCT f.funding_id) AS funding_count,
    (
      COUNT(DISTINCT a.advisor_id) +
      COUNT(DISTINCT t.tutoring_id) +
      COUNT(DISTINCT sup.supply_id) +
      COUNT(DISTINCT h.health_id) +
      COUNT(DISTINCT asupp.support_id) +
      COUNT(DISTINCT f.funding_id)
    ) AS total_resource_count

FROM Student AS s, AdvisorRecord AS a, TutoringRecord AS t, StudentSuppliesRecord AS sup, HealthRecord AS h, FundingRecord AS f, AcademicSupportRecord AS asupp
WHERE a.studentID   = s.studentID
AND t.studentID   = s.studentID
AND sup.studentID = s.studentID
AND h.studentID   = s.studentID
AND asupp.studentID = s.studentID
AND f.studentID   = s.studentID
GROUP BY s.studentID, s.studentName;

SELECT *
FROM academic_advising;

SELECT *
FROM academic_support;

SELECT *
FROM funding;

SELECT *
FROM health_services;

SELECT * 
FROM student_supplies;

SELECT * 
FROM tutoring;