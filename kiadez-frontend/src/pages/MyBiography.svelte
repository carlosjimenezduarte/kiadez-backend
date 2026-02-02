<script>
  import { onMount } from "svelte";

  onMount(() => {
    // =========================
        //  LocalStorage keys (compartibles con Home si quieres)
        // =========================
        const LS = {
          coverImg: "kiadez_user_cover_img",
          coverPos: "kiadez_user_cover_pos",
          purpose: "kiadez_user_purpose"
        };
    
        // =========================
        // COVER (misma mecánica de Home)
        // =========================
        const coverMedia = document.getElementById("coverMedia");
        const coverImg = document.getElementById("coverImg");
        const coverFile = document.getElementById("coverFile");
        const btnChangeCover = document.getElementById("btnChangeCover");
        const coverHint = document.getElementById("coverHint");
    
        let isDraggingCover = false;
        let startX = 0, startY = 0;
        let currentX = 0, currentY = 0;
    
        const applyCoverTransform = () => {
          coverImg.style.transform = `translate(${currentX}px, ${currentY}px)`;
          localStorage.setItem(LS.coverPos, JSON.stringify({ x: currentX, y: currentY }));
        };
    
        const loadCover = () => {
          const savedImg = localStorage.getItem(LS.coverImg);
          if (savedImg) coverImg.src = savedImg;
    
          const savedPos = localStorage.getItem(LS.coverPos);
          if (savedPos) {
            try {
              const p = JSON.parse(savedPos);
              currentX = p.x ?? 0;
              currentY = p.y ?? 0;
              coverImg.style.transform = `translate(${currentX}px, ${currentY}px)`;
            } catch { /* noop */ }
          }
        };
    
        btnChangeCover.addEventListener("click", () => coverFile.click());
    
        coverFile.addEventListener("change", (e) => {
          const file = e.target.files?.[0];
          if (!file) return;
    
          const reader = new FileReader();
          reader.onload = () => {
            localStorage.setItem(LS.coverImg, reader.result);
            coverImg.src = reader.result;
            currentX = 0; currentY = 0;
            applyCoverTransform();
          };
          reader.readAsDataURL(file);
        });
    
        coverMedia.addEventListener("mousedown", (e) => {
          const isButton = e.target.closest(".cover-actions");
          const isPill = e.target.closest(".purpose-pill");
          if (isButton || isPill) return;
    
          isDraggingCover = true;
          startX = e.clientX - currentX;
          startY = e.clientY - currentY;
          coverMedia.classList.add("is-dragging");
          coverHint?.classList.add("hidden");
        });
    
        window.addEventListener("mousemove", (e) => {
          if (!isDraggingCover) return;
          currentX = e.clientX - startX;
          currentY = e.clientY - startY;
          applyCoverTransform();
        });
    
        window.addEventListener("mouseup", () => {
          if (!isDraggingCover) return;
          isDraggingCover = false;
          coverMedia.classList.remove("is-dragging");
        });
    
        // =========================
        // PURPOSE MODAL (misma UX de Home) + persistencia
        // =========================
        const purposeModalOverlay = document.getElementById("purposeModalOverlay");
        const btnEditPurposes = document.getElementById("btnEditPurposes");
        const closePurposeModal = document.getElementById("closePurposeModal");
        const cancelPurposeModal = document.getElementById("cancelPurposeModal");
        const savePurposeModal = document.getElementById("savePurposeModal");
    
        const p1 = document.getElementById("purpose1");
        const p2 = document.getElementById("purpose2");
        const p3 = document.getElementById("purpose3");
    
        const purposeInput1 = document.getElementById("purposeInput1");
        const purposeInput2 = document.getElementById("purposeInput2");
        const purposeInput3 = document.getElementById("purposeInput3");
    
        const loadPurpose = () => {
          const raw = localStorage.getItem(LS.purpose);
          if (!raw) return;
          try {
            const p = JSON.parse(raw);
            if (p.one) p1.textContent = p.one;
            if (p.two) p2.textContent = p.two;
            if (p.three) p3.textContent = p.three;
          } catch { /* noop */ }
        };
    
        const openPurposeModal = () => {
          purposeInput1.value = p1.textContent.trim();
          purposeInput2.value = p2.textContent.trim();
          purposeInput3.value = p3.textContent.trim();
    
          purposeModalOverlay.classList.remove("hidden");
          purposeModalOverlay.setAttribute("aria-hidden", "false");
        };
    
        const closePurpose = () => {
          purposeModalOverlay.classList.add("hidden");
          purposeModalOverlay.setAttribute("aria-hidden", "true");
        };
    
        btnEditPurposes?.addEventListener("click", openPurposeModal);
        closePurposeModal?.addEventListener("click", closePurpose);
        cancelPurposeModal?.addEventListener("click", closePurpose);
    
        savePurposeModal?.addEventListener("click", () => {
          const one = purposeInput1.value.trim() || p1.textContent;
          const two = purposeInput2.value.trim() || p2.textContent;
          const three = purposeInput3.value.trim() || p3.textContent;
    
          p1.textContent = one;
          p2.textContent = two;
          p3.textContent = three;
    
          localStorage.setItem(LS.purpose, JSON.stringify({ one, two, three }));
          closePurpose();
        });
    
        purposeModalOverlay?.addEventListener("click", (e) => {
          if (e.target === purposeModalOverlay) closePurpose();
        });
    
        // =========================
        // INIT
        // =========================
        loadCover();
        loadPurpose();
    
        // (deja aquí tu init del resto de biografía: loadSectionData(), applyPrivacy(), etc.)
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Mi biografía</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-bio biography-background">

    <main class="user-home user-home--bio">

      <!-- PORTADA (MISMA DE HOME) -->
      <section class="cover" id="cover">
        <div class="cover-media" id="coverMedia">
          <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Portada" />

          <div class="cover-actions">
            <button class="icon-btn" id="btnChangeCover" type="button" title="Cambiar portada">
              Cambiar portada
            </button>
            <button class="icon-btn" id="btnEditPurposes" type="button" title="Editar deseos de propósito">
              Editar propósito
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

      <div class="biography-body">
      <!-- NAV (YA LO TIENES IGUAL) -->
      <nav class="profile-nav" aria-label="Navegación de perfil">
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

      <!-- MODAL DE PROPÓSITO (MISMO DE HOME) -->
      <div class="modal-overlay hidden" id="purposeModalOverlay" aria-hidden="true">
        <div class="modal" role="dialog" aria-modal="true" aria-label="Editar deseos de propósito">
          <div class="modal-head">
            <h3>Editar deseos de propósito</h3>
            <button class="modal-close" type="button" id="closePurposeModal">✕</button>
          </div>

          <div class="modal-body">
            <label class="modal-label" for="purposeInput1">Deseo 1</label>
            <input class="modal-input" id="purposeInput1" type="text" />

            <label class="modal-label" for="purposeInput2">Deseo 2</label>
            <input class="modal-input" id="purposeInput2" type="text" />

            <label class="modal-label" for="purposeInput3">Deseo 3</label>
            <input class="modal-input" id="purposeInput3" type="text" />
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline btn-compact" type="button" id="cancelPurposeModal">Cancelar</button>
            <button class="btn btn-primary btn-compact" type="button" id="savePurposeModal">Guardar</button>
          </div>
        </div>
      </div>


      <!-- ======= CUERPO (3 columnas) ======= -->
      <section class="bio-shell">

        <section class="bio-grid">

          <!-- ========== IZQUIERDA: TOC ========== -->
          <aside class="bio-card bio-toc" aria-label="Tabla de contenidos">
            <h2 class="bio-side-title" id="tocUserName">Carlos Jiménez Duarte</h2>

            <ol class="bio-toc-list" id="tocList">
              <li><a href="#sec-about" data-toc="about">Carlos Jiménez Duarte</a></li>
              <li><a href="#sec-dream" data-toc="dream">Sobre su mayor sueño</a></li>
              <li><a href="#sec-pro" data-toc="pro">Logros profesionales</a></li>
              <li><a href="#sec-life" data-toc="life">Logros alcanzados</a></li>
              <li><a href="#sec-quotes" data-toc="quotes">Frases favoritas</a></li>
            </ol>

            <p class="bio-side-note">
              Esta tabla se sincroniza con tus títulos del centro.
            </p>
          </aside>

          <!-- ========== CENTRO: CONTENIDO ========== -->
          <section class="bio-center" aria-label="Biografía editable">

            <!-- Sección 1 -->
            <article class="bio-card bio-section" id="sec-about" data-section="about" data-maxwords="1200">
              <header class="bio-section-header">
                <div>
                  <h2 class="bio-section-title" data-title> Carlos Jiménez Duarte </h2>
                  <p class="bio-section-subtitle">Extensión máxima: <strong>1200</strong> palabras</p>
                </div>

                <div class="bio-section-actions">
                  <button class="btn btn-outline btn-compact" type="button" data-edit>Editar</button>
                  <button class="btn btn-primary btn-compact" type="button" data-save hidden>Guardar</button>
                </div>
              </header>

              <p class="bio-prompt">
                Describe quién eres. Se sugiere hacerlo en tercera persona. Aprovecha este espacio: es tu Wikipedia
                personal.
                Lo que escribas aquí será lo mismo que podrían leer tus seres queridos dentro de 100 años.
              </p>

              <div class="bio-editor">
                <textarea class="bio-textarea" data-input placeholder="Escribe aquí..."></textarea>
                <div class="bio-meta">
                  <span data-counter>0 / 1200 palabras</span>
                  <span class="bio-meta-muted">Se guarda localmente (por ahora).</span>
                </div>
              </div>
            </article>

            <!-- Sección 2 -->
            <article class="bio-card bio-section" id="sec-dream" data-section="dream" data-maxwords="1200">
              <header class="bio-section-header">
                <div class="bio-title-editable">
                  <h2 class="bio-section-title" data-title>Sobre su mayor sueño</h2>
                  <button class="chip-mini" type="button" data-rename title="Renombrar título">✎</button>
                </div>
                <div class="bio-section-actions">
                  <button class="btn btn-outline btn-compact" type="button" data-edit>Editar</button>
                  <button class="btn btn-primary btn-compact" type="button" data-save hidden>Guardar</button>
                </div>
              </header>

              <p class="bio-prompt">
                Describe aquí cuál es ese sueño que te gustaría ver realidad: aquello que, contra todo pronóstico,
                te
                gustaría
                ver realizado. O, si lo sientes, lo que te gustaría alcanzar en una nueva vida. Simplemente sueña y
                cree.
              </p>

              <div class="bio-editor">
                <textarea class="bio-textarea" data-input placeholder="Escribe aquí..."></textarea>
                <div class="bio-meta">
                  <span data-counter>0 / 1200 palabras</span>
                </div>
              </div>
            </article>

            <!-- Sección 3 -->
            <article class="bio-card bio-section" id="sec-pro" data-section="pro" data-maxwords="500">
              <header class="bio-section-header">
                <div class="bio-title-editable">
                  <h2 class="bio-section-title" data-title>Logros profesionales</h2>
                  <button class="chip-mini" type="button" data-rename title="Renombrar título">✎</button>
                </div>
                <div class="bio-section-actions">
                  <button class="btn btn-outline btn-compact" type="button" data-edit>Editar</button>
                  <button class="btn btn-primary btn-compact" type="button" data-save hidden>Guardar</button>
                </div>
              </header>

              <p class="bio-prompt">
                Describe aquí los logros personales o académicos más importantes que consideras has conseguido hasta
                ahora.
                Esto te servirá como tu propia versión de LinkedIn. (Recomendado en viñetas.)
              </p>

              <div class="bio-editor">
                <textarea class="bio-textarea" data-input
                  placeholder="• Logro 1&#10;• Logro 2&#10;• Logro 3"></textarea>
                <div class="bio-meta">
                  <span data-counter>0 / 500 palabras</span>
                </div>
              </div>
            </article>

            <!-- Sección 4 -->
            <article class="bio-card bio-section" id="sec-life" data-section="life" data-maxwords="500">
              <header class="bio-section-header">
                <div class="bio-title-editable">
                  <h2 class="bio-section-title" data-title>Logros alcanzados</h2>
                  <button class="chip-mini" type="button" data-rename title="Renombrar título">✎</button>
                </div>
                <div class="bio-section-actions">
                  <button class="btn btn-outline btn-compact" type="button" data-edit>Editar</button>
                  <button class="btn btn-primary btn-compact" type="button" data-save hidden>Guardar</button>
                </div>
              </header>

              <p class="bio-prompt">
                Describe aquí los logros personales que te hacen sentir orgulloso; aquello que sabes define tu
                existencia.
                (Recomendado en viñetas.)
              </p>

              <div class="bio-editor">
                <textarea class="bio-textarea" data-input placeholder="• Logro 1&#10;• Logro 2"></textarea>
                <div class="bio-meta">
                  <span data-counter>0 / 500 palabras</span>
                </div>
              </div>
            </article>

            <!-- Sección 5 -->
            <article class="bio-card bio-section" id="sec-quotes" data-section="quotes" data-maxwords="500">
              <header class="bio-section-header">
                <div class="bio-title-editable">
                  <h2 class="bio-section-title" data-title>Frases favoritas</h2>
                  <button class="chip-mini" type="button" data-rename title="Renombrar título">✎</button>
                </div>
                <div class="bio-section-actions">
                  <button class="btn btn-outline btn-compact" type="button" data-edit>Editar</button>
                  <button class="btn btn-primary btn-compact" type="button" data-save hidden>Guardar</button>
                </div>
              </header>

              <p class="bio-prompt">
                Describe tu filosofía de vida en 3 o 4 frases. Cuando ya no estés en este mundo, las personas
                podrían
                recordarte
                por estas banderas personales.
              </p>

              <div class="bio-editor">
                <textarea class="bio-textarea" data-input placeholder="• “...” — Autor&#10;• “...” — Autor"></textarea>
                <div class="bio-meta">
                  <span data-counter>0 / 500 palabras</span>
                </div>
              </div>
            </article>

          </section>

          <!-- ========== DERECHA: INFOBOX ========== -->
          <aside class="bio-card bio-infobox" aria-label="Ficha del usuario">

            <div class="infobox-head">
              <h2 class="infobox-title" id="infoName">Carlos Jiménez</h2>
            </div>

            <figure class="infobox-photo">
              <img id="profilePhoto" src="/css/logo-kiadez.webp" alt="Foto del usuario" />
              <figcaption id="photoCaption">Jiménez en 2025.</figcaption>
            </figure>

            <!-- Toggle global (modo edición de privacidad) -->
            <div class="infobox-toggles">
              <span class="infobox-toggle-label">Privacidad</span>
              <button class="chip-mini" id="togglePrivacyMode" type="button">Editar</button>
            </div>

            <!-- Sección -->
            <div class="infobox-section">
              <div class="infobox-section-title">Información personal</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="birthname">
                  <th>Nombre de nacimiento</th>
                  <td><span data-value>Carlos Jiménez Duarte</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="birth">
                  <th>Nacimiento</th>
                  <td><span data-value>5 de mayo de 1986 (39 años); Barrancabermeja, Santander, Colombia</span><span
                      class="infobox-hidden" data-hidden hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="residence">
                  <th>Residencia</th>
                  <td><span data-value>Medellín, Antioquia</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero
                      no decirlo</span></td>
                </tr>
                <tr data-field="nationality">
                  <th>Nacionalidad</th>
                  <td><span data-value>Colombiana</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="lang">
                  <th>Lengua materna</th>
                  <td><span data-value>Español</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="pseudonyms">
                  <th>Seudónimos</th>
                  <td><span data-value>Melquíades, Kiadez, Saint Martin</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero no decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Características físicas</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="height">
                  <th>Altura</th>
                  <td><span data-value>1,80 m</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="weight">
                  <th>Peso</th>
                  <td><span data-value>76 kg</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="eyes">
                  <th>Ojos</th>
                  <td><span data-value>Castaño</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="hair">
                  <th>Cabello</th>
                  <td><span data-value>Castaño</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Educación</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="education">
                  <th>Educado en</th>
                  <td><span data-value>Colegio Calasanz; Universidad Pontificia Bolivariana; Politécnico
                      Grancolombiano</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Información profesional</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="occupation">
                  <th>Ocupación</th>
                  <td><span data-value>Escritor, Ingeniero de Software, Artista Plástico Aficionado</span><span
                      class="infobox-hidden" data-hidden hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="active">
                  <th>Años activo</th>
                  <td><span data-value>2003 — presente</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Distinciones</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="awards">
                  <th>Premio</th>
                  <td><span data-value>Wattys 2019 — Categoría Ciencia Ficción, La Guerra Solar I</span><span
                      class="infobox-hidden" data-hidden hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="guardian">
                  <th>Guardián</th>
                  <td><span data-value>Kiadez.com</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Curiosidades</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="hero">
                  <th>Superhéroe favorito</th>
                  <td><span data-value>Batman</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="song">
                  <th>Canción favorita</th>
                  <td><span data-value>Dreamer — Ozzy Osbourne</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="food">
                  <th>Comida favorita</th>
                  <td><span data-value>Comida mexicana</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span></td>
                </tr>
                <tr data-field="games">
                  <th>Videojuegos</th>
                  <td><span data-value>Dofus, Prince of Persia 2, Batman Arkham Knight</span><span
                      class="infobox-hidden" data-hidden hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="book">
                  <th>Libro favorito</th>
                  <td><span data-value>Las Mil y Una Noches</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero
                      no decirlo</span></td>
                </tr>
                <tr data-field="hobbies">
                  <th>Otros pasatiempos</th>
                  <td><span data-value>Sacar a Willow a paseo, reír, ver series, soñar en grande</span><span
                      class="infobox-hidden" data-hidden hidden>Prefiero no decirlo</span></td>
                </tr>
                <tr data-field="motto">
                  <th>Lema</th>
                  <td><span data-value>A Dios sea la gloria</span><span class="infobox-hidden" data-hidden
                      hidden>Prefiero
                      no decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Actividad en Kiadez.com</div>
              <table class="infobox-table">
                <tbody>
                <tr data-field="wishes_done">
                  <th>Deseos cumplidos</th>
                  <td><span data-value>20</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span>
                  </td>
                </tr>
                <tr data-field="wishes_granted">
                  <th>Deseos concedidos</th>
                  <td><span data-value>57</span><span class="infobox-hidden" data-hidden hidden>Prefiero no
                      decirlo</span>
                  </td>
                </tr>
                <tr data-field="rank">
                  <th>Rango</th>
                  <td><span data-value>Guardián Rango 3</span><span class="infobox-hidden" data-hidden hidden>Prefiero
                      no
                      decirlo</span></td>
                </tr>
                </tbody>
              </table>
            </div>

            <div class="infobox-section">
              <div class="infobox-section-title">Emblema</div>
              <div class="infobox-emblem">
                <img src="/css/logo-kiadez.webp" alt="Emblema" />
              </div>
            </div>

            <!-- Panel de privacidad (aparece en modo edición) -->
            <div class="infobox-privacy-panel" id="privacyPanel" hidden>
              <p class="bio-side-note" style="margin:0 0 10px;">
                Activa/desactiva qué campos aparecen públicos. Si lo apagas, se muestra “Prefiero no decirlo”.
              </p>
              <div class="privacy-grid" id="privacyGrid"></div>
            </div>

          </aside>

        </section>

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
