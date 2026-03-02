<script>
  import { onMount } from "svelte";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";
  import { followApi } from "../lib/api";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";

  const PAGE_SIZE = 25;
  const PAGE_WINDOW = 7;
  const DEFAULT_AVATAR_SRC = "/assets/avatar-default.jpg";
  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  const createSectionState = () => ({
    items: [],
    page: 1,
    page_size: PAGE_SIZE,
    total: 0,
    total_pages: 1,
    range_start: 0,
    range_end: 0,
    loading: false,
    error: "",
  });

  let suggestions = createSectionState();
  let followers = createSectionState();
  let following = createSectionState();

  let followActionError = "";
  let pendingFollowIds = new Set();

  const parseErrorMessage = (error) => {
    const message = String(error?.message || "").trim();
    return message || tr("No se pudo completar la solicitud.", "Could not complete the request.", "Impossible de complete the request.");
  };

  const formatCount = (value) => Number(value || 0).toLocaleString(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO");

  const getDisplayName = (item) => {
    const fullName = String(item?.full_name || "").trim();
    if (fullName) return fullName;
    const userId = Number(item?.user_id || 0);
    return userId > 0 ? tr(`Usuario ${userId}`, `User ${userId}`, `User ${userId}`) : tr("Usuario", "User", "Utilisateur");
  };

  const getHandle = (item) => {
    const handle = String(item?.handle || "").trim();
    if (handle) return handle;
    const username = String(item?.username || "").trim();
    if (username) return `@${username}`;
    const userId = Number(item?.user_id || 0);
    return userId > 0 ? `@id${userId}` : tr("@usuario", "@user", "@utilisateur");
  };

  const getProfileHref = (item) => {
    const href = String(item?.profile_url || "").trim();
    return href || "/home_user.html";
  };

  const getAvatarSrc = (item) => {
    const url = String(item?.avatar_url || "").trim();
    return url || DEFAULT_AVATAR_SRC;
  };

  const isFollowPending = (userId) => pendingFollowIds.has(Number(userId));

  const setFollowPending = (userId, pending) => {
    const normalizedId = Number(userId);
    const next = new Set(pendingFollowIds);
    if (pending) {
      next.add(normalizedId);
    } else {
      next.delete(normalizedId);
    }
    pendingFollowIds = next;
  };

  const getState = (section) => {
    if (section === "suggestions") return suggestions;
    if (section === "followers") return followers;
    return following;
  };

  const setState = (section, patch) => {
    if (section === "suggestions") {
      suggestions = { ...suggestions, ...patch };
      return;
    }
    if (section === "followers") {
      followers = { ...followers, ...patch };
      return;
    }
    following = { ...following, ...patch };
  };

  const getFetcher = (section) => {
    if (section === "suggestions") return followApi.listSuggestions;
    if (section === "followers") return followApi.listFollowers;
    return followApi.listFollowing;
  };

  const buildVisiblePages = (sectionState) => {
    const totalPages = Math.max(1, Number(sectionState?.total_pages || 1));
    const currentPage = Math.max(1, Math.min(Number(sectionState?.page || 1), totalPages));

    if (totalPages <= PAGE_WINDOW) {
      return Array.from({ length: totalPages }, (_, index) => index + 1);
    }

    const side = Math.floor(PAGE_WINDOW / 2);
    let start = Math.max(1, currentPage - side);
    let end = Math.min(totalPages, start + PAGE_WINDOW - 1);

    if (end - start + 1 < PAGE_WINDOW) {
      start = Math.max(1, end - PAGE_WINDOW + 1);
    }

    return Array.from({ length: end - start + 1 }, (_, index) => start + index);
  };

  const loadSection = async (section, requestedPage = 1) => {
    const fetcher = getFetcher(section);
    const normalizedPage = Math.max(1, Number(requestedPage || 1));

    setState(section, {
      loading: true,
      error: "",
    });

    try {
      const data = await fetcher({
        page: normalizedPage,
        page_size: PAGE_SIZE,
      });

      setState(section, {
        items: Array.isArray(data?.items) ? data.items : [],
        page: Math.max(1, Number(data?.page) || normalizedPage),
        page_size: Math.max(1, Number(data?.page_size) || PAGE_SIZE),
        total: Math.max(0, Number(data?.total) || 0),
        total_pages: Math.max(1, Number(data?.total_pages) || 1),
        range_start: Math.max(0, Number(data?.range_start) || 0),
        range_end: Math.max(0, Number(data?.range_end) || 0),
        loading: false,
        error: "",
      });
    } catch (error) {
      setState(section, {
        loading: false,
        items: [],
        error: parseErrorMessage(error),
      });
    }
  };

  const refreshAllSections = async () => {
    await Promise.all([
      loadSection("suggestions", suggestions.page),
      loadSection("followers", followers.page),
      loadSection("following", following.page),
    ]);
  };

  const goToPage = (section, page) => {
    const state = getState(section);
    const totalPages = Math.max(1, Number(state.total_pages || 1));
    const normalizedPage = Math.max(1, Math.min(Number(page || 1), totalPages));
    if (normalizedPage === state.page) return;
    void loadSection(section, normalizedPage);
  };

  const toggleFollow = async (item) => {
    const userId = Number(item?.user_id || 0);
    if (!userId || isFollowPending(userId)) return;

    const shouldFollow = !item.is_following;
    followActionError = "";
    setFollowPending(userId, true);

    try {
      if (shouldFollow) {
        await followApi.follow(userId);
      } else {
        await followApi.unfollow(userId);
      }
      await refreshAllSections();
    } catch (error) {
      followActionError = parseErrorMessage(error);
    } finally {
      setFollowPending(userId, false);
    }
  };

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("followersStarsTotal");
    void refreshAllSections();
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Seguidores", "Kiadez — Followers", "Kiadez — Abonnés")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background followers-page">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input type="search" placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")} aria-label={tr("Buscar", "Search", "Rechercher")} />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <a class="topbar-btn" href="/home_user.html">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Foto de perfil del usuario", "User profile photo", "Photo de profil de l'utilisateur")} />
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/privacy-and-settings.html" role="menuitem">{tr("Configuración y privacidad", "Settings and privacy", "Paramètres et confidentialité")}</a>
          <button type="button" role="menuitem" on:click={logout}>{tr("Cerrar sesión", "Sign out", "Se déconnecter")}</button>
        </div>
      </details>

      <button class="topbar-icon" type="button" aria-label={tr("Notificaciones", "Notifications", "Alertes")}>
        🔔
        <span class="topbar-badge">3</span>
      </button>

      <details class="topbar-dropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem">{tr("Mi Home", "My Home", "Mon accueil")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

  <main class="user-home">
    <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title={tr("Cambiar portada", "Change cover", "Changer la couverture")}>
            {tr("Cambiar portada", "Change cover", "Changer la couverture")}
          </button>
          <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button" title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}>
            {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier ma mission de vie")}
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de mission")}>
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait n°1 : Secret")}
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            {tr("Deseo construir el Reino de Combray", "I wish to build the Kingdom of Combray", "Je souhaite construire le Royaume de Combray")}
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          {tr("Arrastra la portada para encuadrarla", "Drag the cover to frame it", "Déplace la couverture pour l'ajuster")}
        </div>
      </div>
    </section>

    <div class="home-body">
      <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
        <a class="nav-pill" href="/home_user.html" title={tr("Home", "Home", "Accueil")}>{tr("Home", "Home", "Accueil")}</a>
        <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
          <span class="nav-icon">⭐</span>
          <span><strong id="followersStarsTotal">0</strong> {tr("estrellas", "stars", "étoiles")}</span>
        </a>
        <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
        <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
        <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
        <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")}>{tr("Calendario", "Calendar", "Calendrier")}</a>
        <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
      </nav>

      {#if followActionError}
        <section class="panel followers-message-panel" aria-live="polite">
          <p class="followers-status is-error">{followActionError}</p>
        </section>
      {/if}

      <section class="panel followers-section" aria-label={tr("Sugerencias de usuarios a seguir", "Suggested users to follow", "Utilisateurs suggérés à suivre")}>
        <div class="panel-head">
          <h2 class="panel-title">{tr("Sugerencias de usuarios a seguir", "Suggested users to follow", "Utilisateurs suggérés à suivre")}</h2>
          <span class="panel-badge">{formatCount(suggestions.total)} {tr("sugerencias", "suggestions", "recommandations")}</span>
        </div>
        <p class="panel-muted">
          {tr(
            "Modelos a seguir priorizados por guardianes, usuarios recientes y perfiles destacados.",
            "Profiles to follow prioritized by guardians, recent users, and featured accounts."
          )}
        </p>

        {#if suggestions.error}
          <p class="followers-status is-error">{suggestions.error}</p>
        {:else if suggestions.loading}
          <p class="followers-status">{tr("Cargando sugerencias...", "Loading suggestions...", "Chargement des suggestions...")}</p>
        {:else if suggestions.items.length === 0}
          <p class="followers-status">{tr("No hay sugerencias disponibles por ahora.", "No suggestions available right now.", "Aucune suggestion disponible pour le moment.")}</p>
        {:else}
          <div class="followers-grid">
            {#each suggestions.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`${tr("Ver perfil de", "View profile of", "Voir le profil de")} ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} {tr("seguidores", "followers", "abonnés")}</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      {tr("Procesando...", "Processing...", "Traitement...")}
                    {:else if item.is_following}
                      {tr("Dejar de seguir", "Unfollow", "Ne plus suivre")}
                    {:else}
                      {tr("Seguir", "Follow", "Suivre")}
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>{tr("Ver perfil", "View profile", "Voir le profil")}</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if suggestions.total_pages > 1}
          <nav class="followers-pagination" aria-label={tr("Paginación de sugerencias", "Suggestions pagination", "Pagination des suggestions")}>
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página anterior", "Previous page", "Page précédente")}
              on:click={() => goToPage("suggestions", suggestions.page - 1)}
              disabled={suggestions.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(suggestions) as page}
              <button
                class={`followers-page-btn${page === suggestions.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === suggestions.page ? "page" : undefined}
                on:click={() => goToPage("suggestions", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página siguiente", "Next page", "Page suivante")}
              on:click={() => goToPage("suggestions", suggestions.page + 1)}
              disabled={suggestions.page >= suggestions.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !suggestions.loading && !suggestions.error && suggestions.total > 0}
          <p class="followers-range">
            {tr("Mostrando", "Showing", "Affichage")} {suggestions.range_start}-{suggestions.range_end} {tr("de", "of", "de")} {formatCount(suggestions.total)} {tr("sugerencias", "suggestions", "recommandations")}.
          </p>
        {/if}
      </section>

      <section class="panel followers-section" aria-label={tr("Seguidores", "Followers", "Abonnés")}>
        <div class="panel-head">
          <h2 class="panel-title">{tr("Seguidores", "Followers", "Abonnés")}</h2>
          <span class="panel-badge">{formatCount(followers.total)} {tr("seguidores", "followers", "abonnés")}</span>
        </div>
        <p class="panel-muted">
          {tr("Personas que siguen tu camino y celebran tus logros.", "People who follow your path and celebrate your achievements.", "Personnes qui suivent ton chemin et célèbrent tes réalisations.")}
        </p>

        {#if followers.error}
          <p class="followers-status is-error">{followers.error}</p>
        {:else if followers.loading}
          <p class="followers-status">{tr("Cargando seguidores...", "Loading followers...", "Chargement des abonnés...")}</p>
        {:else if followers.items.length === 0}
          <p class="followers-status">{tr("Aún no tienes seguidores registrados.", "You do not have registered followers yet.", "Tu n'as pas encore d'abonnés enregistrés.")}</p>
        {:else}
          <div class="followers-grid">
            {#each followers.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`${tr("Ver perfil de", "View profile of", "Voir le profil de")} ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} {tr("seguidores", "followers", "abonnés")}</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      {tr("Procesando...", "Processing...", "Traitement...")}
                    {:else if item.is_following}
                      {tr("Dejar de seguir", "Unfollow", "Ne plus suivre")}
                    {:else}
                      {tr("Seguir", "Follow", "Suivre")}
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>{tr("Ver perfil", "View profile", "Voir le profil")}</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if followers.total_pages > 1}
          <nav class="followers-pagination" aria-label={tr("Paginación de seguidores", "Followers pagination", "Pagination des abonnés")}>
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página anterior", "Previous page", "Page précédente")}
              on:click={() => goToPage("followers", followers.page - 1)}
              disabled={followers.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(followers) as page}
              <button
                class={`followers-page-btn${page === followers.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === followers.page ? "page" : undefined}
                on:click={() => goToPage("followers", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página siguiente", "Next page", "Page suivante")}
              on:click={() => goToPage("followers", followers.page + 1)}
              disabled={followers.page >= followers.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !followers.loading && !followers.error && followers.total > 0}
          <p class="followers-range">
            {tr("Mostrando", "Showing", "Affichage")} {followers.range_start}-{followers.range_end} {tr("de", "of", "de")} {formatCount(followers.total)} {tr("seguidores", "followers", "abonnés")}.
          </p>
        {/if}
      </section>

      <section class="panel followers-section" aria-label={tr("Siguiendo", "Following", "Abonnements")}>
        <div class="panel-head">
          <h2 class="panel-title">{tr("Siguiendo", "Following", "Abonnements")}</h2>
          <span class="panel-badge">{formatCount(following.total)} {tr("siguiendo", "following", "abonnements")}</span>
        </div>
        <p class="panel-muted">
          {tr("Usuarios a quienes sigues actualmente.", "Users you currently follow.", "Utilisateurs que tu suis actuellement.")}
        </p>

        {#if following.error}
          <p class="followers-status is-error">{following.error}</p>
        {:else if following.loading}
          <p class="followers-status">{tr("Cargando usuarios seguidos...", "Loading followed users...", "Chargement des utilisateurs suivis...")}</p>
        {:else if following.items.length === 0}
          <p class="followers-status">{tr("Aún no sigues a ningún usuario.", "You are not following any users yet.", "Tu ne suis encore aucun utilisateur.")}</p>
        {:else}
          <div class="followers-grid">
            {#each following.items as item (item.user_id)}
              <article class="follower-card">
                <a class="follower-avatar-link" href={getProfileHref(item)} aria-label={`${tr("Ver perfil de", "View profile of", "Voir le profil de")} ${getDisplayName(item)}`}>
                  <img class="follower-avatar" src={getAvatarSrc(item)} alt={`${tr("Foto de perfil de", "Profile photo of", "Photo de profil de")} ${getDisplayName(item)}`} loading="lazy" />
                </a>
                <h3 class="follower-name">{getDisplayName(item)}</h3>
                <p class="follower-handle">{getHandle(item)}</p>
                <p class="follower-count">{formatCount(item.followers_count)} {tr("seguidores", "followers", "abonnés")}</p>
                <div class="follower-actions">
                  <button
                    class={`btn btn-compact${item.is_following ? " btn-outline" : " btn-primary"}`}
                    type="button"
                    disabled={isFollowPending(item.user_id)}
                    on:click={() => toggleFollow(item)}
                  >
                    {#if isFollowPending(item.user_id)}
                      {tr("Procesando...", "Processing...", "Traitement...")}
                    {:else if item.is_following}
                      {tr("Dejar de seguir", "Unfollow", "Ne plus suivre")}
                    {:else}
                      {tr("Seguir", "Follow", "Suivre")}
                    {/if}
                  </button>
                  <a class="btn btn-outline btn-compact" href={getProfileHref(item)}>{tr("Ver perfil", "View profile", "Voir le profil")}</a>
                </div>
              </article>
            {/each}
          </div>
        {/if}

        {#if following.total_pages > 1}
          <nav class="followers-pagination" aria-label={tr("Paginación de siguiendo", "Following pagination", "Pagination des abonnements")}>
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página anterior", "Previous page", "Page précédente")}
              on:click={() => goToPage("following", following.page - 1)}
              disabled={following.page <= 1}
            >
              &lt;&lt;
            </button>
            {#each buildVisiblePages(following) as page}
              <button
                class={`followers-page-btn${page === following.page ? " is-active" : ""}`}
                type="button"
                aria-current={page === following.page ? "page" : undefined}
                on:click={() => goToPage("following", page)}
              >
                {page}
              </button>
            {/each}
            <button
              class="followers-page-btn is-arrow"
              type="button"
              aria-label={tr("Página siguiente", "Next page", "Page suivante")}
              on:click={() => goToPage("following", following.page + 1)}
              disabled={following.page >= following.total_pages}
            >
              &gt;&gt;
            </button>
          </nav>
        {/if}

        {#if !following.loading && !following.error && following.total > 0}
          <p class="followers-range">
            {tr("Mostrando", "Showing", "Affichage")} {following.range_start}-{following.range_end} {tr("de", "of", "de")} {formatCount(following.total)} {tr("seguidos", "followed", "suivis")}.
          </p>
        {/if}
      </section>
    </div>
  </main>
  <AuthFooter />
</div>
