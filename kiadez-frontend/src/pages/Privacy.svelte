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
      ? "Kiadez - Data Protection Policy"
      : isFr
        ? "Kiadez - Politique de protection des données"
        : "Kiadez - Política de Protección de Datos"}
  </title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card legal-content-card">
      <h1 class="content-title">
        {#if isEn}
          DATA PROTECTION POLICY
        {:else if isFr}
          POLITIQUE DE PROTECTION DES DONNÉES
        {:else}
          POLÍTICA DE PROTECCIÓN DE DATOS
        {/if}
      </h1>

      <div class="content-text legal-doc">
        {#if isEn}
          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Last updated: February 21, 2026<br />
            Responsible party: Carlos Jiménez Duarte
          </p>

          <h2>1. General Principle</h2>
          <p>
            Kiadez.com respects privacy as a core value.<br />
            The platform does not monetize data, does not sell information, and does not use behavioral profiling for
            commercial purposes.
          </p>

          <h2>2. Data Collected</h2>
          <p>Kiadez.com may collect:</p>
          <ul>
            <li>Username.</li>
            <li>Email address.</li>
            <li>Phone number (in case of verification).</li>
            <li>Information voluntarily published by the user.</li>
            <li>Basic technical logs required for operation (IP, access logs, security).</li>
          </ul>
          <p>No sensitive data is collected beyond what the user voluntarily decides to publish.</p>

          <h2>3. Purpose of Processing</h2>
          <p>Data is used exclusively for:</p>
          <ul>
            <li>Technical operation of the platform.</li>
            <li>Security and abuse prevention.</li>
            <li>Management of the Guardian system.</li>
            <li>Compliance with legal obligations.</li>
          </ul>
          <p>Data is not used for advertising, resale, or commercial studies.</p>

          <h2>4. Personal Private Key and Encryption</h2>
          <p>Information marked as private by the user may be stored in encrypted form.</p>
          <ul>
            <li>The private key is the sole responsibility of the user.</li>
            <li>The owner has no access to the key.</li>
            <li>If lost, encrypted content cannot be recovered.</li>
            <li>Kiadez.com is not responsible for data loss resulting from forgotten credentials.</li>
          </ul>

          <h2>5. Data Retention</h2>
          <p>Data is retained while the account remains active or as needed for:</p>
          <ul>
            <li>Legal compliance.</li>
            <li>Protection against potential claims.</li>
            <li>Community safety.</li>
          </ul>
          <p>The user may request account deletion.</p>

          <h2>6. User Rights</h2>
          <p>The user may:</p>
          <ul>
            <li>Request access to their data.</li>
            <li>Request correction.</li>
            <li>Request deletion.</li>
            <li>Request account closure.</li>
          </ul>
          <p>Requests must be sent through the official channels indicated on the platform.</p>

          <h2>7. Security</h2>
          <p>
            Reasonable technical and organizational security measures will be implemented.<br />
            However, no digital system guarantees absolute security.
          </p>

          <hr class="legal-divider" />

          <h2>2. UNDERAGE POLICY</h2>

          <h3>1. Access by Minors</h3>
          <p>Kiadez.com allows minors to register under the following conditions:</p>
          <ul>
            <li>The account remains with restricted visibility.</li>
            <li>Validation by a parent or legal guardian is required.</li>
          </ul>

          <h3>2. Verification</h3>
          <p>The minor must provide contact information for the responsible adult for validation.</p>
          <p>If false information is detected, the account may be suspended or permanently deleted.</p>

          <h3>3. Protection</h3>
          <ul>
            <li>Direct private interaction is not allowed.</li>
            <li>Requests for personal data are not allowed.</li>
            <li>Guardians must act with special caution in cases involving minors.</li>
          </ul>

          <h3>4. Responsibility</h3>
          <p>
            Supervision of the minor corresponds to the legal guardian.<br />
            Kiadez.com does not replace parental responsibility.
          </p>

          <hr class="legal-divider" />

          <h2>3. INTEGRITY PROTOCOL AND MISUSE PREVENTION</h2>
          <p>This document establishes preventive measures against:</p>
          <ul>
            <li>Money laundering.</li>
            <li>Emotional manipulation.</li>
            <li>Political or partisan use.</li>
            <li>Media exploitation of others' suffering.</li>
            <li>Coercive behavior.</li>
          </ul>

          <h3>1. General Principle</h3>
          <p>
            Kiadez.com does not act as a financial intermediary.<br />
            The platform does not collect money or manage funds between users.
          </p>

          <h3>2. Risk Signals (Alerts)</h3>
          <p>Internal review may be triggered by:</p>
          <ul>
            <li>Fulfillment offers outside official channels.</li>
            <li>Attempts to condition help on public exposure.</li>
            <li>Repeated use of the system for self-promotion.</li>
            <li>Contributions with opaque or unverifiable origin.</li>
            <li>Insistence on moving communications outside the platform.</li>
          </ul>

          <h3>3. Review Process</h3>
          <p>When a risk signal appears:</p>
          <ul>
            <li>Preventive case suspension.</li>
            <li>Review by the Integrity Committee (3 members).</li>
            <li>Request for additional information where applicable.</li>
            <li>Decision of approval, rejection, or cancellation.</li>
          </ul>

          <h3>4. Sanctions</h3>
          <p>The following may apply:</p>
          <ul>
            <li>Warning.</li>
            <li>Temporary suspension.</li>
            <li>Rank revocation.</li>
            <li>Permanent account deletion.</li>
            <li>Report to authorities if illegal activity is detected.</li>
          </ul>

          <h3>5. Internal Transparency</h3>
          <p>Any external merit accreditation must:</p>
          <ul>
            <li>Include verifiable evidence.</li>
            <li>Leave internal records.</li>
            <li>Be approved according to procedure.</li>
          </ul>
        {:else if isFr}
          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Dernière mise à jour : 21 février 2026<br />
            Responsable : Carlos Jiménez Duarte
          </p>

          <h2>1. Principe général</h2>
          <p>
            Kiadez.com respecte la vie privée comme une valeur fondamentale.<br />
            La plateforme ne monétise pas les données, ne vend pas d'informations et n'utilise pas de profilage
            comportemental à des fins commerciales.
          </p>

          <h2>2. Données collectées</h2>
          <p>Kiadez.com peut collecter :</p>
          <ul>
            <li>Nom d'utilisateur.</li>
            <li>Adresse e-mail.</li>
            <li>Numéro de téléphone (en cas de vérification).</li>
            <li>Informations publiées volontairement par l'utilisateur.</li>
            <li>Journaux techniques de base nécessaires au fonctionnement (IP, logs d'accès, sécurité).</li>
          </ul>
          <p>Aucune donnée sensible n'est collectée au-delà de ce que l'utilisateur décide de publier volontairement.</p>

          <h2>3. Finalité du traitement</h2>
          <p>Les données sont utilisées exclusivement pour :</p>
          <ul>
            <li>Le fonctionnement technique de la plateforme.</li>
            <li>La sécurité et la prévention des abus.</li>
            <li>La gestion du système des Gardiens.</li>
            <li>Le respect des obligations légales.</li>
          </ul>
          <p>Les données ne sont pas utilisées pour la publicité, la revente ou les études commerciales.</p>

          <h2>4. Clé Privée Personnelle et chiffrement</h2>
          <p>Les informations marquées comme privées par l'utilisateur peuvent être stockées sous forme chiffrée.</p>
          <ul>
            <li>La clé privée relève de la seule responsabilité de l'utilisateur.</li>
            <li>Le titulaire n'a aucun accès à la clé.</li>
            <li>En cas de perte, le contenu chiffré ne peut pas être récupéré.</li>
            <li>Kiadez.com n'est pas responsable des pertes de données dues à l'oubli des identifiants.</li>
          </ul>

          <h2>5. Conservation des données</h2>
          <p>Les données sont conservées tant que le compte reste actif ou lorsque nécessaire pour :</p>
          <ul>
            <li>Le respect de la loi.</li>
            <li>La protection contre d'éventuelles réclamations.</li>
            <li>La sécurité de la communauté.</li>
          </ul>
          <p>L'utilisateur peut demander la suppression de son compte.</p>

          <h2>6. Droits de l'utilisateur</h2>
          <p>L'utilisateur peut :</p>
          <ul>
            <li>Demander l'accès à ses données.</li>
            <li>Demander une correction.</li>
            <li>Demander une suppression.</li>
            <li>Demander la fermeture de son compte.</li>
          </ul>
          <p>Les demandes doivent être envoyées par les canaux officiels indiqués sur la plateforme.</p>

          <h2>7. Sécurité</h2>
          <p>
            Des mesures raisonnables de sécurité technique et organisationnelle seront mises en place.<br />
            Toutefois, aucun système numérique ne garantit une sécurité absolue.
          </p>

          <hr class="legal-divider" />

          <h2>2. POLITIQUE RELATIVE AUX MINEURS</h2>

          <h3>1. Accès des mineurs</h3>
          <p>Kiadez.com permet l'inscription des mineurs sous les conditions suivantes :</p>
          <ul>
            <li>Le compte reste avec une visibilité restreinte.</li>
            <li>Une validation par un parent ou tuteur légal est requise.</li>
          </ul>

          <h3>2. Vérification</h3>
          <p>Le mineur doit fournir les coordonnées de l'adulte responsable pour validation.</p>
          <p>En cas d'informations fausses, le compte peut être suspendu ou supprimé définitivement.</p>

          <h3>3. Protection</h3>
          <ul>
            <li>L'interaction privée directe n'est pas autorisée.</li>
            <li>La demande de données personnelles n'est pas autorisée.</li>
            <li>Les Gardiens doivent agir avec une prudence particulière dans les cas impliquant des mineurs.</li>
          </ul>

          <h3>4. Responsabilité</h3>
          <p>
            La supervision du mineur relève du tuteur légal.<br />
            Kiadez.com ne remplace pas la responsabilité parentale.
          </p>

          <hr class="legal-divider" />

          <h2>3. PROTOCOLE D'INTÉGRITÉ ET PRÉVENTION DES USAGES ABUSIFS</h2>
          <p>Ce document établit des mesures préventives contre :</p>
          <ul>
            <li>Le blanchiment d'argent.</li>
            <li>La manipulation émotionnelle.</li>
            <li>L'utilisation politique ou partisane.</li>
            <li>L'exploitation médiatique de la souffrance d'autrui.</li>
            <li>Les comportements coercitifs.</li>
          </ul>

          <h3>1. Principe général</h3>
          <p>
            Kiadez.com n'agit pas comme intermédiaire financier.<br />
            La plateforme ne collecte pas d'argent et ne gère pas de fonds entre utilisateurs.
          </p>

          <h3>2. Signaux de risque (alertes)</h3>
          <p>Une révision interne peut être déclenchée par :</p>
          <ul>
            <li>Des offres d'accomplissement en dehors des canaux officiels.</li>
            <li>Des tentatives de conditionner l'aide à une exposition publique.</li>
            <li>L'usage répété du système à des fins d'autopromotion.</li>
            <li>Des contributions à l'origine opaque ou non vérifiable.</li>
            <li>L'insistance à déplacer les communications hors de la plateforme.</li>
          </ul>

          <h3>3. Processus de révision</h3>
          <p>En présence d'un signal de risque :</p>
          <ul>
            <li>Suspension préventive du cas.</li>
            <li>Révision par le Comité d'Intégrité (3 membres).</li>
            <li>Demande d'informations complémentaires le cas échéant.</li>
            <li>Décision d'approbation, de rejet ou d'annulation.</li>
          </ul>

          <h3>4. Sanctions</h3>
          <p>Les mesures suivantes peuvent être appliquées :</p>
          <ul>
            <li>Avertissement.</li>
            <li>Suspension temporaire.</li>
            <li>Révocation du rang.</li>
            <li>Suppression définitive du compte.</li>
            <li>Signalement aux autorités en cas d'activité illégale détectée.</li>
          </ul>

          <h3>5. Transparence interne</h3>
          <p>Toute accréditation de mérite externe doit :</p>
          <ul>
            <li>Inclure des preuves vérifiables.</li>
            <li>Laisser une trace interne.</li>
            <li>Être approuvée conformément à la procédure.</li>
          </ul>
        {:else}
          <p class="legal-meta">
            <strong>Kiadez.com</strong><br />
            Última actualización: 21 de febrero de 2026<br />
            Responsable: Carlos Jiménez Duarte
          </p>

          <h2>1. Principio General</h2>
          <p>
            Kiadez.com respeta la privacidad como valor fundamental.<br />
            La plataforma no monetiza datos, no vende información y no utiliza perfiles conductuales para fines
            comerciales.
          </p>

          <h2>2. Datos Recopilados</h2>
          <p>Kiadez.com podrá recopilar:</p>
          <ul>
            <li>Nombre de usuario.</li>
            <li>Correo electrónico.</li>
            <li>Número telefónico (en caso de verificación).</li>
            <li>Información voluntariamente publicada por el usuario.</li>
            <li>Registros técnicos básicos necesarios para el funcionamiento (IP, logs de acceso, seguridad).</li>
          </ul>
          <p>No se recopilan datos sensibles más allá de lo que el usuario decida publicar voluntariamente.</p>

          <h2>3. Finalidad del Tratamiento</h2>
          <p>Los datos se utilizan exclusivamente para:</p>
          <ul>
            <li>Funcionamiento técnico de la plataforma.</li>
            <li>Seguridad y prevención de abuso.</li>
            <li>Gestión del sistema de Guardianes.</li>
            <li>Cumplimiento de obligaciones legales.</li>
          </ul>
          <p>No se utilizan para publicidad, venta ni estudios comerciales.</p>

          <h2>4. Clave Privada Personal y Cifrado</h2>
          <p>La información marcada como privada por el usuario podrá almacenarse mediante cifrado.</p>
          <ul>
            <li>La clave privada es responsabilidad exclusiva del usuario.</li>
            <li>El titular no tiene acceso a la clave.</li>
            <li>En caso de pérdida, el contenido cifrado no podrá recuperarse.</li>
            <li>Kiadez.com no será responsable por pérdida de información derivada del olvido de credenciales.</li>
          </ul>

          <h2>5. Conservación de Datos</h2>
          <p>Los datos se conservarán mientras la cuenta esté activa o mientras sea necesario para:</p>
          <ul>
            <li>Cumplimiento legal.</li>
            <li>Protección ante posibles reclamaciones.</li>
            <li>Seguridad de la comunidad.</li>
          </ul>
          <p>El usuario podrá solicitar la eliminación de su cuenta.</p>

          <h2>6. Derechos del Usuario</h2>
          <p>El usuario podrá:</p>
          <ul>
            <li>Solicitar acceso a sus datos.</li>
            <li>Solicitar corrección.</li>
            <li>Solicitar eliminación.</li>
            <li>Solicitar cierre de cuenta.</li>
          </ul>
          <p>Las solicitudes deberán enviarse por los canales oficiales indicados en la plataforma.</p>

          <h2>7. Seguridad</h2>
          <p>
            Se implementarán medidas razonables de seguridad técnica y organizativa.<br />
            No obstante, ningún sistema digital garantiza seguridad absoluta.
          </p>

          <hr class="legal-divider" />

          <h2>2. POLÍTICA DE MENORES DE EDAD</h2>

          <h3>1. Acceso de Menores</h3>
          <p>Kiadez.com permite el registro de menores de edad bajo las siguientes condiciones:</p>
          <ul>
            <li>La cuenta permanecerá con visibilidad restringida.</li>
            <li>Se requerirá acreditación por parte de padre, madre o tutor legal.</li>
          </ul>

          <h3>2. Verificación</h3>
          <p>El menor deberá proporcionar información de contacto del adulto responsable para validación.</p>
          <p>Si se detecta falsedad en la información, la cuenta podrá ser suspendida o eliminada definitivamente.</p>

          <h3>3. Protección</h3>
          <ul>
            <li>No se permite interacción privada directa.</li>
            <li>No se permite solicitud de datos personales.</li>
            <li>Los Guardianes deberán actuar con especial prudencia en casos que involucren menores.</li>
          </ul>

          <h3>4. Responsabilidad</h3>
          <p>
            La supervisión del menor corresponde al tutor legal.<br />
            Kiadez.com no sustituye la responsabilidad parental.
          </p>

          <hr class="legal-divider" />

          <h2>3. PROTOCOLO DE INTEGRIDAD Y PREVENCIÓN DE USO INDEBIDO</h2>
          <p>Este documento establece medidas preventivas contra:</p>
          <ul>
            <li>Lavado de activos.</li>
            <li>Manipulación emocional.</li>
            <li>Uso político o partidista.</li>
            <li>Explotación mediática del dolor ajeno.</li>
            <li>Conductas coercitivas.</li>
          </ul>

          <h3>1. Principio General</h3>
          <p>
            Kiadez.com no actúa como intermediario financiero.<br />
            La plataforma no recauda dinero ni gestiona fondos entre usuarios.
          </p>

          <h3>2. Señales de Riesgo (Alertas)</h3>
          <p>Podrán activar revisión interna:</p>
          <ul>
            <li>Ofertas de cumplimiento fuera del conducto oficial.</li>
            <li>Intentos de condicionar ayuda a exposición pública.</li>
            <li>Uso reiterado del sistema para autopromoción.</li>
            <li>Aportes con origen opaco o no verificable.</li>
            <li>Insistencia en trasladar comunicaciones fuera de la plataforma.</li>
          </ul>

          <h3>3. Proceso de Revisión</h3>
          <p>Ante señal de riesgo:</p>
          <ul>
            <li>Suspensión preventiva del caso.</li>
            <li>Revisión por el Comité de Integridad (3 miembros).</li>
            <li>Solicitud de información adicional si procede.</li>
            <li>Decisión de aprobación, rechazo o cancelación.</li>
          </ul>

          <h3>4. Sanciones</h3>
          <p>Podrán aplicarse:</p>
          <ul>
            <li>Advertencia.</li>
            <li>Suspensión temporal.</li>
            <li>Revocatoria de rango.</li>
            <li>Eliminación definitiva de cuenta.</li>
            <li>Reporte a autoridades si se detecta actividad ilegal.</li>
          </ul>

          <h3>5. Transparencia Interna</h3>
          <p>Toda acreditación de mérito externo deberá:</p>
          <ul>
            <li>Contar con evidencia verificable.</li>
            <li>Dejar registro interno.</li>
            <li>Ser aprobada conforme al procedimiento.</li>
          </ul>
        {/if}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
