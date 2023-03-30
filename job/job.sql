DROP TABLE IF EXISTS `job`;
CREATE TABLE IF NOT EXISTS `job` (
  `job_id` varchar(10) NOT NULL,
  `job_role` varchar(50) NOT NULL,
  `job_company` varchar(50) NOT NULL,
  `job_description` varchar(255) NOT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `job`
--

INSERT INTO `job` (`job_id`, `job_role`, `job_company`, `job_description`) VALUES
('0', 'Software Developer Intern', 'ABC Pte Ltd', 'Work on various projects as a member of a software development team, collaborate with team members to create software solutions'),
('1', 'Data Analyst Intern', 'Assist in collecting and analyzing data, create vi', 'XYZ Pte Ltd'),
('2', 'Cybersecurity Analyst Intern', 'Participate in vulnerability assessments and penet', 'DEF Pte Ltd'),
('3', 'IT Support Intern', 'Provide technical support to end-users, troublesho', 'GHI Pte Ltd'),
('4', 'Web Developer Intern', 'Work on website development projects, build and ma', 'JKL Pte Ltd'),
('5', 'Network Engineer Intern', 'Assist in the configuration and maintenance of net', 'MNO Pte Ltd'),
('6', 'Software Testing Intern', 'Help create and execute test plans, document and r', 'PQR Pte Ltd'),
('7', 'UI/UX Designer Intern', 'Work on designing user interfaces and user experie', 'STU Pte Ltd'),
('8', 'Cloud Computing Intern', 'Assist in the deployment and management of cloud i', 'VWX Pte Ltd'),
('9', 'Artificial Intelligence Intern', 'Participate in AI research and development project', 'YZA Pte Ltd');


DROP TABLE IF EXISTS `jobskill`;
CREATE TABLE IF NOT EXISTS `jobskill` (
  `job_id` varchar(10) NOT NULL,
  `skill_name` varchar(50) NOT NULL,
  PRIMARY KEY (`job_id`,`skill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `jobskill`
--

INSERT INTO `jobskill` (`job_id`, `skill_name`) VALUES
('1', 'Data Analysis'),
('1', 'Data Visualization'),
('1', 'Statistics'),
('2', 'Cybersecurity'),
('2', 'Penetration Testing'),
('2', 'Vulnerability Assessments'),
('3', 'Operating Systems'),
('3', 'Technical Support'),
('3', 'Troubleshooting'),
('4', 'CSS'),
('4', 'HTML'),
('4', 'Web Development'),
('5', 'Network Infrastructure'),
('5', 'Routing Protocols'),
('5', 'Troubleshooting'),
('6', 'Defect Documentation'),
('6', 'Software Testing'),
('6', 'Test Plans'),
('7', 'User Experience Design'),
('7', 'User Interface Design'),
('7', 'Wireframing'),
('8', 'Cloud Infrastructure'),
('8', 'Cloud Management'),
('8', 'Cloud Security'),
('9', 'Artificial Intelligence'),
('9', 'Deep Learning'),
('9', 'Machine Learning');

ALTER TABLE `jobskill`
  ADD CONSTRAINT `jobskill_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`);
COMMIT;
