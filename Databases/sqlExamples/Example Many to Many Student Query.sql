- This query links students to all four major resource types (Tutoring, Supplies, Health, Academic Support)
-- via their respective record tables, aggregates the resource details, and groups the final output.

SELECT
    S.studentName,
    S.studentID,
    ResourceDetails.service,
    ResourceDetails.location,
    ResourceDetails.building,
    ResourceDetails.weekday,
    ResourceDetails.start_time,
    ResourceDetails.end_time
FROM
    Student S
JOIN
    (
        -- 1. Tutoring Resources (M:M relationship: Student -> TutoringRecord -> tutoring)
        SELECT
            TR.studentID,
            T.subject AS service,
            T.location,
            T.building,
            T.weekday,
            T.start_time,
            T.end_time
        FROM
            TutoringRecord TR
        JOIN
            tutoring T ON TR.tutoring_id = T.tutoring_id

        UNION ALL

        -- 2. Student Supplies (M:M relationship: Student -> StudentSuppliesRecord -> student_supplies)
        SELECT
            SSR.studentID,
            SS.item AS service,
            SS.location,
            SS.building,
            SS.weekday,
            SS.start_time,
            SS.end_time
        FROM
            StudentSuppliesRecord SSR
        JOIN
            student_supplies SS ON SSR.supply_id = SS.supply_id

        UNION ALL

        -- 3. Health Services (M:M relationship: Student -> HealthRecord -> health_services)
        -- Note: Building, Start Time, and End Time are not available in the source tables, so we use NULL.
        SELECT
            HR.studentID,
            H.service AS service,
            H.location,
            NULL AS building,
            H.weekday,
            NULL AS start_time,
            NULL AS end_time
        FROM
            HealthRecord HR
        JOIN
            health_services H ON HR.health_id = H.health_id

        UNION ALL

        -- 4. Academic Support (M:M relationship: Student -> AcademicSupportRecord -> academic_support)
        -- Note: Start Time and End Time are not available in the source tables, so we use NULL.
        SELECT
            ASR.studentID,
            A.service_name AS service,
            A.location,
            A.building,
            A.weekday,
            NULL AS start_time,
            NULL AS end_time
        FROM
            AcademicSupportRecord ASR
        JOIN
            academic_support A ON ASR.support_id = A.support_id

    ) AS ResourceDetails ON S.studentID = ResourceDetails.studentID
GROUP BY
    S.studentName,
    S.studentID,
    ResourceDetails.service,
    ResourceDetails.location,
    ResourceDetails.building,
    ResourceDetails.weekday,
    ResourceDetails.start_time,
    ResourceDetails.end_time
ORDER BY
    S.studentName, ResourceDetails.weekday, ResourceDetails.start_time;
