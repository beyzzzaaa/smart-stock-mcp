-- Seed Categories
INSERT INTO categories (id, name) VALUES (1, 'Elektronik') ON CONFLICT (id) DO NOTHING;
INSERT INTO categories (id, name) VALUES (2, 'Ofis Malzemeleri') ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE categories_id_seq RESTART WITH 3;

-- Seed Subcategories
INSERT INTO subcategories (id, category_id, name) VALUES (1, 1, 'Akıllı Telefonlar') ON CONFLICT (id) DO NOTHING;
INSERT INTO subcategories (id, category_id, name) VALUES (2, 1, 'Bilgisayarlar') ON CONFLICT (id) DO NOTHING;
INSERT INTO subcategories (id, category_id, name) VALUES (3, 2, 'Kağıt Ürünleri') ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE subcategories_id_seq RESTART WITH 4;

-- Seed Brands
INSERT INTO brands (id, name) VALUES (1, 'Apple') ON CONFLICT (id) DO NOTHING;
INSERT INTO brands (id, name) VALUES (2, 'Samsung') ON CONFLICT (id) DO NOTHING;
INSERT INTO brands (id, name) VALUES (3, 'HP') ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE brands_id_seq RESTART WITH 4;

-- Seed Models
INSERT INTO models (id, brand_id, name) VALUES (1, 1, 'iPhone 15 Pro') ON CONFLICT (id) DO NOTHING;
INSERT INTO models (id, brand_id, name) VALUES (2, 2, 'Galaxy S24') ON CONFLICT (id) DO NOTHING;
INSERT INTO models (id, brand_id, name) VALUES (3, 3, 'LaserJet Pro') ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE models_id_seq RESTART WITH 4;

-- Seed Products
INSERT INTO products (id, sku, name, description, subcategory_id, model_id, stock_quantity, minimum_stock, target_stock, warehouse_info) 
VALUES (1, 'APP-IPH15P', 'iPhone 15 Pro 128GB', 'Apple amiral gemisi akıllı telefon, siyah titanyum.', 1, 1, 2, 5, 10, 'A-Blok Raf 4')
ON CONFLICT (id) DO NOTHING;

INSERT INTO products (id, sku, name, description, subcategory_id, model_id, stock_quantity, minimum_stock, target_stock, warehouse_info) 
VALUES (2, 'SAM-GS24', 'Galaxy S24 256GB', 'Samsung amiral gemisi akıllı telefon, gri.', 1, 2, 0, 3, 8, 'A-Blok Raf 5')
ON CONFLICT (id) DO NOTHING;

INSERT INTO products (id, sku, name, description, subcategory_id, model_id, stock_quantity, minimum_stock, target_stock, warehouse_info) 
VALUES (3, 'HP-LJP-M15', 'LaserJet M15w Yazıcı', 'HP Lazer yazıcı, siyah-beyaz.', 3, 3, 12, 4, 10, 'B-Blok Raf 12')
ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE products_id_seq RESTART WITH 4;

-- Seed Incoming Orders
INSERT INTO incoming_orders (id, product_id, quantity, status, expected_delivery_date, created_at)
VALUES (1, 1, 3, 'PENDING', CURRENT_TIMESTAMP + INTERVAL '3 days', CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;
ALTER SEQUENCE incoming_orders_id_seq RESTART WITH 2;
