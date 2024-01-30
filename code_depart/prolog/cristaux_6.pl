% Définition initiale de la porte avec trois cristaux et les couleurs spécifiées
initialize_door_6(Colours) :-
    retractall(door(_, _, _, _, _, _, _)),
    create_door_6(Colours).

create_door_6(Colours) :-
    random_member(Metal, Colours),
    random_crystals_6(Cristals),
    assertz(door(Metal, Cristals)).

% Définition des règles pour déverrouiller la porte avec six cristaux et les couleurs spécifiées
unlock_door_6(DoorState, Position) :-
    DoorState = [Metal | Cristals],
    member(Metal, ['silver', 'gold', 'bronze']), % Vérifie si la couleur de la porte est valide

    count_specific_cristaux(Cristals, 'red', RedCount),
    count_specific_cristaux(Cristals, 'blue', BlueCount),
    count_specific_cristaux(Cristals, 'yellow', YellowCount),
    count_specific_cristaux(Cristals, 'white', WhiteCount),

    (   \+ member('yellow', Cristals), Metal == 'bronze' -> Position = 'third'
    ;   count_specific_cristaux(Cristals, 'yellow', 1), WhiteCount > 1 -> Position = 'fourth'
    ;   RedCount == 0 -> Position = 'sixth'
    ;   Position = 'fourth'
    ).

% Prédicat pour compter le nombre de cristaux d'une couleur spécifique
count_specific_cristaux(Cristals, Color, Count) :-
    include(==(Color), Cristals, SpecificCristaux),
    length(SpecificCristaux, Count).