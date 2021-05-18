# %%
# Code correspondant a Pappers API (2.0)

# %%
import requests as rq
import os
import urllib
from urllib.parse import urlencode
import pandas as pd
import re
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

# %%

class ApiException(Exception):
    pass

class IncorrectApiParam(Exception):
    pass

class ExceedElementLimit(Exception):
    pass

class Pappers(object):

    def __init__(self, API_KEY, MAX_DATA_SIZE):
        self.API_KEY = API_KEY
        self.MAX_DATA_SIZE = MAX_DATA_SIZE
        self.BASE_URL = "https://api.pappers.fr/v2"
        self.r = None
        self.resultats = []
        self.count = 0
        self.curr_page = 1
        self.final_page = None
        self.url_list = []

    def check_api_key_validity(self):
        r = rq.get(self.BASE_URL + "/entreprise" + "?api_token=" + self.API_KEY)
        # 400 : code pour requete mal formulée, si ce code apparait alors la clé API est nécessairement correcte
        if r.status_code != 400:
            raise ApiException("Invalid API_KEY, please consider request a valid API KEY on pappers.fr")
        else:
            return True

    def determine_if_n_element_is_sup_to_MAX_DATA_SIZE(self):
        if self.count > MAX_DATA_SIZE:
            raise ExceedElementLimit("Le nombre d'éléments retournés est supérieur à MAX_DATA_SIZE !")

    def determine_how_many_page_in_request(self, request_url):
        # degenerated request with 1 element by page
        self.final_page = 1
        self.curr_page = 1
        m = re.search('par_page=\d*', request_url).group(0)
        page_user = m.split('=')[1]
        if page_user == "":
            page_user = 100
        else:
            page_user = int(page_user)

        self.r = rq.get(self.BASE_URL + re.sub('par_page=\d*', 'par_page=1',request_url))
        self.count = self.r.json()["total"]
        # print(page_user)
        # print(self.curr_page)
        self.final_page = math.ceil(self.count / page_user)

    def generate_list_url(self, request_url):

        while self.curr_page < self.final_page + 1:
            # print(self.BASE_URL + request_url.replace("page=&", "page=%s&" % self.curr_page))
            url = self.BASE_URL + request_url.replace("page=&", "page=%s&" % self.curr_page)
            self.url_list.append(url)
            self.curr_page =  self.curr_page + 1

    def download_file(self, url, file_ct):
        try:
            html = rq.get(url, stream=True)
            # open(f'{file_name}.json', 'wb').write(html.content)
            print(url, " (%s/%s)" % (file_ct, self.count))
            return html
        except rq.exceptions.RequestException as e:
            return e

    def runner(self):
        threads = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            file_ct = 1
            for url in self.url_list:
                threads.append(executor.submit(self.download_file, url, file_ct))
                file_ct += 1

            for task in as_completed(threads):
                # print(task.result())
                self.resultats.extend(task.result().json()["resultats"])

    def execute_api_call(self, request_url):
        self.generate_list_url(request_url)
        self.runner()
    #
    # def recherche_to_dataframe(self):
    #     return pd.DataFrame(self.resultats)



# class Entreprise(Pappers):
#
#     def __init__(self, API_KEY, params):
#         Pappers.__init__(self, API_KEY)
#         super().check_api_key_validity()
#         self.params = urllib.parse.urlencode(params)
#     def exec(self):
#         return super().execute_api_call(self.params)

    # print(Pappers.API_KEY)

# class DownloadDocument(Pappers, Entreprise):
#
#     def __init__(self, API_KEY):
#         Pappers.__init__(self, API_KEY)
#         super().check_api_key_validity()

class Recherche(Pappers):
    def __init__(self, API_KEY, params, MAX_DATA_SIZE):
        Pappers.__init__(self, API_KEY, MAX_DATA_SIZE)
        self.params = urlencode(params)
        self.BRANCH = "/recherche"
        self.companies_urls = []
        self.companies_resultats = []

    def exec(self):
        request_url = self.BRANCH + "?api_token=" + self.API_KEY + "&" + self.params
        super().determine_if_n_element_is_sup_to_MAX_DATA_SIZE()
        super().determine_how_many_page_in_request(request_url)
        super().execute_api_call(request_url)

    def get_companies_url(self):
        sirens = [el['siren'] for el in self.resultats]
        for (isiren, siren) in enumerate(sirens):
            # print(isiren)
            url = self.BASE_URL + "/entreprise?api_token=%s&siren=%s" % (self.API_KEY, siren)
            self.companies_urls.append(url)
            # break

    # def companies_to_dataframe(self):
    #     return pd.DataFrame(self.companies_resultats)

    def runner2(self):
        threads = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            file_ct = 1
            for url in self.companies_urls:

                threads.append(executor.submit(self.download_file, url, file_ct))
                file_ct += 1
                # break
            for task in as_completed(threads):
                # print(task.result())
                self.companies_resultats.append(task.result().json())

    def get_companies_data(self):
        self.get_companies_url()
        self.runner2()


# class RechercheDirigeants(Pappers):
#     def __init__(self, API_KEY):
#         Pappers.__init__(self, API_KEY)
#
# class RechercheDocuments(Pappers):
#     def __init__(self, API_KEY):
#         Pappers.__init__(self, API_KEY)
#
# class RecherchePublications(Pappers):
#     def __init__(self, API_KEY):
#         Pappers.__init__(self, API_KEY)
#
# class Suggestions(Pappers):
#     def __init__(self, API_KEY):
#         Pappers.__init__(self, API_KEY)
#         self.URL = "https://suggestions.pappers.fr/v2"
# %%
# params = {"siren": "",
#           "siret": "",
#           "format_publications_bodacc": ""}

# entreprise = Entreprise(API_KEY, params)
# %%
# v = entreprise.exec()

# %%

API_KEY = "ae0388257ef5a57ce61c5fe6a2fee88b57ecd49c3fb2d346"
MAX_DATA_SIZE = 100_000
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




# b = pd.json_normalize(d, max_level=2)
# # %%
# a = pd.json_normalize(d,
#                   record_path='siren',
#                   meta=[siege])
# # %%
# d0 = pd.DataFrame([d[0]])
# %%
# params = {"par_page": "",
#           "page": "",
#           "precision": "",
#           "q":"",
#           "age_dirigeant_min":"",
#           "age_dirigeant_max":"",
#           "date_de_naissance_dirigeant_min": "",
#           "date_de_naissance_dirigeant_max": "",
#           "code_naf":"",
#           "departement":"",
#           "region":"",
#           "code_postal":"",
#           "convention_collective":"",
#           "categorie_juridique":"",
#           "entreprise_cessee":"",
#           "chiffre_affaires_min":"",
#           "chiffre_affaires_max":"",
#           "resultat_min":"",
#           "resultat_max":"",
#           "date_creation_min":"",
#           "date_creation_max":"",
#           "tranche_effectif_min":"",
#           "tranche_effectif_max":"",
#           "date_depot_document_min":"",
#           "date_depot_document_max": "",
#           "type_publication":"",
#           "date_publication_min":"",
#           "date_publication_max":""}
# recherche_dirigeants = RechercheDirigeants(API_KEY, )
#
# # %%
# params = {"par_page": "",
#           "page": "",
#           "precision": "",
#           "q":"",
#           "date_depot_document_min": "",
#           "date_depot_document_max": "",
#           "code_naf":"",
#           "departement": "",
#           "region": "",
#           "code_postal": "",
#           "convention_collective": "",
#           "categorie_juridique": "",
#           "entreprise_cessee": "",
#           "chiffre_affaires_min": "",
#           "chiffre_affaires_max": "",
#           "resultat_min": "",
#           "resultat_max": "",
#           "date_creation_min": "",
#           "date_creation_max": "",
#           "tranche_effectif_min": "",
#           "tranche_effectif_max": "",
#           "age_dirigeant_min":"",
#           "age_dirigeant_max":"",
#           "date_de_naissance_dirigeant_min": "",
#           "date_de_naissance_dirigeant_max": "",
#           "type_publication":"",
#           "date_publication_min":"",
#           "date_publication_max":""}
# recherche_documents = RechercheDocuments(API_KEY, )
# # %%
# params = {"par_page": "",
#           "page": "",
#           "precision": "",
#           "q":"",
#
#           "code_naf":"",
#           "departement": "",
#           "region": "",
#           "code_postal": "",
#           "convention_collective": "",
#           "categorie_juridique": "",
#           "entreprise_cessee": "",
#           "chiffre_affaires_min": "",
#           "chiffre_affaires_max": "",
#           "resultat_min": "",
#           "resultat_max": "",
#           "date_creation_min": "",
#           "date_creation_max": "",
#           "tranche_effectif_min": "",
#           "tranche_effectif_max": "",
#           "age_dirigeant_min":"",
#           "age_dirigeant_max":"",
#           "date_de_naissance_dirigeant_min": "",
#           "date_de_naissance_dirigeant_max": "",
#           "date_depot_document_min": "",
#           "date_depot_document_max": "",
#           "type_publication":"",
#           "date_publication_min":"",
#           "date_publication_max":""}
# recherche_publications = RecherchePublications(API_KEY, )
# # %%
# params = {
#     "q": "", # required
#     "longueur": "",
#     "cible": ""
# }
# recherche_publications = RecherchePublications(API_KEY, )
