-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 06, 2022 at 01:24 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.3.3

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET SESSION sql_mode='ONLY_FULL_GROUP_BY';
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:0x0";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'kerim@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `desc` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `availability` tinyint(1) NOT NULL,
  `edition` varchar(255) NOT NULL,
  `filepath` varchar(100),
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `info` (
  `id` int(11) NOT NULL primary key auto_increment,
  `type` varchar(255) NOT NULL,
  `sender_id` INT(10) NOT NULL,
  `receiver_id` INT(10) NOT NULL,
  `title` VARCHAR(1000) NOT NULL,
  `description` TEXT,
  `file_path` VARCHAR(10000),
  `create_at` datetime Not NULL,
  `removed_at` datetime
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `name`, `desc`, `author`, `availability`, `edition`, `count`) VALUES
(1, '101 Ways To Be A Software Engineer', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut repudiandae assumenda distinctio quas tempore, voluptatibus accusamus dolores temporibus, recusandae eligendi similique. Optio, eius? Sint vel nemo, quisquam architecto fugit odio!', 'Mr. Johnny Test', 1, '1', 3),
(2, 'JAVA For Absolute Beginners', 'Step into the basics of java programmming along with globally famed programmer', '', 1, '1', 5);

-- --------------------------------------------------------

--
-- Table structure for table `reserve`
--

CREATE TABLE `reserve` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `document` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`sender_id` INT(10) NOT NULL,
	`receiver_id` INT(10) NOT NULL,
	`title` VARCHAR(1000) NOT NULL,
	`description` TEXT,
	`filepath` VARCHAR(100),
	`create_at` datetime Not NULL DEFAULT CURRENT_TIMESTAMP,
	`removed_at` date,
	-- `feedback` int(2),
	PRIMARY KEY (`id`),
	UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `archive` (
  `id` INT(10) NOT NULL auto_increment,
  `sender_id` INT(10) NOT NULL,
  `receiver_id` INT(10) NOT NULL,
  `title` VARCHAR(1000) NOT NULL,
  `description` TEXT,
  `file_path` VARCHAR(10000),
  `create_at` datetime Not NULL,
  `removed_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reserve`
--

INSERT INTO `reserve` (`id`, `user_id`, `book_id`) VALUES
(1, 1, 1),
(2, 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--


CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `password` varchar(1000) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `mob` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `lock` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `bio`, `mob`, `lock`, `created_at`) VALUES
(1, 'Kerim', 'kerim@gmail.com', '1234kk', 'They watch you from the shelf while you sleep 👀. Are you dreaming of them, they wonder, in that wistful mood books are prone to at night when they’re bored and there’s nothing else to do but tease the cat.?', '', 0, '2022-02-14 00:00:00'),
(6, 'KK', 'kk@gmail.com', '1234kk', 'Hi :)! Long time no see ❤️', '', 0, '2022-05-13 23:07:53');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reserve`
--
ALTER TABLE `reserve`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `reserve`
--
ALTER TABLE `reserve`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
