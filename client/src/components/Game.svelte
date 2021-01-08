<script lang="ts">
    import {PLAYERS_STORE} from "../stores";
    import Players from "./Players.svelte";

    let players;

    PLAYERS_STORE.subscribe(value => players = value);
</script>

<style lang="sass">
</style>

<section id="game">
    <h1>Game is running!</h1>
    <Players/>
</section>
