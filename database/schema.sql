-- This file contains the table definitions for the trucks database.

DROP TABLE IF EXISTS FACT_transaction;
DROP TABLE IF EXISTS DIM_truck;
DROP TABLE IF EXISTS DIM_payment_method;

CREATE TABLE DIM_truck(
    truck_id INT IDENTITY(1,1) PRIMARY KEY,
    truck_name VARCHAR(255) NOT NULL,
    truck_description TEXT NOT NULL,
    has_card_reader BOOLEAN NOT NULL,
    fsa_rating SMALLINT NOT NULL
);

CREATE TABLE DIM_payment_method(
    payment_method_id INT IDENTITY(1,1) PRIMARY KEY,
    payment_method_name VARCHAR(32) UNIQUE NOT NULL
);

CREATE TABLE FACT_transaction(
    transaction_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    truck_id INT NOT NULL,
    payment_method_id SMALLINT NOT NULL,
    total INT NOT NULL,
    made_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (truck_id) REFERENCES DIM_truck(truck_id),
    FOREIGN KEY (payment_method_id) REFERENCES DIM_payment_method(payment_method_id)
);

INSERT INTO DIM_payment_method(payment_method_name) VALUES 
('cash'),
('card');

INSERT INTO DIM_truck(truck_name,truck_description,has_card_reader,fsa_rating) VALUES
('Burrito Madness','An authentic taste of Mexico.',true,4),
('Kings of Kebabs','Locally-source meat cooked over a charcoal grill.',true,2),
('Cupcakes by Michelle','Handcrafted cupcakes made with high-quality, organic ingredients.',true,5),
('Hartmann''s Jellied Eels','A taste of history with this classic English dish.',true,4),
('Yoghurt Heaven','All the great tastes, but only some of the calories.',true,4),
('SuperSmoothie','Pick any fruit or vegetable, and we''ll make you a delicious,healthy, multi-vitamin shake. Live well;live wild.',false,3);