CREATE VIEW GAMES_BY_USERs2 AS
SELECT
    g.id,
    g.name,
    g.maker,
    g.game_type_id,
    g.number_of_players,
    g.skill_level,
    g.gamer_id,
    u.id user_id,
    u.first_name || " " || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gmr ON g.gamer_id = gmr.id
JOIN
    auth_user u ON gmr.user_id = u.id


CREATE VIEW EVENTS_BY_USER AS
SELECT
    e.id,
    e.description,
    e.date,
    e.organizer_id,
    g.name AS game_name,
    u.first_name || " " || u.last_name AS full_name
FROM
    levelupapi_event e
JOIN
    levelupapi_game g ON g.id = e.game_id
JOIN
    levelupapi_gamer gmr ON gmr.id = e.organizer_id
JOIN
    auth_user u ON gmr.user_id = u.id