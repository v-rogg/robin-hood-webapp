<script lang="ts">
    import {PLAYERS_STORE} from "../../stores";

    let players;
    PLAYERS_STORE.subscribe(value => players = value)

    function getCurrentPlayer(players) {
        let currentPlayer = {
            name: null,
            uuid: null,
            points: null,
            active: null,
            id: 0
        };
        for (let i = 0; i < players.length; i++) {
            if (players[i].active) {
                currentPlayer = players[i]
                currentPlayer.id = i
            }
        }
        return currentPlayer;
    }

    $: currentPlayer = getCurrentPlayer(players)
</script>

<style lang="sass">
    @import "src/styles/theme"

    #player
        background: $black
        color: white
        margin-top: 20px
        font-size: 1.5rem
        height: 60px
        display: flex
        justify-content: center
        align-items: center

        .even
            border-color: $red !important
            color: $red !important

        span
            border: 2px solid $green
            color: $green
            font-weight: 700
            font-size: 0.825rem
            border-radius: 100%
            width: 18px
            height: 18px
            position: relative
            display: flex
            align-items: center
            justify-content: center
            pointer-events: none
            line-height: 0
            margin-right: .5rem
</style>

<div id="player">
    <span class:even={(currentPlayer.id + 1) % 2 === 0}>{ currentPlayer.id + 1 }</span>
    { currentPlayer.name }
</div>