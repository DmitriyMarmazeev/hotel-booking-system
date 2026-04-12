-- Сначала создаем тестовых пользователей, если их нет
INSERT INTO users (
    id,
    email,
    password_hash,
    first_name,
    last_name,
    role
  )
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'guest@example.com',
    'hashed_password_here',
    'Иван',
    'Гость',
    'guest'
  ),
  (
    '22222222-2222-2222-2222-222222222222',
    'manager@hotel.com',
    'hashed_password_here',
    'Анна',
    'Менеджер',
    'hotel_manager'
  ),
  (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'admin@system.com',
    'hashed_password_here',
    'Админ',
    'Системный',
    'admin'
  ) ON CONFLICT (email) DO NOTHING;
-- Базовые типы номеров
INSERT INTO room_types (
    id,
    name,
    description,
    base_price,
    capacity,
    amenities,
    bed_type
  )
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'Эконом',
    'Комфортабельный номер с всеми необходимыми удобствами',
    2500.00,
    2,
    '["wi_fi", "tv"]',
    'double'
  ),
  (
    '22222222-2222-2222-2222-222222222222',
    'Стандарт',
    'Просторный номер с улучшенной планировкой',
    4000.00,
    2,
    '["wi_fi", "tv", "ac", "minibar"]',
    'double'
  ),
  (
    '33333333-3333-3333-3333-333333333333',
    'Люкс',
    'Роскошный номер с дополнительным пространством',
    7500.00,
    3,
    '["wi_fi", "tv", "ac", "minibar", "jacuzzi"]',
    'king'
  ),
  (
    '44444444-4444-4444-4444-444444444444',
    'Семейный',
    'Просторный номер для семьи с детьми',
    6000.00,
    4,
    '["wi_fi", "tv", "ac", "minibar"]',
    'twin'
  ) ON CONFLICT (id) DO NOTHING;
-- Пример отеля
INSERT INTO hotels (
    id,
    name,
    description,
    address,
    city,
    country,
    star_rating,
    amenities,
    manager_id
  )
VALUES (
    '55555555-5555-5555-5555-555555555555',
    'Гранд Отель',
    'Роскошный отель в центре города',
    'ул. Центральная, 1',
    'Москва',
    'Россия',
    5,
    '["spa", "pool", "restaurant", "gym"]',
    '22222222-2222-2222-2222-222222222222'
  ) ON CONFLICT (id) DO NOTHING;
-- Номера в отеле
INSERT INTO rooms (id, room_number, floor, hotel_id, room_type_id)
VALUES (
    '66666666-6666-6666-6666-666666666666',
    '101',
    1,
    '55555555-5555-5555-5555-555555555555',
    '11111111-1111-1111-1111-111111111111'
  ),
  (
    '77777777-7777-7777-7777-777777777777',
    '102',
    1,
    '55555555-5555-5555-5555-555555555555',
    '11111111-1111-1111-1111-111111111111'
  ),
  (
    '88888888-8888-8888-8888-888888888888',
    '201',
    2,
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222'
  ),
  (
    '99999999-9999-9999-9999-999999999999',
    '301',
    3,
    '55555555-5555-5555-5555-555555555555',
    '33333333-3333-3333-3333-333333333333'
  ) ON CONFLICT (id) DO NOTHING;
-- Пример бронирования (выполняется только если пользователь существует)
INSERT INTO bookings (
    id,
    check_in_date,
    check_out_date,
    number_of_guests,
    total_price,
    status,
    guest_id,
    room_id
  )
SELECT 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  '2024-12-01',
  '2024-12-05',
  2,
  10000.00,
  'confirmed',
  id,
  '66666666-6666-6666-6666-666666666666'
FROM users
WHERE email = 'guest@example.com'
  AND NOT EXISTS (
    SELECT 1
    FROM bookings
    WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
  );
-- Пример платежа
INSERT INTO payments (
    id,
    amount,
    payment_method,
    payment_status,
    booking_id
  )
VALUES (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    10000.00,
    'card',
    'completed',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
  ) ON CONFLICT (id) DO NOTHING;