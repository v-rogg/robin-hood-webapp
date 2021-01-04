<script>
    import {onMount} from "svelte";
    import {players} from "../../stores.ts";
    import {io} from 'socket.io-client';

    const socket = io('ws://localhost:3000');

    let players_value;
    players.subscribe(value => players_value = value);

    let first_name;
    let last_name;

    function getPlayers() {
        // fetch('/api/players', {
        //         method: 'GET',
        //     })
        //         .then(response => response.json())
        //         .then(res => {
        //             players.set(res.players);
        //         })
    }

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

        // fetch('/api/players', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json;charset=utf-8'
        //     },
        //     body: JSON.stringify(user)
        // })
        //     .then(response => response.json())
        //     .then(res => {
        //         players.set(res.players);
        //     })
        socket.emit('addPlayer', user)
    }

    onMount(() => {
        // getPlayers();
        players.set(initialPlayers)
        console.log(players_value)
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
    {#each players_value as {first_name, last_name}}
        <li>
            {first_name} {last_name}
        </li>
    {/each}
</ul>