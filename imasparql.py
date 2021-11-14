# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper

# cvをとってくる関数
def get_idol_cv(name):
    sparql = SPARQLWrapper(endpoint='https://sparql.crssnky.xyz/spql/imas', returnFormat='json')
    sparql.setQuery("""                                                                                                  
    PREFIX imas: <https://sparql.crssnky.xyz/imasrdf/URIs/imas-schema.ttl#>
    PREFIX schema: <http://schema.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT DISTINCT *
    WHERE {
    ?s schema:name '%s'@ja .
    ?s imas:cv ?cv . FILTER( lang(?cv) = 'ja' )
    }                                                           
    """ %name)
    results = sparql.query().convert()
    print(results["results"]["bindings"])
    if results["results"]["bindings"] == []:
        return None
    return results["results"]["bindings"][0]["cv"]["value"]

# プロフィオールをとってくる関数
def get_idol_profile(name):
    sparql = SPARQLWrapper(endpoint='https://sparql.crssnky.xyz/spql/imas', returnFormat='json')
    sparql.setQuery("""                                                                                                  
    PREFIX imas: <https://sparql.crssnky.xyz/imasrdf/URIs/imas-schema.ttl#>
    PREFIX schema: <http://schema.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT DISTINCT *
    WHERE {
    ?s schema:name '%s'@ja .
    ?s foaf:age ?年齢 .
    OPTIONAL { ?s imas:cv ?cv . FILTER( lang(?cv) = 'ja' ) }
    OPTIONAL { ?s schema:description ?description . }
    OPTIONAL { ?s foaf:age ?age . }
    OPTIONAL { ?s schema:height ?height . }
    OPTIONAL { ?s schema:weight ?weight . }
    OPTIONAL { ?s schema:birthDate ?birthDate . }
    }                    
    """ %name)
    results = sparql.query().convert()
    print(results["results"]["bindings"])
    if results["results"]["bindings"] == []:
        return None
    return results["results"]["bindings"][0]["cv"]["value"]