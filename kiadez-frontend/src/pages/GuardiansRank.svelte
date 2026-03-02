<script>
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  const ranks = [
    {
      titleEs: "Rango 9 · Guardián Supremo Absoluto",
      titleEn: "Rank 9 · Absolute Supreme Guardian",
      descEs: "Ser el Logos.<br>La Fuente.<br>El Amado Padre Celestial.<br>El Universo mismo.",
      descEn: "To be the Logos.<br>The Source.<br>The Beloved Heavenly Father.<br>The Universe itself.",
    },
    {
      titleEs: "Rango 8 · Guardián de Guardianes",
      titleEn: "Rank 8 · Guardian of Guardians",
      descEs:
        'Conceder <strong>1.000.000.000</strong> deseos<br><span class="rank-or">o</span><br>ser el <a href="https://kiadez.com/assets/GranMasterJesus.png" target="_blank" rel="noopener noreferrer">Gran Maestro Jesús</a>',
      descEn:
        'Grant <strong>1,000,000,000</strong> wishes<br><span class="rank-or">or</span><br>be the <a href="https://kiadez.com/assets/GranMasterJesus.png" target="_blank" rel="noopener noreferrer">Great Master Jesus</a>',
    },
    {
      titleEs: "Rango 7 · Guardián del Umbral",
      titleEn: "Rank 7 · Threshold Guardian",
      descEs:
        'Conceder <strong>1.000.000</strong> deseos<br><span class="rank-or">o</span><br>haber regresado a la vida tras inmolarse en una cruz',
      descEn:
        'Grant <strong>1,000,000</strong> wishes<br><span class="rank-or">or</span><br>have returned to life after self-sacrifice on a cross',
    },
    {
      titleEs: "Rango 6 · Guardián del Logos",
      titleEn: "Rank 6 · Guardian of the Logos",
      descEs:
        'Conceder <strong>500.000</strong> deseos<br><span class="rank-or">o</span><br>haber resucitado a Lázaro',
      descEn:
        'Grant <strong>500,000</strong> wishes<br><span class="rank-or">or</span><br>have resurrected Lazarus',
    },
    {
      titleEs: "Rango 5 · Guardián Mayor",
      titleEn: "Rank 5 · Senior Guardian",
      descEs:
        'Conceder <strong>50.000</strong> deseos<br><span class="rank-or">o</span><br>haber calmado la tormenta en el Mar de Galilea',
      descEn:
        'Grant <strong>50,000</strong> wishes<br><span class="rank-or">or</span><br>have calmed the storm in the Sea of Galilee',
    },
    {
      titleEs: "Rango 4 · Guardián Consagrado",
      titleEn: "Rank 4 · Consecrated Guardian",
      descEs:
        'Conceder <strong>5.000</strong> deseos<br><span class="rank-or">o</span><br>ser el creador de Dragon Ball Z<br>o ser <a href="https://es.wikipedia.org/wiki/Carlo_Acutis" target="_blank" rel="noopener noreferrer">San Carlo Acutis</a><br>o haber caminado sobre las aguas',
      descEn:
        'Grant <strong>5,000</strong> wishes<br><span class="rank-or">or</span><br>be the creator of Dragon Ball Z<br>or be <a href="https://es.wikipedia.org/wiki/Carlo_Acutis" target="_blank" rel="noopener noreferrer">Saint Carlo Acutis</a><br>or have walked on water',
    },
    {
      titleEs: "Rango 3 · Guardián",
      titleEn: "Rank 3 · Guardian",
      descEs:
        'Conceder <strong>1.000</strong> deseos<br><span class="rank-or">o</span><br>ser el creador de esta red social<br>o <a href="https://www.dofus.com" target="_blank" rel="noopener noreferrer">ser uno de los tres fundadores de Ankama Games</a><br>o haber multiplicado los panes y los peces',
      descEn:
        'Grant <strong>1,000</strong> wishes<br><span class="rank-or">or</span><br>be the creator of this social network<br>or <a href="https://www.dofus.com" target="_blank" rel="noopener noreferrer">be one of the three founders of Ankama Games</a><br>or have multiplied loaves and fish',
    },
    {
      titleEs: "Rango 2 · Aprendiz",
      titleEn: "Rank 2 · Apprentice",
      descEs:
        'Conceder <strong>100</strong> deseos<br><span class="rank-or">o</span><br>haber desarrollado <a href="https://www.chessescape.com" target="_blank" rel="noopener noreferrer">ChessEscape</a><br>o haber convertido el agua en vino en Caná',
      descEn:
        'Grant <strong>100</strong> wishes<br><span class="rank-or">or</span><br>have developed <a href="https://www.chessescape.com" target="_blank" rel="noopener noreferrer">ChessEscape</a><br>or have turned water into wine in Cana',
    },
    {
      titleEs: "Rango 1 · Aspirante",
      titleEn: "Rank 1 · Aspirant",
      descEs:
        'Conceder <strong>10</strong> deseos<br><span class="rank-or">o</span><br>haber bebido <a href="https://www.youtube.com/watch?v=1lr5cBV4fe0" target="_blank" rel="noopener noreferrer">la Cerveza del Pacto</a><br>o haber nacido en Belén en el Año 0',
      descEn:
        'Grant <strong>10</strong> wishes<br><span class="rank-or">or</span><br>have drunk <a href="https://www.youtube.com/watch?v=1lr5cBV4fe0" target="_blank" rel="noopener noreferrer">the Beer of the Covenant</a><br>or have been born in Bethlehem in Year 0',
    },
  ];
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <title>{tr("Rangos de Guardianes", "Guardian Ranks", "Rangs des Gardiens")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-guardian">
  <main class="content-center">
    <article class="content-card">
      <div class="guardian-ranks">
        <p class="guardian-quote">
          {#if isEn || isFr}
            “The higher the rank,<br />the more invisible the ego.”
          {:else}
            “Cuanto más alto el rango,<br />más invisible el ego.”
          {/if}
        </p>

        {#each ranks as rank}
          <div class="rank">
            <h2 class="rank-title">{isEn || isFr ? rank.titleEn : rank.titleEs}</h2>
            <p class="rank-desc">
              {@html isEn || isFr ? rank.descEn : rank.descEs}
            </p>
          </div>
        {/each}
      </div>
    </article>
  </main>

  <AuthFooter />
</div>
