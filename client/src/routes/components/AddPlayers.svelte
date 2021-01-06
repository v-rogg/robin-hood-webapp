<script>
    import {players_store} from "../../stores.ts";
    import {io} from 'socket.io-client';

    const socket = io('ws://localhost:3000');

    let players;
    players_store.subscribe(value => players = value);

    let name;

    socket.on('players', data => {
        players_store.set(JSON.parse(data))
    })

    function addPlayer() {
        let user = {
            name: name,
        }
        name = null;

        socket.emit('addPlayer', user);
    }

    function removePlayer(event) {
        socket.emit('removePlayer', players.find(({uuid}) => uuid === event.target.id));
    }

    function startGame() {
        fetch('/api/start', {method: 'POST'})
    }

    function nextPlayer() {
        fetch('/api/next-player', {method: 'POST'})
    }
</script>

<style lang="sass">
    section
        //display: flex
        //flex-direction: column
        //justify-content: space-between
        //width: 100%
        //height: 100%
        display: flex
        flex-direction: column
        //justify-content: space-between
        height: 100%

    form
        display: flex
        justify-content: space-between
        //margin: 2.5rem auto 0

    input
        flex-grow: 1
        margin-right: 1em

    ul
        padding: 0
        margin: 1rem auto 0
        text-align: left
        list-style: none

    li
        width: max-content
        margin: .5em 0

        span
            font-family: "IBM Plex Mono SemiBold", sans-serif

        &:hover
            cursor: pointer
            text-decoration: line-through
            color: red

    .blue
        color: dodgerblue
</style>

<section>
    <form on:submit|preventDefault={addPlayer}>
        <input type="text" id="name" placeholder="Name" bind:value={name} pattern="[a-zA-Z]+\s?[a-zA-Z]+" minlength="3" maxlength="30">
        <button type="submit">Add player</button>
    </form>

    <ul>
        {#each players as {name, uuid, active, points}}
            <li on:click={removePlayer} id="{uuid}" class:blue={active}>
                {name} <span>{points}</span>
            </li>
        {/each}
    </ul>
</section>
