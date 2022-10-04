<StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:se="http://www.opengis.net/se"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
     <NamedLayer>
        <se:Name>Havnesensor</se:Name>
        <UserStyle>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>annen</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>annen</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_annen3.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>strøm</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>strøm</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_strom.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>temperatur</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>temperatur</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_temperatur.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>vannstand</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>vannstand</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_vannstand.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>vind</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>vind</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_vind.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>værstasjon</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>værstasjon</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_vaerstasjon.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>dørsensor</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>dørsensor</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_dorsensor.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>fartsmåler</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>fartsmåler</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_fartsmaler.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>luftkvalitet</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>luftkvalitet</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_luftkvalitet2.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>portsensor</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>portsensor</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_portsensor.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>redningsbøyeskap-sensor</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>redningsbøyeskapSensor</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_redningsboyeskapsensor.svg"/>
                                <se:Format>image/svg+xml</se:Format>
                            </se:ExternalGraphic>
                        <se:Size>14</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>støymåler</se:Name>
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>sensortype</ogc:PropertyName>
                            <ogc:Literal>støymåler</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <!--Parametric SVG-->
                            <se:ExternalGraphic>
                                <se:OnlineResource xlink:type="simple" xlink:href="https://havnedata.blob.core.windows.net/symboler/Havnesensor_stoymaler.svg"/>
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

