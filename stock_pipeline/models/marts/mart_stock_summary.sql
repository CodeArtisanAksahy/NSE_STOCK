with base as (
    select * from {{ ref('stg_stock_prices') }}
),

with_prev_close as (
    select
        stock_symbol,
        trade_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        lag(close_price) over (
            partition by stock_symbol
            order by trade_date
        ) as prev_close_price
    from base
)

select
    stock_symbol,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    prev_close_price,
    round(
        ((close_price - prev_close_price) / prev_close_price) * 100,
        2
    ) as daily_pct_change
from with_prev_close
