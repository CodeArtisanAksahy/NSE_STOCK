with source as (
    select * from {{ source('raw', 'stock_prices') }}
)

select
    stock_symbol,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    loaded_at
from source
