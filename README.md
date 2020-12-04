

### Referanseimplementasjon for digitalisering / innlegging av havnedata ved bruk av NGIS-OpenAPI

Kartverket har satt i gang et prosjekt for å få kartlagt et utvalg havner i Norge. Prosjektet vil pågå i 2020 og
har som målsetning å få etablert standardiserte datasett for havnedata i 14-17 havner i Norge.

Målsetningen med dette del-prosjektet var å få laget en referanseimplementasjon i QGIS programvaren som
muliggjør innlegging og ajourføring av havnedata-objekter gjennom NGIS-OpenAPI mot SFKB.

Resultatet av prosjektet var QGIS programtillegget «NGIS-OpenAPI Klient» skrevet i python.
Dette programtillegget kan i dag laste ned og presentere datasett fra NGIS-OpenAPI, og støtter også enkel redigering av utvalgte havnedata objekter.

Tilgjengelige datasett i NGIS-OpenAPI (knyttet til havnedata) har blitt brukt under utvikling og testing av dette programtillegget.



### Erfaringer

1.  Alle krav mht. til visning / uttegning av data er oppfylt.  Dette gjelder også ytelse ved nedlasting av data.
2.  Det fungerer å lage et nytt objekt, samt endre og slette eksisterende objekt.


Notes:

*   Det er noen utfordringer med å redigere flateobjekt som referer avgrensingslinjer. Men egenskaper kan redigeres.
*   Program-tillegget er ikke klar for et produksjons-miljø.


</div>

<div style="font-size:.9em;">

For information on writing PyQGIS code, see **http://loc8.cc/pyqgis_resources** for a list of resources.

</div>