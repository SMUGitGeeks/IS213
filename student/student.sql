-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 17, 2023 at 02:25 PM
-- Server version: 8.0.27
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `student` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `student`;

DROP TABLE IF EXISTS `student`;
CREATE TABLE IF NOT EXISTS `student` (
  `student_id` int NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `is_subscribed` tinyint(1) NOT NULL,
  `is_graduated` tinyint(1) NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `studentmodule`;
CREATE TABLE IF NOT EXISTS `studentmodule` (
  `student_id` int NOT NULL,
  `module_id` varchar(10) NOT NULL,
  PRIMARY KEY (`student_id`,`module_id`),
  KEY `fk_StudentModule_Student_idx` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `student` (`student_id`, `student_name`, `email`, `is_subscribed`, `is_graduated`) VALUES
(12345678, 'John Smith', 'john_smith_2022@scis.smu.edu.sg', 0, 1),
(23456789, 'Sarah Lee', 'sarah_lee_2023@scis.smu.edu.sg', 0, 1),
(31238871, 'Katherine Wong', 'katherine_wong_2022@scis.smu.edu.sg', 1, 1),
(34567890, 'Michael Chen', 'michael_chen_2024@scis.smu.edu.sg', 0, 0),
(45678901, 'Emily Wang', 'emily_wang_2022@scis.smu.edu.sg', 1, 1),
(56789012, 'William Tan', 'william_tan_2023@scis.smu.edu.sg', 0, 0),
(67890123, 'Jessica Ng', 'jessica_ng_2024@scis.smu.edu.sg', 0, 1),
(78901234, 'David Lim', 'david_lim_2022@scis.smu.edu.sg', 1, 1),
(89012345, 'Samantha Koh', 'samantha_koh_2023@scis.smu.edu.sg', 0, 0),
(90123456, 'Benjamin Tan', 'benjamin_tan_2024@scis.smu.edu.sg', 0, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

INSERT INTO `studentmodule` (`student_id`, `module_id`) VALUES
(12345678, 'CS205\r'),
(12345678, 'CS441\r'),
(12345678, 'IS105\r'),
(12345678, 'IS111\r'),
(12345678, 'IS112\r'),
(12345678, 'IS113\r'),
(12345678, 'IS212\r'),
(12345678, 'IS213\r'),
(12345678, 'IS214\r'),
(12345678, 'IS417\r'),
(12345678, 'IS424\r'),
(12345678, 'IS442\r'),
(12345678, 'IS445\r'),
(12345678, 'IS453\r'),
(12345678, 'IS458\r'),
(23456789, 'CS106\r'),
(23456789, 'CS205\r'),
(23456789, 'CS426\r'),
(23456789, 'IS105\r'),
(23456789, 'IS111\r'),
(23456789, 'IS112\r'),
(23456789, 'IS113\r'),
(23456789, 'IS212\r'),
(23456789, 'IS213\r'),
(23456789, 'IS214\r'),
(23456789, 'IS417\r'),
(23456789, 'IS424\r'),
(23456789, 'IS442\r'),
(23456789, 'IS445\r'),
(23456789, 'IS453\r'),
(23456789, 'IS458\r'),
(23456789, 'IS470\r'),
(23456789, 'IS471\r'),
(23456789, 'IS472\r'),
(23456789, 'IS483\r'),
(23456789, 'IS484\r'),
(31238871, 'IS105\r'),
(31238871, 'IS111\r'),
(31238871, 'IS112\r'),
(31238871, 'IS113\r'),
(31238871, 'IS212\r'),
(31238871, 'IS213\r'),
(31238871, 'IS214\r'),
(31238871, 'IS215\r'),
(31238871, 'IS217\r'),
(31238871, 'IS424\r'),
(31238871, 'IS428\r'),
(31238871, 'IS434\r'),
(31238871, 'IS442\r'),
(31238871, 'IS444\r'),
(31238871, 'IS445\r'),
(31238871, 'IS446\r'),
(31238871, 'IS450\r'),
(31238871, 'IS453\r'),
(31238871, 'IS458\r'),
(31238871, 'IS461\r'),
(31238871, 'IS462\r'),
(31238871, 'IS470\r'),
(31238871, 'IS471\r'),
(31238871, 'IS602\r'),
(31238871, 'IS607\r'),
(31238871, 'IS613\r'),
(31238871, 'IS614\r'),
(31238871, 'IS615\r'),
(31238871, 'IS617\r'),
(31238871, 'IS620\r'),
(31238871, 'IS621\r'),
(34567890, 'CS102\r'),
(34567890, 'CS106\r'),
(34567890, 'CS440\r'),
(34567890, 'IS105\r'),
(34567890, 'IS111\r'),
(34567890, 'IS112\r'),
(34567890, 'IS113\r'),
(34567890, 'IS212\r'),
(34567890, 'IS213\r'),
(34567890, 'IS214\r'),
(34567890, 'IS417\r'),
(45678901, 'CS301\r'),
(45678901, 'CS445\r'),
(45678901, 'IS105\r'),
(45678901, 'IS212\r'),
(45678901, 'IS215\r'),
(45678901, 'IS444\r'),
(45678901, 'IS446\r'),
(56789012, 'CS421\r'),
(56789012, 'CS442\r'),
(56789012, 'CS461\r'),
(56789012, 'IS111\r'),
(56789012, 'IS113\r'),
(56789012, 'IS213\r'),
(56789012, 'IS424\r'),
(56789012, 'IS450\r'),
(56789012, 'IS461\r'),
(56789012, 'IS483\r'),
(67890123, 'CS102\r'),
(67890123, 'CS205\r'),
(67890123, 'IS105\r'),
(67890123, 'IS111\r'),
(67890123, 'IS212\r'),
(67890123, 'IS442\r'),
(67890123, 'IS450\r'),
(67890123, 'IS460\r'),
(67890123, 'IS484\r'),
(67890123, 'IS617\r'),
(78901234, 'CS102\r'),
(78901234, 'IS111\r'),
(78901234, 'IS113\r'),
(78901234, 'IS212\r'),
(78901234, 'IS458\r'),
(78901234, 'IS462\r'),
(78901234, 'IS471\r'),
(78901234, 'IS485\r'),
(89012345, 'CS106\r'),
(89012345, 'CS460\r'),
(89012345, 'IS105\r'),
(89012345, 'IS113\r'),
(89012345, 'IS213\r'),
(89012345, 'IS434\r'),
(89012345, 'IS459\r'),
(89012345, 'IS614\r'),
(90123456, 'CS470\r'),
(90123456, 'IS112\r'),
(90123456, 'IS213\r'),
(90123456, 'IS415\r'),
(90123456, 'IS462\r'),
(90123456, 'IS617');

ALTER TABLE `studentmodule`
  ADD CONSTRAINT `fk_StudentModule_Student` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`);
COMMIT;