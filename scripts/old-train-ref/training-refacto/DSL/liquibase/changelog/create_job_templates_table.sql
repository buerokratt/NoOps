-- Create a table for job_templates
CREATE TABLE job_templates (
    id SERIAL PRIMARY KEY,
    job_name TEXT NOT NULL,
    job_template TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
