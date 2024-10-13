CREATE TABLE student (
    student_id   INTEGER PRIMARY KEY,
    name         TEXT,
    surname      TEXT,
    dateOfBirth  TEXT,
    yearEnrolled INTEGER
);

CREATE TABLE course (
    course_id     INTEGER PRIMARY KEY,
    name          TEXT,
    creditPoints  INTEGER,
    yearCommenced INTEGER
);

CREATE TABLE staff (
    employee_id INTEGER PRIMARY KEY,
    name        TEXT,
    surname     TEXT,
    jobTitle    TEXT
);

CREATE TABLE program (
    program_id    INTEGER PRIMARY KEY,
    name          TEXT,
    creditPoints  INTEGER,
    yearCommenced INTEGER
);

INSERT INTO 

student (student_id, name, surname, dateOfBirth, yearEnrolled) 

VALUES

(1, 'Nguyễn', 'Văn A', '1999-03-15', 2017),

(2, 'Trần', 'Thị B', '2000-11-25', 2018),

(3, 'Lê', 'Minh C', '1998-07-10', 2016),

(4, 'Phạm', 'Quốc D', '2001-02-20', 2019),

(5, 'Đỗ', 'Thị E', '1997-05-22', 2015),

(6, 'Vũ', 'Văn F', '2000-09-12', 2018),

(7, 'Bùi', 'Thị G', '1999-04-30', 2017),

(8, 'Hoàng', 'Văn H', '1998-06-05', 2016),

(9, 'Phan', 'Thị I', '2001-12-01', 2019),

(10, 'Đinh', 'Văn J', '2000-08-14', 2018);

INSERT INTO course (course_id, name, creditPoints, yearCommenced) VALUES

(101, 'Toán học', 3, 2015),

(102, 'Vật lý', 4, 2016),

(103, 'Hóa học', 3, 2017),

(104, 'Sinh học', 4, 2018),

(105, 'Khoa học máy tính', 6, 2015),

(106, 'Kinh tế học', 3, 2016),

(107, 'Tâm lý học', 4, 2017),

(108, 'Kỹ thuật', 5, 2018),

(109, 'Lịch sử', 3, 2015),

(110, 'Ngôn ngữ Anh', 3, 2016);

INSERT INTO staff (employee_id, name, surname, jobTitle) VALUES

(101, 'Nguyễn', 'Anh', 'Giáo sư'),

(102, 'Trần', 'Bình', 'Phó Giáo sư'),

(103, 'Lê', 'Chiến', 'Giảng viên'),

(104, 'Phạm', 'Dũng', 'Giảng viên chính'),

(105, 'Đỗ', 'Hoàng', 'Giáo sư'),

(106, 'Vũ', 'Kiên', 'Giảng viên'),

(107, 'Bùi', 'Lan', 'Trợ lý Giáo sư'),

(108, 'Hoàng', 'Mạnh', 'Giáo sư'),

(109, 'Phan', 'Ngọc', 'Giảng viên chính'),

(110, 'Đinh', 'Phong', 'Phó Giáo sư');

INSERT INTO program (program_id, name, creditPoints, yearCommenced) VALUES

(201, 'Chương trình Toán học', 120, 2015),

( 202, 'Chương trình Vật lý', 130, 2016),

( 203, 'Chương trình Hóa học', 125, 2017),

( 204, 'Chương trình Sinh học', 135, 2018),

(205, 'Chương trình Khoa học máy tính', 150, 2015),

( 206, 'Chương trình Kinh tế học', 120, 2016),

( 207, 'Chương trình Tâm lý học', 130, 2017),

( 208, 'Chương trình Kỹ thuật', 140, 2018),

( 209, 'Chương trình Lịch sử', 125, 2015),

( 210, 'Chương trình Ngôn ngữ Anh', 120, 2016);

--5-Hiển thị tất cả sinh viên có tên bắt đầu bằng chữ „H”.​
SELECT *
FROM student
WHERE name LIKE 'H%';

--6-Hiển thị tất cả sinh viên hiện đang học năm thứ 4.​
INSERT INTO student (student_id, name, surname, dateOfBirth, yearEnrolled) VALUES (11, 'Ngô', 'Văn K', '2003-09-15', 2020);

SELECT *
FROM student
WHERE strftime('%Y','now') - yearEnrolled = 4;

--7-Hiển thị tất cả các khóa học từ bảng course bắt đầu với những khóa học có số điểm tín chỉ cao nhất.​
SELECT *
FROM course
ORDER BY creditPoints DESC;

--8-Đổi tên sinh viên có student_id thấp nhất thành Adam.​
UPDATE student
SET surname = 'Adam'
WHERE student_id = (SELECT MIN(student_id) FROM student);

--9-Đổi tất cả giá trị trong cột name của bảng course thành chữ hoa.​
UPDATE course
SET name = upper(name);

--10-Xóa sinh viên lớn tuổi nhất trong bảng student.​
DELETE FROM student
WHERE strftime('%Y','now') - strftime('%Y',dateOfBirth) = (SELECT MAX(strftime('%Y','now') - strftime('%Y',dateOfBirth)) FROM student);

--11-Loại bỏ cột yearCommenced khỏi bảng course.​
ALTER TABLE course
DROP COLUMN yearCommenced;

--12-Đổi tên bảng staff thành employee.
ALTER TABLE staff
RENAME TO employee;