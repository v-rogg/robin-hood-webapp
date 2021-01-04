<script>
    import {onMount} from "svelte";
    import {players} from "../../stores.ts";
    import {io} from 'socket.io-client';

    const socket = io('ws://localhost:3000');

    let players_value;
    players.subscribe(value => players_value = value);

    let first_name;
    let last_name;

    socket.on('players', data => {
        console.log(data)
        players.set(data)
    })

    function addPlayer() {
        let user = {
            first_name: first_name,
            last_name: last_name,
        }
        first_name = null;
        last_name = null;

        socket.emit('addPlayer', user)
    }

    function removePlayer(event) {
        console.log(players_value[event.target.id]);
        socket.emit('removePlayer', players_value[event.target.id]);
    }

    onMount(() => {
        players.set(initialPlayers)
    })
</script>

<style lang="sass">
    form
        display: flex
        justify-content: space-evenly

    input
        width: 10rem

    ul
        width: 10em
        margin: 1rem auto 0
        text-align: left
        list-style: none

    li
        &:hover
            color: dodgerblue
            cursor: pointer
</style>

<form on:submit|preventDefault={addPlayer}>
    <input type="text" id="name" placeholder="Name" bind:value={first_name}>
    <input type="text" id="surname" placeholder="Surname" bind:value={last_name}>
    <button type="submit">Add player</button>
</form>

<ul>
    {#each players_value as {first_name, last_name}, id}
        <li on:click={removePlayer} id="{id}">
            {first_name} {last_name}
        </li>
    {/each}
</ul>