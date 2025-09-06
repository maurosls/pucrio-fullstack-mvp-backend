# pucrio-fullstack-mvp-backend

Projeto que será responsável por conter a implementação do Backend feito em Python com Flask. 

## Conceito
A ideia do projeto é representar um sistema de auxílio para nutrição. Nele o usuário pode registrar as suas refeições (meal) diárias e então pode ter o calculo de quanto ele comeu em calorias. 

## Entidades

- Food
    - Representa o alimento ingerido com sua respectiva caloria, unidade de medida e quantidade de referencia.
- Meal
    - Representa um conjunto de alimentos que compõe uma refeição
- Meal item
    - É a entidade que representa a agregação entre Food e Meal
