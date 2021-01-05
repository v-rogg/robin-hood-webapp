<script>
    import {onMount} from "svelte";
    import {players} from "../../stores.ts";
    import {io} from 'socket.io-client';

    const socket = io('ws://localhost:3000');

    let players_value;
    players.subscribe(value => players_value = value);

    let name;

    socket.on('players', data => {
        players.set(JSON.parse(data))
    })

    function addPlayer() {
        let user = {
            name: name,
        }
        name = null;

        socket.emit('addPlayer', user);
    }

    function removePlayer(event) {
        socket.emit('removePlayer', players_value[event.target.id]);
    }

    function startGame() {
        fetch('/api/start', {method: 'POST'})
    }

    function nextPlayer() {
        fetch('/api/next-player', {method: 'POST'})
    }

    onMount(() => {
        players.set(initialPlayers)
    })
</script>

<style lang="sass">
    form
        display: flex
        justify-content: space-between
        margin: 2.5rem auto 0

    input
        //width: 10rem
        flex-grow: 2
        margin-right: 1em

    ul
        padding: 0
        margin: 1rem auto 0
        text-align: left
        list-style: none

    li
        width: max-content
        margin: .5em 0

        &:hover
            cursor: pointer
            text-decoration: line-through
            color: red

    div
        margin: 5rem auto 0
        display: flex
        justify-content: right
        gap: 1em

    .blue
        color: dodgerblue
</style>

<form on:submit|preventDefault={addPlayer}>
    <input type="text" id="name" placeholder="Name" bind:value={name}>
    <button type="submit">Add player</button>
</form>

<hr/>

<ul>
    {#each players_value as {name, uuid, active}}
        <li on:click={removePlayer} id="{uuid}" class:blue={active}>
            {name}
        </li>
    {/each}
</ul>

<div>
    <button on:click={startGame}>
        Start Game
    </button>
    <button on:click={nextPlayer}>
        Next Player
    </button>
</div>
