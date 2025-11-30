-- Создание enum типов
CREATE TYPE user_role AS ENUM ('guest', 'hotel_manager', 'admin');
CREATE TYPE booking_status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed');
CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed', 'refunded');
-- Таблица пользователей
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  role user_role NOT NULL DEFAULT 'guest',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
-- Таблица отелей
CREATE TABLE hotels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  address TEXT NOT NULL,
  city VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  star_rating INTEGER CHECK (
    star_rating >= 1
    AND star_rating <= 5
  ),
  contact_email VARCHAR(255),
  contact_phone VARCHAR(20),
  amenities JSONB DEFAULT '[]',
  images JSONB DEFAULT '[]',
  manager_id UUID NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  -- Добавляем
  FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE RESTRICT
);
-- Таблица типов номеров
CREATE TABLE room_types (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  base_price DECIMAL(10, 2) NOT NULL CHECK (base_price >= 0),
  capacity INTEGER NOT NULL CHECK (capacity > 0),
  amenities JSONB DEFAULT '[]',
  size_sqm INTEGER CHECK (size_sqm > 0),
  bed_type VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- Добавляем
);
-- Таблица номеров
CREATE TABLE rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_number VARCHAR(20) NOT NULL,
  floor INTEGER CHECK (floor >= 0),
  is_available BOOLEAN NOT NULL DEFAULT TRUE,
  images JSONB DEFAULT '[]',
  hotel_id UUID NOT NULL,
  room_type_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  -- Добавляем
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE RESTRICT
);
-- Таблица бронирований
CREATE TABLE bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  check_in_date DATE NOT NULL,
  check_out_date DATE NOT NULL,
  number_of_guests INTEGER NOT NULL CHECK (number_of_guests > 0),
  total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
  status booking_status NOT NULL DEFAULT 'pending',
  special_requests TEXT,
  guest_id UUID NOT NULL,
  room_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  cancelled_at TIMESTAMP WITH TIME ZONE,
  FOREIGN KEY (guest_id) REFERENCES users(id) ON DELETE RESTRICT,
  FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE RESTRICT,
  -- Проверка, что дата выезда после даты заезда
  CONSTRAINT valid_dates_check CHECK (check_out_date > check_in_date)
);
-- Таблица ценообразования
CREATE TABLE pricing (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  is_available BOOLEAN NOT NULL DEFAULT TRUE,
  room_type_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  -- Добавляем
  FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE,
  UNIQUE (room_type_id, date)
);
-- Таблица платежей
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
  payment_method VARCHAR(50) NOT NULL,
  payment_status payment_status NOT NULL DEFAULT 'pending',
  transaction_id VARCHAR(255),
  payment_date TIMESTAMP WITH TIME ZONE,
  booking_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE RESTRICT
);
-- Таблица отзывов
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rating INTEGER NOT NULL CHECK (
    rating >= 1
    AND rating <= 5
  ),
  comment TEXT,
  cleanliness_rating INTEGER CHECK (
    cleanliness_rating >= 1
    AND cleanliness_rating <= 5
  ),
  service_rating INTEGER CHECK (
    service_rating >= 1
    AND service_rating <= 5
  ),
  location_rating INTEGER CHECK (
    location_rating >= 1
    AND location_rating <= 5
  ),
  is_approved BOOLEAN NOT NULL DEFAULT FALSE,
  user_id UUID NOT NULL,
  hotel_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
  -- Один пользователь может оставить только один отзыв на отель
  UNIQUE (user_id, hotel_id)
);
-- Создание индексов для оптимизации запросов
-- Индексы для пользователей
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
-- Индексы для отелей
CREATE INDEX idx_hotels_city ON hotels(city);
CREATE INDEX idx_hotels_country ON hotels(country);
CREATE INDEX idx_hotels_manager ON hotels(manager_id);
CREATE INDEX idx_hotels_location ON hotels(latitude, longitude);
-- Индексы для номеров
CREATE INDEX idx_rooms_hotel ON rooms(hotel_id);
CREATE INDEX idx_rooms_room_type ON rooms(room_type_id);
CREATE INDEX idx_rooms_availability ON rooms(is_available)
WHERE is_available = true;
-- Индексы для бронирований
CREATE INDEX idx_bookings_guest ON bookings(guest_id);
CREATE INDEX idx_bookings_room ON bookings(room_id);
CREATE INDEX idx_bookings_dates ON bookings(check_in_date, check_out_date);
CREATE INDEX idx_bookings_status ON bookings(status);
-- Индексы для ценообразования
CREATE INDEX idx_pricing_date ON pricing(date);
CREATE INDEX idx_pricing_room_type ON pricing(room_type_id);
CREATE INDEX idx_pricing_availability ON pricing(is_available)
WHERE is_available = true;
-- Индексы для платежей
CREATE INDEX idx_payments_booking ON payments(booking_id);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_payments_transaction ON payments(transaction_id);
-- Индексы для отзывов
CREATE INDEX idx_reviews_hotel ON reviews(hotel_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
-- Триггер для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER update_users_updated_at BEFORE
UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();