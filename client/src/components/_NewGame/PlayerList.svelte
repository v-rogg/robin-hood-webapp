<script lang="ts">
    import {io} from "socket.io-client";
    import {PLAYERS_STORE} from "../../stores";
    const socket = io('ws://192.168.178.48:3000');

    let name;
    let players;
    PLAYERS_STORE.subscribe(value => players = value);

    function removePlayer(event) {
        socket.emit('removePlayer', JSON.stringify(players.find(({uuid}) => uuid === event.target.id)))
    }

    function addPlayer() {
        let user = {
            name: name,
        }
        name = null;
        socket.emit('addPlayer', JSON.stringify(user));
    }
</script>

<style lang="sass">
    @import "src/styles/theme"

    ul
        list-style: none
        padding: 0
        margin: 80px 0 0

    li
        height: 80px
        font-family: 'Rubik', sans-serif
        font-size: 1.5rem
        font-weight: 500
        display: flex
        flex-direction: column
        align-items: center
        justify-content: center
        border-top: 1px solid $grey

        &:nth-child(2n+1)
            background: $beige

        &:nth-child(2n+1)
            span
                color: $green
                border-color: $green

        &:nth-child(2n)
            span
                color: $red
                border-color: $red

        &:last-of-type
            border-bottom: 1px solid $grey

        &:hover
            cursor: pointer

            div
                color: $red
                text-decoration: line-through


        div
            height: 1.75rem
            pointer-events: none

        span
            border: 2px solid $grey
            color: $grey
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
            margin-bottom: .25rem
            line-height: 0

    .add
        font-family: 'Rubik', sans-serif
        font-weight: 300
        background: $black !important

        &:hover
            background: lighten($black, 10) !important

        span
            color: white !important
            border-color: white !important

        form
            width: 100%
            height: 1.75rem

        input
            font-family: 'Rubik', sans-serif
            background: none
            border: none
            width: 95%
            text-align: center
            font-size: 1.5rem
            color: white
            outline-style: none

            &::placeholder
                color: white
                font-family: 'Rubik', sans-serif
                font-weight: 100
</style>

<ul id="playerlist">
    {#each players as {name, uuid, active, points}, nr}
        <li on:click={removePlayer} id="{uuid}" class:blue={active}>
            <span>{nr + 1}</span>
            <div>
                {name}
            </div>
        </li>
    {/each}
    <li class="add" on:click={() => {document.getElementById('new-player-input').focus()}}>
        <span>+</span>
        <form on:submit|preventDefault={addPlayer}>
            <input type="text" placeholder="New player" id="new-player-input" bind:value={name}>
            <button type="submit" hidden></button>
        </form>
    </li>
</ul>