��    1      �  C   ,      8  �
  9  A   0     r  
   z     �     �  	   �     �  /   �     �                    &     3     @     N     [     n     {     �     �     �     �     �  	   �  
   �     �     �     �     �  )   �  0   &     W     \     b     g     w     �     �  *   �  8   �  !        #     )     B     `  E   l  L  �  �  �  +   �      !     !  $   ,!     Q!  
   p!     {!  ;   �!     �!     �!     �!     �!     �!     "     ""     4"     E"     \"  
   n"     y"     �"     �"     �"     �"     �"     �"     �"     �"     �"     �"  )   #  4   ;#     p#     x#     ~#     �#     �#     �#     �#  +   �#  8   $  !   A$     c$     i$     �$     �$  E   �$           	   
                                    "       .         &      %           -   1              )   ,   +                  '              $                       #         0      *            /                         !   (       
<div style="font-family: 'Lucida Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">

    <p>Hello ${object.partner_id.name},</p>

    <p>Thank you for purchasing</p>

    <p>Please find enclosed your invoice.</p>

    <p style="border-left: 1px solid #8e0000; margin-left: 30px;">
       &nbsp;&nbsp;<strong>REFERENCES</strong><br />
       &nbsp;&nbsp;Invoice number: <strong>${object.number}</strong><br />
       &nbsp;&nbsp;Invoice total: <strong>${object.amount_total} ${object.currency_id.name}</strong><br />
       &nbsp;&nbsp;Invoice date: ${object.date_invoice}<br />
       % if object.origin:
       &nbsp;&nbsp;Order reference: ${object.origin}<br />
       % endif
    </p>
    <br/>
    <p>Best Regards,</p>
    <p>Debonix</p>
    <br/>
    <br/>
    <div style="width: 375px; margin: 0px; padding: 0px; background-color: #8E0000; border-top-left-radius: 5px 5px; border-top-right-radius: 5px 5px; background-repeat: repeat no-repeat;">
        <h3 style="margin: 0px; padding: 2px 14px; font-size: 12px; color: #DDD;">
            <strong style="text-transform:uppercase;">${object.company_id.name}</strong></h3>
    </div>
    <div style="width: 347px; margin: 0px; padding: 5px 14px; line-height: 16px; background-color: #F2F2F2;">
        <span style="color: #222; margin-bottom: 5px; display: block; ">
        % if object.company_id.street:
            ${object.company_id.street}<br/>
        % endif
        % if object.company_id.street2:
            ${object.company_id.street2}<br/>
        % endif
        % if object.company_id.city or object.company_id.zip:
            ${object.company_id.zip} ${object.company_id.city}<br/>
        % endif
        % if object.company_id.country_id:
            ${object.company_id.state_id and ('%s, ' % object.company_id.state_id.name) or ''} ${object.company_id.country_id.name or ''}<br/>
        % endif
        </span>
        % if object.company_id.phone:
            <div style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; ">
                Phone:&nbsp; ${object.company_id.phone}
            </div>
        % endif
        % if object.company_id.email:
            <div style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; ">
                Email:&nbsp; ${object.company_id.email}
            </div>
        % endif
        % if object.company_id.website:
            <div>
                Web :&nbsp;<a href="${object.company_id.website}">${object.company_id.website}</a>
            </div>
        %endif
        <p></p>
    </div>
</div>

             ${object.company_id.name} Invoice (Ref ${object.number or 'n/a'}) Account Accounting Carrier Tracking Ref Cash on delivery Companies Customer Date of the first invoice generated for this SO Debonix Specific Configuration Group By... Host Invoice Invoice Date Invoice Line Invoice Lines Invoice SFTP No Unit of Measure Packing List Partner Password Path Picking List Port Product SMS Phone Sale Order Sale Order line Sales Order Sales Order Line Search Invoice Send an email with invoice after delivery Send an email with invoice and push it on a SFTP Shop Siret True Unit of Measure Username With carrier Without carrier Your invoice (reference: ${object.number}) account.group_account_user,product.group_product_manager account.statement.completion.rule dummy invoice_${object.number} product.group_product_manager res.company {'invisible': ['|',('picking_ids','=',False),('picking_ids','=',[])]} Project-Id-Version: OpenERP Server 7.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-06-19 13:54+0000
PO-Revision-Date: 2014-06-19 15:56+0100
Last-Translator: Guewen Baconnier <guewen.baconnier@camptocamp.com>
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: 
 <div style="font-family: 'Lucida Grande', Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF; ">

    <p>Bonjour,</p>

    <p>Nous vous remercions pour votre achat.</p>

    <p>Votre commande vient d'être expédiée, vous devriez la réceptionner sous un délai maximum de 48h.</p>

    <p>Veuillez trouver ci joint votre facture.</p>
    <p style="border-left: 1px solid #8e0000; margin-left: 30px;">
       &nbsp;&nbsp;<strong>REFERENCES</strong><br />
       &nbsp;&nbsp;Numéro de facture : <strong>${object.number}</strong><br />
       &nbsp;&nbsp;Total de la facture : <strong>${object.amount_total} ${object.currency_id.name}</strong><br />
       &nbsp;&nbsp;Date de facturation : ${object.date_invoice}<br />
       % if object.origin:
       &nbsp;&nbsp;Référence de la commande : ${object.origin}<br />
       % endif
    </p>
    <br/>
    <p>Cordialement</p>
    <p>Merci et à bientôt sur <a href="${object.company_id.website}">${object.company_id.website}</a></p>
    <br/>
    <br/>
    <div style="width: 375px; margin: 0px; padding: 0px; background-color: #8E0000; border-top-left-radius: 5px 5px; border-top-right-radius: 5px 5px; background-repeat: repeat no-repeat;">
        <h3 style="margin: 0px; padding: 2px 14px; font-size: 12px; color: #DDD;">
            <strong style="text-transform:uppercase;">DEBONIX</strong></h3>
    </div>
    <div style="width: 347px; margin: 0px; padding: 5px 14px; line-height: 16px; background-color: #F2F2F2;">
        <span style="color: #222; margin-bottom: 5px; display: block; ">
        % if object.company_id.street:
            ${object.company_id.street}<br/>
        % endif
        % if object.company_id.street2:
            ${object.company_id.street2}<br/>
        % endif
        % if object.company_id.city or object.company_id.zip:
            ${object.company_id.zip} ${object.company_id.city}<br/>
        % endif
        % if object.company_id.country_id:
            ${object.company_id.state_id and ('%s, ' % object.company_id.state_id.name) or ''} ${object.company_id.country_id.name or ''}<br/>
        % endif
        </span>
        % if object.company_id.phone:
            <div style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; ">
                Tél :&nbsp; ${object.company_id.phone}
            </div>
        % endif
        % if object.company_id.fax:
            <div style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; ">
                Fax : &nbsp; ${object.company_id.fax}
            </div>
        % endif
        % if object.company_id.email:
            <div style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; ">
                Email :&nbsp; ${object.company_id.email}
            </div>
        % endif
        % if object.company_id.website:
            <div>
                Web :&nbsp;<a href="${object.company_id.website}">${object.company_id.website}</a>
            </div>
        %endif
        <p></p>
    </div>
</div> Votre facture (reference: ${object.number}) Compte Comptabilité Référence de suivi du transporteur Livraison contre remboursement Sociétés Client Date de la première facture générée pour cette commande Debonix Specific Configuration Regrouper par... Hôte Facture Date de facturation Lignes de facture Lignes de facture Facture sur SFTP Pas d'unité de mesure Liste de colisage Partenaire Mot de passe Chemin Liste de colisage Port Produit Numéro SMS Commande client Ligne de commande Bon de commande Ligne de commande Recherche de facture Send an email with invoice after delivery Envoyer une facture par e-mail et la copier sur SFTP Magasin Siret True Unité de mesure Nom d'utilisateur Avec méthode de livraison Sans méthode de livraison Votre facture (reference: ${object.number}) account.group_account_user,product.group_product_manager account.statement.completion.rule dummy facture_${object.number} product.group_product_manager res.company {'invisible': ['|',('picking_ids','=',False),('picking_ids','=',[])]} 