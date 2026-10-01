-- AI Travel Planner Agent - Database DDL Schema
-- MySQL 8.0 Compatible

CREATE DATABASE IF NOT EXISTS travel_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE travel_ai;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Destinations Table
CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    climate VARCHAR(100) DEFAULT 'Pleasant',
    best_season VARCHAR(255) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    avg_daily_budget_inr DECIMAL(10, 2) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(500),
    tags_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dest_city (city),
    INDEX idx_dest_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Attractions Table
CREATE TABLE IF NOT EXISTS attractions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL, -- Adventure, Nature, Cultural, Heritage, Food, Nightlife
    description TEXT NOT NULL,
    duration_hours DECIMAL(4, 1) DEFAULT 2.0,
    entry_fee_inr DECIMAL(10, 2) DEFAULT 0.00,
    rating DECIMAL(3, 2) DEFAULT 4.50,
    best_time_of_day VARCHAR(50) DEFAULT 'Morning', -- Morning, Afternoon, Evening, Night
    image_url VARCHAR(500),
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_attraction_dest (destination_id),
    INDEX idx_attraction_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Accommodations Table
CREATE TABLE IF NOT EXISTS accommodations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL, -- Budget, Moderate, Luxury
    price_per_night_inr DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 4.20,
    address VARCHAR(255),
    amenities_json JSON,
    image_url VARCHAR(500),
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_hotel_dest (destination_id),
    INDEX idx_hotel_tier (tier)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Trips / Saved Itineraries Table
CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    destination_id INT NOT NULL,
    days INT NOT NULL,
    travelers_count INT DEFAULT 1,
    travel_style VARCHAR(100) DEFAULT 'Balanced',
    total_budget_inr DECIMAL(12, 2) NOT NULL,
    estimated_cost_inr DECIMAL(12, 2) NOT NULL,
    itinerary_json JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    INDEX idx_trip_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. User Preferences Table
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    preferred_travel_style VARCHAR(100) DEFAULT 'Balanced',
    budget_tier VARCHAR(50) DEFAULT 'Moderate',
    dietary_preferences VARCHAR(255) DEFAULT 'Any',
    pace_preference VARCHAR(50) DEFAULT 'Moderate',
    interests_json JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Conversations & Messages
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(64) PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) DEFAULT 'New Travel Plan',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_conv_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(64) NOT NULL,
    sender VARCHAR(20) NOT NULL, -- user, assistant
    content TEXT NOT NULL,
    agent_steps_json JSON,
    itinerary_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_msg_conv (conversation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
