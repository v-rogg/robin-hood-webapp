<script lang="ts">
    import {onMount} from "svelte";
    import Players from "./routes/components/Players.svelte";
    import AddPlayers from "./routes/components/AddPlayers.svelte";
    import Game from "./routes/components/Game.svelte";
    import States from "./routes/components/States.svelte";
    import {io} from "socket.io-client";

    import {CLIENT_STATE_STORE, players_store, SERVER_STATE_STORE} from "./stores";

    const socket = io('ws://localhost:3000');

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

    function switchMode() {
        switch (CLIENT_STATE) {
            case 'New Game':
                CLIENT_STATE_STORE.set('Add Players');
                break;
            case 'Add Players':
                CLIENT_STATE_STORE.set('New Game');
                break;
        }
    }

    function reset() {
        fetch('/api/reset', {method: 'POST'})
            .then(result => result.json())
            .then(res => {
                // SERVER_STATE_STORE.set(res)
                // CLIENT_STATE_STORE.set(res)
            })
    }
</script>

<style lang="sass">
    main
        font-family: "IBM Plex Sans", sans-serif
        font-weight: 400
        text-align: center
        font-variant-numeric: normal
        gap: 3rem
        height: calc(100vh - 6rem)
        padding: 3rem

    .buttons
        display: flex
        gap: 1em
        margin-left: 13rem
        margin-top: -2rem
</style>

<main>
    <States/>
    <!--{SERVER_STATE}-->
    {#if CLIENT_STATE === 'New Game' || CLIENT_STATE === 'Started'}
        <Players/>
    {/if}
    {#if CLIENT_STATE === 'Add Players'}
        <AddPlayers/>
    {/if}

    <div class="buttons">
        {#if SERVER_STATE === 'New Game'}
            <button on:click={switchMode}>
                Switch Mode
            </button>
        {/if}
        <button on:click={reset}>
            Reset
        </button>
    </div>
</main>
