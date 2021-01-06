<script lang="ts">

    import {CLIENT_STATE_STORE, SERVER_STATE_STORE} from "../../stores";

    let CLIENT_STATE, SERVER_STATE;
    SERVER_STATE_STORE.subscribe(value => SERVER_STATE = value);
    CLIENT_STATE_STORE.subscribe(value => CLIENT_STATE = value);

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
    }

    function startGame() {
        fetch('/api/start', {method: 'POST'})
    }

    function nextPlayer() {
        fetch('/api/next-player', {method: 'POST'})
    }

</script>

<style lang="sass">
    section
        display: flex
        justify-content: space-between
        margin: 0 0 0 14rem
</style>

<section id="controls">
    <div class="left">
        {#if SERVER_STATE === 'New Game'}
            <button on:click={switchMode}>
                Switch Mode
            </button>
        {/if}
        <button on:click={reset}>
            Reset
        </button>
    </div>

    <div class="right">
        {#if SERVER_STATE === 'New Game'}
            <button on:click={startGame}>
                Start Game
            </button>
        {/if}
        {#if SERVER_STATE === 'Started'}
            <button on:click={nextPlayer}>
                Next Player
            </button>
        {/if}
    </div>
</section>
