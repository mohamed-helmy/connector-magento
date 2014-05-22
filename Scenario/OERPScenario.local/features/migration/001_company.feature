@debonix  @migration  @company

Feature: Define report configs

  @report
  Scenario: Define rml report header to remove "Generated by OpenERP.com"
    Given I execute the SQL commands
    """
    UPDATE res_company SET rml_header = ''
    '<header>
         <pageTemplate>
            <frame id="first" x1="1.3cm" y1="3.0cm" height="21.7cm" width="19.0cm"/>
             <stylesheet>
                <!-- Set here the default font to use for all <para> tags -->
                <paraStyle name=''Normal'' fontName="DejaVu Sans"/>
                <paraStyle name="main_footer" fontSize="8.0" alignment="CENTER"/>
                <paraStyle name="main_header" fontSize="8.0" leading="10" alignment="LEFT" spaceBefore="0.0" spaceAfter="0.0"/>
             </stylesheet>
            <pageGraphics>
                <!-- Set here the default font to use for all <drawString> tags -->
                <setFont name="DejaVu Sans" size="8"/>
                <!-- You Logo - Change X,Y,Width and Height -->
                <image x="1.3cm" y="27.7cm" height="40.0" >[[ company.logo or removeParentNode(''image'') ]]</image>
                <fill color="black"/>
                <stroke color="black"/>
     
                <!-- page header -->
                <lines>1.3cm 27.7cm 20cm 27.7cm</lines>
                <drawRightString x="20cm" y="27.8cm">[[ company.rml_header1 ]]</drawRightString>
                <drawString x="1.3cm" y="27.3cm">[[ company.partner_id.name ]]</drawString>
                <place x="1.3cm" y="25.3cm" height="1.8cm" width="15.0cm">
                    <para style="main_header">[[ display_address(company.partner_id) or  '''' ]]</para>
                </place>
                <drawString x="1.3cm" y="25.0cm">Phone:</drawString>
                <drawRightString x="7cm" y="25.0cm">[[ company.partner_id.phone or '''' ]]</drawRightString>
                <drawString x="1.3cm" y="24.6cm">Mail:</drawString>
                <drawRightString x="7cm" y="24.6cm">[[ company.partner_id.email or '''' ]]</drawRightString>
                <lines>1.3cm 24.5cm 7cm 24.5cm</lines>
     
                <!--page bottom-->
                <lines>1.2cm 2.65cm 19.9cm 2.65cm</lines>
                <place x="1.3cm" y="0cm" height="2.55cm" width="19.0cm">
                    <para style="main_footer">[[ company.rml_footer ]]</para>
                    <para style="main_footer">Contact : [[ user.name ]] - Page: <pageNumber/></para>
                </place>
            </pageGraphics>
        </pageTemplate>
    </header>' WHERE name = 'Debonix France SAS'
    """
