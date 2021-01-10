<script lang="ts">
    import {CLIENT_STATE_STORE, SERVER_STATE_STORE} from "../stores";

    let CLIENT_STATE, SERVER_STATE;
    CLIENT_STATE_STORE.subscribe(value => CLIENT_STATE = value);
    SERVER_STATE_STORE.subscribe(value => SERVER_STATE = value);

    function reset() {
        fetch('/api/reset', {method: 'POST'})
    }
</script>

<style lang="sass">
    .states
        position: fixed
        top: 1rem
        left: 3rem
        right: 3rem
        display: flex
        justify-content: space-between
        //gap: 3rem
        font-size: 0.85rem

    span
        font-style: italic

    #reset
        cursor: pointer
</style>

<div class="states">
    <div>
<!--        CS: <span>{CLIENT_STATE}</span>-->
    </div>
    <div>
<!--        SS: <span>{SERVER_STATE}</span>-->
    </div>
    <div on:click={reset} id="reset">
        Reset
    </div>
</div>