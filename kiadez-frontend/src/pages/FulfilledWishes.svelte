<script>
  import { onMount } from "svelte";
  import AuthFooter from "../lib/AuthFooter.svelte";
  import { initPurposeCoverModule } from "../lib/purposeCover";
  import { syncProfileStarsTotal } from "../lib/starsCounter";

  onMount(() => {
    initPurposeCoverModule();
    void syncProfileStarsTotal("fulfilledWishesSimpleStarsTotal");
  });
</script>

<svelte:head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kiadez — My fulfilled wishes</title>
  <link rel="stylesheet" href="/css/styles.css" />
</svelte:head>

<div class="page-background page-background-user home-background">
  <main class="user-home">
  <section class="cover" id="cover">
      <div class="cover-media" id="coverMedia">
        <img id="coverImg" class="cover-img" src="assets/cover-default.jpg" alt="Cover" />

        <div class="cover-actions">
          <button class="icon-btn" id="btnChangeCover" type="button" title="Change cover">
            Change cover
          </button>
          <button class="icon-btn" id="btnEditPurposes" type="button" title="Edit purpose wishes">
            Edit purpose
          </button>

          <input id="coverFile" type="file" accept="image/*" class="hidden" />
        </div>

        <div class="purpose-triangle" aria-label="Purpose wishes">
          <button class="purpose-pill purpose-top" type="button" id="purpose1">
            Wish #1: Secret
          </button>

          <button class="purpose-pill purpose-left" type="button" id="purpose2">
            I wish to build the Kingdom of Combray
          </button>

          <button class="purpose-pill purpose-right" type="button" id="purpose3">
            I wish to be united with Jesus
          </button>
        </div>

        <div class="cover-hint" id="coverHint">
          Drag the cover to frame it
        </div>
      </div>
    </section>

    <div class="home-body">
      <nav class="profile-nav" aria-label="Profile navigation">
        <a class="nav-pill" href="/home_user.html" title="Home">Home</a>
        <a class="nav-pill" href="/star-pool-found.html" title="Stars">
          <span class="nav-icon">⭐</span>
          <span><strong id="fulfilledWishesSimpleStarsTotal">0</strong> stars</span>
        </a>

        <a class="nav-pill" href="/followers.html" title="Followers">Followers</a>
        <a class="nav-pill" href="/achievements.html" title="Recent achievements">Recent achievements</a>
        <a class="nav-pill" href="/gallery.html" title="Gallery">Gallery</a>
        <a class="nav-pill" href="/calendar.html" title="Calendar">Calendar</a>
        <a class="nav-pill" href="/my-biography.html" title="My biography">My biography</a>
        <a class="nav-pill" href="/messages.html" title="Messages">Messages</a>
      </nav>

      <section class="panel">
        <div class="panel-head">
          <h2 class="panel-title">My fulfilled wishes</h2>
          <span class="panel-badge">5 achievements</span>
        </div>
        <p class="panel-muted">Every fulfilled wish strengthens your story.</p>

        <ul class="wish-list">
          <li class="wish-item"><span class="wish-dot"></span> Officially launch Kiadez</li>
          <li class="wish-item"><span class="wish-dot"></span> Reach the first one million users</li>
          <li class="wish-item"><span class="wish-dot"></span> Finish the design of the Sanctuary of the Logos</li>
          <li class="wish-item"><span class="wish-dot"></span> Travel to Mount Manjaro</li>
          <li class="wish-item"><span class="wish-dot"></span> Recover the sold Dofus</li>
        </ul>
      </section>
    </div>
  </main>
  <AuthFooter />

</div>
