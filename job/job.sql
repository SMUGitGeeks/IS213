DROP TABLE IF EXISTS `job`;
CREATE TABLE IF NOT EXISTS `job` (
  `job_id` INT NOT NULL AUTO_INCREMENT,
  `job_role` varchar(61) NOT NULL,
  `job_company` varchar(61) NOT NULL,
  `job_description` varchar(366) NOT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE job AUTO_INCREMENT=1;

--
-- Dumping data for table `job`
--

INSERT INTO `job` (`job_role`, `job_company`, `job_description`) VALUES
('Software Developer Intern', 'ABC Pte Ltd', 'Work on various projects as a member of a software development team, collaborate with team members to create software solutions'),
('Data Analyst Intern', 'XYZ Pte Ltd', 'Assist in collecting and analyzing data, create vi' ),
('Cybersecurity Analyst Intern', 'DEF Pte Ltd', 'Participate in vulnerability assessments and penet' ),
('IT Support Intern', 'GHI Pte Ltd', 'Provide technical support to end-users, troublesho' ),
('Web Developer Intern', 'JKL Pte Ltd', 'Work on website development projects, build and ma' ),
('Network Engineer Intern', 'MNO Pte Ltd', 'Assist in the configuration and maintenance of net' ),
('Software Testing Intern', 'PQR Pte Ltd', 'Help create and execute test plans, document and r'),
('UI/UX Designer Intern', 'STU Pte Ltd', 'Work on designing user interfaces and user experie' ),
('Cloud Computing Intern', 'VWX Pte Ltd', 'Assist in the deployment and management of cloud i'),
('Artificial Intelligence Intern', 'YZA Pte Ltd', 'Participate in AI research and development project' );


DROP TABLE IF EXISTS `jobskill`;
CREATE TABLE IF NOT EXISTS `jobskill` (
  `job_id` INT NOT NULL,
  `skill_name` varchar(61) NOT NULL,
  PRIMARY KEY (`job_id`,`skill_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jobskill`
--

INSERT INTO `jobskill` (`job_id`, `skill_name`) VALUES
(1, 'Agile Methodologies'),
(1, 'Java'),
(1, 'Software Development'),
(2, 'Data Analysis'),
(2, 'Data Visualization'),
(2, 'Statistics'),
(3, 'Cybersecurity'),
(3, 'Penetration Testing'),
(3, 'Vulnerability Assessments'),
(4, 'Operating Systems'),
(4, 'Technical Support'),
(4, 'Troubleshooting'),
(5, 'CSS'),
(5, 'HTML'),
(5, 'Web Development'),
(6, 'Network Infrastructure'),
(6, 'Routing Protocols'),
(6, 'Troubleshooting'),
(7, 'Defect Documentation'),
(7, 'Software Testing'),
(7, 'Test Plans'),
(8, 'User Experience Design'),
(8, 'User Interface Design'),
(8, 'Wireframing'),
(9, 'Cloud Infrastructure'),
(9, 'Cloud Management'),
(9, 'Cloud Security'),
(10, 'Artificial Intelligence'),
(10, 'Deep Learning'),
(10, 'Machine Learning');

ALTER TABLE `jobskill`
  ADD CONSTRAINT `jobskill_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`);
COMMIT;
