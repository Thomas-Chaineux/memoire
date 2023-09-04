<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:foo="whatever"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output method="html" indent="yes"/>
    
    <xsl:variable name="edition_inventaire">
        <xsl:value-of select="concat('EDITION_INVENTAIRE_web_ID','.html')"/>
    </xsl:variable>
    
    <!-- ECRITURE DE FONCTIONS POUR EXTRAIRE DES CARACTERES D'UN ELEMENT <unitid> POUR CLASSER PAR ORDRE CROISSANT  -->
    <xsl:function name="foo:orderingByNumber_item" as="xs:integer">
        <xsl:param name="string" as="xs:string"/>
        <xsl:analyze-string select="$string" regex="[0-9]+$">
            <xsl:matching-substring>
                <xsl:sequence select="xs:integer(.)"></xsl:sequence>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>
    
    <xsl:function name="foo:extractLetters" as="xs:string">
        <xsl:param name="prefix" as="xs:string"/>
        <xsl:analyze-string select="$prefix" regex="^([A-Z]+)([0-9]+)">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(1)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>
    
    <xsl:function name="foo:extractNumbers" as="xs:string">
        <xsl:param name="prefix" as="xs:string"/>
        <xsl:analyze-string select="$prefix" regex="^([A-Z]+)([0-9]+)">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(2)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>
    
    
    
    <!-- Variable pour le head de l'HTML -->
    <xsl:variable name="head">
        <head>
            <title>Edition numérique de l'inventaire des archives de Varagnes</title>
            <meta name="author" content="Thomas Chaineux"></meta>
            <style>
                ul, #myUL {
                list-style-type: none;
                }
                
                #myUL {
                margin: 0;
                padding: 0;
                }
                
                .caret {
                cursor: pointer;
                -webkit-user-select: none; /* Safari 3.1+ */
                -moz-user-select: none; /* Firefox 2+ */
                -ms-user-select: none; /* IE 10+ */
                user-select: none;
                }
                
                .caret::before {
                content: "\25B6";
                color: black;
                display: inline-block;
                margin-right: 6px;
                }
                
                .caret-down::before {
                -ms-transform: rotate(90deg); /* IE 9 */
                -webkit-transform: rotate(90deg); /* Safari */'
                transform: rotate(90deg)  
                }
                
                .nested {
                display: none;
                }
                
                .active {
                display: block;
                }
            </style>
        </head>
    </xsl:variable>
    
    
    
    <xsl:template match="/">
        <xsl:call-template name="edition_inventaire"/>
    </xsl:template>
    
    <xsl:template name="edition_inventaire">
        <xsl:result-document href="{$edition_inventaire}" method="html">
            <html lang="fr">
                <xsl:copy-of select="$head"/>
                <body>
                    <xsl:for-each select="//c[@level='subfonds']">
                        <xsl:sort select="foo:extractLetters(did/unitid)" data-type="text"/>
                        <xsl:sort select="foo:extractNumbers(did/unitid)" data-type="number"/>
                        <ul>
                            <li>
                                <span class="caret">
                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>.</span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                
                                
                                
                                <!--LISTE AU NIVEAU DES SERIES-->
                                
                                <xsl:if test="./c[@level='series']">
                                    <ul class="nested">
                                        <xsl:for-each select="./c[@level='series']">
                                            <xsl:sort select="foo:extractLetters(did/unitid)" data-type="text"/>
                                            <xsl:sort select="foo:extractNumbers(did/unitid)" data-type="number"/>
                                            <xsl:choose>
                                                <!--S'il y a un élément c en dessous, affiche la flèche de déroulement; sinon, donne juste le nom-->
                                                <xsl:when test="./c">
                                                    
                                                    <li>
                                                        <span class="caret">
                                                            <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. 
                                                        </span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>  
                                                        
                                                        
                                                        <!--test si pièces-->
                                                        
                                                        <xsl:if test="./c[@level='item']">
                                                            <ul class="nested">
                                                                <xsl:for-each select="./c[@level='item']">
                                                                    <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                    <li>
                                                                        <xsl:value-of select="./did/unitid/text()"/>.
                                                                        <xsl:if test="./did/unittitle/title">
                                                                            <i><xsl:value-of select="./did/unittitle/title/text()"/></i>. 
                                                                        </xsl:if> 
                                                                        <xsl:value-of select="./did/unittitle/text()"/>.
                                                                        <xsl:if test="./did/unitdate">
                                                                            <xsl:value-of select="./did/unitdate/text()"/>. 
                                                                        </xsl:if>
                                                                        <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                    </li>
                                                                </xsl:for-each>
                                                            </ul>
                                                        </xsl:if>      
                                                        
                                                        <!--LISTE AU NIVEAU DES SOUS-SERIES-->
                                                        
                                                        <xsl:if test="./c[@level='subseries']">                                                
                                                            <ul class="nested">
                                                                <xsl:for-each select="./c[@level='subseries']">
                                                                    <xsl:sort select="foo:extractLetters(did/unitid)" data-type="text"/>
                                                                    <xsl:sort select="foo:extractNumbers(did/unitid)" data-type="number"/>
                                                                    <xsl:choose>
                                                                        <xsl:when test="./c">
                                                                            <li>
                                                                                <span class="caret">
                                                                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>.</span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                
                                                                                
                                                                                <!--test si pièces-->
                                                                                
                                                                                <xsl:if test="./c[@level='item']">
                                                                                    <ul class="nested">
                                                                                        <xsl:for-each select="./c[@level='item']">
                                                                                            <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                                            <li>
                                                                                                <xsl:value-of select="./did/unitid/text()"/>.
                                                                                                <xsl:if test="./did/unittitle/title">
                                                                                                    <i><xsl:value-of select="./did/unittitle/title/text()"/></i>. 
                                                                                                </xsl:if> 
                                                                                                <xsl:value-of select="./did/unittitle/text()"/>.
                                                                                                <xsl:if test="./did/unitdate">
                                                                                                    <xsl:value-of select="./did/unitdate/text()"/>. 
                                                                                                </xsl:if>
                                                                                                <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                            </li>
                                                                                        </xsl:for-each>
                                                                                    </ul>
                                                                                </xsl:if>
                                                                                
                                                                                
                                                                                
                                                                                <!--LISTE AU NIVEAU DES DOSSIERS-->
                                                                                
                                                                                <xsl:if test="./c[@level='file']">
                                                                                    <ul class="nested">
                                                                                        <xsl:for-each select="./c[@level='file']">
                                                                                            <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>                                                                                            
                                                                                            <xsl:choose>
                                                                                                <xsl:when test="./c">
                                                                                                    <li>
                                                                                                        <span class="caret">
                                                                                                            <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>.</span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                        
                                                                                                        
                                                                                                        <!--test si pièces-->
                                                                                                        
                                                                                                        <xsl:if test="./c[@level='item']">
                                                                                                            <ul class="nested">
                                                                                                                <xsl:for-each select="./c[@level='item']">
                                                                                                                    <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                                                                    <li>
                                                                                                                        <xsl:value-of select="./did/unitid/text()"/>.
                                                                                                                        <xsl:if test="./did/unittitle/title">
                                                                                                                            <i><xsl:value-of select="./did/unittitle/title/text()"/></i>. 
                                                                                                                        </xsl:if> 
                                                                                                                        <xsl:value-of select="./did/unittitle/text()"/>.
                                                                                                                        <xsl:if test="./did/unitdate">
                                                                                                                            <xsl:value-of select="./did/unitdate/text()"/>. 
                                                                                                                        </xsl:if>
                                                                                                                        <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                                    </li>
                                                                                                                </xsl:for-each>
                                                                                                            </ul>
                                                                                                        </xsl:if>
                                                                                                        
                                                                                                        
                                                                                                        
                                                                                                        <!--LISTE AU NIVEAU DES SOUS-DOSSIERS-->
                                                                                                        
                                                                                                        <xsl:if test="./c[@level='otherlevel' and @otherlevel='subfile']">   
                                                                                                            <ul class="nested">
                                                                                                                <xsl:for-each select="./c[@level='otherlevel' and @otherlevel='subfile']">
                                                                                                                    <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                                                                    
                                                                                                                    <xsl:choose>
                                                                                                                        <xsl:when test="./c">
                                                                                                                            <li>
                                                                                                                                <span class="caret">
                                                                                                                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>.</span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                                                
                                                                                                                                
                                                                                                                                <!--test si pièces-->
                                                                                                                                
                                                                                                                                <xsl:if test="./c[@level='item']">
                                                                                                                                    <ul class="nested">
                                                                                                                                        <xsl:for-each select="./c[@level='item']">
                                                                                                                                            <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                                                                                            <li>
                                                                                                                                                <xsl:value-of select="./did/unitid/text()"/>.
                                                                                                                                                <xsl:if test="./did/unittitle/title">
                                                                                                                                                    <i><xsl:value-of select="./did/unittitle/title/text()"/></i>. 
                                                                                                                                                </xsl:if> 
                                                                                                                                                <xsl:value-of select="./did/unittitle/text()"/>.
                                                                                                                                                <xsl:if test="./did/unitdate">
                                                                                                                                                    <xsl:value-of select="./did/unitdate/text()"/>. 
                                                                                                                                                </xsl:if>
                                                                                                                                                <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                                                            </li>
                                                                                                                                        </xsl:for-each>
                                                                                                                                    </ul>
                                                                                                                                </xsl:if>
                                                                                                                                
                                                                                                                                
                                                                                                                                
                                                                                                                                <!--LISTE AU NIVEAU DES SOUS-SOUS-DOSSIERS-->
                                                                                                                                
                                                                                                                                <xsl:if test="./c[@level='otherlevel' and @otherlevel='subsubfile']">
                                                                                                                                    <ul class="nested">
                                                                                                                                        <xsl:for-each select="./c[@level='otherlevel' and @otherlevel='subsubfile']">
                                                                                                                                            
                                                                                                                                            <xsl:choose>
                                                                                                                                                <xsl:when test="./c">
                                                                                                                                                    <li>
                                                                                                                                                        <span class="caret">
                                                                                                                                                            <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>
                                                                                                                                                            .</span> <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                                                                        
                                                                                                                                                        
                                                                                                                                                        <!--test si pièces-->
                                                                                                                                                        
                                                                                                                                                        <xsl:if test="./c[@level='item']">
                                                                                                                                                            <ul class="nested">
                                                                                                                                                                <xsl:for-each select="./c[@level='item']">
                                                                                                                                                                    <xsl:sort select="foo:orderingByNumber_item(did/unitid)" data-type="number"/>
                                                                                                                                                                    <li>
                                                                                                                                                                        <xsl:value-of select="./did/unitid/text()"/>.
                                                                                                                                                                        <xsl:if test="./did/unittitle/title">
                                                                                                                                                                            <i><xsl:value-of select="./did/unittitle/title/text()"/></i>. 
                                                                                                                                                                        </xsl:if> 
                                                                                                                                                                        <xsl:value-of select="./did/unittitle/text()"/>.
                                                                                                                                                                        <xsl:if test="./did/unitdate">
                                                                                                                                                                            <xsl:value-of select="./did/unitdate/text()"/>. 
                                                                                                                                                                        </xsl:if>
                                                                                                                                                                        <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a>
                                                                                                                                                                    </li>
                                                                                                                                                                </xsl:for-each>
                                                                                                                                                            </ul>
                                                                                                                                                        </xsl:if>
                                                                                                                                                    </li></xsl:when>
                                                                                                                                                <xsl:otherwise>
                                                                                                                                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a><br/>
                                                                                                                                                </xsl:otherwise>
                                                                                                                                            </xsl:choose>
                                                                                                                                        </xsl:for-each>
                                                                                                                                    </ul>
                                                                                                                                </xsl:if>
                                                                                                                            </li>
                                                                                                                        </xsl:when>
                                                                                                                        <xsl:otherwise>
                                                                                                                            <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a><br/>
                                                                                                                        </xsl:otherwise>
                                                                                                                    </xsl:choose>
                                                                                                                </xsl:for-each>
                                                                                                            </ul>
                                                                                                        </xsl:if>
                                                                                                    </li>
                                                                                                </xsl:when>
                                                                                                <xsl:otherwise>
                                                                                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a><br/>
                                                                                                </xsl:otherwise>
                                                                                            </xsl:choose>
                                                                                        </xsl:for-each>
                                                                                    </ul>
                                                                                </xsl:if>
                                                                            </li>
                                                                        </xsl:when>
                                                                        <xsl:otherwise>
                                                                            <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a><br/>
                                                                        </xsl:otherwise>
                                                                    </xsl:choose>
                                                                </xsl:for-each>
                                                            </ul>
                                                        </xsl:if>
                                                    </li>
                                                    
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="./did/unitid/text()"/>. <xsl:value-of select="./did/unittitle/text()"/>. <xsl:value-of select="./did/unitdate/text()"/>. <a href="https://epotec.univ-nantes.fr/s/seguin/item/{@id}">Vers la Base</a><br/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            
                                        </xsl:for-each>
                                    </ul>
                                </xsl:if>
                            </li>
                        </ul>
                    </xsl:for-each>
                </body>
                <script>
                    var toggler = document.getElementsByClassName("caret");
                    var i;
                    
                    for (i = 0; i &lt; toggler.length; i++) {
                    toggler[i].addEventListener("click", function() {
                    this.parentElement.querySelector(".nested").classList.toggle("active");
                    this.classList.toggle("caret-down");
                    });
                    }
                </script>
            </html>
        </xsl:result-document>
    </xsl:template>
    
</xsl:stylesheet>