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
      ? "Kiadez - My Game Rules"
      : isFr
        ? "Kiadez - Mes règles du jeu"
        : "Kiadez - Mis Reglas de Juego"}
  </title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card legal-content-card">
      <h1 class="content-title">
        {isEn
          ? "My Game Rules and Purpose Document"
          : isFr
            ? "Mes règles du jeu et document de finalité"
            : "Mis Reglas de Juego y Documento de Propósito"}
      </h1>

      <div class="content-text legal-doc">
        {#if isEn}
          <p class="legal-meta">
            <em>Terms and Conditions - human version</em><br />
            Written by Carlos Jiménez Duarte<br />
            February 21, 2026
          </p>

          <p>
            These game rules are easy to read because they are written under oath, with the sincerity of someone who
            wants to clearly present what this project represents by publishing Kiadez.com as a social network
            accessible to everyone.
          </p>

          <p>
            Almost no one reads terms and conditions. So I will summarize them for you, as a man of my word, so that
            you understand what this social network is about, what my commitment is, and what I am willing to represent
            within legal terms.
          </p>

          <p>It is my social network, therefore it operates with my structure and my rules. In short:</p>

          <h2>About the Essence of Kiadez</h2>
          <ul>
            <li>
              This is not a religious social network. I do not seek proselytism around the life of Jesus by placing him
              as one of the main Guardians of Kiadez.com.
            </li>
            <li>If you are atheist, Muslim, Jewish, or belong to any other religion, you are fully welcome.</li>
            <li>
              Kiadez.com defends individual freedom as a core principle. If, among your public or private wishes, you
              want to publish that you long to be a womanizer or an erotic literature writer, there will be no Catholic
              or Christian morality judging you. As the founder of this network, based on my own spiritual journey, I
              give you my word that God does not judge your heart; he simply loves you as you are.
            </li>
            <li>
              Kiadez.com, represented by me, rejects as an organization and/or movement any connection with political
              parties, national or international governments.<br />
              "Render unto Caesar what is Caesar's, and unto God what is God's" (Matthew 22:21).
            </li>
            <li>
              This social network was born as a medium to channel your energy, your creative will, and your desire for
              self-realization. But that does not imply that Kiadez.com is committed to working directly or indirectly
              on fulfilling your wish.<br />
              Publishing your wish - from experience - aligns your thinking with what you truly seek and helps you
              recognize where you are heading. Not knowing where you are walking is likely one of the greatest evils
              humanity has faced since its origin.
            </li>
            <li>
              If this social network starts to frustrate your emotions, if seeing your wishes unfulfilled affects your
              expectations, the sincerest suggestion is that you close your account. You may leave at any time.
            </li>
            <li>
              My dream is that we share Life; that we show how we focus our energy day by day, and that this keeps us
              inspired. The social network then becomes a community channel to leave the impossible aside and create
              content that stimulates us toward a concrete direction: consistency between what we dream and what we
              live.
            </li>
          </ul>

          <h2>About the Guardians</h2>
          <ul>
            <li>Currently, I, Carlos Jiménez Duarte, present myself as the first and only Guardian of Kiadez.com.</li>
            <li>
              The scope of this project aspires to a future where a real organization of Guardians exists, with the
              mission of serving as intermediaries between those who can help fulfill the wishes of others.
            </li>
            <li>
              The Philosophy of the Good Guardian makes it clear that every Guardian is first and foremost a servant:
              someone whose main interest is serving others, without expecting recognition or influencing people. The
              Guardian does not seek display, emotional marketing, or influencer status.
            </li>
            <li>
              The hierarchy system seeks to establish a philosophy of respect. It is inspired by traditional academy
              structures, especially Hap Ki Do philosophy, where order and discipline are pursued.<br />
              Remember:<br />
              <strong>"The higher the rank, the more invisible the ego."</strong>
            </li>
            <li>
              In Kiadez.com, some people may obtain the Guardian rank without exclusively following the traditional path
              of granting wishes one by one. This refers to proven merit. Metaphors related to Jesus' life - such as
              raising Lazarus or multiplying loaves - illustrate the type of merit that may justify accreditation.<br />
              However, I, Carlos Jiménez Duarte, decide whether a person's life achievement is sufficient to accredit
              their rank in this social network.<br />
              If you can fly, had a revealing vision after a night of drinking, or saved a thousand people from a fire,
              that does not automatically grant you the right to become one of my Guardians. The rank is granted to
              those who truly deserve and represent it.
            </li>
            <li>
              Holding the title of Guardian represents a lifelong commitment: to yourself, to the community, and to the
              Supreme Absolute Guardian (God). To preserve that rank, consistency is essential.
            </li>
            <li>
              Becoming a Guardian is a possible destiny for anyone. The history of fulfilled and accredited wishes in
              the official Kiadez.com counter is valued.<br />
              This model can be replicated at home, with family and friends, by keeping your own fulfilled-wishes
              count. That is valid and dignified. However, for now, I am not committed to using those external counts
              as an automatic reference to link someone as an official Guardian.
            </li>
          </ul>

          <h2>About Wish Fulfillment</h2>
          <ul>
            <li>Anyone may approach a Guardian to fulfill another person's wish.</li>
            <li>Wishes may be fulfilled anonymously or with public record of who helped.</li>
            <li>Offering help does not automatically guarantee your participation will be accepted.</li>
            <li>
              When someone decides to collaborate, a serious audit process begins to recognize their intentions.
            </li>
            <li>
              This process ensures that:
              <ul>
                <li>The contributor expects no reward other than the satisfaction of serving.</li>
                <li>They do not seek coercion, manipulation, or emotional debt.</li>
                <li>They do not seek emotional marketing.</li>
                <li>They do not seek political, religious, or institutional influence.</li>
                <li>They know and accept the Philosophy of the Good Guardian.</li>
              </ul>
            </li>
            <li>
              The person receiving the wish acquires no moral commitment beyond sincere gratitude. Wish granting will
              not be used as manipulation, friendship purchase, or relational coercion.
            </li>
            <li>
              The person receiving the wish remains fully free. They acquire no debt with Kiadez.com nor with the one
              who granted the good or service.
            </li>
          </ul>

          <h2>About the Oracle</h2>
          <ul>
            <li>
              The Oracle is a personal reflection tool. It is not for predicting the future or changing the past; only
              for assimilating it.
            </li>
            <li>Its goal is to help you recognize which forces and ideas predominate in your mind.</li>
            <li>It does not replace professional psychological care.</li>
            <li>It can be published or kept private through the Personal Private Key.</li>
          </ul>

          <h2>About Stars and Achievements</h2>
          <ul>
            <li>Users can earn stars through their posts.</li>
            <li>Stars cannot be withdrawn once granted.</li>
            <li>
              If a user deletes posts, associated stars will be deducted, along with achievements unlocked through them.
            </li>
            <li>
              Donating stars to the Common Pool generates no financial compensation or privileges. It is a symbolic act
              of detachment.
            </li>
            <li>
              Achievements grant no privileges within the platform, except the possibility of profile suggestion in the
              followers section.
            </li>
          </ul>

          <h2>About Privacy</h2>
          <ul>
            <li>
              I do not conduct analytical monitoring for commercial purposes. As of February 21, 2026, I give my word
              that I will not sell data or use information for commercial purposes.
            </li>
            <li>
              Minors can create accounts, but their information remains private until accredited by a legal guardian.
              Lying in this process may lead to permanent suspension.
            </li>
            <li>
              The Personal Private Key is designed to protect encrypted user information. I have no access to that key
              or encrypted content. Kiadez.com will never request this password.
            </li>
            <li>The algorithm is not designed to generate addiction.</li>
            <li>
              There will be no ads or institutional accounts. This social network is designed for people, not brands.
            </li>
          </ul>

          <h2>User Commitments</h2>
          <ul>
            <li>Publishing illegal content may result in reporting and suspension.</li>
            <li>Abusing the system to manipulate stars or achievements may result in suspension.</li>
            <li>Fulfilled wishes must be marked under oath of truth.</li>
            <li>Digital bullying is not allowed.</li>
          </ul>

          <hr class="legal-divider" />

          <h2>Purpose Document</h2>
          <p class="legal-meta">
            Kiadez.com<br />
            Foundational Conceptual Basis
          </p>

          <h3>1. What the Project Is</h3>
          <p>Someone once said this social network looked more like a personal diary. They were not wrong.</p>
          <p>
            Kiadez.com, in its deepest essence, is a conscious diary. It was born from the idea that users learn to
            know themselves, to recognize the magnitude of their wishes, both those they can affirm publicly and those
            they prefer to keep private.
          </p>
          <p>That is the essence of the project.</p>
          <p>
            Creating daily content is not a race for visibility, but a search for alignment with what you truly want.
            It is a way to show Life that you are sincere with your path and long to be consistent between what you
            aspire to achieve and what you live day by day.
          </p>
          <p>Kiadez.com is not born from noise, but from purpose.</p>

          <h3>2. What the Project Is Not</h3>
          <p>Kiadez.com is not a platform designed to guarantee the fulfillment of your wishes.</p>
          <p>
            It is not a company that promises results.<br />
            It is not a magical manifestation system.<br />
            It is not a success contract.
          </p>
          <p>
            It is offered as a channel for you to honestly express what you want, but it does not commit to working on
            your behalf or intervening directly in achieving your goals.
          </p>
          <p>
            There is an alternative service, structured around the Guardian system, which can mediate when some users
            choose to share their generosity. However, this service does not constitute any guarantee that exposing your
            wish will make it come true as you imagine.
          </p>
          <p>Publishing a wish does not force the world to grant it.</p>

          <h3>3. Real Scope</h3>
          <p>Kiadez.com is a bridge.</p>
          <p>
            A sincere bridge between those who can help - whether through economic means or voluntary service - and
            those who dare to believe in their own dreams.
          </p>
          <p>But the true scope of the project is not in the external act of fulfillment.</p>
          <p>It is in the internal process of recognition.</p>
          <p>
            The true scope is that the user contemplates daily what they desire and observes whether that sincere
            visualization is reflected in their conduct, their content, and their life.
          </p>
          <p>
            If someone intervenes to help you, let it be a consequence.<br />
            But the center will always be your consistency.
          </p>

          <h3>4. Limits</h3>
          <p>Kiadez.com defends individual freedom as a fundamental principle of human identity.</p>
          <p>However, all freedom implies responsibility toward your environment and toward others.</p>
          <p>
            You are free to express your wishes, public or private, as long as content remains within respect and legal
            limits applicable internationally, considering this is a social network open to the world.
          </p>
          <p>
            The teaching and life of Master Jesus are presented as one of the inspiring axes of the project. However,
            this does not make Kiadez.com a religious or political platform.
          </p>
          <p>
            There is no intention of proselytism or colonization of others' thinking.<br />
            Whatever your spiritual or philosophical conviction, you are welcome.
          </p>

          <h3>5. Responsibilities</h3>
          <p>
            Each user is responsible for their content and the sincerity with which they act within the social network.
          </p>
          <p>
            By publishing a wish, the user declares it reflects an authentic search.<br />
            By marking a wish as fulfilled, they do so under the principle of truth.
          </p>
          <p>Kiadez.com embraces the universal value of the given word as the foundation of coexistence.</p>
          <p>The platform does not police the user's conscience. It trusts it.</p>
        {:else if isFr}
          <p class="legal-meta">
            <em>Termes et conditions - version humaine</em><br />
            Rédigées par Carlos Jiménez Duarte<br />
            21 février 2026
          </p>

          <p>
            Ces règles du jeu sont faciles à lire parce qu'elles sont écrites sous serment de vérité, avec la sincérité
            de quelqu'un qui souhaite exposer clairement ce que représente son projet en publiant Kiadez.com comme un
            réseau social accessible à tous.
          </p>

          <p>
            Presque personne ne lit les termes et conditions. Je vais donc te les résumer, en homme de parole, pour que
            tu comprennes bien ce qu'est ce réseau social, quel est mon engagement et ce que je suis prêt à représenter
            également dans le cadre légal.
          </p>

          <p>C'est mon réseau social, il fonctionne donc avec ma structure et mes règles. En résumé :</p>

          <h2>Sur l'essence de Kiadez</h2>
          <ul>
            <li>
              Ce n'est pas un réseau social religieux. Je ne cherche pas à faire du prosélytisme autour de la vie de
              Jésus en le plaçant comme l'un des principaux Gardiens de Kiadez.com.
            </li>
            <li>Si tu es athée, musulman, juif ou d'une autre religion, tu es pleinement le bienvenu.</li>
            <li>
              Kiadez.com défend la liberté individuelle comme principe fondamental. Si tu souhaites publier, parmi tes
              souhaits publics ou privés, que tu veux être séducteur ou écrivain de littérature érotique, il n'y aura
              aucune morale catholique ou chrétienne pour te juger. En tant que fondateur de ce réseau social, en me
              basant sur mon propre parcours spirituel, je te donne ma parole que Dieu ne juge pas ton coeur ; il t'aime
              simplement tel que tu es.
            </li>
            <li>
              Kiadez.com, représenté par moi, rejette en tant qu'organisation et/ou mouvement tout lien avec des partis
              politiques, des gouvernements nationaux ou internationaux.<br />
              "Rendez à César ce qui est à César, et à Dieu ce qui est à Dieu" (Matthieu 22:21).
            </li>
            <li>
              Ce réseau social est né comme un moyen de canaliser ton énergie, ta volonté créative et ton désir de te
              réaliser. Mais cela n'implique pas que Kiadez.com ait l'engagement de travailler directement ou
              indirectement à la réalisation de ton souhait.<br />
              Publier ton souhait - je le dis par expérience - aligne ta pensée avec ce que tu cherches vraiment et
              t'aide à reconnaître vers où tu te diriges. Ne pas savoir où l'on va est probablement l'un des plus grands
              maux auxquels l'humanité est confrontée depuis son origine.
            </li>
            <li>
              Si ce réseau social commence à frustrer tes émotions, si voir que tes souhaits ne s'accomplissent pas
              affecte tes attentes, la suggestion la plus sincère est de fermer ton compte. Tu peux partir à tout moment.
            </li>
            <li>
              Mon rêve est que nous partagions la Vie ; que nous montrions comment nous orientons notre énergie au
              quotidien et que cela nous maintienne inspirés. Le réseau social devient alors un canal communautaire pour
              laisser de côté l'impossible et créer du contenu qui nous stimule vers une direction concrète : la
              cohérence entre ce que nous rêvons et ce que nous vivons.
            </li>
          </ul>

          <h2>Sur les Gardiens</h2>
          <ul>
            <li>
              Actuellement, moi, Carlos Jiménez Duarte, je me présente comme le premier et unique Gardien de Kiadez.com.
            </li>
            <li>
              La portée de ce projet aspire à ce qu'à l'avenir existe une véritable organisation de Gardiens dont la
              mission soit de servir d'intermédiaires entre ceux qui peuvent aider à accomplir les souhaits d'autres
              personnes.
            </li>
            <li>
              La Philosophie du Bon Gardien précise que tout Gardien est avant tout un serviteur : une personne dont
              l'intérêt principal est d'être au service des autres, sans attendre de reconnaissance ni influencer autrui.
              Le Gardien ne s'exhibe pas, ne cherche pas le marketing émotionnel et n'aspire pas à devenir influenceur.
            </li>
            <li>
              Le système de hiérarchies cherche à établir une philosophie du respect. Il est inspiré de la structure
              traditionnelle des académies, en particulier de la philosophie Hap Ki Do, où l'on recherche ordre et
              discipline.<br />
              Souviens-toi :<br />
              <strong>"Plus le rang est élevé, plus l'ego est invisible."</strong>
            </li>
            <li>
              Sur Kiadez.com, certaines personnes peuvent obtenir le rang de Gardien sans suivre exclusivement le chemin
              traditionnel consistant à accomplir les souhaits un par un. Cela fait référence au mérite avéré. Les
              métaphores liées à la vie de Jésus - comme ressusciter Lazare ou multiplier les pains - illustrent le type
              de mérite pouvant justifier une accréditation.<br />
              Cependant, moi, Carlos Jiménez Duarte, je suis celui qui décide si une réalisation de la vie d'une personne
              est suffisante pour accréditer son rang sur ce réseau social.<br />
              Si tu es capable de voler, que tu as eu une vision révélatrice après une nuit de boisson ou que tu as sauvé
              mille personnes d'un incendie, cela ne te donne pas automatiquement le droit de devenir l'un de mes
              Gardiens. Le rang est accordé à celui qui le mérite vraiment et le représente comme personne.
            </li>
            <li>
              Porter le titre de Gardien représente un engagement à vie : envers toi-même, envers la communauté et envers
              le Gardien Suprême Absolu (Dieu). Pour préserver ce rang, l'essentiel est de maintenir la cohérence.
            </li>
            <li>
              Devenir Gardien est une destinée possible pour tous. L'historique des souhaits accomplis et accrédités dans
              le compteur officiel de Kiadez.com est valorisé.<br />
              Ce modèle peut être reproduit à la maison, entre proches et amis, en tenant son propre comptage de souhaits
              accomplis. C'est valable et digne. Cependant, pour l'instant, je ne m'engage pas à utiliser ces comptages
              externes comme référence automatique pour lier quelqu'un en tant que Gardien officiel.
            </li>
          </ul>

          <h2>Sur l'accomplissement des souhaits</h2>
          <ul>
            <li>Toute personne peut s'adresser à un Gardien pour accomplir le souhait d'une autre.</li>
            <li>Les souhaits peuvent être accomplis de manière anonyme ou avec un enregistrement public de l'aide reçue.</li>
            <li>Offrir son aide ne garantit pas automatiquement que ta participation sera acceptée.</li>
            <li>
              Lorsqu'une personne décide de collaborer, un processus d'audit sérieux commence afin de reconnaître ses
              intentions.
            </li>
            <li>
              Ce processus garantit que :
              <ul>
                <li>Celui qui contribue n'attend aucune récompense autre que la satisfaction de servir.</li>
                <li>Il ne cherche ni à contraindre, ni à manipuler, ni à créer une dette émotionnelle.</li>
                <li>Il ne cherche pas à faire du marketing émotionnel.</li>
                <li>Il ne cherche pas d'influence politique, religieuse ou institutionnelle.</li>
                <li>Il connaît et accepte la Philosophie du Bon Gardien.</li>
              </ul>
            </li>
            <li>
              Celui qui reçoit le souhait n'acquiert aucun engagement moral au-delà d'une gratitude sincère. L'octroi
              d'un souhait ne sera pas utilisé comme mécanisme de manipulation, d'achat d'amitié ou de coercition
              relationnelle.
            </li>
            <li>
              Celui qui reçoit le souhait reste pleinement libre. Il n'acquiert aucune dette envers Kiadez.com ni envers
              la personne ayant offert le bien ou le service.
            </li>
          </ul>

          <h2>Sur l'Oracle</h2>
          <ul>
            <li>
              L'Oracle est un outil de réflexion personnelle. Il ne sert ni à deviner l'avenir ni à modifier le passé ;
              seulement à l'assimiler.
            </li>
            <li>Son objectif est de t'aider à reconnaître quelles forces et idées prédominent dans ton esprit.</li>
            <li>Il ne remplace pas le service d'un psychologue professionnel.</li>
            <li>Il peut être publié ou maintenu privé via la Clé Privée Personnelle.</li>
          </ul>

          <h2>Sur les étoiles et réalisations</h2>
          <ul>
            <li>Les utilisateurs peuvent gagner des étoiles grâce à leurs publications.</li>
            <li>Les étoiles ne peuvent pas être retirées une fois accordées.</li>
            <li>
              Si un utilisateur supprime des publications, les étoiles associées seront retirées, ainsi que les
              réalisations obtenues grâce à elles.
            </li>
            <li>
              Donner des étoiles au Fonds Commun ne génère ni compensation économique ni privilèges. C'est un acte
              symbolique de détachement.
            </li>
            <li>
              Les réalisations n'accordent pas de privilèges dans la plateforme, sauf la possibilité que le profil soit
              suggéré dans la section des abonnés.
            </li>
          </ul>

          <h2>Sur la vie privée</h2>
          <ul>
            <li>
              Je n'effectue pas de suivi analytique à des fins commerciales. À la date du 21 février 2026, je donne ma
              parole que je ne vendrai pas de données et que je n'utiliserai pas les informations à des fins commerciales.
            </li>
            <li>
              Les mineurs peuvent créer un compte, mais leurs informations resteront privées jusqu'à validation par un
              tuteur légal. Mentir dans ce processus peut conduire à une suspension définitive.
            </li>
            <li>
              La Clé Privée Personnelle est conçue pour protéger les informations chiffrées de l'utilisateur. Je n'ai
              accès ni à cette clé ni au contenu chiffré. Kiadez.com ne demandera jamais ce mot de passe.
            </li>
            <li>L'algorithme n'est pas conçu pour générer de l'addiction.</li>
            <li>Il n'y aura pas de publicité ni de comptes institutionnels. Ce réseau social est pensé pour les personnes, pas pour les marques.</li>
          </ul>

          <h2>Engagements des utilisateurs</h2>
          <ul>
            <li>Publier du contenu illégal peut entraîner un signalement et une suspension.</li>
            <li>Abuser du système pour manipuler les étoiles ou les réalisations peut entraîner une suspension.</li>
            <li>Les souhaits accomplis doivent être marqués sous serment de vérité.</li>
            <li>Le harcèlement numérique n'est pas autorisé.</li>
          </ul>

          <hr class="legal-divider" />

          <h2>Document de finalité</h2>
          <p class="legal-meta">
            Kiadez.com<br />
            Base conceptuelle fondatrice
          </p>

          <h3>1. Ce qu'est le projet</h3>
          <p>Quelqu'un a dit un jour que ce réseau social ressemblait davantage à un journal personnel. Il n'avait pas tort.</p>
          <p>
            Kiadez.com, dans son essence la plus profonde, est un journal conscient. Il est né de l'idée que les
            utilisateurs apprennent à se connaître, à reconnaître l'ampleur de leurs souhaits, aussi bien ceux qu'ils
            peuvent affirmer en public que ceux qu'ils préfèrent garder en privé.
          </p>
          <p>Telle est l'essence du projet.</p>
          <p>
            Créer du contenu chaque jour n'est pas une course à la visibilité, mais une recherche d'alignement avec ce
            que tu désires réellement. C'est une manière de montrer à la Vie que tu es sincère avec ton chemin et que tu
            souhaites être cohérent entre ce que tu espères atteindre et ce que tu vis au quotidien.
          </p>
          <p>Kiadez.com ne naît pas du bruit, mais du sens.</p>

          <h3>2. Ce que le projet n'est pas</h3>
          <p>Kiadez.com n'est pas une plateforme conçue pour garantir l'accomplissement de tes souhaits.</p>
          <p>
            Ce n'est pas une entreprise qui promet des résultats.<br />
            Ce n'est pas un système magique de manifestation.<br />
            Ce n'est pas un contrat de réussite.
          </p>
          <p>
            Il est proposé comme un canal pour que tu puisses exprimer honnêtement ce que tu désires, mais il ne s'engage
            pas à travailler à ta place ni à intervenir directement dans la réalisation de tes objectifs.
          </p>
          <p>
            Il existe un service alternatif, structuré autour du système des Gardiens, qui peut servir d'intermédiaire
            lorsque certains utilisateurs décident de partager leur générosité. Toutefois, ce service ne constitue aucune
            garantie que le fait d'exposer ton souhait le réalisera tel que tu l'imagines.
          </p>
          <p>Publier un souhait n'oblige pas le monde à te l'accorder.</p>

          <h3>3. Portée réelle</h3>
          <p>Kiadez.com est un pont.</p>
          <p>
            Un pont sincère entre ceux qui peuvent aider - par capacité économique ou par service volontaire - et ceux
            qui osent croire en leurs propres rêves.
          </p>
          <p>Mais la véritable portée du projet ne réside pas dans l'acte externe d'accomplissement.</p>
          <p>Elle réside dans le processus interne de reconnaissance.</p>
          <p>
            La véritable portée est que l'utilisateur contemple chaque jour ce qu'il désire et observe si cette
            visualisation sincère se reflète dans sa conduite, dans son contenu et dans sa vie.
          </p>
          <p>
            Si quelqu'un intervient pour t'aider, que ce soit une conséquence.<br />
            Mais le centre restera toujours ta cohérence.
          </p>

          <h3>4. Limites</h3>
          <p>Kiadez.com défend la liberté individuelle comme principe fondamental de l'identité humaine.</p>
          <p>Toutefois, toute liberté implique une responsabilité envers son propre environnement et envers les autres.</p>
          <p>
            Tu es libre d'exprimer tes souhaits, publics ou privés, tant que le contenu reste dans le respect et les
            limites légales applicables au niveau international, étant donné qu'il s'agit d'un réseau social ouvert au
            monde.
          </p>
          <p>
            L'enseignement et la vie du Grand Maître Jésus sont présentés comme l'un des axes inspirateurs du projet.
            Cependant, cela ne fait pas de Kiadez.com une plateforme religieuse ni politique.
          </p>
          <p>
            Il n'existe aucune intention de prosélytisme ni de colonisation de la pensée d'autrui.<br />
            Quelle que soit ta conviction spirituelle ou philosophique, tu es le bienvenu.
          </p>

          <h3>5. Responsabilités</h3>
          <p>Chaque utilisateur est responsable de son contenu et de la sincérité avec laquelle il agit dans le réseau social.</p>
          <p>
            En publiant un souhait, l'utilisateur déclare qu'il reflète une recherche authentique.<br />
            En marquant un souhait comme accompli, il le fait sous le principe de vérité.
          </p>
          <p>Kiadez.com adhère à la valeur universelle de la parole donnée comme fondement de la coexistence.</p>
          <p>La plateforme ne surveille pas la conscience de l'utilisateur. Elle lui fait confiance.</p>
        {:else}
          <p class="legal-meta">
            <em>Términos y Condiciones - versión humana</em><br />
            Escritas por Carlos Jiménez Duarte<br />
            21 de febrero de 2026
          </p>

          <p>
            Estas reglas de juego son fáciles de leer porque están escritas bajo verdad de juramento, con la sinceridad
            de alguien que desea exponer con claridad lo que representa su proyecto al publicar Kiadez.com como una red
            social accesible para todos.
          </p>

          <p>
            Casi nadie lee los términos y condiciones. Así que te los voy a resumir, como hombre de palabra que soy,
            para que entiendas bien de qué va esta red social, cuál es mi compromiso y qué estoy dispuesto a
            representar también dentro de los términos legales.
          </p>

          <p>Es mi red social, por lo tanto opera con mi estructura y mis reglas. Te lo resumo:</p>

          <h2>Sobre la esencia de Kiadez</h2>
          <ul>
            <li>
              Esta no es una red social religiosa. No busco hacer proselitismo sobre la vida de Jesús al colocarlo como
              uno de los Guardianes principales de Kiadez.com.
            </li>
            <li>Si eres ateo, musulmán, judío o profesas cualquier otra religión, eres totalmente bienvenido.</li>
            <li>
              En Kiadez.com se defiende la libertad individual como principio fundamental. Si deseas publicar, entre tus
              deseos públicos o privados, que anhelas ser mujeriego o escritor de literatura erótica, no habrá moral
              católica ni cristiana que entre a juzgarte. Como fundador de esta red social, basándome en mi propio
              viaje espiritual, te doy mi palabra de que Dios no juzga tu corazón; sencillamente te ama tal como eres.
            </li>
            <li>
              Kiadez.com, representado por mí, rechaza como organización y/o movimiento cualquier vinculación con
              partidos políticos, gobiernos nacionales o internacionales.<br />
              "Al César lo que es del César, y a Dios lo que es de Dios" (Mateo 22:21).
            </li>
            <li>
              Esta red social nació como medio para canalizar tu energía, tu voluntad creativa y tu deseo de realizarte
              en lo que sueñas. Pero eso no implica que Kiadez.com tenga el compromiso de trabajar directa o
              indirectamente en la realización de tu deseo.<br />
              Publicar tu deseo - lo digo por experiencia - alinea tu pensamiento con lo que realmente buscas y te
              ayuda a reconocer hacia dónde te diriges. No saber hacia dónde caminas es, probablemente, uno de los
              mayores males a los que se ha enfrentado la humanidad desde su origen.
            </li>
            <li>
              Si esta red social empieza a frustrar tus emociones, si ver que tus deseos no se cumplen afecta tus
              expectativas, la sugerencia más sincera es que cierres tu cuenta. Puedes marcharte en cualquier momento.
            </li>
            <li>
              Mi sueño es que compartamos la Vida; que mostremos cómo enfocamos nuestra energía en el día a día y que
              eso nos mantenga inspirados. La red social se convierte entonces en un canal comunitario para dejar a un
              lado lo imposible y crear contenido que nos estimule hacia una dirección concreta: la coherencia entre lo
              que soñamos y lo que vivimos.
            </li>
          </ul>

          <h2>Sobre los Guardianes</h2>
          <ul>
            <li>
              Actualmente, yo, Carlos Jiménez Duarte, me presento como el primer y único Guardián de Kiadez.com.
            </li>
            <li>
              El alcance de este proyecto anhela que, en el futuro, exista una organización real de Guardianes cuya
              misión sea servir como intermediarios entre quienes pueden ayudar a cumplir los deseos de otras personas.
            </li>
            <li>
              La Filosofía del Buen Guardián deja en claro que todo Guardián es, ante todo, un servidor: una persona
              cuyo interés principal es estar al servicio de los demás, sin esperar reconocimiento ni influir sobre
              otros. El Guardián no se exhibe, no busca marketing emocional, ni aspira a convertirse en influencer.
            </li>
            <li>
              El sistema de jerarquías busca establecer una filosofía del respeto. Está inspirado en la estructura
              tradicional de las academias, especialmente en la filosofía del Hap Ki Do, donde se busca orden y
              disciplina.<br />
              Recuerda:<br />
              <strong>"Cuanto más alto el rango, más invisible el ego."</strong>
            </li>
            <li>
              En Kiadez.com algunas personas pueden obtener el rango de Guardián sin seguir exclusivamente el camino
              tradicional de cumplir deseos uno a uno. Esto hace referencia al mérito comprobado. Las metáforas
              relacionadas con la vida de Jesús - como resucitar a Lázaro o multiplicar los panes - ilustran el tipo
              de mérito que puede justificar una acreditación.<br />
              Sin embargo, yo, Carlos Jiménez Duarte, soy quien decide si un logro en la vida de una persona es
              suficiente para acreditar su rango en esta red social.<br />
              Si eres capaz de volar por los aires, tuviste una visión reveladora después de una noche de tragos o
              salvaste a mil personas de un incendio, eso no te otorga automáticamente el derecho a convertirte en uno
              de mis Guardianes. El rango se concede a quien realmente lo merece y lo representa como persona.
            </li>
            <li>
              Ostentar el título de Guardián representa un compromiso de por vida: contigo mismo, con la comunidad y con
              el Guardián Supremo Absoluto (Dios). Para preservar ese rango, lo esencial es mantener la coherencia.
            </li>
            <li>
              Llegar a ser Guardián es un destino posible para cualquiera. Se valora el historial de deseos cumplidos y
              acreditados en el contador oficial de Kiadez.com.<br />
              Este modelo puede ser imitado en el hogar, entre familiares y amigos, llevando su propio conteo de deseos
              cumplidos. Eso es válido y digno. Sin embargo, por ahora, no me comprometo a utilizar esos conteos
              externos como referencia automática para vincular a alguien como Guardián oficial.
            </li>
          </ul>

          <h2>Sobre el cumplimiento de deseos</h2>
          <ul>
            <li>Cualquier persona puede acudir a un Guardián para cumplir el deseo de otra.</li>
            <li>Los deseos pueden cumplirse de manera anónima o dejando constancia pública de quién ayudó.</li>
            <li>Ofrecer ayuda no garantiza automáticamente que tu participación será aceptada.</li>
            <li>Cuando alguien decide colaborar, se inicia un proceso serio de auditoría para reconocer sus intenciones.</li>
            <li>
              Este proceso garantiza que:
              <ul>
                <li>Quien aporta no espera recompensa distinta a la satisfacción de servir.</li>
                <li>No busca coaccionar, manipular ni generar deuda emocional.</li>
                <li>No pretende hacer marketing emocional.</li>
                <li>No busca influir política, religiosa o institucionalmente.</li>
                <li>Conoce y acepta la Filosofía del Buen Guardián.</li>
              </ul>
            </li>
            <li>
              Quien recibe el deseo no adquiere compromiso moral alguno, más allá de la gratitud sincera. No se usará
              la concesión de deseos como mecanismo de manipulación, compra de amistad o coerción relacional.
            </li>
            <li>
              Quien recibe el deseo es plenamente libre. No adquiere deuda con Kiadez.com ni con quien concedió el bien
              o servicio.
            </li>
          </ul>

          <h2>Sobre el Oráculo</h2>
          <ul>
            <li>
              El Oráculo es una herramienta de reflexión personal. No sirve para adivinar el futuro ni modificar el
              pasado; solo para asimilarlo.
            </li>
            <li>Su meta es ayudarte a reconocer qué fuerzas e ideas predominan en tu mente.</li>
            <li>No sustituye el servicio de un psicólogo profesional.</li>
            <li>Puede publicarse o mantenerse en privado mediante la Clave Privada Personal.</li>
          </ul>

          <h2>Sobre las estrellas y logros</h2>
          <ul>
            <li>Los usuarios pueden ganar estrellas a través de sus publicaciones.</li>
            <li>Las estrellas no se pueden retirar una vez concedidas.</li>
            <li>
              Si un usuario borra publicaciones, las estrellas asociadas serán restadas, y también los logros obtenidos
              por ellas.
            </li>
            <li>
              Donar estrellas al Fondo Común no genera compensación económica ni privilegios. Es un acto simbólico de
              desprendimiento.
            </li>
            <li>
              Los logros no otorgan privilegios dentro de la plataforma, salvo la posibilidad de que el perfil sea
              sugerido en la sección de seguidores.
            </li>
          </ul>

          <h2>Sobre la privacidad</h2>
          <ul>
            <li>
              No realizo monitoreo analítico con fines comerciales. A fecha del 21 de febrero de 2026, doy mi palabra
              de que no venderé datos ni utilizaré la información con fines comerciales.
            </li>
            <li>
              Los menores de edad pueden crear cuenta, pero su información permanecerá privada hasta ser acreditada por
              un tutor legal. Mentir en este proceso puede llevar a suspensión definitiva.
            </li>
            <li>
              La Clave Privada Personal está diseñada para proteger la información cifrada del usuario. No tengo acceso
              a dicha clave ni al contenido cifrado. Kiadez.com no solicitará jamás esta contraseña.
            </li>
            <li>El algoritmo no está diseñado para generar adicción.</li>
            <li>
              No habrá anuncios publicitarios ni cuentas institucionales. Esta red social está pensada para personas,
              no para marcas.
            </li>
          </ul>

          <h2>Compromisos de los usuarios</h2>
          <ul>
            <li>Publicar contenido ilegal puede generar denuncia y suspensión.</li>
            <li>Abusar del sistema para manipular estrellas o logros puede generar suspensión.</li>
            <li>Los deseos cumplidos deben marcarse bajo juramento de verdad.</li>
            <li>El bullying digital no está permitido.</li>
          </ul>

          <hr class="legal-divider" />

          <h2>Documento de Propósito</h2>
          <p class="legal-meta">
            Kiadez.com<br />
            Base Conceptual Fundacional
          </p>

          <h3>1. Qué es el proyecto</h3>
          <p>Alguien dijo alguna vez que esta red social parecía más bien un diario personal. No se equivocaba.</p>
          <p>
            Kiadez.com, en su esencia más profunda, es un diario consciente. Nació bajo la idea de que los usuarios
            aprendan a conocerse, a reconocer la magnitud de sus deseos, tanto aquellos que pueden afirmar en público
            como los que prefieren resguardar en privado.
          </p>
          <p>Esa es la esencia del proyecto.</p>
          <p>
            Crear contenido a diario no es una carrera por visibilidad, sino una búsqueda de alineación con lo que
            realmente deseas. Es una manera de demostrarle a la Vida que eres sincero con tu camino y que anhelas ser
            coherente entre lo que aspiras alcanzar y lo que vives en tu día a día.
          </p>
          <p>Kiadez.com no nace del ruido, sino del propósito.</p>

          <h3>2. Qué no es el proyecto</h3>
          <p>Kiadez.com no es una plataforma diseñada para garantizar el cumplimiento de tus deseos.</p>
          <p>
            No es una empresa que prometa resultados.<br />
            No es un sistema mágico de manifestación.<br />
            No es un contrato de éxito.
          </p>
          <p>
            Se ofrece como canal para que puedas expresar con honestidad lo que deseas, pero no se compromete a
            trabajar por ti ni a intervenir directamente en la realización de tus metas.
          </p>
          <p>
            Existe un servicio alternativo, estructurado en torno al sistema de Guardianes, que puede intermediar
            cuando algunos usuarios decidan compartir su generosidad. Sin embargo, dicho servicio no constituye
            garantía alguna de que, por el hecho de exponer tu deseo, este se cumplirá tal como lo imaginas.
          </p>
          <p>Publicar un deseo no obliga al mundo a concedértelo.</p>

          <h3>3. Alcance real</h3>
          <p>Kiadez.com es un puente.</p>
          <p>
            Un puente sincero entre quienes pueden ayudar - ya sea por solvencia económica o servicio voluntario - y
            quienes se atreven a creer en sus propios sueños.
          </p>
          <p>Pero el verdadero alcance del proyecto no está en el acto externo del cumplimiento.</p>
          <p>Está en el proceso interno de reconocimiento.</p>
          <p>
            El verdadero alcance es que el usuario contemple a diario qué es lo que desea y observe si esa
            visualización sincera se refleja en su conducta, en su contenido y en su vida.
          </p>
          <p>
            Si alguien interviene para ayudarte, que sea una consecuencia.<br />
            Pero el centro siempre será tu coherencia.
          </p>

          <h3>4. Límites</h3>
          <p>Kiadez.com defiende la libertad individual como principio fundamental de la identidad humana.</p>
          <p>Sin embargo, toda libertad implica responsabilidad frente al entorno propio y frente a los demás.</p>
          <p>
            Eres libre de expresar tus deseos, públicos o privados, siempre que el contenido permanezca dentro del
            respeto y los límites legales aplicables a nivel internacional, considerando que se trata de una red social
            abierta al mundo.
          </p>
          <p>
            La enseñanza y la vida del Gran Maestro Jesús se presentan como uno de los ejes inspiradores del proyecto.
            No obstante, esto no convierte a Kiadez.com en una plataforma religiosa ni política.
          </p>
          <p>
            No existe intención de proselitismo ni de colonización del pensamiento ajeno.<br />
            Cualquiera que sea tu convicción espiritual o filosófica, eres bienvenido.
          </p>

          <h3>5. Responsabilidades</h3>
          <p>Cada usuario es responsable de su contenido y de la sinceridad con la que actúe dentro de la red social.</p>
          <p>
            Al publicar un deseo, el usuario declara que este refleja una búsqueda auténtica.<br />
            Al marcar un deseo como cumplido, lo hace bajo el principio de verdad.
          </p>
          <p>Kiadez.com se acoge al valor universal de la palabra dada como fundamento de la convivencia.</p>
          <p>La plataforma no vigila la conciencia del usuario. Confía en ella.</p>
        {/if}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
