<script>
  import { buildLangHref, setLocale, t } from "./i18n";

  export let compact = false;

  const langEsHref = buildLangHref("es");
  const langEnHref = buildLangHref("en");
  const langFrHref = buildLangHref("fr");

  const handleLocaleClick = (nextLocale) => {
    setLocale(nextLocale);
  };
</script>

<footer class="kiadez-footer">
  {#if !compact}
    <div class="footer-main">
      <div class="footer-column footer-origin">
        <p class="footer-poem">
          {t("footer.poem.line1")}<br />
          {t("footer.poem.line2")}<br />
          {t("footer.poem.line3")}
        </p>
      </div>

      <div class="footer-columns">
        <div class="footer-column">
          <h4>{t("footer.about_title")}</h4>
          <ul>
            <li><a href="/what-is-kiadez.html">{t("footer.about_links.what_is")}</a></li>
            <li><a href="/downloadapp.html">{t("footer.about_links.download_app")}</a></li>
            <li><a href="/guardians-rank.html">{t("footer.about_links.guardian_ranks")}</a></li>
            <li><a href="/be-a-guardian.html">{t("footer.about_links.be_guardian")}</a></li>
            <li><a href="/contact.html">{t("footer.about_links.contact")}</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{t("footer.languages_title")}</h4>
          <ul>
            <li>
              <a href={langEsHref} on:click={() => handleLocaleClick("es")}>
                {t("common.languages.es")}
              </a>
            </li>
            <li>
              <a href={langEnHref} on:click={() => handleLocaleClick("en")}>
                {t("common.languages.en")}
              </a>
            </li>
            <li>
              <a href={langFrHref} on:click={() => handleLocaleClick("fr")}>
                {t("common.languages.fr")}
              </a>
            </li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{t("footer.contact_title")}</h4>
          <ul>
            <li>info@kiadez.com</li>
            <li>+57 333 225 6078</li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>{t("footer.legal_title")}</h4>
          <ul>
            <li><a href="/mygamerules.html">{t("footer.legal_links.game_rules")}</a></li>
            <li><a href="/terms.html">{t("footer.legal_links.terms")}</a></li>
            <li><a href="/privacy.html">{t("footer.legal_links.privacy")}</a></li>
          </ul>
        </div>
      </div>
    </div>
  {/if}

  <div class="footer-bottom">
    {t("footer.bottom")}
  </div>
</footer>
