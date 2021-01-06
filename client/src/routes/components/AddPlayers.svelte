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
        socket.emit('removePlayer', players.find(({uuid}) => uuid === event.target.parentNode.id));
    }
</script>

<style lang="sass">
    section
        display: flex
        flex-direction: column
        align-items: center
        height: 100%

    form
        display: flex
        justify-content: space-between
        width: 100%
        margin: 0 auto 2.3rem

    input
        flex-grow: 1
        margin-right: 1em

    table
        padding: 0
        margin: 0
        text-align: left
        list-style: none
        min-width: 10rem
        border-collapse: collapse

    th
        text-align: center
        border-bottom: 1px solid black

    tr
        width: max-content
        margin: .5em 0

        &:nth-child(2n)
            background: #DFDFDF

        td
            padding: .5em 1em

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

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Points</th>
                <th>UUID</th>
                <th>State</th>
            </tr>
        </thead>
        <tbody>
            {#each players as {name, uuid, active, points}}
                <tr on:click={removePlayer} id="{uuid}" class:blue={active}>
                    <td>{name}</td>
                    <td><span>{points}</span></td>
                    <td>{uuid}</td>
                    <td>{active}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</section>
