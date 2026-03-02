<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { getLocale } from "../lib/i18n";
  import { logout } from "../lib/logout";
  import { initPurposeCoverModule } from "../lib/purposeCover";

  const locale = getLocale();
  const isEn = locale === "en";
  const isFr = locale === "fr";
  const tr = (es, en, fr = en) => (isEn ? en : isFr ? fr : es);

  onMount(() => {
    document.body.dataset.visitor = "false";
    initPurposeCoverModule();

    const oracleCards = [
      {
        id: 1,
        name: tr("El Ciclo", "The Cycle", "Le Cycle"),
        question: tr(
          "¿Cuál es tu ciclo de las reencarnaciones?",
          "What recurring cycle keeps returning in your life?",
          "Quel cycle récurrent revient sans cesse dans ta vie?"
        ),
        context: tr(
          "Enfocado en comprender situaciones que perturban tu viaje en este mundo. En tu vida diaria, ¿qué es eso que va y vuelve de la misma manera, por más que intentes evitarlo? Por ejemplo: discusiones repetidas, una adicción, un patrón emocional o el deseo constante de tener más de algo.",
          "Focused on understanding situations that disturb your journey in this world. In your daily life, what keeps coming back in the same way even when you try to avoid it? For example: repeated arguments, an addiction, an emotional pattern, or the constant desire for more."
        ),
      },
      {
        id: 2,
        name: tr("La Calma", "Calm", "Le Calme"),
        question: tr(
          "Si pudieras vivir tu vida desde la calma, ¿qué decisión tomarías hoy?",
          "If you could live your life from calm, what decision would you make today?",
          "Si tu pouvais vivre ta vie depuis le calme, quelle décision prendrais-tu aujourd'hui?"
        ),
        context: tr(
          "Enfocado en comprender por qué actúas como actúas actualmente. ¿Qué es lo que realmente te presiona a decidir con prisa? ¿Qué limita tu pensamiento, tu espíritu o tu manera natural de ser en este momento de tu vida?",
          "Focused on understanding why you act the way you do right now. What truly pressures you to decide in a hurry? What limits your thinking, your spirit, or your natural way of being in this season of your life?"
        ),
      },
      {
        id: 3,
        name: tr("El Silencio", "Silence", "Le Silence"),
        question: tr("¿Te cuesta mantenerte en silencio?", "Is it hard for you to stay in silence?", "As-tu du mal à rester en silence ?"),
        context: tr(
          "Enfocado en comprender si puedes escuchar tu propio pensamiento o si actúas solo por impulso. ¿Cuál es tu relación con el silencio? ¿Puedes estar diez minutos sin estímulos o sientes la necesidad de llenar ese espacio con música, pantallas o distracciones?",
          "Focused on understanding whether you can listen to your own thoughts or if you act only on impulse. What is your relationship with silence? Can you spend ten minutes without stimuli, or do you feel the need to fill that space with music, screens, or distractions?"
        ),
      },
      {
        id: 4,
        name: tr("El Anhelo", "Longing", "Le Désir"),
        question: tr("¿Cuál sería la vida de tus sueños?", "What would the life of your dreams look like?", "À quoi ressemblerait la vie de tes rêves ?"),
        context: tr(
          "Enfocado en reconocer qué sientes que te falta para sentirte pleno. Si hoy fuera el último día de tu vida, ¿qué considerarías que no viviste? ¿Qué cualidades, experiencias o formas de ser te hubiera gustado manifestar?",
          "Focused on recognizing what you feel is missing to feel fulfilled. If today were the last day of your life, what would you feel you did not live? What qualities, experiences, or ways of being would you have liked to express?"
        ),
      },
      {
        id: 5,
        name: tr("La Elección", "The Choice", "Le Choix"),
        question: tr(
          "Si pudieras cambiar algo del mundo, ¿qué elegirías?",
          "If you could change something in the world, what would you choose?",
          "Si tu pouvais changer quelque chose du monde, que choisirais-tu ?"
        ),
        context: tr(
          "Enfocado en identificar aquello con lo que no estás de acuerdo. ¿Qué crees que no debería existir ni en tu vida ni en la de los demás? Si pudieras eliminarlo, ¿el mundo sería mejor? ¿Tú te sentirías más libre o en paz?",
          "Focused on identifying what you disagree with. What do you believe should not exist in your life or in others' lives? If you could remove it, would the world be better? Would you feel freer or more at peace?"
        ),
      },
      {
        id: 6,
        name: tr("La Libertad", "Freedom", "La Liberté"),
        question: tr("¿Te consideras una persona libre?", "Do you consider yourself a free person?", "Te considères-tu comme une personne libre ?"),
        context: tr(
          "Enfocado en reconocer cómo te sientes con la vida que llevas. ¿Existe algo que percibas como una carga constante? ¿Alguna situación física, emocional o mental que afecte tu día a día? ¿O te sientes realmente cómodo con tu forma de vivir?",
          "Focused on recognizing how you feel about the life you are living. Is there something you perceive as a constant burden? Any physical, emotional, or mental situation affecting your day-to-day life? Or do you truly feel comfortable with your way of living?"
        ),
      },
      {
        id: 7,
        name: tr("La Sombra", "The Shadow", "L'Ombre"),
        question: tr(
          "¿Qué es lo que más evitas mirar de ti?",
          "What do you avoid seeing in yourself the most?",
          "Qu'est-ce que tu évites le plus de regarder en toi ?"
        ),
        context: tr(
          "Enfocado en reconocer aquello que prefieres no enfrentar. Puede ser una emoción, un recuerdo, una actitud o una verdad incómoda. A veces lo que evitamos mirar es justamente lo que más necesita atención para poder transformarse.",
          "Focused on recognizing what you prefer not to face. It can be an emotion, a memory, an attitude, or an uncomfortable truth. Sometimes what we avoid seeing is exactly what most needs attention to be transformed."
        ),
      },
      {
        id: 8,
        name: tr("El Refugio", "Refuge", "Le Refuge"),
        question: tr("¿Qué te hace sentir en casa?", "What makes you feel at home?", "Qu'est-ce qui te fait te sentir chez toi ?"),
        context: tr(
          "Enfocado en identificar aquello que te brinda seguridad y tranquilidad. Puede ser un lugar, una persona, una actividad o un estado interior. Reconocerlo te ayuda a saber dónde recargar tu energía cuando la vida se vuelve exigente.",
          "Focused on identifying what gives you safety and calm. It can be a place, a person, an activity, or an inner state. Recognizing it helps you know where to recharge your energy when life becomes demanding."
        ),
      },
      {
        id: 9,
        name: tr("El Gozo", "Joy", "La Joie"),
        question: tr(
          "¿Qué parte de tu día disfrutas más?",
          "Which part of your day do you enjoy the most?",
          "Quelle partie de ta journée apprécies-tu le plus ?"
        ),
        context: tr(
          "Enfocado en observar qué momentos te conectan con el gozo. A veces la felicidad no está en grandes logros, sino en instantes simples que solemos pasar por alto. ¿Qué te dice eso sobre lo que realmente valoras?",
          "Focused on observing which moments connect you with joy. Happiness is not always in big achievements, but in simple moments we often overlook. What does that tell you about what you truly value?"
        ),
      },
      {
        id: 10,
        name: tr("El Desgaste", "Drain", "L'Épuisement"),
        question: tr("¿Qué te roba más energía?", "What drains your energy the most?", "Qu'est-ce qui te vole le plus d'énergie ?"),
        context: tr(
          "Enfocado en reconocer hábitos, personas o pensamientos que te desgastan. Identificar qué te drena es el primer paso para proteger tu bienestar y tomar decisiones más conscientes sobre a qué le entregas tu tiempo y tu atención.",
          "Focused on recognizing habits, people, or thoughts that wear you down. Identifying what drains you is the first step to protecting your well-being and making more conscious decisions about where your time and attention go."
        ),
      },
      {
        id: 11,
        name: tr("El Aprendiz", "The Learner", "L'Apprenant"),
        question: tr("¿Qué te gustaría aprender?", "What would you like to learn?", "Qu'aimerais-tu apprendre ?"),
        context: tr(
          "Enfocado en conectar con tu curiosidad natural. Aprender no siempre tiene que ver con estudios formales; puede ser una habilidad, una forma de vivir o una manera distinta de relacionarte contigo y con los demás.",
          "Focused on connecting with your natural curiosity. Learning is not always about formal studies; it can be a skill, a way of living, or a different way of relating to yourself and others."
        ),
      },
      {
        id: 12,
        name: tr("El Mérito", "Merit", "Le Mérite"),
        question: tr(
          "¿Cuándo fue la última vez que te sentiste orgulloso de ti?",
          "When was the last time you felt proud of yourself?",
          "Quand t'es-tu senti fier de toi pour la dernière fois ?"
        ),
        context: tr(
          "Enfocado en reconocer tus propios logros, grandes o pequeños. Muchas veces avanzamos sin detenernos a valorar lo que hemos superado. Recordarlo fortalece la autoestima y el respeto por tu propio camino.",
          "Focused on recognizing your own achievements, big or small. Many times we move forward without stopping to value what we have overcome. Remembering it strengthens self-esteem and respect for your own path."
        ),
      },
      {
        id: 13,
        name: tr("El Apego", "Attachment", "L'Attachement"),
        question: tr("¿Qué te da miedo perder?", "What are you afraid of losing?", "Qu'as-tu peur de perdre ?"),
        context: tr(
          "Enfocado en identificar apegos importantes en tu vida. El miedo a perder algo suele revelar cuánto valor le damos y cuánto dependemos de ello. Observarlo con honestidad ayuda a comprender nuestras decisiones.",
          "Focused on identifying important attachments in your life. Fear of losing something often reveals how much value we assign to it and how dependent we are on it. Looking at it honestly helps us understand our decisions."
        ),
      },
      {
        id: 14,
        name: tr("La Vitalidad", "Vitality", "La Vitalité"),
        question: tr("¿Qué te hace sentir vivo?", "What makes you feel alive?", "Qu'est-ce qui te fait te sentir vivant ?"),
        context: tr(
          "Enfocado en descubrir aquello que despierta tu entusiasmo. Puede ser crear, ayudar, aprender, moverte o compartir. Reconocerlo te orienta hacia una vida más alineada con lo que te nutre internamente.",
          "Focused on discovering what awakens your enthusiasm. It can be creating, helping, learning, moving, or sharing. Recognizing it guides you toward a life more aligned with what nourishes you internally."
        ),
      },
      {
        id: 15,
        name: tr("La Demora", "Delay", "Le Report"),
        question: tr("¿Qué sueles postergar?", "What do you usually postpone?", "Qu'as-tu tendance à remettre à plus tard ?"),
        context: tr(
          "Enfocado en observar aquello que dejas para después. A veces no se trata de pereza, sino de miedo, cansancio o falta de claridad. Entender por qué postergas algo puede darte pistas importantes sobre lo que necesitas.",
          "Focused on observing what you leave for later. Sometimes it is not laziness, but fear, exhaustion, or lack of clarity. Understanding why you postpone something can give you important clues about what you need."
        ),
      },
      {
        id: 16,
        name: tr("La Gratitud", "Gratitude", "La Gratitude"),
        question: tr("¿Qué agradeces hoy?", "What are you grateful for today?", "De quoi es-tu reconnaissant aujourd'hui ?"),
        context: tr(
          "Enfocado en ejercitar la gratitud consciente. Incluso en días difíciles siempre hay algo que reconocer. Agradecer no niega los problemas, pero cambia la forma en que los miras y los atraviesas.",
          "Focused on practicing conscious gratitude. Even on difficult days there is always something to acknowledge. Being grateful does not deny problems, but it changes the way you look at and move through them."
        ),
      },
      {
        id: 17,
        name: tr("La Voz", "Voice", "La Voix"),
        question: tr(
          "¿Qué te gustaría decir y no has dicho?",
          "What would you like to say that you have not said yet?",
          "Qu'aimerais-tu dire que tu n'as pas encore dit ?"
        ),
        context: tr(
          "Enfocado en reconocer palabras retenidas. A veces callamos por miedo a herir, a perder o a exponernos. Identificar lo que no expresas te ayuda a entender qué necesitas comunicar, aunque sea primero contigo mismo.",
          "Focused on recognizing words held back. Sometimes we stay silent out of fear of hurting, losing, or exposing ourselves. Identifying what you do not express helps you understand what you need to communicate, even if first only to yourself."
        ),
      },
      {
        id: 18,
        name: tr("La Paz", "Peace", "La Paix"),
        question: tr("¿Qué te hace sentir en paz?", "What makes you feel at peace?", "Qu'est-ce qui te fait te sentir en paix ?"),
        context: tr(
          "Enfocado en identificar estados, actividades o relaciones que aquietan tu mente. La paz no siempre llega sola; muchas veces se construye al elegir conscientemente aquello que te devuelve equilibrio.",
          "Focused on identifying states, activities, or relationships that quiet your mind. Peace does not always arrive on its own; often it is built by consciously choosing what brings you back to balance."
        ),
      },
      {
        id: 19,
        name: tr("El Cuidado", "Care", "Le Soin"),
        question: tr(
          "¿Qué parte de tu vida necesita más atención?",
          "Which part of your life needs more attention?",
          "Quelle partie de ta vie a le plus besoin d'attention ?"
        ),
        context: tr(
          "Enfocado en observar áreas descuidadas. Puede ser tu cuerpo, tus emociones, tus vínculos o tu descanso. Detectarlo a tiempo permite pequeños ajustes antes de que el desequilibrio se haga mayor.",
          "Focused on observing neglected areas. It can be your body, your emotions, your relationships, or your rest. Detecting it in time allows small adjustments before imbalance grows."
        ),
      },
      {
        id: 20,
        name: tr("La Lección", "Lesson", "La Leçon"),
        question: tr("¿Qué te enseñó tu último error?", "What did your last mistake teach you?", "Qu'est-ce que ta dernière erreur t'a appris ?"),
        context: tr(
          "Enfocado en resignificar el error como aprendizaje. Más allá de la culpa o la frustración, cada error deja una lección. Reconocerla te permite avanzar con más claridad y menos peso.",
          "Focused on reframing mistakes as learning. Beyond guilt or frustration, every mistake leaves a lesson. Recognizing it allows you to move forward with greater clarity and less weight."
        ),
      },
      {
        id: 21,
        name: tr("Lo Esencial", "The Essential", "L'Essentiel"),
        question: tr("¿Qué te gustaría simplificar?", "What would you like to simplify?", "Qu'aimerais-tu simplifier ?"),
        context: tr(
          "Enfocado en identificar excesos. A veces complicamos nuestra vida más de lo necesario. Simplificar puede significar soltar objetos, compromisos, pensamientos o expectativas que ya no te aportan bienestar.",
          "Focused on identifying excess. Sometimes we complicate our lives more than necessary. Simplifying can mean letting go of objects, commitments, thoughts, or expectations that no longer support your well-being."
        ),
      },
      {
        id: 22,
        name: tr("El Cuerpo", "The Body", "Le Corps"),
        question: tr("¿Qué te conecta con tu cuerpo?", "What connects you with your body?", "Qu'est-ce qui te connecte à ton corps ?"),
        context: tr(
          "Enfocado en reconocer cómo habitas tu cuerpo. Puede ser el movimiento, la respiración, el descanso o la alimentación. Escuchar al cuerpo es una forma directa de volver al presente.",
          "Focused on recognizing how you inhabit your body. It can be movement, breathing, rest, or nourishment. Listening to your body is a direct way to return to the present."
        ),
      },
      {
        id: 23,
        name: tr("El Vínculo", "The Bond", "Le Lien"),
        question: tr("¿Qué te hace sentir acompañado?", "What makes you feel accompanied?", "Qu'est-ce qui te fait te sentir accompagné ?"),
        context: tr(
          "Enfocado en identificar vínculos reales. No siempre se trata de estar rodeado de gente, sino de sentir comprensión y presencia. Reconocerlo te ayuda a cuidar mejor tus relaciones.",
          "Focused on identifying real bonds. It is not always about being surrounded by people, but about feeling understanding and presence. Recognizing it helps you care for your relationships better."
        ),
      },
      {
        id: 24,
        name: tr("La Liberación", "Release", "Le Lâcher-prise"),
        question: tr("¿Qué te gustaría soltar?", "What would you like to let go of?", "Qu'aimerais-tu lâcher ?"),
        context: tr(
          "Enfocado en observar cargas innecesarias. Puede ser un resentimiento, una culpa, una expectativa o un hábito. Soltar no es olvidar, es liberar espacio para algo nuevo.",
          "Focused on observing unnecessary burdens. It can be resentment, guilt, an expectation, or a habit. Letting go is not forgetting; it is creating room for something new."
        ),
      },
      {
        id: 25,
        name: tr("El Futuro", "The Future", "Le Futur"),
        question: tr("¿Qué te entusiasma del futuro?", "What excites you about the future?", "Qu'est-ce qui t'enthousiasme dans l'avenir ?"),
        context: tr(
          "Enfocado en conectar con la esperanza. Pensar en lo que viene no como ansiedad, sino como posibilidad. Reconocer qué te ilusiona te da dirección y energía para el presente.",
          "Focused on connecting with hope. Thinking about what comes next not as anxiety, but as possibility. Recognizing what excites you gives you direction and energy for the present."
        ),
      },
      {
        id: 26,
        name: tr("El Aporte", "Contribution", "La Contribution"),
        question: tr("¿Qué te hace sentir útil?", "What makes you feel useful?", "Qu'est-ce qui te fait te sentir utile ?"),
        context: tr(
          "Enfocado en reconocer tu aporte al mundo. Sentirte útil no depende de grandes logros, sino de saber que lo que haces tiene sentido para ti o para otros.",
          "Focused on recognizing your contribution to the world. Feeling useful does not depend on big achievements, but on knowing that what you do has meaning for you or for others."
        ),
      },
      {
        id: 27,
        name: tr("El Reposo", "Rest", "Le Repos"),
        question: tr("¿Qué necesitas descansar?", "What do you need to let rest?", "Qu'as-tu besoin de laisser au repos ?"),
        context: tr(
          "Enfocado en identificar cansancios acumulados. A veces no es solo el cuerpo, sino la mente o el corazón. Reconocerlo es el primer paso para darte permiso de pausar.",
          "Focused on identifying accumulated fatigue. Sometimes it is not only the body, but also the mind or the heart. Recognizing it is the first step to giving yourself permission to pause."
        ),
      },
      {
        id: 28,
        name: tr("La Protección", "Protection", "La Protection"),
        question: tr("¿Qué te gustaría cuidar más?", "What would you like to protect more?", "Qu'aimerais-tu protéger davantage ?"),
        context: tr(
          "Enfocado en reconocer aquello que valoras. Puede ser tu salud, una relación, un sueño o tu tiempo. Cuidar algo implica presencia y decisiones conscientes.",
          "Focused on recognizing what you value. It can be your health, a relationship, a dream, or your time. Caring for something requires presence and conscious decisions."
        ),
      },
      {
        id: 29,
        name: tr("La Identidad", "Identity", "L'Identité"),
        question: tr("¿Qué te recuerda quién eres?", "What reminds you of who you are?", "Qu'est-ce qui te rappelle qui tu es ?"),
        context: tr(
          "Enfocado en identificar anclas personales. Puede ser una actividad, una persona, un recuerdo o un valor. Reconocerlo te ayuda a no perderte cuando todo alrededor cambia.",
          "Focused on identifying personal anchors. It can be an activity, a person, a memory, or a value. Recognizing it helps you not lose yourself when everything around you changes."
        ),
      },
      {
        id: 30,
        name: tr("La Intención", "Intention", "L'Intention"),
        question: tr("¿Qué intención eliges para hoy?", "What intention do you choose for today?", "Quelle intention choisis-tu pour aujourd'hui ?"),
        context: tr(
          "Enfocado en cerrar el ciclo con conciencia. Elegir una intención no es imponer un resultado, sino orientar tu forma de estar en el día. Una pequeña intención puede transformar toda una jornada.",
          "Focused on closing the cycle with awareness. Choosing an intention is not imposing an outcome, but guiding how you show up in your day. A small intention can transform an entire day."
        ),
      },
    ];

    const API = "http://127.0.0.1:8000";
    const AAD_VAULT = new TextEncoder().encode("kiadez-vault-v1");
    const ORACLE_AAD_PREFIX = "kiadez-oracle-v1";
    const COOLDOWN_MS = 72 * 60 * 60 * 1000;
    const YEAR_MS = 365 * 24 * 60 * 60 * 1000;
    const MAX_HISTORY_ENTRIES = 4;
    const MAX_RESPONSE_WORDS = 500;
    const TOTAL_CARDS = oracleCards.length;
    let isViewingOwnProfile = true;
    let viewerUserId = null;
    let viewerUsername = "";
    let activeProfileUserId = null;
    let activeProfileUsername = "";
    let activeProfileFullName = "";
    let oracleUserName = tr("Usuario Kiadez", "Kiadez User", "Utilisateur Kiadez");

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
    const oracleWordCounter = document.getElementById("oracleWordCounter");
    const oracleModalNote = document.getElementById("oracleModalNote");
    const oracleActionRow = document.getElementById("oracleActionRow");
    const oracleSecretActions = document.getElementById("oracleSecretActions");
    const oracleRevealSecretBtn = document.getElementById("oracleRevealSecretBtn");
    const oracleSecretUnlock = document.getElementById("oracleSecretUnlock");
    const oracleSecretUnlockPassword = document.getElementById("oracleSecretUnlockPassword");
    const oracleSecretUnlockError = document.getElementById("oracleSecretUnlockError");
    const oracleSecretUnlockConfirm = document.getElementById("oracleSecretUnlockConfirm");
    const oracleSecretUnlockCancel = document.getElementById("oracleSecretUnlockCancel");
    const oracleConfirm = document.getElementById("oracleConfirm");
    const oracleConfirmText = document.getElementById("oracleConfirmText");
    const oracleConfirmYes = document.getElementById("oracleConfirmYes");
    const oracleConfirmNo = document.getElementById("oracleConfirmNo");
    const oraclePrivatePasswordWrap = document.getElementById("oraclePrivatePasswordWrap");
    const oraclePrivatePasswordInput = document.getElementById("oraclePrivatePassword");
    const oraclePrivatePasswordError = document.getElementById("oraclePrivatePasswordError");
    const oraclePublishBtn = document.getElementById("oraclePublishBtn");
    const oracleSecretBtn = document.getElementById("oracleSecretBtn");
    const oracleHeartBtn = document.getElementById("oracleHeartBtn");
    const oracleHistory = document.getElementById("oracleHistory");
    const oracleHistoryNote = document.getElementById("oracleHistoryNote");
    const oracleHistoryList = document.getElementById("oracleHistoryList");

    const buildFallbackState = () => ({
      cycle: 1,
      cycleStartAt: Date.now(),
      lastPickAt: null,
      cooldownMs: COOLDOWN_MS,
      cooldownRemainingMs: 0,
      cycleComplete: false,
      revealedThisCycle: [],
      history: {}
    });

    let oracleState = buildFallbackState();
    const oracleEntriesById = new Map();
    let selectedCard = null;
    let pendingAction = null;
    let pendingDeleteEntryId = null;
    let pendingSecretRevealEntryId = null;
    let isSubmitting = false;

    const bufToHex = (buf) =>
      [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

    const hexToBuf = (hex) => {
      const normalized = (hex || "").trim();
      if (!normalized) return new ArrayBuffer(0);
      const bytes = new Uint8Array(normalized.length / 2);
      for (let i = 0; i < bytes.length; i += 1) {
        bytes[i] = parseInt(normalized.substr(i * 2, 2), 16);
      }
      return bytes.buffer;
    };

    const getAccessToken = () =>
      localStorage.getItem("access_token") || localStorage.getItem("kiadez_access_token") || "";

    const countWords = (text) => {
      const value = String(text || "").trim();
      if (!value) return 0;
      return value.split(/\s+/).filter(Boolean).length;
    };

    const updateWordCounter = () => {
      if (!oracleWordCounter) return 0;
      const words = countWords(oracleCardResponse?.value || "");
      oracleWordCounter.textContent = tr(
        `${words}/${MAX_RESPONSE_WORDS} palabras`,
        `${words}/${MAX_RESPONSE_WORDS} words`
      );
      oracleWordCounter.classList.toggle("is-exceeded", words > MAX_RESPONSE_WORDS);
      return words;
    };

    const setPrivatePasswordError = (message) => {
      if (!oraclePrivatePasswordError) return;
      oraclePrivatePasswordError.textContent = message || "";
    };

    const setSecretUnlockError = (message) => {
      if (!oracleSecretUnlockError) return;
      oracleSecretUnlockError.textContent = message || "";
    };

    const resetSecretUnlockUi = () => {
      pendingSecretRevealEntryId = null;
      if (oracleSecretUnlock) {
        oracleSecretUnlock.classList.add("hidden");
      }
      if (oracleSecretUnlockPassword) {
        oracleSecretUnlockPassword.value = "";
      }
      setSecretUnlockError("");
    };

    const openSecretUnlockUi = (entryId) => {
      const id = Number(entryId || 0);
      if (!Number.isFinite(id) || id <= 0) return;
      pendingSecretRevealEntryId = id;
      pendingAction = null;
      pendingDeleteEntryId = null;
      oracleConfirm.classList.add("hidden");
      if (oracleSecretUnlock) {
        oracleSecretUnlock.classList.remove("hidden");
      }
      setSecretUnlockError("");
      setTimeout(() => oracleSecretUnlockPassword?.focus(), 0);
    };

    const resetPrivatePasswordUi = () => {
      if (oraclePrivatePasswordWrap) {
        oraclePrivatePasswordWrap.classList.add("hidden");
      }
      if (oraclePrivatePasswordInput) {
        oraclePrivatePasswordInput.value = "";
      }
      setPrivatePasswordError("");
    };

    const showPrivatePasswordUi = () => {
      if (oraclePrivatePasswordWrap) {
        oraclePrivatePasswordWrap.classList.remove("hidden");
      }
      setPrivatePasswordError("");
      setTimeout(() => oraclePrivatePasswordInput?.focus(), 0);
    };

    const parseResponseJson = async (res) => {
      try {
        return await res.json();
      } catch {
        return {};
      }
    };

    const apiFetch = async (path, options = {}) => {
      const token = getAccessToken();
      if (!token) {
        window.location.href = "/login.html";
        throw new Error(tr("No hay sesión activa.", "No active session.", "Aucune session active."));
      }
      const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      };

      const res = await fetch(`${API}${path}`, { ...options, headers });
      if (res.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("kiadez_access_token");
        window.location.href = "/login.html";
        throw new Error(tr("Sesión expirada.", "Session expired.", "Session expirée."));
      }
      return res;
    };

    const normalizeUsername = (value) => {
      let normalized = String(value || "").trim().toLowerCase();
      while (normalized.startsWith("@")) normalized = normalized.slice(1);
      return normalized;
    };

    const fetchViewerIdentity = async () => {
      const res = await apiFetch("/auth/me");
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo cargar tu perfil.", "Could not load your profile.", "Impossible de charger ton profil."));
      }
      const userId = Number(data?.user_number);
      return {
        user_id: Number.isFinite(userId) && userId > 0 ? userId : null,
        username: normalizeUsername(data?.username || ""),
      };
    };

    const fetchFollowProfile = async ({ userId = null, username = null } = {}) => {
      const idValue = Number(userId);
      const usernameValue = normalizeUsername(username || "");
      if (Number.isFinite(idValue) && idValue > 0) {
        const res = await apiFetch(`/follows/profile?user_id=${encodeURIComponent(String(idValue))}`);
        const data = await parseResponseJson(res);
        if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load profile.", "Impossible de charger le profil."));
        return data;
      }
      if (usernameValue) {
        const res = await apiFetch(`/follows/profile?username=${encodeURIComponent(usernameValue)}`);
        const data = await parseResponseJson(res);
        if (!res.ok) throw new Error(data.detail || tr("No se pudo cargar el perfil.", "Could not load profile.", "Impossible de charger le profil."));
        return data;
      }
      throw new Error(tr("Parámetros inválidos para cargar perfil.", "Invalid parameters to load profile.", "Paramètres invalides pour charger le profil."));
    };

    const buildViewerHomeUrl = () => {
      if (viewerUsername) return `/home_user.html?u=${encodeURIComponent(viewerUsername)}`;
      if (viewerUserId) return `/home_user.html?id=${encodeURIComponent(String(viewerUserId))}`;
      return "/home_user.html";
    };

    const buildProfileQueryParams = () => {
      if (activeProfileUsername) return { key: "u", value: activeProfileUsername };
      if (activeProfileUserId) return { key: "id", value: String(activeProfileUserId) };
      return null;
    };

    const buildProfileModuleUrl = (path) => {
      const raw = String(path || "").trim();
      if (!raw) return "";
      try {
        const url = new URL(raw, window.location.origin);
        const qp = buildProfileQueryParams();
        url.searchParams.delete("u");
        url.searchParams.delete("id");
        if (qp) url.searchParams.set(qp.key, qp.value);
        return `${url.pathname}${url.search}`;
      } catch {
        return raw;
      }
    };

    const PROFILE_MODULE_ROUTES = {
      home: "/home_user.html",
      public_wishes: "/my-public-whishes.html",
      fulfilled_wishes: "/my-fulfilled-whises.html",
      calendar: "/calendar.html",
      oracle: "/oracle.html",
    };

    const syncProfileModuleLinks = () => {
      document.querySelectorAll("a[data-profile-module]").forEach((link) => {
        const key = String(link.getAttribute("data-profile-module") || "").trim();
        const basePath = PROFILE_MODULE_ROUTES[key] || link.getAttribute("href") || "";
        const nextHref = buildProfileModuleUrl(basePath);
        if (nextHref) link.href = nextHref;
      });
    };

    const setMyHomeLinks = (href) => {
      const nextHref = String(href || "").trim();
      if (!nextHref) return;
      document.querySelectorAll("a[data-my-home]").forEach((link) => {
        link.href = nextHref;
      });
    };

    const applyReadOnlyProfileMode = () => {
      document.body.dataset.visitor = "true";
      document.querySelectorAll('a[href="/my-private-whishes.html"]').forEach((link) => link.classList.add("hidden"));
      document.getElementById("btnChangeCover")?.classList.add("hidden");
      document.getElementById("btnEditPurposes")?.classList.add("hidden");
      document.querySelectorAll(".purpose-side-btn").forEach((btn) => btn.classList.add("hidden"));
      document.querySelector(".oracle-deck")?.classList.add("hidden");
    };

    const applyOracleHeader = () => {
      const title = document.querySelector(".oracle-title");
      if (title) {
        title.textContent = isViewingOwnProfile
          ? tr("El Oráculo", "The Oracle", "L'Oracle")
          : tr(
              `Oráculo de ${activeProfileFullName || "usuario"}`,
              `Oracle of ${activeProfileFullName || "user"}`,
              `Oracle de ${activeProfileFullName || "utilisateur"}`
            );
      }
      const subtitle = document.querySelector(".oracle-subtitle");
      if (subtitle) {
        subtitle.textContent = isViewingOwnProfile
          ? tr(
            "Selecciona una carta para comprender tu presente. Solo una carta cada 3 días.",
            "Select a card to understand your present. Only one card every 3 days."
          )
          : tr(
              "Solo podrás ver las respuestas públicas de este usuario.",
              "You can only view this user's public answers.",
              "Tu peux seulement voir les réponses publiques de cet utilisateur."
            );
      }
      document.title = isViewingOwnProfile
        ? tr("Kiadez — Oráculo", "Kiadez — Oracle", "Kiadez — Oracle")
        : tr(
            `Kiadez — Oráculo de ${activeProfileFullName || "usuario"}`,
            `Kiadez — Oracle of ${activeProfileFullName || "user"}`,
            `Kiadez — Oracle de ${activeProfileFullName || "utilisateur"}`
          );
      if (!isViewingOwnProfile && oracleRevealedEmpty) {
        oracleRevealedEmpty.textContent = tr(
          "Aún no hay cartas públicas reveladas.",
          "No public cards have been revealed yet.",
          "Aucune carte publique n'a encore été révélée."
        );
      }
    };

    const resolveProfileContext = async () => {
      const params = new URLSearchParams(window.location.search);
      const requestedIdRaw = params.get("id");
      const requestedId = Number(requestedIdRaw);
      const requestedUserId =
        Number.isFinite(requestedId) && requestedId > 0 ? requestedId : null;
      const requestedUsername = normalizeUsername(params.get("u") || "");

      const me = await fetchViewerIdentity();
      viewerUserId = me.user_id;
      viewerUsername = me.username;

      activeProfileUserId = viewerUserId;
      activeProfileUsername = viewerUsername;
      activeProfileFullName = "";
      isViewingOwnProfile = true;
      document.body.dataset.visitor = "false";

      const wantsOtherProfile = Boolean(requestedUserId || requestedUsername);
      if (wantsOtherProfile) {
        const isSelfById = requestedUserId && viewerUserId && requestedUserId === viewerUserId;
        const isSelfByUsername = requestedUsername && viewerUsername && requestedUsername === viewerUsername;
        if (!isSelfById && !isSelfByUsername) {
          const profile = await fetchFollowProfile({
            userId: requestedUserId,
            username: requestedUserId ? null : requestedUsername,
          });
          activeProfileUserId = Number(profile?.user_id) || requestedUserId;
          activeProfileUsername = normalizeUsername(profile?.username || requestedUsername);
          activeProfileFullName = String(profile?.full_name || "").trim();
          isViewingOwnProfile = Boolean(viewerUserId && activeProfileUserId === viewerUserId);
          if (!isViewingOwnProfile) {
            applyReadOnlyProfileMode();
          }
        }
      }

      oracleUserName = activeProfileFullName || tr("Este usuario", "This user", "Cet utilisateur");
      applyOracleHeader();
      setMyHomeLinks(buildViewerHomeUrl());
      syncProfileModuleLinks();
    };

    const pbkdf2Key = async (password, saltBuf, iters) => {
      const baseKey = await crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        "PBKDF2",
        false,
        ["deriveKey"]
      );
      return crypto.subtle.deriveKey(
        { name: "PBKDF2", salt: saltBuf, iterations: iters, hash: "SHA-256" },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false,
        ["encrypt", "decrypt"]
      );
    };

    const decryptDekFromPassword = async (privatePassword) => {
      const vaultRes = await apiFetch("/vault/record");
      const vaultData = await parseResponseJson(vaultRes);
      if (!vaultRes.ok) {
        throw new Error(vaultData.detail || tr("No se pudo leer el vault.", "Could not read the vault.", "Impossible de lire le coffre-fort."));
      }

      const kdfSalt = hexToBuf(vaultData.kdf_salt_b64 || "");
      const wrappedDekNonce = new Uint8Array(hexToBuf(vaultData.wrapped_dek_nonce_b64 || ""));
      const wrappedDek = hexToBuf(vaultData.wrapped_dek_b64 || "");
      const iters = Number(vaultData.kdf_iters || 310000);

      const kek = await pbkdf2Key(privatePassword, kdfSalt, iters);
      const dekRaw = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: wrappedDekNonce, additionalData: AAD_VAULT },
        kek,
        wrappedDek
      );
      return crypto.subtle.importKey("raw", dekRaw, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
    };

    const aesGcmEncryptText = async (key, text, aadBuf) => {
      const nonce = crypto.getRandomValues(new Uint8Array(12));
      const ciphertext = await crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce, additionalData: aadBuf },
        key,
        new TextEncoder().encode(text)
      );
      return { nonce, ciphertext };
    };

    const aesGcmDecryptText = async (key, ciphertextHex, nonceHex, aadBuf) => {
      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: new Uint8Array(hexToBuf(nonceHex)), additionalData: aadBuf },
        key,
        hexToBuf(ciphertextHex)
      );
      return new TextDecoder().decode(decrypted);
    };

    const buildOracleAad = (cardId, cycle) =>
      new TextEncoder().encode(`${ORACLE_AAD_PREFIX}:${cardId}:${cycle}`);

    const normalizeOracleState = (payload) => {
      const fallback = buildFallbackState();
      const history = {};
      oracleEntriesById.clear();

      const responses = Array.isArray(payload?.responses) ? payload.responses : [];
      responses.forEach((response) => {
        const cardId = Number(response?.card_id || 0);
        if (!Number.isFinite(cardId) || cardId < 1 || cardId > TOTAL_CARDS) return;

        const entry = {
          id: Number(response?.id || 0),
          cardId,
          cycle: Number(response?.cycle || 1),
          type: String(response?.response_type || "heart"),
          text: response?.text_public || "",
          ciphertextHex: response?.ciphertext_hex || "",
          nonceHex: response?.nonce_hex || "",
          date: response?.created_at || new Date().toISOString(),
        };

        if (!history[cardId]) history[cardId] = [];
        history[cardId].push(entry);
        if (entry.id > 0) {
          oracleEntriesById.set(entry.id, entry);
        }
      });

      Object.values(history).forEach((entries) => {
        entries.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      });

      const revealedThisCycle = Array.isArray(payload?.revealed_this_cycle)
        ? payload.revealed_this_cycle
            .map((value) => Number(value))
            .filter((value) => Number.isFinite(value) && value >= 1 && value <= TOTAL_CARDS)
        : [];

      return {
        cycle: Number(payload?.cycle || fallback.cycle),
        cycleStartAt: payload?.cycle_started_at
          ? new Date(payload.cycle_started_at).getTime()
          : fallback.cycleStartAt,
        lastPickAt: payload?.last_pick_at ? new Date(payload.last_pick_at).getTime() : null,
        cooldownMs: Number(payload?.cooldown_ms || COOLDOWN_MS),
        cooldownRemainingMs: Math.max(0, Number(payload?.cooldown_remaining_ms || 0)),
        cycleComplete: Boolean(payload?.cycle_complete || revealedThisCycle.length >= TOTAL_CARDS),
        revealedThisCycle,
        history,
      };
    };

    const shuffleCards = (cards) => {
      const shuffled = [...cards];
      for (let i = shuffled.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
      }
      return shuffled;
    };

    const getCardImage = (cardId) => `/css/oracle/Oracle${cardId}.webp`;

    const formatDate = (date) => {
      return new Intl.DateTimeFormat(isEn ? "en-US" : isFr ? "fr-FR" : "es-CO", {
        day: "numeric",
        month: "long",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      }).format(date);
    };

    const formatCooldown = (remainingMs) => {
      const daysLeft = Math.ceil(remainingMs / (24 * 60 * 60 * 1000));
      if (daysLeft <= 1) {
        return tr("En 1 día podrás elegir una nueva carta.", "In 1 day you can choose a new card.", "Dans 1 jour, tu pourras choisir une nouvelle carte.");
      }
      return tr(
        `En ${daysLeft} días podrás elegir una nueva carta.`,
        `In ${daysLeft} days you can choose a new card.`,
        `Dans ${daysLeft} jours, tu pourras choisir une nouvelle carte.`
      );
    };

    const getCardHistory = (cardId) => {
      const entries = oracleState.history[cardId] || [];
      return entries.slice().sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    };

    const isUserResponseEntry = (entry) =>
      Boolean(entry && (entry.type === "public" || entry.type === "secret"));

    const getCardHistoryForDisplay = (cardId) => {
      const allResponses = getCardHistory(cardId).filter((entry) => isUserResponseEntry(entry));
      const now = Date.now();
      const yearlyResponses = allResponses.filter((entry) => {
        const timestamp = new Date(entry.date).getTime();
        if (!Number.isFinite(timestamp)) return false;
        return now - timestamp <= YEAR_MS;
      });
      const source = yearlyResponses.length ? yearlyResponses : allResponses;
      return {
        visible: source.slice(0, MAX_HISTORY_ENTRIES),
        total: allResponses.length,
        sourceType: yearlyResponses.length ? "year" : "all",
      };
    };

    const getCurrentCycleEntries = (cardId) =>
      getCardHistory(cardId).filter((entry) => Number(entry.cycle) === Number(oracleState.cycle));

    const updateCooldownStatus = () => {
      const now = Date.now();
      const cooldownMs = Number(oracleState.cooldownMs || COOLDOWN_MS);
      const remainingMs = oracleState.lastPickAt
        ? Math.max(0, cooldownMs - (now - oracleState.lastPickAt))
        : 0;
      const cooldownActive = remainingMs > 0;
      const cycleComplete = Boolean(oracleState.cycleComplete || oracleState.revealedThisCycle.length >= TOTAL_CARDS);

      if (!cooldownActive && !cycleComplete) {
        oracleStatus.textContent = tr("Selecciona una carta", "Select a card", "Sélectionne une carte");
        oracleCooldown.textContent = "";
      } else {
        oracleStatus.textContent = tr("Carta bloqueada temporalmente", "Card temporarily locked", "Carte temporairement verrouillée");
        oracleCooldown.textContent = formatCooldown(remainingMs || cooldownMs);
      }

      return { cooldownActive, cycleComplete, remainingMs };
    };

    const summarizeEntry = (entry) => {
      if (!entry) return tr("Carta revelada.", "Card revealed.", "Carte révélée.");
      if (entry.type === "heart") {
        return tr(
          `${oracleUserName} decidió no responder inmediatamente y dejó esta respuesta asentándose en su corazón.`,
          `${oracleUserName} chose not to answer immediately and left this response settling in their heart.`
        );
      }
      if (entry.type === "secret") {
        return tr(
          "Respuesta secreta cifrada en tu vault privado.",
          "Secret response encrypted in your private vault.",
          "Réponse secrète chiffrée dans ton coffre-fort privé."
        );
      }
      return entry.text || tr("Respuesta registrada.", "Response recorded.", "Réponse enregistrée.");
    };

    const renderOracleDeck = (cards, cooldownActive, cycleComplete, remainingMs) => {
      oracleDeck.innerHTML = "";
      oracleDeckEmpty.classList.add("hidden");

      const remainingCards = cards.filter((card) => !oracleState.revealedThisCycle.includes(card.id));

      if (remainingCards.length === 0) {
        oracleDeckEmpty.textContent = cooldownActive
          ? formatCooldown(remainingMs || COOLDOWN_MS)
          : tr("En 3 días podrás elegir una nueva carta.", "In 3 days you can choose a new card.", "Dans 3 jours, tu pourras choisir une nouvelle carte.");
        oracleDeckEmpty.classList.remove("hidden");
        return;
      }

      remainingCards.forEach((card) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "oracle-deck-card";
        button.dataset.cardId = `${card.id}`;
        if (cooldownActive || cycleComplete) {
          button.classList.add("is-locked");
          button.disabled = true;
        }
        button.innerHTML = `<img src="/css/oracle/carta.webp" alt=\"${tr("Carta del Oráculo", "Oracle card", "Carte de l'Oracle")}\" />`;
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

        const cardItem = document.createElement("button");
        cardItem.type = "button";
        cardItem.className = "oracle-revealed-card";

        const figure = document.createElement("div");
        figure.className = "oracle-revealed-figure";
        const image = document.createElement("img");
        image.src = getCardImage(cardId);
        image.alt = card?.name || tr("Carta revelada", "Revealed card", "Carte révélée");
        figure.appendChild(image);

        const body = document.createElement("div");
        body.className = "oracle-revealed-body";
        const title = document.createElement("strong");
        title.textContent = card?.name || tr("Carta revelada", "Revealed card", "Carte révélée");
        const paragraph = document.createElement("p");
        paragraph.textContent = summarizeEntry(latest);
        body.appendChild(title);
        body.appendChild(paragraph);
        if (formattedDate) {
          const dateLabel = document.createElement("span");
          dateLabel.textContent = tr(`Respuesta del ${formattedDate}`, `Response from ${formattedDate}`, `Réponse du ${formattedDate}`);
          body.appendChild(dateLabel);
        }

        cardItem.appendChild(figure);
        cardItem.appendChild(body);
        cardItem.addEventListener("click", () => openOracleModal(cardId));
        oracleRevealed.appendChild(cardItem);
      });
    };

    const renderHistory = (cardId) => {
      const { visible: entries, total: totalEntries, sourceType } = getCardHistoryForDisplay(cardId);
      oracleHistoryList.innerHTML = "";

      if (!entries.length) {
        oracleHistory.style.display = "none";
        if (oracleHistoryNote) {
          oracleHistoryNote.textContent = "";
        }
        return;
      }

      oracleHistory.style.display = "block";
      if (oracleHistoryNote) {
        if (sourceType === "year") {
          const hiddenCount = Math.max(0, totalEntries - entries.length);
          oracleHistoryNote.textContent = hiddenCount > 0
            ? tr(
              `Mostrando ${entries.length} respuestas (públicas o privadas) del último año. ${hiddenCount} registros más no se muestran aquí.`,
              `Showing ${entries.length} responses (public or private) from the last year. ${hiddenCount} additional records are not shown here.`
            )
            : tr(
                "Mostrando hasta 4 respuestas (públicas o privadas) del último año.",
                "Showing up to 4 responses (public or private) from the last year.",
                "Affichage de jusqu'à 4 réponses (publiques ou privées) de la dernière année."
              );
        } else {
          oracleHistoryNote.textContent =
            tr(
              "No hay respuestas del último año. Mostrando hasta 4 respuestas previas registradas.",
              "There are no responses from the last year. Showing up to 4 previously recorded responses.",
              "Il n'y a pas de réponses de la dernière année. Affichage de jusqu'à 4 réponses antérieures."
            );
        }
      }

      entries.forEach((entry) => {
        const item = document.createElement("div");
        item.className = "oracle-history-item";
        const isPastCycle = Number(entry.cycle) < Number(oracleState.cycle);

        const head = document.createElement("div");
        head.className = "oracle-history-head";
        const label = document.createElement("span");
        label.textContent = entry.type === "public"
          ? tr("Respuesta pública", "Public response", "Réponse publique")
          : entry.type === "secret"
            ? tr("Respuesta secreta", "Secret response", "Réponse secrète")
            : tr("Respuesta", "Response", "Réponse");
        const dateText = document.createElement("span");
        dateText.textContent = formatDate(new Date(entry.date));
        head.appendChild(label);
        head.appendChild(dateText);
        item.appendChild(head);

        const body = document.createElement("p");
        if (entry.type === "secret") {
          body.textContent = tr(
            "Contenido secreto cifrado. Para visualizarlo debes digitar tu clave privada personal.",
            "Encrypted secret content. To view it, you must enter your personal private key.",
            "Contenu secret chiffré. Pour le visualiser, tu dois saisir ta clé privée personnelle."
          );
          item.appendChild(body);
        } else {
          body.textContent = entry.text || "";
          item.appendChild(body);
        }

        const actions = document.createElement("div");
        actions.className = "oracle-history-item-actions";

        if (entry.type === "secret" && entry.id > 0) {
          const button = document.createElement("button");
          button.type = "button";
          button.className = "btn btn-outline btn-compact oracle-secret-history-btn";
          button.dataset.entryId = `${entry.id}`;
          button.textContent = tr("Visualizar respuesta secreta", "View secret response", "Voir la réponse secrète");
          actions.appendChild(button);
        }

        if (isPastCycle && entry.id > 0) {
          const deleteButton = document.createElement("button");
          deleteButton.type = "button";
          deleteButton.className = "oracle-history-delete-btn";
          deleteButton.dataset.entryId = `${entry.id}`;
          deleteButton.title = tr("Borrar respuesta de forma permanente", "Delete response permanently", "Supprimer la réponse définitivement");
          deleteButton.innerHTML = `<img src="/css/icons/icondelete.webp" alt="${tr("Borrar respuesta", "Delete response", "Supprimer la réponse")}" />`;
          actions.appendChild(deleteButton);
        }

        if (actions.childElementCount > 0) {
          item.appendChild(actions);
        }

        oracleHistoryList.appendChild(item);
      });
    };

    const closeModal = () => {
      oracleModalOverlay.classList.add("hidden");
      oracleModalOverlay.setAttribute("aria-hidden", "true");
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      if (oracleSecretActions) {
        oracleSecretActions.classList.add("hidden");
      }
      if (oracleRevealSecretBtn) {
        delete oracleRevealSecretBtn.dataset.entryId;
      }
      pendingAction = null;
      pendingDeleteEntryId = null;
      selectedCard = null;
    };

    const openOracleModal = (cardId) => {
      selectedCard = oracleCards.find((card) => card.id === cardId);
      if (!selectedCard) return;

      if (!isViewingOwnProfile) {
        const entries = getCardHistory(cardId);
        const latest = entries[0];
        oracleCardName.textContent = selectedCard.name;
        oracleCardQuestion.textContent = selectedCard.question;
        oracleCardImage.src = getCardImage(selectedCard.id);
        oracleCardContext.textContent = selectedCard.context;

        oracleCardResponse.disabled = true;
        oracleCardResponse.placeholder = tr("Sin respuesta pública.", "No public response.", "Aucune réponse publique.");
        oracleCardResponse.value = latest?.text || "";
        oracleActionRow.style.display = "none";
        oracleConfirm.classList.add("hidden");
        resetPrivatePasswordUi();
        resetSecretUnlockUi();
        pendingDeleteEntryId = null;
        pendingAction = null;
        if (oracleSecretActions) oracleSecretActions.classList.add("hidden");

        oracleModalNote.textContent = latest?.date
          ? tr(
            `Respuesta pública registrada el ${formatDate(new Date(latest.date))}.`,
            `Public response recorded on ${formatDate(new Date(latest.date))}.`
          )
          : tr("Esta carta no tiene respuesta pública.", "This card has no public response.", "Cette carte n'a pas de réponse publique.");

        updateWordCounter();
        renderHistory(cardId);
        oracleModalOverlay.classList.remove("hidden");
        oracleModalOverlay.setAttribute("aria-hidden", "false");
        return;
      }

      const currentEntries = getCurrentCycleEntries(cardId);
      const answeredEntry = currentEntries.find((entry) => entry.type === "public" || entry.type === "secret");
      const hasAnswered = Boolean(answeredEntry);
      const hasHeart = currentEntries.some((entry) => entry.type === "heart");

      oracleCardName.textContent = selectedCard.name;
      oracleCardQuestion.textContent = selectedCard.question;
      oracleCardImage.src = getCardImage(selectedCard.id);
      oracleCardContext.textContent = selectedCard.context;

      oracleCardResponse.disabled = hasAnswered;
      oracleCardResponse.placeholder = tr("Escribe tu respuesta...", "Write your response...", "Écris ta réponse...");
      oracleCardResponse.value = "";
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      pendingDeleteEntryId = null;
      pendingAction = null;
      if (oracleSecretActions) oracleSecretActions.classList.add("hidden");

      if (hasAnswered) {
        oracleActionRow.style.display = "none";
        if (answeredEntry?.type === "secret") {
          oracleModalNote.textContent = answeredEntry?.date
            ? tr(
              `Respuesta secreta registrada el ${formatDate(new Date(answeredEntry.date))}. Para verla debes digitar tu clave privada.`,
              `Secret response recorded on ${formatDate(new Date(answeredEntry.date))}. To view it, you must enter your private key.`,
              `Réponse secrète enregistrée le ${formatDate(new Date(answeredEntry.date))}. Pour la voir, tu dois saisir ta clé privée.`
            )
            : tr(
                "Respuesta secreta registrada. Para verla debes digitar tu clave privada.",
                "Secret response recorded. To view it, you must enter your private key.",
                "Réponse secrète enregistrée. Pour la voir, tu dois saisir ta clé privée."
              );
          oracleCardResponse.placeholder = tr(
            "Respuesta secreta cifrada en tu vault.",
            "Secret response encrypted in your vault.",
            "Réponse secrète chiffrée dans ton coffre-fort."
          );
          if (oracleSecretActions && oracleRevealSecretBtn && answeredEntry?.id > 0) {
            oracleRevealSecretBtn.dataset.entryId = `${answeredEntry.id}`;
            oracleSecretActions.classList.remove("hidden");
          }
        } else {
          oracleCardResponse.value = answeredEntry?.text || "";
          oracleModalNote.textContent = answeredEntry?.date
            ? tr(
              `Respuesta registrada el ${formatDate(new Date(answeredEntry.date))}. Este texto es inmodificable.`,
              `Response recorded on ${formatDate(new Date(answeredEntry.date))}. This text cannot be modified.`,
              `Réponse enregistrée le ${formatDate(new Date(answeredEntry.date))}. Ce texte est inmodifiable.`
            )
            : tr("Respuesta registrada. Este texto es inmodificable.", "Response recorded. This text cannot be modified.", "Réponse enregistrée. Ce texte est inmodifiable.");
        }
      } else {
        oracleActionRow.style.display = "flex";
        oracleModalNote.textContent = hasHeart
          ? tr(
            "Esta carta quedó reposando en tu corazón. Puedes responder cuando lo desees durante este ciclo.",
            "This card was left resting in your heart. You can answer whenever you want during this cycle.",
            "Cette carte est restée en repos dans ton coeur. Tu peux répondre quand tu veux pendant ce cycle."
          )
          : tr(
            "Puedes responder ahora, en secreto o dejar la pregunta reposando en tu corazón.",
            "You can answer now, answer in secret, or leave the question resting in your heart.",
            "Tu peux répondre maintenant, en secret, ou laisser la question reposer dans ton coeur."
          );
      }

      updateWordCounter();
      renderHistory(cardId);
      oracleModalOverlay.classList.remove("hidden");
      oracleModalOverlay.setAttribute("aria-hidden", "false");
    };

    const triggerConfirm = (action) => {
      pendingAction = action;
      pendingDeleteEntryId = null;
      resetSecretUnlockUi();
      if (action === "public") {
        oracleConfirmText.textContent = tr("¿Estás seguro de tu respuesta pública?", "Are you sure about your public response?", "Es-tu sûr de ta réponse publique ?");
        resetPrivatePasswordUi();
      } else if (action === "secret") {
        oracleConfirmText.textContent =
          tr(
            "¿Estás seguro de tu respuesta secreta? Deberás digitar tu clave privada para cifrarla.",
            "Are you sure about your secret response? You must enter your private key to encrypt it.",
            "Es-tu sûr de ta réponse secrète ? Tu dois saisir ta clé privée pour la chiffrer."
          );
        showPrivatePasswordUi();
      } else {
        oracleConfirmText.textContent =
          tr(
            "¿Deseas dejar esta pregunta reposando en tu corazón?",
            "Do you want to leave this question resting in your heart?",
            "Souhaites-tu laisser cette question reposer dans ton coeur ?"
          );
        resetPrivatePasswordUi();
      }
      oracleConfirm.classList.remove("hidden");
    };

    const extractSecretText = (raw) => {
      try {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === "object") {
          return String(parsed.text || parsed.response || "");
        }
      } catch {
        // No-op: if payload is not JSON, fallback to plaintext body.
      }
      return String(raw || "");
    };

    const revealSecretEntry = async (entryId, privatePassword, { renderIntoTextarea = true } = {}) => {
      const id = Number(entryId || 0);
      const entry = oracleEntriesById.get(id);
      if (!entry || entry.type !== "secret") {
        throw new Error(tr("No se encontró la respuesta secreta.", "Secret response was not found.", "La réponse secrète n'a pas été trouvée."));
      }

      if (!String(privatePassword || "").trim()) {
        throw new Error(tr("Debes digitar tu clave privada personal.", "You must enter your personal private key.", "Tu dois saisir ta clé privée personnelle."));
      }

      const dekKey = await decryptDekFromPassword(String(privatePassword));
      const plaintext = await aesGcmDecryptText(
        dekKey,
        entry.ciphertextHex,
        entry.nonceHex,
        buildOracleAad(entry.cardId, entry.cycle)
      );
      const secretText = extractSecretText(plaintext);

      if (renderIntoTextarea) {
        oracleCardResponse.value = secretText;
        updateWordCounter();
        oracleModalNote.textContent = tr(
          "Respuesta secreta descifrada localmente en tu navegador.",
          "Secret response decrypted locally in your browser.",
          "Réponse secrète déchiffrée localement dans ton navigateur."
        );
      } else {
        window.alert(secretText || tr("La respuesta secreta está vacía.", "The secret response is empty.", "La réponse secrète est vide."));
      }
    };

    const triggerDeleteHistoryConfirm = (entryId) => {
      const id = Number(entryId || 0);
      if (!Number.isFinite(id) || id <= 0) return;
      pendingDeleteEntryId = id;
      pendingAction = "delete_history";
      resetPrivatePasswordUi();
      resetSecretUnlockUi();
      oracleConfirmText.textContent =
        tr(
          "Vas a borrar esta respuesta de forma permanente. Una vez elimines este recuerdo, no volverás a visualizarlo. ¿Deseas continuar?",
          "You are about to permanently delete this response. Once deleted, this memory will no longer be visible. Do you want to continue?",
          "Tu es sur le point de supprimer définitivement cette réponse. Une fois supprimé, ce souvenir ne sera plus visible. Souhaites-tu continuer ?"
        );
      oracleConfirm.classList.remove("hidden");
    };

    const submitOracleResponse = async (payload) => {
      const res = await apiFetch("/oracle/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(
          data.detail ||
            tr(
              "No se pudo registrar la respuesta del Oráculo.",
              "Could not register the Oracle response.",
              "Impossible d'enregistrer la réponse de l'Oracle."
            )
        );
      }
      oracleState = normalizeOracleState(data);
    };

    const deleteOracleResponse = async (entryId) => {
      const responseId = Number(entryId || 0);
      if (!Number.isFinite(responseId) || responseId <= 0) {
        throw new Error(tr("Respuesta inválida para borrar.", "Invalid response to delete.", "Réponse invalide à supprimer."));
      }

      const res = await apiFetch(`/oracle/responses/${responseId}`, {
        method: "DELETE",
      });
      const data = await parseResponseJson(res);
      if (!res.ok) {
        throw new Error(data.detail || tr("No se pudo borrar la respuesta.", "Could not delete the response.", "Impossible de supprimer la réponse."));
      }
      oracleState = normalizeOracleState(data);
    };

    const finalizeResponse = async () => {
      if (!selectedCard || !pendingAction || isSubmitting) return;

      if (pendingAction === "delete_history") {
        const responseId = Number(pendingDeleteEntryId || 0);
        if (!Number.isFinite(responseId) || responseId <= 0) {
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
          pendingDeleteEntryId = null;
          return;
        }

        isSubmitting = true;
        oracleConfirmYes.disabled = true;
        oracleConfirmNo.disabled = true;

        try {
          await deleteOracleResponse(responseId);
          oracleConfirm.classList.add("hidden");
          pendingAction = null;
          pendingDeleteEntryId = null;
          renderAll();
          openOracleModal(selectedCard.id);
        } catch (err) {
          oracleModalNote.textContent =
            err?.message || tr("No se pudo borrar la respuesta.", "Could not delete the response.", "Impossible de supprimer la réponse.");
        } finally {
          isSubmitting = false;
          oracleConfirmYes.disabled = false;
          oracleConfirmNo.disabled = false;
        }
        return;
      }

      const responseText = oracleCardResponse.value.trim();
      if (pendingAction !== "heart" && !responseText) {
        oracleModalNote.textContent = tr(
          "Escribe una respuesta antes de confirmar esta acción.",
          "Write a response before confirming this action.",
          "Écris une réponse avant de confirmer cette action."
        );
        updateWordCounter();
        return;
      }

      if (pendingAction !== "heart") {
        const words = countWords(responseText);
        updateWordCounter();
        if (words > MAX_RESPONSE_WORDS) {
          oracleModalNote.textContent = tr(
            `Tu respuesta supera el máximo permitido de ${MAX_RESPONSE_WORDS} palabras.`,
            `Your response exceeds the maximum allowed of ${MAX_RESPONSE_WORDS} words.`,
            `Ta réponse dépasse le maximum autorisé de ${MAX_RESPONSE_WORDS} mots.`
          );
          return;
        }
      } else {
        updateWordCounter();
      }

      const payload = {
        card_id: selectedCard.id,
        response_type: pendingAction,
      };

      let privatePassword = "";
      if (pendingAction === "secret") {
        privatePassword = String(oraclePrivatePasswordInput?.value || "");
        if (!privatePassword.trim()) {
          setPrivatePasswordError(tr("Digita tu clave privada personal", "Enter your personal private key", "Saisis ta clé privée personnelle"));
          oraclePrivatePasswordInput?.focus();
          return;
        }
        setPrivatePasswordError("");
      }

      isSubmitting = true;
      oracleConfirmYes.disabled = true;
      oracleConfirmNo.disabled = true;
      let completed = false;

      try {
        if (pendingAction === "public") {
          payload.text_public = responseText;
        } else if (pendingAction === "secret") {
          const dekKey = await decryptDekFromPassword(privatePassword);
          const encoded = JSON.stringify({ text: responseText });
          const encrypted = await aesGcmEncryptText(
            dekKey,
            encoded,
            buildOracleAad(selectedCard.id, oracleState.cycle)
          );

          payload.ciphertext_hex = bufToHex(encrypted.ciphertext);
          payload.nonce_hex = bufToHex(encrypted.nonce.buffer);
        }

        await submitOracleResponse(payload);
        completed = true;
        closeModal();
        renderAll();
      } catch (err) {
        const message =
          err?.message || tr("No se pudo registrar la respuesta.", "Could not register the response.", "Impossible d'enregistrer la réponse.");
        if (pendingAction === "secret") {
          setPrivatePasswordError(message);
        } else {
          oracleModalNote.textContent = message;
        }
      } finally {
        isSubmitting = false;
        oracleConfirmYes.disabled = false;
        oracleConfirmNo.disabled = false;
        if (completed) {
          pendingAction = null;
          pendingDeleteEntryId = null;
        }
      }
    };

    const renderAll = () => {
      const shuffled = shuffleCards(oracleCards);
      const { cooldownActive, cycleComplete, remainingMs } = updateCooldownStatus();
      renderOracleDeck(shuffled, cooldownActive, cycleComplete, remainingMs);
      renderRevealed();
    };

    const loadOracleState = async () => {
      try {
        oracleStatus.textContent = tr("Cargando cartas...", "Loading cards...", "Chargement des cartes...");
        const profileId = Number(activeProfileUserId);
        const endpoint =
          !isViewingOwnProfile && Number.isFinite(profileId) && profileId > 0
            ? `/oracle/public/${encodeURIComponent(String(profileId))}`
            : "/oracle/state";
        const res = await apiFetch(endpoint);
        const data = await parseResponseJson(res);
        if (!res.ok) {
          throw new Error(
            data.detail || tr("No se pudo cargar el estado del Oráculo.", "Could not load Oracle state.", "Impossible de charger l'état de l'Oracle.")
          );
        }
        oracleState = normalizeOracleState(data);
        renderAll();
      } catch (err) {
        oracleStatus.textContent = tr("No se pudo cargar el Oráculo", "Could not load Oracle", "Impossible de charger l'Oracle");
        oracleCooldown.textContent = err?.message || tr("Inténtalo de nuevo.", "Try again.", "Réessaie.");
        if (!isViewingOwnProfile && oracleRevealedEmpty) {
          oracleRevealed.innerHTML = "";
          oracleRevealedEmpty.textContent = err?.message || tr("Este módulo es privado.", "This module is private.", "Ce module est privé.");
          oracleRevealedEmpty.style.display = "block";
        }
      }
    };

    oraclePublishBtn.addEventListener("click", () => triggerConfirm("public"));
    oracleSecretBtn.addEventListener("click", () => triggerConfirm("secret"));
    oracleHeartBtn.addEventListener("click", () => triggerConfirm("heart"));

    oracleConfirmYes.addEventListener("click", () => void finalizeResponse());
    oracleConfirmNo.addEventListener("click", () => {
      oracleConfirm.classList.add("hidden");
      resetPrivatePasswordUi();
      pendingDeleteEntryId = null;
      pendingAction = null;
    });

    if (oraclePrivatePasswordInput) {
      oraclePrivatePasswordInput.addEventListener("input", () => setPrivatePasswordError(""));
      oraclePrivatePasswordInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          void finalizeResponse();
        }
      });
    }

    if (oracleCardResponse) {
      oracleCardResponse.addEventListener("input", () => {
        updateWordCounter();
      });
    }

    if (oracleRevealSecretBtn) {
      oracleRevealSecretBtn.addEventListener("click", () => {
        const entryId = Number(oracleRevealSecretBtn.dataset.entryId || 0);
        if (!entryId) return;
        openSecretUnlockUi(entryId);
      });
    }

    if (oracleHistoryList) {
      oracleHistoryList.addEventListener("click", (event) => {
        const target = event.target instanceof Element ? event.target : null;
        const secretTrigger = target ? target.closest(".oracle-secret-history-btn") : null;
        if (secretTrigger) {
          const entryId = Number(secretTrigger.dataset.entryId || 0);
          if (!entryId) return;
          openSecretUnlockUi(entryId);
          return;
        }

        const deleteTrigger = target ? target.closest(".oracle-history-delete-btn") : null;
        if (deleteTrigger) {
          const entryId = Number(deleteTrigger.dataset.entryId || 0);
          if (!entryId) return;
          triggerDeleteHistoryConfirm(entryId);
        }
      });
    }

    if (oracleSecretUnlockConfirm) {
      oracleSecretUnlockConfirm.addEventListener("click", async () => {
        const password = String(oracleSecretUnlockPassword?.value || "");
        if (!password.trim()) {
          setSecretUnlockError(tr("Digita tu clave privada personal", "Enter your personal private key", "Saisis ta clé privée personnelle"));
          oracleSecretUnlockPassword?.focus();
          return;
        }

        try {
          await revealSecretEntry(pendingSecretRevealEntryId, password, { renderIntoTextarea: true });
          resetSecretUnlockUi();
        } catch (err) {
          setSecretUnlockError(
            err?.message || tr("No se pudo descifrar la respuesta secreta.", "Could not decrypt the secret response.", "Impossible de déchiffrer la réponse secrète.")
          );
        }
      });
    }

    if (oracleSecretUnlockCancel) {
      oracleSecretUnlockCancel.addEventListener("click", () => {
        resetSecretUnlockUi();
      });
    }

    if (oracleSecretUnlockPassword) {
      oracleSecretUnlockPassword.addEventListener("input", () => setSecretUnlockError(""));
      oracleSecretUnlockPassword.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          oracleSecretUnlockConfirm?.click();
        }
      });
    }

    closeOracleModal.addEventListener("click", closeModal);
    oracleModalOverlay.addEventListener("click", (event) => {
      if (event.target === oracleModalOverlay) closeModal();
    });

    updateWordCounter();
    (async () => {
      try {
        await resolveProfileContext();
      } catch (error) {
        console.error(error);
      } finally {
        void loadOracleState();
      }
    })();
  });
</script>

<svelte:head>
<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{tr("Kiadez — Oráculo", "Kiadez — Oracle", "Kiadez — Oracle")}</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user oracle-background">
  <header class="feed-topbar">
    <div class="feed-topbar-zone feed-topbar-left">
      <a class="topbar-logo" href="/feed.html" aria-label="Kiadez">
        <img src="/css/logo-kiadez.webp" alt="Kiadez" />
      </a>
      <form class="topbar-search" role="search" on:submit|preventDefault>
        <input
          type="search"
          placeholder={tr("Buscar en Kiadez", "Search on Kiadez", "Rechercher sur Kiadez")}
          aria-label={tr("Buscar", "Search", "Rechercher")}
        />
      </form>
    </div>

    <div class="feed-topbar-zone feed-topbar-center">
      <a class="topbar-btn" href="/home_user.html" data-profile-module="home">🏠 Home</a>
      <a class="topbar-btn" href="/gallery.html">🖼️ {tr("Galería", "Gallery", "Galerie")}</a>
      <a class="topbar-btn" href="/my-public-whishes.html" data-profile-module="public_wishes">🌐 {tr("Deseos públicos", "Public wishes", "Souhaits publics")}</a>
      <a class="topbar-btn" href="/my-private-whishes.html">🔒 {tr("Deseos privados", "Private wishes", "Souhaits privés")}</a>
      <a class="topbar-btn" href="/my-fulfilled-whises.html" data-profile-module="fulfilled_wishes">✅ {tr("Deseos cumplidos", "Fulfilled wishes", "Souhaits accomplis")}</a>
    </div>

    <div class="feed-topbar-zone feed-topbar-right">
      <details class="topbar-dropdown" id="profileDropdown">
        <summary class="topbar-avatar-btn" aria-label={tr("Perfil del usuario", "User profile", "Profil utilisateur")}>
          <img src="/assets/avatar-default.jpg" alt={tr("Perfil de Carlos Jiménez Duarte", "Carlos Jiménez Duarte profile", "Profil de Carlos Jiménez Duarte")} />
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

      <details class="topbar-dropdown" id="menuDropdown">
        <summary class="topbar-menu-btn" aria-label={tr("Abrir menú", "Open menu", "Ouvrir le menu")}>
          <span class="topbar-menu-icon" aria-hidden="true">☰</span>
          <span class="topbar-menu-label">{tr("Menú", "Menu", "Navigation")}</span>
        </summary>
        <div class="dropdown-menu" role="menu">
          <a href="/home_user.html" role="menuitem" data-my-home>{tr("Mi Home", "My Home", "Mon Home")}</a>
          <a href="/achievements.html" role="menuitem">{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a href="/gallery.html" role="menuitem">{tr("Galería", "Gallery", "Galerie")}</a>
          <a href="/calendar.html" role="menuitem" data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a href="/my-biography.html" role="menuitem">{tr("Mi Biografía", "My Biography", "Ma biographie")}</a>
          <a href="/messages.html" role="menuitem">{tr("Mensajes", "Messages", "Messagerie")}</a>
        </div>
      </details>
    </div>
  </header>

    <main class="user-home">

      <!-- =========================
       *  PORTADA / COVER
       *  ========================= -->
      <section class="cover" id="cover">
        <div class="cover-media" id="coverMedia">
          <img id="coverImg" class="cover-img" src="/assets/cover-default.jpg" alt={tr("Portada", "Cover", "Couverture")} />

          <div class="cover-actions cover-actions-purpose">
            <details class="cover-menu">
              <summary class="icon-btn" id="btnChangeCover" title={tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}>
                {tr("Editar imagen de portada", "Edit cover image", "Modifier l'image de couverture")}
              </summary>
              <div class="cover-menu-panel">
                <button class="cover-menu-item" type="button" id="coverUpload">
                  {tr("Subir imagen", "Upload image", "Téléverser une image")}
                </button>
                <button class="cover-menu-item" type="button" id="coverMove">
                  {tr("Mover imagen", "Move image", "Déplacer l'image")}
                </button>
              </div>
            </details>
            <button class="icon-btn cover-purpose-btn" id="btnEditPurposes" type="button"
              title={tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier mon objectif de vie")}>
              {tr("Editar mi propósito de vida", "Edit my life purpose", "Modifier mon objectif de vie")}
            </button>

            <input id="coverFile" type="file" accept="image/*" class="hidden" />
          </div>

          <div class="cover-save-actions hidden" id="coverSaveActions">
            <button class="btn btn-primary btn-compact" type="button" id="coverSaveBtn">
              {tr("Guardar cambios", "Save changes", "Enregistrer les modifications")}
            </button>
            <button class="btn btn-outline btn-compact" type="button" id="coverCancelBtn">
              {tr("Cancelar", "Cancel", "Annuler")}
            </button>
          </div>

          <div class="purpose-stack purpose-stack-modern" aria-label={tr("Deseos de propósito", "Purpose wishes", "Souhaits de finalité")}>
            <div class="purpose-list">
              <div class="purpose-pill-row">
                <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="1"
                  title={tr("Marcar deseo 1 como cumplido", "Mark wish 1 as fulfilled", "Marquer le souhait 1 comme accompli")}>
                  <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark fulfilled wish", "Marquer souhait accompli")} />
                </button>
                <button class="purpose-pill" type="button" id="purpose1">
                  {tr("Deseo #1: Secreto", "Wish #1: Secret", "Souhait #1 : Secret")}
                </button>
                <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock1"
                  data-slot="1" title={tr("Desbloquear deseo 1", "Unlock wish 1", "Déverrouiller le souhait 1")}>
                  <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller souhait secret")} />
                </button>
              </div>

              <div class="purpose-pill-row">
                <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="2"
                  title={tr("Marcar deseo 2 como cumplido", "Mark wish 2 as fulfilled", "Marquer le souhait 2 comme accompli")}>
                  <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark fulfilled wish", "Marquer souhait accompli")} />
                </button>
                <button class="purpose-pill" type="button" id="purpose2">
                  {tr("Deseo de propósito sin definir", "Undefined purpose wish", "Souhait de finalité non défini")}
                </button>
                <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock2"
                  data-slot="2" title={tr("Desbloquear deseo 2", "Unlock wish 2", "Déverrouiller le souhait 2")}>
                  <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller souhait secret")} />
                </button>
              </div>

              <div class="purpose-pill-row">
                <button class="purpose-side-btn purpose-fulfill-btn" type="button" data-slot="3"
                  title={tr("Marcar deseo 3 como cumplido", "Mark wish 3 as fulfilled", "Marquer le souhait 3 comme accompli")}>
                  <img src="/css/icons/iconfulfill.webp" alt={tr("Marcar deseo cumplido", "Mark fulfilled wish", "Marquer souhait accompli")} />
                </button>
                <button class="purpose-pill" type="button" id="purpose3">
                  {tr("Deseo estar unido a Jesús", "I wish to be united with Jesus", "Je souhaite être uni à Jésus")}
                </button>
                <button class="purpose-side-btn purpose-unlock-btn hidden" type="button" id="purposeUnlock3"
                  data-slot="3" title={tr("Desbloquear deseo 3", "Unlock wish 3", "Déverrouiller le souhait 3")}>
                  <img src="/css/icons/iconkey.webp" alt={tr("Desbloquear deseo secreto", "Unlock secret wish", "Déverrouiller souhait secret")} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="oracle-body">
        <!-- =========================
         *  NAV / LINKS
         *  ========================= -->
        <nav class="profile-nav" aria-label={tr("Navegación de perfil", "Profile navigation", "Navigation du profil")}>
          <a class="nav-pill" href="/home_user.html" title="Home" data-profile-module="home">Home</a>
          <a class="nav-pill" href="/star-pool-found.html" title={tr("Estrellas", "Stars", "Étoiles")}>
            <span class="nav-icon">⭐</span>
            <span><strong>5.000.000</strong> {tr("estrellas", "stars", "étoiles")}</span>
          </a>
          <a class="nav-pill" href="/followers.html" title={tr("Seguidores", "Followers", "Abonnés")}>{tr("Seguidores", "Followers", "Abonnés")}</a>
          <a class="nav-pill" href="/achievements.html" title={tr("Logros recientes", "Recent achievements", "Réalisations récentes")}>{tr("Logros recientes", "Recent achievements", "Réalisations récentes")}</a>
          <a class="nav-pill" href="/gallery.html" title={tr("Galería", "Gallery", "Galerie")}>{tr("Galería", "Gallery", "Galerie")}</a>
          <a class="nav-pill" href="/calendar.html" title={tr("Calendario", "Calendar", "Calendrier")} data-profile-module="calendar">{tr("Calendario", "Calendar", "Calendrier")}</a>
          <a class="nav-pill" href="/my-biography.html" title={tr("Mi biografía", "My biography", "Ma biographie")}>{tr("Mi biografía", "My biography", "Ma biographie")}</a>
        <a class="nav-pill" href="/messages.html" title={tr("Mensajes", "Messages", "Messagerie")}>{tr("Mensajes", "Messages", "Messagerie")}</a>
        </nav>

        <!-- =========================
         *  ORACULO
         *  ========================= -->
        <section class="oracle-shell" aria-label={tr("Oráculo", "Oracle", "Oracle")}>
          <header class="oracle-head">
            <div>
              <h2 class="oracle-title">{tr("El Oráculo", "The Oracle", "L'Oracle")}</h2>
              <p class="oracle-subtitle">
                {tr(
                  "Selecciona una carta para comprender tu presente. Solo una carta cada 3 días.",
                  "Select a card to understand your present. Only one card every 3 days."
                )}
              </p>
            </div>
          </header>

          <section class="panel oracle-intro" aria-label={tr("¿Qué es el Oráculo?", "What is the Oracle?", "Qu'est-ce que l'Oracle ?")}>
            <div class="panel-head">
              <h3 class="panel-title">{tr("¿Qué es el Oráculo?", "What is the Oracle?", "Qu'est-ce que l'Oracle ?")}</h3>
            </div>
            <p class="panel-text">
              {tr(
                "El Oráculo es una herramienta de reflexión de Kiadez.com. Eliges una carta, no para adivinar tu futuro, sino para comprender tu presente. Actualmente el Oráculo está compuesto de 30 cartas y solo puedes seleccionar una sola cada 3 días. La carta te planteará una pregunta, que puedes responder inmediatamente o dejar reposando en tu corazón. Si eres juicioso y disciplinado, responderás la pregunta que te propone la carta hasta 4 veces a lo largo de un solo año. Eso te permitirá reconocer cuánto has progresado en el camino de conocerte a ti mismo.",
                "The Oracle is a reflection tool from Kiadez.com. You choose a card not to predict your future, but to understand your present. The Oracle currently contains 30 cards, and you can select only one every 3 days. The card poses a question that you can answer immediately or leave resting in your heart. If you are disciplined, you can answer the card's question up to 4 times over a single year. This helps you recognize how much progress you have made on the path of self-knowledge."
              )}
            </p>
          </section>

          <section class="panel oracle-deck" aria-label={tr("Cartas no reveladas", "Unrevealed cards", "Cartes non révélées")}>
            <div class="oracle-deck-head">
              <div>
                <h3>{tr("Cartas no reveladas", "Unrevealed cards", "Cartes non révélées")}</h3>
                <p class="oracle-status" id="oracleStatus">{tr("Selecciona una carta", "Select a card", "Sélectionne une carte")}</p>
              </div>
              <div class="oracle-deck-note" id="oracleCooldown"></div>
            </div>
            <div class="oracle-grid" id="oracleDeck"></div>
            <div class="oracle-empty hidden" id="oracleDeckEmpty">
              {tr("En 3 días podrás elegir una nueva carta.", "In 3 days you can choose a new card.", "Dans 3 jours, tu pourras choisir une nouvelle carte.")}
            </div>
          </section>

          <section class="panel oracle-revealed" aria-label={tr("Cartas reveladas", "Revealed cards", "Cartes révélées")}>
            <div class="panel-head">
              <h3 class="panel-title">{tr("Cartas reveladas", "Revealed cards", "Cartes révélées")}</h3>
              <span class="panel-badge">{tr("Respuestas registradas", "Recorded responses", "Réponses enregistrées")}</span>
            </div>
            <div class="oracle-revealed-grid" id="oracleRevealed"></div>
            <div class="oracle-empty" id="oracleRevealedEmpty">
              {tr(
                "Aún no has revelado cartas. Cuando selecciones una, aparecerá aquí.",
                "You have not revealed cards yet. When you select one, it will appear here."
              )}
            </div>
          </section>
        </section>
      </div>

    </main>

    <AuthFooter />
  </div>

  <!-- =========================
   *  MODAL: CARTA SELECCIONADA
   *  ========================= -->
  <div class="modal-overlay hidden" id="oracleModalOverlay" aria-hidden="true">
    <div class="modal modal-wide oracle-modal" role="dialog" aria-modal="true" aria-label={tr("Carta seleccionada", "Selected card", "Carte sélectionnée")}>
      <div class="modal-head">
        <div>
          <h3 id="oracleCardName">{tr("Nombre de la carta", "Card name", "Nom de la carte")}</h3>
          <p class="oracle-card-question" id="oracleCardQuestion"></p>
        </div>
        <button class="modal-close" type="button" id="closeOracleModal">✕</button>
      </div>

      <div class="modal-body">
        <div class="oracle-modal-top">
          <div class="oracle-card-figure">
            <img id="oracleCardImage" src="/css/oracle/Oracle9.png" alt={tr("Carta del Oráculo", "Oracle card", "Carte de l'Oracle")} />
          </div>
          <div class="oracle-card-context">
            <h4>{tr("Contexto", "Context", "Contexte")}</h4>
            <p id="oracleCardContext"></p>
          </div>
        </div>

        <textarea class="modal-textarea" id="oracleCardResponse" rows="6"
          placeholder={tr("Escribe tu respuesta...", "Write your response...", "Écris ta réponse...")}></textarea>
        <p class="oracle-word-counter" id="oracleWordCounter">{tr("0/500 palabras", "0/500 words", "0/500 mots")}</p>
        <div class="oracle-modal-note" id="oracleModalNote"></div>
        <div class="oracle-action-row hidden" id="oracleSecretActions">
          <button class="btn btn-outline btn-compact" type="button" id="oracleRevealSecretBtn">
            {tr("Digitar clave privada para visualizar respuesta secreta", "Enter private key to view secret response", "Saisir la clé privée pour visualiser la réponse secrète")}
          </button>
        </div>
        <div class="oracle-secret-unlock hidden" id="oracleSecretUnlock">
          <p class="oracle-secret-unlock-text">
            {tr(
              "Digita tu clave privada personal para visualizar esta respuesta secreta.",
              "Enter your personal private key to view this secret response."
            )}
          </p>
          <input
            class="oracle-private-password-input"
            id="oracleSecretUnlockPassword"
            type="password"
            placeholder={tr("Digita tu clave privada personal", "Enter your personal private key", "Saisis ta clé privée personnelle")}
            autocomplete="current-password"
          />
          <p class="oracle-private-password-error" id="oracleSecretUnlockError"></p>
          <div class="oracle-confirm-actions">
            <button class="btn btn-primary btn-compact" type="button" id="oracleSecretUnlockConfirm">
              {tr("Visualizar", "View", "Visualiser")}
            </button>
            <button class="btn btn-outline btn-compact" type="button" id="oracleSecretUnlockCancel">
              {tr("Cancelar", "Cancel", "Annuler")}
            </button>
          </div>
        </div>

        <div class="oracle-action-row" id="oracleActionRow">
          <button class="btn btn-primary btn-compact" type="button" id="oraclePublishBtn">{tr("Responder ahora y publicar", "Answer now and publish", "Répondre maintenant et publier")}</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleSecretBtn">{tr("Responder en secreto", "Answer in secret", "Répondre en secret")}</button>
          <button class="btn btn-outline btn-compact" type="button" id="oracleHeartBtn">{tr("Dejar esta pregunta reposando en mi corazón", "Let this question rest in my heart", "Laisser cette question reposer dans mon coeur")}</button>
        </div>

        <div class="oracle-confirm hidden" id="oracleConfirm">
          <p id="oracleConfirmText"></p>
          <div class="oracle-private-password hidden" id="oraclePrivatePasswordWrap">
            <input
              class="oracle-private-password-input"
              id="oraclePrivatePassword"
              type="password"
              placeholder={tr("Digita tu clave privada personal", "Enter your personal private key", "Saisis ta clé privée personnelle")}
              autocomplete="current-password"
            />
            <p class="oracle-private-password-error" id="oraclePrivatePasswordError"></p>
          </div>
          <div class="oracle-confirm-actions">
            <button class="btn btn-primary btn-compact" type="button" id="oracleConfirmYes">{tr("Sí", "Yes", "Oui")}</button>
            <button class="btn btn-outline btn-compact" type="button" id="oracleConfirmNo">{tr("No", "No", "Non")}</button>
          </div>
        </div>

        <div class="oracle-history" id="oracleHistory">
          <h4>{tr("Respuestas anteriores", "Previous responses", "Réponses précédentes")}</h4>
          <p class="oracle-history-note" id="oracleHistoryNote"></p>
          <div class="oracle-history-list" id="oracleHistoryList"></div>
        </div>
      </div>
    </div>
  </div>
