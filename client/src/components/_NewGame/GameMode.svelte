<script lang="ts">
    import {io} from "socket.io-client";
    import {GAMEMODE_STORE} from "../../stores";
    const socket = io('ws://192.168.178.48:3000');

    let gamemode;
    GAMEMODE_STORE.subscribe(value => gamemode = value);

    function setGameMode(mode) {
        socket.emit('setGameMode', JSON.stringify({'gamemode': mode}))
    }
</script>

<style lang="sass">
    @import "src/styles/theme"

    .gamemode
        display: grid
        grid-template-columns: repeat(2, 1fr)

        button
            height: 80px
            display: flex
            align-items: center
            justify-content: center
            margin: 0
            font-size: 1.5rem
            font-weight: 500
            border: none
            border-bottom: 1px solid $grey
            background: none
            outline: none
            padding: 0

            &:not(&:last-of-type)
                border-left: 1px solid $grey

            &:hover
                cursor: pointer
                background: $grey

            &:active
                background: darken($grey, 10)

        &__highlight
            background: $lightgrey !important
</style>

<div class="gamemode">
    <button id="501" class:gamemode__highlight={gamemode === '501'} on:click={() => {setGameMode('501')}}>
        501
    </button>
    <button id="301" class:gamemode__highlight={gamemode === '301'} on:click={() => {setGameMode('301')}}>
        301
    </button>
</div>