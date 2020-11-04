# coding: utf-8

# flake8: noqa

"""
    Oppdateringsgrensesnitt for SFKB

    # NGIS-OpenAPI  Grov oversikt over funksjonalitet:   - Hente liste over tilgjengelige datasett    - Hente metadata for et bestemt datasett   - Hente data fra et bestemt datasett     - Med lesetilgang eller skrivetilgang (medfører låsing)       - områdebegrensning       - egenskapsspørring (begrenset i første versjon til bygningsnummer eller lokalid)   - Lagre data til et bestemt datasett     - Operasjoner som håndteres: nytt objekt, endre objekt og slett objekt  ## Generelle prinsipper for systemet  ### Delt geometri  Flater består av avgrensningslinjer som ligger lagret som egne objekter. På den måten kan en linje avgrense ingen, én eller flere flater. Det er likevel slik at flater hentes ut og lagres med egen geometri for å gjøre det enklere å tegne opp datene, men ved endring av (delte) linjer og flater må det tas hensyn til delt geometri. Forsøk på endring av linje eller flate uten tilsvarende endring av evt. delt geometri vil bli avvist av systemet.  ### Låsing  Dette er nærmere beskrevet i de aktuelle kallene.  Foreløpig er det kun `user_lock` som er støttet. Det betyr at data må hentes ut med `user_lock` før de kan sendes inn med endringer.  ### Porsjonering  All uthenting av feature-objekter vil kunne bli porsjonert av serveren, se `limit`-parameteret.   ### Koordinatsystemer og transformasjon  For å sende inn koordinater i uri-spørringen (f.eks med `bbox`-parameteret) må koordinatsystemet angis med `crs_EPSG`-parameteret.  For å hente ut koordinater på annet koordinatsystem enn i dataset'et kan ønsket koordinatsystem angis i `Accept`-headeren med `crs_EPSG`. Se eksempler på dette i kallene.   # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import apis into sdk package
from swagger_client.api.features_api import FeaturesApi
from swagger_client.api.locks_api import LocksApi
from swagger_client.api.metadata_api import MetadataApi
# import ApiClient
from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration
# import models into sdk package
from swagger_client.models.bounding_box import BoundingBox
from swagger_client.models.dataset import Dataset
from swagger_client.models.dataset_list import DatasetList
from swagger_client.models.dataset_list_inner import DatasetListInner
from swagger_client.models.error import Error
from swagger_client.models.inline_response200 import InlineResponse200
from swagger_client.models.locking import Locking
from swagger_client.models.locks import Locks
from swagger_client.models.locks_inner import LocksInner
