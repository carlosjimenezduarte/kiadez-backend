<script>
  import { onMount } from 'svelte';
  import { syncTopbarAvatar } from './lib/topbarAvatar';
  import { initTopbarNotifications } from './lib/topbarNotifications';
  import { initTopbarSearch } from './lib/topbarSearch';
  import { installAuthSessionInterceptor } from './lib/authSession';
  import Landing from './pages/Landing.svelte';
  import StarPoolFound from './pages/StarPoolFound.svelte';
  import HomeUser from './pages/HomeUser.svelte';
  import Achievements from './pages/Achievements.svelte';
  import BeAGuardian from './pages/BeAGuardian.svelte';
  import Calendar from './pages/Calendar.svelte';
  import CheckEmail from './pages/CheckEmail.svelte';
  import CreatePrivateKey from './pages/CreatePrivateKey.svelte';
  import Emailprueba from './pages/Emailprueba.svelte';
  import EmailVerified from './pages/EmailVerified.svelte';
  import GameStar from './pages/GameStar.svelte';
  import GuardiansRank from './pages/GuardiansRank.svelte';
  import LifeProposal from './pages/LifeProposal.svelte';
  import Login from './pages/Login.svelte';
  import MyBiography from './pages/MyBiography.svelte';
  import MyFulfilledWhises from './pages/MyFulfilledWhises.svelte';
  import MyPublicWhishes from './pages/MyPublicWhishes.svelte';
  import Oracle from './pages/Oracle.svelte';
  import Register from './pages/Register.svelte';
  import WhatIsKiadez from './pages/WhatIsKiadez.svelte';
  import Followers from './pages/Followers.svelte';
  import Gallery from './pages/Gallery.svelte';
  import Contact from './pages/Contact.svelte';
  import DownloadApp from './pages/DownloadApp.svelte';
  import Terms from './pages/Terms.svelte';
  import Privacy from './pages/Privacy.svelte';
  import MyGameRules from './pages/MyGameRules.svelte';
  import ForgotPassword from './pages/ForgotPassword.svelte';
  import FulfilledWishes from './pages/FulfilledWishes.svelte';
  import ResetPassword from './pages/ResetPassword.svelte';
  import Feed from './pages/Feed.svelte';
  import MyPrivateWhishes from './pages/MyPrivateWhishes.svelte';
  import PrivacyAndSettings from './pages/PrivacyAndSettings.svelte';
  import GuardianCenter from './pages/GuardianCenter.svelte';
  import Messages from './pages/Messages.svelte';
  import Notifications from './pages/Notifications.svelte';

  const path = typeof window !== 'undefined' ? window.location.pathname : '/';
  const route = path.replace(/\/+$/, '') || '/';

  installAuthSessionInterceptor();

  const routes = {
    '/': Landing,
    '/index.html': Landing,
    '/star-pool': StarPoolFound,
    '/star-pool-found': StarPoolFound,
    '/star-pool-found.html': StarPoolFound,
    '/home_user': HomeUser,
    '/home_user.html': HomeUser,
    '/achievements': Achievements,
    '/achievements.html': Achievements,
    '/be-a-guardian': BeAGuardian,
    '/be-a-guardian.html': BeAGuardian,
    '/calendar': Calendar,
    '/calendar.html': Calendar,
    '/check-email': CheckEmail,
    '/check-email.html': CheckEmail,
    '/create-private-key': CreatePrivateKey,
    '/create-private-key.html': CreatePrivateKey,
    '/emailprueba': Emailprueba,
    '/emailprueba.html': Emailprueba,
    '/email-verified': EmailVerified,
    '/email-verified.html': EmailVerified,
    '/game-star': GameStar,
    '/game-star.html': GameStar,
    '/guardians-rank': GuardiansRank,
    '/guardians-rank.html': GuardiansRank,
    '/life-proposal': LifeProposal,
    '/life-proposal.html': LifeProposal,
    '/login': Login,
    '/login.html': Login,
    '/my-biography': MyBiography,
    '/my-biography.html': MyBiography,
    '/my-fulfilled-whises': MyFulfilledWhises,
    '/my-fulfilled-whises.html': MyFulfilledWhises,
    '/my-public-whishes': MyPublicWhishes,
    '/my-public-whishes.html': MyPublicWhishes,
    '/oracle': Oracle,
    '/oracle.html': Oracle,
    '/register': Register,
    '/register.html': Register,
    '/what-is-kiadez': WhatIsKiadez,
    '/what-is-kiadez.html': WhatIsKiadez,
    '/followers': Followers,
    '/followers.html': Followers,
    '/gallery': Gallery,
    '/gallery.html': Gallery,
    '/contact': Contact,
    '/contact.html': Contact,
    '/downloadapp': DownloadApp,
    '/downloadapp.html': DownloadApp,
    '/terms': Terms,
    '/terms.html': Terms,
    '/privacy': Privacy,
    '/privacy.html': Privacy,
    '/mygamerules': MyGameRules,
    '/mygamerules.html': MyGameRules,
    '/forgot-password': ForgotPassword,
    '/forgot-password.html': ForgotPassword,
    '/fulfilled-wishes': FulfilledWishes,
    '/fulfilled-wishes.html': FulfilledWishes,
    '/reset-password': ResetPassword,
    '/reset-password.html': ResetPassword,
    '/feed': Feed,
    '/feed.html': Feed,
    '/my-private-whishes': MyPrivateWhishes,
    '/my-private-whishes.html': MyPrivateWhishes,
    '/privacy-and-settings': PrivacyAndSettings,
    '/privacy-and-settings.html': PrivacyAndSettings,
    '/guardiancenter': GuardianCenter,
    '/guardiancenter.html': GuardianCenter,
    '/messages': Messages,
    '/messages.html': Messages,
    '/notifications': Notifications,
    '/notifications.html': Notifications,
  };

  const Component = routes[route] || Landing;

  onMount(() => {
    void syncTopbarAvatar();
    const cleanupNotifications = initTopbarNotifications();
    const cleanupTopbarSearch = initTopbarSearch();
    return () => {
      if (typeof cleanupNotifications === 'function') cleanupNotifications();
      if (typeof cleanupTopbarSearch === 'function') cleanupTopbarSearch();
    };
  });
</script>

<svelte:component this={Component} />
