SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `job` DEFAULT CHARACTER SET utf8 ;
USE `job` ;

-- -----------------------------------------------------
-- Table `job`.`Job`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job`.`Job` (
  `job_id` INT NOT NULL AUTO_INCREMENT,
  `job_role` VARCHAR(50) NOT NULL,
  `job_company` VARCHAR(50) NOT NULL,
  `job_description` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`job_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `job`.`JobSkill`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job`.`JobSkill` (
  `job_id` INT NOT NULL,
  `skill_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`job_id`, `skill_name`),
  CONSTRAINT `fk_JobSkill_Job`
    FOREIGN KEY (`job_id`)
    REFERENCES `job`.`Job` (`job_id`)
)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
