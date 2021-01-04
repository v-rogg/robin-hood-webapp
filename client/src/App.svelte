<script lang="ts">
    import Random from "./routes/components/Random.svelte";
    import AddPlayer from "./routes/components/Players.svelte";

    function startGame() {
        window.open('./start');
    }
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
</main>
