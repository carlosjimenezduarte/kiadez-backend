<script>
  import { onMount } from "svelte";

  onMount(() => {
    document.body.dataset.visitor = "false";

    const oracleCards = [
          {
            id: 1,
            name: "El Ciclo",
            question: "¿Cuál es tu ciclo de las reencarnaciones?",
            context:
              "Enfocado en comprender situaciones que perturban tu viaje en este mundo. En tu vida diaria, ¿qué es eso que va y vuelve de la misma manera, por más que intentes evitarlo? Por ejemplo: discusiones repetidas, una adicción, un patrón emocional o el deseo constante de tener más de algo."
          },
          {
            id: 2,
            name: "La Calma",
            question: "Si pudieras vivir tu vida desde la calma, ¿qué decisión tomarías hoy?",
            context:
              "Enfocado en comprender por qué actúas como actúas actualmente. ¿Qué es lo que realmente te presiona a decidir con prisa? ¿Qué limita tu pensamiento, tu espíritu o tu manera natural de ser en este momento de tu vida?"
          },
          {
            id: 3,
            name: "El Silencio",
            question: "¿Te cuesta mantenerte en silencio?",
            context:
              "Enfocado en comprender si puedes escuchar tu propio pensamiento o si actúas solo por impulso. ¿Cuál es tu relación con el silencio? ¿Puedes estar diez minutos sin estímulos o sientes la necesidad de llenar ese espacio con música, pantallas o distracciones?"
          },
          {
            id: 4,
            name: "El Anhelo",
            question: "¿Cuál sería la vida de tus sueños?",
            context:
              "Enfocado en reconocer qué sientes que te falta para sentirte pleno. Si hoy fuera el último día de tu vida, ¿qué considerarías que no viviste? ¿Qué cualidades, experiencias o formas de ser te hubiera gustado manifestar?"
          },
          {
            id: 5,
            name: "La Elección",
            question: "Si pudieras cambiar algo del mundo, ¿qué elegirías?",
            context:
              "Enfocado en identificar aquello con lo que no estás de acuerdo. ¿Qué crees que no debería existir ni en tu vida ni en la de los demás? Si pudieras eliminarlo, ¿el mundo sería mejor? ¿Tú te sentirías más libre o en paz?"
          },
          {
            id: 6,
            name: "La Libertad",
            question: "¿Te consideras una persona libre?",
            context:
              "Enfocado en reconocer cómo te sientes con la vida que llevas. ¿Existe algo que percibas como una carga constante? ¿Alguna situación física, emocional o mental que afecte tu día a día? ¿O te sientes realmente cómodo con tu forma de vivir?"
          },
          {
            id: 7,
            name: "La Sombra",
            question: "¿Qué es lo que más evitas mirar de ti?",
            context:
              "Enfocado en reconocer aquello que prefieres no enfrentar. Puede ser una emoción, un recuerdo, una actitud o una verdad incómoda. A veces lo que evitamos mirar es justamente lo que más necesita atención para poder transformarse."
          },
          {
            id: 8,
            name: "El Refugio",
            question: "¿Qué te hace sentir en casa?",
            context:
              "Enfocado en identificar aquello que te brinda seguridad y tranquilidad. Puede ser un lugar, una persona, una actividad o un estado interior. Reconocerlo te ayuda a saber dónde recargar tu energía cuando la vida se vuelve exigente."
          },
          {
            id: 9,
            name: "El Gozo",
            question: "¿Qué parte de tu día disfrutas más?",
            context:
              "Enfocado en observar qué momentos te conectan con el gozo. A veces la felicidad no está en grandes logros, sino en instantes simples que solemos pasar por alto. ¿Qué te dice eso sobre lo que realmente valoras?"
          },
          {
            id: 10,
            name: "El Desgaste",
            question: "¿Qué te roba más energía?",
            context:
              "Enfocado en reconocer hábitos, personas o pensamientos que te desgastan. Identificar qué te drena es el primer paso para proteger tu bienestar y tomar decisiones más conscientes sobre a qué le entregas tu tiempo y tu atención."
          },
          {
            id: 11,
            name: "El Aprendiz",
            question: "¿Qué te gustaría aprender?",
            context:
              "Enfocado en conectar con tu curiosidad natural. Aprender no siempre tiene que ver con estudios formales; puede ser una habilidad, una forma de vivir o una manera distinta de relacionarte contigo y con los demás."
          },
          {
            id: 12,
            name: "El Mérito",
            question: "¿Cuándo fue la última vez que te sentiste orgulloso de ti?",
            context:
              "Enfocado en reconocer tus propios logros, grandes o pequeños. Muchas veces avanzamos sin detenernos a valorar lo que hemos superado. Recordarlo fortalece la autoestima y el respeto por tu propio camino."
          },
          {
            id: 13,
            name: "El Apego",
            question: "¿Qué te da miedo perder?",
            context:
              "Enfocado en identificar apegos importantes en tu vida. El miedo a perder algo suele revelar cuánto valor le damos y cuánto dependemos de ello. Observarlo con honestidad ayuda a comprender nuestras decisiones."
          },
          {
            id: 14,
            name: "La Vitalidad",
            question: "¿Qué te hace sentir vivo?",
            context:
              "Enfocado en descubrir aquello que despierta tu entusiasmo. Puede ser crear, ayudar, aprender, moverte o compartir. Reconocerlo te orienta hacia una vida más alineada con lo que te nutre internamente."
          },
          {
            id: 15,
            name: "La Demora",
            question: "¿Qué sueles postergar?",
            context:
              "Enfocado en observar aquello que dejas para después. A veces no se trata de pereza, sino de miedo, cansancio o falta de claridad. Entender por qué postergas algo puede darte pistas importantes sobre lo que necesitas."
          },
          {
            id: 16,
            name: "La Gratitud",
            question: "¿Qué agradeces hoy?",
            context:
              "Enfocado en ejercitar la gratitud consciente. Incluso en días difíciles siempre hay algo que reconocer. Agradecer no niega los problemas, pero cambia la forma en que los miras y los atraviesas."
          },
          {
            id: 17,
            name: "La Voz",
            question: "¿Qué te gustaría decir y no has dicho?",
            context:
              "Enfocado en reconocer palabras retenidas. A veces callamos por miedo a herir, a perder o a exponernos. Identificar lo que no expresas te ayuda a entender qué necesitas comunicar, aunque sea primero contigo mismo."
          },
          {
            id: 18,
            name: "La Paz",
            question: "¿Qué te hace sentir en paz?",
            context:
              "Enfocado en identificar estados, actividades o relaciones que aquietan tu mente. La paz no siempre llega sola; muchas veces se construye al elegir conscientemente aquello que te devuelve equilibrio."
          },
          {
            id: 19,
            name: "El Cuidado",
            question: "¿Qué parte de tu vida necesita más atención?",
            context:
              "Enfocado en observar áreas descuidadas. Puede ser tu cuerpo, tus emociones, tus vínculos o tu descanso. Detectarlo a tiempo permite pequeños ajustes antes de que el desequilibrio se haga mayor."
          },
          {
            id: 20,
            name: "La Lección",
            question: "¿Qué te enseñó tu último error?",
            context:
              "Enfocado en resignificar el error como aprendizaje. Más allá de la culpa o la frustración, cada error deja una lección. Reconocerla te permite avanzar con más claridad y menos peso."
          },
          {
            id: 21,
            name: "Lo Esencial",
            question: "¿Qué te gustaría simplificar?",
            context:
              "Enfocado en identificar excesos. A veces complicamos nuestra vida más de lo necesario. Simplificar puede significar soltar objetos, compromisos, pensamientos o expectativas que ya no te aportan bienestar."
          },
          {
            id: 22,
            name: "El Cuerpo",
            question: "¿Qué te conecta con tu cuerpo?",
            context:
              "Enfocado en reconocer cómo habitas tu cuerpo. Puede ser el movimiento, la respiración, el descanso o la alimentación. Escuchar al cuerpo es una forma directa de volver al presente."
          },
          {
            id: 23,
            name: "El Vínculo",
            question: "¿Qué te hace sentir acompañado?",
            context:
              "Enfocado en identificar vínculos reales. No siempre se trata de estar rodeado de gente, sino de sentir comprensión y presencia. Reconocerlo te ayuda a cuidar mejor tus relaciones."
          },
          {
            id: 24,
            name: "La Liberación",
            question: "¿Qué te gustaría soltar?",
            context:
              "Enfocado en observar cargas innecesarias. Puede ser un resentimiento, una culpa, una expectativa o un hábito. Soltar no es olvidar, es liberar espacio para algo nuevo."
          },
          {
            id: 25,
            name: "El Futuro",
            question: "¿Qué te entusiasma del futuro?",
            context:
              "Enfocado en conectar con la esperanza. Pensar en lo que viene no como ansiedad, sino como posibilidad. Reconocer qué te ilusiona te da dirección y energía para el presente."
          },
          {
            id: 26,
            name: "El Aporte",
            question: "¿Qué te hace sentir útil?",
            context:
              "Enfocado en reconocer tu aporte al mundo. Sentirte útil no depende de grandes logros, sino de saber que lo que haces tiene sentido para ti o para otros."
          },
          {
            id: 27,
            name: "El Reposo",
            question: "¿Qué necesitas descansar?",
            context:
              "Enfocado en identificar cansancios acumulados. A veces no es solo el cuerpo, sino la mente o el corazón. Reconocerlo es el primer paso para darte permiso de pausar."
          },
          {
            id: 28,
            name: "La Protección",
            question: "¿Qué te gustaría cuidar más?",
            context:
              "Enfocado en reconocer aquello que valoras. Puede ser tu salud, una relación, un sueño o tu tiempo. Cuidar algo implica presencia y decisiones conscientes."
          },
          {
            id: 29,
            name: "La Identidad",
            question: "¿Qué te recuerda quién eres?",
            context:
              "Enfocado en identificar anclas personales. Puede ser una actividad, una persona, un recuerdo o un valor. Reconocerlo te ayuda a no perderte cuando todo alrededor cambia."
          },
          {
            id: 30,
            name: "La Intención",
            question: "¿Qué intención eliges para hoy?",
            context:
              "Enfocado en cerrar el ciclo con conciencia. Elegir una intención no es imponer un resultado, sino orientar tu forma de estar en el día. Una pequeña intención puede transformar toda una jornada."
          }
        ];
    
        const oracleUserName = "Carlos Jiménez Duarte";
        const ORACLE_STATE_KEY = "oracle_state_v1";
        const COOLDOWN_MS = 72 * 60 * 60 * 1000;
        const TOTAL_CARDS = oracleCards.length;
    
        const oracleDeck = document.getElementById("oracleDeck");
        const oracleStatus = document.getElementById("oracleStatus");
        const oracleCooldown = document.getElementById("oracleCooldown");
        const oracleDeckEmpty = document.getElementById("oracleDeckEmpty");
        const oracleRevealed = document.getElementById("oracleRevealed");
        const oracleRevealedEmpty = document.getElementById("oracleRevealedEmpty");
    
        const oracleModalOverlay = document.getElementById("oracleModalOverlay");
        const closeOracleModal = document.getElementById("closeOracleModal");
        const oracleCardName = document.getElementById("oracleCardName");
        const oracleCardQuestion = document.getElementById("oracleCardQuestion");
        const oracleCardImage = document.getElementById("oracleCardImage");
        const oracleCardContext = document.getElementById("oracleCardContext");
        const oracleCardResponse = document.getElementById("oracleCardResponse");
        const oracleModalNote = document.getElementById("oracleModalNote");
        const oracleActionRow = document.getElementById("oracleActionRow");
        const oracleConfirm = document.getElementById("oracleConfirm");
        const oracleConfirmText = document.getElementById("oracleConfirmText");
        const oracleConfirmYes = document.getElementById("oracleConfirmYes");
        const oracleConfirmNo = document.getElementById("oracleConfirmNo");
        const oraclePublishBtn = document.getElementById("oraclePublishBtn");
        const oracleSecretBtn = document.getElementById("oracleSecretBtn");
        const oracleHeartBtn = document.getElementById("oracleHeartBtn");
        const oracleHistory = document.getElementById("oracleHistory");
        const oracleHistoryList = document.getElementById("oracleHistoryList");
    
        let selectedCard = null;
        let pendingAction = null;
    
        const loadState = () => {
          const fallback = {
            cycle: 1,
            cycleStartAt: Date.now(),
            lastPickAt: null,
            revealedThisCycle: [],
            history: {}
          };
    
          try {
            const stored = localStorage.getItem(ORACLE_STATE_KEY);
            if (!stored) return fallback;
            const parsed = JSON.parse(stored);
            return {
              ...fallback,
              ...parsed,
              history: parsed.history || {}
            };
          } catch (error) {
            return fallback;
          }
        };
    
        const saveState = (state) => {
          localStorage.setItem(ORACLE_STATE_KEY, JSON.stringify(state));
        };
    
        let oracleState = loadState();
    
        const shuffleCards = (cards) => {
          const shuffled = [...cards];
          for (let i = shuffled.length - 1; i > 0; i -= 1) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
          }
          return shuffled;
        };
    
        const getCardImage = (cardId) => {
          if (cardId === 1) return "/css/oracle/Oracle9.png";
          const index = ((cardId - 1) % 13) + 1;
          return `/css/oracle/Oracle${index}.png`;
        };
    
        const formatDate = (date) => {
          const months = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
          ];
          const day = date.getDate();
          const month = months[date.getMonth()];
          let hours = date.getHours();
          const minutes = date.getMinutes().toString().padStart(2, "0");
          const isPm = hours >= 12;
          hours = hours % 12;
          hours = hours === 0 ? 12 : hours;
          const suffix = isPm ? "p.m." : "a.m.";
          return `${day} de ${month} a las ${hours}:${minutes} ${suffix}`;
        };
    
        const formatCooldown = (remainingMs) => {
          const daysLeft = Math.ceil(remainingMs / (24 * 60 * 60 * 1000));
          if (daysLeft <= 1) {
            return "En 1 día podrás elegir una nueva carta.";
          }
          return `En ${daysLeft} días podrás elegir una nueva carta.`;
        };
    
        const getCardHistory = (cardId) => {
          const entries = oracleState.history[cardId] || [];
          return entries.slice().sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        };
    
        const getCurrentCycleEntries = (cardId) => {
          return getCardHistory(cardId).filter((entry) => entry.cycle === oracleState.cycle);
        };
    
        const updateCooldownStatus = () => {
          const now = Date.now();
          const remainingMs = oracleState.lastPickAt ? Math.max(0, COOLDOWN_MS - (now - oracleState.lastPickAt)) : 0;
          const cooldownActive = remainingMs > 0;
    
          let cycleComplete = oracleState.revealedThisCycle.length >= TOTAL_CARDS;
          if (cycleComplete && remainingMs === 0) {
            oracleState = {
              ...oracleState,
              cycle: oracleState.cycle + 1,
              cycleStartAt: Date.now(),
              revealedThisCycle: []
            };
            saveState(oracleState);
            cycleComplete = false;
          }
    
          if (!cooldownActive && !cycleComplete) {
            oracleStatus.textContent = "Selecciona una carta";
            oracleCooldown.textContent = "";
          } else {
            const message = formatCooldown(remainingMs || COOLDOWN_MS);
            oracleStatus.textContent = "Carta bloqueada temporalmente";
            oracleCooldown.textContent = message;
          }
    
          return { cooldownActive, cycleComplete, remainingMs };
        };
    
        const renderOracleDeck = (cards, cooldownActive, cycleComplete, remainingMs) => {
          oracleDeck.innerHTML = "";
          oracleDeckEmpty.classList.add("hidden");
    
          const remainingCards = cards.filter((card) => !oracleState.revealedThisCycle.includes(card.id));
    
          if (remainingCards.length === 0) {
            oracleDeckEmpty.textContent = cooldownActive
              ? formatCooldown(remainingMs || COOLDOWN_MS)
              : "En 3 días podrás elegir una nueva carta.";
            oracleDeckEmpty.classList.remove("hidden");
            return;
          }
    
          remainingCards.forEach((card) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "oracle-deck-card";
            button.dataset.cardId = card.id;
            if (cooldownActive || cycleComplete) {
              button.classList.add("is-locked");
              button.disabled = true;
            }
            button.innerHTML = `<img src="/css/oracle/carta.webp" alt="Carta del Oráculo" />`;
            button.addEventListener("click", () => openOracleModal(card.id));
            oracleDeck.appendChild(button);
          });
        };
    
        const renderRevealed = () => {
          oracleRevealed.innerHTML = "";
          const revealedIds = oracleState.revealedThisCycle;
    
          if (!revealedIds.length) {
            oracleRevealedEmpty.style.display = "block";
            return;
          }
    
          oracleRevealedEmpty.style.display = "none";
    
          revealedIds.forEach((cardId) => {
            const card = oracleCards.find((item) => item.id === cardId);
            const entries = getCardHistory(cardId);
            const latest = entries[0];
            const formattedDate = latest ? formatDate(new Date(latest.date)) : "";
            const summary = latest
              ? latest.type === "heart"
                ? `${oracleUserName} decidió no responder inmediatamente y dejó esta respuesta asentándose en su corazón.`
                : latest.text || "Respuesta registrada."
              : "Carta revelada.";
    
            const cardItem = document.createElement("button");
            cardItem.type = "button";
            cardItem.className = "oracle-revealed-card";
            cardItem.innerHTML = `
              <div class="oracle-revealed-figure">
                <img src="${getCardImage(cardId)}" alt="${card?.name || "Carta revelada"}" />
              </div>
              <div class="oracle-revealed-body">
                <strong>${card?.name || "Carta revelada"}</strong>
                <p>${summary}</p>
                ${formattedDate ? `<span>Respuesta del ${formattedDate}</span>` : ""}
              </div>
            `;
            cardItem.addEventListener("click", () => openOracleModal(cardId, true));
            oracleRevealed.appendChild(cardItem);
          });
        };
    
        const renderHistory = (cardId) => {
          const entries = getCardHistory(cardId);
          oracleHistoryList.innerHTML = "";
    
          if (!entries.length) {
            oracleHistory.style.display = "none";
            return;
          }
    
          oracleHistory.style.display = "block";
    
          entries.forEach((entry) => {
            const item = document.createElement("div");
            item.className = "oracle-history-item";
            const dateText = formatDate(new Date(entry.date));
            const label = entry.type === "public"
              ? "Respuesta pública"
              : entry.type === "secret"
                ? "Respuesta secreta"
                : "Reposo en el corazón";
            const body = entry.type === "heart"
              ? `${oracleUserName} decidió no responder inmediatamente y dejó esta respuesta asentándose en su corazón.`
              : entry.text || "";
            item.innerHTML = `
              <div class="oracle-history-head">
                <span>${label}</span>
                <span>${dateText}</span>
              </div>
              <p>${body}</p>
            `;
            oracleHistoryList.appendChild(item);
          });
        };
    
        const openOracleModal = (cardId) => {
          selectedCard = oracleCards.find((card) => card.id === cardId);
          if (!selectedCard) return;
    
          const currentEntries = getCurrentCycleEntries(cardId);
          const hasAnswered = currentEntries.some((entry) => entry.type === "public" || entry.type === "secret");
          const hasHeart = currentEntries.some((entry) => entry.type === "heart");
          const latestEntry = getCardHistory(cardId)[0];
    
          oracleCardName.textContent = selectedCard.name;
          oracleCardQuestion.textContent = selectedCard.question;
          oracleCardImage.src = getCardImage(selectedCard.id);
          oracleCardContext.textContent = selectedCard.context;
    
          oracleCardResponse.value = hasAnswered && latestEntry ? latestEntry.text : "";
          oracleCardResponse.disabled = hasAnswered;
    
          if (hasAnswered) {
            const latest = currentEntries.find((entry) => entry.type === "public" || entry.type === "secret");
            oracleModalNote.textContent = latest
              ? `Respuesta registrada el ${formatDate(new Date(latest.date))}. Este texto es inmodificable.`
              : "Respuesta registrada. Este texto es inmodificable.";
            oracleActionRow.style.display = "none";
          } else {
            oracleModalNote.textContent = hasHeart
              ? "Esta carta quedó reposando en tu corazón. Puedes responder cuando lo desees durante este ciclo."
              : "Puedes responder ahora, en secreto o dejar la pregunta reposando en tu corazón.";
            oracleActionRow.style.display = "flex";
          }
    
          oracleConfirm.classList.add("hidden");
          renderHistory(cardId);
    
          oracleModalOverlay.classList.remove("hidden");
          oracleModalOverlay.setAttribute("aria-hidden", "false");
        };
    
        const closeModal = () => {
          oracleModalOverlay.classList.add("hidden");
          oracleModalOverlay.setAttribute("aria-hidden", "true");
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
          selectedCard = null;
        };
    
        const triggerConfirm = (action) => {
          pendingAction = action;
          if (action === "public") {
            oracleConfirmText.textContent = "¿Estás seguro de tu respuesta?";
          } else if (action === "secret") {
            oracleConfirmText.textContent =
              "¿Estás seguro de tu respuesta? Este mensaje quedará encriptado y privado con tu clave personal.";
          } else {
            oracleConfirmText.textContent =
              "¿Deseas dejar esta pregunta reposando en tu corazón?";
          }
          oracleConfirm.classList.remove("hidden");
        };
    
        const finalizeResponse = () => {
          if (!selectedCard || !pendingAction) return;
          const now = new Date();
          const responseText = oracleCardResponse.value.trim();
    
          const entry = {
            type: pendingAction,
            text: responseText,
            date: now.toISOString(),
            cycle: oracleState.cycle
          };
    
          if (!oracleState.history[selectedCard.id]) {
            oracleState.history[selectedCard.id] = [];
          }
          if (pendingAction === "heart") {
            entry.text = "";
          }
    
          oracleState.history[selectedCard.id].push(entry);
    
          const isNewReveal = !oracleState.revealedThisCycle.includes(selectedCard.id);
          if (isNewReveal) {
            oracleState.revealedThisCycle.push(selectedCard.id);
            oracleState.lastPickAt = now.getTime();
          }
          saveState(oracleState);
    
          closeModal();
          renderAll();
        };
    
        const renderAll = () => {
          const shuffled = shuffleCards(oracleCards);
          const { cooldownActive, cycleComplete, remainingMs } = updateCooldownStatus();
          renderOracleDeck(shuffled, cooldownActive, cycleComplete, remainingMs);
          renderRevealed();
        };
    
        oraclePublishBtn.addEventListener("click", () => triggerConfirm("public"));
        oracleSecretBtn.addEventListener("click", () => triggerConfirm("secret"));
        oracleHeartBtn.addEventListener("click", () => triggerConfirm("heart"));
    
        oracleConfirmYes.addEventListener("click", finalizeResponse);
        oracleConfirmNo.addEventListener("click", () => {
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
        });
    
        closeOracleModal.addEventListener("click", closeModal);
        oracleModalOverlay.addEventListener("click", (event) => {
          if (event.target === oracleModalOverlay) closeModal();
        });
    
        renderAll();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — Oráculo</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user oracle-background">

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

      <div class="oracle-body">
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
         *  ORACULO
         *  ========================= -->
        <section class="oracle-shell" aria-label="Oráculo">
          <header class="oracle-head">
            <div>
              <h2 class="oracle-title">El Oráculo</h2>
              <p class="oracle-subtitle">
                Selecciona una carta para comprender tu presente. Solo una carta cada 3 días.
              </p>
            </div>
            <div class="oracle-tags">
              <span class="panel-badge">30 cartas</span>
              <span class="panel-badge">Ciclos de 90 días</span>
              <span class="panel-badge">Reflexión personal</span>
            </div>
          </header>

          <section class="panel oracle-intro" aria-label="¿Qué es el Oráculo?">
            <div class="panel-head">
              <h3 class="panel-title">¿Qué es el Oráculo?</h3>
              <span class="panel-badge">Herramienta de reflexión</span>
            </div>
            <p class="panel-text">
              El Oráculo es una herramienta de reflexión de Kiadez.com. Eliges una carta, no para adivinar tu futuro,
              sino para comprender tu presente. Actualmente el Oráculo está compuesto de 30 cartas y solo puedes
              seleccionar una sola cada 3 días. La carta te planteará una pregunta, que puedes responder inmediatamente
              o dejar reposando en tu corazón. Si eres juicioso y disciplinado, responderás la pregunta que te propone
              la carta hasta 4 veces a lo largo de un solo año. Eso te permitirá reconocer cuánto has progresado en el
              camino de conocerte a ti mismo.
            </p>
          </section>

          <section class="panel oracle-deck" aria-label="Cartas no reveladas">
            <div class="oracle-deck-head">
              <div>
                <h3>Cartas no reveladas</h3>
                <p class="oracle-status" id="oracleStatus">Selecciona una carta</p>
              </div>
              <div class="oracle-deck-note" id="oracleCooldown"></div>
            </div>
            <div class="oracle-grid" id="oracleDeck"></div>
            <div class="oracle-empty hidden" id="oracleDeckEmpty">
              En 3 días podrás elegir una nueva carta.
            </div>
          </section>

          <section class="panel oracle-revealed" aria-label="Cartas reveladas">
            <div class="panel-head">
              <h3 class="panel-title">Cartas reveladas</h3>
              <span class="panel-badge">Respuestas registradas</span>
            </div>
            <div class="oracle-revealed-grid" id="oracleRevealed"></div>
            <div class="oracle-empty" id="oracleRevealedEmpty">
              Aún no has revelado cartas. Cuando selecciones una, aparecerá aquí.
            </div>
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
              <li><a href="/?lang=pt">Português</a></li>
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

  <!-- =========================
   *  MODAL: CARTA SELECCIONADA
   *  ========================= -->
  <div class="modal-overlay hidden" id="oracleModalOverlay" aria-hidden="true">
    <div class="modal modal-wide oracle-modal" role="dialog" aria-modal="true" aria-label="Carta seleccionada">
      <div class="modal-head">
        <div>
          <h3 id="oracleCardName">Nombre de la carta</h3>
          <p class="oracle-card-question" id="oracleCardQuestion"></p>
        </div>
        <button class="modal-close" type="button" id="closeOracleModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="oracle-modal-top">
          <div class="oracle-card-figure">
            <img id="oracleCardImage" src="/css/oracle/Oracle9.png" alt="Carta del Oráculo" />
          </div>
          <div class="oracle-card-context">
            <h4>Contexto</h4>
            <p id="oracleCardContext"></p>
          </div>
        </div>

        <label class="modal-label" for="oracleCardResponse">Cajón de texto</label>
        <textarea class="modal-textarea" id="oracleCardResponse" rows="6"
          placeholder="Escribe tu respuesta..."></textarea>
        <div class="oracle-modal-note" id="oracleModalNote"></div>

        <div class="oracle-action-row" id="oracleActionRow">
          <button class="btn btn-primary btn-compact" type="button" id="oraclePublishBtn">Responder ahora y
            publicar</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleSecretBtn">Responder en secreto</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleHeartBtn">Dejar esta pregunta reposando
            en mi corazón</button>
        </div>

        <div class="oracle-confirm hidden" id="oracleConfirm">
          <p id="oracleConfirmText"></p>
          <div class="oracle-confirm-actions">
            <button class="btn btn-primary btn-compact" type="button" id="oracleConfirmYes">Sí</button>
            <button class="btn btn-outline btn-compact" type="button" id="oracleConfirmNo">No</button>
          </div>
        </div>

        <div class="oracle-history" id="oracleHistory">
          <h4>Respuestas anteriores</h4>
          <div class="oracle-history-list" id="oracleHistoryList"></div>
        </div>
      </div>
    </div>
  </div>
