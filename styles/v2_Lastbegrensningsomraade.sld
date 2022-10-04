<StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:se="http://www.opengis.net/se"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <se:Name>Lastbegrensningsområde</se:Name>
        <UserStyle>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>asfalt/annet, ingen vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#bfbfbf</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.00</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>asfalt, øvre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#b2df8a</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>asfalt, midtre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#a6cee3</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>asfalt, nedre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#fdbf6f</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>betong, ingen vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#636363</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>betong, øvre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#b2df8a</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#33a02c</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>betong, midtre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#a6cee3</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#1f78b4</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>betong, nedre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#fdbf6f</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#ff7f00</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>stein, ingen vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#636363</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#636363</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>stein, øvre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#b2df8a</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#33a02c</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#33a02c</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>stein, midtre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#a6cee3</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#1f78b4</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#1f78b4</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>stein, nedre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#fdbf6f</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#ff7f00</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#ff7f00</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>tredekke, ingen vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#636363</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>tredekke, øvre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#b2df8a</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#33a02c</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>tredekke, midtre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#a6cee3</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#1f78b4</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>tredekke, nedre vekt</se:Name>
                    <se:MaxScaleDenominator>10000.000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#fdbf6f</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e5031e</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#ff7f00</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

