# Recetario de los lechugones

The community recipe book of [CocinaParaLechugones](https://github.com/jsarriaa/recipe-cart).
In the app, **Recetas → ⋮ → Recetas de la comunidad** searches this book and downloads recipes.

*Recetas compartidas por la gente que usa CocinaParaLechugones. Búscalas y descárgalas desde la
app: Recetas → ⋮ → Recetas de la comunidad.*

## How it works

- Every recipe is one file in [`recipes/`](recipes/), in the app's
  [recipe format](https://github.com/jsarriaa/recipe-cart/blob/main/docs/RECIPE_FORMAT.md)
  (`cpl-recipe/1`). The optional `author` field is the name shown as "por …".
- [`index.json`](index.json) lists every recipe with its title, author, tags, time and
  ingredient names. The app downloads it to search and filter. **Do not edit it by hand**: the
  [Build index](.github/workflows/index.yml) workflow rebuilds it after every change to
  `recipes/`. Files that are not valid recipes are left out, with a warning in the workflow log.

## Moderation

Recipes arrive from the app's "Publicar en la comunidad" (one new file per publication), or
are added by hand. The owner ([@jsarriaa](https://github.com/jsarriaa)) can edit or delete any
recipe in GitHub's web editor. The index updates by itself a minute later, and the app sees the
change on its next search (GitHub's file cache can take up to 5 minutes).

Step-by-step guide (change, delete, add, check, undo):
[Editing the community recipe book on GitHub](https://github.com/jsarriaa/recipe-cart#editing-the-community-recipe-book-on-github).

## Licence

By publishing a recipe here you agree to share it under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): anyone may use and adapt it, as long
as they credit its author.
