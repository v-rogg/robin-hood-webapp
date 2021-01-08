<script lang="ts">
    import {CLIENT_STATE_STORE, GAMEMODE_STORE, PLAYERS_STORE} from "../stores.ts";
    import {io} from "socket.io-client";
    const socket = io('ws://192.168.178.48:3000');

    let players, gamemode, client_state;
    PLAYERS_STORE.subscribe(value => players = value);
    GAMEMODE_STORE.subscribe(value => gamemode = value);
    CLIENT_STATE_STORE.subscribe(value => client_state = value);

    function removePlayer(event) {
        console.log(event)
        socket.emit('removePlayer', JSON.stringify(players.find(({uuid}) => uuid === event.target.id)))
    }

    function setGameMode(mode) {
        socket.emit('setGameMode', JSON.stringify({'gamemode': mode}))
    }

    // function switchMode() {
    //     switch (CLIENT_STATE) {
    //         case 'New Game':
    //             CLIENT_STATE_STORE.set('Add Players');
    //             break;
    //         case 'Add Players':
    //             CLIENT_STATE_STORE.set('New Game');
    //             break;
    //     }
    // }

    let name;

    function addPlayer() {
        let user = {
            name: name,
        }
        name = null;

        socket.emit('addPlayer', JSON.stringify(user));
    }

    function startGame() {
        fetch('/api/start', {method: 'POST'})
    }

</script>

<style lang="sass">
    @import "src/styles/theme"

    h1, h2
        //font-family: "Pulp Display", sans-serif
        font-family: 'Rubik', sans-serif
        margin: 0
        padding: 0

    h1
        font-size: 3rem
        font-weight: 600

    h2
        font-size: 1.5rem
        font-weight: 300

    ul
        list-style: none
        padding: 0
        margin: 80px 0 0


    li
        height: 80px
        //font-family: "Pulp Display", sans-serif
        font-family: 'Rubik', sans-serif
        font-size: 1.5rem
        font-weight: 500
        display: flex
        flex-direction: column
        align-items: center
        justify-content: center
        border-top: 1px solid #C5C5C5
        //padding: 1rem 0 1.25rem

        &:nth-child(2n+1)
            //background: #E8E8E8
            background: #FBEAD1

        &:nth-child(2n+1)
            span
                color: #19A962
                border-color: #19A962

        &:nth-child(2n)
            span
                color: #E8472F
                border-color: #E8472F

        &:last-of-type
            border-bottom: 1px solid #C5C5C5

        &:hover
            cursor: pointer
            //background: #C5C5C5
            //background: lighten(#E8472F, 15)

            div
                color: #E8472F
                text-decoration: line-through


        div
            height: 1.75rem
            pointer-events: none

        span
            border: 2px solid #C5C5C5
            color: #C5C5C5
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

    .gamemode
        display: grid
        grid-template-columns: repeat(2, 1fr)

        div
            height: 80px
            display: flex
            align-items: center
            justify-content: center
            //padding: 1.75rem 0 2rem
            margin: 0
            //font-family: "Pulp Display", sans-serif
            font-family: 'Rubik', sans-serif
            font-size: 1.5rem
            font-weight: 500
            border-bottom: 1px solid #C5C5C5

            &:not(&:last-of-type)
                border-left: 1px solid #C5C5C5

            &:hover
                cursor: pointer
                background: #C5C5C5

        &__highlight
            background: #E8E8E8
            //background: #FBEAD1

    .add
        //font-family: "Pulp Display", sans-serif
        font-family: 'Rubik', sans-serif
        font-weight: 300
        background: #030404 !important

        &:hover
            //cursor: pointer
            background: lighten(#030404, 10) !important

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

    .start-game
        cursor: pointer
        width: max-content
        margin: 80px 3rem 0 auto
        display: block
        position: relative

        svg
            position: relative
            display: block

        &--outer-circle, &--inner-circle
            fill: #030404

        &:hover
            .start-game--outer-circle
                fill: $green
            .start-game--inner-circle
                fill: $red

</style>

<h1>New Game</h1>
<h2>Players & Game Mode</h2>

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

<div class="gamemode">
    <div id="501" class:gamemode__highlight={gamemode === '501'} on:click={() => {setGameMode('501')}}>
        501
    </div>
    <div id="301" class:gamemode__highlight={gamemode === '301'} on:click={() => {setGameMode('301')}}>
        301
    </div>
</div>

<div class="start-game" on:click={startGame}>
    <svg x="0px" y="0px" viewBox="0 0 70 70" width="70px" height="70px">
        <path class="start-game--outer-circle" d="M35,0C15.67,0,0,15.67,0,35s15.67,35,35,35s35-15.67,35-35S54.33,0,35,0z M35,62
            C20.09,62,8,49.91,8,35S20.09,8,35,8s27,12.09,27,27S49.91,62,35,62z"/>
        <path class="start-game--inner-circle" d="M35,53c-9.93,0-18-8.08-18-18c0-9.93,8.07-18,18-18c9.92,0,18,8.07,18,18C53,44.92,44.92,53,35,53z
             M35,26c-4.96,0-9,4.04-9,9c0,4.96,4.04,9,9,9c4.96,0,9-4.04,9-9C44,30.04,39.96,26,35,26z"/>
    </svg>
</div>