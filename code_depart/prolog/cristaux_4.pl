
% Définition initiale de la porte avec trois cristaux et les couleurs spécifiées
initialize_door_4(Colours) :-
    retractall(door(_, _, _, _, _, _, _)),
    create_door_4(Colours).

create_door_4(Colours) :-
    random_member(Metal, Colours),
    random_crystals_4(Cristals),
    assertz(door(Metal, Cristals)).

% Définition des règles pour déverrouiller la porte avec quatre cristaux et les couleurs spécifiées
unlock_door_4(DoorState, Position) :-
    DoorState = [Metal | Cristals],
    member(Metal, ['silver', 'gold', 'bronze']), % Vérifie si la couleur de la porte est valide

    count_specific_cristaux(Cristals, 'red', RedCount),
    count_specific_cristaux(Cristals, 'blue', BlueCount),
    count_specific_cristaux(Cristals, 'yellow', YellowCount),

    (   RedCount > 1, Metal == 'silver' -> last_red_position(Cristals, Position)
    ;   last(Cristals, 'yellow'), RedCount == 0 -> Position = 'first'
    ;   count_specific_cristaux(Cristals, 'blue', 1) -> Position = 'first'
    ;   YellowCount > 1 -> last_yellow_position(Cristals, Position)
    ;   Position = 'second'
    ).

% Prédicat pour trouver la position du dernier cristal jaune
last_yellow_position(Cristals, Position) :-
    reverse(Cristals, Reversed),
    nth0(Index, Reversed, 'yellow'),
    length(Reversed, Length),
    PositionIndex is Length - Index - 1,
    nth0(PositionIndex, ['first', 'second', 'third', 'fourth'], Position).

% Prédicat pour trouver la position du dernier cristal rouge
last_red_position(Cristals, Position) :-
    reverse(Cristals, Reversed),
    nth0(Index, Reversed, 'red'),
    length(Reversed, Length),
    PositionIndex is Length - Index - 1,
    nth0(PositionIndex, ['first', 'second', 'third', 'fourth'], Position).

% Prédicat pour compter le nombre d'éléments spécifiques dans une liste
count_specific_cristaux(List, Element, Count) :-
    include(==(Element), List, Filtered),
    length(Filtered, Count).