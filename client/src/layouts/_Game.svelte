<script lang="ts">
    import {PLAYERS_STORE} from "../stores";

    let [d0, d1, d2] = [0, 0, 0];
    $: points = d0 + d1 + d2;

    let players;
    PLAYERS_STORE.subscribe(value => players = value)

    function getCurrentPlayer(x) {
        let currentPlayer = {
            name: null,
            uuid: null,
            points: null,
            active: null
        };
        x.forEach(player => {
            if (player.active) {
                currentPlayer = player
            }
        })
        return currentPlayer
    }

    $: currentPlayer = getCurrentPlayer(players)
</script>

<style lang="sass">
    @import "src/styles/theme"

    #dartboard
        max-height: 300px
        max-width: 300px

    form
        margin-top: 20px
        display: flex
        justify-content: center
        gap: 1rem

        input
            font-size: 4rem
            font-weight: 300
            width: 100px
            border: none
            border-bottom: 1px solid black
            outline: none
            text-align: center
            -moz-appearance: textfield
            &::-webkit-outer-spin-button, &::-webkit-inner-spin-button
                -webkit-appearance: none

    #player
        background: $black
        color: white
        padding: .5rem 0
        margin-top: 20px
        font-size: 1.5rem

    #points
        margin-top: 40px
        font-size: 6rem
        font-weight: 500
</style>

<picture>
    <source src="/app/dartboard-small.webp" type="image/webp">
    <img id="dartboard" src="/app/dartboard-small.png" type="image/png" alt="Dartboard">
</picture>

<form>
    <input type="number" min="0" max="60" placeholder="0" bind:value={d0}>
    <input type="number" min="0" max="60" placeholder="0" bind:value={d1}>
    <input type="number" min="0" max="60" placeholder="0" bind:value={d2}>
    <button type="submit" hidden></button>
</form>


<div id="player">
    { currentPlayer.name }
</div>

<div id="points">
    { currentPlayer.points }
</div>

<button on:click={() => { fetch('/api/next-player', {method: 'POST'}) }}>Next Player</button>