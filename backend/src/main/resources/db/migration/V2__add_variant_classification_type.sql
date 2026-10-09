ALTER TABLE variant
ADD COLUMN classification_type VARCHAR(50) NULL
AFTER variant_type;