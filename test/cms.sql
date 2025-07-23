-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: cms
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `film`
--

DROP TABLE IF EXISTS `film`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `film` (
  `id` int NOT NULL AUTO_INCREMENT,
  `film_name` varchar(50) DEFAULT NULL,
  `film_pic` varchar(100) DEFAULT NULL,
  `actor` varchar(100) DEFAULT NULL,
  `director` varchar(100) DEFAULT NULL,
  `nation` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `language` varchar(100) DEFAULT NULL,
  `summary` text,
  `release_time` varchar(255) DEFAULT NULL,
  `del_flag` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `film`
--

LOCK TABLES `film` WRITE;
/*!40000 ALTER TABLE `film` DISABLE KEYS */;
INSERT INTO `film` VALUES (1,'金刚狼','1659351101988.png','休 杰克曼','詹姆斯 曼高德','美国','1','3','<p style=\"user-select: text;\"><img src=\"http://localhost:9000/cms/public/film/1659351110957.png\" style=\"max-width:100%;\"><br style=\"user-select: text;\"></p>','2017-02-17',0),(2,'test','1658719977070.png','test','test','test','2','1','<p>test</p><p></p>','test',1);
/*!40000 ALTER TABLE `film` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dict`
--

DROP TABLE IF EXISTS `sys_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_code` varchar(20) DEFAULT NULL COMMENT '类型',
  `value` varchar(20) DEFAULT NULL COMMENT '字典名',
  `label` varchar(20) DEFAULT NULL COMMENT '字典值',
  `description` varchar(25) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `create_by` int DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `update_by` int DEFAULT NULL,
  `del_flag` char(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict`
--

LOCK TABLES `sys_dict` WRITE;
/*!40000 ALTER TABLE `sys_dict` DISABLE KEYS */;
INSERT INTO `sys_dict` VALUES (1,'gender','1','男','性别',NULL,NULL,NULL,NULL,'0'),(2,'gender','2','女','性别',NULL,NULL,NULL,NULL,'0'),(3,'orderStatus','1','未付款','订单状态',NULL,NULL,NULL,NULL,'0'),(4,'orderStatus','2','待付款','订单状态',NULL,NULL,NULL,NULL,'0'),(5,'orderStatus','3','已付款','订单状态',NULL,NULL,NULL,NULL,'0'),(6,'orderStatus','4','已收货','订单状态',NULL,NULL,NULL,NULL,'0'),(7,'filmtype','1','动作','类型',NULL,NULL,NULL,NULL,'0'),(8,'filmtype','2','剧情','类型',NULL,NULL,NULL,NULL,'0'),(9,'filmtype','3','情感','类型',NULL,NULL,NULL,NULL,'0'),(10,'filmtype','4','记录','类型',NULL,NULL,NULL,NULL,'0'),(11,'language','1','汉语普通话','语言',NULL,NULL,NULL,NULL,'0'),(12,'language','2','汉语粤语','语言',NULL,NULL,NULL,NULL,'0'),(13,'language','3','英语','语言',NULL,NULL,NULL,NULL,'0'),(14,'language','4','法语','语言',NULL,NULL,NULL,NULL,'0'),(15,'userStatus','1','正常','用户状态',NULL,NULL,NULL,NULL,'0'),(16,'userStatus','2','冻结','用户状态',NULL,NULL,NULL,NULL,'0');
/*!40000 ALTER TABLE `sys_dict` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_menu`
--

DROP TABLE IF EXISTS `sys_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pid` bigint DEFAULT NULL COMMENT '父菜单ID，一级菜单为0',
  `name` varchar(50) DEFAULT NULL COMMENT '菜单名称',
  `url` varchar(200) DEFAULT NULL COMMENT '菜单URL',
  `perms` varchar(500) DEFAULT NULL COMMENT '授权(多个用逗号分隔，如：user:list,user:create)',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `create_by` int DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_by` int DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `del_flag` char(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 COMMENT='菜单管理';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

LOCK TABLES `sys_menu` WRITE;
/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES (1,0,'系统管理',NULL,NULL,'&#xe609;',NULL,NULL,NULL,NULL,'0'),(2,1,'控制台','/a/console',NULL,NULL,NULL,NULL,NULL,NULL,'0'),(3,1,'用户管理','/a/user/list',NULL,NULL,NULL,NULL,NULL,NULL,'0'),(4,1,'菜单管理','/a/menu/list',NULL,NULL,NULL,NULL,NULL,NULL,'0'),(5,1,'角色管理','/a/role/list',NULL,NULL,NULL,NULL,NULL,NULL,'0'),(6,0,'影片管理',NULL,NULL,'&#xe857;',NULL,NULL,NULL,NULL,'0'),(7,6,'图集','/a/album/list',NULL,NULL,NULL,NULL,NULL,NULL,'1'),(14,6,'影片列表','/a/film/list',NULL,NULL,NULL,NULL,NULL,NULL,'0'),(15,6,'图集','/a/album/list',NULL,NULL,NULL,NULL,NULL,NULL,'1'),(16,6,'图集','/a/film/album',NULL,NULL,NULL,NULL,NULL,NULL,'1');
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '角色名称',
  `remark` varchar(255) DEFAULT NULL,
  `create_by` int DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_by` int DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `del_flag` char(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

LOCK TABLES `sys_role` WRITE;
/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES (1,'超级管理员','admin',NULL,NULL,NULL,NULL,'0'),(2,'分店管理员',NULL,NULL,NULL,NULL,NULL,'0'),(8,'系统看客',NULL,NULL,NULL,NULL,NULL,'1'),(9,'系统游客',NULL,NULL,NULL,NULL,NULL,'1');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role_menu`
--

DROP TABLE IF EXISTS `sys_role_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sys_role_id` bigint DEFAULT NULL COMMENT '角色ID',
  `sys_menu_id` bigint DEFAULT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb3 COMMENT='角色与菜单对应关系';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_menu`
--

LOCK TABLES `sys_role_menu` WRITE;
/*!40000 ALTER TABLE `sys_role_menu` DISABLE KEYS */;
INSERT INTO `sys_role_menu` VALUES (108,2,7),(109,2,6),(110,2,14),(111,2,6),(115,3,2),(116,3,1),(118,4,2),(119,4,1),(151,5,2),(152,5,1),(154,6,2),(155,6,1),(157,7,2),(158,7,1),(160,8,2),(161,8,1),(162,1,2),(163,1,1),(164,1,3),(165,1,1),(166,1,4),(167,1,1),(168,1,5),(169,1,1),(170,1,14),(171,1,6),(172,1,16),(173,1,6),(177,9,2),(178,9,1);
/*!40000 ALTER TABLE `sys_role_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(25) DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  `create_by` int DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_by` int DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `del_flag` char(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'admin',NULL,'$2a$10$7YeyQKrlX/lTktWAOKmqD.3t6.iPMuEKBZ2TOnFe4ei9AESHkWG12','1104975916@qq.com','15250420158',1,NULL,NULL,NULL,NULL,'0'),(2,'tony','tony','$2a$10$Obxwu29fB.FXvlNB9tXMHOQZzwZh4MkqsMbGktwJzYCNCZYIMD1ra','1918082411@qq.com','15250420158',1,NULL,NULL,NULL,NULL,'0'),(5,'test','testUser','$2a$10$gS8g8kcxDBx9kRkrx2j4f.wSDPoY.LynmQnlHIa04k0x0A65/dmXa','abc@example.com','10086',1,NULL,NULL,NULL,NULL,'0');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_role`
--

DROP TABLE IF EXISTS `sys_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sys_user_id` int DEFAULT NULL COMMENT '用户ID',
  `sys_role_id` int DEFAULT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 COMMENT='用户与角色对应关系';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_role`
--

LOCK TABLES `sys_user_role` WRITE;
/*!40000 ALTER TABLE `sys_user_role` DISABLE KEYS */;
INSERT INTO `sys_user_role` VALUES (1,1,1),(11,2,2),(12,6,NULL),(13,6,2),(17,3,1),(21,4,1),(22,5,NULL),(23,5,2);
/*!40000 ALTER TABLE `sys_user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-03 11:05:53
