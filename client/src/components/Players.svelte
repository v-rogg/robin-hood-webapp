<script>
    import {PLAYERS_STORE} from "../stores.ts";
    import {io} from 'socket.io-client';

    const socket = io('ws://192.168.178.48:3000');

    let players;
    PLAYERS_STORE.subscribe(value => players = value);

    let name;

    socket.on('players', data => {
        PLAYERS_STORE.set(JSON.parse(data))
    })

    function removePlayer(event) {
        console.log(event)
        socket.emit('removePlayer', JSON.stringify(players.find(({uuid}) => uuid === event.target.parentNode.id)));
    }
</script>

<style lang="sass">
    section
        display: flex
        flex-direction: column
        align-items: center

    table
        padding: 0
        margin: 0
        text-align: left
        list-style: none
        //min-width: 30rem
        width: 100%
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
            text-align: center

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
    <h1>
        Players:
    </h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Points</th>
<!--                <th>UUID</th>-->
<!--                <th>State</th>-->
            </tr>
        </thead>
        <tbody>
            {#each players as {name, uuid, active, points}}
                <tr on:click={removePlayer} id="{uuid}" class:blue={active}>
                    <td>{name}</td>
                    <td><span>{points}</span></td>
<!--                    <td>{uuid}</td>-->
<!--                    <td>{active}</td>-->
                </tr>
            {/each}
        </tbody>
    </table>
</section>
