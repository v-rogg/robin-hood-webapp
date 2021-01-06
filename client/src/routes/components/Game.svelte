<script lang="ts">
    import {players_store} from "../../stores";
    import Players from "./Players.svelte";

    let players;

    players_store.subscribe(value => players = value);
</script>

<style lang="sass">
</style>

<section id="game">
    <h1>Game is running!</h1>
    <Players/>
</section>
