-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 25, 2023 at 07:54 AM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `course`
--

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `Course` (
  `course_id` varchar(10) NOT NULL,
  `course_name` varchar(200) NOT NULL,
  `course_link` varchar(400) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Course`
--

INSERT INTO `Course` (`course_id`, `course_name`, `course_link`) VALUES
('0', 'Agile with Atlassian Jira', 'https://www.coursera.org/learn/agile-atlassian-jira'),
('1', 'Supervised Machine Learning: Regression and Classification', 'https://www.coursera.org/learn/machine-learning'),
('10', 'UX Design: From Concept to Prototype', 'https://www.coursera.org/learn/ux-design-concept-wireframe'),
('11', 'IBM DevOps and Software Engineering Professional Certificate', 'https://www.coursera.org/professional-certificates/devops-and-software-engineering'),
('2', 'AWS Cloud Technical Essentials', 'https://www.coursera.org/learn/aws-cloud-technical-essentials'),
('3', 'Java Programming and Software Engineering Fundamentals Specialization', 'https://www.coursera.org/specializations/java-programming'),
('4', 'Statistics with Python Specialization', 'https://www.coursera.org/specializations/statistics-with-python'),
('5', 'Introduction to Cyber Security Specialization', 'https://www.coursera.org/specializations/intro-cyber-security'),
('6', 'Introduction to Hardware and Operating Systems', 'https://www.coursera.org/learn/introduction-to-hardware-and-operating-systems'),
('7', 'Introduction to Artificial Intelligence (AI)', 'https://www.coursera.org/learn/introduction-to-ai'),
('8', 'HTML, CSS, and Javascript for Web Developers', 'https://www.coursera.org/learn/html-css-javascript-for-web-developers'),
('9', 'The Bits and Bytes of Computer Networking', 'https://www.coursera.org/learn/computer-networking');

-- --------------------------------------------------------

--
-- Table structure for table `CourseSkill`
--

CREATE TABLE `CourseSkill` (
  `course_id` varchar(10) NOT NULL,
  `skill_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `CourseSkill`
--

INSERT INTO `CourseSkill` (`course_id`, `skill_name`) VALUES
('0', 'Agile Methodologies'),
('0', 'Project Management'),
('0', 'Technical Support'),
('1', 'Data Analysis'),
('1', 'Deep Learning'),
('1', 'Machine Learning'),
('10', 'User Experience Design'),
('10', 'User Interface Design'),
('10', 'Wireframing'),
('11', 'Cloud Computing'),
('11', 'Software Testing'),
('11', 'Test Plans'),
('2', 'Cloud Infrastructure'),
('2', 'Cloud Management'),
('2', 'Cloud Security'),
('3', 'Data Structures'),
('3', 'Java'),
('3', 'Software Development'),
('4', 'Data Visualization'),
('4', 'Statistics'),
('4', 'Troubleshooting'),
('5', 'Cybersecurity'),
('5', 'Penetration Testing'),
('5', 'Vulnerability Assessments'),
('6', 'Operating Systems'),
('6', 'Service Management'),
('6', 'Troubleshooting'),
('7', 'AI Governance'),
('7', 'Artificial Intelligence'),
('7', 'Ethics in AI'),
('8', 'CSS'),
('8', 'HTML'),
('8', 'Web Development'),
('9', 'Defect Documentation'),
('9', 'Network Infrastructure'),
('9', 'Routing Protocols');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `CourseSkill`
--
ALTER TABLE `CourseSkill`
  ADD PRIMARY KEY (`course_id`,`skill_name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `CourseSkill`
--
ALTER TABLE `CourseSkill`
  ADD CONSTRAINT `courseskill_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
