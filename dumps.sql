-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: login
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS auth_group;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES auth_group WRITE;
/*!40000 ALTER TABLE auth_group DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS auth_group_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_group_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  group_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id,permission_id),
  KEY auth_group_permissio_permission_id_84c5c92e_fk_auth_perm (permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES auth_group_permissions WRITE;
/*!40000 ALTER TABLE auth_group_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_group_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS auth_permission;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_permission (
  id int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  content_type_id int NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id,codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES auth_permission WRITE;
/*!40000 ALTER TABLE auth_permission DISABLE KEYS */;
INSERT INTO auth_permission VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add login user',7,'add_loginuser'),(26,'Can change login user',7,'change_loginuser'),(27,'Can delete login user',7,'delete_loginuser'),(28,'Can view login user',7,'view_loginuser'),(29,'Can add signup',8,'add_signup'),(30,'Can change signup',8,'change_signup'),(31,'Can delete signup',8,'delete_signup'),(32,'Can view signup',8,'view_signup'),(33,'Can add item',9,'add_item'),(34,'Can change item',9,'change_item'),(35,'Can delete item',9,'delete_item'),(36,'Can view item',9,'view_item');
/*!40000 ALTER TABLE auth_permission ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS auth_user;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user (
  id int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  username varchar(150) NOT NULL,
  first_name varchar(150) NOT NULL,
  last_name varchar(150) NOT NULL,
  email varchar(254) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES auth_user WRITE;
/*!40000 ALTER TABLE auth_user DISABLE KEYS */;
/*!40000 ALTER TABLE auth_user ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS auth_user_groups;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user_groups (
  id bigint NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL,
  group_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_user_groups_user_id_group_id_94350c0c_uniq (user_id,group_id),
  KEY auth_user_groups_group_id_97559544_fk_auth_group_id (group_id),
  CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group (id),
  CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES auth_user_groups WRITE;
/*!40000 ALTER TABLE auth_user_groups DISABLE KEYS */;
/*!40000 ALTER TABLE auth_user_groups ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS auth_user_user_permissions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE auth_user_user_permissions (
  id bigint NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL,
  permission_id int NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY auth_user_user_permissions_user_id_permission_id_14a6b632_uniq (user_id,permission_id),
  KEY auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm (permission_id),
  CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission (id),
  CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES auth_user_user_permissions WRITE;
/*!40000 ALTER TABLE auth_user_user_permissions DISABLE KEYS */;
/*!40000 ALTER TABLE auth_user_user_permissions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS django_admin_log;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_admin_log (
  id int NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext,
  object_repr varchar(200) NOT NULL,
  action_flag smallint unsigned NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int DEFAULT NULL,
  user_id int NOT NULL,
  PRIMARY KEY (id),
  KEY django_admin_log_content_type_id_c4bce8eb_fk_django_co (content_type_id),
  KEY django_admin_log_user_id_c564eba6_fk_auth_user_id (user_id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user (id),
  CONSTRAINT django_admin_log_chk_1 CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES django_admin_log WRITE;
/*!40000 ALTER TABLE django_admin_log DISABLE KEYS */;
/*!40000 ALTER TABLE django_admin_log ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS django_content_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_content_type (
  id int NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY django_content_type_app_label_model_76bd3d3b_uniq (app_label,model)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES django_content_type WRITE;
/*!40000 ALTER TABLE django_content_type DISABLE KEYS */;
INSERT INTO django_content_type VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'members','item'),(7,'members','loginuser'),(8,'members','signup'),(6,'sessions','session');
/*!40000 ALTER TABLE django_content_type ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS django_migrations;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_migrations (
  id bigint NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES django_migrations WRITE;
/*!40000 ALTER TABLE django_migrations DISABLE KEYS */;
INSERT INTO django_migrations VALUES (1,'contenttypes','0001_initial','2024-11-25 16:20:29.349667'),(2,'auth','0001_initial','2024-11-25 16:20:29.822140'),(3,'admin','0001_initial','2024-11-25 16:20:29.995862'),(4,'admin','0002_logentry_remove_auto_add','2024-11-25 16:20:30.007863'),(5,'admin','0003_logentry_add_action_flag_choices','2024-11-25 16:20:30.018868'),(6,'contenttypes','0002_remove_content_type_name','2024-11-25 16:20:30.144977'),(7,'auth','0002_alter_permission_name_max_length','2024-11-25 16:20:30.196028'),(8,'auth','0003_alter_user_email_max_length','2024-11-25 16:20:30.229548'),(9,'auth','0004_alter_user_username_opts','2024-11-25 16:20:30.235580'),(10,'auth','0005_alter_user_last_login_null','2024-11-25 16:20:30.298285'),(11,'auth','0006_require_contenttypes_0002','2024-11-25 16:20:30.301289'),(12,'auth','0007_alter_validators_add_error_messages','2024-11-25 16:20:30.310298'),(13,'auth','0008_alter_user_username_max_length','2024-11-25 16:20:30.398108'),(14,'auth','0009_alter_user_last_name_max_length','2024-11-25 16:20:30.471993'),(15,'auth','0010_alter_group_name_max_length','2024-11-25 16:20:30.492512'),(16,'auth','0011_update_proxy_permissions','2024-11-25 16:20:30.501522'),(17,'auth','0012_alter_user_first_name_max_length','2024-11-25 16:20:30.575581'),(18,'sessions','0001_initial','2024-11-25 16:20:30.613118'),(19,'members','0001_initial','2024-11-25 16:36:17.634056'),(20,'members','0002_alter_signup_email_alter_signup_password_and_more','2024-11-25 16:58:26.692587'),(21,'members','0003_alter_signup_email_alter_signup_username','2024-11-28 15:46:48.716434'),(22,'members','0004_delete_loginuser','2024-11-28 16:11:08.606860'),(23,'members','0002_signup_designation','2025-01-28 09:21:31.991944'),(24,'members','0003_item','2025-02-08 10:35:01.565415'),(25,'members','0004_auto_20250304_1048','2025-03-10 17:46:49.608870');
/*!40000 ALTER TABLE django_migrations ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS django_session;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  KEY django_session_expire_date_a5c62663 (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES django_session WRITE;
/*!40000 ALTER TABLE django_session DISABLE KEYS */;
/*!40000 ALTER TABLE django_session ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members_additem`
--

DROP TABLE IF EXISTS members_additem;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE members_additem (
  id int NOT NULL AUTO_INCREMENT,
  item_id int NOT NULL,
  date_of_production date NOT NULL,
  total_items_produced int unsigned NOT NULL,
  total_production_cost decimal(12,2) NOT NULL,
  PRIMARY KEY (id),
  KEY item_id (item_id),
  CONSTRAINT members_additem_ibfk_1 FOREIGN KEY (item_id) REFERENCES members_item (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_additem`
--

LOCK TABLES members_additem WRITE;
/*!40000 ALTER TABLE members_additem DISABLE KEYS */;
INSERT INTO members_additem VALUES (1,4,'2025-03-10',100,10000.00),(2,2,'2025-03-10',10,10000.00),(3,5,'2025-03-10',10,2000.00),(4,5,'2025-03-10',12,100.00),(5,5,'2025-03-10',13,100.00),(6,5,'2025-03-10',1,100.00),(7,6,'2025-03-10',100,10000.00),(8,6,'2025-03-10',1,100.00),(9,7,'2025-03-11',150,1800.00),(10,7,'2025-03-11',1,200.00);
/*!40000 ALTER TABLE members_additem ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members_item`
--

DROP TABLE IF EXISTS members_item;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE members_item (
  ItemName varchar(255) NOT NULL,
  NumberOfItems int NOT NULL,
  SellingPrice decimal(10,2) NOT NULL,
  id int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id),
  UNIQUE KEY ItemName (ItemName)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_item`
--

LOCK TABLES members_item WRITE;
/*!40000 ALTER TABLE members_item DISABLE KEYS */;
INSERT INTO members_item VALUES ('breakes',190,2000.00,1),('sensor',1,1000.00,2),('Motors',2000,1000.00,3),('Wires',90,10.00,4),('chip',14,1000.00,5),('breakepad',101,1000.00,6),('Bolts',101,20.00,7);
/*!40000 ALTER TABLE members_item ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members_sellitem`
--

DROP TABLE IF EXISTS members_sellitem;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE members_sellitem (
  id int NOT NULL AUTO_INCREMENT,
  item_id int NOT NULL,
  date_of_sales date NOT NULL,
  total_items_sold int unsigned NOT NULL,
  total_sales_price decimal(12,2) NOT NULL,
  PRIMARY KEY (id),
  KEY item_id (item_id),
  CONSTRAINT members_sellitem_ibfk_1 FOREIGN KEY (item_id) REFERENCES members_item (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_sellitem`
--

LOCK TABLES members_sellitem WRITE;
/*!40000 ALTER TABLE members_sellitem DISABLE KEYS */;
INSERT INTO members_sellitem VALUES (1,4,'2025-03-10',10,100.00),(2,2,'2025-03-10',10,10000.00),(3,7,'2025-03-11',50,1000.00);
/*!40000 ALTER TABLE members_sellitem ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members_signup`
--

DROP TABLE IF EXISTS members_signup;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE members_signup (
  id bigint NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  designation varchar(50) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY members_signup_email_4d584715_uniq (email),
  UNIQUE KEY members_signup_username_1e9d684a_uniq (username)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members_signup`
--

LOCK TABLES members_signup WRITE;
/*!40000 ALTER TABLE members_signup DISABLE KEYS */;
INSERT INTO members_signup VALUES (1,'testuser','test@example.com','testpassword','Manager'),(2,'user','user@gmail.com','123','Manager'),(3,'sampleuser','sampleuser@gmail.com','123','Manager'),(4,'cricket','cricket@123','cricket','Staff'),(5,'harish','harish@psg','123','Staff'),(6,'gokul','gokul@psg','221','staff'),(7,'hariharan','hariharan@saibabacolony','1234','manager'),(8,'pranav','pranav@psg','123','manager');
/*!40000 ALTER TABLE members_signup ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-11 14:13:00
