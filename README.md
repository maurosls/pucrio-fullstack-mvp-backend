# Meal Tracker API 

Projeto da disciplina Fullstack Báscico do curso de Pós Graduação em Engenharia de Software pela Puc RIO.

Projeto que será responsável por conter a implementação do Backend feito em Python com Flask. A ideia do projeto é representar um sistema de auxílio para nutrição. Nele o usuário pode registrar as suas refeições (meal) diárias e então pode ter o calculo de quanto ele comeu em calorias. 

API em **Flask + SQLite + SQLAlchemy** para registrar refeições do dia e calcular calorias.
Entidades principais:

* **Food**: alimento com `name`, `calories` (por `amount` na `unit`).
* **Meal**: refeição de um `day` com um `meal_type` (`breakfast`, `lunch`, `dinner`, `snack`).
* **MealItem**: vínculo entre Meal e Food com `quantity` (quantas vezes o `amount` do Food).

O banco `app.db` é criado automaticamente e vem com alguns alimentos e um exemplo de refeição.

---

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

A API sobe em `http://127.0.0.1:5000` por padrão do Flask.

---

## Endpoints

### 1) Listar alimentos

**GET `/foods`**
Retorna todos os alimentos.

**Exemplo de resposta**

```json
[
  {"id": 1, "name": "Banana", "calories": 89, "amount": 100, "unit": "g"}
]
```

### 2) Criar alimento

**POST `/foods`**
Body (JSON):

```json
{
  "name": "Aveia",
  "calories": 389,
  "amount": 100,
  "unit": "g"
}
```

Resposta `201 Created`: objeto `Food` criado.

---

### 3) Criar refeição (com itens opcionais)

**POST `/meals`**
Body (JSON):

```json
{
  "day": "2025-09-09",                 // opcional; padrão = hoje
  "meal_type": "breakfast",            // "breakfast" | "lunch" | "dinner" | "snack"
  "items": [
    {"food_id": 1, "quantity": 1.5}, 
    {"food_id": 3, "quantity": 1}
  ]
}
```

Resposta `201 Created`: objeto `Meal` com `items`, `total_calories`.

---

### 4) Listar refeições (com itens)

**GET `/meals?date=YYYY-MM-DD`**
Query `date` é opcional (padrão: todas).
Retorna lista de refeições do dia (quando filtrado), incluindo itens e `total_calories`.

---

### 5) Buscar uma refeição

**GET `/meals/<meal_id>`**
Retorna a refeição com seus itens e alimentos.

---

### 6) Adicionar item a uma refeição

**POST `/meals/<meal_id>/items`**
Body (JSON):

```json
{
  "food_id": 1,
  "quantity": 2
}
```

Resposta `201 Created`:

```json
{
  "item": { "...": "dados do item criado" },
  "meal": { "...": "refeição atualizada com total_calories" }
}
```

---

### 7) Total de calorias por dia

**GET `/total?date=YYYY-MM-DD`** (padrão: hoje)
Retorna:

```json
{
  "date": "2025-09-09",
  "total_calories": 1234.5,
  "meals": [
    { "meal_id": 10, "meal_type": "breakfast", "calories": 450.0 }
  ]
}
```

---

## Observações de cálculo

* `Food.calories` é por `amount` na `unit` (ex.: 89 kcal por 100 g).
* `MealItem.quantity` multiplica esse valor: `calories_do_item = quantity × Food.calories`.
* `Meal.total_calories` soma as calorias de todos os itens da refeição.
