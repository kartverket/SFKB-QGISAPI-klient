<StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:se="http://www.opengis.net/se"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <NamedLayer>
        <se:Name>Beredskapspunkt</se:Name>
        <UserStyle>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>Fare</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{fare}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---annen.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Brannvesen</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{brannvesen}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---annen.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Brannslukking</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{brannslukking}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_brannslukking.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Varslingssentral</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{varslingssentral}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_varslingssentral.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Annen</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{annen}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---annen.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Nødplakat Infopunkt</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{nødplakatInfopunkt}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_nodplakatInfopunkt.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Redningsbøye</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{redningsbøye}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_redning.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Redningsbøye</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{"redningsbøye"}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_redning.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Stige</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{stige}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---stige.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Oljelenser</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{oljelenser}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---oljelenser.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Båtshake</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{båtshake}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---baatshake.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Førstehjelp</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{forstehjelp}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="http://register.geonorge.no/symbol/files/havnesymboler/beredskapspunkt---annen.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Samlingsplass</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>beredskapstype</ogc:PropertyName>
                            <ogc:Literal>{samlingsplass}</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>2500.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Beredskapspunkt_samlingspunkt.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

