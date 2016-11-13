from django.http import JsonResponse
from HorizonQuiz.my_unit import views_unit, logic
import uuid


def player_start_game(request, width=1, height=1, map_id=1):
    if request.session.session_key:
        return JsonResponse({'error:': 'you are start game'})

    request.session.save()
    player_key = request.session.session_key
    game_map = get_play_map(player_key, int(map_id), int(width), int(height))
    if len(logic.players) == 0:
        logic.players.append(player_key)
        return game_map

    enemy = logic.players[0]  # за врага принимаем первого в очереди
    logic.players = logic.players[1:]  # и удаляем его из очереди

    game_id = uuid.uuid1()  # случайную уникальную комбинацию принимаем за игровой id
    init_game(player_key, enemy, game_id, int(map_id))  # инициализация карты, соперников, стадии игры
    return game_map


def player_want_search_opponent(request, opp_id):
    if not request.session.session_key:
        request.session.save()
    else:
        return JsonResponse({'error:': 'you are start game'})


def get_play_map(player_key, map_id, width, height):
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []
    lst_types = []
    views_unit.fill_regions_info(map_id, lst_areas, lst_pos, lst_sizes, lst_urls, lst_types, width=width, height=height)

    lst_owner = []
    if player_key not in logic.game_ids:
        lst_owner = [1, 0, 0, 0, 0, 0, 0, 2]
    else:
        game_id = logic.game_ids[player_key]
        game_map = logic.games[game_id].game_map
        for region in game_map.regions:
            lst_owner.append(region.owner_id)

    return JsonResponse({
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region-sizes': lst_sizes,
        'region-types': lst_types,
        'region-owner': lst_owner,
    })


def init_game(player_key, his_enemy, game_id, map_id):
    # game_logic.player_ids[player_key] = uuid.uuid1

    logic.enemies[player_key] = his_enemy
    logic.enemies[his_enemy] = player_key
    logic.game_ids[player_key] = game_id  # id сессии нового игрока присваиваем словарю игровых сессий
    logic.game_ids[his_enemy] = game_id  # id сессии его врага присваиваем словарю игровых сессий

    current_map = views_unit.get_game_map_from_model(map_id)  # распределяем локации на карте
    logic.games[game_id] = logic.Game(player_key, his_enemy)
    logic.games[game_id].game_map.set_capitals(current_map)
