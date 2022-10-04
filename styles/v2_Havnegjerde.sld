<StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:se="http://www.opengis.net/se"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <se:Name>Havnegjerde</se:Name>
        <UserStyle>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>Havnegjerde</se:Name>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Havnegjerde ikke-permanent</se:Name>
                    <se:MaxScaleDenominator>5000.000000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.00</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:GraphicStroke>
                                <se:Graphic>
                                    <se:Mark>
                                        <se:WellKnownName>circle</se:WellKnownName>
                                        <se:Fill>
                                            <se:SvgParameter name="fill">#f0f0f0</se:SvgParameter>
                                        </se:Fill>
                                    </se:Mark>
                                    <se:Size>5</se:Size>
                                </se:Graphic>
                            </se:GraphicStroke>
                            <se:SvgParameter name="stroke">#f0f0f0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">5.00</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:GraphicStroke>
                                <se:Graphic>
                                    <se:Mark>
                                        <se:WellKnownName>circle</se:WellKnownName>
                                        <se:Fill>
                                            <se:SvgParameter name="fill">#f0f0f0</se:SvgParameter>
                                        </se:Fill>
                                    </se:Mark>
                                    <se:Size>5</se:Size>
                                </se:Graphic>
                            </se:GraphicStroke>
                            <se:SvgParameter name="stroke">#f0f0f0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">5.00</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

