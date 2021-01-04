<script lang="ts">
    import {onMount} from "svelte";

    let players = [];

    function getPlayers() {
        fetch('./addPlayer', {
                method: 'GET',
            })
                .then(response => response.json())
                .then(res => {
                    players = res.players;
                })
    }

    let name;
    let surname;

    function addPlayer() {
        let user = {
            name: name,
            surname: surname,
        }
        name = null;
        surname = null;

        fetch('./addPlayer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(user)
        })
            .then(response => response.json())
            .then(res => {
                players = res.players
            })
    }

    onMount(() => {
        getPlayers();
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
</style>

<form on:submit|preventDefault={addPlayer}>
    <input type="text" id="name" placeholder="Name" bind:value={name}>
    <input type="text" id="surname" placeholder="Surname" bind:value={surname}>
    <button type="submit">Add player</button>
</form>

<ul>
    {#each players as {name, surname}}
        <li>
            {name} {surname}
        </li>
    {/each}
</ul>