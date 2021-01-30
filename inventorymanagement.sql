-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 30, 2021 at 04:08 PM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventorymanagement`
--

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `location_id` varchar(255) NOT NULL,
  `location_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `location_name`) VALUES
('Agra', 'Agra'),
('Bengaluru', 'Bengaluru'),
('Location X', 'Location X'),
('Location Y', 'Location Y');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_description` text NOT NULL,
  `create_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `product_description`, `create_date`) VALUES
('Product 1', 'Product 1', '', '2021-01-29 17:13:57'),
('Product 2', 'Product 2', '', '2021-01-29 17:14:12'),
('Product A', 'Product A', '', '2021-01-30 10:44:06'),
('Product B', 'Product B', '', '2021-01-30 10:44:18');

-- --------------------------------------------------------

--
-- Table structure for table `productmovement`
--

CREATE TABLE `productmovement` (
  `movement_id` int(11) NOT NULL,
  `product_id` varchar(255) NOT NULL,
  `from_location` varchar(255) NOT NULL,
  `to_location` varchar(255) NOT NULL,
  `qty` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `productmovement`
--

INSERT INTO `productmovement` (`movement_id`, `product_id`, `from_location`, `to_location`, `qty`, `timestamp`) VALUES
(25, 'Product A', 'Location X', '', 23, '2021-01-30 13:48:22'),
(26, 'Product 1', 'Agra', 'Bengaluru', 25, '2021-01-30 13:48:39'),
(27, 'Product 2', 'Bengaluru', 'Location X', 25, '2021-01-30 13:48:50'),
(30, 'Product 2', 'Bengaluru', 'Location X', 5, '2021-01-30 13:57:43'),
(31, 'Product 1', 'Location X', 'Location Y', 5, '2021-01-30 13:58:06'),
(32, 'Product A', 'Location Y', 'Agra', 5, '2021-01-30 13:58:20'),
(33, 'Product B', 'Agra', 'Bengaluru', 5, '2021-01-30 13:58:57'),
(34, 'Product B', '', 'Agra', 5, '2021-01-30 13:59:25'),
(35, 'Product A', '', 'Bengaluru', 5, '2021-01-30 13:59:36'),
(36, 'Product A', '', 'Location X', 5, '2021-01-30 13:59:50'),
(37, 'Product B', 'Location X', 'Location Y', 25, '2021-01-30 14:00:13'),
(38, 'Product 1', 'Bengaluru', 'Location Y', 5, '2021-01-30 14:00:30'),
(39, 'Product B', 'Agra', 'Location Y', 5, '2021-01-30 14:03:11'),
(40, 'Product 1', '', 'Bengaluru', 5, '2021-01-30 14:03:29'),
(41, 'Product 2', 'Agra', '', 5, '2021-01-30 14:03:41'),
(42, 'Product 1', 'Bengaluru', 'Location X', 5, '2021-01-30 14:04:02'),
(43, 'Product B', 'Location Y', 'Location X', 5, '2021-01-30 14:04:42'),
(44, 'Product A', 'Location X', 'Bengaluru', 5, '2021-01-30 14:04:57'),
(45, 'Product A', 'Agra', 'Location X', 5, '2021-01-30 14:05:15'),
(46, 'Product B', 'Agra', '', 15, '2021-01-30 14:26:34'),
(47, 'Product A', '', 'Location X', 20, '2021-01-30 14:41:58');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `productmovement`
--
ALTER TABLE `productmovement`
  ADD PRIMARY KEY (`movement_id`),
  ADD KEY `from_location` (`from_location`),
  ADD KEY `to_location` (`to_location`),
  ADD KEY `product id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `productmovement`
--
ALTER TABLE `productmovement`
  MODIFY `movement_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `productmovement`
--
ALTER TABLE `productmovement`
  ADD CONSTRAINT `product id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
