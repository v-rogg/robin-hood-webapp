<script lang="ts">
    import {onMount} from "svelte";
    import Random from "./routes/components/Random.svelte";
    import AddPlayer from "./routes/components/Players.svelte";
    import Game from "./routes/components/Game.svelte";

    let gameRunning = false;

    function startGame() {
        // window.open('./start');
        fetch('/start', {method: 'POST'});
        getGameRunning();
    }

    function getGameRunning() {
        fetch('./game')
        .then(response => response.json())
        .then(res => gameRunning = res.gameRunning);
    }

    onMount(() => {
        // getGameRunning();
        gameRunning = initialGameRunning;
    })

</script>

<style lang="sass">
    main
        font-family: "IBM Plex Sans", sans-serif
        font-weight: 400
        text-align: center
        padding: 1em
        max-width: 30rem
        margin: 0 auto
        font-variant-numeric: normal
        display: flex
        flex-direction: column
        gap: 3rem
</style>

<main>
    {#if !gameRunning}
    <section>
        <Random/>
    </section>
    <section>
        <AddPlayer/>
    </section>
    <section>
        <button on:click={startGame}>
            Start Game
        </button>
    </section>
    {:else}
    <section>
        <Game/>
    </section>
    {/if}
</main>
