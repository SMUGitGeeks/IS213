SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Job`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Job` (
  `job_id` INT NOT NULL AUTO_INCREMENT,
  `job_role` VARCHAR(50) NOT NULL,
  `job_company` VARCHAR(50) NOT NULL,
  `job_description` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`job_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`JobSkill`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`JobSkill` (
  `job_id` INT NOT NULL,
  `skill_name` VARCHAR(50) NOT NULL,
  `Job_job_id` INT NOT NULL,
  PRIMARY KEY (`job_id`, `Job_job_id`),
  INDEX `fk_JobSkill_Job_idx` (`Job_job_id` ASC) VISIBLE,
  CONSTRAINT `fk_JobSkill_Job`
    FOREIGN KEY (`Job_job_id`)
    REFERENCES `mydb`.`Job` (`job_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
