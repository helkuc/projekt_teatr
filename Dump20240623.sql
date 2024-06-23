-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: teatr
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `listaklientow`
--

DROP TABLE IF EXISTS `listaklientow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listaklientow` (
  `idKlienta` int NOT NULL AUTO_INCREMENT,
  `imie` varchar(100) DEFAULT NULL,
  `nazwisko` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`idKlienta`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listaklientow`
--

LOCK TABLES `listaklientow` WRITE;
/*!40000 ALTER TABLE `listaklientow` DISABLE KEYS */;
/*!40000 ALTER TABLE `listaklientow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listamiejsc`
--

DROP TABLE IF EXISTS `listamiejsc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `listamiejsc` (
  `numer` int NOT NULL AUTO_INCREMENT,
  `dostepne` tinyint(1) DEFAULT NULL,
  `cena` float NOT NULL,
  `dodatkowaOplata` float DEFAULT NULL,
  `udogodnienia` varchar(250) DEFAULT NULL,
  `typ` varchar(100) NOT NULL,
  PRIMARY KEY (`numer`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listamiejsc`
--

LOCK TABLES `listamiejsc` WRITE;
/*!40000 ALTER TABLE `listamiejsc` DISABLE KEYS */;
INSERT INTO `listamiejsc` VALUES (1,1,30,NULL,'Szerokie podejście,brak schodów','NP'),(2,1,30,NULL,'Szerokie podejście,brak schodów','NP'),(3,1,30,NULL,'Brak schodów','NP'),(4,1,30,NULL,NULL,'zwykłe'),(5,1,30,NULL,NULL,'zwykłe'),(6,1,30,NULL,NULL,'zwykłe'),(7,1,30,NULL,NULL,'zwykłe'),(8,1,30,NULL,NULL,'zwykłe'),(9,1,30,NULL,NULL,'zwykłe'),(10,1,30,NULL,NULL,'zwykłe'),(11,1,30,10,NULL,'VIP'),(12,1,30,10,NULL,'VIP'),(13,1,30,10,NULL,'VIP'),(14,1,30,10,NULL,'VIP'),(15,1,30,10,NULL,'VIP'),(16,1,30,10,NULL,'VIP'),(17,1,30,15,NULL,'VIP'),(18,1,30,15,NULL,'VIP'),(19,1,30,15,NULL,'VIP'),(20,1,30,15,NULL,'VIP'),(21,1,30,15,NULL,'VIP');
/*!40000 ALTER TABLE `listamiejsc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rezerwacje`
--

DROP TABLE IF EXISTS `rezerwacje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rezerwacje` (
  `idRezerwacji` int NOT NULL AUTO_INCREMENT,
  `dataRezerwacji` datetime DEFAULT NULL,
  `dataAktualizacji` datetime DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `idKlienta` int DEFAULT NULL,
  `numerMiejsca` int DEFAULT NULL,
  `typ` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idRezerwacji`)
) ENGINE=InnoDB AUTO_INCREMENT=174 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rezerwacje`
--

LOCK TABLES `rezerwacje` WRITE;
/*!40000 ALTER TABLE `rezerwacje` DISABLE KEYS */;
/*!40000 ALTER TABLE `rezerwacje` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-23 23:33:04
