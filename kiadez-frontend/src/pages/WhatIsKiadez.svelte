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
  <title>{isEn ? "What is Kiadez?" : isFr ? "Qu'est-ce que Kiadez ?" : "¿Qué es Kiadez?"}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-kiadez">
  <main class="content-center">
    <article class="content-card">
      <h1 class="content-title">{isEn ? "What is Kiadez?" : isFr ? "Qu'est-ce que Kiadez ?" : "¿Qué es Kiadez?"}</h1>

      <div class="content-text">
        {#if isEn}
          <p>
            Kiadez was a young shepherd of jalatós, skilled in the art of the staff, glyphs, and shields. He lived
            adventures that tempered his character, but one single night changed his destiny: he dreamed that the
            warmth of a star touched his face, and a voice of light asked him to climb to the top of Mount Manjaro.
          </p>

          <p>
            The next morning he began the ascent without promises, without applause, only with faith and discipline.
            Upon arrival, the wind seemed to pronounce his name. Then the goddess Feca appeared in person. She offered
            him an impossible bargain: exchange his shields and belongings for a ticket to the sky.
          </p>

          <p>
            Thus, Kiadez became a star: not to dominate anyone, but to guide mortals. Since then, from above, his
            light does not blind: it guides. It does not force: it accompanies. His light does not boast. His light
            protects.
          </p>

          <p class="content-title"><strong>Core Principles of Kiadez</strong></p>

          <p>
            1. This social network was born as a social experiment to prove that goals can be achieved and dreams can
            come true when there is courage to pursue them.
          </p>

          <p>
            2. Kiadez is a space where we can all share the gift of generosity through the talent entrusted to us
            before coming into this world.
          </p>

          <p>
            3. This social network invites you to know yourself, to keep a conscious record of how you manage your
            wishes day by day, and of how that process can inspire others to remain in a similar frequency of purpose
            and consistency.
          </p>

          <p>
            4. Kiadez is not a network of beggars. Here you express your wish to refine your inner compass, to prove
            to yourself that it is not impossible, and that you can go farther when you are clear about what you are
            pursuing. In the best case, there will be people who, having gone through similar longings, will intervene
            to help you achieve your goal and lighten your path by granting the wish you dared to express.
          </p>

          <p>
            5. If someone contacts you outside Kiadez.com requesting personal data or guaranteeing fulfillment of your
            wish outside the official Guardian service, be cautious. For this reason, Kiadez has no private messages or
            chat rooms. Your personal data will always be your greatest treasure and responsibility.
          </p>

          <p>
            6. Only Guardians are authorized to grant wishes and publicly stand behind their fulfillment. They
            intervene between the one who expresses a wish and the one who decides to make it real, not in search of
            prominence, but as trained servants acting with authenticity, without profit motives, selfishness, or
            desire for media exposure, according to the philosophy of the Good Guardian.
          </p>

          <p>
            7. If you aspire one day to the rank of Guardian, contribute actively to protecting this space: report
            those who pollute the network with toxic messages, attitudes that foster pity, or requests for personal
            information through their own walls.
          </p>

          <p>
            8. The greatest value of Kiadez will always be human talent and the goodness that lives in people who dare
            to dream and build, together, a better world.
          </p>
        {:else if isFr}
          <p>
            Kiadez était un jeune berger de jalatós, habile dans l'art du bâton, des glyphes et des boucliers. Il a
            vécu des aventures qui ont forgé son caractère, mais une seule nuit a changé son destin : il rêva que la
            chaleur d'une étoile touchait son visage et qu'une voix de lumière lui demandait de gravir le sommet du
            mont Manjaro.
          </p>

          <p>
            Le lendemain matin, il entreprit l'ascension sans promesses, sans applaudissements, seulement avec foi et
            discipline. À son arrivée, le vent semblait prononcer son nom. Alors la déesse Feca apparut en personne.
            Elle lui offrit un marché impossible : échanger ses boucliers et ses biens contre un billet pour le ciel.
          </p>

          <p>
            Ainsi, Kiadez devint une étoile : non pour dominer qui que ce soit, mais pour guider les mortels. Depuis
            lors, dans les hauteurs, sa lumière n'éblouit pas : elle oriente. Elle ne force pas : elle accompagne. Sa
            lumière ne se vante pas. Sa lumière protège.
          </p>

          <p class="content-title"><strong>Principes fondamentaux de Kiadez</strong></p>

          <p>
            1. Ce réseau social est né comme une expérience sociale pour démontrer que les objectifs peuvent être
            atteints et que les rêves peuvent se réaliser lorsqu'il existe le courage d'aller à leur rencontre.
          </p>

          <p>
            2. Kiadez est un espace où nous pouvons tous partager le don de la générosité à travers le talent qui nous
            a été confié avant de venir dans ce monde.
          </p>

          <p>
            3. Ce réseau social t'invite à te connaître toi-même, à tenir un registre conscient de la façon dont tu
            gères tes souhaits au quotidien, et de la manière dont ce processus peut inspirer d'autres personnes à
            rester dans une fréquence similaire de sens et de cohérence.
          </p>

          <p>
            4. Kiadez n'est pas un réseau de mendiants. Ici, tu exprimes ton souhait pour affiner ta boussole
            intérieure, pour te prouver que ce n'est pas impossible et que tu peux aller plus loin lorsque tu sais
            clairement ce que tu poursuis. Dans le meilleur des cas, des personnes ayant traversé des désirs similaires
            interviendront pour t'aider à atteindre ton objectif et alléger ton chemin en accordant le souhait que tu
            as osé exprimer.
          </p>

          <p>
            5. Si quelqu'un te contacte en dehors de Kiadez.com pour demander des données personnelles ou garantir
            l'accomplissement de ton souhait en dehors du service officiel des Gardiens, sois prudent. Pour cette
            raison, Kiadez ne dispose pas de messagerie privée ni de salles de chat. Tes données personnelles seront
            toujours ton plus grand trésor et ta plus grande responsabilité.
          </p>

          <p>
            6. Seuls les Gardiens sont autorisés à accomplir des souhaits et à s'exposer publiquement dans leur
            accomplissement. Ils interviennent entre celui qui exprime un souhait et celui qui décide de le rendre
            réel, non pas en quête de protagonisme, mais comme serviteurs formés à agir avec authenticité, sans but
            lucratif, sans égoïsme et sans désir d'exposition médiatique, selon la philosophie du Bon Gardien.
          </p>

          <p>
            7. Si tu aspires un jour au rang de Gardien, contribue activement à protéger cet espace : signale ceux qui
            polluent le réseau avec des messages toxiques, des attitudes qui favorisent la pitié ou des demandes
            d'informations personnelles à travers leurs propres murs.
          </p>

          <p>
            8. La plus grande valeur de Kiadez sera toujours le talent humain et la bonté qui habitent les personnes
            qui osent rêver et construire, ensemble, un monde meilleur.
          </p>
        {:else}
          <p>
            Kiadez fue un joven pastor de jalatós, diestro en el arte del bastón, los glifos y los escudos. Vivió
            aventuras que le templaron el carácter, pero fue una sola noche la que cambió su destino: soñó que el
            calor de una estrella acariciaba su rostro, y una voz de luz le pidió subir hasta la cima del Monte
            Manjaro.
          </p>

          <p>
            A la mañana siguiente emprendió el ascenso sin promesas, sin aplausos, solo con fe y disciplina. Al
            llegar, el viento parecía pronunciar su nombre. Entonces apareció la diosa Feca en persona. Le ofreció un
            trato imposible: cambiar sus escudos y sus pertenencias por un tiquete al cielo.
          </p>

          <p>
            Así, Kiadez se convirtió en una estrella: no para dominar a nadie, sino para orientar a los mortales.
            Desde entonces, en lo alto, no deslumbra: orienta. No obliga: acompaña. Su luz no presume. Su luz guarda.
          </p>

          <p class="content-title"><strong>Principios Fundamentales de Kiadez</strong></p>

          <p>
            1. Esta red social nació como un experimento social para probar y comprobar que las metas pueden
            alcanzarse y que los sueños pueden hacerse realidad cuando existe el valor de salir a su encuentro.
          </p>

          <p>
            2. Kiadez es un espacio donde todos podemos compartir el don de la generosidad a través del talento que
            nos fue confiado antes de venir a este mundo.
          </p>

          <p>
            3. Esta red social te invita a conocerte a ti mismo, a llevar un registro consciente de cómo gestionas día
            a día tus deseos y de cómo ese proceso puede inspirar a otros a mantenerse en una frecuencia similar de
            propósito y constancia.
          </p>

          <p>
            4. Kiadez no es una red de mendigos. Aquí expones tu deseo para afinar tu brújula interna, para demostrarte
            que no es imposible y que puedes llegar más lejos cuando tienes claro lo que persigues. En el mejor de los
            casos, habrá personas que, habiendo atravesado anhelos similares, intercederán para ayudarte a cumplir tu
            objetivo y aliviar la carga de tu camino, concediéndote el deseo que te atreviste a expresar.
          </p>

          <p>
            5. Si alguien te contacta de manera externa a Kiadez.com solicitando datos personales o garantizándote el
            cumplimiento de tu deseo por fuera del servicio de los Guardianes oficiales, desconfía. Por esta razón,
            Kiadez no cuenta con mensajes privados ni salas de chat. Tus datos personales serán siempre tu mayor
            tesoro y responsabilidad.
          </p>

          <p>
            6. Solo los Guardianes están autorizados para conceder deseos y dar la cara en su cumplimiento. Ellos
            interceden entre quien expresa un deseo y quien ha decidido hacerlo realidad, no en busca de protagonismo,
            sino como servidores capacitados para actuar con autenticidad, sin afán de lucro, sin egoísmo y sin deseo
            de exposición mediática, conforme a la filosofía del buen Guardián.
          </p>

          <p>
            7. Si deseas aspirar algún día al rango de Guardián, contribuye activamente a cuidar este espacio: denuncia
            a quienes contaminen la red con mensajes tóxicos, actitudes que fomenten la lástima o solicitudes de
            información personal a través de sus propios muros.
          </p>

          <p>
            8. El mayor valor de Kiadez será siempre el talento humano y la bondad que habita en las personas que se
            atreven a soñar y a construir, juntos, un mundo mejor.
          </p>
        {/if}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
