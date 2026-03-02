const LOCALE_STORAGE_KEY = "kiadez_locale";
const SUPPORTED_LOCALES = ["es", "en", "fr"];
const FALLBACK_LOCALE = "en";

const MESSAGES = {
  es: {
    common: {
      brand: "Kiadez",
      languages: {
        es: "Español",
        en: "English",
        fr: "Français",
      },
    },
    footer: {
      poem: {
        line1: "Kiadez fue llamado por una estrella a subir el Monte Manjaro.",
        line2: "No para dominar, sino para orientar.",
        line3: "Su luz no deslumbra: acompaña.",
      },
      about_title: "Sobre nuestra red social",
      about_links: {
        what_is: "Qué es Kiadez",
        download_app: "Descarga la app",
        guardian_ranks: "Rangos de Guardianes",
        be_guardian: "Ser Guardián",
        contact: "Contacto",
      },
      languages_title: "Idiomas",
      contact_title: "Contacto",
      legal_title: "Información legal",
      legal_links: {
        game_rules: "Mis reglas de juego",
        terms: "Términos y condiciones",
        privacy: "Privacidad",
      },
      bottom: "© 2026 Kiadez — Una red social para cumplir deseos.",
    },
    auth: {
      login: {
        meta_title: "Kiadez — Iniciar sesión",
        title: "Bienvenido de vuelta",
        email_placeholder: "Correo electrónico",
        password_placeholder: "Contraseña",
        submit: "Entrar a Kiadez",
        forgot_password: "¿Olvidaste tu contraseña?",
        create_account: "Crear una cuenta nueva",
        errors: {
          start_session: "Error al iniciar sesión",
          twofa_incorrect: "Código 2FA incorrecto",
          vault_check: "No se pudo verificar el vault",
          life_purpose_check: "No se pudo verificar tu propósito de vida",
          invalid_credentials: "Correo electrónico o contraseña inválida.",
          generic: "No se pudo iniciar sesión.",
        },
        twofa: {
          modal_aria: "Verificación 2FA",
          title: "Verificación 2FA",
          description:
            "Digita el código de 6 dígitos de tu app autenticadora para completar el inicio de sesión.",
          input_placeholder: "123456",
          invalid_code: "Digita un código válido de 6 dígitos.",
          confirm: "Confirmar",
          cancel: "Cancelar",
          close_aria: "Cerrar",
        },
      },
      register: {
        meta_title: "Kiadez — Registro",
        title: "Crear cuenta en Kiadez",
        first_name_placeholder: "Nombre",
        last_name_placeholder: "Apellido",
        email_placeholder: "Correo electrónico",
        gender_placeholder: "Género",
        gender_male: "Hombre",
        gender_female: "Mujer",
        password_placeholder: "Contraseña",
        password_confirm_placeholder: "Confirmar contraseña",
        submit: "Crear cuenta",
        already_have_account: "¿Ya tienes cuenta? Inicia sesión",
        hero_subtitle: "El primer paso para cumplir tus deseos",
        hero_quote: "Todo gran viaje comienza cuando alguien se atreve a decir “sí”.",
        age_warning:
          "Si eres menor de edad, tu cuenta tendrá restricciones hasta que un padre o tutor la autorice.",
        password: {
          policy: "Debe incluir 8+ caracteres, 1 mayúscula, 1 número y 1 símbolo.",
          mismatch: "Las contraseñas deben coincidir.",
          show: "Mostrar contraseña",
          hide: "Ocultar contraseña",
        },
        alerts: {
          register_error: "Error al registrar usuario.",
          server_error: "No se pudo conectar con el servidor.",
        },
      },
      forgot_password: {
        meta_title: "Kiadez — Recuperar contraseña",
        title: "Recuperar contraseña",
        description: "Escribe tu correo y te enviaremos un enlace seguro.",
        email_placeholder: "Correo electrónico",
        submit: "Enviar enlace",
        status_sending: "Enviando enlace...",
        status_sent: "Si el correo existe, enviaremos un enlace de recuperación.",
        error_send: "No se pudo enviar el enlace.",
        back_to_login: "Volver al inicio de sesión",
      },
      reset_password: {
        meta_title: "Kiadez — Restablecer contraseña",
        title: "Restablecer contraseña",
        description: "Crea una nueva contraseña para tu cuenta.",
        password_placeholder: "Nueva contraseña",
        password_confirm_placeholder: "Confirmar contraseña",
        submit: "Actualizar contraseña",
        status_updating: "Actualizando contraseña...",
        errors: {
          token_invalid: "Token inválido.",
          password_required: "Debes digitar tu nueva contraseña.",
          password_policy:
            "La contraseña debe incluir mínimo 8 caracteres, 1 mayúscula, 1 número y 1 carácter especial.",
          password_mismatch: "Las contraseñas no coinciden.",
          update_failed: "No se pudo actualizar la contraseña.",
        },
        back_to_login: "Volver al inicio de sesión",
      },
      check_email: {
        meta_title: "Kiadez — Revisa tu correo",
        title: "Revisa tu correo",
        intro: "Te enviamos un enlace de verificación para activar tu cuenta.",
        hint: "Abre tu bandeja de entrada (y revisa spam si no lo ves).",
        resend: "Reenviar correo",
        resend_with_seconds: "Reenviar correo ({seconds})",
        back_to_login: "Volver al inicio de sesión",
        help: "Si cerraste la ventana o perdiste el enlace, puedes reenviar el correo desde aquí.",
        alerts: {
          missing_email: "No se encontró el correo en la URL.",
          resend_done: "Listo. Si el correo no estaba verificado, enviamos un enlace nuevo.",
          resend_failed: "No se pudo reenviar. Intenta de nuevo.",
          resend_loading: "Enviando...",
        },
      },
      email_verified: {
        meta_title: "Kiadez — Correo verificado",
        title: "Correo verificado",
        success_intro: "Tu cuenta ha sido activada con éxito.",
        redirecting: "Redirigiendo al inicio de sesión en {seconds}…",
        redirecting_short: "Redirigiendo al inicio de sesión…",
        login_button: "Iniciar sesión",
        invalid_intro: "No pudimos validar el enlace.",
        invalid_detail: "El enlace no es válido o expiró. Puedes solicitar uno nuevo.",
        back_to_check_email: "Volver a revisar el correo",
      },
    },
  },
  en: {
    common: {
      brand: "Kiadez",
      languages: {
        es: "Español",
        en: "English",
        fr: "Français",
      },
    },
    footer: {
      poem: {
        line1: "Kiadez was called by a star to climb Mount Manjaro.",
        line2: "Not to dominate, but to guide.",
        line3: "Its light does not blind: it accompanies.",
      },
      about_title: "About our social network",
      about_links: {
        what_is: "What is Kiadez",
        download_app: "Download the app",
        guardian_ranks: "Guardian Ranks",
        be_guardian: "Become a Guardian",
        contact: "Contact",
      },
      languages_title: "Languages",
      contact_title: "Contact",
      legal_title: "Legal Information",
      legal_links: {
        game_rules: "My game rules",
        terms: "Terms and conditions",
        privacy: "Privacy",
      },
      bottom: "© 2026 Kiadez — A social network to fulfill wishes.",
    },
    auth: {
      login: {
        meta_title: "Kiadez — Sign in",
        title: "Welcome back",
        email_placeholder: "Email address",
        password_placeholder: "Password",
        submit: "Enter Kiadez",
        forgot_password: "Forgot your password?",
        create_account: "Create a new account",
        errors: {
          start_session: "Sign-in failed",
          twofa_incorrect: "Incorrect 2FA code",
          vault_check: "Could not verify your vault status",
          life_purpose_check: "Could not verify your life purpose setup",
          invalid_credentials: "Invalid email or password.",
          generic: "Unable to sign in.",
        },
        twofa: {
          modal_aria: "2FA verification",
          title: "2FA verification",
          description:
            "Enter the 6-digit code from your authenticator app to complete sign-in.",
          input_placeholder: "123456",
          invalid_code: "Enter a valid 6-digit code.",
          confirm: "Confirm",
          cancel: "Cancel",
          close_aria: "Close",
        },
      },
      register: {
        meta_title: "Kiadez — Sign up",
        title: "Create your Kiadez account",
        first_name_placeholder: "First name",
        last_name_placeholder: "Last name",
        email_placeholder: "Email address",
        gender_placeholder: "Gender",
        gender_male: "Male",
        gender_female: "Female",
        password_placeholder: "Password",
        password_confirm_placeholder: "Confirm password",
        submit: "Create account",
        already_have_account: "Already have an account? Sign in",
        hero_subtitle: "The first step to fulfill your wishes",
        hero_quote: "Every great journey starts when someone dares to say “yes”.",
        age_warning:
          "If you are underage, your account will stay restricted until a parent or guardian approves it.",
        password: {
          policy: "Must include 8+ characters, 1 uppercase letter, 1 number, and 1 symbol.",
          mismatch: "Passwords must match.",
          show: "Show password",
          hide: "Hide password",
        },
        alerts: {
          register_error: "Could not register the account.",
          server_error: "Could not connect to the server.",
        },
      },
      forgot_password: {
        meta_title: "Kiadez — Recover password",
        title: "Recover password",
        description: "Enter your email and we will send you a secure link.",
        email_placeholder: "Email address",
        submit: "Send link",
        status_sending: "Sending link...",
        status_sent: "If the email exists, we will send a recovery link.",
        error_send: "Unable to send the link.",
        back_to_login: "Back to sign in",
      },
      reset_password: {
        meta_title: "Kiadez — Reset password",
        title: "Reset password",
        description: "Create a new password for your account.",
        password_placeholder: "New password",
        password_confirm_placeholder: "Confirm password",
        submit: "Update password",
        status_updating: "Updating password...",
        errors: {
          token_invalid: "Invalid token.",
          password_required: "You must enter your new password.",
          password_policy:
            "Password must include at least 8 characters, 1 uppercase letter, 1 number, and 1 special character.",
          password_mismatch: "Passwords do not match.",
          update_failed: "Could not update password.",
        },
        back_to_login: "Back to sign in",
      },
      check_email: {
        meta_title: "Kiadez — Check your email",
        title: "Check your email",
        intro: "We sent you a verification link to activate your account.",
        hint: "Open your inbox (and check spam if you do not see it).",
        resend: "Resend email",
        resend_with_seconds: "Resend email ({seconds})",
        back_to_login: "Back to sign in",
        help: "If you closed the window or lost the link, you can resend the email from here.",
        alerts: {
          missing_email: "Email was not found in the URL.",
          resend_done: "Done. If the email was not verified, we sent a new link.",
          resend_failed: "Could not resend. Please try again.",
          resend_loading: "Sending...",
        },
      },
      email_verified: {
        meta_title: "Kiadez — Email verified",
        title: "Email verified",
        success_intro: "Your account has been activated successfully.",
        redirecting: "Redirecting to sign in in {seconds}…",
        redirecting_short: "Redirecting to sign in…",
        login_button: "Sign in",
        invalid_intro: "We could not validate the link.",
        invalid_detail: "The link is invalid or expired. You can request a new one.",
        back_to_check_email: "Back to email verification",
      },
    },
  },
  fr: {
    common: {
      brand: "Kiadez",
      languages: {
        es: "Español",
        en: "English",
        fr: "Français",
      },
    },
    footer: {
      poem: {
        line1: "Kiadez fut appelé par une étoile à gravir le mont Manjaro.",
        line2: "Non pour dominer, mais pour guider.",
        line3: "Sa lumière n'éblouit pas : elle accompagne.",
      },
      about_title: "À propos de notre réseau social",
      about_links: {
        what_is: "Qu'est-ce que Kiadez",
        download_app: "Télécharger l'application",
        guardian_ranks: "Rangs des Gardiens",
        be_guardian: "Devenir Gardien",
        contact: "Contact",
      },
      languages_title: "Langues",
      contact_title: "Contact",
      legal_title: "Informations légales",
      legal_links: {
        game_rules: "Mes règles du jeu",
        terms: "Termes et conditions",
        privacy: "Confidentialité",
      },
      bottom: "© 2026 Kiadez — Un réseau social pour accomplir des souhaits.",
    },
    auth: {
      login: {
        meta_title: "Kiadez — Se connecter",
        title: "Bon retour",
        email_placeholder: "Adresse e-mail",
        password_placeholder: "Mot de passe",
        submit: "Entrer dans Kiadez",
        forgot_password: "Mot de passe oublié ?",
        create_account: "Créer un nouveau compte",
        errors: {
          start_session: "Échec de connexion",
          twofa_incorrect: "Code 2FA incorrect",
          vault_check: "Impossible de vérifier l'état de votre coffre",
          life_purpose_check: "Impossible de vérifier votre objectif de vie",
          invalid_credentials: "E-mail ou mot de passe invalide.",
          generic: "Impossible de se connecter.",
        },
        twofa: {
          modal_aria: "Vérification 2FA",
          title: "Vérification 2FA",
          description:
            "Saisissez le code à 6 chiffres de votre application d'authentification pour terminer la connexion.",
          input_placeholder: "123456",
          invalid_code: "Saisissez un code valide à 6 chiffres.",
          confirm: "Confirmer",
          cancel: "Annuler",
          close_aria: "Fermer",
        },
      },
      register: {
        meta_title: "Kiadez — Inscription",
        title: "Créer votre compte Kiadez",
        first_name_placeholder: "Prénom",
        last_name_placeholder: "Nom",
        email_placeholder: "Adresse e-mail",
        gender_placeholder: "Genre",
        gender_male: "Homme",
        gender_female: "Femme",
        password_placeholder: "Mot de passe",
        password_confirm_placeholder: "Confirmer le mot de passe",
        submit: "Créer un compte",
        already_have_account: "Vous avez déjà un compte ? Connectez-vous",
        hero_subtitle: "La première étape pour accomplir vos souhaits",
        hero_quote: "Tout grand voyage commence quand quelqu'un ose dire « oui ».",
        age_warning:
          "Si vous êtes mineur, votre compte restera restreint jusqu'à l'approbation d'un parent ou tuteur.",
        password: {
          policy: "Doit inclure 8+ caractères, 1 majuscule, 1 chiffre et 1 symbole.",
          mismatch: "Les mots de passe doivent correspondre.",
          show: "Afficher le mot de passe",
          hide: "Masquer le mot de passe",
        },
        alerts: {
          register_error: "Impossible d'enregistrer le compte.",
          server_error: "Impossible de se connecter au serveur.",
        },
      },
      forgot_password: {
        meta_title: "Kiadez — Récupérer le mot de passe",
        title: "Récupérer le mot de passe",
        description: "Saisissez votre e-mail et nous vous enverrons un lien sécurisé.",
        email_placeholder: "Adresse e-mail",
        submit: "Envoyer le lien",
        status_sending: "Envoi du lien...",
        status_sent: "Si l'e-mail existe, nous enverrons un lien de récupération.",
        error_send: "Impossible d'envoyer le lien.",
        back_to_login: "Retour à la connexion",
      },
      reset_password: {
        meta_title: "Kiadez — Réinitialiser le mot de passe",
        title: "Réinitialiser le mot de passe",
        description: "Créez un nouveau mot de passe pour votre compte.",
        password_placeholder: "Nouveau mot de passe",
        password_confirm_placeholder: "Confirmer le mot de passe",
        submit: "Mettre à jour le mot de passe",
        status_updating: "Mise à jour du mot de passe...",
        errors: {
          token_invalid: "Jeton invalide.",
          password_required: "Vous devez saisir votre nouveau mot de passe.",
          password_policy:
            "Le mot de passe doit inclure au moins 8 caractères, 1 majuscule, 1 chiffre et 1 caractère spécial.",
          password_mismatch: "Les mots de passe ne correspondent pas.",
          update_failed: "Impossible de mettre à jour le mot de passe.",
        },
        back_to_login: "Retour à la connexion",
      },
      check_email: {
        meta_title: "Kiadez — Vérifiez votre e-mail",
        title: "Vérifiez votre e-mail",
        intro: "Nous vous avons envoyé un lien de vérification pour activer votre compte.",
        hint: "Ouvrez votre boîte de réception (et vérifiez les spams si vous ne le voyez pas).",
        resend: "Renvoyer l'e-mail",
        resend_with_seconds: "Renvoyer l'e-mail ({seconds})",
        back_to_login: "Retour à la connexion",
        help: "Si vous avez fermé la fenêtre ou perdu le lien, vous pouvez renvoyer l'e-mail depuis ici.",
        alerts: {
          missing_email: "L'e-mail n'a pas été trouvé dans l'URL.",
          resend_done: "Terminé. Si l'e-mail n'était pas vérifié, nous avons envoyé un nouveau lien.",
          resend_failed: "Impossible de renvoyer. Veuillez réessayer.",
          resend_loading: "Envoi...",
        },
      },
      email_verified: {
        meta_title: "Kiadez — E-mail vérifié",
        title: "E-mail vérifié",
        success_intro: "Votre compte a été activé avec succès.",
        redirecting: "Redirection vers la connexion dans {seconds}…",
        redirecting_short: "Redirection vers la connexion…",
        login_button: "Se connecter",
        invalid_intro: "Nous n'avons pas pu valider le lien.",
        invalid_detail: "Le lien est invalide ou expiré. Vous pouvez en demander un nouveau.",
        back_to_check_email: "Retour à la vérification de l'e-mail",
      },
    },
  },
};

const KEY_SEPARATOR = ".";

let bootstrapped = false;
let currentLocale = FALLBACK_LOCALE;

function normalizeLocale(raw) {
  const value = String(raw || "").trim().toLowerCase();
  if (!value) return null;
  if (value.startsWith("es")) return "es";
  if (value.startsWith("en")) return "en";
  if (value.startsWith("fr")) return "fr";
  return null;
}

function localeFromUrl() {
  if (typeof window === "undefined") return null;
  const params = new URLSearchParams(window.location.search);
  return normalizeLocale(params.get("lang"));
}

function localeFromStorage() {
  if (typeof window === "undefined") return null;
  try {
    return normalizeLocale(window.localStorage.getItem(LOCALE_STORAGE_KEY));
  } catch {
    return null;
  }
}

function localeFromBrowser() {
  if (typeof navigator === "undefined") return null;
  const candidates = Array.isArray(navigator.languages) && navigator.languages.length
    ? navigator.languages
    : [navigator.language];

  for (const candidate of candidates) {
    const normalized = normalizeLocale(candidate);
    if (normalized) return normalized;
  }
  return null;
}

function applyLocaleSideEffects(localeCode) {
  if (typeof document !== "undefined") {
    document.documentElement.lang = localeCode;
  }
  if (typeof window !== "undefined") {
    try {
      window.localStorage.setItem(LOCALE_STORAGE_KEY, localeCode);
    } catch {
      // Ignore storage restrictions.
    }
  }
}

function resolveInitialLocale() {
  return (
    localeFromUrl() ||
    localeFromStorage() ||
    localeFromBrowser() ||
    FALLBACK_LOCALE
  );
}

function resolveKey(target, path) {
  return String(path || "")
    .split(KEY_SEPARATOR)
    .filter(Boolean)
    .reduce((cursor, part) => {
      if (cursor && typeof cursor === "object" && part in cursor) {
        return cursor[part];
      }
      return undefined;
    }, target);
}

function interpolate(template, vars = {}) {
  if (typeof template !== "string") return "";
  return template.replace(/\{([a-zA-Z0-9_]+)\}/g, (_, key) => {
    if (!(key in vars)) return `{${key}}`;
    return String(vars[key]);
  });
}

export function bootstrapLocale() {
  if (bootstrapped) return currentLocale;
  currentLocale = resolveInitialLocale();
  applyLocaleSideEffects(currentLocale);
  bootstrapped = true;
  return currentLocale;
}

export function getLocale() {
  return bootstrapLocale();
}

export function setLocale(nextLocale) {
  const normalized = normalizeLocale(nextLocale) || FALLBACK_LOCALE;
  currentLocale = normalized;
  applyLocaleSideEffects(normalized);
  bootstrapped = true;
  return currentLocale;
}

export function t(key, vars = {}) {
  const activeLocale = getLocale();
  const localized = resolveKey(MESSAGES[activeLocale], key);
  if (typeof localized === "string") return interpolate(localized, vars);

  const fallback = resolveKey(MESSAGES[FALLBACK_LOCALE], key);
  if (typeof fallback === "string") return interpolate(fallback, vars);

  return String(key);
}

export function buildLangHref(targetLocale) {
  const normalized = normalizeLocale(targetLocale) || FALLBACK_LOCALE;
  if (typeof window === "undefined") return `?lang=${normalized}`;

  const url = new URL(window.location.href);
  url.searchParams.set("lang", normalized);
  return `${url.pathname}${url.search}${url.hash}`;
}

export function supportedLocales() {
  return [...SUPPORTED_LOCALES];
}

bootstrapLocale();
