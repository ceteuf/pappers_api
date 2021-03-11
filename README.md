# pappers_api

Pappers_api aims at interfacing the Pappers.fr API with python.

Pappers.fr Allows easy access to legal information of french companies and in particular to all legal documentation

About (fr) : https://www.pappers.fr/a-propos

Api documentation page (fr) : https://www.pappers.fr/api/documentation


(WORK IN PROGRESS)


```python
API_KEY = "ae0388257ef5a57ce61c5fe6a2fee88b57ecd49c3fb2d346"
MAX_DATA_SIZE = 100_000
```
```python
params = {"par_page": "1000",
          "page": "",
          "bases": "",
          "precision": "",
          "q":"",
          "code_naf":"56.30Z",
          "departement":"",
          "region":"",
          "code_postal":"30000",
          "convention_collective": "",
          "categorie_juridique":"",
          "entreprise_cessee":"",
          "chiffre_affaires_min":"",
          "chiffre_affaires_max":"",
          "resultat_min":"",
          "resultat_max":"",
          "date_creation_min":"01-01-1980",
          "date_creation_max":"",
          "tranche_effectif_max":"",
          "age_dirigeant_min":"",
          "age_dirigeant_max":"",
          "date_de_naissance_dirigeant_min": "",
          "date_de_naissance_dirigeant_max": "",
          "date_depot_document_min": "",
          "date_depot_document_max": "",
          "type_publication": "",
          "date_publication_min":"",
          "date_publication_max":""}
recherche = Recherche(API_KEY, params, MAX_DATA_SIZE)

# %%
recherche.exec()
# %%
recherche.get_companies_data()
# %%
data = recherche.resultats

# %%
data_companies = recherche.companies_resultats

```
