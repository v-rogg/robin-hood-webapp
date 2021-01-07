<script lang="ts">
    import {onMount} from "svelte";
    import Players from "./routes/components/Players.svelte";
    import AddPlayers from "./routes/components/AddPlayers.svelte";
    import Game from "./routes/components/Game.svelte";
    import States from "./routes/components/States.svelte";
    import {io} from "socket.io-client";

    import {CLIENT_STATE_STORE, players_store, SERVER_STATE_STORE} from "./stores";
    import Controls from "./routes/components/Controls.svelte";

    const socket = io('ws://192.168.178.48:3000');

    let CLIENT_STATE, SERVER_STATE;
    CLIENT_STATE_STORE.subscribe(value => CLIENT_STATE = value);
    SERVER_STATE_STORE.subscribe(value => SERVER_STATE = value);

    onMount(() => {
        SERVER_STATE_STORE.set(INITIAL_SERVER_STATE);
        CLIENT_STATE_STORE.set(INITIAL_SERVER_STATE);
        players_store.set(initialPlayers)
    })

    socket.on('SERVER_STATE', data => {
        SERVER_STATE_STORE.set(data);
        CLIENT_STATE_STORE.set(data);
    })
</script>

<style lang="sass">
    main
        font-family: "IBM Plex Sans", sans-serif
        font-weight: 400
        text-align: center
        font-variant-numeric: normal
        height: calc(100vh - 6rem)
        padding: 3rem
        display: grid
        grid-template-rows: auto max-content
</style>

<main>
    <States/>


    {#if CLIENT_STATE === 'New Game'}
        <Players/>
    {/if}
    {#if CLIENT_STATE === 'Add Players'}
        <AddPlayers/>
    {/if}
    {#if SERVER_STATE === 'Started'}
        <Game/>
    {/if}

    <Controls/>
</main>
