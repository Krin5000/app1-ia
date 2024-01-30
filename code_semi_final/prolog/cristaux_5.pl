% Définition initiale de la porte avec trois cristaux et les couleurs spécifiées
initialize_door_5(Colours) :-
    retractall(door(_, _, _, _, _, _, _)),
    create_door_5(Colours).

create_door_5(Colours) :-
    random_member(Metal, Colours),
    random_crystals_5(Cristals),
    assertz(door(Metal, Cristals)).

% Définition des règles pour déverrouiller la porte avec cinq cristaux et les couleurs spécifiées
unlock_door_5(DoorState, Position) :-
    DoorState = [Metal | Cristals],
    member(Metal, ['silver', 'gold', 'bronze']), % Vérifie si la couleur de la porte est valide

    count_specific_cristaux(Cristals, 'red', RedCount),
    count_specific_cristaux(Cristals, 'black', BlackCount),
    count_specific_cristaux(Cristals, 'yellow', YellowCount),

    (   last(Cristals, 'black'), Metal == 'gold' -> Position = 'fourth'
    ;   count_specific_cristaux(Cristals, 'red', 1), YellowCount > 1 -> Position = 'first'
    ;   \+ member('black', Cristals), BlackCount == 0 -> Position = 'second'
    ;   Position = 'first'
    ).

% Prédicat pour compter le nombre d'éléments spécifiques dans une liste
count_specific_cristaux(List, Element, Count) :-
    include(==(Element), List, Filtered),
    length(Filtered, Count).