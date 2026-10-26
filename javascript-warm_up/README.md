# JavaScript warm up

## Task 0

### var
`var` est un mot-clé JavaScript qui permet de définir une variable. C'est un
ancien mot-clé qui a été remplacé par `let` et `const`, car il permettait de
définir autant de fois que l'on voulait une variable du même nom dans un même
programme. Cela était dangereux, particulièrement lorsque plusieurs
développeurs travaillaient sur le même fichier : on pouvait définir une
variable avec le même nom qu'une définition précédente, ce qui écrasait
l'ancienne valeur sans aucune erreur de la part de l'interpréteur.

### let
`let` est un mot-clé apparu pour remplacer `var` et corriger ses failles.
Cette fois-ci, si l'on essaie de redéfinir une variable déclarée avec `let`,
une erreur apparaît instantanément, sans même lancer le programme : tout
est bloqué immédiatement.

### const
`const` permet lui aussi de définir une variable, mais ce mot-clé bloque
en plus toute tentative de changement de valeur. Comme `let`, il bloque
les redéfinitions avant même le lancement du programme. En revanche, pour
un simple changement de valeur, l'erreur n'apparaît qu'à l'exécution :
les valeurs affichées avant cette ligne s'afficheront donc quand même.
