-- Connect to the database
\c vic_recycle_map;

-- Drop the old views and tables
DROP VIEW IF EXISTS facility_products_buffer;
DROP VIEW IF EXISTS facility_product_categories;
DROP VIEW IF EXISTS facility_product_list_include;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS facility_product_join;
DROP TABLE IF EXISTS products;


CREATE TABLE products
(
   ProductID VARCHAR(20) PRIMARY KEY,
   Name VARCHAR(100),
   FriendlyUrl VARCHAR(100),
   Keywords VARCHAR(2000),
   MainMessage VARCHAR(2000),
   ReduceMessage VARCHAR(2000),
   ReuseMessage VARCHAR(2000),
   RecycleMessage VARCHAR(2000),
   EnvironmentalMessage VARCHAR(2000),
   DidYouKnowMessage Varchar(5000),
   Image Varchar(2000),
   Include VARCHAR(1),
   CategoryID INT
);

CREATE TABLE facility_product_join
(
	Fac_ID VARCHAR(20) NOT NULL,
	Prod_ID VARCHAR(20) NOT NULL,
	CONSTRAINT pk_fac_prod PRIMARY KEY (Fac_ID,Prod_ID)
);

CREATE TABLE product_categories
(
	ID INT NOT NULL,
	CATEGORY VARCHAR(100),
	IMAGE VARCHAR (600),
	CONSTRAINT pk PRIMARY KEY (ID)
);

-- Create View for points containing list of products and urls for product images
CREATE VIEW facility_product_list_include AS
    SELECT a.ogc_fid, a.wkb_geometry, a.facilityid, a.name, a.address, a.postalcode, a.phone_1, a.hours, a.QRImageTag, a.LogoImageTag,
    array_to_string(array_agg(products.name), ', ') as products,
    array_to_string(array_agg(textcat(
            textcat(text '<img id="prod" src="http://myrecyclopedia.ca/assets/images/uploads/', products.Image),
            text '"/>')
            )
        ,'') as product_images,
    products.CategoryID
    FROM facilities a
        LEFT JOIN facility_product_join
        ON a.facilityid = facility_product_join.Fac_ID
            LEFT JOIN products
            ON products.ProductID=facility_product_join.Prod_ID
    WHERE UPPER(products.include) = 'Y'
    GROUP BY a.ogc_fid, a.wkb_geometry, a.facilityid, a.name, a.address, a.postalcode, a.phone_1, a.hours, products.CategoryID, products.include
    ORDER BY a.name;

-- Create view including simplified product images
CREATE VIEW facility_product_categories AS
    SELECT a.ogc_fid, a.wkb_geometry, a.name, a.address, a.phone_1, a.hours, a.QRImageTag, a.LogoImageTag,
    string_agg(b.image, '')  as category_image
    FROM facility_product_list_include a
        LEFT JOIN product_categories as b
        on a.CategoryID = b.ID
    GROUP BY a.ogc_fid, a.wkb_geometry, a.name, a.address, a.phone_1, a.hours, a.QRImageTag, a.LogoImageTag
    ORDER BY a.name;

-- Create view for buffered geometry - this will make the QGIS annotations easier
CREATE VIEW facility_products_buffer AS
    SELECT ogc_fid, ST_Buffer(wkb_geometry, 10), name, address, postalcode, phone_1, hours, products, product_images
    FROM facility_product_list_include;

-- Copy data from 
\copy PRODUCTS FROM './Data/productfacilityinfo - Products.csv' DELIMITER ',' CSV HEADER;
\copy PRODUCT_CATEGORIES FROM './Data/productfacilityinfo - ProductCategories.csv' DELIMITER ',' CSV HEADER;
\copy FACILITY_PRODUCT_JOIN FROM './Data/productfacilityinfo - FacilityProductJoin.csv' DELIMITER ',' CSV HEADER;



