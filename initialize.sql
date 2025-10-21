-- ENTITIES

CREATE TABLE healthServices (
    healthCategory VARCHAR(50) PRIMARY KEY,
    healthBuilding VARCHAR(50) NOT NULL,
    healthLocation VARCHAR(50) NOT NULL,
    healthDate DATE NOT NULL,
    healthTime TIME NOT NULL
);

CREATE TABLE funding (
    fundingType VARCHAR(50) PRIMARY KEY,
    fundingBuilding VARCHAR(50) NOT NULL,
    fundingLocation VARCHAR(50) NOT NULL,
    fundingDate DATE NOT NULL,
    fundingTime TIME NOT NULL
);

CREATE TABLE student (
    studentID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentName VARCHAR(50) NOT NULL
); 

CREATE TABLE academicAdvising (
    advisorName VARCHAR(50) PRIMARY KEY,
    advisingBuilding VARCHAR(50) NOT NULL,
    advisingLocation VARCHAR(50) NOT NULL,
    advisingDate DATE NOT NULL,
    advisingTime TIME NOT NULL
);

CREATE TABLE academicSupport (
    acaSuppName VARCHAR(50) PRIMARY KEY,
    acaSuppBuilding VARCHAR(50) NOT NULL,
    acaSuppLocation VARCHAR(50) NOT NULL,
    acaSuppDate DATE NOT NULL,
    acaSuppTime TIME NOT NULL
);

CREATE TABLE tutoring (
    sessionID INTEGER PRIMARY KEY AUTOINCREMENT,
    courseName VARCHAR(50) NOT NULL,
    sessionDate DATE NOT NULL,
    sessionTime TIME NOT NULL,
    tutoringDepartment VARCHAR(50) NOT NULL,
    tutoringBuilding VARCHAR(50) NOT NULL,
    tutoringLocation VARCHAR(50) NOT NULL
);

CREATE TABLE studentSupplies (
    resourceType VARCHAR(50),
    department VARCHAR(50),
    stuSuppBuilding VARCHAR(50) NOT NULL,
    stuSuppLocation VARCHAR(50) NOT NULL,
    stuSuppDate DATE NOT NULL,
    stuSuppTime TIME NOT NULL,
    PRIMARY KEY (resourceType, department)
);

-- MM RELATIONSHIPS

CREATE TABLE studentSuppliesRecord (
    studentID VARCHAR(50) NOT NULL,
    resourceType VARCHAR(50) NOT NULL,
    stuDepartment VARCHAR(50) NOT NULL,
    stuSuppDate DATE NOT NULL,
    stuSuppTime TIME NOT NULL
);

CREATE TABLE tutoringRecord (
    studentID INTEGER NOT NULL,
    sessionID INTEGER NOT NULL,
    tutoringLocation VARCHAR(50) NOT NULL
);

CREATE TABLE fundingRecord (
    studentID INTEGER NOT NULL,
    fundingType VARCHAR(50) NOT NULL,
    FUNDINGLocation VARCHAR(50) NOT NULL,
    fundingDate DATE NOT NULL,
    fundingTime TIME NOT NULL
);

CREATE TABLE acaSuppRecord (
    studentID INTEGER NOT NULL,
    acaSuppType VARCHAR(50) NOT NULL,
    acaSuppLocation VARCHAR(50) NOT NULL
);

CREATE TABLE healthRecord (
    studentID INTEGER NOT NULL,
    healthCategory VARCHAR(50) NOT NULL,
    healthLocation VARCHAR(50) NOT NULL,
    healthDate DATE NOT NULL,
    healthTime TIME NOT NULL
);

