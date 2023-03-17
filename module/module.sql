SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Module`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Module` (
  `module_id` VARCHAR(10) NOT NULL,
  `module_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`module_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ModuleSkill`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ModuleSkill` (
  `module_id` VARCHAR(10) NOT NULL,
  `skill_name` VARCHAR(50) NOT NULL,
  `Module_module_id` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`module_id`, `skill_name`, `Module_module_id`),
  INDEX `fk_ModuleSkill_Module_idx` (`Module_module_id` ASC) VISIBLE,
  CONSTRAINT `fk_ModuleSkill_Module`
    FOREIGN KEY (`Module_module_id`)
    REFERENCES `mydb`.`Module` (`module_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
