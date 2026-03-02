<script>
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>
    {isEn
      ? "Kiadez - Terms and Conditions"
      : isFr
        ? "Kiadez - Termes et conditions"
        : "Kiadez - Términos y Condiciones"}
  </title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card legal-content-card">
      <h1 class="content-title">
        {#if isEn}
          GENERAL TERMS AND CONDITIONS OF USE
        {:else if isFr}
          CONDITIONS GÉNÉRALES D'UTILISATION
        {:else}
          TÉRMINOS Y CONDICIONES GENERALES DE USO
        {/if}
      </h1>

      <div class="content-text legal-doc">
        {#if isEn}
          <div class="legal-invite">
            <p>
              Almost no one reads terms and conditions. So I will summarize them for you, as a man of my word, so
              that you clearly understand what this social network is about, what my commitment is, and what I am
              willing to represent within the legal framework as well.
            </p>
            <p>If you want to read the human version, click here:</p>
            <div class="legal-actions">
              <a class="btn btn-primary btn-compact" href="/mygamerules.html">My game rules</a>
            </div>
          </div>

          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Last updated: February 21, 2026<br />
            Owner: Carlos Jiménez Duarte
          </p>

          <h2>1. Nature of the Service</h2>
          <p>
            Kiadez.com is a nonprofit digital platform created by Carlos Jiménez Duarte with the purpose of providing
            a space where users can express wishes, reflect on them, and participate in a community dynamic based on
            voluntary service.
          </p>
          <p>
            The platform does not constitute a religious, political, financial, therapeutic, or institutional
            organization, and it is not affiliated with any political party, government, church, or public/private
            entity.
          </p>

          <h2>2. Acceptance of the Terms</h2>
          <p>Accessing and using Kiadez.com implies full acceptance of these Terms and Conditions.</p>
          <p>If the user does not agree with these terms, they must refrain from using the platform.</p>

          <h2>3. Purpose and Scope</h2>
          <p>Kiadez.com allows users to:</p>
          <ul>
            <li>Publish public or private wishes.</li>
            <li>Interact through a symbolic system of stars and achievements.</li>
            <li>Request or channel voluntary help through the Guardian system.</li>
            <li>Use personal reflection tools such as the Oracle.</li>
          </ul>
          <p>Kiadez.com does not guarantee the fulfillment of any published wish.</p>

          <h2>4. No Professional Advice</h2>
          <p>The platform and its tools, including the Oracle, do not constitute:</p>
          <ul>
            <li>Psychological or psychiatric advice.</li>
            <li>Medical guidance.</li>
            <li>Legal advice.</li>
            <li>Financial advice.</li>
            <li>Professional counseling of any kind.</li>
          </ul>
          <p>
            Any decision made by the user based on published content or available tools is their sole responsibility.
          </p>

          <h2>5. User Relationships and Limitation of Liability</h2>
          <ul>
            <li>Wish fulfillments are voluntary actions between private individuals.</li>
            <li>Kiadez.com does not raise funds or act as a financial intermediary.</li>
            <li>The platform does not guarantee users' truthfulness, solvency, or intent.</li>
            <li>
              Kiadez.com assumes no responsibility for:
              <ul>
                <li>Noncompliance between users.</li>
                <li>Economic losses.</li>
                <li>Indirect or consequential damages.</li>
                <li>Unmet expectations.</li>
                <li>Personal conflicts arising from voluntary interactions.</li>
              </ul>
            </li>
            <li>
              Any relationship or agreement resulting from the use of the platform is carried out under the exclusive
              responsibility of the involved parties.
            </li>
          </ul>

          <h2>6. Disclaimer of Warranties</h2>
          <p>Kiadez.com is provided "as is" and subject to availability.</p>
          <p>There is no guarantee of:</p>
          <ul>
            <li>Uninterrupted operation.</li>
            <li>Absence of technical errors.</li>
            <li>Permanent service availability.</li>
            <li>Absolute security against external attacks.</li>
          </ul>

          <h2>7. Guardian System</h2>
          <ul>
            <li>The appointment of Guardians is a discretionary power of the owner.</li>
            <li>Ranks are symbolic and do not constitute legal authority.</li>
            <li>Failure to comply with the internal code may result in immediate revocation.</li>
            <li>A Guardian's participation does not make Kiadez.com a guarantor of fulfillment.</li>
          </ul>

          <h2>8. Prohibited Conduct</h2>
          <p>The following is prohibited:</p>
          <ul>
            <li>Publishing illegal content.</li>
            <li>Requesting personal data outside official channels.</li>
            <li>Using the platform for political or partisan purposes.</li>
            <li>Harassment or coercion.</li>
            <li>Attempting to use the platform for money laundering.</li>
            <li>Offering fulfillments outside the established system.</li>
            <li>Manipulating the stars or achievements system.</li>
          </ul>
          <p>Violations may result in suspension or permanent removal.</p>

          <h2>9. Stars and Achievements System</h2>
          <ul>
            <li>Stars have no economic value.</li>
            <li>They are non-refundable.</li>
            <li>They do not constitute an investment or property right.</li>
            <li>Achievements do not grant legal or economic privileges.</li>
            <li>Kiadez.com may modify the system when necessary.</li>
          </ul>

          <h2>10. Privacy and Security</h2>
          <ul>
            <li>Kiadez.com does not sell data to third parties.</li>
            <li>No advertising monetization systems are implemented.</li>
            <li>The user is responsible for protecting their credentials.</li>
            <li>The Personal Private Key is not accessible to the owner.</li>
            <li>If the key is lost, encrypted information cannot be recovered.</li>
            <li>Kiadez.com is not responsible for unauthorized access due to user negligence.</li>
          </ul>

          <h2>11. Force Majeure</h2>
          <p>Kiadez.com is not responsible for interruptions or damages resulting from:</p>
          <ul>
            <li>External server failures.</li>
            <li>Cyberattacks.</li>
            <li>Natural disasters.</li>
            <li>Electrical or connectivity failures.</li>
            <li>Any event beyond the owner's reasonable control.</li>
          </ul>

          <h2>12. Termination</h2>
          <p>The user may close their account at any time.</p>
          <p>Kiadez.com may suspend or remove accounts when:</p>
          <ul>
            <li>Serious noncompliance is detected.</li>
            <li>There is risk to the community.</li>
            <li>Essential principles of the project are violated.</li>
          </ul>

          <h2>13. Modifications</h2>
          <p>
            The owner may modify these terms whenever deemed necessary. Changes will take effect upon publication on
            the platform.
          </p>

          <h2>14. Law and Jurisdiction</h2>
          <p>These terms are governed by the law in force at the owner's domicile.</p>
          <p>Any dispute will be submitted to the corresponding competent jurisdiction.</p>
        {:else if isFr}
          <div class="legal-invite">
            <p>
              Presque personne ne lit les termes et conditions. Je vais donc te les résumer, en homme de parole, pour
              que tu comprennes clairement ce qu'est ce réseau social, quel est mon engagement et ce que je suis prêt
              à représenter aussi dans le cadre légal.
            </p>
            <p>Si tu veux lire la version humaine, clique ici :</p>
            <div class="legal-actions">
              <a class="btn btn-primary btn-compact" href="/mygamerules.html">Mes règles du jeu</a>
            </div>
          </div>

          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Dernière mise à jour : 21 février 2026<br />
            Titulaire : Carlos Jiménez Duarte
          </p>

          <h2>1. Nature du service</h2>
          <p>
            Kiadez.com est une plateforme numérique à but non lucratif créée par Carlos Jiménez Duarte dans le but
            d'offrir un espace où les utilisateurs peuvent exprimer des souhaits, y réfléchir et participer à une
            dynamique communautaire fondée sur le service volontaire.
          </p>
          <p>
            La plateforme ne constitue pas une organisation religieuse, politique, financière, thérapeutique ou
            institutionnelle, et n'est affiliée à aucun parti politique, gouvernement, église ou entité publique/privée.
          </p>

          <h2>2. Acceptation des conditions</h2>
          <p>L'accès et l'utilisation de Kiadez.com impliquent l'acceptation pleine des présentes conditions.</p>
          <p>Si l'utilisateur n'accepte pas ces conditions, il doit s'abstenir d'utiliser la plateforme.</p>

          <h2>3. Objet et portée</h2>
          <p>Kiadez.com permet de :</p>
          <ul>
            <li>Publier des souhaits publics ou privés.</li>
            <li>Interagir via un système symbolique d'étoiles et de réalisations.</li>
            <li>Demander ou canaliser une aide volontaire via le système des Gardiens.</li>
            <li>Utiliser des outils de réflexion personnelle comme l'Oracle.</li>
          </ul>
          <p>Kiadez.com ne garantit pas l'accomplissement d'un souhait publié.</p>

          <h2>4. Absence de conseil professionnel</h2>
          <p>La plateforme et ses outils, y compris l'Oracle, ne constituent pas :</p>
          <ul>
            <li>Un conseil psychologique ou psychiatrique.</li>
            <li>Une orientation médicale.</li>
            <li>Un conseil juridique.</li>
            <li>Un conseil financier.</li>
            <li>Un accompagnement professionnel de quelque nature que ce soit.</li>
          </ul>
          <p>
            Toute décision prise par l'utilisateur à partir des contenus publiés ou des outils disponibles relève de sa
            seule responsabilité.
          </p>

          <h2>5. Relations entre utilisateurs et limitation de responsabilité</h2>
          <ul>
            <li>Les accomplissements de souhaits sont des actes volontaires entre particuliers.</li>
            <li>Kiadez.com ne collecte pas de fonds et n'agit pas comme intermédiaire financier.</li>
            <li>La plateforme ne garantit ni la véracité, ni la solvabilité, ni l'intention des utilisateurs.</li>
            <li>
              Kiadez.com n'assume aucune responsabilité en cas de :
              <ul>
                <li>Non-respect entre utilisateurs.</li>
                <li>Pertes économiques.</li>
                <li>Dommages indirects ou consécutifs.</li>
                <li>Attentes non satisfaites.</li>
                <li>Conflits personnels issus d'interactions volontaires.</li>
              </ul>
            </li>
            <li>
              Toute relation ou tout accord découlant de l'usage de la plateforme se fait sous la responsabilité
              exclusive des parties impliquées.
            </li>
          </ul>

          <h2>6. Exclusion de garanties</h2>
          <p>Kiadez.com est fourni « tel quel » et selon disponibilité.</p>
          <p>Il n'est pas garanti :</p>
          <ul>
            <li>Un fonctionnement ininterrompu.</li>
            <li>L'absence d'erreurs techniques.</li>
            <li>La disponibilité permanente du service.</li>
            <li>Une sécurité absolue face aux attaques externes.</li>
          </ul>

          <h2>7. Système des Gardiens</h2>
          <ul>
            <li>La nomination des Gardiens est un pouvoir discrétionnaire du titulaire.</li>
            <li>Les rangs sont symboliques et ne constituent pas une autorité légale.</li>
            <li>Le non-respect du code interne peut entraîner une révocation immédiate.</li>
            <li>La participation d'un Gardien ne fait pas de Kiadez.com un garant de l'accomplissement.</li>
          </ul>

          <h2>8. Conduites interdites</h2>
          <p>Sont interdites :</p>
          <ul>
            <li>La publication de contenu illégal.</li>
            <li>La demande de données personnelles hors des canaux officiels.</li>
            <li>L'usage de la plateforme à des fins politiques ou partisanes.</li>
            <li>Le harcèlement ou la coercition.</li>
            <li>La tentative d'utiliser la plateforme pour le blanchiment d'argent.</li>
            <li>L'offre d'accomplissements en dehors du système établi.</li>
            <li>La manipulation du système d'étoiles ou de réalisations.</li>
          </ul>
          <p>Toute infraction peut entraîner une suspension ou une suppression définitive.</p>

          <h2>9. Système d'étoiles et de réalisations</h2>
          <ul>
            <li>Les étoiles n'ont aucune valeur économique.</li>
            <li>Elles ne sont pas remboursables.</li>
            <li>Elles ne constituent ni un investissement ni un droit patrimonial.</li>
            <li>Les réalisations n'accordent aucun privilège légal ou économique.</li>
            <li>Kiadez.com peut modifier le système lorsque nécessaire.</li>
          </ul>

          <h2>10. Confidentialité et sécurité</h2>
          <ul>
            <li>Kiadez.com ne vend pas de données à des tiers.</li>
            <li>Aucun système de monétisation publicitaire n'est implémenté.</li>
            <li>L'utilisateur est responsable de la protection de ses identifiants.</li>
            <li>La Clé Privée Personnelle n'est pas accessible au titulaire.</li>
            <li>En cas de perte de la clé, les informations chiffrées ne pourront pas être récupérées.</li>
            <li>Kiadez.com n'est pas responsable des accès non autorisés dus à la négligence de l'utilisateur.</li>
          </ul>

          <h2>11. Force majeure</h2>
          <p>Kiadez.com n'est pas responsable des interruptions ou dommages dus à :</p>
          <ul>
            <li>Des défaillances de serveurs externes.</li>
            <li>Des cyberattaques.</li>
            <li>Des catastrophes naturelles.</li>
            <li>Des pannes électriques ou de connectivité.</li>
            <li>Tout événement hors du contrôle raisonnable du titulaire.</li>
          </ul>

          <h2>12. Résiliation</h2>
          <p>L'utilisateur peut fermer son compte à tout moment.</p>
          <p>Kiadez.com peut suspendre ou supprimer des comptes lorsque :</p>
          <ul>
            <li>Un non-respect grave est détecté.</li>
            <li>Il existe un risque pour la communauté.</li>
            <li>Des principes essentiels du projet sont violés.</li>
          </ul>

          <h2>13. Modifications</h2>
          <p>
            Le titulaire peut modifier ces conditions lorsqu'il le juge nécessaire. Les modifications entreront en
            vigueur dès leur publication sur la plateforme.
          </p>

          <h2>14. Législation et juridiction</h2>
          <p>Ces conditions sont régies par la législation en vigueur au domicile du titulaire.</p>
          <p>Tout litige sera soumis à la juridiction compétente correspondante.</p>
        {:else}
          <div class="legal-invite">
            <p>
              Casi nadie lee los términos y condiciones. Así que te los voy a resumir, como hombre de palabra que soy,
              para que entiendas bien de qué va esta red social, cuál es mi compromiso y qué estoy dispuesto a
              representar también dentro de los términos legales.
            </p>
            <p>Si quieres leer esta versión, da clic aquí:</p>
            <div class="legal-actions">
              <a class="btn btn-primary btn-compact" href="/mygamerules.html">Mis reglas de juego</a>
            </div>
          </div>

          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Última actualización: 21 de febrero de 2026<br />
            Titular: Carlos Jiménez Duarte
          </p>

          <h2>1. Naturaleza del Servicio</h2>
          <p>
            Kiadez.com es una plataforma digital sin ánimo de lucro creada por Carlos Jiménez Duarte con el propósito
            de ofrecer un espacio donde los usuarios puedan expresar deseos, reflexionar sobre ellos y participar en
            una dinámica comunitaria basada en el servicio voluntario.
          </p>
          <p>
            La plataforma no constituye una organización religiosa, política, financiera, terapéutica ni institucional,
            ni se encuentra afiliada a partido político, gobierno, iglesia o entidad pública o privada.
          </p>

          <h2>2. Aceptación de los Términos</h2>
          <p>El acceso y uso de Kiadez.com implica la aceptación plena de los presentes Términos y Condiciones.</p>
          <p>Si el usuario no está de acuerdo con estos términos, deberá abstenerse de utilizar la plataforma.</p>

          <h2>3. Objeto y Alcance</h2>
          <p>Kiadez.com permite:</p>
          <ul>
            <li>Publicar deseos públicos o privados.</li>
            <li>Interactuar mediante un sistema simbólico de estrellas y logros.</li>
            <li>Solicitar o canalizar ayuda voluntaria a través del sistema de Guardianes.</li>
            <li>Utilizar herramientas de reflexión personal como el Oráculo.</li>
          </ul>
          <p>Kiadez.com no garantiza el cumplimiento de ningún deseo publicado.</p>

          <h2>4. Ausencia de Asesoría Profesional</h2>
          <p>La plataforma y sus herramientas, incluyendo el Oráculo, no constituyen:</p>
          <ul>
            <li>Asesoría psicológica o psiquiátrica.</li>
            <li>Orientación médica.</li>
            <li>Asesoría jurídica.</li>
            <li>Asesoría financiera.</li>
            <li>Consejería profesional de ningún tipo.</li>
          </ul>
          <p>
            Cualquier decisión adoptada por el usuario a partir de contenidos publicados o herramientas disponibles es
            de su exclusiva responsabilidad.
          </p>

          <h2>5. Relaciones entre Usuarios y Limitación de Responsabilidad</h2>
          <ul>
            <li>Los cumplimientos de deseos son actos voluntarios entre particulares.</li>
            <li>Kiadez.com no recauda fondos ni actúa como intermediario financiero.</li>
            <li>La plataforma no garantiza la veracidad, solvencia o intención de los usuarios.</li>
            <li>
              Kiadez.com no asume responsabilidad por:
              <ul>
                <li>Incumplimientos entre usuarios.</li>
                <li>Pérdidas económicas.</li>
                <li>Daños indirectos o consecuenciales.</li>
                <li>Expectativas no cumplidas.</li>
                <li>Conflictos personales derivados de interacciones voluntarias.</li>
              </ul>
            </li>
            <li>
              Toda relación o acuerdo derivado del uso de la plataforma se realiza bajo la exclusiva responsabilidad de
              las partes involucradas.
            </li>
          </ul>

          <h2>6. Exención de Garantías</h2>
          <p>Kiadez.com se proporciona "tal cual" y según disponibilidad.</p>
          <p>No se garantiza:</p>
          <ul>
            <li>Funcionamiento ininterrumpido.</li>
            <li>Ausencia de errores técnicos.</li>
            <li>Disponibilidad permanente del servicio.</li>
            <li>Seguridad absoluta frente a ataques externos.</li>
          </ul>

          <h2>7. Sistema de Guardianes</h2>
          <ul>
            <li>El nombramiento de Guardianes es una facultad discrecional del titular.</li>
            <li>Los rangos tienen carácter simbólico y no constituyen autoridad legal.</li>
            <li>El incumplimiento del código interno podrá implicar revocación inmediata.</li>
            <li>La participación de un Guardián no convierte a Kiadez.com en garante del cumplimiento.</li>
          </ul>

          <h2>8. Conductas Prohibidas</h2>
          <p>Se prohíbe:</p>
          <ul>
            <li>Publicar contenido ilegal.</li>
            <li>Solicitar datos personales fuera del conducto oficial.</li>
            <li>Utilizar la plataforma con fines políticos o partidistas.</li>
            <li>Generar acoso o coerción.</li>
            <li>Intentar utilizar la plataforma para lavado de activos.</li>
            <li>Ofrecer cumplimientos por fuera del sistema establecido.</li>
            <li>Manipular el sistema de estrellas o logros.</li>
          </ul>
          <p>La infracción podrá implicar suspensión o eliminación definitiva.</p>

          <h2>9. Sistema de Estrellas y Logros</h2>
          <ul>
            <li>Las estrellas no poseen valor económico.</li>
            <li>No son reembolsables.</li>
            <li>No constituyen inversión ni derecho patrimonial.</li>
            <li>Los logros no otorgan privilegios legales ni económicos.</li>
            <li>Kiadez.com podrá modificar el sistema cuando sea necesario.</li>
          </ul>

          <h2>10. Privacidad y Seguridad</h2>
          <ul>
            <li>Kiadez.com no vende datos a terceros.</li>
            <li>No se implementan sistemas de monetización publicitaria.</li>
            <li>El usuario es responsable de proteger sus credenciales.</li>
            <li>La Clave Privada Personal no es accesible por el titular.</li>
            <li>En caso de pérdida de la clave, la información cifrada no podrá recuperarse.</li>
            <li>Kiadez.com no será responsable por accesos indebidos derivados de negligencia del usuario.</li>
          </ul>

          <h2>11. Fuerza Mayor</h2>
          <p>Kiadez.com no será responsable por interrupciones o daños derivados de:</p>
          <ul>
            <li>Fallos de servidores externos.</li>
            <li>Ataques cibernéticos.</li>
            <li>Desastres naturales.</li>
            <li>Fallos eléctricos o de conectividad.</li>
            <li>Cualquier evento fuera del control razonable del titular.</li>
          </ul>

          <h2>12. Terminación</h2>
          <p>El usuario podrá cerrar su cuenta en cualquier momento.</p>
          <p>Kiadez.com podrá suspender o eliminar cuentas cuando:</p>
          <ul>
            <li>Se detecte incumplimiento grave.</li>
            <li>Exista riesgo para la comunidad.</li>
            <li>Se vulneren principios esenciales del proyecto.</li>
          </ul>

          <h2>13. Modificaciones</h2>
          <p>
            El titular podrá modificar estos términos cuando lo considere necesario. Las modificaciones entrarán en
            vigor desde su publicación en la plataforma.
          </p>

          <h2>14. Legislación y Jurisdicción</h2>
          <p>Estos términos se rigen por la legislación vigente en el domicilio del titular.</p>
          <p>Cualquier controversia será sometida a la jurisdicción competente correspondiente.</p>
        {/if}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
