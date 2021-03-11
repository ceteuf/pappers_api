# pappers_api

Pappers_api aims at interfacing the Pappers.fr API with python.

Pappers.fr Allows easy access to legal information of french companies and in particular to all legal documentation

About (fr) : https://www.pappers.fr/a-propos

Api documentation page (fr) : https://www.pappers.fr/api/documentation

Please, get a free key here (need to register) : https://www.pappers.fr/api/register

(WORK IN PROGRESS)

## API ORGANIZATION
Pappers Api offers 3 types of routes: 
* companies 
* search
* documents

pappers_api module design : 

search for companies following criteria => get companies data => download (all/specifics) documents

## USAGE

```python
API_KEY = "your_api_key"
MAX_DATA_SIZE = 100_000 # sets the maximum number of elements beyond which a more precise search must be performed
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
```         

```python
recherche = Recherche(API_KEY, params, MAX_DATA_SIZE)
recherche.exec() # performs api calls, return the companies found according to the criteria
recherche.get_companies_data() # retrieve data from the companies listed in the previous order
data = recherche.resultats # list of companies
data_companies = recherche.companies_resultats # company data

```
## TODOs

* implement all remaining routes
- companies (entreprise) routes
- other search root
* implement data formating functions (from neested json dict to multiple dataframes ?)
