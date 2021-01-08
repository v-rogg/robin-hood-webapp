<script lang="ts">
    import {onMount} from "svelte";
    import Game from "./components/Game.svelte";
    import States from "./components/States.svelte";
    import NewGameLayout from "./layouts/_NewGame.svelte";
    import {io} from "socket.io-client";

    import {CLIENT_STATE_STORE, GAMEMODE_STORE, PLAYERS_STORE, SERVER_STATE_STORE} from "./stores";

    const socket = io('ws://192.168.178.48:3000');

    let CLIENT_STATE, SERVER_STATE;
    CLIENT_STATE_STORE.subscribe(value => CLIENT_STATE = value);
    SERVER_STATE_STORE.subscribe(value => SERVER_STATE = value);

    onMount(() => {
        SERVER_STATE_STORE.set(INITIAL_SERVER_STATE);
        CLIENT_STATE_STORE.set(INITIAL_SERVER_STATE);
        PLAYERS_STORE.set(INITIAL_PLAYERS);
        GAMEMODE_STORE.set(INITIAL_GAMEMODE);
    })

    socket.on('SERVER_STATE', data => {
        SERVER_STATE_STORE.set(JSON.parse(data));
        CLIENT_STATE_STORE.set(JSON.parse(data));
    })

    socket.on('players', data => {
        PLAYERS_STORE.set(JSON.parse(data))
    })

    socket.on('gamemode', data => {
        GAMEMODE_STORE.set(JSON.parse(data))
    })
</script>

<style lang="sass">
    robin
        display: block
        font-family: 'Rubik', sans-serif
        font-weight: 400
        text-align: center
        font-variant-numeric: normal
        padding: 5rem 0 5rem
</style>

<robin>
    <States/>


    {#if SERVER_STATE === 'New Game'}
        <NewGameLayout/>
    {/if}
    <!--{#if CLIENT_STATE === 'Add Players'}-->
<!--    {/if}-->
    {#if SERVER_STATE === 'Started'}
        <Game/>
    {/if}

</robin>
