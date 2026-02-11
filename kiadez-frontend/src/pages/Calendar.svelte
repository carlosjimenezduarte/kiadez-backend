<script>
  import { onMount } from "svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";

  onMount(() => {
    initPurposeCoverModule();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Calendario</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user calendar-background">

    <main class="user-home">

      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
      <section class="cover" id="cover">
        <div class="cover-media" id="coverMedia">
          <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Portada" />

          <div class="cover-actions">
            <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
              Cambiar portada
            </button>
            <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title="Editar mi propósito de vida">
              Editar mi propósito de vida
            </button>

            <input id="coverFile" type="file" accept="image/*" class="hidden" />
          </div>

          <div class="purpose-triangle" aria-label="Deseos de propósito">
            <button class="purpose-pill purpose-top" type="button" id="purpose1">
              Deseo #1: Secreto
            </button>

            <button class="purpose-pill purpose-left" type="button" id="purpose2">
              Deseo construir el Reino de Combray
            </button>

            <button class="purpose-pill purpose-right" type="button" id="purpose3">
              Deseo estar unido a Jesús
            </button>
          </div>

          <div class="cover-hint" id="coverHint">
            Arrastra la portada para encuadrarla
          </div>
        </div>
      </section>

      <div class="calendar-body">
        <!-- =========================
         *  NAV / LINKS
         *  ========================= -->
        <nav class="profile-nav" aria-label="Navegación de perfil">
          <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
          <a class="nav-pill" href="/star-pool-found.html" title="Estrellas">
            <span class="nav-icon">⭐</span>
            <span><strong>5.000.000</strong> estrellas</span>
          </a>

          <a class="nav-pill" href="/followers.html" title="Seguidores">Seguidores</a>
          <a class="nav-pill" href="/achievements.html" title="Logros recientes">Logros recientes</a>
          <a class="nav-pill" href="/gallery.html" title="Galería">Galería</a>
          <a class="nav-pill" href="/calendar.html" title="Calendario">Calendario</a>
          <a class="nav-pill" href="/my-biography.html" title="Mi biografía">Mi biografía</a>
        </nav>

        <!-- =========================
         *  CALENDARIO 2026
         *  ========================= -->
        <section class="calendar-shell" aria-label="Calendario anual">
          <div class="calendar-head">
            <h2 class="calendar-title">Calendario 2026</h2>
            <div class="calendar-legend">
              <span><strong>Disponible</strong> (hasta el 23 de enero)</span>
            </div>
          </div>

        <article class="calendar-year" aria-label="Vista anual 2026">
          <h3 class="year-label">2026 · Enero a Diciembre</h3>
          <div class="month-grid">
            <article class="month-card">
              <div class="month-name">Enero<span class="month-status">Actual</span></div>
              <div class="month-dots">
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-available"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Febrero<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Marzo<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Abril<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Mayo<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Junio<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Julio<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Agosto<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Septiembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Octubre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Noviembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
            <article class="month-card">
              <div class="month-name">Diciembre<span class="month-status">Próximo</span></div>
              <div class="month-dots">
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
                <span class="month-dot is-future"></span>
              </div>
            </article>
          </div>
        </article>

        <article class="calendar-current" aria-label="Detalle del mes actual">
          <div class="current-head">
            <h3 class="current-month">Enero 2026</h3>
            <div class="calendar-legend">
              <span>⭐ Estrellas</span>
              <span>✅ Deseos cumplidos</span>
              <span>🌟 Deseos públicos</span>
              <span>🏆 Logros</span>
              <span>📝 Publicaciones</span>
            </div>
          </div>

          <div class="calendar-grid">
            <div class="weekday">Lun</div>
            <div class="weekday">Mar</div>
            <div class="weekday">Mié</div>
            <div class="weekday">Jue</div>
            <div class="weekday">Vie</div>
            <div class="weekday">Sáb</div>
            <div class="weekday">Dom</div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell is-empty"></div>
            <div class="day-cell">
              <div class="day-number"><span>1</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>2</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>3</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>⭐</span><span>120 estrellas</span></div>
                <div class="day-metric"><span>✅</span><span>2 deseos cumplidos</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>4</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>5</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>6</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>7</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🌟</span><span>1 deseo público</span></div>
                <div class="day-metric"><span>📝</span><span>2 publicaciones</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>8</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>9</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>10</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>11</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>12</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🏆</span><span>1 logro</span></div>
                <div class="day-metric"><span>📝</span><span>1 publicación</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>13</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>14</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>15</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>16</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>17</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>18</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>⭐</span><span>60 estrellas</span></div>
                <div class="day-metric"><span>✅</span><span>1 deseo cumplido</span></div>
                <div class="day-metric"><span>📝</span><span>3 publicaciones</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>19</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>20</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>21</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell">
              <div class="day-number"><span>22</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>🌟</span><span>2 deseos públicos</span></div>
                <div class="day-metric"><span>🏆</span><span>1 logro</span></div>
              </div>
            </div>
            <div class="day-cell is-today">
              <div class="day-number"><span>23</span><span class="day-badge">Hoy</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>•</span><span>Sin registros</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>24</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>25</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>26</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>27</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>28</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>29</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>30</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-future">
              <div class="day-number"><span>31</span></div>
              <div class="day-metrics">
                <div class="day-metric"><span>☁️</span><span>Por llegar</span></div>
              </div>
            </div>
            <div class="day-cell is-empty"></div>
          </div>
        </article>
      </section>
      </div>

    </main>

    <!-- FOOTER reutilizado -->
    <footer class="kiadez-footer">
      <div class="footer-main">

        <div class="footer-column footer-origin">
          <p class="footer-poem">
            Kiadez fue llamado por una estrella a subir el Monte Manjaro.<br>
            No para dominar, sino para orientar.<br>
            Su luz no deslumbra: acompaña.
          </p>
        </div>

        <div class="footer-columns">
          <div class="footer-column">
            <h4>Sobre nuestra red social</h4>
            <ul>
              <li><a href="/what-is-kiadez.html">Qué es Kiadez</a></li>
              <li><a href="/guardians-rank.html">Rangos de Guardianes</a></li>
              <li><a href="/be-a-guardian.html">Ser Guardián</a></li>
              <li><a href="/contact.html">Contacto</a></li>
            </ul>
          </div>

          <div class="footer-column">
            <h4>Idiomas</h4>
            <ul>
              <li><a href="/?lang=es">Español</a></li>
              <li><a href="/?lang=en">English</a></li>
              <li><a href="/?lang=fr">Français</a></li>
            </ul>
          </div>

          <div class="footer-column">
            <h4>Contacto</h4>
            <ul>
              <li>info@kiadez.com</li>
              <li>+57 333 225 6078</li>
            </ul>
          </div>

          <div class="footer-column">
            <h4>Información legal</h4>
            <ul>
              <li><a href="/terms.html">Términos y condiciones</a></li>
              <li><a href="/privacy.html">Privacidad</a></li>
            </ul>
          </div>
        </div>

      </div>

      <div class="footer-bottom">
        © 2026 Kiadez — Una red social para cumplir deseos.
      </div>
    </footer>

  </div>
