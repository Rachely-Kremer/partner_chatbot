-- Create the customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT
);

-- Create the services table
CREATE TABLE services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    service_type TEXT CHECK (services_type IN ('mobile', 'internet', 'tv')),
    plan TEXT NOT NULL,
    status TEXT CHECK(status IN ('active','inactive')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create the usage table
CREATE TABLE usage (
    usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER,
    usage_type TEXT CHECK (usage_type IN  ('data', 'calls', 'sms')),
    amount REAL NOT NULL,
    usage_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- Insert sample customers
INSERT INTO customers (name, email, phone, address) VALUES
    ('Alice Johnson', 'alice.j@partner.com', '123-456-7890', '123 Elm St.'),
    ('Bob Smith', 'bob.s@partner.com', '234-567-8901', '456 Oak St.'),
    ('Charlie Davis', 'charlie.d@partner.com', '345-678-9012', '789 Pine St.');

-- Insert sample services
INSERT INTO services (customer_id, service_type, plan, status) VALUES
    (1, 'mobile', 'Unlimited Plan', 'active'),
    (1, 'internet', 'Fiber 100Mb', 'active'),
    (2, 'tv', 'Premium TV', 'active'),
    (3, 'mobile', 'Basic Plan', 'inactive');

-- Insert sample usage
INSERT INTO usage (service_id, usage_type, amount) VALUES
    (1, 'data', 2.5), -- Data usage in GB
    (1, 'calls', 120), -- Call usage in minutes
    (2, 'data', 50), -- Internet usage in GB
    (3, 'calls', 60), -- Call usage in minutes
    (4, 'sms', 30); -- SMS count
