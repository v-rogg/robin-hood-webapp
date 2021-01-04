<script>
    import {onMount} from "svelte";
    import {players} from "../../stores.ts";

    let players_value;
    players.subscribe(value => players_value = value);

    let first_name;
    let last_name;

    function getPlayers() {
        fetch('/api/players', {
                method: 'GET',
            })
                .then(response => response.json())
                .then(res => {
                    players.set(res.players);
                })
    }

    function addPlayer() {
        let user = {
            first_name: first_name,
            last_name: last_name,
        }
        first_name = null;
        last_name = null;

        fetch('/api/players', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(user)
        })
            .then(response => response.json())
            .then(res => {
                players.set(res.players);
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