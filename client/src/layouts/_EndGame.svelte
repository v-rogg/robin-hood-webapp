<script lang="ts">
    import PlayerList from "../components/_EndGame/PlayerList.svelte";
    import NextButtons from "../components/_EndGame/NextButtons.svelte";

    import {PLAYERS_STORE} from "../stores";

    let players;
    PLAYERS_STORE.subscribe(value => players = value);
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
</style>

<h1>
    {#if players.length > 0}
        {players[0].name}
    {/if}
</h1>
<h2>Winner</h2>

<PlayerList/>
<NextButtons/>
<!--<GameMode/>-->
<!--<StartButton/>-->