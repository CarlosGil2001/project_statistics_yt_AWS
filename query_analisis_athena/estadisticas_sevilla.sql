WITH estadisticas_sevilla AS (    
    SELECT nombre_canal as Canal,
           suscripciones as Suscripciones,
           lag(suscripciones,1) over (order by created_at) as Suscripciones_previa, --N° de suscriptores del día anterior
           cantidad_videos as Cantidad_videos,
           lag(cantidad_videos) over (order by created_at) as Cantidad_videos_previa, --N° de videos del día anterior
           total_vistas as Vistas,
           lag(total_vistas) over (order by created_at) as Vistas_previas,  --N° de vistas del día anterior
           created_at as Fecha
    FROM "estadisticas_canal"."yt_estadisticas_output" 
    WHERE nombre_canal='Sevilla'
    ORDER BY created_at desc
)

-- %Incremento 
SELECT Canal,
       Suscripciones - Suscripciones_previa as Cantidad_suscripciones,
       ((cast(Suscripciones as decimal(16,4)) / cast(Suscripciones_previa as decimal(16,4))) -1) * 100 as Cambio_suscripciones,
       Vistas - Vistas_previas as Cantidad_Vistas,
       ((cast(Vistas as decimal(16,4)) / cast(Vistas_previas as decimal(16,4))) -1) * 100 as Cambio_vistas,
       Cantidad_videos - Cantidad_videos_previa as Cantidad_videos,
       ((cast(Cantidad_videos as decimal(16,4)) / cast(Cantidad_videos_previa as decimal(16,4))) -1) * 100 as Cambio_cantidad_videos,
       Fecha
FROM estadisticas_sevilla;