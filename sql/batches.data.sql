INSERT INTO public.batches ("number", "sku", "qty", "eta")
VALUES 
    ('fast-batch', 'LAMP', 100, '2023-01-23'),
    ('normal-batch', 'LAMP', 100, '2023-01-24'),
    ('old-batch', 'LAMP', 100, '2023-02-20');
    
begin;
truncate public.allocations;
truncate public.order_lines CASCADE;
truncate public.batches CASCADE;
commit;