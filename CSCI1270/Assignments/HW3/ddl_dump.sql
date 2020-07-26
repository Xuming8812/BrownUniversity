
--contents of ddl\_dump.sql

--1. create table department
CREATE TABLE department(
    dept_id SERIAL NOT NULL,
    dept TEXT NOT NULL,
    CONSTRAINT dept_pk PRIMARY KEY(dept_id)
);

--2.create table of instructor
CREATE TABLE instructor(
    inst_id SERIAL NOT NULL,
    inst TEXT NOT NULL,
    office TEXT NOT NULL,
    CONSTRAINT inst_pk PRIMARY KEY(inst_id)
);

--3.create table of evaluation
CREATE TABLE evaluation(
    evaluation_id SERIAL NOT NULL,
    evaluation TEXT NOT NULL,
    CONSTRAINT eval_pk PRIMARY KEY(evaluation_id)
);

--4. create table of course
CREATE TABLE course(
    c_id SERIAL NOT NULL,
    dept_id INT NOT NULL,
    inst_id INT NOT NULL,
    CONSTRAINT course_pk PRIMARY KEY(c_id),
    CONSTRAINT course_dept_fk FOREIGN KEY(dept_id) references department,
    CONSTRAINT course_inst_fk FOREIGN KEY(inst_id) references instructor,
    CONSTRAINT course_range CHECK(
        CASE
            WHEN dept_id = 1 THEN c_id>0 AND c_id<151
            WHEN dept_id = 2 THEN c_id>150 AND c_id<301
            WHEN dept_id = 3 THEN c_id>300 AND c_id<501
        END 
    )
);

--5.create table of course-eval
CREATE TABLE course_eval(
    c_id INT NOT NULL,
    evaluation_id INT,
    CONSTRAINT course_eval_pk PRIMARY KEY(c_id, evaluation_id),
    CONSTRAINT course_fk FOREIGN KEY(c_id) references course,
    CONSTRAINT eval_fk FOREIGN KEY(evaluation_id) references evaluation
);

--6.create table of course-time
CREATE TABLE course_time(
    c_id INT NOT NULL,
    sect CHAR(1) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT time_pk PRIMARY KEY(c_id, sect),
    CONSTRAINT time_fk FOREIGN KEY(c_id) references course
);

--add total participation
ALTER TABLE course_time
ADD CONSTRAINT course_time_pk FOREIGN KEY(c_id) REFERENCES course
DEFERRABLE INITIALLY IMMEDIATE;

--7.populate table
INSERT INTO department(dept)
VALUES('CS'),('MATH'),('PHYS');

INSERT INTO instructor(inst,office)
VALUES  ('Eddie Kolher','345'),
        ('Stratos Idreos','346'),
        ('Andy Pavlo','346'),
        ('Nesime Tatbul','347');

INSERT INTO evaluation(evaluation)
VALUES  ('HW, Midterm, Final'),
        ('Project, Final'),
        ('HW'),
        ('Midterm, Final');

INSERT INTO course(c_id,dept_id,inst_id)
VALUES(61,1,1),(165,2,2),(265,2,3),(455,3,4);

INSERT INTO course_eval(c_id,evaluation_id)
VALUES(61,1),(165,2),(265,3),(455,4);

INSERT INTO course_time(c_id,sect,start_time,end_time)
VALUES  (61,'A','08:00:00','10:00:00'),
        (61,'B','13:00:00','15:00:00'),
        (165,'A','10:00:00','11:00:00'),
        (165,'B','19:00:00','20:00:00'),
        (265,'B','13:00:00','14:00:00'),
        (455,'B','18:00:00','19:00:00');

