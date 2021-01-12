<script lang="ts">
    import PlayerList from "../components/_EndGame/PlayerList.svelte";
    import NextButtons from "../components/_EndGame/NextButtons.svelte";
    import * as canvasConfetti from "canvas-confetti";


    import {PLAYERS_STORE} from "../stores";

    let players;
    PLAYERS_STORE.subscribe(value => players = value);

    let confettiCanvas = document.getElementById('confetti');

    const confettiObj = canvasConfetti.create(<HTMLCanvasElement>confettiCanvas, {
        resize: true,
        useWorker: true
    });


    const duration = 5 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
      return Math.random() * (max - min) + min;
    }

    let interval = setInterval(function() {
      let timeLeft = animationEnd - Date.now();

      if (timeLeft <= 0) {
        return clearInterval(interval);
      }

      let particleCount = 50 * (timeLeft / duration);
      // since particles fall down, start a bit higher than random
      confettiObj(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
      confettiObj(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);
</script>

<style lang="sass">
    h1, h2
        margin: 0
        padding: 0

    h1
        font-size: 3rem
        font-weight: 600

    h2
        font-size: 1.5rem
        font-weight: 300

    canvas
        width: 0
        height: 0
</style>

<h1>
    {#if players.length > 0}
        {players[0].name}
    {/if}
</h1>
<h2>Winner</h2>

<canvas id="confetti"></canvas>

<PlayerList/>
<NextButtons/>
<!--<GameMode/>-->
<!--<StartButton/>-->