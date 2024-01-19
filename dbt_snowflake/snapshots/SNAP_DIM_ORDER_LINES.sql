{% snapshot SNAP_DIM_ORDER_LINES %}
    {{
        config(
            target_database='development',
            target_schema='snapshots',
            unique_key='OL_PK',
            strategy='check',
            check_cols='all'
        )
    }}

select * from {{ ref('DIM_ORDER_LINES') }}
-- comment for PR

{% endsnapshot %}
