
% Définition initiale de la porte avec trois cristaux et les couleurs spécifiées
initialize_door_3(Colours) :-
    retractall(door(_, _, _, _, _, _, _)),
    create_door_3(Colours).

create_door_3(Colours) :-
    random_member(Metal, Colours),
    random_crystals_3(Cristals),
    assertz(door(Metal, Cristals)).

% Définition des règles pour déverrouiller la porte avec trois cristaux et les couleurs spécifiées
unlock_door_3(DoorState, Position) :-
    DoorState = [Metal | Cristals],
    member(Metal, ['silver', 'gold', 'bronze']), % Vérifie si la couleur de la porte est valide

    count_specific_cristaux(Cristals, 'red', RedCount),
    count_specific_cristaux(Cristals, 'blue', BlueCount),
    count_specific_cristaux(Cristals, 'white', WhiteCount),

    (   RedCount == 0 -> Position = 'second'
    ;   last(Cristals, 'white') -> Position = 'last'
    ;   BlueCount > 1 -> last_blue_position(Cristals, Position), !
    ;   Position = 'first'
    ).

% Prédicat pour trouver la position du dernier cristal bleu
last_blue_position(Cristals, Position) :-
    reverse(Cristals, Reversed),
    nth0(Index, Reversed, 'blue'),
    length(Reversed, Length),
    PositionIndex is Length - Index - 1,
    nth0(PositionIndex, ['first', 'second', 'third'], Position).

% Prédicat pour compter le nombre d'éléments spécifiques dans une liste
count_specific_cristaux(List, Element, Count) :-
    include(==(Element), List, Filtered),
    length(Filtered, Count).
