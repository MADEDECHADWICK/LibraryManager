--Kenyan Library Management System Database Schema
--Contains all SQL statements to create and populate the database
--Includes: Tables, Constraints, Relationships, and Sample Data

--Database Creation
CREATE DATABASE kenyan_library_management;
USE kenyan_library_management;

--Members table with Kenyan-specific fields
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    id_number VARCHAR(20) UNIQUE COMMENT 'Kenyan National ID',
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL COMMENT 'Format: 2547XXXXXXXX',
    county VARCHAR(50) NOT NULL COMMENT 'Kenyan county of residence',
    town VARCHAR(50) NOT NULL,
    postal_address VARCHAR(100),
    membership_date DATE NOT NULL,
    membership_type ENUM('student', 'adult', 'senior', 'institutional') NOT NULL,
    membership_status ENUM('active', 'expired', 'suspended') DEFAULT 'active',
    CONSTRAINT chk_email CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_phone CHECK (phone REGEXP '^254[17][0-9]{8}$')
) COMMENT 'Library members with Kenyan context';

--publishers table
CREATE TABLE publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    county VARCHAR(50) NOT NULL,
    town VARCHAR(50) NOT NULL,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20) NOT NULL,
    registration_number VARCHAR(20) COMMENT 'KPA registration',
    CONSTRAINT chk_pub_phone CHECK (contact_phone REGEXP '^254[17][0-9]{8}$')
) COMMENT 'Kenyan publishers information';

--authors table
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    nationality VARCHAR(50) DEFAULT 'Kenyan',
    county_of_origin VARCHAR(50)
) COMMENT 'Authors with Kenyan focus';

--Books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publication_year INT,
    publisher_id INT,
    language ENUM('English', 'Kiswahili', 'Local', 'Other') DEFAULT 'English',
    category ENUM('Fiction', 'Non-Fiction', 'Academic', 'Children', 'Kenyan Literature', 'African Studies'),
    kicd_approved BOOLEAN DEFAULT FALSE COMMENT 'KICD approval status',
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE SET NULL,
    CONSTRAINT chk_copies CHECK (available_copies <= total_copies AND available_copies >= 0)
) COMMENT 'Books with Kenyan context';

--Book-Authors relationship table
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
) COMMENT 'Book-author relationships';

--Book loans table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('active', 'returned', 'overdue', 'lost') DEFAULT 'active',
    loan_officer VARCHAR(100),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    CONSTRAINT chk_dates CHECK (due_date >= loan_date AND (return_date IS NULL OR return_date >= loan_date))
) COMMENT 'Book loans tracking';

--Fines table 
CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL COMMENT 'Amount in KES',
    issue_date DATE NOT NULL,
    payment_date DATE,
    payment_method ENUM('MPesa', 'Cash', 'Bank Transfer', 'Cheque'),
    status ENUM('pending', 'paid', 'waived') DEFAULT 'pending',
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE CASCADE,
    CONSTRAINT chk_amount CHECK (amount >= 0)
) COMMENT 'Fines in Kenyan Shillings';

--Sample Data 
--Publishers
INSERT INTO publishers (name, address, county, town, contact_phone, registration_number) VALUES
('Longhorn Publishers', 'P.O Box 18033-00500, Nairobi', 'Nairobi', 'Nairobi', '254722123456', 'KP12345'),
('EAEP', 'P.O Box 45314-00100, Nairobi', 'Nairobi', 'Nairobi', '254733987654', 'KP67890'),
('Storymoja', 'P.O Box 2519-00606, Nairobi', 'Nairobi', 'Nairobi', '254711112233', 'KP11223'),
('Mvule Africa', 'P.O Box 1234-40100, Kisumu', 'Kisumu', 'Kisumu', '254700445566', 'KP44556');

--Authors
INSERT INTO authors (name, bio, county_of_origin) VALUES
('Ngũgĩ wa Thiong''o', 'Renowned Kenyan writer and academic', 'Kiambu'),
('Grace Ogot', 'Pioneering Kenyan author and politician', 'Kisumu'),
('Binyavanga Wainaina', 'Founder of Kwani Trust', 'Nakuru'),
('Yvonne Adhiambo Owuor', 'Author of "Dust"', 'Nairobi'),
('Mwenda Mbatiah', 'Popular Swahili literature author', 'Meru');

--Books
INSERT INTO books (title, isbn, publication_year, publisher_id, language, category, kicd_approved, total_copies, available_copies) VALUES
('Weep Not, Child', '9780143106692', 1964, 1, 'English', 'Kenyan Literature', TRUE, 10, 8),
('The River and the Source', '9789966464754', 1994, 2, 'English', 'Kenyan Literature', TRUE, 8, 5),
('Dust', '9781472110385', 2013, 3, 'English', 'Fiction', FALSE, 5, 5),
('Kiu', '9789966466789', 1990, 4, 'Kiswahili', 'Fiction', TRUE, 7, 3);

--Book-author relationships
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1), (2, 2), (3, 4), (4, 5);

--Kenyan library members
INSERT INTO members (first_name, last_name, id_number, email, phone, county, town, membership_date, membership_type) VALUES
('Wanjiku', 'Kamau', '12345678', 'wanjiku@example.com', '254712345678', 'Nairobi', 'Nairobi', '2023-01-15', 'adult'),
('John', 'Mwangi', '23456789', 'john@example.com', '254723456789', 'Kiambu', 'Thika', '2023-03-10', 'student'),
('Amina', 'Mohamed', '34567890', 'amina@example.com', '254734567890', 'Mombasa', 'Mombasa', '2023-02-05', 'adult');

--Sample loans
INSERT INTO loans (book_id, member_id, loan_date, due_date, loan_officer) VALUES
(1, 1, '2023-05-01', '2023-05-15', 'James Kariuki'),
(2, 2, '2023-05-10', '2023-05-24', 'Mary Wambui'),
(4, 3, '2023-04-15', '2023-04-29', 'Peter Maina');

--Sample fines
INSERT INTO fines (loan_id, amount, issue_date, payment_method, status) VALUES
(3, 200.00, '2023-04-30', 'MPesa', 'paid');